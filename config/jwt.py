# config/jwt.py

import os
from datetime import datetime, timedelta
import jwt

# Configuración de JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")
JWT_TOKEN_LOCATION = ["headers"]
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))  # segundos (por defecto 1 hora)
JWT_HEADER_NAME = "Authorization"
JWT_HEADER_TYPE = "Bearer"


def create_access_token(identity: dict):
	"""Genera un JWT firmado con la identidad proporcionada.
	identity: diccionario con los datos mínimos del usuario (por ejemplo id y username).
	Retorna el token como string.
	"""
	payload = {
		"sub": identity,
		"iat": datetime.utcnow(),
		"exp": datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRES),
	}
	token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
	# pyjwt >=2 devuelve str, versiones antiguas bytes
	if isinstance(token, bytes):
		token = token.decode("utf-8")
	return token


def decode_token(token: str):
	"""Decodifica y valida un token JWT. Retorna el payload o None si es inválido/expirado."""
	try:
		payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
		return payload
	except jwt.ExpiredSignatureError:
		return None
	except jwt.InvalidTokenError:
		return None
