import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

from models.users_models import Base as UsersBase
from models.cita_model import Base as CitaBase

logging.basicConfig(level=logging.INFO)
load_dotenv()

MYSQL_URI = os.getenv("MYSQL_URI")
SQLITE_URI = "sqlite:///app_database.db"

def get_engine():
    """
    Intenta crear una conexión con MySQL. Si falla, usa SQLite local.
    """
    if MYSQL_URI:
        try:
            engine = create_engine(MYSQL_URI, echo=True)
            # Probar conexión
            conn = engine.connect()
            conn.close()
            logging.info("Conexión a MySQL exitosa.")
            return engine
        except OperationalError:
            logging.warning("No se pudo conectar a MySQL. Usando SQLite local.")
    # Fallback a SQLite
    engine = create_engine(SQLITE_URI, echo=True)
    return engine

engine = get_engine()
Session = sessionmaker(bind=engine)

# Crear todas las tablas de los modelos
UsersBase.metadata.create_all(engine)
CitaBase.metadata.create_all(engine)

def get_db_session():
    """
    Retorna una nueva sesión de base de datos para ser utilizada en los servicios o controladores.
    """
    return Session()
