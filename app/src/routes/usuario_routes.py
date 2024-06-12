from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas import usuario_schema as schemas
from src.repositories import usuario_repositories as crud
from typing import Annotated
from src.database.database import get_db

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

# Rotas da API

@router.post("/usuarios/", response_model=schemas.UsuarioBase)
async def create_usuario(usuario: schemas.UsuarioCreate, db: db_dependency):
    try:
        return crud.create_usuario(db=db, usuario=usuario)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/usuarios/{id_usuario}", response_model=schemas.UsuarioResponse)
async def read_user(id_usuario: int, db: db_dependency):
    db_usuario = crud.get_usuario(db, id_usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_usuario
