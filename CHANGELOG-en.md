# Changelog - Simi

## v2.8
- Fixed a bug that did no properly detect the default paths for version 2018 and 2019 for all programs (Windows and macOS)

## v2.7
- Fixed a bug that did not detect the default path for Character Animator 2026 on macOS
- Simi's interface is now available in English and Spanish
- New informational message when changing the language of Premiere Pro
- Renamed the Help menu option
- New URL to report an issue

## v2.6
- Support for Adobe 2026 versions
- Folder paths are now shown in Spanish or English based on the OS language
- Fixed a bug that showed Animate as available for version 2025
- Fixed a bug that hid Character Animator for version 2025
- Code optimization
- Fixed an issue that prevented using the numpad Enter key on macOS
- Minor cosmetic changes to the interface
- Language packages moved to the [`archivos-idioma`](https://github.com/leandroprz/Simi/tree/archivos-idioma) branch

## v2.5
- New feature to restore the language of programs previously modified with Simi

## v2.4
- Fixed an issue that allowed deleting parts of the interface
- New feature: click on a path to open the folder in the file explorer

## v2.3
- macOS support
- Can now switch from any language to English or Spanish
- Creates a backup of the application.xml file (in future versions it will be possible to revert to the backup language automatically; for now it is manual)
- New interface that looks nearly identical on both Windows and macOS (except for the font and OS window decorations)
- Folders can now be dragged and dropped (macOS only)
- Entire codebase rewritten from scratch in Python for Windows and macOS compatibility
- PowerShell version archived in the [`archive-powershell`](https://github.com/leandroprz/Simi/tree/archive-powershell) branch

## v2.2
- Improvements to Animate language packages

## v2.1
- App changes to prepare future Windows and macOS compatibility
- Improvements to Photoshop language packages

## v2.0
- Adobe 2025 compatibility
- New menu option to report a bug

## v1.9
- Option to check for new versions of Simi
- Now asks if you want to close the Adobe program before changing the language
- Improvements to Media Encoder language switching
- Visual changes

## v1.8
- Adobe 2024 compatibility
- Now works with Character Animator 2018–2024

## v1.7
- New option to specify the Adobe program installation path
- Now shows the exact size of the downloaded language file
- Cosmetic bug fixes
- Fixed a bug in the Illustrator language change

## v1.6
- Fixed an issue that caused InDesign to not work correctly (now requires an internet connection to change the language)
- Fixed a bug in the Illustrator language change
- Added support for InCopy 2018–2023 (requires internet connection)

## v1.5
- Now works with:
    - After Effects 2023, Premiere Pro 2023, Audition 2023, InDesign 2023, Media Encoder 2023, Photoshop 2023 and Animate 2023
    - Illustrator 2018–2023 (requires internet connection)
- Downloaded language files are now saved in the folder from which Simi is run

## v1.4
- Now works with Animate 2018–2022 (requires internet connection)
- Improved warning messages

## v1.3
- Now works with Photoshop 2018–2022 (requires internet connection)
- New icon
- Error and warning messages are now clearer
- PowerShell v5.1 or later is now required

## v1.2
- Now works with Adobe 2022 versions
- Fixed a bug when changing the language of Media Encoder

## v1.1
- Antivirus software should no longer flag it as a false positive
- Now supports Spanish (Spain) (es_ES), Latin American Spanish (es_MX), US English (en_US) and UK English (en_GB)
- Logic and general code optimization

## v1.0
- First public release
