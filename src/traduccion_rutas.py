#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Traduce las rutas que se muestran al usuario del inglés al español, si el sistema operativo tiene como display language el español

Copyright (C) 2025 Leandro Pérez
Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles
"""

import platform
import re
import subprocess
import ctypes
import os

if os.name == 'nt':
    from ctypes import windll

# Constantes
_SISTEMA_OPERATIVO = platform.system()
_PATRON_RUTA_WINDOWS = re.compile(r'[A-Z]:[\\\/][^\n\r\x1b\[\]]+')
_PATRON_RUTA_MACOS = re.compile(r'/[^\n\r\x1b\[\]\s]+(?:/[^\n\r\x1b\[\]\s]+)*')
_PATRON_CODIGOS_COLOR = re.compile(r'\x1b\[[0-9;]*m')
_TRADUCCIONES_CACHE = None

def _detectar_idioma_sistema():
    """
    Detecta si el sistema está en español

    Returns:
        bool: True si el sistema está en español
    """
    try:
        if _SISTEMA_OPERATIVO == 'Windows':
            windll = ctypes.windll.kernel32 # type: ignore
            idioma_codigo = windll.GetUserDefaultUILanguage()
            idioma_primario = idioma_codigo & 0x3FF
            return idioma_primario == 0x0A

        elif _SISTEMA_OPERATIVO == 'Darwin':
            try:
                resultado = subprocess.run(
                    ['defaults', 'read', '-g', 'AppleLanguages'],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                idiomas = resultado.stdout.strip()

                if idiomas.startswith('('):
                    primer_idioma = re.search(r'"\s*([^"]+?)\s*"', idiomas)
                    if primer_idioma:
                        idioma_principal = primer_idioma.group(1).lower()
                        return idioma_principal.startswith('es')
                return False

            except:
                return False
    except:
        return False

def obtener_traducciones_carpetas():
    """
    Devuelve un diccionario con las traducciones de carpetas específicas

    Returns:
        dict: Diccionario con traducciones {carpeta_ingles: carpeta_traducida}
    """
    global _TRADUCCIONES_CACHE

    # Si ya lo calculamos antes, devuelve el caché
    if _TRADUCCIONES_CACHE is not None:
        return _TRADUCCIONES_CACHE

    # Detecta idioma
    es_espanol = _detectar_idioma_sistema()

    if not es_espanol:
        _TRADUCCIONES_CACHE = {}
        return _TRADUCCIONES_CACHE

    # Traducciones solo para carpetas específicas que muestra Simi
    if _SISTEMA_OPERATIVO == 'Windows':
        _TRADUCCIONES_CACHE = {
            'Users': 'Usuarios',
            'Downloads': 'Descargas',
            'Program Files': 'Archivos de programa'
        }
    else: # macOS
        _TRADUCCIONES_CACHE = {
            'Users': 'Usuarios',
            'Downloads': 'Descargas',
            'Library': 'Biblioteca',
            'Applications': 'Aplicaciones'
        }

    return _TRADUCCIONES_CACHE

def traducir_ruta(ruta):
    """
    Traduce una ruta individual

    Args:
        ruta (str): Ruta a traducir

    Returns:
        str: Ruta traducida
    """
    traducciones = obtener_traducciones_carpetas()

    if not traducciones:
        return ruta

    ruta_traducida = ruta

    for ingles, traducido in traducciones.items():
        # Separadores de ruta en medio
        ruta_traducida = ruta_traducida.replace(f"/{ingles}/", f"/{traducido}/")
        ruta_traducida = ruta_traducida.replace(f"\\{ingles}\\", f"\\{traducido}\\")

        # Al inicio de la ruta
        if ruta_traducida.startswith(f"/{ingles}"):
            ruta_traducida = f"/{traducido}" + ruta_traducida[len(f"/{ingles}"):]
        if ruta_traducida.startswith(f"{ingles}\\"):
            ruta_traducida = f"{traducido}\\" + ruta_traducida[len(f"{ingles}\\"):]

        # Al final de la ruta
        if ruta_traducida.endswith(f"/{ingles}"):
            ruta_traducida = ruta_traducida[:-len(f"/{ingles}")] + f"/{traducido}"
        if ruta_traducida.endswith(f"\\{ingles}"):
            ruta_traducida = ruta_traducida[:-len(f"\\{ingles}")] + f"\\{traducido}"

    return ruta_traducida

def traducir_texto_con_rutas(texto):
    """
    Traduce todas las rutas en un texto, preservando el resto del contenido

    Args:
        texto (str): Texto que puede contener rutas

    Returns:
        str: Texto con rutas traducidas
    """
    traducciones = obtener_traducciones_carpetas()

    if not traducciones:
        return texto

    # Usa el regex precompilado según el sistema
    patron_ruta = _PATRON_RUTA_WINDOWS if _SISTEMA_OPERATIVO == 'Windows' else _PATRON_RUTA_MACOS

    def reemplazar_ruta(match):
        ruta_original = match.group()
        # Limpia caracteres finales como puntuación
        ruta_limpia = ruta_original.rstrip('.,;:!?)]')
        sufijo = ruta_original[len(ruta_limpia):]

        ruta_traducida = traducir_ruta(ruta_limpia)
        return ruta_traducida + sufijo

    return patron_ruta.sub(reemplazar_ruta, texto)

def limpia_codigos_color_para_longitud(texto):
    """
    Limpia códigos de color ANSI para calcular la longitud visible real del texto
    Incluye la traducción de rutas en el cálculo

    Args:
        texto (str): Texto con posibles códigos ANSI y rutas

    Returns:
        str: Texto sin códigos ANSI pero con rutas traducidas
    """
    # Primero traduce las rutas
    texto_traducido = traducir_texto_con_rutas(texto)

    # Usa regex precompilado para limpiar códigos de color
    texto_limpio = _PATRON_CODIGOS_COLOR.sub('', texto_traducido)

    return texto_limpio

def preparar_texto_para_mostrar(texto):
    """
    Prepara el texto para mostrarlo. Traduce rutas y preserva códigos de color

    Args:
        texto (str): Texto original con códigos ANSI

    Returns:
        str: Texto con rutas traducidas y códigos de color preservados
    """
    return traducir_texto_con_rutas(texto)

def destraducir_ruta(ruta_traducida):
    """
    Convierte una ruta traducida de vuelta al inglés para verificar si existe

    Args:
        ruta_traducida (str): Ruta que puede estar en español

    Returns:
        str: Ruta en inglés
    """
    traducciones = obtener_traducciones_carpetas()

    if not traducciones:
        return ruta_traducida

    ruta_original = ruta_traducida

    # Invierte el diccionario una sola vez
    traducciones_invertidas = {traducido: ingles for ingles, traducido in traducciones.items()}

    for traducido, ingles in traducciones_invertidas.items():
        # Separadores de ruta en medio
        ruta_original = ruta_original.replace(f"/{traducido}/", f"/{ingles}/")
        ruta_original = ruta_original.replace(f"\\{traducido}\\", f"\\{ingles}\\")

        # Al inicio de la ruta
        if ruta_original.startswith(f"/{traducido}"):
            ruta_original = f"/{ingles}" + ruta_original[len(f"/{traducido}"):]
        if ruta_original.startswith(f"{traducido}\\"):
            ruta_original = f"{ingles}\\" + ruta_original[len(f"{traducido}\\"):]

        # Al final de la ruta
        if ruta_original.endswith(f"/{traducido}"):
            ruta_original = ruta_original[:-len(f"/{traducido}")] + f"/{ingles}"
        if ruta_original.endswith(f"\\{traducido}"):
            ruta_original = ruta_original[:-len(f"\\{traducido}")] + f"\\{ingles}"

    return ruta_original

# Popula el caché al cargar el módulo, el chequeo de idioma se hace una sola vez al inicio
obtener_traducciones_carpetas()
