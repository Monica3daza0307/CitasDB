from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL de conexión: ajusta según tu configuración
DATABASE_URL = "mysql+pymysql://usuario:contraseña@localhost/citas_db"

# Crear motor de conexión
engine = create_engine(DATABASE_URL)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
