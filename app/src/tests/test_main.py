import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from back_end.src.database.database import Base, get_db
from back_end.main import app

from dotenv import load_dotenv

load_dotenv()

db_password = os.getenv("SENHA_BANCO")

DATABASE_URL = f"postgresql://avnadmin:{db_password}@pg-25cb39a-abnschlink-031a.h.aivencloud.com:22352/db_fitKids?sslmode=require"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_usuario(client):
    response = client.post("/usuarios/", json={
        "email_usuario": "test@example.com",
        "nome": "Test User",
        "senha": "password123@A",
        "papel": "admin",
        "id_animal": None
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email_usuario"] == "test@example.com"
    assert data["nome"] == "Test User"
    assert "id_usuario" in data

def test_read_usuarios(client):
    response = client.get("/usuarios/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_usuario(client):
    response = client.get("/usuarios/1")
    assert response.status_code == 200
    data = response.json()
    assert data["email_usuario"] == "test@example.com"
    assert data["nome"] == "Test User"

def test_update_usuario(client):
    response = client.put("/usuarios/1", json={
        "email_usuario": "updated@example.com",
        "nome": "Updated User",
        "senha": "newpassword123",
        "papel": "user",
        "id_animal": None
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email_usuario"] == "updated@example.com"
    assert data["nome"] == "Updated User"

def test_delete_usuario(client):
    response = client.delete("/usuarios/1")
    assert response.status_code == 200
    data = response.json()
    assert data["email_usuario"] == "updated@example.com"
