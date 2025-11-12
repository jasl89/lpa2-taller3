"""
Script para insertar datos de prueba en la base de datos
Autor: Jhon Salcedo (@jasl89)
"""

from sqlmodel import Session, select

from app.database import engine
from app.models import Cancion, Usuario


def seed_database():
    """Inserta datos de prueba en la base de datos"""

    # Datos de usuarios
    usuarios_data = [
        {
            "nombre": "María García",
            "email": "maria.garcia@email.com",
            "edad": 25,
        },
        {
            "nombre": "Juan Pérez",
            "email": "juan.perez@email.com",
            "edad": 30,
        },
        {
            "nombre": "Ana Rodríguez",
            "email": "ana.rodriguez@email.com",
            "edad": 22,
        },
        {
            "nombre": "Carlos López",
            "email": "carlos.lopez@email.com",
            "edad": 28,
        },
        {
            "nombre": "Laura Martínez",
            "email": "laura.martinez@email.com",
            "edad": 26,
        },
    ]

    # Datos de canciones
    canciones_data = [
        {
            "titulo": "Bohemian Rhapsody",
            "artista": "Queen",
            "album": "A Night at the Opera",
            "duracion": 354,
            "genero": "Rock",
            "anio": 1975,
        },
        {
            "titulo": "Imagine",
            "artista": "John Lennon",
            "album": "Imagine",
            "duracion": 183,
            "genero": "Rock",
            "anio": 1971,
        },
        {
            "titulo": "Billie Jean",
            "artista": "Michael Jackson",
            "album": "Thriller",
            "duracion": 294,
            "genero": "Pop",
            "anio": 1982,
        },
        {
            "titulo": "Stairway to Heaven",
            "artista": "Led Zeppelin",
            "album": "Led Zeppelin IV",
            "duracion": 482,
            "genero": "Rock",
            "anio": 1971,
        },
        {
            "titulo": "Hotel California",
            "artista": "Eagles",
            "album": "Hotel California",
            "duracion": 391,
            "genero": "Rock",
            "anio": 1976,
        },
        {
            "titulo": "Smells Like Teen Spirit",
            "artista": "Nirvana",
            "album": "Nevermind",
            "duracion": 301,
            "genero": "Grunge",
            "anio": 1991,
        },
        {
            "titulo": "Sweet Child O' Mine",
            "artista": "Guns N' Roses",
            "album": "Appetite for Destruction",
            "duracion": 356,
            "genero": "Rock",
            "anio": 1987,
        },
        {
            "titulo": "Wonderwall",
            "artista": "Oasis",
            "album": "(What's the Story) Morning Glory?",
            "duracion": 258,
            "genero": "Rock",
            "anio": 1995,
        },
        {
            "titulo": "Like a Rolling Stone",
            "artista": "Bob Dylan",
            "album": "Highway 61 Revisited",
            "duracion": 369,
            "genero": "Rock",
            "anio": 1965,
        },
        {
            "titulo": "Hey Jude",
            "artista": "The Beatles",
            "album": "Hey Jude",
            "duracion": 431,
            "genero": "Rock",
            "anio": 1968,
        },
    ]

    with Session(engine) as session:
        # Verificar si ya existen datos
        usuarios_existentes = session.exec(select(Usuario)).all()
        canciones_existentes = session.exec(select(Cancion)).all()

        if usuarios_existentes:
            print(f"⚠️  Ya existen {len(usuarios_existentes)} usuarios en la base de datos")
        else:
            # Insertar usuarios
            print("Insertando usuarios...")
            for user_data in usuarios_data:
                usuario = Usuario(**user_data)
                session.add(usuario)
            session.commit()
            print(f"✓ {len(usuarios_data)} usuarios insertados correctamente")

        if canciones_existentes:
            print(f"⚠️  Ya existen {len(canciones_existentes)} canciones en la base de datos")
        else:
            # Insertar canciones
            print("Insertando canciones...")
            for cancion_data in canciones_data:
                cancion = Cancion(**cancion_data)
                session.add(cancion)
            session.commit()
            print(f"✓ {len(canciones_data)} canciones insertadas correctamente")

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
    print("Iniciando inserción de datos de prueba...")
    seed_database()
    print("\n✓ Proceso completado!")
