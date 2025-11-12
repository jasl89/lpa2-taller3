"""
Sistema de logging centralizado.
Configura el logging para toda la aplicación.
"""

import logging
import sys
from pathlib import Path

from app.config import get_settings

settings = get_settings()


def setup_logging():
    """
    Configura el sistema de logging de la aplicación.
    Los logs se escriben tanto en archivo como en consola.
    """
    # Crear directorio de logs si no existe
    log_dir = Path(settings.log_file).parent
    log_dir.mkdir(exist_ok=True)

    # Configurar formato de logs
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configurar el logger raíz
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format=log_format,
        datefmt=date_format,
        handlers=[
            # Handler para archivo
            logging.FileHandler(settings.log_file, encoding="utf-8"),
            # Handler para consola
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Logger específico para la aplicación
    logger = logging.getLogger("app")
    logger.info("Sistema de logging inicializado")
    logger.info(f"Logs guardados en: {settings.log_file}")

    return logger


# Inicializar logging al importar el módulo
logger = setup_logging()
