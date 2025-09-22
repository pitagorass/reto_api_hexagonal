from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PersonaIn(BaseModel):
    identificacion: str
    nombre: str
    email: str

class PersonaOut(BaseModel):
    id: int
    identificacion: str
    nombre: str
    email: str
    created_at: Optional[datetime] = None
