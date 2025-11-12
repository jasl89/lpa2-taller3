"""
Script para limpiar y reinsertar datos en la base de datos
Autor: Jhon Salcedo (@jasl89)
"""

from sqlmodel import Session, select

from app.database import engine
from app.models import Cancion, Favorito, Usuario


def clean_and_seed():
    """Limpia la base de datos y inserta datos de prueba"""

    # Datos de usuarios
    usuarios_data = [
        {
            "nombre": "María García",
            "correo": "maria.garcia@email.com",
        },
        {
            "nombre": "Juan Pérez",
            "correo": "juan.perez@email.com",
        },
        {
            "nombre": "Ana Rodríguez",
            "correo": "ana.rodriguez@email.com",
        },
        {
            "nombre": "Carlos López",
            "correo": "carlos.lopez@email.com",
        },
        {
            "nombre": "Laura Martínez",
            "correo": "laura.martinez@email.com",
        },
    ]

    # Datos de canciones colombianas reconocidas
    canciones_data = [
        {
            "titulo": "La Tierra del Olvido",
            "artista": "Carlos Vives",
            "album": "La Tierra del Olvido",
            "duracion": 252,
            "genero": "Vallenato",
            "anio": 1995,
        },
        {
            "titulo": "A Dios le Pido",
            "artista": "Juanes",
            "album": "Un Día Normal",
            "duracion": 207,
            "genero": "Rock Latino",
            "anio": 2002,
        },
        {
            "titulo": "La Camisa Negra",
            "artista": "Juanes",
            "album": "Mi Sangre",
            "duracion": 213,
            "genero": "Pop Rock",
            "anio": 2004,
        },
        {
            "titulo": "Fruta Fresca",
            "artista": "Carlos Vives",
            "album": "Fruta Fresca",
            "duracion": 234,
            "genero": "Vallenato",
            "anio": 1999,
        },
        {
            "titulo": "Robarte un Beso",
            "artista": "Carlos Vives",
            "album": "Vives",
            "duracion": 233,
            "genero": "Vallenato Pop",
            "anio": 2017,
        },
        {
            "titulo": "Cali Pachanguero",
            "artista": "Grupo Niche",
            "album": "Al Pasito",
            "duracion": 318,
            "genero": "Salsa",
            "anio": 1984,
        },
        {
            "titulo": "Yo Te Esperaré",
            "artista": "Cali y El Dandee",
            "album": "Yo Te Esperaré",
            "duracion": 192,
            "genero": "Pop",
            "anio": 2012,
        },
        {
            "titulo": "Traicionera",
            "artista": "Sebastián Yatra",
            "album": "Mantra",
            "duracion": 198,
            "genero": "Pop Latino",
            "anio": 2016,
        },
        {
            "titulo": "La Gota Fría",
            "artista": "Carlos Vives",
            "album": "Clásicos de la Provincia",
            "duracion": 267,
            "genero": "Vallenato",
            "anio": 1993,
        },
        {
            "titulo": "Gotas de Lluvia",
            "artista": "Grupo Niche",
            "album": "Cielo de Tambores",
            "duracion": 294,
            "genero": "Salsa",
            "anio": 1990,
        },
    ]

    with Session(engine) as session:
        # Limpiar datos existentes
        print("Limpiando base de datos...")

        # Eliminar favoritos primero (por las foreign keys)
        favoritos = session.exec(select(Favorito)).all()
        for favorito in favoritos:
            session.delete(favorito)

        # Eliminar usuarios
        usuarios = session.exec(select(Usuario)).all()
        for usuario in usuarios:
            session.delete(usuario)

        # Eliminar canciones
        canciones = session.exec(select(Cancion)).all()
        for cancion in canciones:
            session.delete(cancion)

        session.commit()
        print("Base de datos limpiada")

        # Insertar usuarios
        print("\nInsertando usuarios...")
        for user_data in usuarios_data:
            usuario = Usuario(**user_data)
            session.add(usuario)
        session.commit()
        print(f"✓ {len(usuarios_data)} usuarios insertados")

        # Insertar canciones
        print("\nInsertando canciones...")
        for cancion_data in canciones_data:
            cancion = Cancion(**cancion_data)
            session.add(cancion)
        session.commit()
        print(f"✓ {len(canciones_data)} canciones insertadas")

        # Mostrar resumen
        total_usuarios = len(session.exec(select(Usuario)).all())
        total_canciones = len(session.exec(select(Cancion)).all())

        print("\n" + "=" * 50)
        print("RESUMEN DE LA BASE DE DATOS")
        print("=" * 50)
        print(f"Total de usuarios: {total_usuarios}")
        print(f"Total de canciones: {total_canciones}")
        print("=" * 50)


if __name__ == "__main__":
    print("Iniciando limpieza y carga de datos...")
    clean_and_seed()
    print("\n✓ Proceso completado!")
