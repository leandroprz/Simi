@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Simi - Launcher (Windows)
:: Chequea dependencias, las instala en caso de ser necesario y luego ejecuta la app

:: Copyright (C) 2025 Leandro Pérez
:: Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles

:: Chequea permisos admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permisos de administrador...
    :: Abre nuevamente con permisos de admin
    powershell -Command "Start-Process '%~f0' -Verb RunAs -ArgumentList '-WorkDir', '%CD%'"
    exit /b
)
if "%~1"=="-WorkDir" (
    cd /d "%~2"
)

echo.
echo ================
echo Launcher de Simi
echo ================
echo.

:: Chequea si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no está instalado en tu sistema operativo o no está presente en PATH.
    echo.
    echo Instalá Python 3.8 o superior desde https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Get versión Python instalada
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Tenés Python %PYTHON_VERSION% instalado en tu sistema operativo.
echo.

:: Chequea si el archivo requirements.txt existe
if not exist "requirements.txt" (
    echo Error: No se encontró el archivo requirements.txt
    echo Asegurate de ejecutar este script desde la carpeta de Simi.
    echo.
    echo Carpeta actual: %CD%
    echo.
    pause
    exit /b 1
)

:: Chequea si las dependencias están instaladas, intenta importarlas
echo Chequeando dependencias...
python -c "import colorama, requests, psutil, tkinterdnd2" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Faltan dependencias. Vamos a instalarlas...
    echo.

    python -m pip install --upgrade pip --quiet

    :: Instala dependencias
    python -m pip install -r requirements.txt
    set INSTALL_RESULT=%errorlevel%

    if !INSTALL_RESULT! neq 0 (
        echo.
        echo Error: Hubo un problema instalando las dependencias.
        echo.
        echo Intentá instalarlas manualmente usando: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )

    echo.
    echo Dependencias instaladas correctamente.
    echo.
) else (
    echo Todas las dependencias están instaladas.
    echo.
)

:: Ejecuta Simi
echo Iniciando Simi en otra ventana...
echo.

if exist "src/simi.py" (
    python src/simi.py
) else (
    echo Error: No se encontró simi.py en la carpeta /src
    echo.
    pause
    exit /b 1
)

exit /b 0
