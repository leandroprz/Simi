#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mensajes y texto de la interfaz de Simi en español e inglés

Copyright (C) 2025 Leandro Pérez
Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles
"""

_TEXTOS_ES = {
    # Input
    'input_ruta': 'Tipeá la ruta y presioná Enter:',
    'input_opcion': 'Elegí una opción y presioná Enter:',
    'input_error_menu': 'Elegí una opción del menú:',
    'input_error_sn': 'Ingresá S o N:',
    'input_continuar': 'Presioná Enter para continuar:',
    'ruta_instalacion': 'Ingresá la ruta donde instalaste el programa o presioná Enter para usar la ruta por defecto:',
    'input_menu_anterior': 'Presioná Enter para volver al menú anterior:',

    # Menú
    'menu_principal': 'Menú principal',
    'menu_cambio_espanol': 'Cambiar programas al español',
    'menu_cambio_ingles': 'Cambiar programas al inglés',
    'menu_buscar_version': 'Buscar nueva versión de Simi',
    'menu_restaurar_xml': 'Restaurar idioma',
    'menu_usando_bak': 'usando backup de Simi',
    'menu_ayuda': 'Ayuda y tutorial',
    'menu_reportar_error': 'Reportar un error',
    'menu_cambiar_idioma_simi': 'Cambiar idioma de Simi',
    'menu_salir': 'Salir',

    # Procesos ejecutándose
    'programa_abierto': 'está abierto! Es recomendable cerrarlo antes de cambiar el idioma.',
    'intento_cierre_app': 'Se intentará cambiar el idioma sin cerrar el programa, pero es posible que no se cambie correctamente.\nDeberás reiniciar el programa manualmente para ver el nuevo idioma.',
    'error_cierre': 'Ocurrió un error al intentar cerrar',
    'queres_cerrar': '¿Querés cerrarlo? (S/n):',

    # Admin/sudo
    'permisos_admin_requeridos': 'Error. Se requieren permisos de Administrador/root para descomprimir en la ruta:',
    'ejecutar_como_admin': 'Debes abrir Simi como Administrador.',
    'ejecutar_con_sudo': 'Debes abrir Simi usando sudo.',
    'no_puede_escribir': 'Error. No se pudo escribir en la ruta:',
    'ejecutar_admin_sudo': 'Abrí Simi con permisos de Administrador/root.',
    'cerrar_app': 'Cerrar',
    'cerrar_app_requiere_permisos': 'Se requieren permisos de Administrador para cerrar',
    'cerrar_app_error_permisos': 'No se pudieron obtener permisos para cerrar',
    'no_se_detectaron_permisos': 'No tenés permisos de Administrador.',
    'error_ejecutar_comando': 'Error al ejecutar el comando:',
    'error_operacion': 'Error al ejecutar la operación:',
    'error_permisos_carpeta_descargas': 'Error de permisos al crear la carpeta de descarga:',

    # Permisos admin macOS
    'macos_osascript_error1': 'Error en el script de autenticación.',
    'macos_osascript_cancelado': 'Operación cancelada por el usuario.',
    'macos_osascript_error2': 'Error de autenticación:',
    'macos_osascript_timeout': 'Timeout al pedir permisos de administrador.',
    'macos_osascript_error3': 'Error al pedir permisos administrativos:',
    'macos_osascript_error_ejecutar': 'Error al ejecutar las operaciones de cambio de idioma:',
    'macos_osascript_timeout2': 'Timeout al ejecutar las operaciones de cambio de idioma.',
    'permisos_insuficientes': 'No tenés permisos suficientes para realizar la operación:',

    # Zip
    'no_pudo_descomprimir': 'No se pudo descomprimir',
    'zip_error_descomprimir': 'Error al descomprimir el archivo',
    'zip_no_valido_1': 'Error. El archivo',
    'zip_no_valido_2': 'no es un paquete de idioma válido.',
    'zip_permiso_denegado': 'Error. No hay suficientes permisos para descomprimir en la ruta:',
    'copia_permiso_denegado': 'Error. No hay suficientes permisos para copiar a la ruta:',
    'zip_error_unzip': 'Ocurrió un error al descomprimir el paquete de idioma:',
    'zip_parametro_requerido': 'Error. Tenés que agregar el parámetro ruta_unzip cuando uses auto_unzip=True.',
    'zip_error_copia': 'Error al intentar copiar el paquete de idioma:',
    'descarga_no_descomprime': 'No se pudo descomprimir el paquete de idioma.',

    # Cambio idioma
    'copiando_idioma': 'Copiando archivos de idioma...',
    'idioma_cambio_exitoso_1': 'El idioma se cambió al',
    'idioma_cambio_exitoso_2': 'correctamente en la ruta:',
    'idioma_backup_1': 'Se hizo una copia de seguridad en la ruta:',
    'idioma_backup_2': 'Vas a necesitar ese archivo si algo malió sal.',
    'no_cambio': '¡No se pudo cambiar el idioma!',
    'razones': 'Puede ser por diferentes razones:\n• El programa no está instalado en la ruta que ingresaste\n• La versión que elegiste no está instalada en tu computadora\n• Simi no encontró el archivo application.xml en la ruta que ingresaste\n• El programa no se instaló usando la aplicación Adobe Creative Cloud',
    'no_restauro': '¡No se pudo restaurar el idioma!',
    'razones_bak': 'Puede ser por diferentes razones:\n• El programa no está instalado en la ruta que ingresaste\n• La versión que elegiste no está instalada en tu computadora\n• Simi no encontró el archivo application.bak en la ruta que ingresaste',
    'no_encontro_bak': 'No se encontró la copia de seguridad de Simi (application.bak)',
    'cambiar_idioma': 'Cambiar idioma de',
    'al': 'al',
    'cambiar_a': 'Cambiar a',
    'cambiar_programas': 'Cambiar programas al',
    'cambio_ps': 'Podés elegir el nuevo idioma desde Photoshop, ingresando al menú Editar > Preferencias > Interfaz > Idioma de la interfaz.\nReiniciá Photoshop para ver los cambios.',
    'cambio_ppro': 'Si no ves el nuevo idioma, probá cerrando y abriendo nuevamente Premiere Pro. Al reiniciarlo por segunda vez deberías ver el idioma cambiado.',
    'error_inesperado': 'Error inesperado:',
    'restauro_correctamente_1': 'El idioma se restauró correctamente al',
    'restauro_correctamente_2': 'usando la copia de seguridad en la ruta:',
    'restaura_ps': 'Podés volver al idioma anterior desde Photoshop, ingresando al menú Editar > Preferencias > Interfaz > Idioma de la interfaz.\nReiniciá Photoshop para ver los cambios.',

    # Conectividad y descarga
    'archivo_existente': 'Se usará el archivo que se descargó previamente en la ruta:',
    'descargando': 'Descargando archivo...',
    'descarga_a_medias_1': 'Hubo un problema con la descarga.',
    'descarga_a_medias_2': 'Se descargaron',
    'descarga_a_medias_3': 'pero deberían haberse descargado',
    'descarga_exitosa': 'El archivo se descargó correctamente en la ruta:',
    'error_descarga_idioma': 'No se pudo descargar correctamente el paquete de idioma.',
    'error_descarga': 'No se pudo descargar el archivo.',
    'error_guardar_archivo': 'No se pudo guardar el archivo.',
    'no_pudo_chequear_version': 'No se pudo comprobar la última versión.',
    'titulo_version_update_1': 'Buscando nueva versión...',
    'titulo_version_update_2': 'Descargando nueva versión',
    'nueva_v_disponible': '¡Hay una nueva versión disponible!:',
    'desea_descargar': '¿Querés descargarla? (S/n):',
    'desea_abrir': '¿Querés abrir la nueva versión? (S/n):',
    'no_descargo': 'No se pudo descargar la nueva versión.',
    'usando_ultima_version': 'Ya tenés la última versión:',
    'version_actual_1': 'La versión que estás usando',
    'version_actual_2': 'es más nueva que la última versión disponible para descargar:',

    # Simi
    'simi_titulo': 'Simi by Leandro Pérez',
    'simi_descripcion': 'Cambiá el idioma de Adobe sin reinstalar los programas',
    'agradecimiento': 'Gracias por usar Simi.',
    'mensaje_resenia': '¡No olvides dejarnos una reseña en www.leandroperez.art!',
    'mensaje_url_ayuda': 'En breve se abrirá la página de ayuda.',
    'mensaje_reportar_error': 'En breve se abrirá la página para reportar un error.',
    'aviso_importante_1': 'Aviso importante',
    'aviso_importante_2': 'Los paquetes de idioma que se usan en este programa pertenecen a Adobe y sus respectivos propietarios.',
    'aviso_importante_3': 'Este software solo facilita su gestión y se proporcionan únicamente con fines educativos.',
    'idioma_cambiado': 'El idioma de Simi se cambió al',
    'idioma_espanol': 'Español',
    'idioma_ingles': 'Inglés',

    # Misc
    'de': 'de',
    'barra_progreso_modo1': 'Modo no soportado:',
    'barra_progreso_modo2': 'Usá descarga, unzip o copia.',
    'error_ruta_descargas': 'No se pudo obtener la ruta de la carpeta Descargas.',
    'no_soportado': 'Sistema no soportado',
    'error_en_script': 'Error en el script:'
}

_TEXTOS_EN = {
    # Input
    'input_ruta': 'Type the path and press Enter:',
    'input_opcion': 'Choose an option and press Enter:',
    'input_error_menu': 'Choose an option from the menu:',
    'input_error_sn': 'Enter Y or N:',
    'input_continuar': 'Press Enter to continue:',
    'ruta_instalacion': 'Enter the path where you installed the program or press Enter to use the default path:',
    'input_menu_anterior': 'Press Enter to go back to the previous menu:',

    # Menu
    'menu_principal': 'Main menu',
    'menu_cambio_espanol': 'Change programs to Spanish',
    'menu_cambio_ingles': 'Change programs to English',
    'menu_buscar_version': 'Check for a new version of Simi',
    'menu_restaurar_xml': 'Restore language',
    'menu_usando_bak': 'using Simi backup',
    'menu_ayuda': 'Help and tutorial',
    'menu_reportar_error': 'Report a bug',
    'menu_cambiar_idioma_simi': 'Change Simi language',
    'menu_salir': 'Exit',

    # Running processes
    'programa_abierto': 'is running! It is recommended to close it before changing the language.',
    'intento_cierre_app': 'Simi will try to change the language without closing the program, but it may not change correctly.\nYou will need to restart the program manually to see the new language.',
    'error_cierre': 'An error occurred while trying to close',
    'queres_cerrar': 'Do you want to close it? (Y/n):',

    # Admin/sudo
    'permisos_admin_requeridos': 'Error. Administrator/root permissions are required to extract to the path:',
    'ejecutar_como_admin': 'You must open Simi as Administrator.',
    'ejecutar_con_sudo': 'You must open Simi using sudo.',
    'no_puede_escribir': 'Error. Could not write to the path:',
    'ejecutar_admin_sudo': 'Open Simi with Administrator/root permissions.',
    'cerrar_app': 'Close',
    'cerrar_app_requiere_permisos': 'Administrator permissions are required to close',
    'cerrar_app_error_permisos': 'Could not obtain permissions to close',
    'no_se_detectaron_permisos': 'You do not have Administrator permissions.',
    'error_ejecutar_comando': 'Error executing command:',
    'error_operacion': 'Error executing operation:',
    'error_permisos_carpeta_descargas': 'Permission error creating download folder:',

    # macOS admin permissions
    'macos_osascript_error1': 'Error in authentication script.',
    'macos_osascript_cancelado': 'Operation cancelled by user.',
    'macos_osascript_error2': 'Authentication error:',
    'macos_osascript_timeout': 'Timeout requesting administrator permissions.',
    'macos_osascript_error3': 'Error requesting administrative permissions:',
    'macos_osascript_error_ejecutar': 'Error executing language change operations:',
    'macos_osascript_timeout2': 'Timeout executing language change operations.',
    'permisos_insuficientes': 'You do not have sufficient permissions to perform the operation:',

    # Zip
    'no_pudo_descomprimir': 'Could not extract',
    'zip_error_descomprimir': 'Error extracting file',
    'zip_no_valido_1': 'Error. The file',
    'zip_no_valido_2': 'is not a valid language package.',
    'zip_permiso_denegado': 'Error. Insufficient permissions to extract to the path:',
    'copia_permiso_denegado': 'Error. Insufficient permissions to copy to the path:',
    'zip_error_unzip': 'An error occurred while extracting the language package:',
    'zip_parametro_requerido': 'Error. You must add the ruta_unzip parameter when using auto_unzip=True.',
    'zip_error_copia': 'Error trying to copy the language package:',
    'descarga_no_descomprime': 'Could not extract the language package.',

    # Language change
    'copiando_idioma': 'Copying language files...',
    'idioma_cambio_exitoso_1': 'The language was successfully changed to',
    'idioma_cambio_exitoso_2': 'at the path:',
    'idioma_backup_1': 'A backup was created at the path:',
    'idioma_backup_2': "You'll need that file if something went wrong.",
    'no_cambio': 'An error occurred while changing the language!',
    'razones': 'This may be due to different reasons:\n• The program is not installed at the path you entered\n• The version you chose is not installed on your computer\n• Simi could not find the application.xml file at the path you entered\n• The program was not installed using the Adobe Creative Cloud application',
    'no_restauro': 'An error occurred while restoring the language!',
    'razones_bak': 'This may be due to different reasons:\n• The program is not installed at the path you entered\n• The version you chose is not installed on your computer\n• Simi could not find the application.bak file at the path you entered',
    'no_encontro_bak': "Simi's backup file was not found (application.bak)",
    'cambiar_idioma': 'Change the language of',
    'al': 'to',
    'cambiar_a': 'Change to',
    'cambiar_programas': 'Change programs to',
    'cambio_ps': 'You can choose the new language from Photoshop by going to Edit > Preferences > Interface > UI Language.\nRestart Photoshop to see the changes.',
    'cambio_ppro': "If you don't see the new language, try closing and reopening Premiere Pro. On the second restart you should see the language changed.",
    'error_inesperado': 'Unexpected error:',
    'restauro_correctamente_1': 'The language was successfully restored to',
    'restauro_correctamente_2': 'using the backup at the path:',
    'restaura_ps': 'You can revert to the previous language from Photoshop by going to Edit > Preferences > Interface > UI Language.\nRestart Photoshop to see the changes.',

    # Connectivity and download
    'archivo_existente': 'Using the previously downloaded file at the path:',
    'descargando': 'Downloading file...',
    'descarga_a_medias_1': 'There was a problem with the download.',
    'descarga_a_medias_2': 'Downloaded',
    'descarga_a_medias_3': 'but should have downloaded',
    'descarga_exitosa': 'The file was downloaded successfully at the path:',
    'error_descarga_idioma': 'Could not download the language package correctly.',
    'error_descarga': 'Could not download the file.',
    'error_guardar_archivo': 'Could not save the file.',
    'no_pudo_chequear_version': 'Could not check for the latest version.',
    'titulo_version_update_1': 'Checking for a new version...',
    'titulo_version_update_2': 'Downloading new version',
    'nueva_v_disponible': 'A new version is available!:',
    'desea_descargar': 'Do you want to download it? (Y/n):',
    'desea_abrir': 'Do you want to open the new version? (Y/n):',
    'no_descargo': 'Could not download the new version.',
    'usando_ultima_version': 'You already have the latest version:',
    'version_actual_1': 'The version you are using',
    'version_actual_2': 'is newer than the latest available version for download:',

    # Simi
    'simi_titulo': 'Simi by Leandro Pérez',
    'simi_descripcion': 'Change the language of Adobe apps without reinstalling them',
    'agradecimiento': 'Thanks for using Simi.',
    'mensaje_resenia': "Don't forget to leave us a review at www.leandroperez.art!",
    'mensaje_url_ayuda': 'The help page will open shortly.',
    'mensaje_reportar_error': 'The bug report page will open shortly.',
    'aviso_importante_1': 'Important notice',
    'aviso_importante_2': 'The language packages used in this program belong to Adobe and their respective owners.',
    'aviso_importante_3': 'This software facilitates their management and is provided for educational purposes only.',
    'idioma_cambiado': 'Simi language changed to',
    'idioma_espanol': 'Spanish',
    'idioma_ingles': 'English',

    # Misc
    'de': 'of',
    'barra_progreso_modo1': 'Unsupported mode:',
    'barra_progreso_modo2': 'Use download, unzip or copy.',
    'error_ruta_descargas': 'Could not get the Downloads folder path.',
    'no_soportado': 'Unsupported system',
    'error_en_script': 'Error in script:'
}

# Diccionario para modificar las strings
TEXTOS = dict(_TEXTOS_ES)
