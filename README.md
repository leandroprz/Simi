# Simi - Cambiá el idioma de Adobe sin reinstalar los programas

<p align="center">
    <a href=".github\simi-win-1.jpg" target="_blank"><img src=".github\simi-win-1.jpg" width="45%"></img></a> <a href=".github\simi-mac-1.png" target="_blank"><img src=".github\simi-mac-1.png" width="45%"></img></a>
</p>

[![Última versión](https://img.shields.io/github/v/release/leandroprz/Simi?color=998f68&label=Última%20Versión&style=for-the-badge)](https://github.com/leandroprz/Simi/releases/latest) [![Plataforma](https://img.shields.io/badge/Plataforma-Windows%20&amp;%20macOS-6f628a?style=for-the-badge)](#) [![Language](https://img.shields.io/badge/Language-English%20&amp;%20Spanish-8a6f62?style=for-the-badge)](/README-en.md) [![Python](https://img.shields.io/badge/Python-v3.8+-687d99?style=for-the-badge)](#) [![Licencia](https://img.shields.io/badge/Licencia-GPL%20v2-628a6f?style=for-the-badge)](/LICENSE) [![Descargas](https://img.shields.io/github/downloads/leandroprz/simi/total?style=for-the-badge&label=Descargas&color=cc8959)](#)


## ¿Qué es Simi?
Esta herramienta nace a partir de la necesidad de cambiar rápidamente los idiomas de los diferentes programas de Adobe sin tener que reinstalarlos. Hace un tiempo hice [un tutorial donde expliqué](https://leandroperez.art/blog/cambia-el-idioma-de-los-programas-de-adobe-sin-reinstalarlos/) cómo cambiar los idiomas editando unos archivos de texto, pero era un poco engorroso y sobre todo molesto si son como yo, que necesitan cambiar constantemente el idioma de inglés a español o viceversa.

---

## Cómo usar Simi

### Versión compilada (Windows y macOS)
[Hacé click aquí](https://github.com/leandroprz/Simi/releases/latest) para abrir la página de releases y descargá la última versión disponible para tu sistema operativo. Elegí el archivo que termina en `.exe` si usás Windows o el que termina en `.dmg` si usas macOS.

### Versión sin compilar (Windows)
1. Descargá y descomprimí el código
2. Hacé doble click en `Simi.bat`
   - Se instalarán las dependencias automáticamente (solo la primera vez)
   - Luego se abrirá Simi

### Versión sin compilar (macOS)
1. Descargá y descomprimí el código
2. Hacé doble click en `Simi.command` (click derecho → Abrir si es necesario)
   - Se instalarán las dependencias automáticamente (solo la primera vez)
   - Luego se abrirá Simi

## Compatibilidad
- Windows 10+ (x64)
- macOS 10.13+ (sólo lo probé en Intel, pero debería funcionar en Apple Silicon)

---

## Características
- No hace falta reinstalar los programas de Adobe para cambiar el idioma
- Compatible con programas de Adobe 2018-2026
- Soporte para Windows y macOS
- Interfaz simple con rutas clickeables
- Drag & drop de carpetas
- Backup automático de paquetes de idioma
- Soporte para español e inglés

### Programas soportados
- After Effects
- Premiere Pro
- Audition
- InDesign
- Media Encoder
- Photoshop
- Illustrator
- InCopy
- Character Animator
- Animate

---

## Estructura del proyecto
```
simi/
├── src/
│   ├── config.py              # Configuración
│   ├── i18n.py                # Internacionalización
│   ├── idiomas_adobe.py       # Lógica de cambio de idioma
│   ├── interfaz.py            # Componentes de UI
│   ├── main.py                # Script principal con menús
│   ├── permisos_admin.py      # Gestión de permisos
│   ├── resource_helper.py     # Helpers de recursos para PyInstaller
│   ├── shared_state.py        # Estado compartido entre módulos
│   ├── simi.py                # Muestra la GUI con styling y todas las funcionalidades
│   ├── traduccion_rutas.py    # Traducción de rutas
│   ├── utils_adobe.py         # Utilidades de programas de Adobe
│   ├── utils_app.py           # Utilidades de la app Simi
│   └── utils_archivos.py      # Manejo de archivos
├── assets/                    # Íconos y fondos
│   ├── dmg_background.png
│   ├── dmg_icon.icns
│   ├── icono_mac.icns
│   └── icono_win.ico
├── Simi.bat                   # Launcher para Windows
├── Simi.command               # Launcher para macOS
├── requirements.txt           # Dependencias Python
└── version.txt                # Archivo para chequear nuevas versiones
```

---

## Para desarrolladores

### Requisitos
- Python 3.8+
- pip
- ~50MB de espacio para las dependencias

### Dependencias Python
- colorama
- requests
- psutil
- tkinterdnd2

Todas se instalan automáticamente con `Simi.bat` / `Simi.command`

### Configuración de entorno dev
```bash
# 1. Cloná el repositorio
git clone https://github.com/leandroprz/Simi.git
cd Simi

# 2. Opcional - Creá y activá un entorno virtual
python -m venv simi-venv # Windows/macOS
simi-venv\Scripts\activate # Windows
source simi-venv/bin/activate # macOS

# 3. Instalá las dependencias
pip install -r requirements.txt # Windows
pip3 install -r requirements.txt # macOS

# 4. Ejecutá el script
python simi.py # Windows (abrir como admin)
python3 simi.py # macOS
```

### Compilar con PyInstaller
Creá un archivo `.spec` con el contenido que está más abajo (según tu plataforma), guardalo en la carpeta `/simi` y luego en una consola:

```bash
# Windows
pip install pyinstaller
pyinstaller simi.spec --clean

# macOS
pip3 install pyinstaller
pyinstaller simi.spec --clean
```

Después encontrarás el archivo compilado dentro de la carpeta `/dist`.

### Archivos .spec para PyInstaller

<details>
<summary>simi.spec Windows</summary>
<pre>
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src\\simi.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'config', 'main', 'i18n', 'idiomas_adobe', 'interfaz', 'permisos_admin', 'resource_helper', 'shared_state', 'simi', 'traduccion_rutas', 'utils_adobe', 'utils_app', 'utils_archivos', 'platform', 'os', 'sys', 'psutil', 'webbrowser', 'requests', 'subprocess', 'shutil', 'zipfile', 'ctypes', 'xml.etree.ElementTree', 'colorama', 'textwrap', 'pathlib', 'typing', 'urllib.parse', 're', 'runpy', 'time', 'tkinter', 'threading', 'queue', 'plistlib', 'uuid', 'tempfile', 'tkinterdnd2'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Simi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\icono_win.ico'],
    uac_admin=True,
)
</pre>
</details>

<details>
<summary>simi.spec macOS</summary>
<pre>
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src/simi.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'config', 'main', 'i18n', 'idiomas_adobe', 'interfaz', 'permisos_admin', 'resource_helper', 'shared_state', 'simi', 'traduccion_rutas', 'utils_adobe', 'utils_app', 'utils_archivos', 'platform', 'os', 'sys', 'psutil', 'webbrowser', 'requests', 'subprocess', 'shutil', 'zipfile', 'ctypes', 'xml.etree.ElementTree', 'colorama', 'textwrap', 'pathlib', 'typing', 'urllib.parse', 're', 'runpy', 'time', 'tkinter', 'threading', 'queue', 'plistlib', 'uuid', 'tempfile', 'tkinterdnd2'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Simi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icono_mac.icns',
)

app = BUNDLE(
    exe,
    name='Simi.app',
    icon='assets/icono_mac.icns',
    bundle_identifier=None,
    info_plist={
        'NSHighResolutionCapable': True,
    },
)
</pre>
</details>

Por algún motivo al usar `pyinstaller` con argumentos directamente desde la consola, la app no se compila correctamente y no tengo idea a qué se debe. Por ahí yo soy el inútil, o tal vez PyInstaller es el mañoso :P

Al compilar en macOS, a veces la app aparece en el Dock, luego desaparece, pero finalmente vuelve a aparecer y se ve la ventana de Simi.

[Más info sobre cómo usar PyInstaller aquí](https://pyinstaller.org/en/stable/usage.html).

---

## ToDo y known issues
- Optimizar la ejecución de la app compilada con PyInstaller. A mi gusto demora mucho en abrir (probé otras alternativas, ninguna entrega un único ejecutable)
- Drag and drop no funciona en Windows
- Seguro me olvido de algo

---

## Disclaimer

Los paquetes de idioma que se usan en este programa pertenecen a Adobe y sus respectivos propietarios.

Este software solo facilita su gestión y se proporcionan únicamente con fines educativos.

---

## Acerca de Simi

[![Mirá el video en YouTube](https://img.youtube.com/vi/jVJ8n9s3CZQ/maxresdefault.jpg)](https://youtu.be/jVJ8n9s3CZQ)
[Mirá el video en YouTube](https://youtu.be/jVJ8n9s3CZQ)

### Licencia
Este proyecto está bajo la Licencia GPLv2. Ver `LICENSE` para más detalles.

### Autor
Leandro Pérez
- Website: [leandroperez.art](https://leandroperez.art)
- GitHub: [@leandroprz](https://github.com/leandroprz)
- YouTube: [@leandroprz](https://www.youtube.com/@leandroprz)

### Apoyá el proyecto
Si Simi te fue de utilidad, no olvides:
- Darle una ⭐ en GitHub
- Compartirlo con otros
- [Reportar bugs o sugerir features](https://github.com/leandroprz/Simi/issues)
- [Hacer una donación](https://leandroperez.art/colaboraciones/)
