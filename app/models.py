"""
Modelos de datos de la API de Música.
Define las tablas de Usuario, Cancion y Favorito usando SQLModel.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

# =============================================================================
# MODELO: USUARIO
# =============================================================================


class UsuarioBase(SQLModel):
    """Modelo base para Usuario con validaciones"""

    nombre: str = Field(min_length=1, max_length=100, description="Nombre del usuario")
    correo: str = Field(
        min_length=3,
        max_length=100,
        description="Correo electrónico único",
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    )


class Usuario(UsuarioBase, table=True):
    """Modelo de tabla Usuario"""

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_registro: datetime = Field(default_factory=datetime.now)

    # Relación con favoritos
    favoritos: list["Favorito"] = Relationship(back_populates="usuario")


class UsuarioCreate(UsuarioBase):
    """Esquema para crear un usuario"""

    pass


class UsuarioRead(UsuarioBase):
    """Esquema para leer un usuario"""

    id: int
    fecha_registro: datetime


class UsuarioUpdate(SQLModel):
    """Esquema para actualizar un usuario"""

    nombre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    correo: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100,
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    )


# =============================================================================
# MODELO: CANCIÓN
# =============================================================================


class CancionBase(SQLModel):
    """Modelo base para Canción con validaciones"""

    titulo: str = Field(min_length=1, max_length=200, description="Título de la canción")
    artista: str = Field(min_length=1, max_length=100, description="Artista o intérprete")
    album: Optional[str] = Field(default=None, max_length=200, description="Álbum")
    duracion: int = Field(gt=0, description="Duración en segundos")
    año: Optional[int] = Field(default=None, ge=1900, le=2100, description="Año de lanzamiento")
    genero: Optional[str] = Field(default=None, max_length=50, description="Género musical")


class Cancion(CancionBase, table=True):
    """Modelo de tabla Canción"""

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_creacion: datetime = Field(default_factory=datetime.now)

    # Relación con favoritos
    favoritos: list["Favorito"] = Relationship(back_populates="cancion")


class CancionCreate(CancionBase):
    """Esquema para crear una canción"""

    pass


class CancionRead(CancionBase):
    """Esquema para leer una canción"""

    id: int
    fecha_creacion: datetime


class CancionUpdate(SQLModel):
    """Esquema para actualizar una canción"""

    titulo: Optional[str] = Field(default=None, min_length=1, max_length=200)
    artista: Optional[str] = Field(default=None, min_length=1, max_length=100)
    album: Optional[str] = Field(default=None, max_length=200)
    duracion: Optional[int] = Field(default=None, gt=0)
    año: Optional[int] = Field(default=None, ge=1900, le=2100)
    genero: Optional[str] = Field(default=None, max_length=50)


# =============================================================================
# MODELO: FAVORITO
# =============================================================================


class FavoritoBase(SQLModel):
    """Modelo base para Favorito"""

    usuario_id: int = Field(foreign_key="usuario.id")
    cancion_id: int = Field(foreign_key="cancion.id")


class Favorito(FavoritoBase, table=True):
    """Modelo de tabla Favorito"""

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_agregado: datetime = Field(default_factory=datetime.now)

    # Relaciones
    usuario: Optional[Usuario] = Relationship(back_populates="favoritos")
    cancion: Optional[Cancion] = Relationship(back_populates="favoritos")


class FavoritoCreate(FavoritoBase):
    """Esquema para crear un favorito"""

    pass


class FavoritoRead(FavoritoBase):
    """Esquema para leer un favorito"""

    id: int
    fecha_agregado: datetime


class FavoritoConDetalles(SQLModel):
    """Esquema para leer un favorito con detalles de la canción"""

    id: int
    usuario_id: int
    cancion_id: int
    fecha_agregado: datetime
    cancion: CancionRead
