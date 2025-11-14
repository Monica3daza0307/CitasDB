import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from flask import Blueprint, request, jsonify
from services.cita_service import CitaService
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.database import get_db_session

# Obtain a DB session instance (Session object) and pass it to the service.
db_session = get_db_session()


citas_bp = Blueprint('citas_bp', __name__)
service = CitaService(db_session)

@citas_bp.route('/citas', methods=['GET'])
@jwt_required()
def get_citas():
    logger.info("Consulta de todas las citas")
    citas = service.listar_citas()
    return jsonify([
        {
            'id': c.id,
            'paciente': c.paciente,
            'fecha': c.fecha.isoformat(),
            'hora': c.hora,
            'motivo': c.motivo,
            'estado': c.estado
        } for c in citas
    ]), 200, {'Content-Type': 'application/json; charset=utf-8'}

@citas_bp.route('/citas/<int:cita_id>', methods=['GET'])
@jwt_required()
def get_cita(cita_id):
    cita = service.obtener_cita(cita_id)
    if cita:
        logger.info(f"Consulta de cita por ID: {cita_id}")
        return jsonify({
            'id': cita.id,
            'paciente': cita.paciente,
            'fecha': cita.fecha.isoformat(),
            'hora': cita.hora,
            'motivo': cita.motivo,
            'estado': cita.estado
        }), 200, {'Content-Type': 'application/json; charset=utf-8'}
    logger.warning(f"Cita no encontrada: {cita_id}")
    return jsonify({'error': 'Cita no encontrada'}), 404, {'Content-Type': 'application/json; charset=utf-8'}

@citas_bp.route('/citas', methods=['POST'])
@jwt_required()
def create_cita():
    data = request.get_json()
    required_fields = ['paciente', 'fecha', 'hora', 'motivo', 'estado']
    if not all(field in data for field in required_fields):
        logger.warning("Faltan campos obligatorios para crear cita")
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400, {'Content-Type': 'application/json; charset=utf-8'}

    # Extract user id from JWT identity and pass it to the service/repository
    jwt_identity = get_jwt_identity()
    try:
        user_id = int(jwt_identity) if jwt_identity is not None else None
    except (TypeError, ValueError):
        user_id = None

    cita = service.crear_cita(
        paciente=data['paciente'],
        fecha=data['fecha'],
        hora=data['hora'],
        motivo=data['motivo'],
        estado=data['estado'],
        user_id=user_id
    )
    logger.info(f"Cita creada: {cita.id}")
    return jsonify({'id': cita.id}), 201, {'Content-Type': 'application/json; charset=utf-8'}

@citas_bp.route('/citas/<int:cita_id>', methods=['PUT'])
@jwt_required()
def update_cita(cita_id):
    data = request.get_json()
    cita = service.actualizar_cita(cita_id, data)
    if cita:
        logger.info(f"Cita actualizada: {cita_id}")
        return jsonify({'message': 'Cita actualizada'}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    logger.warning(f"Cita no encontrada para actualizar: {cita_id}")
    return jsonify({'error': 'Cita no encontrada'}), 404, {'Content-Type': 'application/json; charset=utf-8'}

@citas_bp.route('/citas/<int:cita_id>', methods=['DELETE'])
@jwt_required()
def delete_cita(cita_id):
    cita = service.eliminar_cita(cita_id)
    if cita:
        logger.info(f"Cita eliminada: {cita_id}")
        return jsonify({'message': 'Cita eliminada'}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    logger.warning(f"Cita no encontrada para eliminar: {cita_id}")
    return jsonify({'error': 'Cita no encontrada'}), 404, {'Content-Type': 'application/json; charset=utf-8'}
