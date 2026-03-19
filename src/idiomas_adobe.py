#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Funciones que permiten cambiar y restaurar los idiomas de los programas de Adobe

Copyright (C) 2025 Leandro Pérez
Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles
"""

import platform
from pathlib import Path
from colorama import Fore

# Imports Simi
import shared_state
from config import VERSION_ACTUAL_SIMI, URLS, CONFIG_PROGRAMAS_ADOBE
from i18n import TEXTOS
from interfaz import limpia_pantalla, borde_superior, borde_inferior, muestra_contenido, muestra_input_usuario, titulo_subrayado
from utils_adobe import ruta_instalacion_programa, chequea_cierra_app
from utils_archivos import descargar_archivo, edita_idioma_xml, restaura_idioma_xml
from permisos_admin import ejecutar_operaciones_pendientes

def cambiar_idioma_programa(programa_key):
    """
    Cambia el idioma de un programa de Adobe (listados en config.py)

    Args:
        programa_key (str): Clave del programa en CONFIG_PROGRAMAS_ADOBE ('after_effects', 'premiere_pro', 'photoshop', etc.)

    Returns:
        bool: True si el cambio fue exitoso, False si hubo error
    """
    # Validación
    if programa_key not in CONFIG_PROGRAMAS_ADOBE:
        raise ValueError(f"El programa {programa_key} no está cargado en la configuración de Simi.")

    # Obtiene valores de shared_state.py que son ingresados en los menús
    locale_xml = shared_state.locale_xml
    version_adobe = shared_state.version_adobe
    idioma_menu_ui = shared_state.idioma_menu_ui

    # Nos aseguramos que locale_xml no sea None (definido en shared_state.py)
    if locale_xml is None:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\n")
        borde_inferior()
        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return False

    shared_state.operaciones_pendientes_admin = []

    config = CONFIG_PROGRAMAS_ADOBE[programa_key]
    NOMBRE_PROGRAMA = config['nombre']

    titulo_menu = titulo_subrayado(
        f"{TEXTOS['cambiar_idioma']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['al']} {idioma_menu_ui}"
    )

    # Interfaz superior
    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa_base = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa=config['ruta_macos'], # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Guarda en shared_state.py para mostrar al usuario
    shared_state.ruta_instal_print = ruta_instal_programa_base

    # Determina ruta del XML si no es solo locale
    ruta_xml = None
    if not config.get('solo_locale', False):
        xml_subpath = config['xml_paths'].get(platform.system())
        if xml_subpath:
            ruta_xml = Path(ruta_instal_programa_base) / xml_subpath

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo XML existe (si se necesita)
    if ruta_xml and (not ruta_xml or not ruta_xml.exists()):
        limpia_pantalla()
        borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
        muestra_contenido(
            f"\n{TEXTOS['simi_descripcion']}\n\n"
            f"\n{titulo_menu}\n\n"
            f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['razones']}\n"
        )
        borde_inferior()

        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return False

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Descarga paquete de idioma
    if config.get('necesita_locale', False):
        locale_code = config['locale_code']
        url_key = 'url_locales_win' if platform.system() == 'Windows' else 'url_locales_mac'
        url_locale = f"{URLS[url_key]}/{locale_code}/{version_adobe}/{locale_xml}.zip"

        descarga_exitosa = descargar_archivo(
            url_locale,
            auto_unzip=True,
            ruta_unzip=str(ruta_instal_programa_base) # Convierte path a string
        )

        if not descarga_exitosa:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_descarga_idioma']}\n")
            borde_inferior()
            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

    # Edita el XML si no es solo locale
    if not config.get('solo_locale', False):
        # Nos aseguramos que ruta_xml no sea None
        if ruta_xml is None:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\n")
            borde_inferior()
            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        xml_exitoso = edita_idioma_xml(str(ruta_xml), locale_xml)
        if not xml_exitoso:
            return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if shared_state.operaciones_pendientes_admin:
        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Cambiar idioma de {NOMBRE_PROGRAMA} al {idioma_menu_ui}",
            mensaje=f"Se requieren permisos de Administrador para cambiar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()
            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

    # Mensaje exitoso
    if programa_key == 'photoshop':
        mensaje_extra = f"{Fore.LIGHTCYAN_EX}{TEXTOS['cambio_ps']}\n"
    elif programa_key == 'premiere_pro':
        mensaje_extra = f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{shared_state.ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n\n{Fore.LIGHTCYAN_EX}{TEXTOS['cambio_ppro']}\n"
    else:
        mensaje_extra = f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{shared_state.ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"

    muestra_contenido(
        f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{shared_state.ruta_instal_print}]\n\n"
        f"{mensaje_extra}"
    )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def restaurar_xml_programa(programa_key):
    """
    Restaura el XML de un programa de Adobe (listados en config.py) desde un backup

    Args:
        programa_key (str): Clave del programa en CONFIG_PROGRAMAS_ADOBE ('after_effects', 'premiere_pro', 'photoshop', etc.)

    Returns:
        bool: True si la restauración fue exitosa, False si hubo error
    """
    # Validación
    if programa_key not in CONFIG_PROGRAMAS_ADOBE:
        raise ValueError(f"El programa {programa_key} no está cargado en la configuración de Simi.")

    # Obtiene valores de shared_state.py que son ingresados en los menús
    version_adobe = shared_state.version_adobe

    shared_state.operaciones_pendientes_admin = []

    config = CONFIG_PROGRAMAS_ADOBE[programa_key]
    NOMBRE_PROGRAMA = config['nombre']

    # Photoshop no restaura, solo muestra indicaciones
    if programa_key == 'photoshop':
        titulo_menu = titulo_subrayado(
            f"{TEXTOS['menu_restaurar_xml']} {TEXTOS['de']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['menu_usando_bak']}"
        )
        limpia_pantalla()
        borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
        muestra_contenido(
            f"\n{TEXTOS['simi_descripcion']}\n\n"
            f"\n{titulo_menu}\n\n"
            f"{Fore.LIGHTCYAN_EX}{TEXTOS['restaura_ps']}\n"
        )
        borde_inferior()

        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return True

    titulo_menu = titulo_subrayado(
        f"{TEXTOS['menu_restaurar_xml']} {TEXTOS['de']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['menu_usando_bak']}"
    )

    # Interfaz superior
    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa_base = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa=config['ruta_macos'], # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Guarda en shared_state.py para mostrar al usuario
    shared_state.ruta_instal_print = ruta_instal_programa_base

    # Construye ruta del .bak
    xml_subpath = config['xml_paths'].get(platform.system())
    ruta_bak = Path(ruta_instal_programa_base) / xml_subpath.replace('.xml', '.bak')

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo .bak existe
    if not ruta_bak or not ruta_bak.exists():
        limpia_pantalla()
        borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
        muestra_contenido(
            f"\n{TEXTOS['simi_descripcion']}\n\n"
            f"\n{titulo_menu}\n\n"
            f"{Fore.LIGHTRED_EX}{TEXTOS['no_restauro']}\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['razones_bak']}\n"
        )
        borde_inferior()

        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return False

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Restaura el .bak
    ruta_xml = ruta_bak.with_suffix('.xml')
    bak_exitoso, idioma_restaurado = restaura_idioma_xml(ruta_xml)
    if not bak_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if shared_state.operaciones_pendientes_admin:
        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Restaurar idioma de {NOMBRE_PROGRAMA} {version_adobe}",
            mensaje=f"Se requieren permisos de Administrador para restaurar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

    # Mensaje exitoso
    muestra_contenido(
        f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_bak}]\n"
    )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True
