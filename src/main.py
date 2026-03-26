from fastapi import BackgroundTasks, FastAPI

from ingestion.ingestion import process_ingestion


app = FastAPI()


@app.get('/')
async def root():
    return {
        'message': 'Data Ingestion API ist online. Gehe zu /docs für die Dokumentation.'
    }


@app.post('/start-ingestion')
async def start_ingestion(folder_path: str, background_tasks: BackgroundTasks):
    """This function ..."""

    background_tasks.add_task(process_ingestion, folder_path)
    return {'status': 'Ingestion gestartet', 'path': folder_path}


@app.post('/price-recommendations')
async def price_recommendation():
    pass


@app.post('/max-recommendation')
async def max_recommendation():
    pass
