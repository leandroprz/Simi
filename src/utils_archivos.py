#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Funciones relacionadas al manejo de archivos: descarga, copia, lectura

Copyright (C) 2025 Leandro Pérez
Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles
"""

import os
import re
import platform
import tempfile
import shutil
from pathlib import Path
from typing import Tuple, Optional, Dict, List
from colorama import Fore
from urllib.parse import urlparse

# Imports Simi
import shared_state
from config import TAG_IDIOMAS
from i18n import TEXTOS
from interfaz import ANCHO_PANTALLA, PADDING_EXT, BarraProgreso, muestra_contenido, borde_inferior, muestra_input_usuario
from permisos_admin import requiere_permisos_administrativos, planifica_ops_sis_archivos

# Constantes
_SISTEMA_OPERATIVO = platform.system()
_ES_WINDOWS = _SISTEMA_OPERATIVO == 'Windows'
_ES_MACOS = _SISTEMA_OPERATIVO == 'Darwin'
_REGEX_ENCODING = re.compile(r'encoding\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)

def get_carpeta_descargas() -> str:
    """ Obtiene la carpeta Descargas del usuario """
    if _ES_WINDOWS:
        return _get_carpeta_descargas_windows()
    else: # macOS
        return os.path.join(os.path.expanduser("~"), "Downloads")

def _get_carpeta_descargas_windows() -> str:
    """ Helper para obtener carpeta Descargas en Windows (incluso si fue movida) """
    from uuid import UUID
    import ctypes
    from ctypes import windll, wintypes # type: ignore

    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD), # type: ignore
            ("Data2", wintypes.WORD), # type: ignore
            ("Data3", wintypes.WORD), # type: ignore
            ("Data4", wintypes.BYTE * 8) # type: ignore
        ]

        def __init__(self, uuid_str):
            uuid = UUID(uuid_str)
            ctypes.Structure.__init__(self)
            self.Data1, self.Data2, self.Data3, \
                self.Data4[0], self.Data4[1], rest = uuid.fields

            for i in range(2, 8):
                self.Data4[i] = rest>>(8-i-1)*8 & 0xff

    SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath # type: ignore
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID), wintypes.DWORD, # type: ignore
        wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p) # type: ignore
    ]

    ruta_ptr = ctypes.c_wchar_p()
    guid = GUID('{374DE290-123F-4565-9164-39C4925E467B}') # Carpeta Downloads

    if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(ruta_ptr)):
        raise ctypes.WinError() # type: ignore

    if ruta_ptr.value is None:
        raise ValueError(f"{Fore.LIGHTRED_EX}{TEXTOS['error_ruta_descargas']}")

    return ruta_ptr.value

def detecta_encoding(ruta_archivo: str) -> str:
    """
    Detecta el encoding de un archivo XML

    Args:
        ruta_archivo: Ruta del archivo XML

    Returns:
        Encoding detectado (default: 'utf-8')
    """
    import xml.etree.ElementTree as ET

    try:
        # Parsea el XML (valida encoding automáticamente)
        ET.parse(ruta_archivo)

        # Extrae el encoding usando regex precompilado
        with open(ruta_archivo, 'rb') as f:
            primera_linea = f.readline().decode('ascii', errors='ignore')

        match = _REGEX_ENCODING.search(primera_linea)
        return match.group(1).lower() if match else 'utf-8'

    except:
        return 'utf-8' # Fallback

def _mostrar_error_y_salir(mensaje: str) -> bool:
    """ Helper para mostrar mensaje de error y esperar input """
    muestra_contenido(mensaje)
    borde_inferior()
    muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
    return False

def edita_idioma_xml(ruta_carpeta: str, nuevo_idioma: str) -> bool:
    """
    Modifica el archivo XML de un programa de Adobe para cambiar su idioma y crea una copia de seguridad

    Args:
        ruta_carpeta: Ruta del archivo XML
        nuevo_idioma: Nuevo código de idioma (ej: 'es_ES', 'en_US')

    Returns:
        True si fue exitoso
    """
    import xml.etree.ElementTree as ET

    try:
        ruta_archivo_xml = os.path.join(ruta_carpeta)

        # Chequea si el archivo existe
        if not os.path.exists(ruta_archivo_xml):
            return _mostrar_error_y_salir(
                f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\n\n"
                f"{Fore.LIGHTYELLOW_EX}{TEXTOS['razones']}\n"
            )

        # Lee y valida XML
        encoding = detecta_encoding(ruta_archivo_xml)
        with open(ruta_archivo_xml, 'r', encoding=encoding) as f:
            contenido = f.read()

        if not re.search(TAG_IDIOMAS, contenido):
            return _mostrar_error_y_salir(
                f"{Fore.LIGHTRED_EX}{TEXTOS['no_cambio']}\n\n"
                f"{Fore.LIGHTYELLOW_EX}{TEXTOS['razones']}\n"
            )

        # Cambia el contenido
        nuevo_tag = f'<Data key="installedLanguages">{nuevo_idioma}</Data>'
        contenido_actualizado = re.sub(TAG_IDIOMAS, nuevo_tag, contenido)

        # Prepara las rutas
        ruta_xml = Path(ruta_archivo_xml)
        ruta_backup_xml = ruta_xml.with_suffix('.bak')
        shared_state.ruta_backup_xml = str(ruta_backup_xml)

        # Construye operaciones según el sistema operativo
        operaciones = _construir_operaciones_edicion_xml(
            ruta_archivo_xml, ruta_backup_xml,
            contenido_actualizado, encoding
        )

        planifica_ops_sis_archivos(operaciones)
        return True

    except Exception as e:
        return _mostrar_error_y_salir(f"{TEXTOS['no_cambio']}\nError: {e}\n")

def _construir_operaciones_edicion_xml(ruta_xml: str, ruta_backup: Path,
                                       contenido: str, encoding: str) -> List[Dict]:
    """ Helper para construir lista de operaciones según OS """
    if _ES_MACOS:
        return [
            {'accion': 'comando', 'comando': f"cp -p '{ruta_xml}' '{ruta_backup}'"},
            {'accion': 'escribir_archivo', 'contenido': contenido,
             'destino': str(ruta_xml), 'encoding': encoding},
            {'accion': 'comando',
             'comando': f"chmod --reference='{ruta_backup}' '{ruta_xml}' 2>/dev/null || "
                       f"chmod $(stat -f '%Mp%Lp' '{ruta_backup}') '{ruta_xml}'"}
        ]
    else:
        return [
            {'accion': 'copiar_archivo', 'origen': str(ruta_xml), 'destino': str(ruta_backup)},
            {'accion': 'escribir_archivo', 'contenido': contenido,
             'destino': str(ruta_xml), 'encoding': encoding}
        ]

def restaura_idioma_xml(ruta_carpeta: str) -> Tuple[bool, Optional[str]]:
    """
    Restaura el idioma de un programa de Adobe desde un backup

    Args:
        ruta_carpeta: Ruta donde se encuentra el archivo .bak

    Returns:
        Tuple of (success, idioma_legible)
    """
    try:
        ruta_archivo_xml = os.path.join(ruta_carpeta)
        ruta_xml = Path(ruta_archivo_xml)
        ruta_backup_xml = ruta_xml.with_suffix('.bak')

        # Chequea si el archivo .bak existe
        if not os.path.exists(ruta_backup_xml):
            muestra_contenido(
                f"{Fore.LIGHTRED_EX}{TEXTOS['no_restauro']}\n\n"
                f"{Fore.LIGHTYELLOW_EX}{TEXTOS['no_encontro_bak']}\n"
            )
            borde_inferior()
            muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
            return False, None

        # Lee el contenido del .bak para extraer el idioma
        idioma_legible = _extraer_idioma_de_backup(ruta_backup_xml)

        # Construye operaciones según OS
        operaciones = _construir_operaciones_restauracion(ruta_archivo_xml, ruta_backup_xml)

        # Planifica las operaciones
        planifica_ops_sis_archivos(operaciones)

        return True, idioma_legible

    except Exception as e:
        muestra_contenido(f"{TEXTOS['no_restauro']}\nError: {e}\n")
        borde_inferior()
        muestra_input_usuario(f"{TEXTOS['input_menu_anterior']}").strip()
        return False, None

def _extraer_idioma_de_backup(ruta_backup: Path) -> str:
    """ Helper para extraer el idioma del archivo backup """
    try:
        encoding = detecta_encoding(str(ruta_backup))
        with open(ruta_backup, 'r', encoding=encoding) as f:
            contenido_bak = f.read()

        match = re.search(TAG_IDIOMAS, contenido_bak)
        if match:
            idioma_locale = match.group(1).strip()
            # Mapeo de locales a nombres legibles
            if idioma_locale == 'en_US':
                return 'inglés'
            elif idioma_locale == 'es_ES':
                return 'español'
            else:
                return idioma_locale
    except:
        pass

    return "desconocido"

def _construir_operaciones_restauracion(ruta_xml: str, ruta_backup: Path) -> List[Dict]:
    """ Helper para construir operaciones de restauración según OS """
    operaciones = []

    if _ES_MACOS:
        # Solo elimina XML si existe
        if os.path.exists(ruta_xml):
            operaciones.append({
                'accion': 'comando',
                'comando': f"rm -f '{ruta_xml}'"
            })
        # Renombra backup .bak a .xml
        operaciones.append({
            'accion': 'comando',
            'comando': f"mv '{ruta_backup}' '{ruta_xml}'"
        })
    else: # Windows
        if os.path.exists(ruta_xml):
            operaciones.append({
                'accion': 'comando',
                'comando': f'del /F /Q "{ruta_xml}"'
            })
        operaciones.append({
            'accion': 'comando',
            'comando': f'move /Y "{ruta_backup}" "{ruta_xml}"'
        })

    return operaciones

def _construye_mapeo_localized(ruta_destino: str) -> Dict[str, str]:
    """
    Construye un mapeo de carpetas que tienen 'extensión' .localized en el destino
    Adobe lo usa en algunas carpetas en macOS

    Args:
        ruta_destino: Ruta donde se van a copiar los archivos

    Returns:
        Diccionario con mapeo nombre_original -> nombre_con_localized
    """
    mapeo = {}

    try:
        if not os.path.exists(ruta_destino):
            return mapeo

        items_destino = os.listdir(ruta_destino)
        carpetas_destino = [item for item in items_destino if os.path.isdir(os.path.join(ruta_destino, item))]
        carpetas_localized = [carpeta for carpeta in carpetas_destino if carpeta.endswith('.localized')]

        for carpeta_loc in carpetas_localized:
            nombre_base = carpeta_loc[:-10] # Quita '.localized' (10 caracteres)
            if nombre_base not in carpetas_destino:
                mapeo[nombre_base] = carpeta_loc

    except:
        pass

    return mapeo

def descomprime_zip(ruta_zip: str, ruta_unzip: str, elimina_zip: bool = False) -> bool:
    """
    Descomprime un archivo ZIP a una ruta específica, sobreescribiendo archivos y carpetas sin preguntar

    Args:
        ruta_zip: Ruta del archivo ZIP
        ruta_unzip: Ruta donde extraer
        elimina_zip: Si eliminar el ZIP después de extraer

    Returns:
        True si fue exitoso
    """
    import zipfile

    try:
        if _ES_WINDOWS:
            return _descomprime_zip_windows(ruta_zip, ruta_unzip, elimina_zip)
        else: # macOS
            return _descomprime_zip_macos(ruta_zip, ruta_unzip, elimina_zip)

    except zipfile.BadZipFile:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['zip_no_valido_1']} [{ruta_zip}] {TEXTOS['zip_no_valido_2']}\n")
        return False

    except Exception as e:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['zip_error_unzip']} {e}\n")
        return False

def _descomprime_zip_windows(ruta_zip: str, ruta_unzip: str, elimina_zip: bool) -> bool:
    """ Helper para descomprimir ZIP en Windows """
    if requiere_permisos_administrativos(str(ruta_unzip)):
        return _descomprime_zip_windows_admin(ruta_zip, ruta_unzip, elimina_zip)
    else:
        return _descomprime_zip_windows_directo(ruta_zip, ruta_unzip, elimina_zip)

def _descomprime_zip_windows_admin(ruta_zip: str, ruta_unzip: str, elimina_zip: bool) -> bool:
    """ Helper para descomprimir con permisos de admin en Windows """
    import zipfile

    carpeta_temp = tempfile.mkdtemp(prefix='simi_zip_')

    try:
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
            print(" " * PADDING_EXT + "│" + " " * (ANCHO_PANTALLA - 2) + "│")

        # Planifica copia con permisos de admin
        operaciones = [{'accion': 'crear_carpeta', 'ruta': str(ruta_unzip)}]

        for item in os.listdir(carpeta_temp):
            ruta_origen = os.path.join(carpeta_temp, item)
            if os.path.isdir(ruta_origen):
                operaciones.append({'accion': 'comando', 'comando': f'xcopy /E /I /Y "{ruta_origen}" "{os.path.join(ruta_unzip, item)}\\"'})
            else:
                operaciones.append({'accion': 'comando', 'comando': f'copy /Y "{ruta_origen}" "{os.path.join(ruta_unzip, item)}"'})

        if elimina_zip:
            operaciones.append({'accion': 'comando', 'comando': f'del "{ruta_zip}"'})

        operaciones.append({'accion': 'comando', 'comando': f'rmdir /S /Q "{carpeta_temp}"'})
        planifica_ops_sis_archivos(operaciones)
        return True

    except Exception as e:
        try:
            shutil.rmtree(carpeta_temp)
        except:
            pass
        raise e

def _descomprime_zip_windows_directo(ruta_zip: str, ruta_unzip: str, elimina_zip: bool) -> bool:
    """ Helper para descomprimir directamente en Windows (sin admin) """
    import zipfile

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

    return True

def _descomprime_zip_macos(ruta_zip: str, ruta_unzip: str, elimina_zip: bool) -> bool:
    """ Helper para descomprimir ZIP en macOS """
    import zipfile

    carpeta_temp = tempfile.mkdtemp(prefix='simi_zip_')

    try:
        with zipfile.ZipFile(ruta_zip, 'r', metadata_encoding='utf-8') as zip_ref:
            zip_ref.extractall(carpeta_temp)

        if requiere_permisos_administrativos(str(ruta_unzip)):
            return _descomprime_zip_macos_admin(carpeta_temp, ruta_unzip, ruta_zip, elimina_zip)
        else:
            return _descomprime_zip_macos_directo(carpeta_temp, ruta_unzip, ruta_zip, elimina_zip)

    except Exception as e:
        try:
            shutil.rmtree(carpeta_temp)
        except:
            pass
        raise e

def _descomprime_zip_macos_admin(carpeta_temp: str, ruta_unzip: str, ruta_zip: str, elimina_zip: bool) -> bool:
    """ Helper para descomprimir con permisos admin en macOS """
    archivos_totales = sum(len(files) for _, _, files in os.walk(carpeta_temp))

    shared_state._temp_copy_info = {
        'carpeta_temp': carpeta_temp,
        'archivos_totales': archivos_totales,
        'elimina_zip': elimina_zip,
        'ruta_zip': ruta_zip
    }

    operaciones = [{'accion': 'crear_carpeta', 'ruta': str(ruta_unzip)}]
    mapeo_localized = _construye_mapeo_localized(str(ruta_unzip))

    for item in os.listdir(carpeta_temp):
        ruta_origen = os.path.join(carpeta_temp, item)

        if os.path.isdir(ruta_origen):
            nombre_destino = mapeo_localized.get(item, item)
            ruta_destino = os.path.join(str(ruta_unzip), nombre_destino)
            operaciones.append({'accion': 'crear_carpeta', 'ruta': ruta_destino})
            operaciones.append({
                'accion': 'comando',
                'comando': f"cp -R '{ruta_origen}'/* '{ruta_destino}'/ 2>/dev/null || true"
            })
        else:
            ruta_destino = os.path.join(str(ruta_unzip), item)
            operaciones.append({
                'accion': 'comando',
                'comando': f"cp '{ruta_origen}' '{ruta_destino}'"
            })

    if elimina_zip:
        operaciones.append({'accion': 'comando', 'comando': f"rm '{ruta_zip}'"})

    operaciones.append({'accion': 'comando', 'comando': f"rm -rf '{carpeta_temp}'"})
    planifica_ops_sis_archivos(operaciones)

    return True

def _descomprime_zip_macos_directo(carpeta_temp: str, ruta_unzip: str, ruta_zip: str, elimina_zip: bool) -> bool:
    """ Helper para descomprimir directamente en macOS (sin admin) """
    archivos_totales = sum(len(files) for _, _, files in os.walk(carpeta_temp))

    if archivos_totales > 0:
        muestra_contenido(f"\n{TEXTOS['copiando_idioma']}")
        progreso = BarraProgreso(archivos_totales, modo='copia', tiempo_actualizacion=0.05)

        mapeo_localized = _construye_mapeo_localized(str(ruta_unzip))

        def copytree_con_progreso_y_localized(src, dst):
            def _procesa_carpeta(dir_origen, ruta_relativa=""):
                for item in os.listdir(dir_origen):
                    ruta_origen = os.path.join(dir_origen, item)
                    clave_mapeo = f"{ruta_relativa}/{item}" if ruta_relativa else item

                    if os.path.isdir(ruta_origen):
                        nombre_destino_relativo = mapeo_localized.get(clave_mapeo, clave_mapeo)
                        ruta_destino = os.path.join(dst, nombre_destino_relativo)
                        os.makedirs(ruta_destino, exist_ok=True)
                        _procesa_carpeta(ruta_origen, nombre_destino_relativo)
                    else:
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

    if elimina_zip:
        os.remove(ruta_zip)

    shutil.rmtree(carpeta_temp)
    print(" " * PADDING_EXT + "│" + " " * (ANCHO_PANTALLA - 2) + "│")

    return True

def descargar_archivo(url: str, auto_unzip: bool = False, ruta_unzip: Optional[str] = None,
                     ruta_destino: Optional[str] = None, ultima_version: Optional[float] = None) -> Tuple[bool, Optional[str]]:
    """
    Descarga un archivo, muestra una barra de progreso y el tamaño del archivo

    Args:
        url: URL desde donde descargar
        auto_unzip: Si descomprimir automáticamente archivos ZIP
        ruta_unzip: Ruta donde descomprimir (requerido si auto_unzip=True)
        ruta_destino: Ruta específica donde guardar
        ultima_version: Número de versión para mapeo de carpetas

    Returns:
        Tuple of (success, ruta_archivo)
    """
    import requests

    try:
        carpeta_descargas = get_carpeta_descargas()
        carpeta_simi = os.path.join(carpeta_descargas, "Simi")

        if ruta_destino:
            ruta_archivo = ruta_destino
            carpeta_base = os.path.dirname(ruta_archivo)
        else:
            ruta_archivo, carpeta_base = _construir_ruta_descarga(url, carpeta_simi, ultima_version)

        # Chequea si el archivo existe
        if os.path.exists(ruta_archivo):
            return _manejar_archivo_existente(ruta_archivo, auto_unzip, ruta_unzip)

        # Descarga el archivo
        return _descargar_archivo_nuevo(url, ruta_archivo, carpeta_base, auto_unzip, ruta_unzip)

    except requests.exceptions.RequestException as e:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_descarga']}. Error: {e}\n")
        return False, None

    except IOError as e:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_guardar_archivo']}. Error: {e}\n")
        return False, None

    except Exception as e:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_inesperado']} {e}\n")
        return False, None

def _construir_ruta_descarga(url: str, carpeta_simi: str, ultima_version: Optional[float]) -> Tuple[str, str]:
    """ Helper para construir ruta de descarga desde URL """
    parsed_url = urlparse(url)
    ruta_url = parsed_url.path
    filename = ruta_url.split('/')[-1]

    partes_ruta = [part for part in ruta_url.split('/') if part and part != filename]

    # Quita partes específicas de la URL
    partes_a_quitar = ['leandroprz', 'simi', 'raw', 'main', 'archivos-idioma', 'releases', 'download']
    partes_ruta = [part for part in partes_ruta if part.lower() not in [p.lower() for p in partes_a_quitar]]

    # Mapea carpetas
    mapeo_carpetas = {'locales': 'idiomas'}
    if ultima_version:
        mapeo_carpetas[f'v{ultima_version}'] = 'versiones'

    partes_ruta = [mapeo_carpetas.get(part.lower(), part) for part in partes_ruta]

    if partes_ruta:
        partes_str = [str(part) for part in partes_ruta]
        subcarpeta = os.path.join(*partes_str)
        carpeta_base = os.path.join(carpeta_simi, subcarpeta)
    else:
        carpeta_base = carpeta_simi

    ruta_archivo = os.path.join(carpeta_base, filename)
    return ruta_archivo, carpeta_base

def _manejar_archivo_existente(ruta_archivo: str, auto_unzip: bool, ruta_unzip: Optional[str]) -> Tuple[bool, Optional[str]]:
    """ Helper para manejar archivos existentes """
    muestra_contenido(f"{Fore.LIGHTCYAN_EX}{TEXTOS['archivo_existente']}\n[{ruta_archivo}]")

    if auto_unzip and ruta_archivo.lower().endswith('.zip'):
        if ruta_unzip is None:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['zip_parametro_requerido']}\n")
            return False, None

        descomp_exitosa = descomprime_zip(ruta_archivo, ruta_unzip, elimina_zip=False)
        if not descomp_exitosa:
            muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['descarga_no_descomprime']}\n")
            return False, None

    return True, ruta_archivo

def _descargar_archivo_nuevo(url: str, ruta_archivo: str, carpeta_base: str,
                             auto_unzip: bool, ruta_unzip: Optional[str]) -> Tuple[bool, Optional[str]]:
    """ Helper para descargar archivo nuevo """
    import requests

    try:
        os.makedirs(carpeta_base, exist_ok=True)

    except PermissionError:
        muestra_contenido(f"{Fore.LIGHTRED_EX}{TEXTOS['error_permisos_carpeta_descargas']} {carpeta_base}\n")
        return False, None

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        tamanio_total = int(r.headers.get('content-length', 0))

        muestra_contenido(f"{TEXTOS['descargando']}")
        progreso = BarraProgreso(tamanio_total, modo='descarga')

        with open(ruta_archivo, 'wb') as f:
            descargado = 0
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    descargado += len(chunk)
                    progreso.actualiza(len(chunk))

        progreso.finaliza()
        print(" " * PADDING_EXT + "│" + " " * (ANCHO_PANTALLA - 2) + "│")

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
