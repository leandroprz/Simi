#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuración general de Simi

Copyright (C) 2025 Leandro Pérez
Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles
"""

import os

# Constantes Simi
VERSION_ACTUAL_SIMI = "3.1"
NOMBRE_RELEASE = "Simi_v"

# URLs locales, releases, etc
URLS = {
    'url_locales_win': 'https://github.com/leandroprz/Simi/raw/archivos-idioma/locales/win',
    'url_locales_mac': 'https://github.com/leandroprz/Simi/raw/archivos-idioma/locales/mac',
    'latest_vcheck': 'https://github.com/leandroprz/Simi/raw/main/version.txt',
    'url_releases': 'https://github.com/leandroprz/Simi/releases/download',
    'url_ayuda_tienda': 'https://leandroperez.art/tienda/productos-gratuitos/simi-cambia-idioma-adobe-sin-reinstalar/',
    'url_reportar_error': 'https://github.com/leandroprz/Simi/issues'
}

# Carpeta común de Adobe: no depende de dónde se instaló cada programa
RUTAS_COMUN_ADOBE = {
    'Windows': os.path.join(os.environ.get('PROGRAMDATA', 'C:\\ProgramData'), 'Adobe'),
    'Darwin': '/Library/Application Support/Adobe'
}

# Carpeta dentro de los paquetes de idioma obtenidos del servidor de Adobe
CARPETA_DATOS_COMPARTIDOS = 'SharedApplicationData'

# Comentarios que se agregan a los zips de idioma guardados en la carpeta Downloads
COMENTARIO_ZIP_OFICIAL = b'Source: official'
COMENTARIO_ZIP_FALLBACK = b'Source: fallback'

# Programas de Adobe
CONFIG_PROGRAMAS_ADOBE = {
    'after_effects': {
        'nombre': 'After Effects',
        'ruta_macos': 'after_effects',
        'xml_paths': {
            'Windows': 'Support Files/AMT/application.xml',
            'Darwin': 'AMT/application.xml'
        },
        'necesita_locale': False # No descarga zip
    },
    'premiere_pro': {
        'nombre': 'Premiere Pro',
        'ruta_macos': 'premiere_pro',
        'xml_paths': {
            'Windows': 'AMT/application.xml',
            'Darwin': 'AMT/application.xml'
        },
        'necesita_locale': False
    },
    'audition': {
        'nombre': 'Audition',
        'ruta_macos': 'audition',
        'xml_paths': {
            'Windows': 'AMT/application.xml',
            'Darwin': 'AMT/application.xml'
        },
        'necesita_locale': False
    },
    'indesign': {
        'nombre': 'InDesign',
        'ruta_macos': 'indesign',
        'xml_paths': {
            'Windows': 'AMT/application.xml',
            'Darwin': 'Resources/AMT/ID/AMT/application.xml'
        },
        'necesita_locale': True,
        'locale_code': 'ind', # Parte de la URL de descarga
        'sap_adobe': 'IDSN', # Código SAP de Adobe
        'cdn_descarta': ['*', 'INSTALLDIR'], # Descarta carpetas - Ver utils_adobe_cdn.py
        'cdn_conserva': ['*', CARPETA_DATOS_COMPARTIDOS], # Carpetas que se conservan en el zip
        'carpeta_comun_adobe': 'InDesign', # Carpeta dentro de RUTAS_COMUN_ADOBE
        'macos_renombra_en_us': {
            # Año: carpetas (relativas a la instalación) que contienen una carpeta en_US
            2027: [
                'Presets/InDesign Shortcut Sets'
            ]
        },
        'cdn_anio_a_major': {2018: 13, 2019: 14, 2020: 15, 2021: 16, 2022: 17, 2023: 18, 2024: 19, 2025: 20, 2026: 21, 2027: 22}
    },
    'media_encoder': {
        'nombre': 'Media Encoder',
        'ruta_macos': 'media_encoder',
        'xml_paths': {
            'Windows': 'AMT/application.xml',
            'Darwin': 'AMT/application.xml'
        },
        'necesita_locale': False
    },
    'photoshop': {
        'nombre': 'Photoshop',
        'ruta_macos': 'photoshop',
        'xml_paths': {}, # No modifica XML
        'necesita_locale': True,
        'locale_code': 'ps',
        'solo_locale': True, # Solo descarga locale, no modifica XML
        'sap_adobe': 'PHSP',
        'cdn_descarta': [], # En Windows no hay nada que descartar
        'cdn_descarta_darwin': ['Application'], # En macOS hay una carpeta "Application" extra antes de "Locales"
        'cdn_anio_a_major': {2018: 19, 2019: 20, 2020: 21, 2021: 22, 2022: 23, 2023: 24, 2024: 25, 2025: 26, 2026: 27, 2027: 28}
    },
    'animate': {
        'nombre': 'Animate',
        'ruta_macos': 'animate',
        'xml_paths': {
            'Windows': 'AMT/application.xml',
            'Darwin': 'App/Contents/Resources/AMT/application.xml'
        },
        'necesita_locale': True,
        'locale_code': 'ani',
        'sap_adobe': 'FLPR',
        'cdn_descarta': ['{locale}', 'AppFiles'], # {locale} se reemplaza por el código de idioma (es_ES, en_US)
        'cdn_anio_a_major': {2018: 18, 2019: 19, 2020: 20, 2021: 21, 2022: 22, 2023: 23, 2024: 24, 2027: 27} # Sin 2025/2026
    },
    'illustrator': {
        'nombre': 'Illustrator',
        'ruta_macos': 'illustrator',
        'xml_paths': {
            'Windows': 'Support Files/Contents/Windows/AMT/application.xml',
            'Darwin': 'Support Files/AMT/AI/AMT/application.xml'
        },
        'necesita_locale': True,
        'locale_code': 'il',
        'sap_adobe': 'ILST',
        'cdn_descarta': ['*', 'Application'],
        'cdn_anio_a_major': {2018: 22, 2019: 23, 2020: 24, 2021: 25, 2022: 26, 2023: 27, 2024: 28, 2025: 29, 2026: 30, 2027: 31}
    },
    'incopy': {
        'nombre': 'InCopy',
        'ruta_macos': 'incopy',
        'xml_paths': {
            'Windows': 'AMT/application.xml',
            'Darwin': 'Resources/AMT/IC/AMT/application.xml'
        },
        'necesita_locale': True,
        'locale_code': 'inc',
        'sap_adobe': 'AICY',
        'cdn_descarta': ['*', 'INSTALLDIR'],
        'cdn_conserva': ['*', CARPETA_DATOS_COMPARTIDOS],
        'carpeta_comun_adobe': 'InCopy',
        'macos_renombra_en_us': {
            2027: [
                'Presets/InCopy Shortcut Sets'
            ]
        },
        'cdn_anio_a_major': {2018: 13, 2019: 14, 2020: 15, 2021: 16, 2022: 17, 2023: 18, 2024: 19, 2025: 20, 2026: 21, 2027: 22}
    },
    'character_animator': {
        'nombre': 'Character Animator',
        'ruta_macos': 'character_animator',
        'xml_paths': {
            'Windows': 'Support Files/AMT/application.xml',
            'Darwin': 'AMT/application.xml'
        },
        'necesita_locale': False
    }
}

# Versiones de los programas de Adobe según el año ya que en macOS se usa la versión de la app (major release) en lugar del año para la ruta del archivo XML
# Nota: en el 2022 Adobe unificó todas las versiones según el año (por lo menos para las apps aquí listadas)
VERSIONES_ADOBE_MACOS = {
    'after_effects': {
        2018: '15.0', 2019: '16.0', 2020: '17.0', 2021: '18.0', 2022: '22.0',
        2023: '23.0', 2024: '24.0', 2025: '25.0', 2026: '26.0', 2027: '27.0'
    },
    'audition': {
        2018: '11.0', 2019: '12.0', 2020: '13.0', 2021: '14.0', 2022: '22.0',
        2023: '23.0', 2024: '24.0', 2025: '25.0', 2026: '26.0', 2027: '27.0'
    },
    'character_animator': {
        2018: '1.1', 2019: '2.0', 2020: '3.0', 2021: '4.0', 2022: '22.0',
        2023: '23.0', 2024: '24.0', 2025: '25.0', 2026: '26.0' # Sin versión 2027 por ahora
        },
    'media_encoder': {
        2018: '12.0', 2019: '13.0', 2020: '14.0', 2021: '15.0', 2022: '22.0',
        2023: '23.0', 2024: '24.0', 2025: '25.0', 2026: '26.0', 2027: '27.0'
        },
    'premiere_pro': {
        2018: '12.0', 2019: '13.0', 2020: '14.0', 2021: '15.0', 2022: '22.0',
        2023: '23.0', 2024: '24.0', 2025: '25.0', 2026: '26.0', 2027: '27.0'
    }
}

# Rutas de instalación por defecto en macOS
RUTAS_ADOBE_MACOS = {
    # Programas con ruta default en "/Library/Application Support" (usan el número de versión en el nombre de la carpeta donde está el XML)
    # cc_versions: versiones que usan "Adobe <nombre> CC <year>" en lugar del número de versión en el nombre de la carpeta
    # override_paths: rutas completas por defecto para versiones con un formato completamente distinto según el año
    'after_effects': {
        'ruta_default': '/Library/Application Support/Adobe/After Effects',
        'usa_version': True,
        'override_paths': {
            2018: '/Library/Application Support/Adobe/Adobe After Effects CC 2018'
        }
    },
    'audition': {
        'ruta_default': '/Library/Application Support/Adobe/Audition',
        'usa_version': True
    },
    'character_animator': {
        'ruta_default': '/Library/Application Support/Adobe/Character Animator',
        'usa_version': True
    },
    'media_encoder': {
        'ruta_default': '/Library/Application Support/Adobe/Media Encoder',
        'usa_version': True,
        'override_paths': {
            2018: '/Library/Application Support/Adobe/AdobeMediaEncoder/12.0'
        }
    },
    'premiere_pro': {
        'ruta_default': '/Library/Application Support/Adobe/Premiere Pro',
        'usa_version': True,
        'override_paths': {
            2018: '/Library/Application Support/Adobe/PremierePro/12.0'
        }
    },

    # Programas con ruta default en "/Applications" (usan el año en el nombre de la carpeta)
    # cc_versions: versiones que incluyen "CC" en el nombre de la carpeta
    'animate': {
        'ruta_default': '/Applications/Adobe Animate',
        'usa_version': False,
        'cc_versions': [2018, 2019]
    },
    'illustrator': {
        'ruta_default': '/Applications/Adobe Illustrator',
        'usa_version': False,
        'cc_versions': [2018, 2019]
    },
    'incopy': {
        'ruta_default': '/Applications/Adobe InCopy',
        'usa_version': False,
        'cc_versions': [2018, 2019]
    },
    'indesign': {
        'ruta_default': '/Applications/Adobe InDesign',
        'usa_version': False,
        'cc_versions': [2018, 2019]
    },
    'photoshop': {
        'ruta_default': '/Applications/Adobe Photoshop',
        'usa_version': False,
        'cc_versions': [2018, 2019]
    }
}

# Constante idiomas
TAG_IDIOMAS = r'<Data key="installedLanguages">([^<]*)<\/Data>'
