from pydantic import BaseModel
from typing import List, Optional


class ObjetivosBase(BaseModel):
    id_objetivo: Optional[int] = None
    descricao: str
    pontuacao: int
    status: bool

class ObjetivosUpdate(ObjetivosBase):
    descricao:  Optional[str] = None
    pontuacao:  Optional[int] = None
    status:  Optional[bool] = None

class Objetivos(ObjetivosBase):
    id_objetivo: int
    descricao:  Optional[str] = None
    pontuacao:  Optional[int] = None
    status:  Optional[bool] = None

    class Config:
         orm= True

