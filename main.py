from flask import Flask
from controllers.cita_controller import cita_bp
from controllers.auth_controller import auth_bp
from controllers.users_controller import users_bp
from models.db import db
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'tu-clave-secreta-temporal')

# Configuración de la base de datos
MYSQL_URI = os.getenv('MYSQL_URI')
if MYSQL_URI:
    app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_URI
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///citas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
db.init_app(app)
jwt = JWTManager(app)

# Registrar blueprints (prefijos corregidos)
# auth -> /api/auth  => /api/auth/login
# users -> /api      => /api/login, /api/register, /api/users
# citas -> /api      => /api/citas
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(users_bp, url_prefix='/api')
app.register_blueprint(cita_bp, url_prefix='/api')

# Crear todas las tablas
with app.app_context():
    db.create_all()

# Configurar CORS para permitir peticiones desde cualquier origen
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
