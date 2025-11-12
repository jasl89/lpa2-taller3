"""
Router de Favoritos.
Endpoints para gestionar las canciones favoritas de los usuarios.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.cache import CacheManager
from app.database import get_session
from app.models import (
    Cancion,
    CancionRead,
    Favorito,
    FavoritoConDetalles,
    FavoritoCreate,
    FavoritoRead,
    Usuario,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=FavoritoRead, status_code=status.HTTP_201_CREATED)
def agregar_favorito(favorito: FavoritoCreate, session: Session = Depends(get_session)) -> Favorito:
    """
    Agrega una canción a los favoritos de un usuario.

    - **usuario_id**: ID del usuario
    - **cancion_id**: ID de la canción
    """
    logger.info(f"Agregando favorito: Usuario {favorito.usuario_id}, Canción {favorito.cancion_id}")

    # Verificar que el usuario existe
    usuario = session.get(Usuario, favorito.usuario_id)
    if not usuario:
        logger.warning(f"Usuario no encontrado: {favorito.usuario_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    # Verificar que la canción existe
    cancion = session.get(Cancion, favorito.cancion_id)
    if not cancion:
        logger.warning(f"Canción no encontrada: {favorito.cancion_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Canción no encontrada")

    # Verificar que no existe ya este favorito
    statement = select(Favorito).where(
        Favorito.usuario_id == favorito.usuario_id, Favorito.cancion_id == favorito.cancion_id
    )
    existing = session.exec(statement).first()
    if existing:
        logger.warning(
            f"Favorito ya existe: Usuario {favorito.usuario_id}, Canción {favorito.cancion_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta canción ya está en los favoritos del usuario",
        )

    # Crear favorito
    db_favorito = Favorito.model_validate(favorito)
    session.add(db_favorito)
    session.commit()
    session.refresh(db_favorito)

    # Limpiar caché
    CacheManager.clear_all()

    logger.info(f"Favorito agregado exitosamente con ID: {db_favorito.id}")
    return db_favorito


@router.get("/usuario/{usuario_id}", response_model=list[FavoritoConDetalles])
def listar_favoritos_usuario(
    usuario_id: int, session: Session = Depends(get_session)
) -> list[dict]:
    """
    Lista todos los favoritos de un usuario con detalles de las canciones.
    """
    logger.info(f"Listando favoritos del usuario: {usuario_id}")

    # Verificar que el usuario existe
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        logger.warning(f"Usuario no encontrado: {usuario_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    # Obtener favoritos con detalles de canciones
    statement = select(Favorito, Cancion).where(
        Favorito.usuario_id == usuario_id, Favorito.cancion_id == Cancion.id
    )
    results = session.exec(statement).all()

    # Construir respuesta con detalles
    favoritos_detallados = []
    for favorito, cancion in results:
        favorito_detalle = {
            "id": favorito.id,
            "usuario_id": favorito.usuario_id,
            "cancion_id": favorito.cancion_id,
            "fecha_agregado": favorito.fecha_agregado,
            "cancion": CancionRead.model_validate(cancion),
        }
        favoritos_detallados.append(favorito_detalle)

    logger.info(
        f"Se encontraron {len(favoritos_detallados)} favoritos para el usuario {usuario_id}"
    )
    return favoritos_detallados


@router.get("/", response_model=list[FavoritoRead])
def listar_todos_favoritos(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
) -> list[Favorito]:
    """
    Lista todos los favoritos con paginación.

    - **skip**: Número de registros a saltar
    - **limit**: Número máximo de registros a retornar
    """
    logger.info(f"Listando todos los favoritos (skip={skip}, limit={limit})")
    statement = select(Favorito).offset(skip).limit(limit)
    favoritos = session.exec(statement).all()
    logger.info(f"Se encontraron {len(favoritos)} favoritos")
    return favoritos


@router.delete("/{favorito_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_favorito(favorito_id: int, session: Session = Depends(get_session)) -> None:
    """
    Elimina un favorito específico.
    """
    logger.info(f"Eliminando favorito: {favorito_id}")

    favorito = session.get(Favorito, favorito_id)
    if not favorito:
        logger.warning(f"Favorito no encontrado: {favorito_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorito no encontrado")

    session.delete(favorito)
    session.commit()

    # Limpiar caché
    CacheManager.clear_all()

    logger.info(f"Favorito eliminado exitosamente: {favorito_id}")


@router.delete("/usuario/{usuario_id}/cancion/{cancion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_favorito_por_usuario_cancion(
    usuario_id: int, cancion_id: int, session: Session = Depends(get_session)
) -> None:
    """
    Elimina un favorito específico por usuario y canción.
    """
    logger.info(f"Eliminando favorito: Usuario {usuario_id}, Canción {cancion_id}")

    statement = select(Favorito).where(
        Favorito.usuario_id == usuario_id, Favorito.cancion_id == cancion_id
    )
    favorito = session.exec(statement).first()

    if not favorito:
        logger.warning(f"Favorito no encontrado: Usuario {usuario_id}, Canción {cancion_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorito no encontrado")

    session.delete(favorito)
    session.commit()

    # Limpiar caché
    CacheManager.clear_all()

    logger.info(f"Favorito eliminado exitosamente: Usuario {usuario_id}, Canción {cancion_id}")
