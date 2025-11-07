import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from services.cita_service import CitaService

cita_bp = Blueprint('cita_bp', __name__)
service = CitaService()

@cita_bp.route('/citas', methods=['GET'])
@jwt_required()
def get_citas():
    try:
        citas = service.listar()
        logger.info("Consulta de todas las citas")
        return jsonify(citas), 200
    except Exception as e:
        logger.error(f"Error al obtener las citas: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@cita_bp.route('/citas/<int:cita_id>', methods=['GET'])
@jwt_required()
def get_cita(cita_id):
    try:
        cita = service.obtener(cita_id)
        if cita:
            logger.info(f"Consulta de cita por ID: {cita_id}")
            return jsonify(cita), 200
        logger.warning(f"Cita no encontrada: {cita_id}")
        return jsonify({'error': 'Cita no encontrada'}), 404
    except Exception as e:
        logger.error(f"Error al obtener la cita {cita_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@cita_bp.route('/citas', methods=['POST'])
@jwt_required()
def create_cita():
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['cliente', 'servicio', 'fecha', 'hora']
        for field in required_fields:
            if field not in data:
                logger.warning(f"Creación de cita fallida: campo {field} no proporcionado")
                return jsonify({'error': f'El campo {field} es obligatorio'}), 400
        
        try:
            # Convertir fecha y hora a los formatos correctos
            fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
            hora = datetime.strptime(data['hora'], '%H:%M').time()
            
            # Crear objeto de datos para el servicio
            cita_data = {
                'cliente': data['cliente'],
                'servicio': data['servicio'],
                'fecha': fecha,
                'hora': hora,
                'estado': data.get('estado', 'pendiente')  # valor por defecto: pendiente
            }
            
            cita = service.crear(cita_data)
            logger.info(f"Cita creada para el cliente: {data['cliente']}")
            return jsonify(cita), 201
            
        except ValueError as e:
            logger.error(f"Error al procesar fecha/hora: {str(e)}")
            return jsonify({'error': 'Formato de fecha u hora inválido. Use YYYY-MM-DD para fecha y HH:MM para hora'}), 400
    except Exception as e:
        logger.error(f"Error al crear la cita: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@cita_bp.route('/citas/<int:cita_id>', methods=['PUT'])
@jwt_required()
def update_cita(cita_id):
    try:
        data = request.get_json()
        
        try:
            # Convertir fecha y hora si están presentes
            if 'fecha' in data:
                data['fecha'] = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
            if 'hora' in data:
                data['hora'] = datetime.strptime(data['hora'], '%H:%M').time()
            
            cita = service.actualizar(cita_id, data)
            if cita:
                logger.info(f"Cita actualizada: {cita_id}")
                return jsonify(cita), 200
            
            logger.warning(f"Cita no encontrada para actualizar: {cita_id}")
            return jsonify({'error': 'Cita no encontrada'}), 404
            
        except ValueError as e:
            logger.error(f"Error al procesar fecha/hora: {str(e)}")
            return jsonify({'error': 'Formato de fecha u hora inválido. Use YYYY-MM-DD para fecha y HH:MM para hora'}), 400
    except Exception as e:
        logger.error(f"Error al actualizar la cita {cita_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@cita_bp.route('/citas/<int:cita_id>', methods=['DELETE'])
@jwt_required()
def delete_cita(cita_id):
    try:
        if service.eliminar(cita_id):
            logger.info(f"Cita eliminada: {cita_id}")
            return jsonify({'message': 'Cita eliminada correctamente'}), 200
        
        logger.warning(f"Cita no encontrada para eliminar: {cita_id}")
        return jsonify({'error': 'Cita no encontrada'}), 404
    except Exception as e:
        logger.error(f"Error al eliminar la cita {cita_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500