import base64
import io
import os
from fastapi.responses import HTMLResponse, StreamingResponse
import plotly.express as px
from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.repositories import consumo_animal_repositories as crud
from src.schemas import consumo_animal_schema as schemas
from src.database.database import get_db

router = APIRouter()

@router.post("/consumo", response_model=schemas.ConsumoAnimal)
def create_consumo(consumo: schemas.ConsumoAnimalBase, db: Session = Depends(get_db)):
    try:
        return crud.create_consumo(db=db, consumo_animal=consumo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/consumo/{id_consumo}", response_model=schemas.ConsumoAnimalBase)
def read_consumo(id_consumo: int, db: Session = Depends(get_db)):
    db_consumo = crud.get_consumo(db, id_consumo=id_consumo)
    if db_consumo is None:
        raise HTTPException(status_code=404, detail="consumo not found")
    return db_consumo

@router.get("/consumo", response_model=List[schemas.ConsumoAnimal])
def read_consumo(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    consumo = crud.get_consumos(db, skip=skip, limit=limit)
    return consumo


@router.delete("/consumo/{id_consumo}", response_model=schemas.ConsumoAnimal)
def delete_consumo(id_consumo: int, db: Session = Depends(get_db)):
    return crud.delete_consumo_animal(db=db, id_consumo=id_consumo)



# Gráfico

def plot_consumo_alimentos(df):
    df_agrupado = df.groupby('grupo_alimento')['qtd'].sum().reset_index()
    fig = px.bar(df_agrupado, x='grupo_alimento', y='qtd', color='grupo_alimento',
                 title='Consumo de Alimentos por Grupo',
                 labels={'qtd': 'Quantidade Consumida (Unidades)', 'grupo_alimento': 'Grupo de Alimento'})
    fig.update_layout(title_font_size=20, xaxis_title_font_size=16, yaxis_title_font_size=16, legend_title_font_size=14)
    return fig

def plot_media_grupo_alimento(df):
    df_media = df.groupby('grupo_alimento')['qtd'].mean().reset_index()
    fig = px.bar(df_media, x='grupo_alimento', y='qtd', color='grupo_alimento',
                 title='Média de Consumo de Alimentos por Grupo',
                 labels={'qtd': 'Média de Quantidade Consumida', 'grupo_alimento': 'Grupo de Alimento'},
                 color_continuous_scale=px.colors.sequential.Viridis)
    fig.update_layout(title_font_size=20, xaxis_title_font_size=16, yaxis_title_font_size=16, legend_title_font_size=14)
    return fig

def plot_moda_grupo_alimento(df):
    df['month'] = df['created_at'].dt.month
    
    moda_por_mes = df.groupby(['month', 'grupo_alimento']).size().reset_index(name='count')
    moda_por_mes = moda_por_mes.loc[moda_por_mes.groupby('month')['count'].idxmax()]
    
    # Mapear números de mês para nomes de mês
    month_names = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    moda_por_mes['month'] = moda_por_mes['month'].map(month_names)  # Converter o número do mês para o nome do mês
    
    fig = px.bar(moda_por_mes, x='month', y='count', color='grupo_alimento',
                 title='Grupo de Alimento Mais Consumido por Mês',
                 labels={'count': 'Frequência', 'month': 'Mês'},
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    return fig

def plot_to_base64(plot_func, df):
    fig = plot_func(df)
    img_data = io.BytesIO()
    fig.write_image(img_data, format='png')
    img_data.seek(0)
    base64_bytes = base64.b64encode(img_data.getvalue())
    return base64_bytes.decode('utf-8')

@router.get("/consumo_animal/")
async def get_consumo_animal(ano: int, db: Session = Depends(get_db)):
    try:
        df = crud.get_consumo_animal_dataframe(db, ano)
        if df.empty:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para o ano especificado.")

        consumo_plot = plot_to_base64(plot_consumo_alimentos, df)
        media_plot = plot_to_base64(plot_media_grupo_alimento, df)
        moda_plot = plot_to_base64(plot_moda_grupo_alimento, df)

        return {
            "consumo_plot": consumo_plot,
            "media_plot": media_plot,
            "moda_plot": moda_plot,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/consumo_animal_html/", response_class=HTMLResponse)
async def get_consumo_animal_html(ano: int, db: Session = Depends(get_db)):
    try:
        df = crud.get_consumo_animal_dataframe(db, ano)
        if df.empty:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para o ano especificado.")

        consumo_plot = plot_to_base64(plot_consumo_alimentos, df)
        media_plot = plot_to_base64(plot_media_grupo_alimento, df)
        moda_plot = plot_to_base64(plot_moda_grupo_alimento, df)

        html_content = f"""
        <html>
        <head>
            <title>Consumo Animal</title>
        </head>
        <body>
            <h1>Consumo de Alimentos por Grupo</h1>
            <img src="data:image/png;base64,{consumo_plot}" alt="Consumo de Alimentos por Grupo">
            <h1>Média de Consumo de Alimentos por Grupo</h1>
            <img src="data:image/png;base64,{media_plot}" alt="Média de Consumo de Alimentos por Grupo">
            <h1>Grupo de Alimento Mais Consumido por Mês</h1>
            <img src="data:image/png;base64,{moda_plot}" alt="Grupo de Alimento Mais Consumido por Mês">
        </body>
        </html>
        """

        return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))