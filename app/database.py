"""
Configuración de la base de datos.
Gestiona la conexión a SQLite y la creación de tablas.
"""

import logging

from sqlmodel import Session, SQLModel, create_engine

from app.config import get_settings

# Configuración
settings = get_settings()

# Logger
logger = logging.getLogger(__name__)

# Motor de base de datos
engine = create_engine(
    settings.database_url,
    echo=False,  # Cambiar a True para ver las queries SQL en desarrollo
    connect_args={"check_same_thread": False},  # Necesario para SQLite
)


def create_db_and_tables():
    """
    Crea todas las tablas definidas en los modelos.
    Se ejecuta al iniciar la aplicación.
    """
    logger.info("Creando tablas en la base de datos...")
    SQLModel.metadata.create_all(engine)
    logger.info("Tablas creadas exitosamente")


def get_session():
    """
    Generador de sesión de base de datos.
    Se usa como dependencia en FastAPI para inyectar la sesión.
    """
    with Session(engine) as session:
        yield session
