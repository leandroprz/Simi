#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mensajes y texto de la interfaz de Simi

Copyright (C) 2025 Leandro Pérez
Este proyecto está bajo la Licencia GPLv2 - ver LICENSE para más detalles
"""

TEXTOS = {
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
    'menu_ayuda': 'Ayuda',
    'menu_reportar_error': 'Reportar un error',
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

    # ZIP
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
    'error_inesperado': 'Error inesperado:',
    'restauro_correctamente_1': 'El idioma se restauró correctamente al',
    'restauro_correctamente_2': 'usando la copia de seguridad en la ruta:',
    'restaura_ps': 'Podés volver al idioma anterior desde Photoshop, ingresando al menú Editar > Preferencias > Interfaz > Idioma de la interfaz.\nReiniciá Photoshop para ver los cambios.',

    # Connectividad y descarga
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

    # Misc
    'de': 'de',
    'barra_progreso_modo1': 'Modo no soportado:',
    'barra_progreso_modo2': 'Usá descarga, unzip o copia.',
    'error_ruta_descargas': 'No se pudo obtener la ruta de la carpeta Descargas.',
    'no_soportado': 'Sistema no soportado',
    'error_en_script': 'Error en el script:'
}
