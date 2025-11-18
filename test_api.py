#!/usr/bin/env python3
"""Basic tests for Multimodal Input API"""

import pytest
from fastapi.testclient import TestClient
from multimodal_input_api import app
import io
from PIL import Image

client = TestClient(app)


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Multimodal Input API" in data["message"]


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_text_input():
    """Test text input processing"""
    response = client.post(
        "/text",
        json={"text": "Test message", "metadata": {"test": True}}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data


def test_image_upload():
    """Test image upload processing"""
    # Create test image
    img = Image.new('RGB', (100, 100), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    response = client.post(
        "/image",
        files={"file": ("test.png", img_bytes, "image/png")},
        data={"description": "Test"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
