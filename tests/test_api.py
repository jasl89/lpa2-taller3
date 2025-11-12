"""
Tests para la API de Música.
Pruebas unitarias y de integración usando pytest.

Autor: Jhon Salcedo (@jasl89)
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_session
from app.models import Cancion, Usuario
from main import app

# =============================================================================
# CONFIGURACIÓN DE FIXTURES
# =============================================================================


@pytest.fixture(name="session")
def session_fixture():
    """
    Crea una sesión de base de datos en memoria para cada test.
    Se limpia automáticamente después de cada test.
    """
    # Crear engine en memoria para tests
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Crear todas las tablas
    SQLModel.metadata.create_all(engine)

    # Crear sesión
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Crea un cliente de pruebas de FastAPI con la sesión de test.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


@pytest.fixture(name="usuario_test")
def usuario_test_fixture(session: Session):
    """
    Crea un usuario de prueba en la base de datos.
    """
    usuario = Usuario(nombre="Usuario Test", correo="test@example.com")
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@pytest.fixture(name="cancion_test")
def cancion_test_fixture(session: Session):
    """
    Crea una canción de prueba en la base de datos.
    """
    cancion = Cancion(
        titulo="Canción Test",
        artista="Artista Test",
        album="Álbum Test",
        duracion=180,
        año=2020,
        genero="Rock",
    )
    session.add(cancion)
    session.commit()
    session.refresh(cancion)
    return cancion


# =============================================================================
# TESTS DE USUARIOS
# =============================================================================


class TestUsuarios:
    """Tests para los endpoints de usuarios."""

    def test_listar_usuarios(self, client: TestClient):
        """Verifica que se puedan listar usuarios (puede estar vacío)"""
        response = client.get("/api/usuarios/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_crear_usuario(self, client: TestClient):
        """Verifica la creación de un nuevo usuario"""
        usuario_data = {"nombre": "Juan Pérez", "correo": "juan@example.com"}
        response = client.post("/api/usuarios/", json=usuario_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == usuario_data["nombre"]
        assert data["correo"] == usuario_data["correo"]
        assert "id" in data
        assert "fecha_registro" in data

    def test_crear_usuario_correo_duplicado(self, client: TestClient, usuario_test: Usuario):
        """Verifica que no se permiten correos duplicados"""
        usuario_data = {"nombre": "Otro Usuario", "correo": usuario_test.correo}
        response = client.post("/api/usuarios/", json=usuario_data)
        assert response.status_code == 400
        assert "correo electrónico ya está registrado" in response.json()["detail"].lower()

    def test_obtener_usuario(self, client: TestClient, usuario_test: Usuario):
        """Verifica la obtención de un usuario por ID"""
        response = client.get(f"/api/usuarios/{usuario_test.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == usuario_test.id
        assert data["nombre"] == usuario_test.nombre
        assert data["correo"] == usuario_test.correo

    def test_obtener_usuario_no_existe(self, client: TestClient):
        """Verifica error 404 con usuario inexistente"""
        response = client.get("/api/usuarios/99999")
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"].lower()

    def test_actualizar_usuario(self, client: TestClient, usuario_test: Usuario):
        """Verifica la actualización de un usuario"""
        update_data = {"nombre": "Nombre Actualizado"}
        response = client.patch(f"/api/usuarios/{usuario_test.id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == update_data["nombre"]
        assert data["correo"] == usuario_test.correo

    def test_eliminar_usuario(self, client: TestClient, usuario_test: Usuario):
        """Verifica la eliminación de un usuario"""
        response = client.delete(f"/api/usuarios/{usuario_test.id}")
        assert response.status_code == 204

        # Verificar que ya no existe
        response = client.get(f"/api/usuarios/{usuario_test.id}")
        assert response.status_code == 404


# =============================================================================
# TESTS DE CANCIONES
# =============================================================================


class TestCanciones:
    """Tests para los endpoints de canciones."""

    def test_listar_canciones(self, client: TestClient):
        """Verifica que se puedan listar canciones (puede estar vacío)"""
        response = client.get("/api/canciones/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_crear_cancion(self, client: TestClient):
        """Verifica la creación de una nueva canción"""
        cancion_data = {
            "titulo": "Bohemian Rhapsody",
            "artista": "Queen",
            "album": "A Night at the Opera",
            "duracion": 354,
            "año": 1975,
            "genero": "Rock",
        }
        response = client.post("/api/canciones/", json=cancion_data)
        assert response.status_code == 201
        data = response.json()
        assert data["titulo"] == cancion_data["titulo"]
        assert data["artista"] == cancion_data["artista"]
        assert data["duracion"] == cancion_data["duracion"]
        assert "id" in data
        assert "fecha_creacion" in data

    def test_obtener_cancion(self, client: TestClient, cancion_test: Cancion):
        """Verifica la obtención de una canción por ID"""
        response = client.get(f"/api/canciones/{cancion_test.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == cancion_test.id
        assert data["titulo"] == cancion_test.titulo
        assert data["artista"] == cancion_test.artista

    def test_actualizar_cancion(self, client: TestClient, cancion_test: Cancion):
        """Verifica la actualización de una canción"""
        update_data = {"titulo": "Título Actualizado", "año": 2024}
        response = client.patch(f"/api/canciones/{cancion_test.id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["titulo"] == update_data["titulo"]
        assert data["año"] == update_data["año"]
        assert data["artista"] == cancion_test.artista

    def test_eliminar_cancion(self, client: TestClient, cancion_test: Cancion):
        """Verifica la eliminación de una canción"""
        response = client.delete(f"/api/canciones/{cancion_test.id}")
        assert response.status_code == 204

        # Verificar que ya no existe
        response = client.get(f"/api/canciones/{cancion_test.id}")
        assert response.status_code == 404

    def test_filtrar_canciones_por_artista(self, client: TestClient, cancion_test: Cancion):
        """Verifica el filtro de canciones por artista"""
        response = client.get(f"/api/canciones/?artista={cancion_test.artista}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert all(cancion_test.artista in c["artista"] for c in data)

    def test_filtrar_canciones_por_genero(self, client: TestClient, cancion_test: Cancion):
        """Verifica el filtro de canciones por género"""
        response = client.get(f"/api/canciones/?genero={cancion_test.genero}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert all(cancion_test.genero in c["genero"] for c in data)


# =============================================================================
# TESTS DE FAVORITOS
# =============================================================================


class TestFavoritos:
    """Tests para los endpoints de favoritos."""

    def test_listar_favoritos(self, client: TestClient):
        """Verifica que se puedan listar favoritos (puede estar vacío)"""
        response = client.get("/api/favoritos/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_crear_favorito(self, client: TestClient, usuario_test: Usuario, cancion_test: Cancion):
        """Verifica la creación de un favorito"""
        favorito_data = {"usuario_id": usuario_test.id, "cancion_id": cancion_test.id}
        response = client.post("/api/favoritos/", json=favorito_data)
        assert response.status_code == 201
        data = response.json()
        assert data["usuario_id"] == usuario_test.id
        assert data["cancion_id"] == cancion_test.id
        assert "id" in data
        assert "fecha_agregado" in data

    def test_crear_favorito_duplicado(
        self, client: TestClient, usuario_test: Usuario, cancion_test: Cancion
    ):
        """Verifica que no se permiten favoritos duplicados"""
        favorito_data = {"usuario_id": usuario_test.id, "cancion_id": cancion_test.id}
        # Crear el primer favorito
        response = client.post("/api/favoritos/", json=favorito_data)
        assert response.status_code == 201

        # Intentar crear el mismo favorito de nuevo
        response = client.post("/api/favoritos/", json=favorito_data)
        assert response.status_code == 400
        assert "ya está en los favoritos" in response.json()["detail"].lower()

    def test_listar_favoritos_usuario(
        self, client: TestClient, usuario_test: Usuario, cancion_test: Cancion
    ):
        """Verifica que se puedan listar los favoritos de un usuario"""
        # Crear un favorito primero
        favorito_data = {"usuario_id": usuario_test.id, "cancion_id": cancion_test.id}
        client.post("/api/favoritos/", json=favorito_data)

        # Listar favoritos del usuario
        response = client.get(f"/api/favoritos/usuario/{usuario_test.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["usuario_id"] == usuario_test.id
        assert "cancion" in data[0]

    def test_eliminar_favorito(
        self, client: TestClient, usuario_test: Usuario, cancion_test: Cancion
    ):
        """Verifica la eliminación de un favorito"""
        # Crear un favorito primero
        favorito_data = {"usuario_id": usuario_test.id, "cancion_id": cancion_test.id}
        response = client.post("/api/favoritos/", json=favorito_data)
        favorito_id = response.json()["id"]

        # Eliminar el favorito
        response = client.delete(f"/api/favoritos/{favorito_id}")
        assert response.status_code == 204

        # Verificar que ya no existe
        response = client.get(f"/api/favoritos/usuario/{usuario_test.id}")
        data = response.json()
        assert len(data) == 0

    def test_eliminar_favorito_por_usuario_cancion(
        self, client: TestClient, usuario_test: Usuario, cancion_test: Cancion
    ):
        """Verifica la eliminación de un favorito por usuario y canción"""
        # Crear un favorito primero
        favorito_data = {"usuario_id": usuario_test.id, "cancion_id": cancion_test.id}
        client.post("/api/favoritos/", json=favorito_data)

        # Eliminar el favorito por usuario y canción
        response = client.delete(
            f"/api/favoritos/usuario/{usuario_test.id}/cancion/{cancion_test.id}"
        )
        assert response.status_code == 204

        # Verificar que ya no existe
        response = client.get(f"/api/favoritos/usuario/{usuario_test.id}")
        data = response.json()
        assert len(data) == 0


# =============================================================================
# TESTS ADICIONALES
# =============================================================================


class TestEndpointsBasicos:
    """Tests para endpoints básicos de la API."""

    def test_root_endpoint(self, client: TestClient):
        """Verifica el endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "nombre" in data
        assert "version" in data
        assert "autor" in data

    def test_health_check(self, client: TestClient):
        """Verifica el endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestIntegracion:
    """Tests de integración que prueban flujos completos."""

    # TODO: Test de flujo completo: crear usuario, canción y marcar favorito
    def test_flujo_completo(self, client: TestClient):
        """Test que verifica el flujo completo de la aplicación"""
        # 1. Crear usuario

        # 2. Crear canción

        # 3. Marcar como favorito

        # 4. Verificar que aparece en favoritos del usuario

        pass


# =============================================================================
# TESTS DE VALIDACIÓN
# =============================================================================


class TestValidacion:
    """Tests para validaciones de datos."""

    # TODO: Test para validar email inválido
    def test_email_invalido(self, client: TestClient):
        """Test para verificar validación de email"""

        pass

    # TODO: Test para validar año de canción
    def test_año_cancion_invalido(self, client: TestClient):
        """Test para verificar validación de año"""

        pass

    # TODO: Test para validar campos requeridos
    def test_campos_requeridos(self, client: TestClient):
        """Test para verificar que los campos requeridos son obligatorios"""

        pass
