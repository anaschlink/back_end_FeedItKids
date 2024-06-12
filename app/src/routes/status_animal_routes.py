from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from src.repositories import status_animal_repositories as crud
from src.schemas import status_animal_schema as schemas
from src.database.database import get_db

router = APIRouter()

@router.post("/status_animal/", response_model=schemas.StatusAnimalBase)
def create_status_animal(status_animal: schemas.StatusAnimalBase, db: Session = Depends(get_db)):
    try:
        return crud.create_status_animal(db=db, status_animal=status_animal)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/status_animal/{id_usuario}", response_model=schemas.StatusAnimal)
def get_status_by_id_animal(id_usuario: int, db: Session = Depends(get_db)):
    db_status_animal = crud.get_status_animal(db, id_usuario=id_usuario)
    if db_status_animal is None:
        raise HTTPException(status_code=404, detail="StatusAnimal not found")
    return db_status_animal

@router.get("/status_animal/", response_model=List[schemas.StatusAnimal])
def read_status_animal(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    status_animal = crud.get_status_animals(db, skip=skip, limit=limit)
    return status_animal


@router.get("/iniciar_agendamento")
async def iniciar_agendamento(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Agendar a função de atualização
    crud.agendar_atualizacao(db)
    # Adicionar a função de execução de tarefas agendadas ao plano de fundo
    background_tasks.add_task(crud.executar_tarefas_agendadas, db)
    return {"message": "Agendamento iniciado com sucesso!"}