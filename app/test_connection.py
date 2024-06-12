import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

db_password = os.getenv("SENHA_BANCO")

SQLALCHEMY_DATABASE_URL = f"postgresql://avnadmin:{db_password}@pg-25cb39a-abnschlink-031a.h.aivencloud.com:22352/db_fitKids?sslmode=require"


# Cria uma engine de banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL)

try:
    # Tenta estabelecer uma conexão
    with engine.connect() as connection:
        print("Conexão bem-sucedida!")
except Exception as e:
    print("Erro ao conectar:", e)