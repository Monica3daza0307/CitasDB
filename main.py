from models.db import Base
from config.database import engine
from flask import Flask
from config.jwt import *
from controllers.citas_controller import citas_bp
from controllers.users_controller import user_bp, register_jwt_error_handlers
from flask_jwt_extended import JWTManager
from config.database import SessionLocal
from repositories.users_repository import UsersRepository
from werkzeug.security import generate_password_hash

app = Flask(__name__)


# Configurar JWT
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_TOKEN_LOCATION'] = JWT_TOKEN_LOCATION
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
app.config['JWT_HEADER_NAME'] = JWT_HEADER_NAME
app.config['JWT_HEADER_TYPE'] = JWT_HEADER_TYPE

jwt = JWTManager(app)
__all__ = ["engine", "SessionLocal"]


# Registrar blueprints
app.register_blueprint(citas_bp)
app.register_blueprint(user_bp)

# Registrar manejadores personalizados de error JWT
register_jwt_error_handlers(app)

if __name__ == "__main__":
    print("Verificando y creando tablas de base de datos si es necesario...")
    Base.metadata.create_all(engine)
    print("Tablas listas.")
    # Crear usuario administrador por defecto si no existe
    try:
        db = SessionLocal()
        users_repo = UsersRepository(db)
        admin_username = 'admin'
        admin_password = 'admin123'  # Cambia esta contraseña en producción
        existing = users_repo.get_user_by_username(admin_username)
        if not existing:
            hashed = generate_password_hash(admin_password)
            users_repo.create_user(admin_username, hashed, role='admin')
            print(f"Usuario administrador creado: {admin_username}")
        else:
            print("Usuario administrador ya existe.")
    except Exception as e:
        print("No se pudo crear el usuario admin automáticamente:", e)
    finally:
        try:
            db.close()
        except:
            pass
    app.run(debug=True)

