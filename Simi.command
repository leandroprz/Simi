#!/bin/bash

# Simi - Launcher (macOS)
# Chequea dependencias, las instala en caso de ser necesario y luego ejecuta la app

# Copyright (C) 2025 Leandro Pérez
# Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles

echo ""
echo "================"
echo "Launcher de Simi"
echo "================"
echo ""

# Chequea carpeta contenedora de este script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Chequea si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python no está instalado en tu sistema operativo."
    echo ""
    echo "Instalá Python 3.8 o superior desde https://www.python.org/downloads/"
    echo ""
    read -p "Presioná Enter para salir..."
    exit 1
fi

# Get versión Python instalada
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Tenés Python $PYTHON_VERSION instalado en tu sistema operativo."
echo ""

# Chequea si el archivo requirements.txt existe
if [ ! -f "requirements.txt" ]; then
    echo "Error: No se encontró el archivo requirements.txt"
    echo "Asegurate de ejecutar este script desde la carpeta de Simi."
    echo ""
    read -p "Presioná Enter para salir..."
    exit 1
fi

# Chequea si las dependencias están instaladas, intenta importarlas
echo "Chequeando dependencias..."
python3 -c "import colorama, requests, psutil, tkinterdnd2" &> /dev/null

if [ $? -ne 0 ]; then
    echo ""
    echo "Faltan dependencias. ¿Querés instalarlas ahora? (S/n): "
    read -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Ss]$ ]] || [[ -z $REPLY ]]; then
        # Actualiza pip
        echo "Actualizando pip..."
        python3 -m pip install --upgrade pip --user --quiet

        # Instala dependencias
        echo "Instalando dependencias..."
        python3 -m pip install -r requirements.txt --user

        if [ $? -ne 0 ]; then
            echo ""
            echo "Error: Hubo un problema instalando las dependencias."
            echo ""
            echo "Intentá instalarlas manualmente usando: pip3 install -r requirements.txt"
            echo ""
            read -p "Presioná Enter para salir..."
            exit 1
        fi

        echo ""
        echo "Dependencias instaladas correctamente."
        echo ""
    else
        echo "Instalación cancelada. Simi no puede ejecutarse sin las dependencias."
        read -p "Presioná Enter para salir..."
        exit 1
    fi
else
    echo "Todas las dependencias están instaladas."
    echo ""
fi

# Ejecuta Simi
echo "Iniciando Simi en otra ventana..."
echo ""

if [ -f "src/simi.py" ]; then
    python3 src/simi.py
else
    echo "Error: No se encontró simi.py en la carpeta /src"
    echo ""
    read -p "Presioná Enter para salir..."
    exit 1
fi

exit 0
