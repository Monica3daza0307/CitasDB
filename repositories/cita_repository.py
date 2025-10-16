# repositories/cita_repository.py
from models.cita_model import Cita
from models.db import db

class CitaRepository:
    def get_all(self):
        citas = Cita.query.all()
        return [cita.to_dict() for cita in citas]

    def get_by_id(self, cita_id):
        cita = Cita.query.get(cita_id)
        return cita.to_dict() if cita else None

    def create(self, data):
        nueva_cita = Cita(
            fecha=data.get('fecha'),
            descripcion=data.get('descripcion')
        )
        db.session.add(nueva_cita)
        db.session.commit()
        return nueva_cita.to_dict()  # 👈 devuelves un dict

    def update(self, cita_id, data):
        cita = Cita.query.get(cita_id)
        if not cita:
            return None
        cita.fecha = data.get('fecha', cita.fecha)
        cita.descripcion = data.get('descripcion', cita.descripcion)
        db.session.commit()
        return cita.to_dict()

    def delete(self, cita_id):
        cita = Cita.query.get(cita_id)
        if not cita:
            return False
        db.session.delete(cita)
        db.session.commit()
        return True
