from sqlalchemy import Column, Integer, String, Date, Time
from models.db import db

class Cita(db.Model):
    __tablename__ = 'citas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente = Column(String(100), nullable=False)
    servicio = Column(String(100), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    estado = Column(String(50), default='pendiente')  # pendiente / confirmada / cancelada

    def to_dict(self):
        return {
            "id": self.id,
            "cliente": self.cliente,
            "servicio": self.servicio,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "hora": self.hora.strftime("%H:%M:%S") if self.hora else None,
            "estado": self.estado
        }
