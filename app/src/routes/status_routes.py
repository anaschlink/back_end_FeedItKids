from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models import status_alimento_model as models
from src.repositories import status_repositories as crud
from src.schemas import status_schema as schemas
from src.database.database import get_db

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/status/", response_model=List[schemas.StatusResponse])
def get_status_list(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    statuses = crud.get_status_list(db, skip=skip, limit=limit)
    return statuses

@router.get("/status/{id_status}", response_model=schemas.StatusResponse)
def get_status(id_status: int, db: Session = Depends(get_db)):
    status = crud.get_status(db, id_status)
    if status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return status

@router.get("/status/{grupo_alimento}", response_model=int)
def get_status_by_group(grupo_alimento: str, db: Session = Depends(get_db)):
    id_status = crud.get_status_by_grupo_alimento(db, grupo_alimento)
    if id_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return id_status

@router.get("/status/{grupo_alimento}", response_model=schemas.StatusResponse)
def get_status_by_group(grupo_alimento: str, db: Session = Depends(get_db)):
    status_alimento = crud.get_status_by_grupo_alimento(db, grupo_alimento)
    if status_alimento is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return status_alimento


@router.put("/status/{id_status}", response_model=schemas.StatusResponse)
def update_status(id_status: int, status_update: schemas.StatusBase, db: Session = Depends(get_db)):
    updated_status = crud.update_status(db=db, id_status=id_status, status_update=status_update)
    if updated_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return updated_status

@router.delete("/status/{id_status}", response_model=schemas.StatusResponse)
def delete_status(id_status: int, db: Session = Depends(get_db)):
    deleted_status = crud.delete_status(db=db, id_status=id_status)
    if deleted_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return deleted_status
