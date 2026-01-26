#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para compartir estado de variables entre otros módulos

Copyright (C) 2025 Leandro Pérez
Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles
"""

# Información temporal para operaciones de copia (usado en descomprime_zip y _ejecutar_operaciones_macos)
_temp_copy_info = None

# Lista de operaciones pendientes que requieren permisos administrativos
operaciones_pendientes_admin = []

# Variables de configuración del menú
idioma_menu_ui = None # 'español' o 'inglés'
locale_xml = None # 'es_ES' o 'en_US'
version_adobe = None # 2018+

# Rutas de archivos
ruta_backup_xml = None # Ruta del archivo .bak creado por Simi
ruta_instal_print = None # Ruta de instalación para mostrar al usuario
