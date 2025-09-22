import os
from fastapi import FastAPI, HTTPException
from .models import PersonaIn, PersonaOut
from .adapters.db.postgres import PostgresPersonRepository
from .services.person_service import PersonService

# Read env vars (these will be injected by ECS via SSM/Secrets)
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = int(os.environ.get('DB_PORT', 5432))
DB_NAME = os.environ.get('DB_NAME', 'appdb')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
API_PORT = int(os.environ.get('API_PORT', 3000))

if not all([DB_HOST, DB_USER, DB_PASS]):
    # On startup we will allow running locally without raising; route handlers will fail clearly if missing
    print('Warning: DB_* env vars not fully set. Provide DB_HOST, DB_USER, DB_PASS for DB connectivity.')

repo = PostgresPersonRepository(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
service = PersonService(repo)

app = FastAPI(title='Reto AWS - API (hexagonal)')

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/guardarpersona', response_model=PersonaOut, status_code=201)
def guardar_persona(payload: PersonaIn):
    try:
        created = service.create_person(payload.identificacion, payload.nombre, payload.email)
        return created
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/consultarpersona/{id}', response_model=PersonaOut)
def consultar_persona(id: int):
    p = service.get_person_by_id(id)
    if p is None:
        raise HTTPException(status_code=404, detail='persona no encontrada')
    return p
