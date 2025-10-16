# services/cita_service.py
from repositories.cita_repository import CitaRepository

from models.cita_model import Base
from sqlalchemy.orm import Session

class CitaService:
    def __init__(self):
        self.repo = CitaRepository()

    def listar(self):
        return self.repo.get_all()

    def obtener(self, cita_id):
        return self.repo.get_by_id(cita_id)

    def crear(self, data):
        return self.repo.create(data)

    def actualizar(self, cita_id, data):
        return self.repo.update(cita_id, data)

    def eliminar(self, cita_id):
        return self.repo.delete(cita_id)