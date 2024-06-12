import datetime
from fastapi import HTTPException
import pytz
from sqlalchemy.orm import Session
from src.models import Objetivo_model as models 
from src.schemas import objetivo_completo_schema as schemas
from datetime import datetime
# CRUD objetivos completo

utc_timezone = pytz.utc

def get_objetivo_completo(db: Session, id_objetivo: int, id_usuario: int):
    return db.query(models.ObjetivoCompleto).filter(
        models.ObjetivoCompleto.id_objetivo == id_objetivo,
        models.ObjetivoCompleto.id_usuario == id_usuario
    ).first()

def get_objetivo_completo_by_usuario(db: Session, id_usuario: int, skip: int = 0, limit: int = 10):
    return db.query(models.ObjetivoCompleto).filter(
        models.ObjetivoCompleto.id_usuario == id_usuario
    ).offset(skip).limit(limit).all()

def get_objetivos_completo(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ObjetivoCompleto).offset(skip).limit(limit).all()


def create_objetivo_completo(db: Session, objetivo_completo: schemas.ObjetivoCompletoCreate):
    db_objetivo_completo = models.ObjetivoCompleto(
        id_usuario=objetivo_completo.id_usuario,
        id_objetivo=objetivo_completo.id_objetivo,
        pontuacao=objetivo_completo.pontuacao,
        created_at=objetivo_completo.created_at or datetime.now(utc_timezone),
        updated_at=objetivo_completo.updated_at or datetime.now(utc_timezone)
    )
    db.add(db_objetivo_completo)
    db.commit()
    db.refresh(db_objetivo_completo)
    return db_objetivo_completo


def update_objetivo_completo(db: Session, id_objetivo: int, objetivo: schemas.ObjetivoCompletoUpdate):
    db_objetivo_completo = db.query(models.ObjetivoCompleto).filter(models.ObjetivoCompleto.id_objetivo == id_objetivo).first()
    if db_objetivo_completo:
        for key, value in objetivo.model_dump(exclude_unset=True).items():
            setattr(db_objetivo_completo, key, value)
        db.commit()
        db.refresh(db_objetivo_completo)
    return db_objetivo_completo


def delete_objetivo_completo(db: Session, id_objetivo: int, id_usuario: int):
    objetivo_completo = db.query(models.ObjetivoCompleto).filter(
        models.ObjetivoCompleto.id_objetivo == id_objetivo,
        models.ObjetivoCompleto.id_usuario == id_usuario
    ).first()
    
    if objetivo_completo:
        db.delete(objetivo_completo)
        db.commit()
        return {"message": "Objetivo Completo deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Objetivo Completo not found")

