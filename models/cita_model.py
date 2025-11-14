import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from models.db import Base

"""
La clase Cita representa una cita médica dentro del sistema.
Cada instancia corresponde a una cita específica, almacenando información como:
- Nombre del paciente
- Fecha y hora de la cita
- Motivo de la consulta
- Estado (pendiente, confirmada, cancelada)
- Usuario que la registró
"""
class Cita(Base):
    __tablename__ = 'citas'
    id = Column(Integer, primary_key=True, index=True)
    paciente = Column(String(100), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    motivo = Column(String(255), nullable=False)
    estado = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='citas')
