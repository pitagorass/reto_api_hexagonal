from abc import ABC, abstractmethod
from typing import Optional
from ..models import PersonaOut

class PersonRepositoryPort(ABC):
    @abstractmethod
    def create_person(self, identificacion: str, nombre: str, email: str) -> PersonaOut:
        raise NotImplementedError()

    @abstractmethod
    def get_person_by_id(self, id: int) -> Optional[PersonaOut]:
        raise NotImplementedError()
