from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_items():
    r = client.get("/items/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 2


def test_get_item():
    r = client.get("/items/1")
    assert r.status_code == 200
    assert r.json()["id"] == 1


def test_get_item_not_found():
    r = client.get("/items/9999")
    assert r.status_code == 404


def test_create_item():
    payload = {"name": "Test Item", "price": 5.50}
    r = client.post("/items/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 5.50


def test_delete_item():
    r = client.delete("/items/2")
    assert r.status_code == 204
