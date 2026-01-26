#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Funciones relacionadas a los programas de Adobe

Copyright (C) 2025 Leandro Pérez
Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles
"""

import platform
import os
from typing import List, Optional, Dict
from colorama import Fore
from pathlib import Path

# Imports Simi
import shared_state
from interfaz import muestra_contenido, borde_inferior, muestra_input_usuario, titulo_subrayado, limpia_pantalla, borde_superior
from i18n import TEXTOS
from config import VERSION_ACTUAL_SIMI, VERSIONES_ADOBE_MACOS, RUTAS_ADOBE_MACOS

# Constantes
_SISTEMA_OPERATIVO = platform.system()
_ES_WINDOWS = _SISTEMA_OPERATIVO == 'Windows'
_ES_MACOS = _SISTEMA_OPERATIVO == 'Darwin'

if _ES_WINDOWS:
    _PROGRAMW6432 = os.environ.get('PROGRAMW6432', '')
    _PROGRAMFILES_X86 = os.environ.get('PROGRAMFILES(X86)', '')
    _RUTAS_PROGRAM_FILES = [_PROGRAMW6432, _PROGRAMFILES_X86]
else:
    _PROGRAMW6432 = ''
    _RUTAS_PROGRAM_FILES = []

def versiones_adobe_macos(version_adobe: int) -> Dict[str, str]:
    """
    Devuelve la versión de los programas de Adobe según el año, definido en config.py

    Args:
        version_adobe: Año (ej: 2024, 2025)

    Returns:
        Diccionario que mapea los nombres de los programas a las versiones como string
    """
    return {
        programa: versiones[version_adobe]
        for programa, versiones in VERSIONES_ADOBE_MACOS.items()
        if version_adobe in versiones
    }

def rutas_adobe_macos(nombre_programa: str, version_adobe: int) -> Optional[str]:
    """
    Devuelve la ruta de instalación por defecto para los programas de Adobe en macOS, definido en config.py

    Args:
        nombre_programa: ID del programa (ej: 'after_effects')
        version_adobe: Año (ej: 2024, 2025)

    Returns:
        Ruta como string o None si no se encontró
    """
    versiones_dict = versiones_adobe_macos(version_adobe)
    if not versiones_dict or nombre_programa not in RUTAS_ADOBE_MACOS:
        return None

    info = RUTAS_ADOBE_MACOS[nombre_programa]
    ruta_base = info['ruta_default']

    if info['usa_version'] and nombre_programa in versiones_dict:
        return f"{ruta_base}/{versiones_dict[nombre_programa]}"
    else:
        return f"{ruta_base} {version_adobe}"

def get_version_macos(version_adobe: int, nombre_programa: str) -> Optional[str]:
    """
    Obtiene la versión de un programa de Adobe en macOS

    Args:
        version_adobe: Año (ej: 2024, 2025)
        nombre_programa: ID del programa

    Returns:
        Versión como string o None
    """
    versiones_dict = versiones_adobe_macos(version_adobe)
    return versiones_dict.get(nombre_programa)

def ruta_instalacion_programa(ruta_subcarpeta: Optional[str] = None,
                              nombre_programa: Optional[str] = None,
                              version_adobe: Optional[int] = None) -> Path:
    """
    Permite ingresar una ruta de instalación para cada programa de Adobe o se usa la ruta por defecto

    Args:
        ruta_subcarpeta: Subcarpeta para usar en Windows
        nombre_programa: ID de cada programa para macOS
        version_adobe: Año para las rutas en macOS

    Returns:
        Ruta de instalación final ingresada por el usuario o ruta por defecto
    """
    if _ES_WINDOWS or not nombre_programa or version_adobe is None:
        ruta_base = f"{_PROGRAMW6432}\\Adobe"
        ruta_instalacion_default = os.path.join(ruta_base, ruta_subcarpeta) if ruta_subcarpeta else ruta_base
    else: # macOS
        rutas_default = rutas_adobe_macos(nombre_programa, version_adobe)

        if rutas_default is None:
            # Fallback si no se encuentra en RUTAS_ADOBE_MACOS
            ruta_base = "/Applications/Adobe"
            ruta_instalacion_default = os.path.join(ruta_base, ruta_subcarpeta) if ruta_subcarpeta else ruta_base
        else:
            ruta_instalacion_default = rutas_default

    # Muestra la ruta default al usuario
    muestra_contenido(
        f"\n{Fore.LIGHTCYAN_EX}{TEXTOS['ruta_instalacion']}\n"
        f"[{ruta_instalacion_default}]\n"
    )
    borde_inferior()

    # Pide input al usuario
    input_usuario = muestra_input_usuario(f"{TEXTOS['input_ruta']}").strip()
    ruta_instalacion_final = input_usuario if input_usuario else ruta_instalacion_default

    # Resuelve la ruta absoluta
    ruta_corregida = str(Path(ruta_instalacion_final).resolve())

    return Path(ruta_corregida)

def _busca_procesos_por_nombre(nombre: str) -> List:
    """
    Busca todos los procesos según el nombre indicado (case-insensitive)

    Args:
        nombre: Nombre del proceso a buscar (ej: "After Effects")

    Returns:
        Lista de procesos encontrados
    """
    import psutil

    procesos = []
    nombre_lower = nombre.lower()

    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            info_proc = proc.info
            nombre_proc = info_proc['name'] or ''
            exe_proc = info_proc['exe'] or ''

            if nombre_lower in nombre_proc.lower() or nombre_lower in exe_proc.lower():
                procesos.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return procesos

def _finaliza_arbol_de_procesos(proceso) -> bool:
    """
    Finaliza todos los procesos y sus children

    Args:
        proceso: Proceso de psutil a finalizar

    Returns:
        True si se finalizó exitosamente
    """
    import psutil

    try:
        children = list(proceso.children(recursive=True))

        # Finaliza children
        for child in children:
            try:
                child.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Espera que finalicen los children
        gone, alive = psutil.wait_procs(children, timeout=3)

        # Fuerza la finalización de children restantes
        for child in alive:
            try:
                child.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Finaliza el proceso principal
        proceso.terminate()
        try:
            proceso.wait(timeout=5)

        except psutil.TimeoutExpired:
            proceso.kill()
            proceso.wait(timeout=3)
        return True

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False

def _requiere_permisos_para_cerrar_proceso(proceso) -> bool:
    """
    Determina si se necesitan permisos administrativos para cerrar un proceso

    Args:
        proceso: Proceso de psutil

    Returns:
        True si requiere permisos admin
    """
    import psutil

    try:
        ruta_exe = proceso.exe()

        if _ES_MACOS:
            rutas_sistema = ['/Applications', '/System', '/usr', '/bin', '/sbin']
            return any(ruta_exe.startswith(ruta) for ruta in rutas_sistema)

        elif _ES_WINDOWS:
            return any(
                ruta_exe.lower().startswith(ruta.lower())
                for ruta in _RUTAS_PROGRAM_FILES if ruta
            )

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return True

    return False

def chequea_cierra_app(nombre_app: str) -> bool:
    """
    Chequea si una aplicación está ejecutándose y pregunta al usuario si quiere cerrarla

    Args:
        nombre_app: Nombre de la aplicación a chequear (ej: "Adobe After Effects", "audition", "Photoshop")

    Returns:
        True si la app se encontró, False si no estaba abierta
    """
    procesos_coinciden = _busca_procesos_por_nombre(nombre_app)

    if not procesos_coinciden:
        return False

    muestra_contenido(f"{Fore.LIGHTRED_EX}¡{nombre_app} {TEXTOS['programa_abierto']}\n")
    borde_inferior()

    titulo_menu = titulo_subrayado(
        f"{TEXTOS['cambiar_idioma']} {nombre_app} {TEXTOS['al']} {shared_state.idioma_menu_ui}"
    )

    while True:
        respuesta = muestra_input_usuario(f"{TEXTOS['queres_cerrar']}").upper().strip() or 'S'

        if respuesta == 'S':
            break
        elif respuesta == 'N':
            limpia_pantalla()
            borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
            muestra_contenido(
                f"\n{TEXTOS['simi_descripcion']}\n\n\n{titulo_menu}\n\n"
                f"{Fore.LIGHTYELLOW_EX}{TEXTOS['intento_cierre_app']}\n"
            )
            borde_inferior()
            muestra_input_usuario(f"{TEXTOS['input_continuar']}").upper().strip()
            return True
        else:
            muestra_contenido(f"{TEXTOS['input_error_sn']}")

    necesita_permisos_admin = any(
        _requiere_permisos_para_cerrar_proceso(p)
        for p in procesos_coinciden
    )

    if not necesita_permisos_admin:
        contador = sum(
            1 for proc in procesos_coinciden
            if _finaliza_arbol_de_procesos(proc)
        )
        return contador > 0

    # Si requiere permisos administrativos, agrega a operaciones pendientes
    if shared_state.operaciones_pendientes_admin is None:
        shared_state.operaciones_pendientes_admin = []

    for proc in procesos_coinciden:
        if _ES_MACOS:
            cmd = f"kill -TERM {proc.pid} 2>/dev/null || kill -KILL {proc.pid} 2>/dev/null"
        else:  # Windows
            cmd = f'taskkill /PID {proc.pid} /F'

        shared_state.operaciones_pendientes_admin.append({
            'tipo': 'comando',
            'comando': cmd,
            'descripcion': f'{TEXTOS["cerrar_app"]} {nombre_app} (PID: {proc.pid})'
        })

    return True
