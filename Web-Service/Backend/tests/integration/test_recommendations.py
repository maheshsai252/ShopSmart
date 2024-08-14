from fastapi.testclient import TestClient
import sys
import os

from main import app

client = TestClient(app)

def test_recommendations():
    payload = {"user_id": 1}
    response = client.get("/user-recommendations/",  params=payload)
    assert len(response.json()['response']) == 3


