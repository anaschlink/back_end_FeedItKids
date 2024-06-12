from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.repositories import objetivos_repositories as crud
from src.schemas import objetivos_schema as schemas
from src.database.database import get_db

router = APIRouter()

@router.post("/objetivos/", response_model=schemas.Objetivos)
async def create_objetivos(objetivo: schemas.ObjetivosBase, db: Session = Depends(get_db)):
    try:
        return crud.create_objetivos(db=db, objetivos=objetivo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/objetivos/{id_objetivo}", response_model=schemas.Objetivos)
async def read_objetivo(id_objetivo: int, db: Session = Depends(get_db)):
    try:
        db_objetivo = crud.get_objetivo(db, id_objetivo=id_objetivo)
        if db_objetivo is None:
            raise HTTPException(status_code=404, detail="Objetivo not found")
        return db_objetivo
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/objetivos/", response_model=List[schemas.Objetivos])
async def read_objetivos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try: 
        objetivos = crud.get_objetivos(db, skip=skip, limit=limit)
        return objetivos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/objetivos/{id_objetivo}", response_model=schemas.Objetivos)
async def update_objetivo(id_objetivo: int, objetivo: schemas.ObjetivosUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_objetivo(db=db, id_objetivo=id_objetivo, objetivo=objetivo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/objetivos/{id_objetivo}")
async def delete_objetivo_completo(id_objetivo: int, db: Session = Depends(get_db)):
    return crud.delete_objetivos(db, id_objetivo)