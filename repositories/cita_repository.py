# repositories/cita_repository.py
from config.settings import CITAS

class CitaRepository:
    def get_all(self):
        return CITAS

    def get_by_id(self, cita_id):
        return next((c for c in CITAS if c["id"] == cita_id), None)

    def create(self, data):
        CITAS.append(data)
        return data

    def update(self, cita_id, data):
        for i, cita in enumerate(CITAS):
            if cita["id"] == cita_id:
                CITAS[i].update(data)
                return CITAS[i]
        return None

    def delete(self, cita_id):
        cita = self.get_by_id(cita_id)
        if cita:
            CITAS.remove(cita)
            return True
        return False