# Multimodal Input API

A FastAPI-based REST API for handling multiple input modalities including text, images, audio, and video.

## Features

- **Text Processing**: Handle text inputs with metadata
- **Image Processing**: Accept and process image uploads
- **Audio Processing**: Handle audio file uploads with optional transcription
- **Video Processing**: Process video file uploads
- **Multimodal Processing**: Handle multiple input types simultaneously
- **CORS Enabled**: Ready for cross-origin requests
- **Auto-generated API Documentation**: Interactive docs at `/docs`

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Garrettc123/multimodal-input-api.git
cd multimodal-input-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

```bash
python multimodal_input_api.py
```

Or using uvicorn directly:
```bash
uvicorn multimodal_input_api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### Health Check
```bash
GET /health
```

#### Root Information
```bash
GET /
```
Returns API information and available endpoints.

#### Text Processing
```bash
POST /text
Content-Type: application/json

{
  "text": "Your text here",
  "metadata": {"optional": "metadata"}
}
```

#### Image Processing
```bash
POST /image
Content-Type: multipart/form-data

file: [image file]
description: "Optional description"
```

#### Audio Processing
```bash
POST /audio
Content-Type: multipart/form-data

file: [audio file]
transcription: "Optional transcription"
```

#### Video Processing
```bash
POST /video
Content-Type: multipart/form-data

file: [video file]
description: "Optional description"
```

#### Multimodal Processing
```bash
POST /multimodal
Content-Type: multipart/form-data

text: "Optional text"
image: [optional image file]
audio: [optional audio file]
video: [optional video file]
```

## Example Usage

### Using cURL

```bash
# Text input
curl -X POST "http://localhost:8000/text" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, World!"}'

# Image upload
curl -X POST "http://localhost:8000/image" \
  -F "file=@path/to/image.jpg" \
  -F "description=Sample image"

# Multimodal input
curl -X POST "http://localhost:8000/multimodal" \
  -F "text=Hello" \
  -F "image=@path/to/image.jpg" \
  -F "audio=@path/to/audio.mp3"
```

### Using Python

```python
import requests

# Text processing
response = requests.post(
    "http://localhost:8000/text",
    json={"text": "Hello, World!", "metadata": {"source": "test"}}
)
print(response.json())

# Image processing
with open("image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/image",
        files={"file": f},
        data={"description": "Test image"}
    )
print(response.json())
```

## Interactive API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Response Format

All endpoints return a JSON response with the following structure:

```json
{
  "status": "success",
  "message": "Description of the operation",
  "data": {
    // Endpoint-specific data
  }
}
```

## Error Handling

Errors return appropriate HTTP status codes with details:

```json
{
  "detail": "Error description"
}
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black multimodal_input_api.py
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Garrettc123
