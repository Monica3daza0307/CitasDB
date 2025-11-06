import logging
from repositories.users_repository import UsersRepository
from models.users_model import User
from werkzeug.security import generate_password_hash, check_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UsersService:
    """
    Capa de servicios para la gestión de usuarios en la API de citas médicas.
    Encapsula la lógica de negocio relacionada con autenticación, registro y administración de usuarios.
    """

    def __init__(self, db_session):
        self.users_repository = UsersRepository(db_session)

    def authenticate_user(self, username: str, password: str):
        """
        Verifica las credenciales del usuario y retorna el usuario si son válidas.
        """
        user = self.users_repository.get_user_by_username(username)
        logger.info(f"Autenticando usuario: {username}")
        if user and check_password_hash(user.password, password):
            logger.info(f"Usuario autenticado correctamente: {username}")
            return user
        logger.warning(f"Intento fallido de autenticación: {username}")
        return None

    def get_all_users(self):
        """
        Retorna todos los usuarios registrados.
        """
        logger.info("Consultando todos los usuarios")
        return self.users_repository.get_all_users()

    def get_user_by_id(self, user_id: int):
        """
        Retorna un usuario por su ID.
        """
        logger.info(f"Consultando usuario por ID: {user_id}")
        return self.users_repository.get_user_by_id(user_id)

    def create_user(self, username: str, password: str):
        """
        Crea un nuevo usuario con contraseña encriptada.
        """
        password_hashed = generate_password_hash(password)
        logger.info(f"Creando usuario: {username}")
        return self.users_repository.create_user(username, password_hashed)

    def update_user(self, user_id: int, username: str = None, password: str = None):
        """
        Actualiza el nombre de usuario y/o contraseña.
        """
        logger.info(f"Actualizando usuario: {user_id}")
        if password:
            password = generate_password_hash(password)
        return self.users_repository.update_user(user_id, username, password)

    def delete_user(self, user_id: int):
        """
        Elimina un usuario por su ID.
        """
        logger.info(f"Eliminando usuario: {user_id}")
        return self.users_repository.delete_user(user_id)

    def user_exists(self, username: str):
        """
        Verifica si un usuario ya existe por nombre.
        """
        logger.info(f"Verificando existencia de usuario: {username}")
        return self.users_repository.get_user_by_username(username) is not None
