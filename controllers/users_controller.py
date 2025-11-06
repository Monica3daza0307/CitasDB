import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError

from config.database import get_db_session
from services.users_services import UsersService

user_bp = Blueprint('users_bp', __name__)
service = UsersService(get_db_session())

def register_jwt_error_handlers(app):
    @app.errorhandler(NoAuthorizationError)
    def handle_no_auth_error(e):
        logger.warning("Intento de acceso sin autenticación JWT")
        return jsonify({'error': 'No autenticado. Debe enviar un token JWT válido en el header Authorization.'}), 401, {'Content-Type': 'application/json; charset=utf-8'}

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        logger.warning("Login fallido: usuario o contraseña no proporcionados")
        return jsonify({'error': 'El nombre de usuario y la contraseña son obligatorios'}), 400, {'Content-Type': 'application/json; charset=utf-8'}
    
    user = service.authenticate_user(username, password)
    if user:
        access_token = create_access_token(identity=str(user.id))
        logger.info(f"Usuario autenticado: {username}")
        return jsonify({'access_token': access_token}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
    logger.warning(f"Login fallido para usuario: {username}")
    return jsonify({'error': 'Credenciales inválidas'}), 401, {'Content-Type': 'application/json; charset=utf-8'}

@user_bp.route('/registry', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        logger.warning("Registro fallido: usuario o contraseña no proporcionados")
        return jsonify({'error': 'El nombre de usuario y la contraseña son obligatorios'}), 400, {'Content-Type': 'application/json; charset=utf-8'}
    
    user = service.create_user(username, password)
    logger.info(f"Usuario creado: {username}")
    return jsonify({'id': user.id, 'username': user.username}), 201, {'Content-Type': 'application/json; charset=utf-8'}

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = service.get_all_users()
    logger.info("Consulta de todos los usuarios")
    return jsonify([{'id': u.id, 'username': u.username} for u in users]), 200, {'Content-Type': 'application/json; charset=utf-8'}

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = service.get_user_by_id(user_id)
    if user:
        logger.info(f"Consulta de usuario por ID: {user_id}")
        return jsonify({'id': user.id, 'username': user.username}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
    logger.warning(f"Usuario no encontrado: {user_id}")
    return jsonify({'error': 'Usuario no encontrado'}), 404, {'Content-Type': 'application/json; charset=utf-8'}

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = service.update_user(user_id, username, password)
    if user:
        logger.info(f"Usuario actualizado: {user_id}")
        return jsonify({'id': user.id, 'username': user.username}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
    logger.warning(f"Usuario no encontrado para actualizar: {user_id}")
    return jsonify({'error': 'Usuario no encontrado'}), 404, {'Content-Type': 'application/json; charset=utf-8'}

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = service.delete_user(user_id)
    if user:
        logger.info(f"Usuario eliminado: {user_id}")
        return jsonify({'message': 'Usuario eliminado correctamente'}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
    logger.warning(f"Usuario no encontrado para eliminar: {user_id}")
    return jsonify({'error': 'Usuario no encontrado'}), 404, {'Content-Type': 'application/json; charset=utf-8'}
