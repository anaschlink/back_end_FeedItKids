import pandas as pd
from sqlalchemy import extract
from sqlalchemy.orm import Session
from src.models import Animal_model as models
from src.schemas import consumo_animal_schema as schemas


# CRUD BANCO DE DADOS 


def get_consumo(db: Session, id_consumo: int):
    return db.query(models.ConsumoAnimal).filter(models.ConsumoAnimal.id_consumo == id_consumo).first()

def get_consumos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ConsumoAnimal).offset(skip).limit(limit).all()


def create_consumo(db: Session, consumo_animal: schemas.ConsumoAnimalBase):
    db_consumo_animal = models.ConsumoAnimal(
        id_usuario=consumo_animal.id_usuario,
        id_status_alimento=consumo_animal.id_status_alimento,
        alimento=consumo_animal.alimento
    )
    db.add(db_consumo_animal)
    db.commit()
    db.refresh(db_consumo_animal)
    return db_consumo_animal

def update_consumo(db: Session, id_consumo: int, consumo_update: schemas.ConsumoAnimalBase) -> models.ConsumoAnimal:
    db_consumo_animal = db.query(models.ConsumoAnimal).filter(models.ConsumoAnimal.id_consumo == id_consumo).first()

    if not db_consumo_animal:
        return None

    for field, value in consumo_update.dict(exclude_unset=True).items():
        setattr(db_consumo_animal, field, value)

    db.commit()
    db.refresh(db_consumo_animal)
    return db_consumo_animal


def delete_consumo_animal(db: Session, id_consumo: int):
    db_consumo_animal = get_consumo(db, id_consumo)
    if not db_consumo_animal:
        return None
    db.delete(db_consumo_animal)
    db.commit()
    return db_consumo_animal

def create_consumo_by_id_status(db: Session, consumo_animal: schemas.ConsumoRequest, id_status:int):
    db_consumo_animal = models.ConsumoAnimal(
        id_usuario=consumo_animal.id_usuario,
        id_status_alimento=id_status,
        alimento = consumo_animal.alimento
    )
    db.add(db_consumo_animal)
    db.commit()
    db.refresh(db_consumo_animal)
    return db_consumo_animal

# Gráfico médico

def get_consumo_animal_dataframe(db: Session, ano: int, mes: int):
    # Filtrar os registros da tabela consumo_animal pelo ano e mês
    consumos = db.query(models.ConsumoAnimal).filter(
        extract('year', models.ConsumoAnimal.created_at) == ano,
        extract('month', models.ConsumoAnimal.created_at) == mes
    ).all()

    # Criar uma lista de dicionários com os atributos desejados
    dados = [{
        "alimento": consumo.alimento,
        "qtd": consumo.qtd,
        "created_at": consumo.created_at,
        "updated_at": consumo.updated_at
    } for consumo in consumos]

    # Criar o DataFrame a partir da lista de dicionários
    df = pd.DataFrame(dados)

    return df