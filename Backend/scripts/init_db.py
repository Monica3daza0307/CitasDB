"""Inicializa las tablas en la base de datos usadas por el proyecto.
Ejecutar:
  python scripts/init_db.py
"""
from config.database import engine
import models.users_models as users_mod
import models.cita_model as cita_mod

print('Creando tablas para users...')
users_mod.Base.metadata.create_all(engine)
print('Creando tablas para citas...')
cita_mod.Base.metadata.create_all(engine)
print('Inicialización completada.')
