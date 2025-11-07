import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth_bp', __name__)

# Usuario de prueba (en producción esto debería estar en una base de datos)
TEST_USER = {
    'username': 'admin',
    'password': 'admin123'
}

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            logger.warning("Login fallido: usuario o contraseña no proporcionados")
            return jsonify({'error': 'El nombre de usuario y la contraseña son obligatorios'}), 400

        # Validar credenciales (en producción esto debería validar contra una base de datos)
        if username == TEST_USER['username'] and password == TEST_USER['password']:
            access_token = create_access_token(identity=username)
            logger.info(f"Usuario autenticado: {username}")
            return jsonify({'access_token': access_token}), 200

        logger.warning(f"Login fallido para usuario: {username}")
        return jsonify({'error': 'Credenciales inválidas'}), 401

    except Exception as e:
        logger.error(f"Error en el login: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500