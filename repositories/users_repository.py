import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from models.users_model import User
from sqlalchemy.orm import Session

class UsersRepository:
    """
    Repositorio para la gestión de usuarios en la API de citas médicas.
    Proporciona métodos para crear, consultar, actualizar y eliminar usuarios.
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_users(self):
        """
        Recupera todos los usuarios registrados en el sistema.
        """
        logger.info("Obteniendo todos los usuarios desde el repositorio")
        return self.db.query(User).all()

    def get_user_by_username(self, username: str):
        """
        Busca y retorna un usuario por su nombre de usuario.
        """
        logger.info(f"Buscando usuario por username: {username}")
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: int):
        """
        Busca y retorna un usuario específico por su ID.
        """
        logger.info(f"Buscando usuario por ID: {user_id}")
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, username: str, password: str, role: str = 'user'):
        """
        Crea y almacena un nuevo usuario en la base de datos.
        """
        logger.info(f"Creando usuario: {username}")
        new_user = User(username=username, password=password, role=role)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_user(self, user_id: int, username: str = None, password: str = None):
        """
        Actualiza la información de un usuario existente.
        """
        user = self.get_user_by_id(user_id)
        if user:
            logger.info(f"Actualizando usuario: {user_id}")
            if username:
                user.username = username
            if password:
                user.password = password
            self.db.commit()
            self.db.refresh(user)
            return user
        logger.warning(f"Usuario no encontrado para actualizar: {user_id}")
        return None

    def delete_user(self, user_id: int):
        """
        Elimina un usuario del sistema por su ID.
        """
        user = self.get_user_by_id(user_id)
        if user:
            logger.info(f"Eliminando usuario: {user_id}")
            self.db.delete(user)
            self.db.commit()
            return user
        logger.warning(f"Usuario no encontrado para eliminar: {user_id}")
        return None
