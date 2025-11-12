@echo off
REM Script de inicialización rápida para API de Música - Windows
REM Autor: Jhon Salcedo (@jasl89)

echo ==========================================
echo    API de Música - Inicialización Rápida
echo    Autor: Jhon Salcedo (@jasl89)
echo ==========================================
echo.

REM Verificar Python
echo [1/6] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo √ %PYTHON_VERSION% encontrado
echo.

REM Crear entorno virtual
echo [2/6] Creando entorno virtual...
if exist venv (
    echo √ Entorno virtual ya existe
) else (
    python -m venv venv
    echo √ Entorno virtual creado
)
echo.

REM Activar entorno virtual
echo [3/6] Activando entorno virtual...
call venv\Scripts\activate.bat
echo √ Entorno virtual activado
echo.

REM Instalar dependencias
echo [4/6] Instalando dependencias...
python -m pip install -q --upgrade pip
pip install -q -r requirements.txt
echo √ Dependencias instaladas
echo.

REM Instalar pre-commit
echo [5/6] Configurando pre-commit...
pre-commit install
echo √ Pre-commit configurado
echo.

REM Crear archivo .env si no existe
echo [6/6] Verificando configuración...
if not exist .env (
    copy .env.example .env
    echo √ Archivo .env creado desde .env.example
) else (
    echo √ Archivo .env ya existe
)
echo.

REM Resumen
echo ==========================================
echo    ¡Inicialización Completa!
echo ==========================================
echo.
echo Para ejecutar el servidor:
echo   python main.py
echo.
echo Para ejecutar las pruebas:
echo   pytest --maxfail=1 --disable-warnings -q
echo.
echo URLs importantes:
echo   API: http://localhost:8000
echo   Docs: http://localhost:8000/docs
echo   Frontend: http://localhost:8000/static/index.html
echo.
echo ==========================================
pause
