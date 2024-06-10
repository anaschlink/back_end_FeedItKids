from fastapi import HTTPException
from psycopg2 import OperationalError
from sqlalchemy.orm import Session
from src.models import Objetivo_model as models
from src.schemas import objetivos_schema as schemas

# CRUD Objetivos

def get_objetivo(db: Session, id_objetivo: int):
    return db.query(models.Objetivos).filter(models.Objetivos.id_objetivo == id_objetivo).first()

def get_objetivos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Objetivos).offset(skip).limit(limit).all()

def create_objetivos(db:Session, objetivos:schemas.ObjetivosBase):
    db_objetivos = models.Objetivos(
        descricao = objetivos.descricao,
        pontuacao = objetivos.pontuacao,
    )
    db.add(db_objetivos)
    db.commit()
    db.refresh(db_objetivos)
    return db_objetivos

def update_objetivo(db: Session, id_objetivo: int, objetivo: schemas.ObjetivosUpdate):
    db_objetivo = db.query(models.Objetivos).filter(models.Objetivos.id_objetivo == id_objetivo).first()
    if db_objetivo:
        for key, value in objetivo.model_dump(exclude_unset=True).items():
            setattr(db_objetivo, key, value)
        db.commit()
        db.refresh(db_objetivo)
    return db_objetivo

def delete_objetivos(db: Session, id_objetivo: int):
    db_objetivos = db.query(models.Objetivos).filter(models.Objetivos.id_objetivo == id_objetivo).first()
    if  db_objetivos:
        db.delete( db_objetivos)
        db.commit()
        return {"message":"Objetivo deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Objetivo  not found")
    
# Funções baseadas no objetivo

def get_objetivos_status_false(db:Session):
    try:
        return db.query(models.Objetivos).filter(models.Objetivos.status == False).all()
    except OperationalError as e:
        raise Exception(f"Database error: {str(e)}") from e   
    
def update_objetivo_status(db: Session, id_objetivo: int, status: bool):
    try:
        objetivo = db.query(models.Objetivos).filter(models.Objetivos.id_objetivo == id_objetivo).one_or_none()
        if objetivo:
            objetivo.status = status
            db.commit()
            db.refresh(objetivo)
            return objetivo
        else:
            raise HTTPException(status_code=404, detail="Objetivo não encontrado!")
    except OperationalError as e:
        raise Exception(f"Database error: {str(e)}") from e
    

