#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main script con menús y pantalla principal

Copyright (C) 2025 Leandro Pérez
Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles
"""

# Imports Simi
import shared_state
from interfaz import limpia_pantalla, titulo_subrayado, borde_superior, borde_inferior, muestra_contenido, muestra_input_usuario
from config import VERSION_ACTUAL_SIMI, CONFIG_PROGRAMAS_ADOBE
from i18n import TEXTOS

# Lazy import de colorama solo cuando se necesita
def get_fore():
    from colorama import Fore
    return Fore

def pantalla_splash():
    """
    Muestra mensaje sobre uso de las locales en Simi
    """
    Fore = get_fore()
    titulo_menu = titulo_subrayado(f"{TEXTOS['aviso_importante_1']}")

    while True:
        limpia_pantalla()
        borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
        muestra_contenido(
            f"\n{TEXTOS['simi_descripcion']}\n\n"
            f"\n{titulo_menu}\n\n"
            f"{Fore.LIGHTCYAN_EX}{TEXTOS['aviso_importante_2']}\n\n{TEXTOS['aviso_importante_3']}\n"
        )
        borde_inferior()
        muestra_input_usuario(f"{TEXTOS['input_continuar']}").strip()
        menu_principal()
        return

def menu_principal():
    """
    Muestra el menú principal de Simi y permite ir a otros menús mediante inputs del usuario
    Guarda info de idiomas para usar posteriormente
    """
    titulo_menu = titulo_subrayado(f"{TEXTOS['menu_principal']}")

    while True:
        limpia_pantalla()
        borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
        muestra_contenido(
            f"\n{TEXTOS['simi_descripcion']}\n\n"
            f"\n{titulo_menu}\n\n"
            f"[1] {TEXTOS['menu_cambio_espanol']}\n"
            f"[2] {TEXTOS['menu_cambio_ingles']}\n"
            f"[3] {TEXTOS['menu_restaurar_xml']} {TEXTOS['menu_usando_bak']}\n"
            f"[4] {TEXTOS['menu_buscar_version']}\n"
            f"[5] {TEXTOS['menu_ayuda']}\n"
            f"[6] {TEXTOS['menu_reportar_error']}\n"
            f"[7] {TEXTOS['menu_salir']}\n"
        )
        borde_inferior()

        seleccion = muestra_input_usuario().strip()

        if seleccion == '1':
            shared_state.idioma_menu_ui = 'español'
            shared_state.locale_xml = 'es_ES'
            menu_secundario(modo='cambiar')
        elif seleccion == '2':
            shared_state.idioma_menu_ui = 'inglés'
            shared_state.locale_xml = 'en_US'
            menu_secundario(modo='cambiar')
        elif seleccion == '3':
            shared_state.idioma_menu_ui = ""
            menu_secundario(modo='restaurar')
        elif seleccion == '4':
            from utils_app import version_update
            version_update()
        elif seleccion == '5':
            from utils_app import abre_url_ayuda
            abre_url_ayuda()
        elif seleccion == '6':
            from utils_app import abre_url_reportar_error
            abre_url_reportar_error()
        elif seleccion == '7':
            from utils_app import cierra_programa
            cierra_programa()
        else:
            muestra_input_usuario(f"{TEXTOS['input_error_menu']}").strip()

def menu_secundario(modo='cambiar'):
    """
    Muestra el menú secundario de Simi con las versiones de Adobe y permite ir a otros menús mediante inputs del usuario
    Guarda info de la versión de los programas de Adobe para usar posteriormente

    Args:
        modo: 'cambiar' para cambiar idioma, 'restaurar' para restaurar desde backup
    """
    if modo == 'cambiar':
        titulo_menu = titulo_subrayado(f"{TEXTOS['cambiar_programas']} {shared_state.idioma_menu_ui}")
    else:
        titulo_menu = titulo_subrayado(f"{TEXTOS['menu_restaurar_xml']} {TEXTOS['menu_usando_bak']}")

    while True:
        limpia_pantalla()
        borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
        muestra_contenido(
            f"\n{TEXTOS['simi_descripcion']}\n\n"
            f"\n{titulo_menu}\n\n"
            " [1] Adobe 2026\n"
            " [2] Adobe 2025\n"
            " [3] Adobe 2024\n"
            " [4] Adobe 2023\n"
            " [5] Adobe 2022\n"
            " [6] Adobe 2021\n"
            " [7] Adobe 2020\n"
            " [8] Adobe 2019\n"
            " [9] Adobe 2018\n"
            f"[10] {TEXTOS['menu_principal']}\n"
            f"[11] {TEXTOS['menu_ayuda']}\n"
            f"[12] {TEXTOS['menu_reportar_error']}\n"
            f"[13] {TEXTOS['menu_salir']}\n"
        )
        borde_inferior()

        seleccion = muestra_input_usuario().strip()

        if seleccion in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            # Mapeo de selección a año
            version_map = {
                '1': 2026,
                '2': 2025,
                '3': 2024,
                '4': 2023,
                '5': 2022,
                '6': 2021,
                '7': 2020,
                '8': 2019,
                '9': 2018
            }
            shared_state.version_adobe = version_map[seleccion]
            menu_terciario(modo)
        elif seleccion == '10':
            menu_principal()
            return
        elif seleccion == '11':
            from utils_app import abre_url_ayuda
            abre_url_ayuda()
        elif seleccion == '12':
            from utils_app import abre_url_reportar_error
            abre_url_reportar_error()
        elif seleccion == '13':
            from utils_app import cierra_programa
            cierra_programa()
        else:
            muestra_input_usuario(f"{TEXTOS['input_error_menu']}").strip()

def menu_terciario(modo='cambiar'):
    """
    Muestra el menú terciario de Simi con los programas de Adobe y permite ir a otros menús mediante inputs del usuario
    """
    from idiomas_adobe import cambiar_idioma_programa, restaurar_xml_programa
    from utils_app import abre_url_ayuda, abre_url_reportar_error, cierra_programa

    if modo == 'cambiar':
        titulo_menu = titulo_subrayado(f"Adobe {shared_state.version_adobe} - {TEXTOS['cambiar_a']} {shared_state.idioma_menu_ui}")
    else:
        titulo_menu = titulo_subrayado(f"Adobe {shared_state.version_adobe} - {TEXTOS['menu_restaurar_xml']} {TEXTOS['menu_usando_bak']}")

    # Define el orden de los programas en el menú
    ORDEN_PROGRAMAS = [
        'after_effects', 'premiere_pro', 'audition', 'indesign', 'media_encoder',
        'photoshop', 'illustrator', 'incopy', 'character_animator', 'animate'
    ]

    # Reglas de disponibilidad por programa
    REGLAS_DISPONIBILIDAD = {
        'animate': lambda v: v in range(2018, 2025) # Sólo versiones 2018-2024
    }

    while True:
        limpia_pantalla()
        borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")

        # Construye menú usando info de config.py
        menu_items = [f"\n{TEXTOS['simi_descripcion']}\n\n", f"\n{titulo_menu}\n\n"]

        # Mapeo de números a program keys
        numero_a_key = {}
        num_actual = 1

        for prog_key in ORDEN_PROGRAMAS:
            # Chequea disponibilidad
            if prog_key in REGLAS_DISPONIBILIDAD:
                if not REGLAS_DISPONIBILIDAD[prog_key](shared_state.version_adobe):
                    continue

            # Verifica que existe en config.py
            if prog_key not in CONFIG_PROGRAMAS_ADOBE:
                continue

            nombre = CONFIG_PROGRAMAS_ADOBE[prog_key]['nombre']
            espaciado = ' ' if num_actual < 10 else ''
            menu_items.append(f"{espaciado}[{num_actual}] {nombre}\n")
            numero_a_key[str(num_actual)] = prog_key
            num_actual += 1

        ultima_opcion = num_actual - 1

        # Opciones de navegación
        opcion_menu_principal = ultima_opcion + 1
        opcion_ayuda = ultima_opcion + 2
        opcion_reportar = ultima_opcion + 3
        opcion_salir = ultima_opcion + 4

        menu_items.extend([
            f"{' ' if opcion_menu_principal < 10 else ''}[{opcion_menu_principal}] {TEXTOS['menu_principal']}\n",
            f"{' ' if opcion_ayuda < 10 else ''}[{opcion_ayuda}] {TEXTOS['menu_ayuda']}\n",
            f"{' ' if opcion_reportar < 10 else ''}[{opcion_reportar}] {TEXTOS['menu_reportar_error']}\n",
            f"{' ' if opcion_salir < 10 else ''}[{opcion_salir}] {TEXTOS['menu_salir']}\n"
        ])

        muestra_contenido(''.join(menu_items))
        borde_inferior()

        seleccion = muestra_input_usuario().strip()

        # Menús
        if seleccion == str(opcion_menu_principal):
            menu_principal()
            return
        elif seleccion == str(opcion_ayuda):
            abre_url_ayuda()
        elif seleccion == str(opcion_reportar):
            abre_url_reportar_error()
        elif seleccion == str(opcion_salir):
            cierra_programa()
        else:
            # Selección de programa de Adobe
            if seleccion in numero_a_key:
                prog_key = numero_a_key[seleccion]

                if modo == 'cambiar':
                    cambiar_idioma_programa(prog_key)
                else:
                    restaurar_xml_programa(prog_key)
            else:
                muestra_input_usuario(f"{TEXTOS['input_error_menu']}").strip()

if __name__ == "__main__":
    try:
        pantalla_splash()
    except KeyboardInterrupt:
        from utils_app import cierra_programa
        cierra_programa()
