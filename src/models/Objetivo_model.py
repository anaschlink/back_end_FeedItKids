from sqlalchemy import Boolean, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database  import Base
from src.models.mixins import Timestamp

class Objetivos(Base):
    __tablename__ = "objetivos"

    id_objetivo = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255), nullable=False)
    pontuacao = Column(Integer, nullable=False)
    status = Column(Boolean,default=False)

    objetivo_completos =relationship("ObjetivoCompleto")

class ObjetivoCompleto(Timestamp, Base):
    __tablename__ = "objetivo_completo"

    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), primary_key=True)
    id_objetivo = Column(Integer, ForeignKey("objetivos.id_objetivo"), primary_key=True)
    pontuacao = Column(Integer, nullable=False)

    usuario = relationship("Usuario", back_populates="objetivos_completos")
    objetivo = relationship("Objetivos", back_populates="objetivo_completos")