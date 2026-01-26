#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dibuja la interfaz de la app y barra de progreso de descarga/copia de archivos

Copyright (C) 2025 Leandro Pérez
Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles
"""

import time
import re
import sys
import colorama
from colorama import Style
from textwrap import fill

# Imports Simi
from i18n import TEXTOS
from traduccion_rutas import limpia_codigos_color_para_longitud, preparar_texto_para_mostrar

# Para que colorama funcione en la GUI de tkinter
colorama.init(strip=False)

# Constantes caja UI
CARACTER_BORDE = "─"
ANCHO_PANTALLA = 80
PADDING_INT = 3
PADDING_EXT = 4

# Compila el regex una sola vez al iniciar la app
_COLOR_CODE_PATTERN = re.compile(r'\x1b\[[0-9;]*m')

class BarraProgreso:
    def __init__(self, total, modo='descarga', tiempo_actualizacion=0.1):
        """
        Barra de progreso que se muestra al descargar, copiar o extraer archivos

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

        # Config para cada modo - OPTIMIZADO: dict lookup es más rápido que if/elif
        self.config_modo = {
            'descarga': {
                'unidad': 'B',
                'sufijo_velocidad': '/s',
                'formato_func': self._formato_bytes,
            },
            'unzip': {
                'unidad': 'files',
                'sufijo_velocidad': '/s',
                'formato_func': self._formato_cantidad,
            },
            'copia': {
                'unidad': 'files',
                'sufijo_velocidad': '/s',
                'formato_func': self._formato_cantidad,
            }
        }

        if self.modo not in self.config_modo:
            raise ValueError(f"{TEXTOS['barra_progreso_modo1']} {modo}. {TEXTOS['barra_progreso_modo2']}")

    @staticmethod
    def _formato_bytes(valor_bytes):
        """ Formatea bytes a otras unidades """
        for unidad in ['B', 'KB', 'MB', 'GB']:
            if valor_bytes < 1024.0:
                return f"{valor_bytes:.1f} {unidad}"
            valor_bytes /= 1024.0
        return f"{valor_bytes:.1f} TB"

    @staticmethod
    def _formato_cantidad(contador):
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
    Limpia la pantalla
    """
    sys.stdout.write('\x1b[2J\x1b[H\n\n')
    sys.stdout.flush()


def borde_superior(texto_izq="", texto_der=""):
    """
    Muestra el borde superior con texto a la izquierda y derecha para armar la caja de contenido

    Formato: ╭─ texto_izq ───── texto_der ─╮

    Args:
        texto_izq (str): Texto que se muestra en la izquierda
        texto_der (str): Texto que se muestra en la derecha
    """
    ancho_total = ANCHO_PANTALLA - 2

    # Limpia el texto de códigos de color para calcular longitud real
    texto_izq_limpio = limpia_codigos_color_para_longitud(texto_izq)
    texto_der_limpio = limpia_codigos_color_para_longitud(texto_der)

    # Calcula la línea respecto a los textos que existen
    if texto_izq_limpio and texto_der_limpio:
        espacios_libres = max(5, ancho_total - len(texto_izq_limpio) - len(texto_der_limpio) - 6)
        borde_medio = CARACTER_BORDE * espacios_libres
        texto_izq_mostrar = preparar_texto_para_mostrar(texto_izq)
        texto_der_mostrar = preparar_texto_para_mostrar(texto_der)
        linea_superior = f"╭{CARACTER_BORDE} {texto_izq_mostrar} {borde_medio} {texto_der_mostrar} {CARACTER_BORDE}╮"
    elif texto_izq_limpio:
        espacios_libres = ancho_total - len(texto_izq_limpio) - 3
        borde_resto = CARACTER_BORDE * espacios_libres
        texto_izq_mostrar = preparar_texto_para_mostrar(texto_izq)
        linea_superior = f"╭{CARACTER_BORDE} {texto_izq_mostrar} {borde_resto}╮"
    elif texto_der_limpio:
        espacios_libres = ancho_total - len(texto_der_limpio) - 3
        borde_resto = CARACTER_BORDE * espacios_libres
        texto_der_mostrar = preparar_texto_para_mostrar(texto_der)
        linea_superior = f"╭{borde_resto} {texto_der_mostrar} {CARACTER_BORDE}╮"
    else:
        linea_superior = "╭" + CARACTER_BORDE * ancho_total + "╮"

    sys.stdout.write(" " * PADDING_EXT + linea_superior + Style.RESET_ALL + '\n')
    sys.stdout.flush()


def borde_inferior():
    """
    Muestra el borde inferior para armar la caja de contenido

    Formato: ╰───────────────────────╯
    """
    sys.stdout.write(" " * PADDING_EXT + "╰" + CARACTER_BORDE * (ANCHO_PANTALLA - 2) + "╯\n")
    sys.stdout.flush()

def extrae_codigos_color_activos(texto):
    """
    Extrae todos los códigos de color que están activos al final del texto

    Args:
        texto (str): Texto al que se le extrae el código de color
    """
    # Busca todos los códigos ANSI en el texto
    codigos = _COLOR_CODE_PATTERN.findall(texto)

    if not codigos:
        return ""

    ultimo_codigo = codigos[-1]

    # Si es un reset, no hay colores activos
    if ultimo_codigo == '\x1b[0m' or 'RESET' in ultimo_codigo:
        return ""

    return ultimo_codigo

def muestra_contenido(texto):
    """
    Muestra el texto dentro de la caja de contenido redondeada y agrega padding por dentro y fuera
    Acumula output y hace un solo write al final

    Args:
        texto (str): El texto del contenido
    """
    lineas = texto.split("\n")
    colores_heredados = ""
    output_lines = [] # Junta todas las líneas
    ancho_disponible = ANCHO_PANTALLA - 4 - PADDING_INT * 2

    for linea in lineas:
        # Si la línea está vacía, muestra una línea vacía y mantiene colores heredados
        if not linea.strip():
            output_lines.append(" " * PADDING_EXT + "│" + " " * (ANCHO_PANTALLA - 2) + "│")
            continue

        # Busca códigos de color en la línea actual
        codigos_en_linea = _COLOR_CODE_PATTERN.findall(linea)

        # Si la línea tiene códigos de color, se usan; si no, usa los colores heredados
        if codigos_en_linea:
            linea_con_colores = linea
            colores_heredados = extrae_codigos_color_activos(linea)
        else:
            linea_con_colores = colores_heredados + linea

        # Extrae solo el texto visible (sin códigos de color)
        linea_visible = limpia_codigos_color_para_longitud(linea_con_colores)

        # Envuelve el texto si es necesario
        if len(linea_visible) > ancho_disponible:
            lineas_envueltas = fill(linea_visible, width=ancho_disponible).split("\n")

            for linea_envuelta in lineas_envueltas:
                color_a_usar = "".join(codigos_en_linea) if codigos_en_linea else colores_heredados
                linea_envuelta_traducida = preparar_texto_para_mostrar(linea_envuelta)
                texto_coloreado = f"{color_a_usar}{linea_envuelta_traducida}{Style.RESET_ALL}"
                len_visible_actual = len(linea_envuelta)
                padding_relleno = " " * (ancho_disponible - len_visible_actual)
                linea_interna = f'{" " * PADDING_INT}{texto_coloreado}{padding_relleno}{" " * PADDING_INT}'
                output_lines.append(f'{" " * PADDING_EXT}│ {linea_interna} │{Style.RESET_ALL}')
        else:
            color_a_usar = "".join(codigos_en_linea) if codigos_en_linea else colores_heredados
            linea_visible_traducida = preparar_texto_para_mostrar(linea_visible)
            texto_coloreado = f"{color_a_usar}{linea_visible_traducida}{Style.RESET_ALL}"
            len_visible_actual = len(linea_visible)
            padding_relleno = " " * (ancho_disponible - len_visible_actual)
            linea_interna = f'{" " * PADDING_INT}{texto_coloreado}{padding_relleno}{" " * PADDING_INT}'
            output_lines.append(f'{" " * PADDING_EXT}│ {linea_interna} │{Style.RESET_ALL}')

    # Escribe output
    sys.stdout.write('\n'.join(output_lines) + '\n')
    sys.stdout.flush()

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
    texto_limpio = _COLOR_CODE_PATTERN.sub('', texto)

    # Crea la línea de subrayado con la misma longitud
    subrayado = caracter_subrayado * len(texto_limpio)

    # Aplica un color si se especifica
    if color:
        return f"{color}{texto}{Style.RESET_ALL}\n{subrayado}"
    else:
        return f"{texto}\n{subrayado}"

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
    sys.stdout.write("\n" + (" " * padding_total) + texto_prompt + '\n')
    sys.stdout.write(" " * padding_total + "> ")
    sys.stdout.flush()

    return input()
