from io import StringIO
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import IntegrityError, OperationalError
from sqlalchemy.orm import Session
from src.models import Animal_model as models

from src.repositories import consumo_animal_repositories as crud
from src.schemas import consumo_animal_schema as schemas
from src.database.database import get_db

router = APIRouter()

@router.post("/consumo", response_model=schemas.ConsumoAnimal)
def create_consumo(consumo: schemas.ConsumoAnimalBase, db: Session = Depends(get_db)):
    try:
        return crud.create_consumo(db=db, consumo_animal=consumo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/consumo/{id_consumo}", response_model=schemas.ConsumoAnimalBase)
def read_consumo(id_consumo: int, db: Session = Depends(get_db)):
    db_consumo = crud.get_consumo(db, id_consumo=id_consumo)
    if db_consumo is None:
        raise HTTPException(status_code=404, detail="consumo not found")
    return db_consumo

@router.get("/consumo", response_model=List[schemas.ConsumoAnimal])
def read_consumo(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    consumo = crud.get_consumos(db, skip=skip, limit=limit)
    return consumo

# @router.put("/consumo/{id_consumo}", response_model=schemas.ConsumoAnimal)
# def update_consumo(id_consumo: int, consumo: schemas.ConsumoAnimalBase, db: Session = Depends(get_db)):
#     return crud.update_consumo(db=db, id_consumo=id_consumo, consumo=consumo)

@router.delete("/consumo/{id_consumo}", response_model=schemas.ConsumoAnimal)
def delete_consumo(id_consumo: int, db: Session = Depends(get_db)):
    return crud.delete_consumo_animal(db=db, id_consumo=id_consumo)


@router.get("/consumo_animal/")
async def get_consumo_animal(ano: int, mes: int, db: Session = Depends(get_db)):
    try:
        # Obter o DataFrame filtrado pelo ano e mês
        df = crud.get_consumo_animal_dataframe(db, ano, mes)

        if df.empty:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para o ano e mês especificados.")

        # Converter o DataFrame para CSV para enviar como resposta
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_str = csv_buffer.getvalue()

        return csv_str
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))