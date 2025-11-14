import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.db import Base

"""
La clase User representa a un usuario del sistema.
Cada instancia corresponde a un usuario con credenciales de acceso y relación con sus citas médicas.
"""
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    # role: 'user' or 'admin'
    role = Column(String(50), nullable=False, default='user')

    citas = relationship('Cita', back_populates='user', cascade='all, delete-orphan')
