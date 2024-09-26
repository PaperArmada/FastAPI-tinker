from fastapi import FastAPI, HTTPException
from models import User, UserCreate

app = FastAPI()

# In-memory "database"
users_db = []

# Init with a few users
users_db.append(User(id=1, name="John Doe", email="john@example.com", age=30))
users_db.append(User(id=2, name="Jane Smith", email="jane@example.com", age=25))

@app.get("/")
def read_root():
    return {"message": "Welcom to the FastAPI CRUD API!"}

@app.get("/users/", response_model=list[User])
def get_users():
    return users_db

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = next((user for user in users_db if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=User)
def create_user(user: UserCreate):
    new_id = len(users_db) + 1  # Placeholder assignment logic
    user_data = user.model_dump()
    user_data["id"] = new_id
    new_user = User(**user_data)
    users_db.append(new_user)
    return new_user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserCreate):
    user = next((user for user in users_db if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = user_update.name
    user.email = user_update.email
    user.age = user_update.age
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    user = next((user for user in users_db if user.id == user_id), None)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    users_db.remove(user)
    return {"detail": "User deleted"}