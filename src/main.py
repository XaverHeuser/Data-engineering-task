from fastapi import BackgroundTasks, FastAPI

from src.ingestion.ingestion import process_ingestion
from src.recommendations.recommendations import (
    calculate_max_recommendation,
    price_recommendations,
)


app = FastAPI()


@app.get('/')
async def root():
    return {
        'message': 'Data Ingestion API ist online. Gehe zu /docs für die Dokumentation.'
    }


@app.post('/start-ingestion')
async def start_ingestion(folder_path: str, background_tasks: BackgroundTasks):
    """This function starts the ingestion process."""

    background_tasks.add_task(process_ingestion, folder_path)
    return {'status': 'Ingestion gestartet', 'path': folder_path}


@app.post('/price-recommendations')
async def price_recommendation(background_tasks: BackgroundTasks):
    """This function calculates the price recommendations."""

    background_tasks.add_task(price_recommendations)
    return {'status': 'Price recommendations started'}


@app.post('/max-recommendation')
async def max_recommendation(background_tasks: BackgroundTasks):
    """This function calculates the maximum recommendations."""

    background_tasks.add_task(calculate_max_recommendation)
    return {'status': 'Max recommendations started'}
