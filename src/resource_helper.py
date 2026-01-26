#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Helper para encontrar archivos en entornos de desarrollo y de PyInstaller

Copyright (C) 2025 Leandro Pérez
Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles
"""

import os
import sys

def get_ruta_resource(ruta_relativa):
    """
    Obtiene la ruta absoluta donde se encuentran los archivos, funciona en entornos dev y de PyInstaller

    Args:
        ruta_relativa: Ruta relativa al root del proyecto (ej: 'src/main.py')

    Returns:
        Ruta absoluta al archivo
    """
    try:
        # PyInstaller usa la carpeta temporal _MEIPASS
        ruta_base = getattr(sys, '_MEIPASS', None)
        if ruta_base is None:
            raise AttributeError("_MEIPASS not found")

    except (AttributeError, Exception):
        # Entorno de desarrollo, usa la carpeta que contiene este script
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(ruta_base, ruta_relativa)

def get_ruta_script(nombre_script):
    """
    Obtiene la ruta donde se encuentra un script

    Args:
        nombre_script: Nombre del script (ej: 'main.py')

    Returns:
        Ruta absoluta al script
    """
    return get_ruta_resource(f'src/{nombre_script}')

def existe_archivo(ruta_relativa):
    """
    Chequea si un archivo existe

    Args:
        ruta_relativa: Ruta relativa al root del proyecto

    Returns:
        True si el archivo existe, caso contrario False
    """
    return os.path.exists(get_ruta_resource(ruta_relativa))

def get_ruta_asset(nombre_asset):
    """
    Obtiene la ruta donde se encuentra un asset

    Args:
        nombre_asset: Nombre del asset (ej: 'icono_win.ico')

    Returns:
        Ruta absoluta al asset
    """
    return get_ruta_resource(f'assets/{nombre_asset}')

def get_ruta_base():
    """
    Obtiene la ruta base de la app

    Returns:
        Ruta base como string
    """
    try:
        ruta_base = getattr(sys, '_MEIPASS', None)
        if ruta_base is None:
            raise AttributeError("_MEIPASS no encontrada")
        return ruta_base

    except (AttributeError, Exception):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
