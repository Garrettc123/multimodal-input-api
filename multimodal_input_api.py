from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import base64
import io
from PIL import Image
import json

app = FastAPI(
    title="Multimodal Input API",
    description="API for handling multiple input types: text, images, audio, and video",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str
    metadata: Optional[dict] = None

class MultimodalResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None

@app.get("/")
async def root():
    return {
        "message": "Multimodal Input API",
        "version": "1.0.0",
        "endpoints": {
            "/text": "POST - Process text input",
            "/image": "POST - Process image input",
            "/audio": "POST - Process audio input",
            "/video": "POST - Process video input",
            "/multimodal": "POST - Process multiple input types simultaneously"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/text", response_model=MultimodalResponse)
async def process_text(input_data: TextInput):
    """Process text input"""
    try:
        return MultimodalResponse(
            status="success",
            message="Text processed successfully",
            data={
                "input_type": "text",
                "text_length": len(input_data.text),
                "word_count": len(input_data.text.split()),
                "metadata": input_data.metadata
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/image", response_model=MultimodalResponse)
async def process_image(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
):
    """Process image input"""
    try:
        # Read image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Get image info
        image_info = {
            "filename": file.filename,
            "format": image.format,
            "mode": image.mode,
            "size": image.size,
            "width": image.width,
            "height": image.height,
            "description": description
        }
        
        return MultimodalResponse(
            status="success",
            message="Image processed successfully",
            data={
                "input_type": "image",
                **image_info
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/audio", response_model=MultimodalResponse)
async def process_audio(
    file: UploadFile = File(...),
    transcription: Optional[str] = Form(None)
):
    """Process audio input"""
    try:
        # Read audio file
        contents = await file.read()
        file_size = len(contents)
        
        audio_info = {
            "filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": file_size,
            "transcription": transcription
        }
        
        return MultimodalResponse(
            status="success",
            message="Audio processed successfully",
            data={
                "input_type": "audio",
                **audio_info
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/video", response_model=MultimodalResponse)
async def process_video(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
):
    """Process video input"""
    try:
        # Read video file
        contents = await file.read()
        file_size = len(contents)
        
        video_info = {
            "filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": file_size,
            "description": description
        }
        
        return MultimodalResponse(
            status="success",
            message="Video processed successfully",
            data={
                "input_type": "video",
                **video_info
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/multimodal", response_model=MultimodalResponse)
async def process_multimodal(
    text: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    audio: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None)
):
    """Process multiple input types simultaneously"""
    try:
        results = {
            "inputs_received": []
        }
        
        if text:
            results["inputs_received"].append("text")
            results["text"] = {
                "length": len(text),
                "word_count": len(text.split())
            }
        
        if image:
            results["inputs_received"].append("image")
            img_contents = await image.read()
            img = Image.open(io.BytesIO(img_contents))
            results["image"] = {
                "filename": image.filename,
                "size": img.size
            }
        
        if audio:
            results["inputs_received"].append("audio")
            audio_contents = await audio.read()
            results["audio"] = {
                "filename": audio.filename,
                "size_bytes": len(audio_contents)
            }
        
        if video:
            results["inputs_received"].append("video")
            video_contents = await video.read()
            results["video"] = {
                "filename": video.filename,
                "size_bytes": len(video_contents)
            }
        
        return MultimodalResponse(
            status="success",
            message=f"Processed {len(results['inputs_received'])} input types",
            data=results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
