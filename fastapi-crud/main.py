from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal, User
from models import UserCreate, User as UserSchema

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcom to the FastAPI CRUD API!"}

@app.get("/users/", response_model=UserSchema)
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/users/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/users/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = user_update.name
    user.email = user_update.email
    user.age = user_update.age
    db.commit()
    db.refresh(user)
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}