# API de Música

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![SQLModel](https://img.shields.io/badge/SQLModel-0.0.14-red.svg)](https://sqlmodel.tiangolo.com/)
[![Ruff](https://img.shields.io/badge/Ruff-0.1.9-black.svg)](https://github.com/astral-sh/ruff)

Una API RESTful completa para gestionar usuarios, canciones y favoritos. Desarrollada con FastAPI, SQLModel y Pydantic.

**Estudiante:** Jhon Salcedo
**GitHub:** [@jasl89](https://github.com/jasl89)
**Repositorio:** [https://github.com/jasl89/lpa2-taller3](https://github.com/jasl89/lpa2-taller3)

---

## Descripción

Esta API permite administrar:
- Usuarios: Crear y gestionar perfiles de usuarios con validación de correos únicos
- Canciones: Agregar, actualizar y eliminar canciones con metadatos completos
- Favoritos: Gestionar las canciones favoritas de cada usuario

### Características Implementadas

- Backend completo con FastAPI
  - Endpoints CRUD para todas las entidades
  - Validación de datos con Pydantic
  - Base de datos SQLite con SQLModel
  - Documentación automática con Swagger UI

- Sistema de Caché
  - Implementación con `lru_cache` para mejorar rendimiento
  - Limpieza automática al modificar datos

- Sistema de Logging
  - Registro de eventos y errores en `logs/app.log`
  - Niveles configurables de logging
  - Trazabilidad completa de operaciones

- Frontend con Bootstrap
  - Interfaz moderna con paleta de colores cálidos
  - Gestión completa desde el navegador
  - Diseño responsive

- Testing Completo
  - Pruebas unitarias con pytest
  - Cobertura de todos los endpoints
  - Base de datos en memoria para tests

- Pre-commits con Ruff
  - Formateo automático de código
  - Análisis estático
  - Validaciones antes de cada commit

---

## Estructura del Proyecto

```
lpa2-taller3/
├── app/
│   ├── __init__.py           # Inicialización del paquete
│   ├── config.py             # Configuración de la aplicación
│   ├── models.py             # Modelos SQLModel (Usuario, Cancion, Favorito)
│   ├── database.py           # Configuración de base de datos
│   ├── logger.py             # Sistema de logging
│   ├── cache.py              # Sistema de caché
│   └── routers/
│       ├── __init__.py
│       ├── usuarios.py       # Endpoints de usuarios
│       ├── canciones.py      # Endpoints de canciones
│       └── favoritos.py      # Endpoints de favoritos
├── frontend/
│   ├── index.html            # Interfaz web Bootstrap
│   └── app.js                # Lógica del frontend
├── logs/
│   └── app.log               # Archivo de logs
├── tests/
│   └── test_api.py           # Pruebas unitarias
├── main.py                   # Punto de entrada de la aplicación
├── requirements.txt          # Dependencias del proyecto
├── pyproject.toml            # Configuración de Ruff
├── .pre-commit-config.yaml   # Configuración de pre-commit
├── .gitignore                # Archivos ignorados por Git
├── setup.sh / setup.bat      # Scripts de inicialización
├── musica.db                 # Base de datos SQLite (generada)
└── README.md                 # Este archivo
```

---

## 🗄️ Modelo de Datos

### Usuario
```json
{
  "id": "int (auto)",
  "nombre": "string (1-100 caracteres)",
  "correo": "string (único, formato email)",
  "fecha_registro": "datetime (auto)"
}
```

### Canción
```json
{
  "id": "int (auto)",
  "titulo": "string (1-200 caracteres)",
  "artista": "string (1-100 caracteres)",
  "album": "string | null (opcional)",
  "duracion": "int (segundos, > 0)",
  "año": "int | null (1900-2100, opcional)",
  "genero": "string | null (opcional)",
  "fecha_creacion": "datetime (auto)"
}
```

### Favorito
```json
{
  "id": "int (auto)",
  "usuario_id": "int (FK -> Usuario)",
  "cancion_id": "int (FK -> Cancion)",
  "fecha_agregado": "datetime (auto)"
}
```

---

## Instalación y Ejecución

### Opción 1: Inicialización Automática (Recomendada)

Linux/Mac:
```bash
./setup.sh
```

Windows:
```bash
setup.bat
```

### Opción 2: Instalación Manual

#### 1. Clonar el Repositorio

```bash
git clone https://github.com/jasl89/lpa2-taller3.git
cd lpa2-taller3
```

#### 2. Crear Entorno Virtual

```bash
python -m venv .venv

# En Linux/Mac:
source .venv/bin/activate

# En Windows:
.venv\Scripts\activate
```

#### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

#### 4. Configurar Pre-commit (Opcional)

```bash
pre-commit install
```

#### 5. Ejecutar el Servidor

```bash
python main.py
```

O usando uvicorn directamente (con puerto personalizado si 8000 está ocupado):

```bash
uvicorn main:app --reload --port 8080
```

El servidor estará disponible en:
- API: http://localhost:8080
- Documentación Swagger: http://localhost:8080/docs
- Documentación ReDoc: http://localhost:8080/redoc
- Frontend: http://localhost:8080/static/index.html

### Ejecutar el Frontend

Una vez el servidor esté corriendo, abre tu navegador y accede a:

```
http://localhost:8080/static/index.html
```

La interfaz incluye:
- Panel de estadísticas en tiempo real
- Formularios para crear usuarios, canciones y favoritos
- Listados con filtros por artista y género
- Acciones de editar y eliminar
- Diseño responsive con colores cálidos (beige #D4A574, naranja #C87941, marrón #8B5A3C)

---

## Endpoints de la API

### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/usuarios/` | Listar todos los usuarios |
| POST | `/api/usuarios/` | Crear un nuevo usuario |
| GET | `/api/usuarios/{id}` | Obtener un usuario específico |
| PATCH | `/api/usuarios/{id}` | Actualizar un usuario |
| DELETE | `/api/usuarios/{id}` | Eliminar un usuario |

### Canciones

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/canciones/` | Listar todas las canciones |
| POST | `/api/canciones/` | Crear una nueva canción |
| GET | `/api/canciones/{id}` | Obtener una canción específica |
| PATCH | `/api/canciones/{id}` | Actualizar una canción |
| DELETE | `/api/canciones/{id}` | Eliminar una canción |

**Filtros disponibles en GET:**
- `?artista=nombre` - Filtrar por artista
- `?genero=genero` - Filtrar por género
- `?skip=0&limit=100` - Paginación

### Favoritos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/favoritos/` | Listar todos los favoritos |
| POST | `/api/favoritos/` | Agregar una canción a favoritos |
| GET | `/api/favoritos/usuario/{id}` | Listar favoritos de un usuario |
| DELETE | `/api/favoritos/{id}` | Eliminar un favorito |
| DELETE | `/api/favoritos/usuario/{uid}/cancion/{cid}` | Eliminar favorito específico |

---

## 💡 Ejemplos de Uso

### Crear un Usuario

```bash
curl -X POST "http://localhost:8000/api/usuarios/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "correo": "juan@example.com"
  }'
```

### Crear una Canción

```bash
curl -X POST "http://localhost:8000/api/canciones/" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Bohemian Rhapsody",
    "artista": "Queen",
    "album": "A Night at the Opera",
    "duracion": 354,
    "año": 1975,
    "genero": "Rock"
  }'
```

### Agregar a Favoritos

```bash
curl -X POST "http://localhost:8000/api/favoritos/" \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": 1,
    "cancion_id": 1
  }'
```

---

## 🧪 Ejecutar Pruebas

Las pruebas están implementadas con pytest y cubren todos los endpoints de la API.

### Ejecutar todas las pruebas:

```bash
pytest
```

### Ejecutar con el formato solicitado:

```bash
pytest --maxfail=1 --disable-warnings -q
```

### Ejecutar con detalles:

```bash
pytest -v
```

### Cobertura de pruebas:

```bash
pytest --cov=app tests/
```

### ¿Qué valida cada prueba?

**TestUsuarios (7 tests):**
- Listado de usuarios
- Creación de usuario con validaciones
- Correos únicos (no duplicados)
- Obtención por ID
- Error 404 para usuarios inexistentes
- Actualización de datos
- Eliminación de usuarios

**TestCanciones (7 tests):**
- Listado de canciones
- Creación con metadatos completos
- Obtención por ID
- Actualización de campos
- Eliminación de canciones
- Filtro por artista
- Filtro por género

**TestFavoritos (5 tests):**
- Listado de favoritos
- Creación con relaciones
- Restricción de duplicados
- Listado por usuario con detalles
- Eliminación por ID y por usuario/canción

**TestEndpointsBasicos (2 tests):**
- Endpoint raíz
- Health check

**Total: 21 pruebas unitarias**

---

## Frontend con Bootstrap

El frontend está diseñado con una paleta de colores cálidos:
- Primario: #D4A574 (Beige/Ocre cálido)
- Secundario: #C87941 (Naranja terracota)
- Acento: #8B5A3C (Marrón medio)
- Fondo: #FFF8F0 (Crema suave)

### Características del Frontend:

- Diseño responsive con Bootstrap 5
- Tarjetas con hover effects
- Formularios con validación
- Estadísticas en tiempo real
- Filtrado de canciones
- Gestión completa de usuarios, canciones y favoritos

Acceso: http://localhost:8080/static/index.html

---

## Pre-commits y Estilo de Código

Este proyecto usa **Ruff** para mantener un código limpio y consistente.

### Configuración de Pre-commit

El archivo `.pre-commit-config.yaml` incluye:
- **Ruff Linter**: Analiza el código y corrige problemas automáticamente
- **Ruff Formatter**: Formatea el código según estándares
- **Hooks adicionales**: Espacios en blanco, fin de archivo, verificación YAML/JSON

### Instalar pre-commit:

```bash
pip install pre-commit
pre-commit install
```

### Ejecutar manualmente:

```bash
# Ejecutar en todos los archivos
pre-commit run --all-files

# Ejecutar solo ruff
pre-commit run ruff --all-files
```

### Formato de Commits

Los commits deben seguir el formato convencional en español:

```bash
feat: agregar modelo de canciones
fix: corregir validación de correo electrónico
test: añadir pruebas de favoritos
docs: actualizar README con instrucciones
style: formatear código con ruff
refactor: reorganizar estructura de routers
```

---

## Workflow de Git

### Configurar Git

```bash
git config user.name "Jhon Salcedo"
git config user.email "tu-email@ejemplo.com"
```

### Comandos Básicos

```bash
# Ver estado de los archivos
git status

# Agregar archivos al staging
git add .

# Hacer commit con mensaje en español
git commit -m "feat: implementar sistema de usuarios"

# Subir cambios al repositorio remoto
git push origin main
```

### Ejemplos de Commits por Módulo

```bash
# Configuración y utilidades
git add app/config.py app/logger.py app/cache.py app/database.py
git commit -m "feat: agregar configuración y utilidades base"

# Modelos de datos
git add app/models.py
git commit -m "feat: implementar modelos de datos SQLModel"

# Routers/Endpoints
git add app/routers/
git commit -m "feat: agregar endpoints REST API"

# Frontend
git add frontend/
git commit -m "feat: implementar interfaz web con Bootstrap"

# Tests
git add tests/
git commit -m "test: agregar pruebas unitarias con pytest"

# Documentación
git add README.md requirements.txt
git commit -m "docs: agregar documentación completa"
```

---

## Sistema de Caché

El proyecto implementa un sistema de caché para mejorar el rendimiento:

- Uso de `functools.lru_cache` para cachear consultas frecuentes
- Limpieza automática del caché al modificar datos (POST, PATCH, DELETE)
- Gestor centralizado de caché en `app/cache.py`

Beneficios:
- Reducción de consultas a la base de datos
- Mejora en tiempos de respuesta
- Configuración de TTL (Time To Live) en `app/config.py`

---

## Sistema de Logging

Todos los eventos y errores se registran en `logs/app.log`:

```python
# Configuración en app/config.py
log_level = "INFO"
log_file = "logs/app.log"
```

**Qué se registra:**
- Inicio y cierre de la aplicación
- Creación, actualización y eliminación de registros
- Errores y excepciones
- Accesos a endpoints
- Operaciones de caché

**Ver logs en tiempo real:**
```bash
tail -f logs/app.log
```

---

## 🔄 Control de Versiones con Git

### Configurar usuario Git:

```bash
git config --global user.name "Jhon Salcedo"
git config --global user.email "tu-email@example.com"
```

### Flujo de trabajo:

```bash
# 1. Ver cambios
git status

# 2. Agregar archivos
git add .

# 3. Hacer commit (pre-commit se ejecuta automáticamente)
git commit -m "feat: mensaje corto en español"

# 4. Subir cambios
git push origin main
```

### Tipos de mensajes de commit:

- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de errores
- `test:` - Pruebas
- `docs:` - Documentación
- `style:` - Formateo de código
- `refactor:` - Refactorización
- `perf:` - Mejoras de rendimiento
- `chore:` - Tareas de mantenimiento

---

## Extensiones Opcionales

### 1. Dockerización del Proyecto

Crear un `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Y `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./musica.db:/app/musica.db
      - ./logs:/app/logs
    environment:
      - DATABASE_URL=sqlite:///./musica.db
```

### 2. Autenticación JWT

Para implementar autenticación con JWT:

```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

Agregar modelos de autenticación, endpoints de login y middleware de verificación de tokens.

### 3. Estadísticas y Recomendaciones

Implementar endpoints adicionales:
- `/api/estadisticas/` - Estadísticas generales
- `/api/canciones/populares/` - Canciones más agregadas a favoritos
- `/api/usuarios/{id}/recomendaciones/` - Recomendaciones basadas en favoritos

---

## Solución de Problemas

### Problema: "No module named 'fastapi'"

Solución: Asegúrate de haber activado el entorno virtual y ejecutado `pip install -r requirements.txt`

```bash
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Problema: "Address already in use"

Solución: El puerto 8000 ya está en uso. Usa otro puerto:

```bash
uvicorn main:app --reload --port 8080
```

### Problema: No se crea la base de datos

Solución: Verifica permisos de escritura en el directorio. La base de datos `musica.db` se crea automáticamente al iniciar el servidor.

### Problema: Pre-commit no funciona

Solución: Reinstala los hooks:

```bash
pre-commit uninstall
pre-commit install
```

---

## Documentación Adicional

- FastAPI: https://fastapi.tiangolo.com/
- SQLModel: https://sqlmodel.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/
- Pytest: https://docs.pytest.org/
- Ruff: https://docs.astral.sh/ruff/
- Bootstrap: https://getbootstrap.com/

---

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## Licencia

Este proyecto está bajo la Licencia MIT.

---

## Autor

Jhon Salcedo
GitHub: [@jasl89](https://github.com/jasl89)
Repositorio: [https://github.com/jasl89/lpa2-taller3](https://github.com/jasl89/lpa2-taller3)

---

## Soporte

Para preguntas o soporte, por favor abre un issue en el repositorio de GitHub.
