from models.cita_model import Cita
from config.database import get_db_session


class CitaRepository:
    def get_all(self):
        session = get_db_session()
        try:
            citas = session.query(Cita).all()
            return citas
        finally:
            session.close()

    def get_by_id(self, cita_id):
        session = get_db_session()
        try:
            cita = session.query(Cita).get(cita_id)
            return cita
        finally:
            session.close()

    def create(self, data):
        session = get_db_session()
        try:
            nueva_cita = Cita(
                cliente=data.get('cliente'),
                servicio=data.get('servicio'),
                fecha=data.get('fecha'),
                hora=data.get('hora'),
                estado=data.get('estado', 'pendiente')
            )
            session.add(nueva_cita)
            session.commit()
            session.refresh(nueva_cita)
            return nueva_cita
        finally:
            session.close()

    def update(self, cita_id, data):
        session = get_db_session()
        try:
            cita = session.query(Cita).get(cita_id)
            if not cita:
                return None
            cita.cliente = data.get('cliente', cita.cliente)
            cita.servicio = data.get('servicio', cita.servicio)
            cita.fecha = data.get('fecha', cita.fecha)
            cita.hora = data.get('hora', cita.hora)
            cita.estado = data.get('estado', cita.estado)
            session.commit()
            return cita
        finally:
            session.close()

    def delete(self, cita_id):
        session = get_db_session()
        try:
            cita = session.query(Cita).get(cita_id)
            if not cita:
                return False
            session.delete(cita)
            session.commit()
            return True
        finally:
            session.close()
