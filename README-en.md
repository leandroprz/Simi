# Simi - Change the language of Adobe apps without reinstalling them

<p align="center">
    <a href=".github\simi-win-1.jpg" target="_blank"><img src=".github\simi-win-1.jpg" width="45%"></img></a> <a href=".github\simi-mac-1.png" target="_blank"><img src=".github\simi-mac-1.png" width="45%"></img></a>
</p>

[![Latest version](https://img.shields.io/github/v/release/leandroprz/Simi?color=998f68&label=Latest%20Version&style=for-the-badge)](https://github.com/leandroprz/Simi/releases/latest) [![Platform](https://img.shields.io/badge/Platform-Windows%20&amp;%20macOS-6f628a?style=for-the-badge)](#) [![Idioma](https://img.shields.io/badge/Idioma-Español%20e%20Inglés-8a6f62?style=for-the-badge)](/README.md) [![Python](https://img.shields.io/badge/Python-v3.8+-687d99?style=for-the-badge)](#) [![License](https://img.shields.io/badge/License-GPL%20v2-628a6f?style=for-the-badge)](/LICENSE) [![Downloads](https://img.shields.io/github/downloads/leandroprz/simi/total?style=for-the-badge&label=Downloads&color=cc8959)](#)

## What is Simi?
This tool was born out of the need to quickly switch the language of different Adobe programs without having to reinstall them. A while back I wrote [a tutorial explaining](https://leandroperez.art/blog/cambia-el-idioma-de-los-programas-de-adobe-sin-reinstalarlos/) how to change languages by editing some text files, but it was a bit cumbersome — especially if you're like me and constantly need to switch back and forth between English and Spanish.

---

## How to use Simi

### Compiled version (Windows and macOS)
[Click here](https://github.com/leandroprz/Simi/releases/latest) to open the releases page and download the latest version for your operating system. Choose the file ending in `.exe` for Windows or `.dmg` for macOS.

### Uncompiled version (Windows)
1. Download and extract the code
2. Double-click `Simi.bat`
   - Dependencies will be installed automatically (first run only)
   - Simi will then open

### Uncompiled version (macOS)
1. Download and extract the code
2. Double-click `Simi.command` (right-click → Open if needed)
   - Dependencies will be installed automatically (first run only)
   - Simi will then open

## Compatibility
- Windows 10+ (x64)
- macOS 10.13+ (only tested on Intel, but should work on Apple Silicon)

---

## Features
- No need to reinstall Adobe programs to change the language
- Compatible with Adobe 2018–2026
- Windows and macOS support
- Simple interface with clickable paths
- Drag & drop folder support
- Automatic backup of language packages
- Interface available in Spanish and English (auto-detected from OS language)
- Spanish and English support

### Supported programs
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

## Project structure
```
simi/
├── src/
│   ├── config.py              # Configuration
│   ├── i18n.py                # Internationalization
│   ├── idiomas_adobe.py       # Language change logic
│   ├── interfaz.py            # UI components
│   ├── main.py                # Main script with menus
│   ├── permisos_admin.py      # Permission management
│   ├── resource_helper.py     # Resource helpers for PyInstaller
│   ├── shared_state.py        # Shared state between modules
│   ├── simi.py                # GUI with styling and all features
│   ├── traduccion_rutas.py    # Path translation
│   ├── utils_adobe.py         # Adobe program utilities
│   ├── utils_app.py           # Simi app utilities
│   └── utils_archivos.py      # File management
├── assets/                    # Icons and backgrounds
│   ├── dmg_background.png
│   ├── dmg_icon.icns
│   ├── icono_mac.icns
│   └── icono_win.ico
├── Simi.bat                   # Windows launcher
├── Simi.command               # macOS launcher
├── requirements.txt           # Python dependencies
└── version.txt                # File for checking new versions
```

---

## For developers

### Requirements
- Python 3.8+
- pip
- ~50MB of space for dependencies

### Python dependencies
- colorama
- requests
- psutil
- tkinterdnd2

All installed automatically via `Simi.bat` / `Simi.command`

### Dev environment setup
```bash
# 1. Clone the repository
git clone https://github.com/leandroprz/Simi.git
cd Simi

# 2. Optional - Create and activate a virtual environment
python -m venv simi-venv  # Windows/macOS
simi-venv\Scripts\activate  # Windows
source simi-venv/bin/activate  # macOS

# 3. Install dependencies
pip install -r requirements.txt   # Windows
pip3 install -r requirements.txt  # macOS

# 4. Run the script
python simi.py   # Windows (run as admin)
python3 simi.py  # macOS
```

### Building with PyInstaller
Create a `.spec` file with the content below (according to your platform), save it in the `/simi` folder, then run in a terminal:

```bash
# Windows
pip install pyinstaller
pyinstaller simi.spec --clean

# macOS
pip3 install pyinstaller
pyinstaller simi.spec --clean
```

The compiled file will be inside the `/dist` folder.

### PyInstaller .spec files

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

For some reason, building with `pyinstaller` arguments directly from the terminal doesn't compile correctly and I have no idea why. Maybe I'm the one doing it wrong, or maybe PyInstaller is just being difficult :P

When building on macOS, sometimes the app appears in the Dock, then disappears, but eventually comes back and the Simi window shows up.

[More info on how to use PyInstaller here](https://pyinstaller.org/en/stable/usage.html).

---

## ToDo and known issues
- Optimize startup time of the PyInstaller compiled app (tried other alternatives, none produce a single executable)
- Drag and drop doesn't work on Windows
- Probably forgetting something

---

## Disclaimer

The language packages used in this program belong to Adobe and their respective owners.

This software only facilitates their management and is provided for educational purposes only.

---

## About Simi

[![Watch the video on YouTube](https://img.youtube.com/vi/jVJ8n9s3CZQ/maxresdefault.jpg)](https://youtu.be/jVJ8n9s3CZQ)
[Watch the video on YouTube](https://youtu.be/jVJ8n9s3CZQ)

### License
This project is licensed under GPLv2. See `LICENSE` for more details.

### Author
Leandro Pérez
- Website: [leandroperez.art](https://leandroperez.art)
- GitHub: [@leandroprz](https://github.com/leandroprz)
- YouTube: [@leandroprz](https://www.youtube.com/@leandroprz)

### Support the project
If Simi was useful to you, don't forget to:
- Give it a ⭐ on GitHub
- Share it with others
- [Report bugs or suggest features](https://github.com/leandroprz/Simi/issues)
- [Make a donation](https://leandroperez.art/colaboraciones/)
