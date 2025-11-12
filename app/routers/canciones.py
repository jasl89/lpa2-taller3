"""
Router de Canciones.
Endpoints CRUD para gestionar canciones.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.cache import CacheManager
from app.database import get_session
from app.models import Cancion, CancionCreate, CancionRead, CancionUpdate

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=CancionRead, status_code=status.HTTP_201_CREATED)
def crear_cancion(cancion: CancionCreate, session: Session = Depends(get_session)) -> Cancion:
    """
    Crea una nueva canción.

    - **titulo**: Título de la canción
    - **artista**: Artista o intérprete
    - **album**: Álbum al que pertenece (opcional)
    - **duracion**: Duración en segundos
    - **año**: Año de lanzamiento (opcional)
    - **genero**: Género musical (opcional)
    """
    logger.info(f"Creando canción: {cancion.titulo} - {cancion.artista}")

    db_cancion = Cancion.model_validate(cancion)
    session.add(db_cancion)
    session.commit()
    session.refresh(db_cancion)

    # Limpiar caché
    CacheManager.clear_all()

    logger.info(f"Canción creada exitosamente con ID: {db_cancion.id}")
    return db_cancion


@router.get("/", response_model=list[CancionRead])
def listar_canciones(
    skip: int = 0,
    limit: int = 100,
    artista: Optional[str] = Query(None, description="Filtrar por artista"),
    genero: Optional[str] = Query(None, description="Filtrar por género"),
    session: Session = Depends(get_session),
) -> list[Cancion]:
    """
    Lista todas las canciones con paginación y filtros opcionales.

    - **skip**: Número de registros a saltar
    - **limit**: Número máximo de registros a retornar
    - **artista**: Filtrar por nombre de artista (opcional)
    - **genero**: Filtrar por género musical (opcional)
    """
    logger.info(
        f"Listando canciones (skip={skip}, limit={limit}, artista={artista}, genero={genero})"
    )

    statement = select(Cancion)

    # Aplicar filtros
    if artista:
        statement = statement.where(Cancion.artista.contains(artista))
    if genero:
        statement = statement.where(Cancion.genero.contains(genero))

    statement = statement.offset(skip).limit(limit)
    canciones = session.exec(statement).all()

    logger.info(f"Se encontraron {len(canciones)} canciones")
    return canciones


@router.get("/{cancion_id}", response_model=CancionRead)
def obtener_cancion(cancion_id: int, session: Session = Depends(get_session)) -> Cancion:
    """
    Obtiene una canción específica por su ID.
    """
    logger.info(f"Buscando canción con ID: {cancion_id}")
    cancion = session.get(Cancion, cancion_id)
    if not cancion:
        logger.warning(f"Canción no encontrada: {cancion_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Canción no encontrada")
    return cancion


@router.patch("/{cancion_id}", response_model=CancionRead)
def actualizar_cancion(
    cancion_id: int, cancion_update: CancionUpdate, session: Session = Depends(get_session)
) -> Cancion:
    """
    Actualiza una canción existente.
    Solo se actualizan los campos proporcionados.
    """
    logger.info(f"Actualizando canción: {cancion_id}")

    db_cancion = session.get(Cancion, cancion_id)
    if not db_cancion:
        logger.warning(f"Canción no encontrada: {cancion_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Canción no encontrada")

    # Actualizar campos
    update_data = cancion_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cancion, key, value)

    session.add(db_cancion)
    session.commit()
    session.refresh(db_cancion)

    # Limpiar caché
    CacheManager.clear_all()

    logger.info(f"Canción actualizada exitosamente: {cancion_id}")
    return db_cancion


@router.delete("/{cancion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cancion(cancion_id: int, session: Session = Depends(get_session)) -> None:
    """
    Elimina una canción y todos sus registros de favoritos asociados.
    """
    logger.info(f"Eliminando canción: {cancion_id}")

    cancion = session.get(Cancion, cancion_id)
    if not cancion:
        logger.warning(f"Canción no encontrada: {cancion_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Canción no encontrada")

    session.delete(cancion)
    session.commit()

    # Limpiar caché
    CacheManager.clear_all()

    logger.info(f"Canción eliminada exitosamente: {cancion_id}")
