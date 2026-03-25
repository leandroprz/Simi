#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuración general de Simi

Copyright (C) 2025 Leandro Pérez
Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles
"""

# Constantes Simi
VERSION_ACTUAL_SIMI = "2.7"
NOMBRE_RELEASE = "Simi_v"

# URLs locales, releases, etc
URLS = {
    'url_locales_win': 'https://github.com/leandroprz/Simi/raw/archivos-idioma/locales/win',
    'url_locales_mac': 'https://github.com/leandroprz/Simi/raw/archivos-idioma/locales/mac',
    'latest_vcheck': 'https://github.com/leandroprz/Simi/raw/main/version.txt',
    'url_releases': 'https://github.com/leandroprz/Simi/releases/download',
    'url_ayuda_tienda': 'https://leandroperez.art/tienda/productos-gratuitos/simi-cambia-idioma-adobe-sin-reinstalar/',
    'url_reportar_error': 'https://github.com/leandroprz/Simi/issues/new'
}

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
        'necesita_locale': True, # Sí descarga zip
        'locale_code': 'ind' # Parte de la URL de descarga
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
        'solo_locale': True # Solo descarga locale, no modifica XML
    },
    'animate': {
        'nombre': 'Animate',
        'ruta_macos': 'animate',
        'xml_paths': {
            'Windows': 'AMT/application.xml',
            'Darwin': 'App/Contents/Resources/AMT/application.xml'
        },
        'necesita_locale': True,
        'locale_code': 'ani'
    },
    'illustrator': {
        'nombre': 'Illustrator',
        'ruta_macos': 'illustrator',
        'xml_paths': {
            'Windows': 'Support Files/Contents/Windows/AMT/application.xml',
            'Darwin': 'Support Files/AMT/AI/AMT/application.xml'
        },
        'necesita_locale': True,
        'locale_code': 'il'
    },
    'incopy': {
        'nombre': 'InCopy',
        'ruta_macos': 'incopy',
        'xml_paths': {
            'Windows': 'AMT/application.xml',
            'Darwin': 'Resources/AMT/IC/AMT/application.xml'
        },
        'necesita_locale': True,
        'locale_code': 'inc'
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
        2018: '15.0',
        2019: '16.0',
        2020: '17.0',
        2021: '18.0',
        2022: '22.0',
        2023: '23.0',
        2024: '24.0',
        2025: '25.0',
        2026: '26.0'
    },
    'audition': {
        2018: '11.0',
        2019: '12.0',
        2020: '13.0',
        2021: '14.0',
        2022: '22.0',
        2023: '23.0',
        2024: '24.0',
        2025: '25.0',
        2026: '26.0'
    },
    'character_animator': {
        2018: '1.1',
        2019: '2.0',
        2020: '3.0',
        2021: '4.0',
        2022: '22.0',
        2023: '23.0',
        2024: '24.0',
        2025: '25.0',
        2026: '26.0'
    },
    'media_encoder': {
        2018: '12.0',
        2019: '13.0',
        2020: '14.0',
        2021: '15.0',
        2022: '22.0',
        2023: '23.0',
        2024: '24.0',
        2025: '25.0',
        2026: '26.0'
    },
    'premiere_pro': {
        2018: '12.0',
        2019: '13.0',
        2020: '14.0',
        2021: '15.0',
        2022: '22.0',
        2023: '23.0',
        2024: '24.0',
        2025: '25.0',
        2026: '26.0'
    }
}

# Rutas de instalación por defecto en macOS
RUTAS_ADOBE_MACOS = {
    # Programas con ruta default en "/Library/Application Support" (usan la versión en el nombre de la carpeta donde está el XML)
    'after_effects': {
        'ruta_default': '/Library/Application Support/Adobe/After Effects',
        'usa_version': True
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
        'usa_version': True
    },
    'premiere_pro': {
        'ruta_default': '/Library/Application Support/Adobe/Premiere Pro',
        'usa_version': True
    },

    # Programas con ruta default en "/Applications" (usan el año en el nombre de la carpeta)
    'animate': {
        'ruta_default': '/Applications/Adobe Animate',
        'usa_version': False
    },
    'illustrator': {
        'ruta_default': '/Applications/Adobe Illustrator',
        'usa_version': False
    },
    'incopy': {
        'ruta_default': '/Applications/Adobe InCopy',
        'usa_version': False
    },
    'indesign': {
        'ruta_default': '/Applications/Adobe InDesign',
        'usa_version': False
    },
    'photoshop': {
        'ruta_default': '/Applications/Adobe Photoshop',
        'usa_version': False
    }
}

# Constante idiomas
TAG_IDIOMAS = r'<Data key="installedLanguages">([^<]*)<\/Data>'
