from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.repositories import objetivo_completo_repositories as crud
from src.schemas import objetivo_completo_schema as schemas
from src.database.database import get_db

router = APIRouter()

@router.post("/objetivo_completo/", response_model=schemas.ObjetivoCompleto)
async def create_objetivo_completo(objetivo_completo: schemas.ObjetivoCompletoCreate, db: Session = Depends(get_db)):
    db_objetivo_completo = crud.create_objetivo_completo(db=db, objetivo_completo=objetivo_completo)
    if db_objetivo_completo is None:
        raise HTTPException(status_code=400, detail="Error creating objetivo completo")
    return db_objetivo_completo

@router.get("/objetivoCompleto/{id_objetivo}/{id_usuario}", response_model=schemas.ObjetivoCompleto)
async def read_objetivo_completo(id_objetivo: int, id_usuario: int, db: Session = Depends(get_db)):
    objetivo_completo = crud.get_objetivo_completo(db, id_objetivo, id_usuario)
    if objetivo_completo is None:
        raise HTTPException(status_code=404, detail="Objetivo Completo not found")
    return objetivo_completo


@router.get("/objetivoCompleto/{id_usuario}", response_model=List[schemas.ObjetivoCompleto])
async def read_objetivo_completo_by_usuario(id_usuario: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        objetivos_completos = crud.get_objetivo_completo_by_usuario(db, id_usuario=id_usuario, skip=skip, limit=limit)
        if not objetivos_completos:
            raise HTTPException(status_code=404, detail="Objetivos Completos not found for this user")
        return objetivos_completos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/objetivoCompleto/{id_objetivo}",response_model=schemas.ObjetivoCompleto)
async def update_objetivo(id_objetivo: int, objetivo: schemas.ObjetivoCompletoUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_objetivo_completo(db=db, id_objetivo = id_objetivo, objetivo = objetivo)
    except Exception as e :
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/objetivoCompleto/{id_objetivo}/{id_usuario}")
async def delete_objetivo_completo(id_objetivo: int, id_usuario: int, db: Session = Depends(get_db)):
    return crud.delete_objetivo_completo(db, id_objetivo, id_usuario)