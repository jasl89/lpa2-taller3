"""
Router de Usuarios.
Endpoints CRUD para gestionar usuarios.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.cache import CacheManager
from app.database import get_session
from app.models import Usuario, UsuarioCreate, UsuarioRead, UsuarioUpdate

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, session: Session = Depends(get_session)) -> Usuario:
    """
    Crea un nuevo usuario.

    - **nombre**: Nombre del usuario
    - **correo**: Correo electrónico único
    """
    logger.info(f"Creando usuario: {usuario.nombre}")

    # Verificar que el correo no exista
    statement = select(Usuario).where(Usuario.correo == usuario.correo)
    existing = session.exec(statement).first()
    if existing:
        logger.warning(f"Intento de crear usuario con correo duplicado: {usuario.correo}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        )

    # Crear usuario
    db_usuario = Usuario.model_validate(usuario)
    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)

    # Limpiar caché
    CacheManager.clear_all()

    logger.info(f"Usuario creado exitosamente con ID: {db_usuario.id}")
    return db_usuario


@router.get("/", response_model=list[UsuarioRead])
def listar_usuarios(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
) -> list[Usuario]:
    """
    Lista todos los usuarios con paginación.

    - **skip**: Número de registros a saltar
    - **limit**: Número máximo de registros a retornar
    """
    logger.info(f"Listando usuarios (skip={skip}, limit={limit})")
    statement = select(Usuario).offset(skip).limit(limit)
    usuarios = session.exec(statement).all()
    logger.info(f"Se encontraron {len(usuarios)} usuarios")
    return usuarios


@router.get("/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: int, session: Session = Depends(get_session)) -> Usuario:
    """
    Obtiene un usuario específico por su ID.
    """
    logger.info(f"Buscando usuario con ID: {usuario_id}")
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        logger.warning(f"Usuario no encontrado: {usuario_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario


@router.patch("/{usuario_id}", response_model=UsuarioRead)
def actualizar_usuario(
    usuario_id: int, usuario_update: UsuarioUpdate, session: Session = Depends(get_session)
) -> Usuario:
    """
    Actualiza un usuario existente.
    Solo se actualizan los campos proporcionados.
    """
    logger.info(f"Actualizando usuario: {usuario_id}")

    # Obtener usuario
    db_usuario = session.get(Usuario, usuario_id)
    if not db_usuario:
        logger.warning(f"Usuario no encontrado: {usuario_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    # Verificar correo único si se está actualizando
    if usuario_update.correo:
        statement = select(Usuario).where(
            Usuario.correo == usuario_update.correo, Usuario.id != usuario_id
        )
        existing = session.exec(statement).first()
        if existing:
            logger.warning(f"Intento de actualizar con correo duplicado: {usuario_update.correo}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado",
            )

    # Actualizar campos
    update_data = usuario_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_usuario, key, value)

    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)

    # Limpiar caché
    CacheManager.clear_all()

    logger.info(f"Usuario actualizado exitosamente: {usuario_id}")
    return db_usuario


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(usuario_id: int, session: Session = Depends(get_session)) -> None:
    """
    Elimina un usuario y todos sus favoritos asociados.
    """
    logger.info(f"Eliminando usuario: {usuario_id}")

    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        logger.warning(f"Usuario no encontrado: {usuario_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    session.delete(usuario)
    session.commit()

    # Limpiar caché
    CacheManager.clear_all()

    logger.info(f"Usuario eliminado exitosamente: {usuario_id}")
