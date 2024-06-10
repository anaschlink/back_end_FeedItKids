from pydantic import BaseModel, EmailStr

class ConsumoAnimalBase(BaseModel):
    id_usuario: int 
    id_status_alimento: int
    alimento: str

class ConsumoRequest(BaseModel):
    id_alimento: int
    alimento: str
    id_usuario: int

class ConsumoAnimal(ConsumoAnimalBase):
    id_consumo: int

    class Config:
        orm_mode = True
