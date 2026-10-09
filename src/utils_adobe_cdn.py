#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Descarga paquetes de idioma desde los servidores de Adobe para las versiones más nuevas.
Si algo falla, sigue con la descarga desde GitHub

Copyright (C) 2025 Leandro Pérez
Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles
"""

import platform
import random
import re
import shutil
import string
import zipfile
from pathlib import Path
from typing import Dict, List, Optional
from xml.etree import ElementTree as ET

# Imports Simi
from config import CONFIG_PROGRAMAS_ADOBE

# Constantes de los servidores de Adobe
_URL_PRODUCTOS = (
    'https://prod-rel-ffc-ccm.oobesaas.adobe.com/adobe-ffc-external/core/v6/products/all'
    '?_type=xml&channel=ccm&channel=sti&platform=win64,win32,osx10-64,osx10,macarm64,macuniversal&productType=Desktop'
)
_URL_APLICACION = 'https://cdn-ffc.oobesaas.adobe.com/core/v3/applications'
_TIMEOUT = 15
_TAMANIO_CHUNK = 256 * 1024

def _headers(build_guid: Optional[str] = None) -> Dict[str, str]:
    """ Headers para los servidores de Adobe """
    headers = {
        'X-Adobe-App-Id': 'accc-apps-panel-desktop',
        'User-Agent': 'Adobe Application Manager 2.0',
        'X-Api-Key': 'CC_HD_ESD_1_0',
        'Cookie': 'fg=' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=26)) + '======'
    }
    if build_guid:
        headers['x-adobe-build-guid'] = build_guid
    return headers

def _busca_producto(sap: str, prefijo_version: str, plataforma: str) -> Optional[tuple]:
    """
    Busca en el catálogo de Adobe la versión más nueva de un programa cuya versión empiece
    con prefijo_version (ej: '27.' para Photoshop 2026)

    Args:
        sap: Código SAP del programa (PHSP, AICY, IDSN, ILST, FLPR)
        prefijo_version: Prefijo de la versión mayor a buscar (ej: '27.')
        plataforma: 'win64' o 'macuniversal'/'osx10-64'

    Returns:
        Tuple (version, build_guid) o None si no se encontró (versión vieja, fuera del catálogo v6)
    """
    import requests

    respuesta = requests.get(_URL_PRODUCTOS, headers=_headers(), timeout=_TIMEOUT)
    respuesta.raise_for_status()
    raiz = ET.fromstring(respuesta.content)

    plataformas_a_probar = [plataforma]
    if platform.system() == 'Darwin':
        plataformas_a_probar.append('osx10-64' if plataforma == 'macuniversal' else 'macuniversal')

    for pf_probada in plataformas_a_probar:
        candidatos = []
        for producto in raiz.findall('channels/channel/products/product'):
            version = producto.get('version', '')
            if producto.get('id') != sap or not version.startswith(prefijo_version):
                continue

            for pf in producto.findall('platforms/platform'):
                if pf.get('id') != pf_probada:
                    continue

                language_set = pf.find('languageSet')
                if language_set is None:
                    continue

                guid = language_set.get('buildGuid')
                if guid:
                    orden = tuple(int(n) for n in re.findall(r'\d+', version))
                    candidatos.append((orden, version, guid))

        if candidatos:
            candidatos.sort()
            _, version, guid = candidatos[-1]
            return version, guid

    return None

def _paquete_de_idioma(build_guid: str, idioma: str) -> Optional[dict]:
    """
    Busca dentro de application.json el único paquete que corresponde al idioma pedido

    Returns:
        Dict con 'cdn', 'path', 'compresion' o None si no se encontró
    """
    import requests

    respuesta = requests.get(_URL_APLICACION, headers=_headers(build_guid), timeout=_TIMEOUT)
    respuesta.raise_for_status()
    app_json = respuesta.json()

    condicion = f'[installLanguage]=={idioma}'
    # El paquete de idioma siempre termina con el código de idioma en el nombre. Adobe a veces
    # incluye paquetes sidecar con la misma condition que no son el paquete de idioma
    # (paquetes que terminan en "-Roman" o "CommonLang" que no los necesitamos)
    idioma_en_nombre = re.compile(rf'-{re.escape(idioma)}(?:_x64)?$')
    paquetes = [
        p for p in app_json.get('Packages', {}).get('Package', [])
        if condicion in p.get('Condition', '')
        and idioma_en_nombre.search(p.get('PackageName', ''))
        and 'CommonLang' not in p.get('PackageName', '')
    ]

    if len(paquetes) != 1:
        return None

    cdn = app_json.get('Cdn', {}).get('Secure')
    path = paquetes[0].get('Path')
    compresion = app_json.get('CompressionType', '').strip().lower()

    if not cdn or not path:
        return None

    return {'cdn': cdn, 'path': path, 'compresion': compresion}

def _descarga_a_memoria(url: str) -> bytes:
    """ Descarga un archivo completo a memoria (los paquetes de idioma son chicos, unos pocos MB) """
    import requests

    with requests.get(url, headers=_headers(), stream=True, timeout=_TIMEOUT) as r:
        r.raise_for_status()
        partes = bytearray()
        for chunk in r.iter_content(chunk_size=_TAMANIO_CHUNK):
            partes.extend(chunk)
        return bytes(partes)

def _tamanio_diccionario(byte_prop: int) -> int:
    """ Convierte el byte de propiedades LZMA2 en tamaño de diccionario """
    if byte_prop > 40:
        raise ValueError(f"Byte de propiedades LZMA2 inválido: {byte_prop}")
    return min((2 | (byte_prop & 1)) << (byte_prop // 2 + 11), 0xFFFFFFFF)

def _descomprime_lzma2(datos: bytes) -> bytes:
    """ Descomprime un stream [1 byte de diccionario][LZMA2 crudo] """
    import lzma

    if not datos:
        return b''

    filtros = [{'id': lzma.FILTER_LZMA2, 'dict_size': _tamanio_diccionario(datos[0])}]
    return lzma.decompress(datos[1:], format=lzma.FORMAT_RAW, filters=filtros)

def _extrae_paquete(datos_zip: bytes, carpeta_destino: Path, lzma2: bool) -> None:
    """ Extrae el zip de Adobe en carpeta_destino, descomprimiendo cada archivo si lzma2=True """
    import io

    carpeta_destino = carpeta_destino.resolve()

    with zipfile.ZipFile(io.BytesIO(datos_zip), metadata_encoding='utf-8') as z:
        for info in z.infolist():
            # Adobe usa "\" en los nombres y zipfile solo lo convierte a "/" en Windows
            nombre = info.filename.replace('\\', '/')

            if nombre.endswith('/'): # Carpeta vacía: se crea igual (ej: Panels en Photoshop)
                ruta_carpeta = (carpeta_destino / nombre).resolve()
                if carpeta_destino not in ruta_carpeta.parents and ruta_carpeta != carpeta_destino:
                    raise ValueError(f"Ruta no esperada en el zip: {info.filename}")
                ruta_carpeta.mkdir(parents=True, exist_ok=True)
                continue

            ruta = (carpeta_destino / nombre).resolve()
            if carpeta_destino not in ruta.parents:
                raise ValueError(f"Ruta no esparada en el zip: {info.filename}")

            ruta.parent.mkdir(parents=True, exist_ok=True)
            contenido = z.read(info)

            if lzma2 and not nombre.lower().endswith('.pimx'):
                contenido = _descomprime_lzma2(contenido)

            ruta.write_bytes(contenido)

def _quita_localized(nombre: str) -> str:
    """ Quita el sufijo .localized que usa macOS en algunas carpetas de Adobe """
    return nombre[:-len('.localized')] if nombre.endswith('.localized') else nombre

def _reorganiza_paquete(carpeta_extraida: Path, sap: str, locale: str, lista_descarta: List[str]) -> Path:
    """
    Reorganiza el árbol ya extraído para que quede igual a los zips de idioma que están en Github
    Entra a la carpeta numérica de Adobe, descarta las carpetas intermedias que ese programa no necesita
    (lista_descarta, de config.py), y mueve el resto a la raíz

    Returns:
        Carpeta final con la estructura lista para comprimir
    """
    descarta = [p.replace('{locale}', locale) for p in lista_descarta]

    def avanza(origen: Path, partes: List[str]) -> Path:
        for parte in partes:
            if parte == '*':
                candidatos = [c for c in origen.iterdir() if c.is_dir()]
                if len(candidatos) != 1:
                    raise ValueError(f"Se esperaba una única carpeta en {origen}, se encontraron {len(candidatos)}")
                origen = candidatos[0]
            else:
                origen = origen / parte

            if not origen.exists():
                raise ValueError(f"No se encontró la ruta esperada dentro del paquete: {origen}")
        return origen

    subcarpetas = [c for c in carpeta_extraida.iterdir() if c.is_dir()]
    if len(subcarpetas) != 1:
        raise ValueError(f"Se esperaba una única carpeta numérica, se encontraron {len(subcarpetas)}")

    origen = avanza(subcarpetas[0], descarta)

    carpeta_final = carpeta_extraida.parent / f"{sap}_{locale}_final"
    if carpeta_final.exists():
        shutil.rmtree(carpeta_final)

    def mueve_arbol(src: Path, dst: Path) -> None:
        dst.mkdir(parents=True, exist_ok=True)
        for item in src.iterdir():
            destino = dst / _quita_localized(item.name)
            if item.is_dir():
                mueve_arbol(item, destino)
            else:
                destino.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item), str(destino))

    mueve_arbol(origen, carpeta_final)
    shutil.rmtree(carpeta_extraida)

    return carpeta_final

def _comprime_carpeta(carpeta: Path, ruta_zip: Path) -> None:
    """ Comprime el contenido de carpeta en ruta_zip, con los archivos en la raíz del zip """
    ruta_zip.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for ruta in sorted(carpeta.rglob('*')):
            nombre_en_zip = ruta.relative_to(carpeta).as_posix()
            if ruta.is_dir():
                if not any(ruta.iterdir()): # Conserva carpetas vacías (ej: Panels en Photoshop)
                    z.writestr(nombre_en_zip + '/', b'')
            else:
                z.write(ruta, nombre_en_zip)

def descarga_desde_adobe(programa_key: str, anio: int, locale_xml: str, ruta_zip_destino: Path) -> bool:
    """
    Descarga el paquete de idioma desde el servidor de Adobe y arma un zip en ruta_zip_destino idéntico
    a los que están en Github. Adobe solo lista en su catálogo actual (v6) las últimas dos versiones
    mayores de cada programa; para años más viejos esta función no intenta nada y devuelve False

    Args:
        programa_key: Clave del programa en CONFIG_PROGRAMAS_ADOBE (ej: 'photoshop')
        anio: Año de la versión de Adobe elegida por el usuario
        locale_xml: Código de idioma (ej: 'es_ES', 'en_US')
        ruta_zip_destino: Ruta completa donde debe quedar el zip final

    Returns:
        True si el zip quedó armado correctamente en ruta_zip_destino, False en cualquier
        otro caso (sin intentar mostrar el error: quien llama sigue con el fallback a GitHub)
    """
    config_programa = CONFIG_PROGRAMAS_ADOBE.get(programa_key, {})
    sap = config_programa.get('sap_adobe')
    if sap is None: # Programa que no necesita locale, no debería llegar acá
        return False

    major_version = config_programa.get('cdn_anio_a_major', {}).get(anio)
    if major_version is None: # Año fuera del catálogo actual de Adobe (versión vieja o inexistente)
        return False

    if platform.system() == 'Darwin' and 'cdn_descarta_darwin' in config_programa:
        lista_descarta = config_programa['cdn_descarta_darwin']
    else:
        lista_descarta = config_programa['cdn_descarta']

    carpeta_temporal = ruta_zip_destino.parent / f"_temp_{sap}_{locale_xml}"

    try:
        plataforma = 'win64' if platform.system() == 'Windows' else 'macuniversal'

        resultado = _busca_producto(sap, f"{major_version}.", plataforma)
        if resultado is None:
            return False
        _, guid = resultado

        info_paquete = _paquete_de_idioma(guid, locale_xml)
        if info_paquete is None:
            return False

        datos_zip = _descarga_a_memoria(info_paquete['cdn'] + info_paquete['path'])

        if carpeta_temporal.exists():
            shutil.rmtree(carpeta_temporal)
        carpeta_temporal.mkdir(parents=True, exist_ok=True)

        _extrae_paquete(datos_zip, carpeta_temporal, lzma2=(info_paquete['compresion'] == 'zip-lzma2'))
        carpeta_final = _reorganiza_paquete(carpeta_temporal, sap, locale_xml, lista_descarta)
        _comprime_carpeta(carpeta_final, ruta_zip_destino)
        shutil.rmtree(carpeta_final, ignore_errors=True)

        return ruta_zip_destino.exists()

    except Exception:
        return False

    finally:
        if carpeta_temporal.exists():
            shutil.rmtree(carpeta_temporal, ignore_errors=True)
