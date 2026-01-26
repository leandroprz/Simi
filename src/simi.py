#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simi by Leandro Pérez
Cambiá el idioma de los programas de Adobe sin reinstalarlos
https://leandroperez.art/tienda/productos-gratuitos/simi-cambia-idioma-adobe-sin-reinstalar/

Versión multiplataforma para Windows y macOS
"""

import os
import re
import platform
import sys
import psutil
import time
import webbrowser
import requests
import subprocess
import shutil
import zipfile
import ctypes
import tempfile
import xml.etree.ElementTree as ET
import colorama
from textwrap import fill
from pathlib import Path
from typing import List
from urllib.parse import urlparse
from colorama import Fore, Style, init
from uuid import UUID
if os.name == 'nt':
    from ctypes import windll, wintypes

# Colorama
colorama.init(strip=False) # Para que funcione en la GUI de tkinter

# Constantes caja UI
CARACTER_BORDE = "─"
ANCHO_PANTALLA = 80
PADDING_INT = 3
PADDING_EXT = 4

# Constantes Simi
VERSION_ACTUAL_SIMI = "2.5"
NOMBRE_RELEASE = "Simi_v"

# Constantes idiomas
TAG_IDIOMAS = r'<Data key="installedLanguages">([^<]*)<\/Data>'

# URLs locales, releases, etc
URLS = {
    'url_locales_win': 'https://github.com/leandroprz/Simi/raw/main/locales/win',
    #'url_locales_win': 'http://localhost/simi/locales/win',
    'url_locales_mac': 'https://github.com/leandroprz/Simi/raw/main/locales/mac',
    #'url_locales_mac': 'http://localhost/simi/locales/mac',
    'latest_vcheck': 'https://github.com/leandroprz/Simi/raw/main/vcheck/latest.txt',
    #'latest_vcheck': 'http://localhost/simi/vcheck/latest.txt',
    'url_releases': 'https://github.com/leandroprz/Simi/releases/download',
    #'url_releases': 'http://localhost/simi/releases/download',
    'url_ayuda_tienda': 'https://leandroperez.art/tienda/productos-gratuitos/simi-cambia-idioma-adobe-sin-reinstalar/',
    'url_reportar_error': 'https://leandroperez.art/contacto/?tu-motivo=Otro'
}

# Textos interfaz
TEXTOS = {
    # Input
    'input_ruta': 'Tipeá la ruta y presioná Enter:',
    'input_opcion': 'Elegí una opción y presioná Enter:',
    'input_error_menu': 'Elegí una opción del menú:',
    'input_error_sn': 'Ingresá S o N:',
    'input_continuar': 'Presioná Enter para continuar:',
    'ruta_instalacion': 'Ingresá la ruta donde instalaste el programa o presioná Enter para usar la ruta por defecto:',
    'input_menu_anterior': 'Presioná Enter para volver al menú anterior:',
    # Menú
    'menu_principal': 'Menú principal',
    'menu_cambio_espanol': 'Cambiar programas al español',
    'menu_cambio_ingles': 'Cambiar programas al inglés',
    'menu_buscar_version': 'Buscar nueva versión de Simi',
    'menu_restaurar_xml': 'Restaurar idioma',
    'menu_usando_bak': 'usando backup de Simi',
    'menu_ayuda': 'Ayuda',
    'menu_reportar_error': 'Reportar un error',
    'menu_salir': 'Salir',
    # Procesos ejecutandose
    'programa_abierto': 'está abierto! Es recomendable cerrarlo antes de cambiar el idioma.',
    'intento_cierre_app': 'Se intentará cambiar el idioma sin cerrar el programa, pero es posible que no se cambie correctamente.\nDeberás reiniciar el programa manualmente para ver el nuevo idioma.',
    'error_cierre': 'Ocurrió un error al intentar cerrar',
    'queres_cerrar': '¿Querés cerrarlo? (S/n):',
    # Admin/sudo
    'permisos_admin_requeridos': 'Error. Se requieren permisos de Administrador/root para descomprimir en la ruta:',
    'ejecutar_como_admin': 'Debes abrir Simi como Administrador.',
    'ejecutar_con_sudo': 'Debes abrir Simi usando sudo.',
    'no_puede_escribir': 'Error. No se pudo escribir en la ruta:',
    'ejecutar_admin_sudo': 'Abrí Simi con permisos de Administrador/root.',
    'cerrar_app': 'Cerrar',
    'cerrar_app_requiere_permisos': 'Se requieren permisos de administrador para cerrar',
    'cerrar_app_error_permisos': 'No se pudieron obtener permisos para cerrar',
    'no_se_detectaron_permisos': 'No tenés permisos de administrador.',
    'error_ejecutar_comando': 'Error al ejecutar el comando:',
    'error_operacion': 'Error al ejecutar la operación:',
    'error_permisos_carpeta_descargas': 'Error de permisos al crear la carpeta de descarga:',
    # Permisos admin macOS
    'macos_osascript_error1': 'Error en el script de autenticación.',
    'macos_osascript_cancelado': 'Operación cancelada por el usuario.',
    'macos_osascript_error2': 'Error de autenticación:',
    'macos_osascript_timeout': 'Timeout al pedir permisos de administrador.',
    'macos_osascript_error3': 'Error al pedir permisos administrativos:',
    'macos_osascript_error_ejecutar': 'Error al ejecutar las operaciones de cambio de idioma:',
    'macos_osascript_timeout2': 'Timeout al ejecutar las operaciones de cambio de idioma.',
    'permisos_insuficientes': 'No tenés permisos suficientes para realizar la operación:',
    # ZIP
    'no_pudo_descomprimir': 'No se pudo descomprimir',
    'zip_error_descomprimir': 'Error al descomprimir el archivo',
    'zip_no_valido_1': 'Error. El archivo',
    'zip_no_valido_2': 'no es un paquete de idioma válido.',
    'zip_permiso_denegado': 'Error. No hay suficientes permisos para descomprimir en la ruta:',
    'copia_permiso_denegado': 'Error. No hay suficientes permisos para copiar a la ruta:',
    'zip_error_unzip': 'Ocurrió un error al descomprimir el paquete de idioma:',
    'zip_parametro_requerido': 'Error. Tenés que agregar el parámetro ruta_unzip cuando uses auto_unzip=True.',
    'zip_error_copia': 'Error al intentar copiar el paquete de idioma:',
    'descarga_no_descomprime': 'No se pudo descomprimir el paquete de idioma.',
    # Cambio idioma
    'copiando_idioma': 'Copiando archivos de idioma...',
    'idioma_cambio_exitoso_1': 'El idioma se cambió al',
    'idioma_cambio_exitoso_2': 'correctamente en la ruta:',
    'idioma_backup_1': 'Se hizo una copia de seguridad en la ruta:',
    'idioma_backup_2': 'Vas a necesitar ese archivo si algo malió sal.',
    'no_cambio': '¡No se pudo cambiar el idioma!',
    'razones': 'Puede ser por diferentes razones:\n• El programa no está instalado en la ruta que ingresaste\n• La versión que elegiste no está instalada en tu computadora\n• Simi no encontró el archivo application.xml en la ruta que ingresaste\n• El programa no se instaló usando la aplicación Adobe Creative Cloud',
    'no_restauro': '¡No se pudo restaurar el idioma!',
    'razones_bak': 'Puede ser por diferentes razones:\n• El programa no está instalado en la ruta que ingresaste\n• La versión que elegiste no está instalada en tu computadora\n• Simi no encontró el archivo application.bak en la ruta que ingresaste',
    'cambiar_idioma': 'Cambiar idioma de',
    'al': 'al',
    'cambiar_a': 'Cambiar a',
    'cambiar_programas': 'Cambiar programas al',
    'cambio_ps': 'Podés elegir el nuevo idioma desde Photoshop, ingresando al menú Editar > Preferencias > Interfaz > Idioma de la interfaz.\nReiniciá Photoshop para ver los cambios.',
    'error_inesperado': 'Error inesperado:',
    'restauro_correctamente_1': 'El idioma se restauró correctamente al',
    'restauro_correctamente_2': 'usando la copia de seguridad en la ruta:',
    'restaura_ps': 'Podés volver al idioma anterior desde Photoshop, ingresando al menú Editar > Preferencias > Interfaz > Idioma de la interfaz.\nReiniciá Photoshop para ver los cambios.',
    # Connectividad y descarga
    'archivo_existente': 'Se usará el archivo que se descargó previamente en la ruta:',
    'descargando': 'Descargando archivo...',
    'descarga_a_medias_1': 'Hubo un problema con la descarga.',
    'descarga_a_medias_2': 'Se descargaron',
    'descarga_a_medias_3': 'pero deberían haberse descargado',
    'descarga_exitosa': 'El archivo se descargó correctamente en la ruta:',
    'error_descarga_idioma': 'No se pudo descargar correctamente el paquete de idioma.',
    'error_descarga': 'No se pudo descargar el archivo.',
    'error_guardar_archivo': 'No se pudo guardar el archivo.',
    'no_pudo_chequear_version': 'No se pudo comprobar la última versión.',
    'titulo_version_update_1': 'Buscando nueva versión...',
    'titulo_version_update_2': 'Descargando nueva versión',
    'nueva_v_disponible': '¡Hay una nueva versión disponible!:',
    'desea_descargar': '¿Querés descargarla? (S/n):',
    'desea_abrir': '¿Querés abrir la nueva versión? (S/n):',
    'no_descargo': 'No se pudo descargar la nueva versión.',
    'usando_ultima_version': 'Ya tenés la última versión:',
    'version_actual_1': 'La versión que estás usando',
    'version_actual_2': 'es más nueva que la última versión disponible para descargar:',
    # Simi
    'simi_titulo': 'Simi by Leandro Pérez',
    'simi_descripcion': 'Cambiá el idioma de Adobe sin reinstalar los programas',
    'agradecimiento': 'Gracias por usar Simi.',
    'mensaje_resenia': '¡No olvides dejarnos una reseña en www.leandroperez.art!',
    'mensaje_url_ayuda': 'En breve se abrirá la página de ayuda.',
    'mensaje_reportar_error': 'En breve se abrirá la página para reportar un error.',
    'aviso_importante_1': 'Aviso importante',
    'aviso_importante_2': 'Los paquetes de idioma que se usan en este programa pertenecen a Adobe y sus respectivos propietarios.',
    'aviso_importante_3': 'Este software solo facilita su gestión y se proporcionan únicamente con fines educativos.',
    # Misc
    'de': 'de',
    'barra_progreso_modo1': 'Modo no soportado:',
    'barra_progreso_modo2': 'Usá descarga, unzip o copia.',
    'error_ruta_descargas': 'No se pudo obtener la ruta de la carpeta Descargas.',
    'no_soportado': 'Sistema no soportado',
    'error_en_script': 'Error en el script:'
}

class BarraProgreso:
    def __init__(self, total, modo='descarga', tiempo_actualizacion=0.1):
        """
        Barra de carga que se muestra al descargar, copiar o extraer archivos.

        Args:
            total (int): Total de unidades a procesar (bytes si se descarga, archivos si se copia o descomprime)
            modo (str): Modo de operación - 'descarga', 'unzip', 'copia'
            tiempo_actualizacion (float): Intervalo de tiempo en segundos para mostrar los updates en pantalla
        """
        self.total = total
        self.actual = 0
        self.modo = modo.lower()
        self.tiempo_inicio = time.time()
        self.ultima_actualizacion = 0
        self.tiempo_actualizacion = tiempo_actualizacion
        self.item_actual = ""

        # Config para cada modo
        self.config_modo = {
            'descarga': {
                'unidad': 'B',
                'sufijo_velocidad': '/s',
                'formato_func': self._formato_bytes,
                'formato_progreso': '{porcentaje:3d}% |{barra}| {formato_actual}/{formato_total} [{formato_velocidad}]'
            },
            'unzip': {
                'unidad': 'files',
                'sufijo_velocidad': '/s',
                'formato_func': self._formato_cantidad,
                'formato_progreso': '{porcentaje:3d}% |{barra}| {actual}/{total} archivos [{velocidad:.1f}/s]'
            },
            'copia': {
                'unidad': 'files',
                'sufijo_velocidad': '/s',
                'formato_func': self._formato_cantidad,
                'formato_progreso': '{porcentaje:3d}% |{barra}| {actual}/{total} archivos [{velocidad:.1f}/s]'
            }
        }

        if self.modo not in self.config_modo:
            raise ValueError(f"{TEXTOS['barra_progreso_modo1']} {modo}. {TEXTOS['barra_progreso_modo2']}")

    def _formato_bytes(self, valor_bytes):
        """ Formatea bytes a otras unidades """
        for unidad in ['B', 'KB', 'MB', 'GB']:
            if valor_bytes < 1024.0:
                return f"{valor_bytes:.1f} {unidad}"
            valor_bytes /= 1024.0
        return f"{valor_bytes:.1f} TB"

    def _formato_cantidad(self, contador):
        """ Formatea contador para que muestre un único número """
        return str(int(contador))

    def actualiza(self, incremento, item_actual=""):
        """
        Progreso de la actualización de la barra

        Args:
            incremento (int): Monto a incrementar (bytes si es descarga, 1 para archivos)
            item_actual (str): Item que se está procesado actualmente (filename, etc.)
        """
        self.actual += incremento
        self.item_actual = item_actual
        tiempo_actual = time.time()

        # Actualiza lo que se muestra según el intervalo
        if tiempo_actual - self.ultima_actualizacion > self.tiempo_actualizacion:
            self.muestra_progreso()
            self.ultima_actualizacion = tiempo_actual

    def muestra_progreso(self):
        """ Muestra la barra de progreso """
        # Calcula el progreso
        porcentaje = int((self.actual / self.total) * 100) if self.total > 0 else 0

        # Calcula la velocidad
        tiempo_transcurrido = time.time() - self.tiempo_inicio
        velocidad = self.actual / tiempo_transcurrido if tiempo_transcurrido > 0 else 0

        # Get configuración según modo
        config = self.config_modo[self.modo]
        ancho_disponible = ANCHO_PANTALLA - 4 - PADDING_INT * 2

        if self.modo == 'descarga':
            # Formato de descarga (bytes)
            formato_actual = config['formato_func'](self.actual)
            formato_total = config['formato_func'](self.total)
            formato_velocidad = config['formato_func'](velocidad) + config['sufijo_velocidad']

            # Calcula espacios para la barra de progreso
            partes_texto = f"{porcentaje:3d}% || {formato_actual}/{formato_total} [{formato_velocidad}]"
            longitud_texto = len(partes_texto)
            ancho_barra = max(10, ancho_disponible - longitud_texto)

            ancho_completado = int((self.actual / self.total) * ancho_barra) if self.total > 0 else 0
            barra = "█" * ancho_completado + "░" * (ancho_barra - ancho_completado)

            texto_progreso = f"{porcentaje:3d}% |{barra}| {formato_actual}/{formato_total} [{formato_velocidad}]"

        else:
            # Formato para modo unzip/copia (archivos)
            partes_texto = f"{porcentaje:3d}% || {self.actual}/{self.total} archivos [{velocidad:.1f}/s]"
            longitud_texto = len(partes_texto)
            ancho_barra = max(10, ancho_disponible - longitud_texto)

            ancho_completado = int((self.actual / self.total) * ancho_barra) if self.total > 0 else 0
            barra = "█" * ancho_completado + "░" * (ancho_barra - ancho_completado)

            texto_progreso = f"{porcentaje:3d}% |{barra}| {self.actual}/{self.total} archivos [{velocidad:.1f}/s]"

        # Acorta si es muy larga
        if len(texto_progreso) > ancho_disponible:
            texto_progreso = texto_progreso[:ancho_disponible-3] + "..."

        # Agrega padding
        padding_relleno = " " * (ancho_disponible - len(texto_progreso))
        linea_interna = f'{" " * PADDING_INT}{texto_progreso}{padding_relleno}{" " * PADDING_INT}'

        # Print con carriage return para sobreescribir la línea
        print(f'\r{" " * PADDING_EXT}│ {linea_interna} │', end='', flush=True)

    def finaliza(self):
        """ Completa el progreso y continua con la línea siguiente """
        self.muestra_progreso()
        print() # Nueva línea luego de finalizar

def limpia_pantalla():
    """
    Limpia la pantalla, compatible con gui_wrapper.py
    """
    print('\x1b[2J\x1b[H', end='')
    print("\n\n", end="")

def borde_superior(texto_izq="", texto_der=""):
    """
    Muestra el borde superior con texto a la izquierda y derecha para armar la caja de contenido

    Formato: ╭─ texto_izq ───── texto_der ─╮

    Args:
        texto_izq (str): Texto que se muestra en la izquierda.
        texto_der (str): Texto que se muestra en la derecha.
    """
    ancho_total = ANCHO_PANTALLA - 2

    # Limpia el texto de códigos de color para calcular longitud real
    texto_izq_limpio = re.sub(r'\x1b\[[0-9;]*m', '', texto_izq)
    texto_der_limpio = re.sub(r'\x1b\[[0-9;]*m', '', texto_der)

    # Calcula espacios necesarios
    if texto_izq_limpio and texto_der_limpio:
        # Si existen ambos textos
        espacios_libres = ancho_total - len(texto_izq_limpio) - len(texto_der_limpio) - 6 # -6 por "─ " + " " + " " + "─"
        if espacios_libres < 5: # Mínimo 5 guiones de separación
            espacios_libres = 5

        borde_medio = CARACTER_BORDE * espacios_libres
        linea_superior = f"╭{CARACTER_BORDE} {texto_izq} {borde_medio} {texto_der} {CARACTER_BORDE}╮"

    elif texto_izq_limpio:
        # Solo texto izquierdo
        espacios_libres = ancho_total - len(texto_izq_limpio) - 3 # -3 por "─ " + " "
        borde_resto = CARACTER_BORDE * espacios_libres
        linea_superior = f"╭{CARACTER_BORDE} {texto_izq} {borde_resto}╮"

    elif texto_der_limpio:
        # Solo texto derecho
        espacios_libres = ancho_total - len(texto_der_limpio) - 3 # -3 por " " + " ─"
        borde_resto = CARACTER_BORDE * espacios_libres
        linea_superior = f"╭{borde_resto} {texto_der} {CARACTER_BORDE}╮"

    else:
        # Sin texto
        linea_superior = "╭" + CARACTER_BORDE * ancho_total + "╮"

    print(" " * PADDING_EXT + linea_superior + Style.RESET_ALL)

def borde_inferior():
    """
    Muestra el borde inferior para armar la caja de contenido

    Formato: ╰─────────────────────────────────╯
    """
    print(" " * PADDING_EXT + "╰" + CARACTER_BORDE * (ANCHO_PANTALLA - 2) + "╯")

def extrae_codigos_color_activos(texto):
    """
    Extrae todos los códigos de color que están activos al final del texto

    Args:
        texto (str): Texto al que se le extrae el código de color
    """
    # Busca todos los códigos ANSI en el texto
    codigos = re.findall(r'\x1b\[[0-9;]*m', texto)

    # Si no hay códigos, no hay colores activos
    if not codigos:
        return ""

    # El último código determina el estado actual
    ultimo_codigo = codigos[-1]

    # Si es un reset, no hay colores activos
    if ultimo_codigo == '\x1b[0m' or 'RESET' in ultimo_codigo:
        return ""

    # Si es un código de color, ese es el activo
    return ultimo_codigo

def muestra_contenido(texto):
    """
    Muestra el texto dentro de la caja de contenido redondeada y agrega padding por dentro y fuera

    Args:
        texto (str): El texto del contenido
    """
    lineas = texto.split("\n")
    colores_heredados = ""

    for linea in lineas:
        # Si la línea está vacía, muestra una línea vacía y mantiene colores heredados
        if not linea.strip():
            print(" " * PADDING_EXT + "│" + " " * (ANCHO_PANTALLA - 2) + "│")
            continue

        # Busca códigos de color en la línea actual
        codigos_en_linea = re.findall(r'\x1b\[[0-9;]*m', linea)

        # Si la línea tiene códigos de color, se usan, si no, usa los colores heredados
        if codigos_en_linea:
            # La línea tiene su propio color
            linea_con_colores = linea
            # Actualiza colores heredados basado en esta línea
            colores_heredados = extrae_codigos_color_activos(linea)
        else:
            # La línea no tiene color, se usan colores heredados
            linea_con_colores = colores_heredados + linea

        # Extrae solo el texto visible (sin códigos de color)
        linea_visible = re.sub(r'\x1b\[[0-9;]*m', '', linea_con_colores)

        # Calcula ancho disponible
        ancho_disponible = ANCHO_PANTALLA - 4 - PADDING_INT * 2

        # Envuelve el texto si es necesario
        if len(linea_visible) > ancho_disponible:
            lineas_envueltas = fill(linea_visible, width=ancho_disponible).split("\n")

            # Para cada línea envuelta, aplica el color correcto
            for i, linea_envuelta in enumerate(lineas_envueltas):
                if codigos_en_linea:
                    # Usa el color de la línea original
                    color_a_usar = "".join(codigos_en_linea)
                else:
                    # Usa colores heredados
                    color_a_usar = colores_heredados

                texto_coloreado = f"{color_a_usar}{linea_envuelta}{Style.RESET_ALL}"

                # Calcula padding
                len_visible_actual = len(linea_envuelta)
                padding_relleno = " " * (ancho_disponible - len_visible_actual)

                # Crea línea interna con reset para evitar bleeding en el borde
                linea_interna = f'{" " * PADDING_INT}{texto_coloreado}{padding_relleno}{" " * PADDING_INT}'
                print(f'{" " * PADDING_EXT}│ {linea_interna} │{Style.RESET_ALL}')
        else:
            # La línea cabe en una sola línea
            if codigos_en_linea:
                # Usa el color de la línea original
                color_a_usar = "".join(codigos_en_linea)
            else:
                # Usa colores heredados
                color_a_usar = colores_heredados

            texto_coloreado = f"{color_a_usar}{linea_visible}{Style.RESET_ALL}"

            # Calcula padding
            len_visible_actual = len(linea_visible)
            padding_relleno = " " * (ancho_disponible - len_visible_actual)

            # Crea línea interna con reset para evitar bleeding en el borde
            linea_interna = f'{" " * PADDING_INT}{texto_coloreado}{padding_relleno}{" " * PADDING_INT}'
            print(f'{" " * PADDING_EXT}│ {linea_interna} │{Style.RESET_ALL}')

def titulo_subrayado(texto, caracter_subrayado="─", color=""):
    """
    Subraya el texto según su longitud, para usar en los títulos de los menús

    Args:
        texto (str): El texto del título
        caracter_subrayado (str): Caracter para el subrayado (default: ─)
        color (str, opcional): Código de color de Colorama

    Returns:
        str: Texto subrayado para usar en los títulos
    """
    # Quita códigos de color para calcular la longitud real
    texto_limpio = re.sub(r'\x1b\[[0-9;]*m', '', texto)

    # Crea la línea de subrayado con la misma longitud
    subrayado = caracter_subrayado * len(texto_limpio)

    # Aplica un color si se especifica
    if color:
        texto_coloreado = f"{color}{texto}{Style.RESET_ALL}"
        resultado = f"{texto_coloreado}\n{subrayado}"
    else:
        resultado = f"{texto}\n{subrayado}"

    return resultado

def muestra_input_usuario(mensaje=None):
    """
    Pide input al usuario para los diferentes menús y funciones

    Args:
        mensaje (str): Texto del input

    Returns:
        str: Mensaje que se muestra al usuario
    """
    padding_total = PADDING_EXT + 1
    texto_prompt = mensaje if mensaje is not None else TEXTOS['input_opcion']
    print("\n" + (" " * padding_total) + texto_prompt)

    return input(" " * padding_total + "> ")

def versiones_adobe_macos(version_adobe):
    """
    Contiene las versiones de los programas de Adobe según el año ya que en macOS se usa la versión de la app (major release) en lugar del año para la ruta del archivo XML.
    Nota: en el 2022 Adobe unificó todas las versiones según el año (por lo menos para las apps aquí listadas).

    Args:
        version_adobe (int): Año 2018+

    Returns:
        dict: Diccionario que contiene el nombre de los programas como key y las versiones como valores.
    """

    # Programas de Adobe con sus respectivas versiones
    versiones_adobe_map = {
        'after_effects': {
            2018: '15.0',
            2019: '16.0',
            2020: '17.0',
            2021: '18.0',
            2022: '22.0',
            2023: '23.0',
            2024: '24.0',
            2025: '25.0'
        },
        'audition': {
            2018: '11.0',
            2019: '12.0',
            2020: '13.0',
            2021: '14.0',
            2022: '22.0',
            2023: '23.0',
            2024: '24.0',
            2025: '25.0'
        },
        'character_animator': {
            2018: '1.1',
            2019: '2.0',
            2020: '3.0',
            2021: '4.0',
            2022: '22.0',
            2023: '23.0',
            2024: '24.0',
            2025: '25.0'
        },
        'media_encoder': {
            2018: '12.0',
            2019: '13.0',
            2020: '14.0',
            2021: '15.0',
            2022: '22.0',
            2023: '23.0',
            2024: '24.0',
            2025: '25.0'
        },
        'premiere_pro': {
            2018: '12.0',
            2019: '13.0',
            2020: '14.0',
            2021: '15.0',
            2022: '22.0',
            2023: '23.0',
            2024: '24.0',
            2025: '25.0'
        }
    }

    # Crea un diccionario con todos los programas y sus respectivas versiones según el año
    resultado = {}
    for programa_adobe, versiones in versiones_adobe_map.items():
        resultado[programa_adobe] = versiones[version_adobe]

    return resultado

def rutas_adobe_macos(nombre_programa, version_adobe):
    """
    Devuelve la ruta de instalación por defecto de cada programa de Adobe en macOS, usando el nombre del programa y el año ingresado.

    Args:
        nombre_programa (str): ID del programa (after_effects, audition, character_animator, media_encoder, premiere_pro, animator, illustrator, incopy, indesign, photoshop)
        version_adobe (int): Año 2018+

    Returns:
        str o list: Ruta de instalación por defecto para el programa con su respectivo año
    """

    # Obtiene la versión según el año
    versiones_dict = versiones_adobe_macos(version_adobe)
    if not versiones_dict:
        return None

    # Nombre de los programas con sus respectivas rutas por defecto
    rutas_programas_map = {
        # Programas con ruta default en "/Library/Application Support" (usan la versión en el nombre de la carpeta donde está el XML)
        'after_effects': {
            'ruta_default': '/Library/Application Support/Adobe/After Effects',
            'nombre_programa_adobe': 'After Effects'
        },
        'audition': {
            'ruta_default': '/Library/Application Support/Adobe/Audition',
            'nombre_programa_adobe': 'Audition'
        },
        'character_animator': {
            'ruta_default': '/Library/Application Support/Adobe/Character Animator',
            'nombre_programa_adobe': 'Character Animator'
        },
        'media_encoder': {
            'ruta_default': '/Library/Application Support/Adobe/Media Encoder',
            'nombre_programa_adobe': 'Media Encoder'
        },
        'premiere_pro': {
            'ruta_default': '/Library/Application Support/Adobe/Premiere Pro',
            'nombre_programa_adobe': 'Premiere Pro'
        },

        # Programas con ruta default en "/Applications" (usan el año en el nombre de la carpeta)
        'animate': {
            'ruta_default': '/Applications/Adobe Animate',
            'nombre_programa_adobe': 'Animate'
        },
        'illustrator': {
            'ruta_default': '/Applications/Adobe Illustrator',
            'nombre_programa_adobe': 'Illustrator'
        },
        'incopy': {
            'ruta_default': '/Applications/Adobe InCopy',
            'nombre_programa_adobe': 'InCopy'
        },
        'indesign': {
            'ruta_default': '/Applications/Adobe InDesign',
            'nombre_programa_adobe': 'InDesign'
        },
        'photoshop': {
            'ruta_default': '/Applications/Adobe Photoshop',
            'nombre_programa_adobe': 'Photoshop'
        }
    }

    informacion_programa = rutas_programas_map[nombre_programa]

    # Devuelve los programas en la ruta "/Library/Application Support" (solo necesitan cambios en el archivo XML)
    if nombre_programa in ['after_effects', 'audition', 'character_animator', 'media_encoder', 'premiere_pro']:
        version = versiones_dict[nombre_programa]
        return f"{informacion_programa['ruta_default']}/{version}"

    # Devuelve los programas en la ruta "/Applications" (animate, illustrator, incopy, indesign, photoshop) - Se debe descargar un paquete de idiomas
    else:
        return f"{informacion_programa['ruta_default']} {version_adobe}"

def get_version_macos(version_adobe, nombre_programa):
    """
    Obtiene en macOS la versión del programa de Adobe según el año ingresado

    Args:
        version_adobe (int): Año 2018+
        nombre_programa (str): Nombre del programa de Adobe (after_effects, audition, character_animator, media_encoder, premiere_pro)

    Returns:
        str: Version del programa de Adobe como string para usar en una ruta (ej: 22.0)
    """
    versiones_dict = versiones_adobe_macos(version_adobe)
    if versiones_dict and nombre_programa in versiones_dict:
        return versiones_dict[nombre_programa]
    return None

def ruta_instalacion_programa(ruta_subcarpeta=None, nombre_programa=None, version_adobe=None):
    """
    Permite ingresar una ruta de instalación para cada programa de Adobe o se usa la ruta por defecto, según el año

    Args:
        ruta_subcarpeta (str): Subcarpeta para usar en Windows
        nombre_programa (str): ID de cada programa para macOS
        version_adobe (int): Año para las rutas en macOS

    Returns:
        Path: Ruta de instalación final ingresada por el usuario o ruta por defecto
    """
    # Rutas en Windows
    if platform.system() == 'Windows' or not nombre_programa:
        ruta_base = os.environ['PROGRAMW6432'] + "\\Adobe"
        ruta_instalacion_default = os.path.join(ruta_base, ruta_subcarpeta) if ruta_subcarpeta else ruta_base

    # macOS
    else:
        rutas_default = rutas_adobe_macos(nombre_programa, version_adobe)

        if rutas_default is None:
            # Fallback en caso de no encontrarse nada en programa_adobe
            ruta_base = "/Applications/Adobe"
            ruta_instalacion_default = os.path.join(ruta_base, ruta_subcarpeta) if ruta_subcarpeta else ruta_base

            # Pide ruta al usuario
            muestra_contenido(
                f"\n{Fore.LIGHTCYAN_EX}{TEXTOS['ruta_instalacion']}\n"
                f"[{ruta_instalacion_default}]\n"
            )
            borde_inferior()

        else:
            ruta_instalacion_default = rutas_default

    # Pide ruta al usuario
    muestra_contenido(
        f"\n{Fore.LIGHTCYAN_EX}{TEXTOS['ruta_instalacion']}\n"
        f"[{ruta_instalacion_default}]\n"
    )
    borde_inferior()

    input_usuario = muestra_input_usuario(f"{TEXTOS['input_ruta']}").strip()
    ruta_instalacion_final = input_usuario if input_usuario else ruta_instalacion_default
    ruta_corregida = str(Path(ruta_instalacion_final).resolve())

    return Path(ruta_corregida)

def chequea_cierra_app(nombre_app: str) -> bool:
    """
    Chequea si una aplicación está ejecutándose y pregunta al usuario si quiere cerrarla

    Args:
        nombre_app (str): Nombre de la aplicación a cerrar (ej: "Adobe After Effects", "audition", "Photoshop")

    Returns:
        bool: True si la app se encontró y cerró, False si la app no estaba abierta
    """

    def busca_procesos_por_nombre(nombre: str) -> List[psutil.Process]:
        """ Busca todos los procesos según el nombre indicado (case-insensitive) """
        procesos = []
        nombre_lower = nombre.lower()

        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                info_proc = proc.info
                nombre_proc = info_proc['name'] or ''
                exe_proc = info_proc['exe'] or ''

                # Chequea si el nombre coincide con el nombre del proceso o la ruta desde donde se ejecuta
                if (nombre_lower in nombre_proc.lower() or
                    nombre_lower in exe_proc.lower()):
                    procesos.append(proc)

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Los procesos terminaron de ejecutarse o no hay permisos para chequear
                continue

        return procesos

    def get_procesos_children(proceso: psutil.Process) -> List[psutil.Process]:
        """ Obtiene todos los procesos children de forma recursiva """
        children = []
        try:
            for child in proceso.children(recursive=True):
                children.append(child)
        except psutil.NoSuchProcess:
            pass
        return children

    def finaliza_arbol_de_procesos(proceso: psutil.Process) -> bool:
        """ Finaliza todos los procesos y sus children """
        try:
            # Get todos los children
            children = get_procesos_children(proceso)

            # Finaliza los children
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

            # Espera que finalice el proceso principal
            try:
                proceso.wait(timeout=5)
            except psutil.TimeoutExpired:
                proceso.kill()
                proceso.wait(timeout=3)

            return True

        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            return False

    def requiere_permisos_para_cerrar_proceso(proceso: psutil.Process) -> bool:
        """ Determina si se necesitan permisos administrativos para cerrar un proceso """
        try:
            # En macOS verifica si el proceso está en las siguientes rutas
            if platform.system() == 'Darwin':
                ruta_exe = proceso.exe()
                rutas_sistema = [
                    '/Applications',
                    '/System',
                    '/usr',
                    '/bin',
                    '/sbin'
                ]
                return any(ruta_exe.startswith(ruta) for ruta in rutas_sistema)

            # En Windows verifica si está en Program Files
            elif platform.system() == 'Windows':
                ruta_exe = proceso.exe()
                rutas_program_files = [
                    os.environ.get('PROGRAMW6432', ''),
                    os.environ.get('PROGRAMFILES(X86)', '')
                ]
                return any(ruta_exe.lower().startswith(ruta.lower()) for ruta in rutas_program_files if ruta)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Si no se puede acceder al proceso, probablemente se necesitan permisos
            return True

        return False

    # Busca procesos que coincidan con el nombre del programa
    procesos_coinciden = busca_procesos_por_nombre(nombre_app)

    if not procesos_coinciden:
        return False

    muestra_contenido(f"{Fore.LIGHTRED_EX}¡{nombre_app} {TEXTOS['programa_abierto']}\n")
    borde_inferior()

    titulo_menu = titulo_subrayado(f"{TEXTOS['cambiar_idioma']} {nombre_app} {TEXTOS['al']} {idioma_menu_ui}")

    while True:
        respuesta = muestra_input_usuario(f"{TEXTOS['queres_cerrar']}").upper().strip() or 'S'
        if respuesta == 'S':
            break
        elif respuesta == 'N':
            limpia_pantalla()

            borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
            muestra_contenido(
                f"\n{TEXTOS['simi_descripcion']}\n\n"
                f"\n{titulo_menu}\n\n"
                f"{Fore.LIGHTYELLOW_EX}{TEXTOS['intento_cierre_app']}\n"
            )
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_continuar']}").upper().strip()
            return True

        else:
            muestra_contenido(f"{TEXTOS['input_error_sn']}")

    # Verifica si algún proceso requiere permisos administrativos
    necesita_permisos_admin = any(requiere_permisos_para_cerrar_proceso(proc) for proc in procesos_coinciden)

    # Intenta cerrar procesos sin permisos de admin primero
    if not necesita_permisos_admin:
        contador_procesos_cerrados = 0
        for proc in procesos_coinciden:
            try:
                if finaliza_arbol_de_procesos(proc):
                    contador_procesos_cerrados += 1
            except Exception as e:
                muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_cierre']} {nombre_app} (PID: {proc.pid}). Error: {e}.\n")
        return contador_procesos_cerrados > 0

    # Si requiere permisos administrativos, agrega a operaciones pendientes
    global operaciones_pendientes_admin
    if 'operaciones_pendientes_admin' not in globals():
        operaciones_pendientes_admin = []

    sistema = platform.system()
    for proc in procesos_coinciden:
        if sistema == 'Darwin':
            operaciones_pendientes_admin.append({
                'tipo': 'comando',
                'comando': f"kill -TERM {proc.pid} 2>/dev/null || kill -KILL {proc.pid} 2>/dev/null",
                'descripcion': f'{TEXTOS['cerrar_app']} {nombre_app} (PID: {proc.pid})'
            })
        else: # Windows
            operaciones_pendientes_admin.append({
                'tipo': 'comando',
                'comando': f'taskkill /PID {proc.pid} /F',
                'descripcion': f'{TEXTOS['cerrar_app']} {nombre_app} (PID: {proc.pid})'
            })

    return True

def get_carpeta_descargas() -> str:
    """
    Obtiene la carpeta Descargas del usuario en Windows (incluso si fue movida) y macOS

    Returns:
        str: Ruta de la carpeta Descargas
    """
    if os.name == 'nt': # Windows
        class GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", wintypes.DWORD),
                ("Data2", wintypes.WORD),
                ("Data3", wintypes.WORD),
                ("Data4", wintypes.BYTE * 8)
            ]
            def __init__(self, uuid_str):
                uuid = UUID(uuid_str)
                ctypes.Structure.__init__(self)
                self.Data1, self.Data2, self.Data3, \
                    self.Data4[0], self.Data4[1], rest = uuid.fields

                for i in range(2, 8):
                    self.Data4[i] = rest>>(8-i-1)*8 & 0xff

        SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
        SHGetKnownFolderPath.argtypes = [
            ctypes.POINTER(GUID), wintypes.DWORD,
            wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
        ]

        def _get_ruta_carpeta_descargas(uuid_str: str) -> str:
            ruta_ptr = ctypes.c_wchar_p()
            guid = GUID(uuid_str)

            if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(ruta_ptr)):
                raise ctypes.WinError()

            # Se asegura de tener una ruta válida
            if ruta_ptr.value is None:
                raise ValueError(f"{Fore.LIGHTRED_EX}{TEXTOS['error_ruta_descargas']}")

            return ruta_ptr.value

        id_carpeta_downloads = '{374DE290-123F-4565-9164-39C4925E467B}'
        return _get_ruta_carpeta_descargas(id_carpeta_downloads)

    else: # macOS
        home = os.path.expanduser("~")
        return os.path.join(home, "Downloads")

def detecta_encoding(ruta_archivo):
    """
    Detecta el encoding de un archivo XML usando la detección automática del parser

    Args:
        ruta_archivo (str): Ruta donde está el archivo XML

    Returns:
        str: Encoding detectado o 'utf-8' como fallback
    """
    try:
        # XML parser hace su magia automáticamente
        tree = ET.parse(ruta_archivo)
        # Si está todo OK, entonces se detectó correctamente el encoding y luego lo extrae del XML
        with open(ruta_archivo, 'rb') as f:
            primera_linea = f.readline().decode('ascii', errors='ignore')

        coincide = re.search(r'encoding\s*=\s*["\']([^"\']+)["\']', primera_linea, re.IGNORECASE)

        if coincide:
            return coincide.group(1).lower()
        return 'utf-8' # Default

    except:
        return 'utf-8' # Fallback

def es_administrador():
    """
    Chequea si el script está ejecutándose como Administrador/root

    Returns:
        bool: True si es admin/root, de lo contrario False
    """
    sistema = platform.system()

    try:
        if sistema == 'Windows':
            return ctypes.windll.shell32.IsUserAnAdmin() # type: ignore
        elif sistema == 'Darwin': # macOS
            return os.geteuid() == 0 # type: ignore
        else:
            return False

    except (AttributeError, OSError):
        return False

def requiere_permisos_administrativos(ruta):
    """
    Chequea si en las rutas donde se instalan los programas de Adobe se requieren permisos de Administrador/root

    Args:
        ruta (str): Ruta en la que se chequean los permisos
    """
    sistema = platform.system()
    ruta = os.path.abspath(ruta)

    if sistema == 'Windows':
        rutas_protegidas = [
            os.environ.get('PROGRAMW6432', '') + "\\Adobe",
            os.environ.get('PROGRAMFILES(X86)', '') + "\\Adobe"
        ]
        return any(ruta.lower().startswith(protegida.lower()) for protegida in rutas_protegidas if protegida)

    elif sistema == 'Darwin':
        rutas_protegidas = [
            "/Applications",
            "/Library/Application Support"
        ]

        # Chequea rutas del sistema
        if any(ruta.startswith(protegida) for protegida in rutas_protegidas):
            return True

        # Chequea si el archivo/carpeta existe y pertenece a root
        try:
            if os.path.exists(ruta):
                stat_info = os.stat(ruta)
                # Si el archivo pertenece a root (UID 0), requiere permisos
                if stat_info.st_uid == 0:
                    return True
            else:
                # Si no existe, chequea la carpeta padre
                carpeta_padre = os.path.dirname(ruta)
                if carpeta_padre and os.path.exists(carpeta_padre):
                    stat_info = os.stat(carpeta_padre)
                    if stat_info.st_uid == 0:
                        return True

        except (OSError, PermissionError):
            # Si no se puede acceder, asume que requiere permisos
            return True

    return False

def chequea_permisos_escritura(ruta):
    """
    Chequea si se puede escribir en una ruta

    Args:
        ruta (str): Ruta en la que se hace el chequeo

    Returns:
        bool: True si se puede escribir, caso contrario False
    """
    try:
        # Si la ruta existe, chequea si es escribible
        if os.path.exists(ruta):
            # En macOS, chequea si el archivo pertenece a root
            if platform.system() == 'Darwin':
                stat_info = os.stat(ruta)
                if stat_info.st_uid == 0:
                    return False

            # Intenta crear un archivo temporal para chequear los permisos de escritura
            archivo_prueba = os.path.join(ruta, ".test_temp")
            with open(archivo_prueba, 'w') as f:
                f.write("test")
            os.remove(archivo_prueba)
            return True

        else:
            # Si no existe, intenta crear la carpeta
            os.makedirs(ruta, exist_ok=True)

            # Chequea si la carpeta creada pertenece a root en macOS
            if platform.system() == 'Darwin':
                stat_info = os.stat(ruta)
                if stat_info.st_uid == 0:
                    return False

            # Intenta crear un archivo temporal
            archivo_prueba = os.path.join(ruta, ".test_temp")
            with open(archivo_prueba, 'w') as f:
                f.write("test")
            os.remove(archivo_prueba)
            return True

    except (PermissionError, OSError):
        return False

def agregar_operacion_pendiente(operacion):
    """
    Agrega una operación a la lista de operaciones pendientes que requieren permisos de Admin/root.

    Args:
        operacion (dict): Operación a agregar
    """
    global operaciones_pendientes_admin
    if 'operaciones_pendientes_admin' not in globals():
        operaciones_pendientes_admin = []

    operaciones_pendientes_admin.append(operacion)

def ejecutar_operaciones_pendientes(titulo="Operaciones con permisos administrativos", mensaje="Se requieren permisos de administrador para completar las operaciones pendientes", muestra_mensaje_func=None):
    """
    Ejecuta todas las operaciones pendientes que requieren permisos administrativos de un solo saque

    Returns:
        tuple: (success: bool, results: list, error: str)
    """
    global operaciones_pendientes_admin

    if 'operaciones_pendientes_admin' not in globals() or not operaciones_pendientes_admin:
        return True, [], ""

    # Ejecuta todas las operaciones pendientes (ya incluyen la copia de archivos con admin)
    success, results, error = ejecutar_operacion_con_permisos(
        operaciones_pendientes_admin,
        titulo=titulo,
        mensaje=mensaje,
        muestra_mensaje_func=muestra_mensaje_func
    )

    # Limpia la lista de operaciones pendientes
    operaciones_pendientes_admin = []

    return success, results, error

def ejecutar_operacion_con_permisos(operaciones, titulo="Se requieren permisos administrativos", mensaje="Se requieren permisos de administrador para realizar esta operación", muestra_mensaje_func=None):
    """
    Ejecuta múltiples operaciones con permisos administrativos de un solo saque

    Args:
        operaciones (list): Lista de diccionarios con operaciones:
                           {'tipo': 'comando', 'comando': 'comando_shell'}
                           {'tipo': 'archivo', 'origen': 'ruta', 'destino': 'ruta'}
                           {'tipo': 'contenido', 'contenido': 'texto', 'destino': 'ruta', 'encoding': 'utf-8'}

    Returns:
        tuple: (success: bool, results: list, error: str)
    """
    def mostrar_mensaje(msj):
        if muestra_mensaje_func:
            muestra_mensaje_func(msj)
        else:
            print(msj)

    sistema = platform.system()

    if sistema == 'Windows':
        if not es_administrador():
            return False, [], f"{TEXTOS['no_se_detectaron_permisos']}"
        return _ejecutar_operaciones_windows(operaciones, mostrar_mensaje)

    elif sistema == 'Darwin':
        return _ejecutar_operaciones_macos(operaciones, titulo, mensaje, mostrar_mensaje)

    return False, [], f"{Fore.LIGHTRED_EX}{TEXTOS['no_soportado']}"

def _ejecutar_operaciones_windows(operaciones, mostrar_mensaje):
    """ Ejecuta operaciones en Windows usando permisos existentes """
    resultados = []

    for operacion in operaciones:
        try:
            if operacion['tipo'] == 'comando':
                resultado = subprocess.run(operacion['comando'], shell=True, capture_output=True, text=True)
                resultados.append({
                    'tipo': 'comando',
                    'exitoso': resultado.returncode == 0,
                    'salida': resultado.stdout,
                    'error': resultado.stderr
                })

            elif operacion['tipo'] == 'archivo':
                os.makedirs(os.path.dirname(operacion['destino']), exist_ok=True)
                shutil.copy2(operacion['origen'], operacion['destino'])
                resultados.append({'tipo': 'archivo', 'exitoso': True})

            elif operacion['tipo'] == 'contenido':
                os.makedirs(os.path.dirname(operacion['destino']), exist_ok=True)
                with open(operacion['destino'], 'w', encoding=operacion.get('encoding', 'utf-8')) as f:
                    f.write(operacion['contenido'])
                resultados.append({'tipo': 'contenido', 'exitoso': True})

        except Exception as e:
            resultados.append({'tipo': operacion['tipo'], 'exitoso': False, 'error': str(e)})

    return True, resultados, ""

def _ejecutar_operaciones_macos(operaciones, titulo, mensaje, mostrar_mensaje):
    """ Ejecuta operaciones en macOS combinándolas en un solo comando con permisos, así se muestra 1 único popup pidiendo ingresar contraseña
    """
    try:
        #mostrar_mensaje(f"Ejecutando operaciones con permisos administrativos...")

        global _temp_copy_info
        archivos_totales = 0
        if '_temp_copy_info' in globals():
            archivos_totales = _temp_copy_info.get('archivos_totales', 0)

        comandos = []
        archivos_temporales = []

        for i, operacion in enumerate(operaciones):
            if operacion['tipo'] == 'comando':
                comandos.append(operacion['comando'])

            elif operacion['tipo'] == 'archivo':
                # Crea carpeta destino si no existe
                carpeta_destino = os.path.dirname(operacion['destino'])
                comandos.append(f"mkdir -p '{carpeta_destino}'")
                comandos.append(f"cp '{operacion['origen']}' '{operacion['destino']}'")

            elif operacion['tipo'] == 'contenido':
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=f'_op_{i}.tmp',
                                               encoding=operacion.get('encoding', 'utf-8')) as archivo_temp:
                    archivo_temp.write(operacion['contenido'])
                    ruta_temp = archivo_temp.name
                    archivos_temporales.append(ruta_temp)

                # Crea carpeta de destino y mueve archivo
                carpeta_destino = os.path.dirname(operacion['destino'])
                comandos.append(f"mkdir -p '{carpeta_destino}'")
                comandos.append(f"mv '{ruta_temp}' '{operacion['destino']}'")

        if not comandos:
            return True, [], ""

        comando_completo = " && ".join(comandos)

        # Escapa comillas y barras en AppleScript
        comando_escapado = comando_completo.replace('\\', '\\\\').replace('"', '\\"')

        script = f'''
        try
            set dialogMessage to "{mensaje}"
            set resultado to do shell script "{comando_escapado}" with administrator privileges with prompt dialogMessage
            return "SUCCESS:" & resultado
        on error errorMessage number errorNumber
            if errorNumber is -128 then
                return "USER_CANCELLED"
            else
                return "ERROR:" & errorMessage
            end if
        end try
        '''

        # Ejecuta el AppleScript primero (incluye el popup de contraseña)
        resultado = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=300
        )

        # Si el AppleScript fue exitoso Y hay archivos para copiar, muestra el progreso
        if resultado.returncode == 0 and archivos_totales > 0:
            output = resultado.stdout.strip()

            # Verifica que realmente fue exitoso (no cancelado por el usuario)
            if output.startswith("SUCCESS:"):
                mostrar_mensaje(f"{TEXTOS['copiando_idioma']}")
                progreso = BarraProgreso(archivos_totales, modo='copia', tiempo_actualizacion=0.05)

                # Simula progreso rápido ya que los archivos YA se copiaron con el comando admin
                tiempo_estimado = min(max(archivos_totales * 0.05, 0.3), 0.8) # Entre 0.3 y 0.8 segundos
                intervalo = tiempo_estimado / archivos_totales

                for i in range(archivos_totales):
                    time.sleep(intervalo)
                    nombre_archivo = f"archivo_{i+1}.dat"
                    progreso.actualiza(1, nombre_archivo)

                progreso.finaliza()
                # Agrega línea vacía con padding
                print(" " * PADDING_EXT + "│" + " " * (ANCHO_PANTALLA - 2) + "│")

        # Limpia archivos temporales
        for archivo_temp in archivos_temporales:
            try:
                os.unlink(archivo_temp)
            except:
                pass

        # Limpia la información temporal global
        if '_temp_copy_info' in globals():
            try:
                # Solo limpia la carpeta temp si el comando falló (si fue exitoso ya se limpió)
                if resultado.returncode != 0:
                    carpeta_temp = _temp_copy_info.get('carpeta_temp')
                    if carpeta_temp and os.path.exists(carpeta_temp):
                        shutil.rmtree(carpeta_temp)
                del _temp_copy_info
            except:
                pass

        output = resultado.stdout.strip()

        if resultado.returncode != 0:
            return False, [], f"{Fore.LIGHTRED_EX}{TEXTOS['error_en_script']} {resultado.stderr}\n"

        if output.startswith("SUCCESS:"):
            #mostrar_mensaje("Operaciones ejecutadas exitosamente.")
            resultados = [{'tipo': op['tipo'], 'exitoso': True} for op in operaciones]
            return True, resultados, ""

        elif output == "USER_CANCELLED":
            #mostrar_mensaje(f"{Fore.LIGHTYELLOW_EX}{TEXTOS['macos_osascript_cancelado']}\n")
            return False, [], f"{TEXTOS['macos_osascript_cancelado']}"

        else:
            msj_error = output[6:] if output.startswith("ERROR:") else output
            mostrar_mensaje(f"{Fore.LIGHTRED_EX}{TEXTOS['macos_osascript_error_ejecutar']} {msj_error}\n")
            return False, [], msj_error

    except subprocess.TimeoutExpired:
        progreso_activo = False # Detiene el progreso en caso de timeout
        #mostrar_mensaje(f"{Fore.LIGHTRED_EX}{TEXTOS['macos_osascript_timeout2']}\n")
        # Limpia archivos temporales en caso de timeout
        for archivo_temp in archivos_temporales:
            try:
                os.unlink(archivo_temp)
            except:
                pass
        # Limpia carpeta temporal si existe
        if '_temp_copy_info' in globals():
            try:
                carpeta_temp = _temp_copy_info.get('carpeta_temp')
                if carpeta_temp and os.path.exists(carpeta_temp):
                    shutil.rmtree(carpeta_temp)
                del _temp_copy_info
            except:
                pass
        return False, [], f"{TEXTOS['macos_osascript_timeout2']}"

    except Exception as e:
        progreso_activo = False # Detiene el progreso en caso de error
        mostrar_mensaje(f"{Fore.LIGHTRED_EX}Error: {str(e)}\n")
        # Limpia carpeta temporal si existe
        if '_temp_copy_info' in globals():
            try:
                carpeta_temp = _temp_copy_info.get('carpeta_temp')
                if carpeta_temp and os.path.exists(carpeta_temp):
                    shutil.rmtree(carpeta_temp)
                del _temp_copy_info
            except:
                pass
        return False, [], str(e)

def planifica_ops_sis_archivos(operaciones):
    """
    Planifica operaciones del sistema de archivos para luego ejecutarlas

    Args:
        operaciones (list): Lista de operaciones:
            - {'accion': 'crear_carpeta', 'ruta': 'path'}
            - {'accion': 'copiar_archivo', 'origen': 'src', 'destino': 'dst'}
            - {'accion': 'escribir_archivo', 'contenido': 'text', 'destino': 'path', 'encoding': 'utf-8'}
            - {'accion': 'comando', 'comando': 'shell_command'}
    """
    global operaciones_pendientes_admin
    if 'operaciones_pendientes_admin' not in globals():
        operaciones_pendientes_admin = []

    # Determina si requiere permisos administrativos
    for op in operaciones:
        requiere_admin = False

        if op['accion'] in ['crear_carpeta', 'escribir_archivo']:
            ruta_check = op.get('ruta', op.get('destino', ''))
            if requiere_permisos_administrativos(ruta_check):
                requiere_admin = True
        elif op['accion'] == 'copiar_archivo':
            if requiere_permisos_administrativos(op['destino']):
                requiere_admin = True
        elif op['accion'] == 'comando':
            requiere_admin = True

        if requiere_admin:
            # Convierte a formato del sistema de permisos administrativos
            if op['accion'] == 'crear_carpeta':
                sistema = platform.system()
                if sistema == 'Windows':
                    operaciones_pendientes_admin.append({'tipo': 'comando', 'comando': f'mkdir "{op["ruta"]}" 2>nul || echo.'})
                else:
                    operaciones_pendientes_admin.append({'tipo': 'comando', 'comando': f"mkdir -p '{op['ruta']}'"})

            elif op['accion'] == 'copiar_archivo':
                operaciones_pendientes_admin.append({'tipo': 'archivo', 'origen': op['origen'], 'destino': op['destino']})

            elif op['accion'] == 'escribir_archivo':
                operaciones_pendientes_admin.append({
                    'tipo': 'contenido',
                    'contenido': op['contenido'],
                    'destino': op['destino'],
                    'encoding': op.get('encoding', 'utf-8')
                })

            elif op['accion'] == 'comando':
                operaciones_pendientes_admin.append({'tipo': 'comando', 'comando': op['comando']})
        else:
            # Ejecuta directamente si no requiere admin
            try:
                _ejecuta_operacion_directa(op)
            except PermissionError:
                # Si falla por permisos, agrega a operaciones pendientes con admin
                if op['accion'] == 'escribir_archivo':
                    operaciones_pendientes_admin.append({
                        'tipo': 'contenido',
                        'contenido': op['contenido'],
                        'destino': op['destino'],
                        'encoding': op.get('encoding', 'utf-8')
                    })
                elif op['accion'] == 'copiar_archivo':
                    operaciones_pendientes_admin.append({'tipo': 'archivo', 'origen': op['origen'], 'destino': op['destino']})
                elif op['accion'] == 'crear_carpeta':
                    sistema = platform.system()
                    if sistema == 'Darwin':
                        operaciones_pendientes_admin.append({'tipo': 'comando', 'comando': f"mkdir -p '{op['ruta']}'"})

def _ejecuta_operacion_directa(operacion):
    """ Ejecuta una operación individual sin permisos administrativos """
    try:
        if operacion['accion'] == 'crear_carpeta':
            # Verifica permisos antes de intentar crear
            if os.path.exists(operacion['ruta']):
                if not chequea_permisos_escritura(operacion['ruta']):
                    raise PermissionError(f"{TEXTOS['permisos_insuficientes']} {operacion['ruta']}")
            os.makedirs(operacion['ruta'], exist_ok=True)

        elif operacion['accion'] == 'copiar_archivo':
            carpeta_destino = os.path.dirname(operacion['destino'])
            # Verifica permisos en el destino
            if not chequea_permisos_escritura(carpeta_destino if os.path.exists(carpeta_destino) else os.path.dirname(carpeta_destino)):
                raise PermissionError(f"{TEXTOS['permisos_insuficientes']} {operacion['destino']}")
            os.makedirs(carpeta_destino, exist_ok=True)
            shutil.copy2(operacion['origen'], operacion['destino'])

        elif operacion['accion'] == 'escribir_archivo':
            carpeta_destino = os.path.dirname(operacion['destino'])
            # Verifica permisos antes de escribir
            if os.path.exists(operacion['destino']):
                # El archivo existe, chequea si se puede escribir
                if platform.system() == 'Darwin':
                    stat_info = os.stat(operacion['destino'])
                    if stat_info.st_uid == 0 or not os.access(operacion['destino'], os.W_OK):
                        raise PermissionError(f"{TEXTOS['permisos_insuficientes']} {operacion['destino']}")
            else:
                # El archivo no existe, chequea la carpeta padre
                if not chequea_permisos_escritura(carpeta_destino if os.path.exists(carpeta_destino) else os.path.dirname(carpeta_destino)):
                    raise PermissionError(f"{TEXTOS['permisos_insuficientes']} {operacion['destino']}")

            os.makedirs(carpeta_destino, exist_ok=True)
            with open(operacion['destino'], 'w', encoding=operacion.get('encoding', 'utf-8')) as f:
                f.write(operacion['contenido'])

        elif operacion['accion'] == 'comando':
            resultado = subprocess.run(operacion['comando'], shell=True, capture_output=True, text=True)
            if resultado.returncode != 0:
                raise Exception(f"{Fore.LIGHTRED_EX}{TEXTOS['error_ejecutar_comando']} {resultado.stderr}\n")

        return True

    except PermissionError as e:
        # Propaga el error de permisos para que sea manejado correctamente
        raise e

    except Exception as e:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_operacion']} {e}\n")
        return False

def _construye_mapeo_localized(ruta_destino):
    """
    Construye un mapeo de carpetas que tienen 'extensión' .localized en el destino. Usado en algunas carpetas en macOS.

    Args:
        ruta_destino (str): Ruta donde se van a copiar los archivos

    Returns:
        dict: Mapeo de nombre_original -> nombre_con_localized
    """
    mapeo = {}

    try:
        if not os.path.exists(ruta_destino):
            return mapeo

        # Obtiene la lista de carpetas en el destino
        items_destino = os.listdir(ruta_destino)
        carpetas_destino = [item for item in items_destino if os.path.isdir(os.path.join(ruta_destino, item))]

        # Busca carpetas con .localized
        carpetas_localized = [carpeta for carpeta in carpetas_destino if carpeta.endswith('.localized')]

        # Crea mapeo: nombre sin .localized -> nombre con .localized
        for carpeta_loc in carpetas_localized:
            nombre_base = carpeta_loc[:-10] # Quita '.localized' (10 chars)
            # Solo mapea si no existe ya una carpeta con el nombre base
            if nombre_base not in carpetas_destino:
                mapeo[nombre_base] = carpeta_loc

    except Exception as e:
        # Si hay error, devuelve mapeo vacío para usar nombres originales
        pass

    return mapeo

def descomprime_zip(ruta_zip, ruta_unzip, elimina_zip=False):
    """
    Descomprime un archivo ZIP a una ruta específica, sobreescribiendo archivos y carpetas sin preguntar

    Args:
        ruta_zip (str): Ruta donde se encuentra el zip (paquete de idiomas)
        ruta_unzip (str): Ruta donde será copiado y extraido el zip
        elimina_zip (bool): Si es True, elimina el zip luego de la extracción
    """
    try:

        # En Windows, descomprime y muestra progreso directamente
        if platform.system() == 'Windows':
            # Chequea si requiere permisos administrativos
            if requiere_permisos_administrativos(str(ruta_unzip)):
                # Crea carpeta temporal
                carpeta_temp = tempfile.mkdtemp(prefix='simi_zip_')

                try:
                    # Extrae a carpeta temporal
                    with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
                        lista_archivos = zip_ref.namelist()
                        muestra_contenido(f"\n{TEXTOS['copiando_idioma']}")
                        progreso = BarraProgreso(len(lista_archivos), modo='unzip', tiempo_actualizacion=0.05)

                        for info_archivo in zip_ref.infolist():
                            try:
                                zip_ref.extract(info_archivo, carpeta_temp)
                                progreso.actualiza(1, info_archivo.filename)
                            except Exception as e:
                                muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['zip_error_descomprimir']} {info_archivo.filename}: {e}\n")
                                progreso.actualiza(1, info_archivo.filename)

                        progreso.finaliza()

                    # Planifica copia con permisos de admin
                    operaciones = []
                    operaciones.append({'accion': 'crear_carpeta', 'ruta': str(ruta_unzip)})

                    # Copia cada elemento del directorio temporal individualmente
                    for item in os.listdir(carpeta_temp):
                        ruta_origen = os.path.join(carpeta_temp, item)
                        if os.path.isdir(ruta_origen):
                            # Es una carpeta, usa xcopy para copiar recursivamente
                            operaciones.append({'accion': 'comando', 'comando': f'xcopy /E /I /Y "{ruta_origen}" "{os.path.join(ruta_unzip, item)}\\"'})
                        else:
                            # Es un archivo individual
                            operaciones.append({'accion': 'comando', 'comando': f'copy /Y "{ruta_origen}" "{os.path.join(ruta_unzip, item)}"'})

                    if elimina_zip:
                        operaciones.append({'accion': 'comando', 'comando': f'del "{ruta_zip}"'})

                    operaciones.append({'accion': 'comando', 'comando': f'rmdir /S /Q "{carpeta_temp}"'})
                    planifica_ops_sis_archivos(operaciones)

                except Exception as e:
                    try:
                        shutil.rmtree(carpeta_temp)
                    except:
                        pass
                    raise e
            else:
                # Si no requiere permisos copia directamente
                with zipfile.ZipFile(ruta_zip, 'r', metadata_encoding='utf-8') as zip_ref:
                    lista_archivos = zip_ref.namelist()
                    progreso = BarraProgreso(len(lista_archivos), modo='unzip', tiempo_actualizacion=0.05)

                    for info_archivo in zip_ref.infolist():
                        try:
                            zip_ref.extract(info_archivo, ruta_unzip)
                            progreso.actualiza(1, info_archivo.filename)
                        except Exception as e:
                            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['zip_error_descomprimir']} {info_archivo.filename}: {e}\n")
                            progreso.actualiza(1, info_archivo.filename)

                    progreso.finaliza()

                if elimina_zip:
                    os.remove(ruta_zip)

        else: # macOS
            carpeta_temp = tempfile.mkdtemp(prefix='simi_zip_')

            try:
                with zipfile.ZipFile(ruta_zip, 'r', metadata_encoding='utf-8') as zip_ref:
                    zip_ref.extractall(carpeta_temp)

                # Si requiere permisos admin, planifica copia con admin
                if requiere_permisos_administrativos(str(ruta_unzip)):
                    # Cuenta archivos para el progreso
                    archivos_totales = sum(len(files) for _, _, files in os.walk(carpeta_temp))

                    # Guarda info para el progreso
                    global _temp_copy_info
                    _temp_copy_info = {
                        'carpeta_temp': carpeta_temp,
                        'archivos_totales': archivos_totales,
                        'elimina_zip': elimina_zip,
                        'ruta_zip': ruta_zip
                    }

                    # Crea operaciones individuales para cada carpeta/archivo del zip para manejar correctamente las carpetas .localized
                    operaciones = []
                    operaciones.append({'accion': 'crear_carpeta', 'ruta': str(ruta_unzip)})

                    # Crea mapeo de carpetas .localized
                    mapeo_localized = _construye_mapeo_localized(str(ruta_unzip))

                    # Procesa cada elemento en la carpeta temporal
                    for item in os.listdir(carpeta_temp):
                        ruta_origen = os.path.join(carpeta_temp, item)

                        if os.path.isdir(ruta_origen):
                            # Si es carpeta chequea si existe versión .localized en destino
                            nombre_destino = mapeo_localized.get(item, item)
                            ruta_destino = os.path.join(str(ruta_unzip), nombre_destino)

                            # Crea carpeta en destino
                            operaciones.append({'accion': 'crear_carpeta', 'ruta': ruta_destino})

                            # Copia contenido de forma recursiva
                            operaciones.append({
                                'accion': 'comando',
                                'comando': f"cp -R '{ruta_origen}'/* '{ruta_destino}'/ 2>/dev/null || true"
                            })
                        else:
                            # Es un archivo, entonces lo copia directamente
                            ruta_destino = os.path.join(str(ruta_unzip), item)
                            operaciones.append({
                                'accion': 'comando',
                                'comando': f"cp '{ruta_origen}' '{ruta_destino}'"
                            })

                    if elimina_zip:
                        operaciones.append({'accion': 'comando', 'comando': f"rm '{ruta_zip}'"})

                    # Limpia carpeta temporal
                    operaciones.append({'accion': 'comando', 'comando': f"rm -rf '{carpeta_temp}'"})

                    planifica_ops_sis_archivos(operaciones)

                else:
                    # Si no requiere permisos, copia directamente
                    archivos_totales = sum(len(files) for _, _, files in os.walk(carpeta_temp))
                    if archivos_totales > 0:
                        muestra_contenido(f"\n{TEXTOS['copiando_idioma']}")
                        progreso = BarraProgreso(archivos_totales, modo='copia', tiempo_actualizacion=0.05)

                        # Crea mapeo de carpetas .localized
                        mapeo_localized = _construye_mapeo_localized(str(ruta_unzip))

                        def copytree_con_progreso_y_localized(src, dst):

                            def _procesa_carpeta(dir_origen, ruta_relativa=""):
                                """ Procesa carpetas con mapeo .localized """
                                for item in os.listdir(dir_origen):
                                    ruta_origen = os.path.join(dir_origen, item)
                                    clave_mapeo = f"{ruta_relativa}/{item}" if ruta_relativa else item

                                    if os.path.isdir(ruta_origen):
                                        # Si es carpeta usa mapeo .localized
                                        nombre_destino_relativo = mapeo_localized.get(clave_mapeo, clave_mapeo)
                                        ruta_destino = os.path.join(dst, nombre_destino_relativo)

                                        # Crea carpeta destino
                                        os.makedirs(ruta_destino, exist_ok=True)

                                        # Procesa contenido recursivamente
                                        _procesa_carpeta(ruta_origen, nombre_destino_relativo)
                                    else:
                                        # Es un archivo, entonces lo copia
                                        if ruta_relativa:
                                            ruta_destino = os.path.join(dst, ruta_relativa, item)
                                        else:
                                            ruta_destino = os.path.join(dst, item)

                                        os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
                                        shutil.copy2(ruta_origen, ruta_destino)
                                        progreso.actualiza(1, item)

                            _procesa_carpeta(src)

                        copytree_con_progreso_y_localized(carpeta_temp, ruta_unzip)
                        progreso.finaliza()

                        #print(" " * PADDING_EXT + "│" + " " * (ANCHO_PANTALLA - 2) + "│")

                    if elimina_zip:
                        os.remove(ruta_zip)

                    # Limpia carpeta temporal
                    shutil.rmtree(carpeta_temp)

            except Exception as e:
                # Limpia carpeta temporal en caso de error
                try:
                    shutil.rmtree(carpeta_temp)
                except:
                    pass
                raise e

        print(" " * PADDING_EXT + "│" + " " * (ANCHO_PANTALLA - 2) + "│")
        #muestra_contenido(f"{Fore.LIGHTGREEN_EX}Archivos preparados para instalación.\n")
        return True

    except zipfile.BadZipFile:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['zip_no_valido_1']} [{ruta_zip}] {TEXTOS['zip_no_valido_2']}\n")
        return False

    except Exception as e:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['zip_error_unzip']} {e}\n")
        return False

def descargar_archivo(url, auto_unzip=False, ruta_unzip=None, ruta_destino=None, ultima_version=None):
    """
    Descarga un archivo, muestra una barra de progreso y el tamaño del archivo.
    Guarda automáticamente en la carpeta Descargas del usuario y crea subcarpetas según la estructura de la URL.

    Args:
        url (str): URL desde donde se descarga el archivo
        auto_unzip (bool): Si es True descomprime automáticamente los archivos zip luego de descargar (default: False)
        ruta_unzip (str, optional): Ruta donde se descomprimirá el zip. Requerido si se usa auto_unzip=True
        ruta_destino (str, optional): Ruta específica donde guardar el archivo
        ultima_version (float, optional): Número de versión para usar en el mapeo de carpetas

    Returns:
        tuple: (bool, str) - (True/False para éxito, ruta del archivo guardado o None si falló)
    """
    try:
        # Obtiene la ruta de la carpeta Descargas y crea subcarpeta "Simi"
        carpeta_descargas = get_carpeta_descargas()
        carpeta_simi = os.path.join(carpeta_descargas, "Simi")

        if ruta_destino:
            # Usa la ruta de destino proporcionada
            ruta_archivo = ruta_destino
            carpeta_base = os.path.dirname(ruta_archivo)
        else:
            # Parsea la URL para extraer la estructura de la ruta
            parsed_url = urlparse(url)
            ruta_url = parsed_url.path

            # Extrae nombre de archivo de la URL
            filename = ruta_url.split('/')[-1]

            # Obtiene la estructura de carpetas de la URL
            partes_ruta = [part for part in ruta_url.split('/') if part and part != filename]

            # Quita partes específicas de la URL
            partes_a_quitar = [
                'leandroprz',
                'simi',
                'raw',
                'main',
                'releases',
                'download'
            ]
            partes_ruta = [part for part in partes_ruta if part.lower() not in [p.lower() for p in partes_a_quitar]]

            # Mapea carpetas específicas
            mapeo_carpetas = {
                'locales': 'idiomas'
            }

            # Si se proporciona ultima_version, agregar mapeo para esa versión
            if ultima_version:
                mapeo_carpetas[f'v{ultima_version}'] = 'versiones'

            # Aplica el mapeo de nombres de carpetas
            partes_ruta = [mapeo_carpetas.get(part.lower(), part) for part in partes_ruta]

            # Crea la estructura de carpetas
            if partes_ruta:
                # Une todas las partes para crear subcarpetas y se asegura que sean string
                partes_str = [str(part) for part in partes_ruta]
                subcarpeta = os.path.join(*partes_str)
                carpeta_base = os.path.join(carpeta_simi, subcarpeta)
            else:
                # Si no hay una estructura de carpetas, usa la carpeta Simi
                carpeta_base = carpeta_simi

            # Crea la ruta completa
            ruta_archivo = os.path.join(carpeta_base, filename)

        # Chequea si el archivo existe
        if os.path.exists(ruta_archivo):
            muestra_contenido(f"{Fore.LIGHTCYAN_EX}{TEXTOS['archivo_existente']}\n[{ruta_archivo}]")

            # Si es un archivo ZIP y auto_unzip está habilitado, procede con la descompresión
            if auto_unzip and ruta_archivo.lower().endswith('.zip'):
                if ruta_unzip is None:
                    muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['zip_parametro_requerido']}\n")
                    return False, None

                descomp_exitosa = descomprime_zip(ruta_archivo, ruta_unzip, elimina_zip=False)

                if not descomp_exitosa:
                    muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['descarga_no_descomprime']}\n")
                    return False, None

            return True, ruta_archivo

        else:
            # Crea la carpeta Descargas en caso de que no exista
            try:
                os.makedirs(carpeta_base, exist_ok=True)

            except PermissionError:
                muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_permisos_carpeta_descargas']} {carpeta_base}\n")
                return False, None

            # Obtiene info del archivo a descargar
            with requests.get(url, stream=True) as r:
                r.raise_for_status()

                # Obtiene tamaño del archivo
                tamanio_total = int(r.headers.get('content-length', 0))

                # Muestra info de descarga
                muestra_contenido(f"{TEXTOS['descargando']}")

                # Crea barra de progreso de la descarga
                progreso = BarraProgreso(tamanio_total, modo='descarga')

                # Descarga el archivo
                with open(ruta_archivo, 'wb') as f:
                    descargado = 0
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            descargado += len(chunk)
                            progreso.actualiza(len(chunk))

                progreso.finaliza()

                # Agrega línea vacía con padding
                print(" " * PADDING_EXT + "│" + " " * (ANCHO_PANTALLA - 2) + "│")

                # Verifica descarga
                if tamanio_total > 0 and descargado != tamanio_total:
                    muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['descarga_a_medias_1']} {TEXTOS['descarga_a_medias_2']} {descargado} bytes, {TEXTOS['descarga_a_medias_3']} {tamanio_total} bytes.\n")
                    return False, None

                muestra_contenido(f"{Fore.LIGHTGREEN_EX}{TEXTOS['descarga_exitosa']}\n[{ruta_archivo}]")

        # Descomprime zip si es necesario
        if auto_unzip and ruta_archivo.lower().endswith('.zip'):
            if ruta_unzip is None:
                muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['zip_parametro_requerido']}\n")
                return False, None

            descomp_exitosa = descomprime_zip(ruta_archivo, ruta_unzip, elimina_zip=False)

            if not descomp_exitosa:
                muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['descarga_no_descomprime']}\n")
                return False, None

        return True, ruta_archivo

    except requests.exceptions.RequestException as e:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_descarga']}. Error: {e}\n")
        return False, None

    except IOError as e:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_guardar_archivo']}. Error: {e}\n")
        return False, None

    except Exception as e:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_inesperado']} {e}\n")
        return False, None

def edita_idioma_xml(ruta_carpeta, nuevo_idioma):
    """
    Modifica archivos XML donde Adobe configura el idioma de cada programa. Específicamente cambia la locale dentro del tag <installedLanguages> en el archivo application.xml. También hace un backup del archivo antes de modificarlo.

    Args:
        ruta_carpeta (str): Ruta de la carpeta donde se encuentra el archivo xml
        nuevo_idioma (str): Locale a modificarse dentro del tag <installedLanguages>
    """
    global ruta_backup_xml
    try:
        # Obtiene ruta donde está el archivo application.xml
        ruta_archivo_xml = os.path.join(ruta_carpeta)

        # Chequea si el archivo XML existe
        if not os.path.exists(ruta_archivo_xml):
            muestra_contenido(
                f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\n\n"
                f"{Fore.LIGHTYELLOW_EX}{TEXTOS['razones']}\n"
            )
            borde_inferior()
            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        # Detecta encoding del XML
        encoding = detecta_encoding(ruta_archivo_xml)

        # Lee el contenido del XML
        with open(ruta_archivo_xml, 'r', encoding=encoding) as f:
            contenido = f.read()

        # Chequea si el tag de idioma existe
        if not re.search(TAG_IDIOMAS, contenido):
            muestra_contenido(
                f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\n\n"
                f"{Fore.LIGHTYELLOW_EX}{TEXTOS['razones']}\n"
            )
            borde_inferior()
            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        # Prepara el nuevo contenido del tag
        nuevo_tag = f'<Data key="installedLanguages">{nuevo_idioma}</Data>'
        contenido_actualizado = re.sub(TAG_IDIOMAS, nuevo_tag, contenido)

        # Define rutas
        ruta_xml = Path(ruta_archivo_xml)
        ruta_backup_xml = ruta_xml.with_suffix('.bak')

        sistema = platform.system()

        if sistema == 'Darwin':
            # En macOS usa comandos que preservan permisos
            operaciones = [
                {
                    'accion': 'comando',
                    'comando': f"cp -p '{ruta_archivo_xml}' '{ruta_backup_xml}'"
                },
                {
                    'accion': 'escribir_archivo',
                    'contenido': contenido_actualizado,
                    'destino': str(ruta_archivo_xml),
                    'encoding': encoding
                },
                {
                    'accion': 'comando',
                    # Restaura los permisos originales del archivo XML después de escribir
                    'comando': f"chmod --reference='{ruta_backup_xml}' '{ruta_archivo_xml}' 2>/dev/null || chmod $(stat -f '%Mp%Lp' '{ruta_backup_xml}') '{ruta_archivo_xml}'"
                }
            ]
        else:
            # En Windows la copia normal debería preservar permisos
            operaciones = [
                {
                    'accion': 'copiar_archivo',
                    'origen': str(ruta_archivo_xml),
                    'destino': str(ruta_backup_xml)
                },
                {
                    'accion': 'escribir_archivo',
                    'contenido': contenido_actualizado,
                    'destino': str(ruta_archivo_xml),
                    'encoding': encoding
                }
            ]

        planifica_ops_sis_archivos(operaciones)

        #muestra_contenido(f"{Fore.LIGHTGREEN_EX}Configuración de idioma preparada para aplicación.\n")
        return True

    except Exception as e:
        muestra_contenido(f"{TEXTOS['no_cambio']}\nError: {e}\n")
        borde_inferior()
        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return False

def restaura_idioma_xml(ruta_carpeta):
    """
    Restaura el archivo application.xml desde su backup (.bak)
    Elimina el archivo XML actual y renombra el .bak a .xml

    Args:
        ruta_carpeta (str): Ruta de la carpeta donde se encuentra el archivo bak

    Returns:
        tuple: (bool, str) - (éxito, idioma_legible) donde idioma_legible es el nombre del idioma o (False, None) si hay error
    """
    try:
        # Obtiene ruta donde está el archivo application.xml
        ruta_archivo_xml = os.path.join(ruta_carpeta)

        # Define rutas
        ruta_xml = Path(ruta_archivo_xml)
        ruta_backup_xml = ruta_xml.with_suffix('.bak')

        # Chequea si el archivo .bak existe
        if not os.path.exists(ruta_backup_xml):
            muestra_contenido(
                f"{Fore.LIGHTRED_EX}{TEXTOS['no_restauro']}\n\n"
                f"{Fore.LIGHTYELLOW_EX}No se encontró la copia de seguridad (application.bak)\n"
            )
            borde_inferior()
            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False, None

        # Lee el contenido del .bak para extraer el idioma
        idioma_locale = None
        idioma_legible = "desconocido"

        try:
            # Detecta encoding del archivo .bak
            encoding = detecta_encoding(ruta_backup_xml)

            # Lee el contenido del .bak
            with open(ruta_backup_xml, 'r', encoding=encoding) as f:
                contenido_bak = f.read()

            # Busca el tag de idioma
            match = re.search(TAG_IDIOMAS, contenido_bak)

            if match:
                idioma_locale = match.group(1).strip()

                # Mapeo de locales a nombres legibles
                if idioma_locale == 'en_US':
                    idioma_legible = 'inglés'
                elif idioma_locale == 'es_ES':
                    idioma_legible = 'español'
                else:
                    idioma_legible = idioma_locale

        except Exception as e:
            # Si no puede leer el idioma, continúa con la restauración de todas formas
            idioma_legible = "desconocido"

        sistema = platform.system()

        if sistema == 'Darwin':
            # En macOS usa comandos del sistema
            # Primero elimina el XML si existe, luego renombra el BAK
            operaciones = []

            # Solo intenta eliminar si el archivo XML existe
            if os.path.exists(ruta_archivo_xml):
                operaciones.append({
                    'accion': 'comando',
                    'comando': f"rm -f '{ruta_archivo_xml}'"
                })

            # Renombra (mueve) el .bak a .xml
            operaciones.append({
                'accion': 'comando',
                'comando': f"mv '{ruta_backup_xml}' '{ruta_archivo_xml}'"
            })

        else:
            # En Windows usa comandos del sistema también para consistencia
            operaciones = []

            # Solo intenta eliminar si el archivo XML existe
            if os.path.exists(ruta_archivo_xml):
                operaciones.append({
                    'accion': 'comando',
                    'comando': f'del /F /Q "{ruta_archivo_xml}"'
                })

            # Renombra el .bak a .xml
            operaciones.append({
                'accion': 'comando',
                'comando': f'move /Y "{ruta_backup_xml}" "{ruta_archivo_xml}"'
            })

        # Planifica las operaciones para ejecutarlas con permisos administrativos si es necesario
        planifica_ops_sis_archivos(operaciones)

        return True, idioma_legible

    except Exception as e:
        muestra_contenido(f"{TEXTOS['no_restauro']}\nError: {e}\n")
        borde_inferior()
        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return False, None

def version_update():
    """
    Chequea si hay una nueva versión de Simi leyendo el contenido de un txt que tiene solo el número de versión
    """
    titulo_menu_1 = titulo_subrayado(f"{TEXTOS['titulo_version_update_1']}")
    titulo_menu_2 = titulo_subrayado(f"{TEXTOS['titulo_version_update_2']}")

    try:
        # Chequea número de versión en una URL
        respuesta = requests.get(URLS['latest_vcheck'], timeout=5)
        respuesta.raise_for_status()
        ultima_version = float(respuesta.text.strip())

        if ultima_version > float(VERSION_ACTUAL_SIMI):
            limpia_pantalla()

            borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
            muestra_contenido(
                f"\n{TEXTOS['simi_descripcion']}\n\n"
                f"\n{titulo_menu_1}\n\n"
                f"{Fore.LIGHTGREEN_EX}{TEXTOS['nueva_v_disponible']} v{ultima_version}\n"
            )
            borde_inferior()

            seleccion = muestra_input_usuario(f"{TEXTOS['desea_descargar']}").upper().strip() or 'S'

            if seleccion == 'S':
                # Define ruta de descarga del archivo
                ruta_descarga = get_carpeta_descargas()

                # Crea nombre de la versión según la plataforma
                if platform.system() == 'Windows':
                    extension = '.exe'
                    texto_os = '_win'
                    url_release_os = f"{URLS['url_releases']}/v{ultima_version}/{NOMBRE_RELEASE}{ultima_version}{texto_os}{extension}"
                else:
                    extension = '.dmg'
                    texto_os = '_mac'
                    url_release_os = f"{URLS['url_releases']}/v{ultima_version}/{NOMBRE_RELEASE}{ultima_version}{texto_os}{extension}"

                nombre_archivo_descargado = f"{NOMBRE_RELEASE}{ultima_version}{texto_os}{extension}"

                # Define la carpeta donde se guardará la nueva versión
                ruta_archivo_descargado = os.path.join(ruta_descarga, "Simi", "versiones", nombre_archivo_descargado)

                limpia_pantalla()

                borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
                muestra_contenido(
                    f"\n{TEXTOS['simi_descripcion']}\n\n"
                    f"\n{titulo_menu_2}\n"
                )

                # Descarga la nueva versión con ruta específica
                descarga_exitosa, ruta_real_archivo = descargar_archivo(url_release_os, ruta_destino=ruta_archivo_descargado, ultima_version=ultima_version)

                if not descarga_exitosa:
                    muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_descargo']}\n")
                    borde_inferior()
                    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
                    return

                muestra_contenido("")
                borde_inferior()

                seleccion_abrir = muestra_input_usuario(f"{TEXTOS['desea_abrir']}").upper().strip() or 'S'

                # Abre la nueva versión según el sistema operativo
                if seleccion_abrir == 'S':
                    if platform.system() == 'Windows':
                        os.startfile(ruta_real_archivo) # type: ignore
                    else: # macOS
                        subprocess.run(['open', ruta_real_archivo], check=True)
                    os._exit(0)

        elif ultima_version == float(VERSION_ACTUAL_SIMI):

            limpia_pantalla()

            borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
            muestra_contenido(
                f"\n{TEXTOS['simi_descripcion']}\n\n"
                f"\n{titulo_menu_1}\n\n"
                f"{Fore.LIGHTCYAN_EX}{TEXTOS['usando_ultima_version']} v{VERSION_ACTUAL_SIMI}\n"
            )
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return

        else:
            limpia_pantalla()

            borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
            muestra_contenido(
                f"\n{TEXTOS['simi_descripcion']}\n\n"
                f"\n{titulo_menu_1}\n\n"
                f"{Fore.LIGHTCYAN_EX}{TEXTOS['version_actual_1']} ({VERSION_ACTUAL_SIMI}) {TEXTOS['version_actual_2']} v{ultima_version}\n"
            )
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return

    except requests.RequestException as e:
        limpia_pantalla()

        borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
        muestra_contenido(
            f"\n{TEXTOS['simi_descripcion']}\n\n"
            f"\n{titulo_menu_1}\n\n"
            f"{Fore.LIGHTRED_EX}{TEXTOS['no_pudo_chequear_version']}\nError: {e}.\n"
        )
        borde_inferior()

        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return

    except Exception as e:
        limpia_pantalla()

        borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
        muestra_contenido(
            f"\n{TEXTOS['simi_descripcion']}\n\n"
            f"\n{titulo_menu_1}\n\n"
            f"{Fore.LIGHTRED_EX}{TEXTOS['no_descargo']} Error:\n{e}\n"
        )
        borde_inferior()

        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return

    menu_principal()
    return

def abre_url_ayuda():
    """
    Muestra un mensaje y abre una URL usando el navegador default del sistema operativo
    """
    limpia_pantalla()

    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{TEXTOS['agradecimiento']}\n"
        f"{Fore.LIGHTGREEN_EX}{TEXTOS['mensaje_url_ayuda']}\n"
    )
    borde_inferior()

    time.sleep(3) # Espera antes de continuar
    webbrowser.open(URLS['url_ayuda_tienda'])

    menu_principal()
    return

def abre_url_reportar_error():
    """
    Muestra un mensaje y abre una URL usando el navegador default del sistema operativo
    """
    limpia_pantalla()

    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{TEXTOS['agradecimiento']}\n"
        f"{Fore.LIGHTGREEN_EX}{TEXTOS['mensaje_reportar_error']}\n"
    )
    borde_inferior()

    time.sleep(3)
    webbrowser.open(URLS['url_reportar_error'])

    menu_principal()
    return

def cierra_programa():
    """
    Muestra un mensaje y cierra el script
    """
    limpia_pantalla()

    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{TEXTOS['agradecimiento']}\n"
        f"{Fore.LIGHTCYAN_EX}{TEXTOS['mensaje_resenia']}\n"
    )
    borde_inferior()

    time.sleep(3)
    sys.exit(0)

def cambio_idioma_after_effects(locale_xml):
    """
    Cambia el idioma de After Effects modificando el archivo application.xml; usando la versión, ruta y locale ingresada por el usuario

    Args:
        locale_xml (str): String que puede ser en_US o es_ES
    """
    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "After Effects"
    titulo_menu = titulo_subrayado(f"{TEXTOS['cambiar_idioma']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['al']} {idioma_menu_ui}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='after_effects', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del XML según el sistema operativo
    RUTA_XML = {
        'Windows': Path(ruta_instal_programa) / 'Support Files' / 'AMT' / 'application.xml',
        'Darwin': Path(ruta_instal_programa) / 'AMT' / 'application.xml'
    }

    ruta_instal_programa = RUTA_XML.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo XML existe
    if not ruta_instal_programa or not ruta_instal_programa.exists():
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

    # Planifica edición del XML
    xml_exitoso = edita_idioma_xml(ruta_instal_programa, locale_xml)
    if not xml_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Cambiar idioma de {NOMBRE_PROGRAMA} al {idioma_menu_ui}",
            mensaje=f"Se requieren permisos de administrador para cambiar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def cambio_idioma_premiere_pro(locale_xml):
    """
    Cambia el idioma de Premiere Pro modificando el archivo application.xml; usando la versión, ruta y locale ingresada por el usuario

    Args:
        locale_xml (str): String que puede ser en_US o es_ES
    """
    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "Premiere Pro"
    titulo_menu = titulo_subrayado(f"{TEXTOS['cambiar_idioma']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['al']} {idioma_menu_ui}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='premiere_pro', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del XML según el sistema operativo
    RUTA_XML = {
        'Windows': Path(ruta_instal_programa) / 'AMT' / 'application.xml',
        'Darwin': Path(ruta_instal_programa) / 'AMT' / 'application.xml'
    }

    ruta_instal_programa = RUTA_XML.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo XML existe
    if not ruta_instal_programa or not ruta_instal_programa.exists():
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

    # Planifica edición del XML
    xml_exitoso = edita_idioma_xml(ruta_instal_programa, locale_xml)
    if not xml_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Cambiar idioma de {NOMBRE_PROGRAMA} al {idioma_menu_ui}",
            mensaje=f"Se requieren permisos de administrador para cambiar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def cambio_idioma_audition(locale_xml):
    """
    Cambia el idioma de Audition modificando el archivo application.xml; usando la versión, ruta y locale ingresada por el usuario

    Args:
        locale_xml (str): String que puede ser en_US o es_ES
    """
    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "Audition"
    titulo_menu = titulo_subrayado(f"{TEXTOS['cambiar_idioma']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['al']} {idioma_menu_ui}")

    limpia_pantalla()

    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='audition', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del XML según el sistema operativo
    RUTA_XML = {
        'Windows': Path(ruta_instal_programa) / 'AMT' / 'application.xml',
        'Darwin': Path(ruta_instal_programa) / 'AMT' / 'application.xml'
    }

    ruta_instal_programa = RUTA_XML.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo XML existe
    if not ruta_instal_programa or not ruta_instal_programa.exists():
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

    # Planifica edición del XML
    xml_exitoso = edita_idioma_xml(ruta_instal_programa, locale_xml)
    if not xml_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Cambiar idioma de {NOMBRE_PROGRAMA} al {idioma_menu_ui}",
            mensaje=f"Se requieren permisos de administrador para cambiar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def cambio_idioma_indesign(locale_xml):
    """
    Cambia el idioma de InDesign modificando el archivo application.xml; usando la versión, ruta y locale ingresada por el usuario. También descarga y copia un paquete de idioma en la ruta especificada

    Args:
        locale_xml (str): String que puede ser en_US o es_ES
    """
    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "InDesign"
    titulo_menu = titulo_subrayado(f"{TEXTOS['cambiar_idioma']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['al']} {idioma_menu_ui}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='indesign', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del XML según el sistema operativo
    RUTA_XML = {
        'Windows': Path(ruta_instal_programa) / 'AMT' / 'application.xml',
        'Darwin': Path(ruta_instal_programa) / 'Resources' / 'AMT' / 'ID' / 'AMT' / 'application.xml'
    }

    # Ruta para el zip con el idioma según el sistema operativo
    RUTA_DESCOMP_ZIP = {
        'Windows': Path(ruta_instal_programa),
        'Darwin': Path(ruta_instal_programa)
    }

    # URL de descarga del idioma según el sistema operativo
    URL_LOCALE = {
        'Windows': f"{URLS['url_locales_win']}/ind/{version_adobe}/{locale_xml}.zip",
        'Darwin': f"{URLS['url_locales_mac']}/ind/{version_adobe}/{locale_xml}.zip"
    }

    ruta_instal_programa = RUTA_XML.get(platform.system())
    ruta_extraccion_programa = RUTA_DESCOMP_ZIP.get(platform.system())
    url_locale_programa = URL_LOCALE.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo XML existe
    if not ruta_instal_programa or not ruta_instal_programa.exists():
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

    # Descarga y planifica descompresión del zip
    descarga_exitosa = descargar_archivo(url_locale_programa, auto_unzip=True, ruta_unzip=ruta_extraccion_programa)
    if not descarga_exitosa:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_descarga_idioma']}\n")
        borde_inferior()
        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return False

    # Planifica edición del XML
    xml_exitoso = edita_idioma_xml(ruta_instal_programa, locale_xml)
    if not xml_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Cambiar idioma de {NOMBRE_PROGRAMA} al {idioma_menu_ui}",
            mensaje=f"Se requieren permisos de administrador para cambiar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def cambio_idioma_media_encoder(locale_xml):
    """
    Cambia el idioma de Media Encoder modificando el archivo application.xml; usando la versión, ruta y locale ingresada por el usuario

    Args:
        locale_xml (str): String que puede ser en_US o es_ES
    """
    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "Media Encoder"
    titulo_menu = titulo_subrayado(f"{TEXTOS['cambiar_idioma']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['al']} {idioma_menu_ui}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='media_encoder', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del XML según el sistema operativo
    RUTA_XML = {
        'Windows': Path(ruta_instal_programa) / 'AMT' / 'application.xml',
        'Darwin': Path(ruta_instal_programa) / 'AMT' / 'application.xml'
    }

    ruta_instal_programa = RUTA_XML.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo XML existe
    if not ruta_instal_programa or not ruta_instal_programa.exists():
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

    # Planifica edición del XML
    xml_exitoso = edita_idioma_xml(ruta_instal_programa, locale_xml)
    if not xml_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Cambiar idioma de {NOMBRE_PROGRAMA} al {idioma_menu_ui}",
            mensaje=f"Se requieren permisos de administrador para cambiar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def cambio_idioma_photoshop(locale_xml):
    """
    Cambia el idioma de Photoshop usando la versión, ruta y locale ingresada por el usuario. También descarga y copia un paquete de idioma en la ruta especificada

    Args:
        locale_xml (str): String que puede ser en_US o es_ES
    """
    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "Photoshop"
    titulo_menu = titulo_subrayado(f"{TEXTOS['cambiar_idioma']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['al']} {idioma_menu_ui}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='photoshop', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta para el zip con el idioma según el sistema operativo
    RUTA_DESCOMP_ZIP = {
        'Windows': Path(ruta_instal_programa),
        'Darwin': Path(ruta_instal_programa)
    }

    # URL de descarga del idioma según el sistema operativo
    URL_LOCALE = {
        'Windows': f"{URLS['url_locales_win']}/ps/{version_adobe}/{locale_xml}.zip",
        'Darwin': f"{URLS['url_locales_mac']}/ps/{version_adobe}/{locale_xml}.zip"
    }

    ruta_extraccion_programa = RUTA_DESCOMP_ZIP.get(platform.system())
    url_locale_programa = URL_LOCALE.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo XML existe
    if not ruta_instal_programa or not ruta_instal_programa.exists():
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

    # Descarga y planifica descompresión del zip
    descarga_exitosa = descargar_archivo(url_locale_programa, auto_unzip=True, ruta_unzip=ruta_extraccion_programa)
    if not descarga_exitosa:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_descarga_idioma']}\n")
        borde_inferior()
        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Cambiar idioma de {NOMBRE_PROGRAMA} al {idioma_menu_ui}",
            mensaje=f"Se requieren permisos de administrador para cambiar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTCYAN_EX}{TEXTOS['cambio_ps']}\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTCYAN_EX}{TEXTOS['cambio_ps']}\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def cambio_idioma_animate(locale_xml):
    """
    Cambia el idioma de Animate modificando el archivo application.xml; usando la versión, ruta y locale ingresada por el usuario. También descarga y copia un paquete de idioma en la ruta especificada

    Args:
        locale_xml (str): String que puede ser en_US o es_ES
    """
    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "Animate"
    titulo_menu = titulo_subrayado(f"{TEXTOS['cambiar_idioma']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['al']} {idioma_menu_ui}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='animate', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del XML según el sistema operativo
    RUTA_XML = {
        'Windows': Path(ruta_instal_programa) / 'AMT' / 'application.xml',
        'Darwin': Path(ruta_instal_programa) / 'App' / 'Contents' / 'Resources' / 'AMT' / 'application.xml'
    }

    # Ruta para el zip con el idioma según el sistema operativo
    RUTA_DESCOMP_ZIP = {
        'Windows': Path(ruta_instal_programa),
        'Darwin': Path(ruta_instal_programa)
    }

    # URL de descarga del idioma según el sistema operativo
    URL_LOCALE = {
        'Windows': f"{URLS['url_locales_win']}/ani/{version_adobe}/{locale_xml}.zip",
        'Darwin': f"{URLS['url_locales_mac']}/ani/{version_adobe}/{locale_xml}.zip"
    }

    ruta_instal_programa = RUTA_XML.get(platform.system())
    ruta_extraccion_programa = RUTA_DESCOMP_ZIP.get(platform.system())
    url_locale_programa = URL_LOCALE.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo XML existe
    if not ruta_instal_programa or not ruta_instal_programa.exists():
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

    # Descarga y planifica descompresión del zip
    descarga_exitosa = descargar_archivo(url_locale_programa, auto_unzip=True, ruta_unzip=ruta_extraccion_programa)
    if not descarga_exitosa:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_descarga_idioma']}\n")
        borde_inferior()
        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return False

    # Planifica edición del XML
    xml_exitoso = edita_idioma_xml(ruta_instal_programa, locale_xml)
    if not xml_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Cambiar idioma de {NOMBRE_PROGRAMA} al {idioma_menu_ui}",
            mensaje=f"Se requieren permisos de administrador para cambiar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def cambio_idioma_illustrator(locale_xml):
    """
    Cambia el idioma de Illustrator modificando el archivo application.xml; usando la versión, ruta y locale ingresada por el usuario. También descarga y copia un paquete de idioma en la ruta especificada

    Args:
        locale_xml (str): String que puede ser en_US o es_ES
    """
    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "Illustrator"
    titulo_menu = titulo_subrayado(f"{TEXTOS['cambiar_idioma']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['al']} {idioma_menu_ui}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='illustrator', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del XML según el sistema operativo
    RUTA_XML = {
        'Windows': Path(ruta_instal_programa) / 'Support Files' / 'Contents' / 'Windows' / 'AMT' / 'application.xml',
        'Darwin': Path(ruta_instal_programa) / 'Support Files' / 'AMT' / 'AI' / 'AMT' / 'application.xml'
    }

    # Ruta para el zip con el idioma según el sistema operativo
    RUTA_DESCOMP_ZIP = {
        'Windows': Path(ruta_instal_programa),
        'Darwin': Path(ruta_instal_programa)
    }

    # URL de descarga del idioma según el sistema operativo
    URL_LOCALE = {
        'Windows': f"{URLS['url_locales_win']}/il/{version_adobe}/{locale_xml}.zip",
        'Darwin': f"{URLS['url_locales_mac']}/il/{version_adobe}/{locale_xml}.zip"
    }

    ruta_instal_programa = RUTA_XML.get(platform.system())
    ruta_extraccion_programa = RUTA_DESCOMP_ZIP.get(platform.system())
    url_locale_programa = URL_LOCALE.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo XML existe
    if not ruta_instal_programa or not ruta_instal_programa.exists():
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

    # Descarga y planifica descompresión del zip
    descarga_exitosa = descargar_archivo(url_locale_programa, auto_unzip=True, ruta_unzip=ruta_extraccion_programa)
    if not descarga_exitosa:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_descarga_idioma']}\n")
        borde_inferior()
        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return False

    # Planifica edición del XML
    xml_exitoso = edita_idioma_xml(ruta_instal_programa, locale_xml)
    if not xml_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Cambiar idioma de {NOMBRE_PROGRAMA} al {idioma_menu_ui}",
            mensaje=f"Se requieren permisos de administrador para cambiar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def cambio_idioma_incopy(locale_xml):
    """
    Cambia el idioma de InCopy modificando el archivo application.xml; usando la versión, ruta y locale ingresada por el usuario. También descarga y copia un paquete de idioma en la ruta especificada

    Args:
        locale_xml (str): String que puede ser en_US o es_ES
    """
    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "InCopy"
    titulo_menu = titulo_subrayado(f"{TEXTOS['cambiar_idioma']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['al']} {idioma_menu_ui}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='incopy', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del XML según el sistema operativo
    RUTA_XML = {
        'Windows': Path(ruta_instal_programa) / 'AMT' / 'application.xml',
        'Darwin': Path(ruta_instal_programa) / 'Resources' / 'AMT' / 'IC' / 'AMT' / 'application.xml'
    }

    # Ruta para el zip con el idioma según el sistema operativo
    RUTA_DESCOMP_ZIP = {
        'Windows': Path(ruta_instal_programa),
        'Darwin': Path(ruta_instal_programa)
    }

    # URL de descarga del idioma según el sistema operativo
    URL_LOCALE = {
        'Windows': f"{URLS['url_locales_win']}/inc/{version_adobe}/{locale_xml}.zip",
        'Darwin': f"{URLS['url_locales_mac']}/inc/{version_adobe}/{locale_xml}.zip"
    }

    ruta_instal_programa = RUTA_XML.get(platform.system())
    ruta_extraccion_programa = RUTA_DESCOMP_ZIP.get(platform.system())
    url_locale_programa = URL_LOCALE.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo XML existe
    if not ruta_instal_programa or not ruta_instal_programa.exists():
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

    # Descarga y planifica descompresión del zip
    descarga_exitosa = descargar_archivo(url_locale_programa, auto_unzip=True, ruta_unzip=ruta_extraccion_programa)
    if not descarga_exitosa:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_descarga_idioma']}\n")
        borde_inferior()
        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return False

    # Planifica edición del XML
    xml_exitoso = edita_idioma_xml(ruta_instal_programa, locale_xml)
    if not xml_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Cambiar idioma de {NOMBRE_PROGRAMA} al {idioma_menu_ui}",
            mensaje=f"Se requieren permisos de administrador para cambiar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def cambio_idioma_character_animator(locale_xml):
    """
    Cambia el idioma de Character Animator modificando el archivo application.xml; usando la versión, ruta y locale ingresada por el usuario

    Args:
        locale_xml (str): String que puede ser en_US o es_ES
    """
    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "Character Animator"
    titulo_menu = titulo_subrayado(f"{TEXTOS['cambiar_idioma']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['al']} {idioma_menu_ui}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='character_animator', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del XML según el sistema operativo
    RUTA_XML = {
        'Windows': Path(ruta_instal_programa) / 'Support Files' / 'AMT' / 'application.xml',
        'Darwin': Path(ruta_instal_programa) / 'AMT' / 'application.xml'
    }

    ruta_instal_programa = RUTA_XML.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo XML existe
    if not ruta_instal_programa or not ruta_instal_programa.exists():
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

    # Planifica edición del XML
    xml_exitoso = edita_idioma_xml(ruta_instal_programa, locale_xml)
    if not xml_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Cambiar idioma de {NOMBRE_PROGRAMA} al {idioma_menu_ui}",
            mensaje=f"Se requieren permisos de administrador para cambiar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['idioma_cambio_exitoso_1']} {idioma_menu_ui} {TEXTOS['idioma_cambio_exitoso_2']} [{ruta_instal_print}]\n\n"
            f"{Fore.LIGHTYELLOW_EX}{TEXTOS['idioma_backup_1']} [{ruta_backup_xml}]. {TEXTOS['idioma_backup_2']}\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def restaurar_xml_after_effects(version_adobe):
    """
    Restaura el idioma de After Effects usando el archivo application.bak, la versión y ruta ingresada por el usuario

    Args:
	    version_adobe (int): Int que puede ser 2018-2025+
    """

    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "After Effects"
    titulo_menu = titulo_subrayado(f"{TEXTOS['menu_restaurar_xml']} {TEXTOS['de']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['menu_usando_bak']}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa_bak = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='after_effects', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del BAK según el sistema operativo
    RUTA_BAK = {
        'Windows': Path(ruta_instal_programa_bak) / 'Support Files' / 'AMT' / 'application.bak',
        'Darwin': Path(ruta_instal_programa_bak) / 'AMT' / 'application.bak'
    }

    ruta_instal_programa_bak = RUTA_BAK.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo BAK existe
    if not ruta_instal_programa_bak or not ruta_instal_programa_bak.exists():
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

    # Planifica restaurar el BAK a XML
    ruta_xml = ruta_instal_programa_bak.with_suffix('.xml')
    bak_exitoso, idioma_restaurado = restaura_idioma_xml(ruta_xml)
    if not bak_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Restaurar idioma de {NOMBRE_PROGRAMA} {version_adobe}",
            mensaje=f"Se requieren permisos de administrador para restaurar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def restaurar_xml_premiere_pro(version_adobe):
    """
    Restaura el idioma de Premiere Pro usando el archivo application.bak, la versión y ruta ingresada por el usuario

    Args:
	    version_adobe (int): Int que puede ser 2018-2025+
    """

    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "Premiere Pro"
    titulo_menu = titulo_subrayado(f"{TEXTOS['menu_restaurar_xml']} {TEXTOS['de']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['menu_usando_bak']}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa_bak = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='premiere_pro', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del BAK según el sistema operativo
    RUTA_BAK = {
        'Windows': Path(ruta_instal_programa_bak) / 'AMT' / 'application.bak',
        'Darwin': Path(ruta_instal_programa_bak) / 'AMT' / 'application.bak'
    }

    ruta_instal_programa_bak = RUTA_BAK.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo BAK existe
    if not ruta_instal_programa_bak or not ruta_instal_programa_bak.exists():
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

    # Planifica restaurar el BAK a XML
    ruta_xml = ruta_instal_programa_bak.with_suffix('.xml')
    bak_exitoso, idioma_restaurado = restaura_idioma_xml(ruta_xml)
    if not bak_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Restaurar idioma de {NOMBRE_PROGRAMA} {version_adobe}",
            mensaje=f"Se requieren permisos de administrador para restaurar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def restaurar_xml_audition(version_adobe):
    """
    Restaura el idioma de Audition usando el archivo application.bak, la versión y ruta ingresada por el usuario

    Args:
	    version_adobe (int): Int que puede ser 2018-2025+
    """

    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "Audition"
    titulo_menu = titulo_subrayado(f"{TEXTOS['menu_restaurar_xml']} {TEXTOS['de']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['menu_usando_bak']}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa_bak = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='audition', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del BAK según el sistema operativo
    RUTA_BAK = {
        'Windows': Path(ruta_instal_programa_bak) / 'AMT' / 'application.bak',
        'Darwin': Path(ruta_instal_programa_bak) / 'AMT' / 'application.bak'
    }

    ruta_instal_programa_bak = RUTA_BAK.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo BAK existe
    if not ruta_instal_programa_bak or not ruta_instal_programa_bak.exists():
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

    # Planifica restaurar el BAK a XML
    ruta_xml = ruta_instal_programa_bak.with_suffix('.xml')
    bak_exitoso, idioma_restaurado = restaura_idioma_xml(ruta_xml)
    if not bak_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Restaurar idioma de {NOMBRE_PROGRAMA} {version_adobe}",
            mensaje=f"Se requieren permisos de administrador para restaurar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def restaurar_xml_indesign(version_adobe):
    """
    Restaura el idioma de InDesign usando el archivo application.bak, la versión y ruta ingresada por el usuario

    Args:
	    version_adobe (int): Int que puede ser 2018-2025+
    """

    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "InDesign"
    titulo_menu = titulo_subrayado(f"{TEXTOS['menu_restaurar_xml']} {TEXTOS['de']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['menu_usando_bak']}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa_bak = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='indesign', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del BAK según el sistema operativo
    RUTA_BAK = {
        'Windows': Path(ruta_instal_programa_bak) / 'AMT' / 'application.bak',
        'Darwin': Path(ruta_instal_programa_bak) / 'Resources' / 'AMT' / 'ID' / 'AMT' / 'application.bak'
    }

    ruta_instal_programa_bak = RUTA_BAK.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo BAK existe
    if not ruta_instal_programa_bak or not ruta_instal_programa_bak.exists():
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

    # Planifica restaurar el BAK a XML
    ruta_xml = ruta_instal_programa_bak.with_suffix('.xml')
    bak_exitoso, idioma_restaurado = restaura_idioma_xml(ruta_xml)
    if not bak_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Restaurar idioma de {NOMBRE_PROGRAMA} {version_adobe}",
            mensaje=f"Se requieren permisos de administrador para restaurar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def restaurar_xml_media_encoder(version_adobe):
    """
    Restaura el idioma de Media Encoder usando el archivo application.bak, la versión y ruta ingresada por el usuario

    Args:
	    version_adobe (int): Int que puede ser 2018-2025+
    """

    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "Media Encoder"
    titulo_menu = titulo_subrayado(f"{TEXTOS['menu_restaurar_xml']} {TEXTOS['de']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['menu_usando_bak']}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa_bak = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='media_encoder', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del BAK según el sistema operativo
    RUTA_BAK = {
        'Windows': Path(ruta_instal_programa_bak) / 'AMT' / 'application.bak',
        'Darwin': Path(ruta_instal_programa_bak) / 'AMT' / 'application.bak'
    }

    ruta_instal_programa_bak = RUTA_BAK.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo BAK existe
    if not ruta_instal_programa_bak or not ruta_instal_programa_bak.exists():
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

    # Planifica restaurar el BAK a XML
    ruta_xml = ruta_instal_programa_bak.with_suffix('.xml')
    bak_exitoso, idioma_restaurado = restaura_idioma_xml(ruta_xml)
    if not bak_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Restaurar idioma de {NOMBRE_PROGRAMA} {version_adobe}",
            mensaje=f"Se requieren permisos de administrador para restaurar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def restaurar_xml_photoshop(version_adobe):
    """
    Muestra un mensaje indicándole al usuario cómo debe cambiar el idioma de Photoshop desde la interfaz del programa
    """
    NOMBRE_PROGRAMA = "Photoshop"

    titulo_menu = titulo_subrayado(f"{TEXTOS['menu_restaurar_xml']} {TEXTOS['de']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['menu_usando_bak']}")

    while True:
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

def restaurar_xml_animate(version_adobe):
    """
    Restaura el idioma de Animate usando el archivo application.bak, la versión y ruta ingresada por el usuario

    Args:
	    version_adobe (int): Int que puede ser 2018-2025+
    """

    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "Animate"
    titulo_menu = titulo_subrayado(f"{TEXTOS['menu_restaurar_xml']} {TEXTOS['de']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['menu_usando_bak']}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa_bak = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='animate', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del BAK según el sistema operativo
    RUTA_BAK = {
        'Windows': Path(ruta_instal_programa_bak) / 'AMT' / 'application.bak',
        'Darwin': Path(ruta_instal_programa_bak) / 'App' / 'Contents' / 'Resources' / 'AMT' / 'application.bak'
    }

    ruta_instal_programa_bak = RUTA_BAK.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo BAK existe
    if not ruta_instal_programa_bak or not ruta_instal_programa_bak.exists():
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

    # Planifica restaurar el BAK a XML
    ruta_xml = ruta_instal_programa_bak.with_suffix('.xml')
    bak_exitoso, idioma_restaurado = restaura_idioma_xml(ruta_xml)
    if not bak_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Restaurar idioma de {NOMBRE_PROGRAMA} {version_adobe}",
            mensaje=f"Se requieren permisos de administrador para restaurar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def restaurar_xml_illustrator(version_adobe):
    """
    Restaura el idioma de Illustrator usando el archivo application.bak, la versión y ruta ingresada por el usuario

    Args:
	    version_adobe (int): Int que puede ser 2018-2025+
    """

    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "Illustrator"
    titulo_menu = titulo_subrayado(f"{TEXTOS['menu_restaurar_xml']} {TEXTOS['de']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['menu_usando_bak']}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa_bak = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='illustrator', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del BAK según el sistema operativo
    RUTA_BAK = {
        'Windows': Path(ruta_instal_programa_bak) / 'Support Files' / 'Contents' / 'Windows' / 'AMT' / 'application.bak',
        'Darwin': Path(ruta_instal_programa_bak) / 'Support Files' / 'AMT' / 'AI' / 'AMT' / 'application.bak'
    }

    ruta_instal_programa_bak = RUTA_BAK.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo BAK existe
    if not ruta_instal_programa_bak or not ruta_instal_programa_bak.exists():
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

    # Planifica restaurar el BAK a XML
    ruta_xml = ruta_instal_programa_bak.with_suffix('.xml')
    bak_exitoso, idioma_restaurado = restaura_idioma_xml(ruta_xml)
    if not bak_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Restaurar idioma de {NOMBRE_PROGRAMA} {version_adobe}",
            mensaje=f"Se requieren permisos de administrador para restaurar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def restaurar_xml_incopy(version_adobe):
    """
    Restaura el idioma de InCopy usando el archivo application.bak, la versión y ruta ingresada por el usuario

    Args:
	    version_adobe (int): Int que puede ser 2018-2025+
    """

    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "InCopy"
    titulo_menu = titulo_subrayado(f"{TEXTOS['menu_restaurar_xml']} {TEXTOS['de']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['menu_usando_bak']}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa_bak = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='incopy', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del BAK según el sistema operativo
    RUTA_BAK = {
        'Windows': Path(ruta_instal_programa_bak) / 'AMT' / 'application.bak',
        'Darwin': Path(ruta_instal_programa_bak) / 'Resources' / 'AMT' / 'IC' / 'AMT' / 'application.bak'
    }

    ruta_instal_programa_bak = RUTA_BAK.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo BAK existe
    if not ruta_instal_programa_bak or not ruta_instal_programa_bak.exists():
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

    # Planifica restaurar el BAK a XML
    ruta_xml = ruta_instal_programa_bak.with_suffix('.xml')
    bak_exitoso, idioma_restaurado = restaura_idioma_xml(ruta_xml)
    if not bak_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Restaurar idioma de {NOMBRE_PROGRAMA} {version_adobe}",
            mensaje=f"Se requieren permisos de administrador para restaurar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def restaurar_xml_character_animator(version_adobe):
    """
    Restaura el idioma de Character Animator usando el archivo application.bak, la versión y ruta ingresada por el usuario

    Args:
	    version_adobe (int): Int que puede ser 2018-2025+
    """

    global ruta_instal_print, operaciones_pendientes_admin
    operaciones_pendientes_admin = [] # Inicializa la lista

    NOMBRE_PROGRAMA = "Character Animator"
    titulo_menu = titulo_subrayado(f"{TEXTOS['menu_restaurar_xml']} {TEXTOS['de']} {NOMBRE_PROGRAMA} {version_adobe} {TEXTOS['menu_usando_bak']}")

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}"
    )

    # Pide ruta al usuario
    ruta_instal_programa_bak = ruta_instal_print = ruta_instalacion_programa(
        ruta_subcarpeta=f"Adobe {NOMBRE_PROGRAMA} {version_adobe}", # Ruta Windows
        nombre_programa='character_animator', # Ruta macOS
        version_adobe=version_adobe # Versión macOS
    )

    # Ruta del BAK según el sistema operativo
    RUTA_BAK = {
        'Windows': Path(ruta_instal_programa_bak) / 'Support Files' / 'AMT' / 'application.bak',
        'Darwin': Path(ruta_instal_programa_bak) / 'AMT' / 'application.bak'
    }

    ruta_instal_programa_bak = RUTA_BAK.get(platform.system())

    limpia_pantalla()
    borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
    muestra_contenido(
        f"\n{TEXTOS['simi_descripcion']}\n\n"
        f"\n{titulo_menu}\n"
    )

    # Cierra el programa
    chequea_cierra_app(f"Adobe {NOMBRE_PROGRAMA} {version_adobe}")
    borde_inferior()

    # Chequea si el archivo BAK existe
    if not ruta_instal_programa_bak or not ruta_instal_programa_bak.exists():
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

    # Planifica restaurar el BAK a XML
    ruta_xml = ruta_instal_programa_bak.with_suffix('.xml')
    bak_exitoso, idioma_restaurado = restaura_idioma_xml(ruta_xml)
    if not bak_exitoso:
        return False

    # Ejecuta todas las operaciones pendientes de un solo saque
    if operaciones_pendientes_admin:
        #muestra_contenido(f"{Fore.LIGHTCYAN_EX}Aplicando cambios con permisos administrativos...\n")

        success, results, error = ejecutar_operaciones_pendientes(
            titulo=f"Restaurar idioma de {NOMBRE_PROGRAMA} {version_adobe}",
            mensaje=f"Se requieren permisos de administrador para restaurar el idioma de {NOMBRE_PROGRAMA} {version_adobe}.",
            muestra_mensaje_func=muestra_contenido
        )

        if not success:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\nError: {error}\n")
            borde_inferior()

            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False

        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    else: # No necesita permisos de admin
        muestra_contenido(
            f"{Fore.LIGHTGREEN_EX}{TEXTOS['restauro_correctamente_1']} {idioma_restaurado} {TEXTOS['restauro_correctamente_2']} [{ruta_instal_programa_bak}]\n"
        )
    borde_inferior()

    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return True

def pantalla_splash():
    """
    Muestra una pantalla de inicio con un aviso sobre los paquetes de idioma y espera input del usuario
    """
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

def menu_terciario(modo='cambiar'):
    """
    Muestra el menú terciario de Simi con los programas de Adobe y permite ir a otros menús mediante inputs del usuario

    Args:
        modo: 'cambiar' para cambiar idioma, 'restaurar' para restaurar desde backup
    """
    if modo == 'cambiar':
        titulo_menu = titulo_subrayado(f"Adobe {version_adobe} - {TEXTOS['cambiar_a']} {idioma_menu_ui}")
    else:
        titulo_menu = titulo_subrayado(f"Adobe {version_adobe} - {TEXTOS['menu_restaurar_xml']} {TEXTOS['menu_usando_bak']}")

    # Mapeo de programas a sus funciones
    programas_funciones = {
        '1': {
            'cambiar': lambda: cambio_idioma_after_effects(locale_xml),
            'restaurar': lambda: restaurar_xml_after_effects(version_adobe)
        },
        '2': {
            'cambiar': lambda: cambio_idioma_premiere_pro(locale_xml),
            'restaurar': lambda: restaurar_xml_premiere_pro(version_adobe)
        },
        '3': {
            'cambiar': lambda: cambio_idioma_audition(locale_xml),
            'restaurar': lambda: restaurar_xml_audition(version_adobe)
        },
        '4': {
            'cambiar': lambda: cambio_idioma_indesign(locale_xml),
            'restaurar': lambda: restaurar_xml_indesign(version_adobe)
        },
        '5': {
            'cambiar': lambda: cambio_idioma_media_encoder(locale_xml),
            'restaurar': lambda: restaurar_xml_media_encoder(version_adobe)
        },
        '6': {
            'cambiar': lambda: cambio_idioma_photoshop(locale_xml),
            'restaurar': lambda: restaurar_xml_photoshop(version_adobe)
        },
        '7': {
            'cambiar': lambda: cambio_idioma_animate(locale_xml),
            'restaurar': lambda: restaurar_xml_animate(version_adobe)
        },
        '8': {
            'cambiar': lambda: cambio_idioma_illustrator(locale_xml),
            'restaurar': lambda: restaurar_xml_illustrator(version_adobe)
        },
        '9': {
            'cambiar': lambda: cambio_idioma_incopy(locale_xml),
            'restaurar': lambda: restaurar_xml_incopy(version_adobe)
        },
        '10': {
            'cambiar': lambda: cambio_idioma_character_animator(locale_xml),
            'restaurar': lambda: restaurar_xml_character_animator(version_adobe)
        }
    }

    while True:
        limpia_pantalla()

        borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
        muestra_contenido(
            f"\n{TEXTOS['simi_descripcion']}\n\n"
            f"\n{titulo_menu}\n\n"
            " [1] After Effects\n"
            " [2] Premiere Pro\n"
            " [3] Audition\n"
            " [4] InDesign\n"
            " [5] Media Encoder\n"
            " [6] Photoshop\n"
            " [7] Animate\n"
            " [8] Illustrator\n"
            " [9] InCopy"
        )

        # Sólo se muestra si Character Animator es diferente a 2025 (no hay versión 2025 de Character Animator)
        if version_adobe != 2025:
            muestra_contenido("[10] Character Animator")
            ultima_opcion = 10
        else:
            ultima_opcion = 9

        # Opciones default - Se cambia el número si Character Animator se oculta
        muestra_contenido(
            f"[{ultima_opcion+1}] {TEXTOS['menu_principal']}\n"
            f"[{ultima_opcion+2}] {TEXTOS['menu_ayuda']}\n"
            f"[{ultima_opcion+3}] {TEXTOS['menu_reportar_error']}\n"
            f"[{ultima_opcion+4}] {TEXTOS['menu_salir']}\n"
        )
        borde_inferior()

        seleccion = muestra_input_usuario().strip()

        # Primero chequea las opciones de navegación (tienen prioridad)
        if seleccion == str(ultima_opcion+1):
            menu_principal()
            return
        elif seleccion == str(ultima_opcion+2):
            abre_url_ayuda()
        elif seleccion == str(ultima_opcion+3):
            abre_url_reportar_error()
        elif seleccion == str(ultima_opcion+4):
            cierra_programa()
        # Luego ejecuta función del programa seleccionado
        elif seleccion in programas_funciones:
            # Chequea que Character Animator no esté disponible en 2025
            if seleccion == '10' and version_adobe == 2025:
                muestra_input_usuario(f"{TEXTOS['input_error_menu']}").strip()
            else:
                # Ejecuta función correspondiente al modo
                programas_funciones[seleccion][modo]()
        else:
            muestra_input_usuario(f"{TEXTOS['input_error_menu']}").strip()

def menu_secundario(modo='cambiar'):
    """
    Muestra el menú secundario de Simi con las versiones de Adobe y permite ir a otros menús mediante inputs del usuario
    Guarda info de la versión de los programas de Adobe para usar posteriormente en otras funciones

    Args:
        modo: 'cambiar' para cambiar idioma, 'restaurar' para restaurar desde backup
    """
    if modo == 'cambiar':
        titulo_menu = titulo_subrayado(f"{TEXTOS['cambiar_programas']} {idioma_menu_ui}")
    else:
        titulo_menu = titulo_subrayado(f"{TEXTOS['menu_restaurar_xml']} {TEXTOS['menu_usando_bak']}")

    global version_adobe # Se usa afuera de esta función

    while True:
        limpia_pantalla()

        borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
        muestra_contenido(
            f"\n{TEXTOS['simi_descripcion']}\n\n"
            f"\n{titulo_menu}\n\n"
            " [1] Adobe 2025\n"
            " [2] Adobe 2024\n"
            " [3] Adobe 2023\n"
            " [4] Adobe 2022\n"
            " [5] Adobe 2021\n"
            " [6] Adobe 2020\n"
            " [7] Adobe 2019\n"
            " [8] Adobe 2018\n"
            f" [9] {TEXTOS['menu_principal']}\n"
            f"[10] {TEXTOS['menu_ayuda']}\n"
            f"[11] {TEXTOS['menu_reportar_error']}\n"
            f"[12] {TEXTOS['menu_salir']}\n"
        )
        borde_inferior()

        seleccion = muestra_input_usuario().strip()

        if seleccion in ['1', '2', '3', '4', '5', '6', '7', '8']:
            # Mapeo de selección a año
            version_map = {
                '1': 2025,
                '2': 2024,
                '3': 2023,
                '4': 2022,
                '5': 2021,
                '6': 2020,
                '7': 2019,
                '8': 2018
            }
            version_adobe = version_map[seleccion]
            menu_terciario(modo)
        elif seleccion == '9':
            menu_principal()
            return
        elif seleccion == '10':
            abre_url_ayuda()
        elif seleccion == '11':
            abre_url_reportar_error()
        elif seleccion == '12':
            cierra_programa()
        else:
            muestra_input_usuario(f"{TEXTOS['input_error_menu']}").strip()

def menu_principal():
    """
    Muestra el menú principal de Simi y permite ir a otros menús mediante inputs del usuario
    Guarda info de idiomas para usar posteriormente en otras funciones
    """
    titulo_menu = titulo_subrayado(f"{TEXTOS['menu_principal']}")

    # Las usamos afuera de esta función para el resto de los menus y funciones que modifican los idiomas
    global idioma_menu_ui, locale_xml

    while True:
        limpia_pantalla()

        borde_superior(f"{TEXTOS['simi_titulo']}", f"v{VERSION_ACTUAL_SIMI}")
        muestra_contenido(
            f"\n{TEXTOS['simi_descripcion']}\n\n"
            f"\n{titulo_menu}\n\n"
            f"[1] {TEXTOS['menu_cambio_espanol']}\n"
            f"[2] {TEXTOS['menu_cambio_ingles']}\n"
            f"[3] {TEXTOS['menu_restaurar_xml']} {TEXTOS['menu_usando_bak']}\n" # Nueva opción
            f"[4] {TEXTOS['menu_buscar_version']}\n"
            f"[5] {TEXTOS['menu_ayuda']}\n"
            f"[6] {TEXTOS['menu_reportar_error']}\n"
            f"[7] {TEXTOS['menu_salir']}\n"
        )
        borde_inferior()

        seleccion = muestra_input_usuario().strip()

        if seleccion == '1':
            idioma_menu_ui = 'español'
            locale_xml = 'es_ES'
            menu_secundario(modo='cambiar')
        elif seleccion == '2':
            idioma_menu_ui = 'inglés'
            locale_xml = 'en_US'
            menu_secundario(modo='cambiar')
        elif seleccion == '3':
            idioma_menu_ui = ""
            menu_secundario(modo='restaurar')
        elif seleccion == '4':
            version_update()
        elif seleccion == '5':
            abre_url_ayuda()
        elif seleccion == '6':
            abre_url_reportar_error()
        elif seleccion == '7':
            cierra_programa()
        else:
            muestra_input_usuario(f"{TEXTOS['input_error_menu']}").strip()

if __name__ == "__main__":
    try:
        #menu_principal()
        pantalla_splash()
    except KeyboardInterrupt:
        cierra_programa()
