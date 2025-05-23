from fastapi.testclient import TestClient
from serving.main import app

client = TestClient(app)

def test_status():
    res = client.get("/status")
    assert res.status_code == 200
    assert "status" in res.json()

def test_model_post():
    res = client.post("/model", json={"model_id": "gpt2"})
    assert res.status_code == 200
