from sqlalchemy.orm import Session
from src.models import status_alimento_model as models
from src.schemas import status_schema as schemas

# CRUD BANCO DE DADOS

def get_status_by_grupo_alimento(db: Session, grupo_alimento: str):
    return db.query(models.StatusAlimento).filter(models.StatusAlimento.grupo_alimento == grupo_alimento).first()

def get_status(db: Session, id_status_alimento: int):

    return db.query(models.StatusAlimento).filter(models.StatusAlimento.id_status_alimento == id_status_alimento).first()


def get_status_list(db: Session, skip: int = 0, limit: int = 10):

    return db.query(models.StatusAlimento).offset(skip).limit(limit).all()


def create_status_alimento(db: Session, status_alimento: schemas.StatusBase):
    db_status_alimento = models.StatusAlimento(
        grupo_alimento=status_alimento.grupo_alimento,
        alimentacao_saudavel=status_alimento.alimentacao_saudavel,
        energia=status_alimento.energia,
        forca=status_alimento.forca,
        felicidade=status_alimento.felicidade
    )
    db.add(db_status_alimento)
    db.commit()
    db.refresh(db_status_alimento)
    return db_status_alimento

def update_status(db: Session, id_status: str, status_update: schemas.StatusBase):
    db_status = get_status(db, id_status)
    if not db_status:
        return None

    for field, value in status_update.model_dump(exclude_unset=True).items():
        if not hasattr(models.StatusAlimento, field): 
            continue  
        setattr(db_status, field, value)

    db.commit()
    db.refresh(db_status)
    return db_status


def delete_status(db: Session, id_status: str):

    db_status = get_status(db, id_status)
    if not db_status:
        return None
    db.delete(db_status)
    db.commit()
    return db_status
