import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from models.cita_model import Cita
from sqlalchemy.orm import Session

class CitaRepository:
    """
    Repositorio para la gestión de citas médicas en la base de datos.
    Proporciona métodos para crear, consultar, actualizar y eliminar citas.
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_citas(self):
        """
        Recupera todas las citas almacenadas en la base de datos.
        """
        logger.info("Obteniendo todas las citas desde el repositorio")
        return self.db.query(Cita).all()

    def get_cita_by_id(self, cita_id: int):
        """
        Busca y retorna una cita específica según su ID.
        """
        logger.info(f"Buscando cita por ID: {cita_id}")
        return self.db.query(Cita).filter(Cita.id == cita_id).first()

    def create_cita(self, paciente: str, fecha, hora, motivo: str, estado: str, user_id: int):
        """
        Crea y almacena una nueva cita en la base de datos.
        """
        logger.info(f"Creando cita para paciente: {paciente}")
        nueva_cita = Cita(
            paciente=paciente,
            fecha=fecha,
            hora=hora,
            motivo=motivo,
            estado=estado,
            user_id=user_id
        )
        self.db.add(nueva_cita)
        self.db.commit()
        self.db.refresh(nueva_cita)
        return nueva_cita

    def update_cita(self, cita_id: int, data: dict):
        """
        Actualiza la información de una cita existente.
        """
        cita = self.get_cita_by_id(cita_id)
        if cita:
            logger.info(f"Actualizando cita: {cita_id}")
            for key, value in data.items():
                if hasattr(cita, key):
                    setattr(cita, key, value)
            self.db.commit()
            self.db.refresh(cita)
        else:
            logger.warning(f"Cita no encontrada para actualizar: {cita_id}")
        return cita

    def delete_cita(self, cita_id: int):
        """
        Elimina una cita de la base de datos según su ID.
        """
        cita = self.get_cita_by_id(cita_id)
        if cita:
            logger.info(f"Eliminando cita: {cita_id}")
            self.db.delete(cita)
            self.db.commit()
        else:
            logger.warning(f"Cita no encontrada para eliminar: {cita_id}")
        return cita
