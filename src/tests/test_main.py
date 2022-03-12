from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/test")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["result"] == "success"
    assert response_json["message"] == "It worked just now!"
