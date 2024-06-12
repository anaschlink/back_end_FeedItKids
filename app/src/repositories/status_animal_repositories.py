from sched import scheduler
import time
from fastapi import BackgroundTasks, Depends, HTTPException
from psycopg2 import IntegrityError, OperationalError
import schedule
from sqlalchemy import func
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models import Animal_model as models
from src.models import status_alimento_model
from src.schemas import status_animal_schema as schemas

# CRUD BANCO DE DADOS


def get_status_animal(db: Session, id_usuario: int):
    return db.query(models.StatusAnimal).filter(models.StatusAnimal.id_usuario == id_usuario).first()


def get_status_animals(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.StatusAnimal).offset(skip).limit(limit).all()

def create_status_animal(db: Session, status_animal: schemas.StatusAnimalBase):

    db_status_animal = models.StatusAnimal(
        id_usuario = status_animal.id_usuario,
        alimentacao_saudavel=status_animal.alimentacao_saudavel,
        energia =status_animal.energia,
        forca=status_animal.forca,
        felicidade =status_animal.felicidade
    )
    db.add(db_status_animal)
    db.commit()
    db.refresh(db_status_animal)
    return db_status_animal


def update_status_animal(db: Session, status_animal_id: int, status_animal_update: schemas.StatusAnimalUpdate):
    db_status_animal = get_status_animal(db, status_animal_id)
    if not db_status_animal:
        return None
    for field, value in status_animal_update.model_dump(exclude_unset=True).items():
        if field not in ("id", "id_status", "id_usuario"):
            setattr(db_status_animal, field, value)

    db.commit()
    db.refresh(db_status_animal)
    return db_status_animal


def delete_status_animal(db: Session, status_animal_id: int):
    db_status_animal = get_status_animal(db, status_animal_id)
    if not db_status_animal:
        return {"message": "StatusAnimal not found"}
    db.delete(db_status_animal)
    db.commit()
    return {"message": "StatusAnimal deleted successfully"}

def formatar_valor(valor):
    tolerancia = 1e-10  # Define uma tolerância para considerar valores muito próximos de zero como zero
    if abs(valor) < tolerancia:
        return 0
    else:
        return valor


def update_status_animal(db: Session, id_status: int, id_usuario: int):

    # Buscar o registro de ConsumoAnimal inserido recentemente
    consumo_animal = db.query(models.ConsumoAnimal).filter(
        models.ConsumoAnimal.id_status_alimento == id_status,
        models.ConsumoAnimal.id_usuario == id_usuario
    ).order_by(models.ConsumoAnimal.id_consumo.desc()).first()
    
    if consumo_animal is None:
        raise HTTPException(status_code=404, detail="ConsumoAnimal not found")
    
    # Buscar os atributos do AlimentoStatus correspondente usando o id_status_alimento
    status_alimento = db.query(status_alimento_model.StatusAlimento).filter(status_alimento_model.StatusAlimento.id_status_alimento == consumo_animal.id_status_alimento).first()
    if status_alimento is None:
        raise HTTPException(status_code=404, detail="StatusAlimento not found")
    
    # Buscar o registro de StatusAnimal usando o id_usuario do ConsumoAnimal
    status_animal = db.query(models.StatusAnimal).filter(models.StatusAnimal.id_usuario == consumo_animal.id_usuario).first()
    
    # Se não existir um registro de StatusAnimal, criar um novo
    if status_animal is None:
        status_animal = models.StatusAnimal(
            id_usuario=consumo_animal.id_usuario,
            alimentacao_saudavel=0.0,
            energia=0.0,
            forca=0.0,
            felicidade=0.0
        )
        db.add(status_animal)
        db.commit()
        db.refresh(status_animal)
        print(f"insert_into_consumo_animal: {status_animal}")
    
    # Atualizar os valores de StatusAnimal com os valores de StatusAlimento, respeitando o limite de 10

    status_animal.alimentacao_saudavel = formatar_valor(min(status_animal.alimentacao_saudavel + status_alimento.alimentacao_saudavel, 10.0))
    status_animal.energia = formatar_valor(min(status_animal.energia + status_alimento.energia, 10.0))
    status_animal.forca = formatar_valor(min(status_animal.forca + status_alimento.forca, 10.0))
    status_animal.felicidade = formatar_valor(min(status_animal.felicidade + status_alimento.felicidade, 10.0))

    
    # Commitar as mudanças no banco de dados
    db.commit()
    db.refresh(status_animal)
    
    print(f"update_status_animal: {status_animal}")
    return status_animal

def update_status_animal_attributes(db: Session):
    # Buscar todos os registros na tabela StatusAnimal
    status_animais = db.query(models.StatusAnimal).all()
    
    # Iterar sobre cada registro e atualizar os valores
    for status_animal in status_animais:
        # Atualizar os valores de acordo com a lógica desejada
        status_animal.alimentacao_saudavel = formatar_valor(round(min(status_animal.alimentacao_saudavel + (0.1 if status_animal.alimentacao_saudavel < 0 else -0.1), 10.0), 2))

        status_animal.energia = formatar_valor(round(min(status_animal.energia + (0.1 if status_animal.energia < 0 else -0.1), 10.0), 2))

        status_animal.forca = formatar_valor(round(min(status_animal.forca + (0.1 if status_animal.forca < 0 else -0.1), 10.0), 2))
        status_animal.felicidade = formatar_valor(round(min(status_animal.felicidade + (0.1 if status_animal.felicidade < 0 else -0.1), 10.0), 2))

    print("tarefa agendada atualização status")
    # Confirmar as alterações no banco de dados
    db.add(status_animal)
    db.commit()
    db.refresh(status_animal)
    return status_animal



# Agendar a função de atualização
def agendar_atualizacao(db: Session = Depends(get_db)):
    # Agendar a função para ser executada a cada 1 minuto
    schedule.every(30).minutes.do(update_status_animal_attributes, db)

# Função de background para executar as tarefas agendadas
def executar_tarefas_agendadas(db:Session = Depends(get_db)):
    while True:
        # Executar as tarefas agendadas
        schedule.run_pending()
        # Aguardar 1 segundo antes de verificar novamente
        time.sleep(1)

