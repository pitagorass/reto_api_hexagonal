from typing import Optional
from ..ports.repository import PersonRepositoryPort
from ..models import PersonaOut

class PersonService:
    def __init__(self, repo: PersonRepositoryPort):
        # Accepts any repo implementing the port (Postgres adapter does)
        self.repo = repo

    def create_person(self, identificacion: str, nombre: str, email: str) -> PersonaOut:
        # Here you can add domain validation rules
        if not identificacion or not nombre or not email:
            raise ValueError('faltan campos obligatorios')
        return self.repo.create_person(identificacion, nombre, email)

    def get_person_by_id(self, id: int) -> Optional[PersonaOut]:
        return self.repo.get_person_by_id(id)
