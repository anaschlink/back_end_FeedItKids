from sqlalchemy import Column, Float, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from  src.database.database import Base
from .mixins import Timestamp 

class ConsumoAnimal(Timestamp, Base):
    __tablename__ = "consumo_animal"

    id_consumo = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_status_alimento = Column(Integer, ForeignKey("alimento_status.id_status_alimento"))
    alimento = Column(String(255))
    qtd = Column(Float, default=1.0)

    usuario = relationship("Usuario", back_populates="consumos_animais")
    status_alimento = relationship("StatusAlimento", back_populates="consumos_animais")

class StatusAnimal(Timestamp, Base):
    __tablename__ = "status_animal"

    id_status_animal = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    alimentacao_saudavel = Column(Float, default=10, nullable=False)
    energia = Column(Float, default=10, nullable=False)
    forca = Column(Float, default=10, nullable=False)
    felicidade = Column(Float, default=10, nullable=False)

    usuario = relationship("Usuario", back_populates="status_animais")
    