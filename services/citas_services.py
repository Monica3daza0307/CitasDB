import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from repositories.cita_repository import CitaRepository
from models.cita_model import Cita
from sqlalchemy.orm import Session

"""
Librerías utilizadas:
- repositories.cita_repository: Proporciona la clase CitaRepository para la gestión de citas médicas en la base de datos.
- models.cita_model: Define el modelo Cita que representa la entidad de cita médica.
- sqlalchemy.orm.Session: Permite manejar la sesión de la base de datos para realizar operaciones transaccionales.
"""

class CitaService:
    """
    Capa de servicios para la gestión de citas médicas.
    Esta clase orquesta la lógica de negocio relacionada con las citas,
    utilizando el repositorio para acceder a los datos.
    Permite mantener la lógica de negocio separada de la capa de acceso a datos.
    """

    def __init__(self, db_session: Session):
        """
        Inicializa el servicio de citas con una sesión de base de datos y un repositorio de citas.
        """
        self.repository = CitaRepository(db_session)
        logger.info("Servicio de citas inicializado")

    def listar_citas(self):
        """
        Recupera y retorna todas las citas registradas en el sistema.
        Utiliza el repositorio para obtener la lista completa.
        """
        logger.info("Listando todas las citas")
        return self.repository.get_all_citas()

    def obtener_cita(self, cita_id: int):
        """
        Busca y retorna una cita específica por su identificador único (ID).
        """
        logger.info(f"Obteniendo cita por ID: {cita_id}")
        return self.repository.get_cita_by_id(cita_id)

    def crear_cita(self, paciente: str, fecha, hora, motivo: str, estado: str, user_id: int):
        """
        Crea una nueva cita con los datos proporcionados.
        """
        logger.info(f"Creando cita para paciente: {paciente}")
        return self.repository.create_cita(paciente, fecha, hora, motivo, estado, user_id)

    def actualizar_cita(self, cita_id: int, data: dict):
        """
        Actualiza la información de una cita existente.
        """
        logger.info(f"Actualizando cita: {cita_id}")
        return self.repository.update_cita(cita_id, data)

    def eliminar_cita(self, cita_id: int):
        """
        Elimina una cita del sistema según su identificador único (ID).
        """
        logger.info(f"Eliminando cita: {cita_id}")
        return self.repository.delete_cita(cita_id)
