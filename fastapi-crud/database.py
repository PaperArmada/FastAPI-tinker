from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(os.path.join(BASE_DIR, 'db')):
    os.makedirs(os.path.join(BASE_DIR, 'db'))

DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'db/test.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer)
