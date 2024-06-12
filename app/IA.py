import asyncio
import os
import json
from typing import Annotated
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
import base64
import httpx
from sqlalchemy.orm import Session
from src.repositories.status_animal_repositories import update_status_animal
from src.database.database import get_db
from src.repositories.consumo_animal_repositories import create_consumo
from src.models import Animal_model as models
from src.models.status_alimento_model import StatusAlimento

db_dependency = Annotated[Session, Depends(get_db)]

load_dotenv()

api_key = os.getenv("CHAVE_API")

# Initialize FastAPI app
router = APIRouter()

# OpenAI API Key
api_key = api_key

# Function to encode the image file to base64
def encode_image(image_file):
    # Read the image file and encode it to base64
    return base64.b64encode(image_file.read()).decode('utf-8')

# Function to process the image using OpenAI API
async def process_image(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
"Identifique a categoria do alimento com base nas seguintes opções de fluxo: o número é o id_status, nome do grupo é o [paes]

1: Pães, Massas, Cereais, Arroz, Aveia, Raízes, Tubérculos
2: Frutas
3: Legumes
4: Leite e Derivados, Iogurte, Queijos
5: Carnes, Ovos, Leguminosas e Oleaginosas
6: Doces, Chocolate, Balas, Guloseimas
7: Salgados de Padaria/Festa
8: Refrigerante, Bebidas Gaseificadas, Sucos de Caixinha
9: Suco Natural de Fruta, Água
10: Embutidos, Presunto, Peito de Peru, Mortadela

Se for fast-food, classifique como Guloseimas.

Na resposta, forneça a categoria, o nome do grupo da categoria[paes,frutas], se houver, o nome do alimento.
 A resposta deve ser um didionario python:
 [{"id_status": categoria,"grupo_alimento": "nome grupo categoria","alimento": "nome do alimento" }]. não adicione "\n" e nem /."
"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        # Acessa o conteúdo da chave "content" dentro do JSON retornado
        content = response.json()["choices"][0]["message"]["content"]
        return content
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

@router.post("/process_image/", response_model=None)
async def process_image_route(id_usuario: int, image: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Call the function to encode the image to base64
        base64_image = encode_image(image.file)
        
        # Call the function to process the image using OpenAI API
        response_data = await process_image(base64_image)  # Use await para chamar a função assíncrona
        
        # Transforma a resposta em um dicionário Python
        response_dict = json.loads(response_data)

        # Agora você pode acessar os dados conforme necessário
        id_status = response_dict[0]["id_status"]
        grupo_alimento = response_dict[0]["grupo_alimento"]
        alimento = response_dict[0]["alimento"]

        # Use essas variáveis conforme necessário
        print(f"id_status: {id_status}, grupo_alimento: {grupo_alimento}, alimento: {alimento}")

        process_data(db, id_status, alimento, id_usuario)  # Pass db parameter here

        return response_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





def process_data(db: Session, id_status, alimento, id_usuario):
    # Verifica se o id_status existe na tabela alimento_status
    if check_id_status(db, id_status):
        # Insere o id_status, alimento e id_usuario na tabela consumo_animal
        insert_into_consumo_animal(db, id_status, alimento, id_usuario)
        print("Dados inseridos com sucesso na tabela consumo_animal!")
        # Atualiza o status do animal após a inserção
        update_status_animal(db, id_status, id_usuario)
        print("Dados inseridos com sucesso na tabela status_animal!")
    else:
        print("Erro: O id_status não existe na tabela alimento_status.")


# Função para verificar se o id_status existe na tabela alimento_status
def check_id_status(db: Session, id_status):
    result = db.query(StatusAlimento).filter_by(id_status_alimento=id_status).first()
    return result is not None

def insert_into_consumo_animal(db: Session, id_status: int, alimento: str, id_usuario: int):
    new_consumo_animal = models.ConsumoAnimal(
        id_status_alimento=id_status,
        alimento=alimento,
        id_usuario=id_usuario
    )
    db.add(new_consumo_animal)
    db.commit()
    db.refresh(new_consumo_animal)
    print(f"insert_into_consumo_animal: {new_consumo_animal}")
    return new_consumo_animal