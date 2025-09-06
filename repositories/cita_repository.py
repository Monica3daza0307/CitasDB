# repositories/cita_repository.py
from config.settings import CITAS
from models.cita_model import Cita

class CitaRepository:
    def get_all(self):
        return [Cita(**c) for c in CITAS]

    def get_by_id(self, cita_id):
        for c in CITAS:
            if c["id"] == cita_id:
                return Cita(**c)
        return None

    def create(self, data):
        new_id = max(c["id"] for c in CITAS) + 1 if CITAS else 1
        data["id"] = new_id
        CITAS.append(data)
        return Cita(**data)

    def update(self, cita_id, data):
        for i, c in enumerate(CITAS):
            if c["id"] == cita_id:
                CITAS[i].update(data)
                return Cita(**CITAS[i])
        return None

    def delete(self, cita_id):
        for c in CITAS:
            if c["id"] == cita_id:
                CITAS.remove(c)
                return True
        return False