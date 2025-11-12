"""
Configuración de la aplicación.
Define constantes, configuraciones de base de datos y parámetros del sistema.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # Información de la aplicación
    app_name: str = "API de Música"
    app_version: str = "1.0.0"
    app_description: str = "API RESTful para gestionar usuarios, canciones y favoritos"

    # Base de datos
    database_url: str = "sqlite:///./musica.db"

    # Configuración de servidor
    host: str = "0.0.0.0"
    port: int = 8000

    # Configuración de logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"

    # Configuración de caché
    cache_ttl: int = 300  # Tiempo de vida del caché en segundos

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """
    Obtiene la configuración de la aplicación con caché.
    Se carga una sola vez y se reutiliza.
    """
    return Settings()
