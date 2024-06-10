from fastapi import Depends, FastAPI
import IA
from src.database.database import SessionLocal, engine, Base, get_db
from src.models.status_alimento_model import StatusAlimento
from src.models.Animal_model import ConsumoAnimal, StatusAnimal
from src.models.Usuario_model import Usuario
from src.models.Objetivo_model import Objetivos, ObjetivoCompleto
from src.routes import usuario_routes, objetivos_routes, objetivo_completo_routes,consumo_animal_routes,status_animal_routes,status_routes,auth_routes
import fila_objetivos
from fastapi.middleware.cors import CORSMiddleware

import schedule
import time
from src.repositories.status_animal_repositories import  update_status_animal_attributes  # Importe sua função de atualização

app = FastAPI()

origins = [
    "http://localhost:8081",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(usuario_routes.router, prefix="/usuarios" ,tags=["usuarios"])
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(objetivos_routes.router, prefix="/objetivos", tags=["objetivos"])
app.include_router(objetivo_completo_routes.router, prefix="/objetivoCompleto", tags=["objetivoCompleto"])
app.include_router(consumo_animal_routes.router, prefix="/consumo", tags=["consumo"])
app.include_router(status_animal_routes.router, prefix="/status_animal", tags=["status_animal"])
app.include_router(status_routes.router, prefix="/status", tags=["status"])
app.include_router(IA.router , prefix='/process_image', tags=["process_image"])
app.include_router(fila_objetivos.router, prefix='/fila_objetivos', tags=["fila_objetivos"])

# Define database initialization and table creation as a separate function
def initialize_database():
    # Create all tables if they do not exist
    Base.metadata.create_all(bind=engine)

# Call the database initialization function before starting the FastAPI application
initialize_database()

@app.get("/")
async def root():
    return {"message": "teste"}


def initialize_scheduling():
    # Schedule the update_status_animal_attributes function to run every hour
    schedule.every().hour.do(update_status_animal_attributes, db=SessionLocal())

    # Start the scheduling loop
    while True:
        schedule.run_pending()
        time.sleep(1)

# Run the scheduling logic when the script is executed
if __name__ == "__main__":
    print("Scheduling initialized.")
    initialize_scheduling()