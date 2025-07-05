from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_login_success():
    response = client.post("/auth/login", json={"username": "admin", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure():
    response = client.post("/auth/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401

def test_rate_limit_login():
    headers = {"X-Forwarded-For": "5.5.5.5"}
    for _ in range(5):
        res = client.post("/auth/login", json={"username": "admin", "password": "password"}, headers=headers)
        assert res.status_code == 200

    # 6. request bi trebao pasti
    res = client.post("/auth/login", json={"username": "admin", "password": "password"}, headers=headers)
    assert res.status_code == 429
    assert res.json()["detail"] == "Rate limit exceeded. Try again later."
