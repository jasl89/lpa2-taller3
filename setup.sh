#!/bin/bash

# Script de inicialización rápida para API de Música
# Autor: Jhon Salcedo (@jasl89)

echo "=========================================="
echo "   API de Música - Inicialización Rápida"
echo "   Autor: Jhon Salcedo (@jasl89)"
echo "=========================================="
echo ""

# Colores para la salida
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python
echo -e "${YELLOW}[1/6] Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 no está instalado${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ $PYTHON_VERSION encontrado${NC}"
echo ""

# Crear entorno virtual
echo -e "${YELLOW}[2/6] Creando entorno virtual...${NC}"
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ Entorno virtual ya existe${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Entorno virtual creado${NC}"
fi
echo ""

# Activar entorno virtual
echo -e "${YELLOW}[3/6] Activando entorno virtual...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Entorno virtual activado${NC}"
echo ""

# Instalar dependencias
echo -e "${YELLOW}[4/6] Instalando dependencias...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencias instaladas${NC}"
echo ""

# Instalar pre-commit
echo -e "${YELLOW}[5/6] Configurando pre-commit...${NC}"
pre-commit install
echo -e "${GREEN}✓ Pre-commit configurado${NC}"
echo ""

# Crear archivo .env si no existe
echo -e "${YELLOW}[6/6] Verificando configuración...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Archivo .env creado desde .env.example${NC}"
else
    echo -e "${GREEN}✓ Archivo .env ya existe${NC}"
fi
echo ""

# Resumen
echo "=========================================="
echo -e "${GREEN}   ¡Inicialización Completa!${NC}"
echo "=========================================="
echo ""
echo "Para ejecutar el servidor:"
echo "  python main.py"
echo ""
echo "Para ejecutar las pruebas:"
echo "  pytest --maxfail=1 --disable-warnings -q"
echo ""
echo "URLs importantes:"
echo "  API: http://localhost:8000"
echo "  Docs: http://localhost:8000/docs"
echo "  Frontend: http://localhost:8000/static/index.html"
echo ""
echo "=========================================="
