from flask import Blueprint, request, jsonify
from services.users_services import authenticate_user
from config.jwt import create_access_token, JWT_HEADER_TYPE

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/login', methods=['POST'])
def login():
	data = request.get_json() or {}
	username = data.get('username')
	password = data.get('password')

	if not username or not password:
		return jsonify({"msg": "username and password required"}), 400

	user = authenticate_user(username, password)
	if not user:
		return jsonify({"msg": "Invalid credentials"}), 401

	identity = {"id": user.id, "username": user.username}
	token = create_access_token(identity)
	return jsonify({"access_token": token, "token_type": JWT_HEADER_TYPE, "user": identity}), 200
