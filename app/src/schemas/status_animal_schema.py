from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class StatusAnimalBase(BaseModel):
    id_usuario: int
    alimentacao_saudavel:float
    energia :float
    forca:float
    felicidade :float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
class StatusAnimalUpdate(StatusAnimalBase):
    alimentacao_saudavel:Optional[float]
    energia :Optional[float]
    forca:Optional[float]
    felicidade :Optional[float]
    

class StatusAnimal(StatusAnimalBase):
    id_status_animal: int

    class Config:
        orm= True
