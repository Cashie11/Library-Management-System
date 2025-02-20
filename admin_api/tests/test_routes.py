# admin_api/tests/test_routes.py
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app  # Make sure your app is imported correctly

client = TestClient(app)

def test_add_book():
    # Prepare the request data according to your BookCreate model
    payload = {
        "title": "Test Book",
        "publisher": "Test Publisher",
        "category": "Test Category"
    }
    response = client.post("/books", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    # Verify the response contains the expected fields
    assert data["title"] == payload["title"]
    # Add more assertions as needed
