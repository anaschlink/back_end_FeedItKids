import pandas as pd
import matplotlib as plt
from sqlalchemy import extract
from sqlalchemy.orm import Session
from src.models import Animal_model as models
from src.models import status_alimento_model as status
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

def get_grupo_alimento_por_id(db: Session, id_status_alimento: int):
    # Consulta o banco de dados para obter o grupo de alimento pelo id_status_alimento
    status_alimento = db.query(status.StatusAlimento).filter_by(id_status_alimento=id_status_alimento).first()
    
    # Verifica se o status_alimento foi encontrado
    if status_alimento:
        return status_alimento.grupo_alimento
    else:
        return None  # Retorna None se não encontrar o status_alimento

def get_id_alimento_por_nome(db: Session, nome_alimento: str):
    # Consulta o banco de dados para obter o ID do alimento pelo nome
    alimento = db.query(status.StatusAlimento).filter_by(nome=nome_alimento).first()
    
    # Verifica se o alimento foi encontrado
    if alimento:
        return alimento.id_status_alimento
    else:
        return None  # Retorna None se não encontrar o alimento

def get_consumo_animal_dataframe(db: Session, ano: int):
    # Filtrar os registros da tabela consumo_animal pelo ano
    consumos = db.query(models.ConsumoAnimal).filter(
        extract('year', models.ConsumoAnimal.created_at) == ano,
    ).all()

    # Criar uma lista de dicionários com os atributos desejados
    dados = []
    for consumo in consumos:
        grupo_alimento = get_grupo_alimento_por_id(db, consumo.id_status_alimento)
        dados.append({
            "qtd": consumo.qtd,
            "alimento":consumo.alimento,
            "grupo_alimento": grupo_alimento,
            "created_at": consumo.created_at,
            "updated_at": consumo.updated_at
        })

    # Criar o DataFrame a partir da lista de dicionários
    df = pd.DataFrame(dados)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])

    return df

# criação do gráfico 


