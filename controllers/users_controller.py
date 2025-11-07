import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from services.users_services import UsersService

users_bp = Blueprint('users_bp', __name__)
service = UsersService()

@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            logger.warning("Login fallido: usuario o contraseña no proporcionados")
            return jsonify({
                'error': 'El nombre de usuario y la contraseña son obligatorios'
            }), 400
        
        user = service.authenticate_user(username, password)
        if user:
            access_token = create_access_token(identity=str(user.id))
            logger.info(f"Usuario autenticado: {username}")
            return jsonify({'access_token': access_token}), 200
        
        logger.warning(f"Login fallido para usuario: {username}")
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    except Exception as e:
        logger.error(f"Error en el login: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@users_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            logger.warning("Registro fallido: usuario o contraseña no proporcionados")
            return jsonify({
                'error': 'El nombre de usuario y la contraseña son obligatorios'
            }), 400
        
        existing_user = service.get_user_by_username(username)
        if existing_user:
            logger.warning(f"Registro fallido: el usuario {username} ya existe")
            return jsonify({
                'error': 'El nombre de usuario ya está en uso'
            }), 400
        
        user = service.create_user(username, password)
        logger.info(f"Usuario creado: {username}")
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user': {
                'id': user.id,
                'username': user.username
            }
        }), 201
    
    except Exception as e:
        logger.error(f"Error en el registro: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = service.get_all_users()
        return jsonify([{
            'id': user.id,
            'username': user.username
        } for user in users]), 200
    
    except Exception as e:
        logger.error(f"Error al obtener usuarios: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@users_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        user = service.get_user_by_id(user_id)
        if not user:
            logger.warning(f"Usuario no encontrado: {user_id}")
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'id': user.id,
            'username': user.username
        }), 200
    
    except Exception as e:
        logger.error(f"Error al obtener usuario {user_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username and not password:
            return jsonify({
                'error': 'Debe proporcionar al menos un campo para actualizar'
            }), 400
        
        user = service.update_user(user_id, username, password)
        if not user:
            logger.warning(f"Usuario no encontrado para actualizar: {user_id}")
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        logger.info(f"Usuario actualizado: {user_id}")
        return jsonify({
            'message': 'Usuario actualizado exitosamente',
            'user': {
                'id': user.id,
                'username': user.username
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Error al actualizar usuario {user_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        success = service.delete_user(user_id)
        if not success:
            logger.warning(f"Usuario no encontrado para eliminar: {user_id}")
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        logger.info(f"Usuario eliminado: {user_id}")
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    
    except Exception as e:
        logger.error(f"Error al eliminar usuario {user_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500