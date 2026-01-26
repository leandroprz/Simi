#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Funciones relacionadas a la app Simi

Copyright (C) 2025 Leandro Pérez
Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles
"""

import platform
import os
import subprocess
import time
import sys
import webbrowser
from typing import Tuple, Optional
from colorama import Fore

# Imports Simi
from interfaz import titulo_subrayado, limpia_pantalla, borde_superior, muestra_contenido, borde_inferior, muestra_input_usuario
from i18n import TEXTOS
from config import URLS, VERSION_ACTUAL_SIMI, NOMBRE_RELEASE
from utils_archivos import get_carpeta_descargas, descargar_archivo

# Constantes
_SISTEMA_OPERATIVO = platform.system()
_ES_WINDOWS = _SISTEMA_OPERATIVO == 'Windows'

def _mostrar_mensaje(titulo_menu: str, mensaje: str) -> None:
    """
    Helper para mostrar mensajes con formato e interfaz consistentes

    Args:
        titulo_menu: Título del menú
        mensaje: Mensaje a mostrar
    """
    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n\n"
        f"{mensaje}"
    )
    borde_inferior()

def _obtener_ultima_version() -> Tuple[bool, Optional[float], Optional[str]]:
    """
    Helper para obtener la última versión disponible de Simi

    Returns:
        Tuple de (success, version, error_message)
    """
    import requests

    try:
        respuesta = requests.get(URLS['latest_vcheck'], timeout=5)
        respuesta.raise_for_status()
        ultima_version = float(respuesta.text.strip())
        return True, ultima_version, None

    except requests.RequestException as e:
        return False, None, str(e)

def _construir_info_descarga(ultima_version: float) -> Tuple[str, str, str]:
    """
    Helper para construir información de descarga según el sistema operativo

    Args:
        ultima_version: Número de versión a descargar

    Returns:
        Tuple de (extension, texto_os, nombre_archivo)
    """
    if _ES_WINDOWS:
        extension = '.exe'
        texto_os = '_win'
    else:
        extension = '.dmg'
        texto_os = '_mac'

    nombre_archivo = f"{NOMBRE_RELEASE}{ultima_version}{texto_os}{extension}"
    return extension, texto_os, nombre_archivo

def _abrir_archivo_sistema(ruta: str) -> bool:
    """
    Helper para abrir un archivo según el sistema operativo

    Args:
        ruta: Ruta del archivo a abrir

    Returns:
        True si se abrió exitosamente
    """
    try:
        if _ES_WINDOWS:
            os.startfile(ruta) # type: ignore
        else:
            subprocess.run(['open', ruta], check=True)
        return True

    except Exception:
        return False

def version_update() -> bool:
    """
    Chequea si hay una nueva versión de Simi y ofrece descargarla

    Returns:
        True si la operación fue exitosa, False si hubo error
    """
    titulo_menu_1 = titulo_subrayado(f"{TEXTOS['titulo_version_update_1']}")
    titulo_menu_2 = titulo_subrayado(f"{TEXTOS['titulo_version_update_2']}")

    # Chequea update
    exito, ultima_version, error = _obtener_ultima_version()

    if not exito or ultima_version is None:
        _mostrar_mensaje(
            titulo_menu_1,
            f"{Fore.LIGHTRED_EX}{TEXTOS['no_pudo_chequear_version']}\nError: {error}.\n"
        )
        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return False

    version_actual = float(VERSION_ACTUAL_SIMI)

    # Está usando la última versión
    if ultima_version == version_actual:
        _mostrar_mensaje(
            titulo_menu_1,
            f"{Fore.LIGHTCYAN_EX}{TEXTOS['usando_ultima_version']} v{VERSION_ACTUAL_SIMI}\n"
        )
        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return True

    # Está usando versión superior a la disponible públicamente
    if ultima_version < version_actual:
        _mostrar_mensaje(
            titulo_menu_1,
            f"{Fore.LIGHTCYAN_EX}{TEXTOS['version_actual_1']} ({VERSION_ACTUAL_SIMI}) "
            f"{TEXTOS['version_actual_2']} v{ultima_version}\n"
        )
        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return True

    # Actualización disponible
    _mostrar_mensaje(
        titulo_menu_1,
        f"{Fore.LIGHTGREEN_EX}{TEXTOS['nueva_v_disponible']} v{ultima_version}\n"
    )

    seleccion = muestra_input_usuario(f"{TEXTOS['desea_descargar']}").upper().strip() or 'S'
    if seleccion != 'S':
        return True

    # Descarga nueva versión
    return _descargar_nueva_version(ultima_version, titulo_menu_1, titulo_menu_2)

def _descargar_nueva_version(ultima_version: float, titulo_menu_1: str, titulo_menu_2: str) -> bool:
    """
    Helper para descargar una nueva versión de Simi

    Args:
        ultima_version: Versión a descargar
        titulo_menu_1: Título del menú principal
        titulo_menu_2: Título del menú de descarga

    Returns:
        True si la descarga fue exitosa
    """
    try:
        ruta_descarga = get_carpeta_descargas()

        # Construye URL de descarga y nombre de archivo
        extension, texto_os, nombre_archivo = _construir_info_descarga(ultima_version)
        url_release = f"{URLS['url_releases']}/v{ultima_version}/{nombre_archivo}"
        ruta_archivo = os.path.join(ruta_descarga, "Simi", "versiones", nombre_archivo)

        # Muestra pantalla de descarga
        _mostrar_mensaje(titulo_menu_2, "")

        # Descarga
        descarga_exitosa, ruta_real = descargar_archivo(
            url_release,
            ruta_destino=ruta_archivo,
            ultima_version=ultima_version
        )

        if not descarga_exitosa:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_descargo']}\n")
            borde_inferior()
            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        # Pregunta si quiere abrir nueva versión
        muestra_contenido("")
        borde_inferior()
        seleccion_abrir = muestra_input_usuario(f"{TEXTOS['desea_abrir']}").upper().strip() or 'S'

        if seleccion_abrir == 'S' and ruta_real:
            if _abrir_archivo_sistema(ruta_real):
                os._exit(0)

        return True

    except Exception as e:
        _mostrar_mensaje(
            titulo_menu_1,
            f"{Fore.LIGHTRED_EX}{TEXTOS['no_descargo']} Error:\n{e}\n"
        )
        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return False

def abre_url_ayuda() -> None:
    """ Muestra mensaje y abre URL usando el navegador default del sistema operativo """
    _mostrar_mensaje(
        TEXTOS['agradecimiento'],
        f"{Fore.LIGHTCYAN_EX}{TEXTOS['mensaje_url_ayuda']}\n"
    )
    time.sleep(3)
    webbrowser.open(URLS['url_ayuda_tienda'])

def abre_url_reportar_error() -> None:
    """ Muestra mensaje y abre URL usando el navegador default del sistema operativo """
    _mostrar_mensaje(
        TEXTOS['agradecimiento'],
        f"{Fore.LIGHTCYAN_EX}{TEXTOS['mensaje_reportar_error']}\n"
    )
    time.sleep(3)
    webbrowser.open(URLS['url_reportar_error'])

def cierra_programa() -> None:
    """ Muestra un mensaje y cierra la app """
    _mostrar_mensaje(
        TEXTOS['agradecimiento'],
        f"{Fore.LIGHTCYAN_EX}{TEXTOS['mensaje_resenia']}\n"
    )
    time.sleep(3)
    sys.exit(0)
