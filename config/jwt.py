# Configuración de JWT para la API de citas médicas
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_TOKEN_LOCATION = ["headers"]
JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hora
JWT_HEADER_NAME = "Authorization"
JWT_HEADER_TYPE = "Bearer"
