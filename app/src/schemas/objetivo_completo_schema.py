from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ObjetivoCompletoBase(BaseModel):
    id_usuario: int
    id_objetivo: int
    pontuacao: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ObjetivoCompletoCreate(ObjetivoCompletoBase):
    pass


class ObjetivoCompletoUpdate(BaseModel):
    id_usuario: Optional[int] = None  
    id_objetivo: Optional[int] = None 
    pontuacao: Optional[int] = None  

class ObjetivoCompleto(ObjetivoCompletoBase):
    class Config:
        orm_mode = True

