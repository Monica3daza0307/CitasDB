# controllers/cita_controller.py
from flask import Blueprint, request, jsonify
from services.cita_service import CitaService

cita_bp = Blueprint('cita_bp', __name__)
service = CitaService()

@cita_bp.route('/citas', methods=['GET'])
def get_citas():
    return jsonify([c.to_dict() for c in service.listar()])

@cita_bp.route('/citas/<int:cita_id>', methods=['GET'])
def get_cita(cita_id):
    cita = service.obtener(cita_id)
    if not cita:
        return jsonify({'error': 'Cita no encontrada'}), 404
    return jsonify(cita.to_dict())

@cita_bp.route('/citas', methods=['POST'])
def create_cita():
    data = request.get_json()
    cita = service.crear(data)
    return jsonify(cita.to_dict()), 201

@cita_bp.route('/citas/<int:cita_id>', methods=['PUT'])
def update_cita(cita_id):
    data = request.get_json()
    cita = service.actualizar(cita_id, data)
    if not cita:
        return jsonify({'error': 'Cita no encontrada'}), 404
    return jsonify(cita.to_dict())

@cita_bp.route('/citas/<int:cita_id>', methods=['DELETE'])
def delete_cita(cita_id):
    if service.eliminar(cita_id):
        return jsonify({'mensaje': 'Cita eliminada'})
    return jsonify({'error': 'Cita no encontrada'}), 404