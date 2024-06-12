import os
import threading
import time
from typing import List
from openai import OpenAI

from dotenv import load_dotenv
import openai
from requests import Session
import schedule
from src.database.database import SessionLocal, get_db
from src.repositories import objetivos_repositories as crud
from fastapi import APIRouter, Depends, HTTPException, Query
from src.models.Objetivo_model import Objetivos
from src.schemas import objetivos_schema as schemas
from src.repositories import usuario_repositories

load_dotenv()

openai.api_key = os.getenv("CHAVE_API")
# OpenAI API Key


router = APIRouter()

# Fila de requisição de objetivos

class No:
    def __init__(self, info):
        self.info = info
        self.proximo = None

# Funções da fila 
class FilaObjetivos:
    def __init__(self):
        self.primeiro = None
        self.ultimo = None

    def esta_vazia(self):
        return self.primeiro is None

    def enfileira(self, objetivo):
        novo = No(objetivo)
        if self.esta_vazia():
            self.primeiro = novo
        else:
            self.ultimo.proximo = novo
        self.ultimo = novo

    def desenfileira(self):
        if self.esta_vazia():
            return None
        temp = self.primeiro.info
        self.primeiro = self.primeiro.proximo
        if self.primeiro is None:
            self.ultimo = None
        return temp

fila_objetivos = FilaObjetivos()

@router.post("/objetivos/")
async def adicionar_objetivo(db: Session = Depends(get_db)):
    try:
        objetivos_status_false = crud.get_objetivos_status_false(db)
        
        if not objetivos_status_false:
            raise HTTPException(status_code=404, detail="Nenhum objetivo com status False encontrado.")

        for objetivo in objetivos_status_false:
            fila_objetivos.enfileira(objetivo)

        return {"message": "Objetivos adicionados à fila com sucesso!", "objetivos": objetivos_status_false}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/objetivos/")
async def remover_objetivo( id_usuario: int, db: Session = Depends(get_db)):
    objetivo_removido = fila_objetivos.desenfileira()
    if objetivo_removido:

        try:
            crud.update_objetivo_status(db, objetivo_removido.id_objetivo, status=True)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        try:
            pontuacao = objetivo_removido.pontuacao 
            usuario_repositories.update_usuario_pontuacao(db, id_usuario, pontuacao)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return {"message": "Objetivo removido com sucesso!", "objetivo": objetivo_removido}
    else:
        raise HTTPException(status_code=404, detail="Fila de objetivos vazia!")





@router.get("/objetivos_limit/")
async def obter_fila_objetivos_5(limit: int = Query(5, ge=1, le=100)):
    fila_lista = []
    no_atual = fila_objetivos.primeiro
    count = 0
    while no_atual is not None and count < limit:
        fila_lista.append(no_atual.info)
        no_atual = no_atual.proximo
        count += 1
    return fila_lista

# @router.post("/objetivos/gerar/")
# async def gerar_objetivos():
#     try:
#         gerar_objetivos_semanalmente()
#         return {"message": "Objetivos gerados com sucesso!"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Função para gerar 5 objetivos
# def gerar_objetivos_semanalmente():
#     print("Gerando objetivos semanalmente...")
#     with SessionLocal() as db:
#         for _ in range(5):
#             try:
#                 response = openai.chat.completions.create(
#                     model="gpt-3.5-turbo",
#                     response_format={ "type": "json_object" }
#                     prompt=[

#                             "role": "user",
#                             "content": "Crie um objetivo semanal para um aplicativo infantil de combate à obesidade, envolvendo atividades físicas ou alimentação saudável."
                        
#                     ],
#                     max_tokens=50
#                 )
                
#                 objetivo_texto = response['choices'][0]['message']['content'].strip()
#                 novo_objetivo = schemas.Objetivos(
#                     id_objetivo=0,  # Ajuste conforme necessário
#                     descricao=objetivo_texto,
#                     pontuacao=10,    # Ajuste conforme necessário
#                     status=False
#                 )
#                 db_objetivo = crud.create_objetivos(db, novo_objetivo)
#                 fila_objetivos.enfileira(db_objetivo)
#                 print(f"Objetivo gerado: {objetivo_texto}")
#             except Exception as e:
#                 print(f"Erro ao gerar objetivo: {e}")
                
