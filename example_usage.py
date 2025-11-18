#!/usr/bin/env python3
"""Example usage of the Multimodal Input API"""

import requests
import json

API_BASE = "http://localhost:8000"


def test_text_input():
    """Test text input endpoint"""
    print("Testing text input...")
    
    response = requests.post(
        f"{API_BASE}/text",
        json={
            "text": "This is a test message for the multimodal API",
            "metadata": {"source": "example", "timestamp": "2025-11-17"}
        }
    )
    
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()


def test_image_upload():
    """Test image upload endpoint"""
    print("Testing image upload...")
    
    # Create a test image
    from PIL import Image
    import io
    
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    response = requests.post(
        f"{API_BASE}/image",
        files={"file": ("test.png", img_bytes, "image/png")},
        data={"description": "Test image"}
    )
    
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()


def test_health():
    """Test health check endpoint"""
    print("Testing health check...")
    
    response = requests.get(f"{API_BASE}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()


if __name__ == "__main__":
    print("=" * 50)
    print("Multimodal Input API - Example Usage")
    print("=" * 50)
    print()
    
    try:
        test_health()
        test_text_input()
        test_image_upload()
        
        print("All tests completed successfully!")
        print("Visit http://localhost:8000/docs for interactive API documentation")
        
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API")
        print("Make sure the server is running: python multimodal_input_api.py")
    except Exception as e:
        print(f"Error: {e}")
