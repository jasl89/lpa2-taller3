"""
API de Música - Backend
Aplicación principal FastAPI para gestionar usuarios, canciones y favoritos.

Autor: Jhon Salcedo (@jasl89)
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import create_db_and_tables
from app.routers import canciones, favoritos, usuarios

# Configuración
settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor de ciclo de vida de la aplicación.
    Se ejecuta al iniciar y al cerrar la aplicación.
    """
    # Startup: Inicializar logging y base de datos
    logger.info("=== Iniciando API de Música ===")
    logger.info(f"Versión: {settings.app_version}")
    create_db_and_tables()
    logger.info("Aplicación lista para recibir peticiones")

    yield

    # Shutdown: Limpiar recursos
    logger.info("Cerrando aplicación...")


# Crear la instancia de FastAPI con metadatos apropiados
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
    contact={
        "name": "Jhon Salcedo",
        "url": "https://github.com/jasl89",
    },
    license_info={
        "name": "MIT",
    },
)


# Configurar CORS para permitir solicitudes desde diferentes orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Montar archivos estáticos para el frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")


# Incluir los routers
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(canciones.router, prefix="/api/canciones", tags=["Canciones"])
app.include_router(favoritos.router, prefix="/api/favoritos", tags=["Favoritos"])


@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz de la API.
    Retorna información básica y enlaces a la documentación.
    """
    logger.info("Acceso al endpoint raíz")
    return {
        "nombre": settings.app_name,
        "version": settings.app_version,
        "descripcion": settings.app_description,
        "autor": "Jhon Salcedo (@jasl89)",
        "documentacion": "/docs",
        "documentacion_alternativa": "/redoc",
        "frontend": "/static/index.html",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint para verificar el estado de la API.
    Útil para sistemas de monitoreo y orquestación.
    """
    logger.info("Health check realizado")
    return {"status": "healthy", "version": settings.app_version, "database": "sqlite:///musica.db"}


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Iniciando servidor en {settings.host}:{settings.port}")
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level.lower(),
    )
