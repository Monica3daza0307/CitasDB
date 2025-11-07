from werkzeug.security import check_password_hash
from config.database import get_db_session
from repositories.users_repository import get_by_username


def authenticate_user(username: str, password: str):
	"""Valida credenciales. Retorna el objeto User si las credenciales son correctas, o None.

	Cierra la sesión antes de retornar.
	"""
	session = get_db_session()
	try:
		user = get_by_username(session, username)
		if not user:
			return None
		if not check_password_hash(user.password, password):
			return None
		return user
	finally:
		session.close()

