from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcom to the FastAPI CRUD API!"}

def test_get_all_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) > 0  # Assuming initial users are present

def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"

def test_create_user():
    new_user = {"name": "Test User", "email": "test@example.com", "age": 35}
    response = client.post("/users/", json=new_user)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_user["name"]
    assert data["email"] == new_user["email"]
    assert data["age"] == new_user["age"]

def test_update_user():
    update_data = {"name": "Updated User", "email": "updated@example.com", "age": 36}
    response = client.put("/users/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["email"] == update_data["email"]
    assert data["age"] == update_data["age"]

def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted"}

    # Verify user was deleted
    response = client.get("/users/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}