from pydantic import BaseModel

class StatusBase(BaseModel):
    grupo_alimento: str
    alimentacao_saudavel: float  
    energia: float
    forca: float
    felicidade: float

class StatusResponse(StatusBase):
    id_status_alimento: int

    class Config:
        orm_mode = True