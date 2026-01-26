#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Funciones que permiten realizar tareas que requieren permisos de administrador

Copyright (C) 2025 Leandro Pérez
Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles
"""

import platform
import os
import subprocess
import time
from colorama import Fore

# Imports Simi
import shared_state
from i18n import TEXTOS
from interfaz import BarraProgreso, PADDING_EXT, ANCHO_PANTALLA, muestra_contenido

# Constantes
MACOS_ADMIN_TIMEOUT = 300  # 5 minutes
MACOS_PROGRESS_MIN_TIME = 0.3  # seconds
MACOS_PROGRESS_MAX_TIME = 0.8  # seconds
MACOS_PROGRESS_PER_FILE = 0.05  # seconds
_SISTEMA_OPERATIVO = platform.system()

def es_administrador():
    """
    Chequea si el script está ejecutándose como Administrador/root

    Returns:
        bool: True si es admin/root, de lo contrario False
    """
    if _SISTEMA_OPERATIVO == 'Windows':
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() # type: ignore
        except (AttributeError, OSError):
            return False
    elif _SISTEMA_OPERATIVO == 'Darwin':
        return os.geteuid() == 0 # type: ignore

    return False

def requiere_permisos_administrativos(ruta):
    """
    Chequea si en las rutas donde se instalan los programas de Adobe se requieren permisos de Administrador/root

    Args:
        ruta (str): Ruta en la que se chequean los permisos

    Returns:
        bool: True si requiere permisos administrativos
    """
    ruta = os.path.abspath(ruta)

    if _SISTEMA_OPERATIVO == 'Windows':
        rutas_protegidas = [
            path + "\\Adobe"
            for key in ['PROGRAMW6432', 'PROGRAMFILES(X86)']
            if (path := os.environ.get(key, ''))
        ]
        return any(ruta.lower().startswith(protegida.lower()) for protegida in rutas_protegidas)

    elif _SISTEMA_OPERATIVO == 'Darwin':
        rutas_protegidas = ["/Applications", "/Library/Application Support"]

        # Chequea rutas del sistema
        if any(ruta.startswith(protegida) for protegida in rutas_protegidas):
            return True

        # Chequea si el archivo/carpeta pertenece a root
        return _es_propiedad_de_root(ruta)

    return False

def _es_propiedad_de_root(ruta):
    """
    Helper para chequear si una ruta pertenece a root en macOS

    Args:
        ruta (str): Ruta a chequear

    Returns:
        bool: True si pertenece a root o no se puede acceder
    """
    try:
        if os.path.exists(ruta):
            return os.stat(ruta).st_uid == 0

        # Si no existe, chequea la carpeta padre
        carpeta_padre = os.path.dirname(ruta)
        if carpeta_padre and os.path.exists(carpeta_padre):
            return os.stat(carpeta_padre).st_uid == 0

    except (OSError, PermissionError):
        # Si no se puede acceder, se asume que requiere permisos
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
        # Si la ruta existe, chequea si se puede escribir
        if os.path.exists(ruta):
            # Chequea si el archivo le pertenece a root (macOS)
            if _SISTEMA_OPERATIVO == 'Darwin' and os.stat(ruta).st_uid == 0:
                return False

            # Intenta crear un archivo temporal para chequear los permisos de escritura
            return _test_escritura(ruta)
        else:
            # Si no existe, intenta crear la carpeta
            os.makedirs(ruta, exist_ok=True)

            # Chequea si la carpeta creada pertenece a root en macOS
            if _SISTEMA_OPERATIVO == 'Darwin' and os.stat(ruta).st_uid == 0:
                return False

            return _test_escritura(ruta)

    except (PermissionError, OSError):

        return False

def _test_escritura(ruta):
    """
    Helper para testear permisos de escritura creando un archivo temporal

    Args:
        ruta (str): Ruta donde testear

    Returns:
        bool: True si se puede escribir
    """
    archivo_prueba = os.path.join(ruta, ".test_temp")
    try:
        with open(archivo_prueba, 'w') as f:
            f.write("test")
        os.remove(archivo_prueba)
        return True

    except (PermissionError, OSError):
        return False

def agregar_operacion_pendiente(operacion):
    """
    Agrega una operación a la lista de operaciones pendientes que requieren permisos de Admin/root

    Args:
        operacion (dict): Operación a agregar
    """
    if shared_state.operaciones_pendientes_admin is None:
        shared_state.operaciones_pendientes_admin = []

    shared_state.operaciones_pendientes_admin.append(operacion)

def ejecutar_operaciones_pendientes(titulo="Operaciones con permisos administrativos",
                                    mensaje="Se requieren permisos de Administrador para completar las operaciones pendientes",
                                    muestra_mensaje_func=None):
    """
    Ejecuta todas las operaciones pendientes que requieren permisos administrativos de un solo saque

    Returns:
        tuple: (success: bool, results: list, error: str)
    """
    if not shared_state.operaciones_pendientes_admin:
        return True, [], ""

    # Ejecuta todas las operaciones pendientes
    success, results, error = ejecutar_operacion_con_permisos(
        shared_state.operaciones_pendientes_admin,
        titulo=titulo,
        mensaje=mensaje,
        muestra_mensaje_func=muestra_mensaje_func
    )

    # Limpia la lista de operaciones pendientes
    shared_state.operaciones_pendientes_admin = []

    return success, results, error

def ejecutar_operacion_con_permisos(operaciones, titulo="Se requieren permisos administrativos",
                                    mensaje="Se requieren permisos de Administrador para realizar esta operación",
                                    muestra_mensaje_func=None):
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

    if _SISTEMA_OPERATIVO == 'Windows':
        if not es_administrador():
            return False, [], f"{TEXTOS['no_se_detectaron_permisos']}"
        return _ejecutar_operaciones_windows(operaciones, mostrar_mensaje)

    elif _SISTEMA_OPERATIVO == 'Darwin':
        return _ejecutar_operaciones_macos(operaciones, titulo, mensaje, mostrar_mensaje)

    return False, [], f"{Fore.LIGHTRED_EX}{TEXTOS['no_soportado']}"

def _ejecutar_operaciones_windows(operaciones, mostrar_mensaje):
    """ Ejecuta operaciones en Windows usando permisos existentes """
    import shutil

    resultados = []

    for operacion in operaciones:
        try:
            tipo = operacion['tipo']

            if tipo == 'comando':
                resultado = subprocess.run(operacion['comando'], shell=True, capture_output=True, text=True)
                resultados.append({
                    'tipo': 'comando',
                    'exitoso': resultado.returncode == 0,
                    'salida': resultado.stdout,
                    'error': resultado.stderr
                })

            elif tipo == 'archivo':
                os.makedirs(os.path.dirname(operacion['destino']), exist_ok=True)
                shutil.copy2(operacion['origen'], operacion['destino'])
                resultados.append({'tipo': 'archivo', 'exitoso': True})

            elif tipo == 'contenido':
                os.makedirs(os.path.dirname(operacion['destino']), exist_ok=True)
                with open(operacion['destino'], 'w', encoding=operacion.get('encoding', 'utf-8')) as f:
                    f.write(operacion['contenido'])
                resultados.append({'tipo': 'contenido', 'exitoso': True})

        except Exception as e:
            resultados.append({'tipo': operacion['tipo'], 'exitoso': False, 'error': str(e)})

    return True, resultados, ""

def _ejecutar_operaciones_macos(operaciones, titulo, mensaje, mostrar_mensaje):
    """
    Ejecuta operaciones en macOS combinándolas en un solo comando con permisos, así se muestra 1 único popup pidiendo ingresar contraseña
    """
    import shutil
    import tempfile

    archivos_temporales = []

    try:
        archivos_totales = 0
        if shared_state._temp_copy_info:
            archivos_totales = shared_state._temp_copy_info.get('archivos_totales', 0)

        comandos = []

        for i, operacion in enumerate(operaciones):
            tipo = operacion['tipo']

            if tipo == 'comando':
                comandos.append(operacion['comando'])

            elif tipo == 'archivo':
                # Crea carpeta destino si no existe
                carpeta_destino = os.path.dirname(operacion['destino'])
                comandos.append(f"mkdir -p '{carpeta_destino}'")
                comandos.append(f"cp '{operacion['origen']}' '{operacion['destino']}'")

            elif tipo == 'contenido':
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

        # Construye comandos
        comando_completo = " && ".join(comandos)
        comando_escapado = comando_completo.replace('\\', '\\\\').replace('"', '\\"')

        # AppleScript para ejecutar con permisos de admin
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

        # Ejecuta el AppleScript (incluye el popup de contraseña)
        resultado = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=MACOS_ADMIN_TIMEOUT
        )

        # Si fue exitoso Y hay archivos para copiar, muestra el progreso
        output = resultado.stdout.strip()

        if resultado.returncode == 0 and output.startswith("SUCCESS:") and archivos_totales > 0:
            _mostrar_progreso_copia_macos(archivos_totales, mostrar_mensaje)

        # Limpia archivos temporales
        _limpiar_archivos_temporales(archivos_temporales)
        _limpiar_temp_copy_info(resultado.returncode != 0)

        # Procesa resultado
        if resultado.returncode != 0:
            return False, [], f"{Fore.LIGHTRED_EX}{TEXTOS['error_en_script']} {resultado.stderr}\n"

        if output.startswith("SUCCESS:"):
            resultados = [{'tipo': op['tipo'], 'exitoso': True} for op in operaciones]
            return True, resultados, ""

        elif output == "USER_CANCELLED":
            return False, [], f"{TEXTOS['macos_osascript_cancelado']}"

        else:
            msj_error = output[6:] if output.startswith("ERROR:") else output
            mostrar_mensaje(f"{Fore.LIGHTRED_EX}{TEXTOS['macos_osascript_error_ejecutar']} {msj_error}\n")
            return False, [], msj_error

    except subprocess.TimeoutExpired:
        _limpiar_archivos_temporales(archivos_temporales)
        _limpiar_temp_copy_info(True)
        return False, [], f"{TEXTOS['macos_osascript_timeout2']}"

    except Exception as e:
        mostrar_mensaje(f"{Fore.LIGHTRED_EX}Error: {str(e)}\n")
        _limpiar_temp_copy_info(True)
        return False, [], str(e)

def _mostrar_progreso_copia_macos(archivos_totales, mostrar_mensaje):
    """ Helper para mostrar barra de progreso en macOS """
    mostrar_mensaje(f"\n{TEXTOS['copiando_idioma']}")
    progreso = BarraProgreso(archivos_totales, modo='copia', tiempo_actualizacion=0.05)

    # Simula progreso rápido ya que los archivos YA se copiaron con el comando admin
    tiempo_estimado = min(max(archivos_totales * MACOS_PROGRESS_PER_FILE, MACOS_PROGRESS_MIN_TIME), MACOS_PROGRESS_MAX_TIME)
    intervalo = tiempo_estimado / archivos_totales

    for i in range(archivos_totales):
        time.sleep(intervalo)
        nombre_archivo = f"archivo_{i+1}.dat"
        progreso.actualiza(1, nombre_archivo)

    progreso.finaliza()
    print(" " * PADDING_EXT + "│" + " " * (ANCHO_PANTALLA - 2) + "│")

def _limpiar_archivos_temporales(archivos_temporales):
    """ Helper para limpiar archivos temporales """
    for archivo_temp in archivos_temporales:
        try:
            os.unlink(archivo_temp)
        except:
            pass

def _limpiar_temp_copy_info(limpiar_carpeta=False):
    """ Helper para limpiar información temporal de shared_state.py """
    if not shared_state._temp_copy_info:
        return

    try:
        if limpiar_carpeta:
            carpeta_temp = shared_state._temp_copy_info.get('carpeta_temp')
            if carpeta_temp and os.path.exists(carpeta_temp):
                import shutil
                shutil.rmtree(carpeta_temp)
        shared_state._temp_copy_info = None
    except:
        pass

def planifica_ops_sis_archivos(operaciones):
    """
    Planifica operaciones del sistema de archivos para luego ejecutarlas a todas juntas

    Args:
        operaciones (list): Lista de operaciones:
            - {'accion': 'crear_carpeta', 'ruta': 'path'}
            - {'accion': 'copiar_archivo', 'origen': 'src', 'destino': 'dst'}
            - {'accion': 'escribir_archivo', 'contenido': 'text', 'destino': 'path', 'encoding': 'utf-8'}
            - {'accion': 'comando', 'comando': 'shell_command'}
    """
    if shared_state.operaciones_pendientes_admin is None:
        shared_state.operaciones_pendientes_admin = []

    # Procesa cada operación
    for op in operaciones:
        requiere_admin = _chequea_si_requiere_admin(op)

        if requiere_admin:
            _agregar_operacion_admin(op)
        else:
            # Ejecuta directamente si no requiere admin
            try:
                _ejecuta_operacion_directa(op)
            except PermissionError:
                # Si falla por permisos, agrega a operaciones pendientes con admin
                _agregar_operacion_admin(op)

def _chequea_si_requiere_admin(op):
    """ Helper para determinar si una operación requiere permisos de admin """
    accion = op['accion']

    if accion in ['crear_carpeta', 'escribir_archivo']:
        ruta_check = op.get('ruta', op.get('destino', ''))
        return requiere_permisos_administrativos(ruta_check)
    elif accion == 'copiar_archivo':
        return requiere_permisos_administrativos(op['destino'])
    elif accion == 'comando':
        return True

    return False

def _agregar_operacion_admin(op):
    """ Helper para agregar operación a la lista de operaciones con admin """
    accion = op['accion']

    if accion == 'crear_carpeta':
        if _SISTEMA_OPERATIVO == 'Windows':
            shared_state.operaciones_pendientes_admin.append({
                'tipo': 'comando',
                'comando': f'mkdir "{op["ruta"]}" 2>nul || echo.'
            })
        else:
            shared_state.operaciones_pendientes_admin.append({
                'tipo': 'comando',
                'comando': f"mkdir -p '{op['ruta']}'"
            })

    elif accion == 'copiar_archivo':
        shared_state.operaciones_pendientes_admin.append({
            'tipo': 'archivo',
            'origen': op['origen'],
            'destino': op['destino']
        })

    elif accion == 'escribir_archivo':
        shared_state.operaciones_pendientes_admin.append({
            'tipo': 'contenido',
            'contenido': op['contenido'],
            'destino': op['destino'],
            'encoding': op.get('encoding', 'utf-8')
        })

    elif accion == 'comando':
        shared_state.operaciones_pendientes_admin.append({
            'tipo': 'comando',
            'comando': op['comando']
        })

def _ejecuta_operacion_directa(operacion):
    """ Ejecuta una operación individual sin permisos administrativos """
    import shutil

    accion = operacion['accion']

    if accion == 'crear_carpeta':
        ruta = operacion['ruta']
        if os.path.exists(ruta) and not chequea_permisos_escritura(ruta):
            raise PermissionError(f"{TEXTOS['permisos_insuficientes']} {ruta}")
        os.makedirs(ruta, exist_ok=True)
        return True

    if accion == 'copiar_archivo':
        carpeta_destino = os.path.dirname(operacion['destino'])
        carpeta_check = carpeta_destino if os.path.exists(carpeta_destino) else os.path.dirname(carpeta_destino)

        if not chequea_permisos_escritura(carpeta_check):
            raise PermissionError(f"{TEXTOS['permisos_insuficientes']} {operacion['destino']}")

        os.makedirs(carpeta_destino, exist_ok=True)
        shutil.copy2(operacion['origen'], operacion['destino'])
        return True

    if accion == 'escribir_archivo':
        destino = operacion['destino']
        carpeta_destino = os.path.dirname(destino)

        # Chequea permisos
        if os.path.exists(destino):
            if _SISTEMA_OPERATIVO == 'Darwin':
                stat_info = os.stat(destino)
                if stat_info.st_uid == 0 or not os.access(destino, os.W_OK):
                    raise PermissionError(f"{TEXTOS['permisos_insuficientes']} {destino}")
        else:
            carpeta_check = carpeta_destino if os.path.exists(carpeta_destino) else os.path.dirname(carpeta_destino)
            if not chequea_permisos_escritura(carpeta_check):
                raise PermissionError(f"{TEXTOS['permisos_insuficientes']} {destino}")

        os.makedirs(carpeta_destino, exist_ok=True)
        with open(destino, 'w', encoding=operacion.get('encoding', 'utf-8')) as f:
            f.write(operacion['contenido'])
        return True

    if accion == 'comando':
        resultado = subprocess.run(operacion['comando'], shell=True, capture_output=True, text=True)
        if resultado.returncode != 0:
            raise Exception(f"{Fore.LIGHTRED_EX}{TEXTOS['error_ejecutar_comando']} {resultado.stderr}\n")
        return True

    return False
