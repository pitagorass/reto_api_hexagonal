from pydantic import BaseModel

class PersonaIn(BaseModel):
    identificacion: str
    nombre: str
    email: str

class PersonaOut(BaseModel):
    id: int
    identificacion: str
    nombre: str
    email: str
    created_at: str | None = None
