# Changelog - Simi

## v2.7
- Solucionado un error que no detectaba la ruta por defecto de Character Animator 2026 en macOS
- La interfaz de Simi ahora está disponible en inglés y español
- Nuevo mensaje informativo al cambiar el idioma de Premiere Pro
- Se cambió el nombre del menú Ayuda
- Nueva URL para reportar un error

## v2.6
- Soporte para las versiones 2026 de los programas de Adobe
- Ahora las rutas de las carpetas se muestran en español o inglés, según el idioma del sistema operativo
- Se corrigió un error que mostraba Animate disponible para la versión 2025
- Se corrigió un error que ocultaba Character Animator para la versión 2025
- Optimización del código
- Se solucionó un problema que impedía usar la tecla Enter del teclado numérico en macOS
- Pequeños cambios cosméticos en la interfaz
- Se movieron los paquetes de idioma a la rama [`archivos-idioma`](https://github.com/leandroprz/Simi/tree/archivos-idioma)

## v2.5
- Nueva función para restaurar el idioma de los programas si fueron modificados con Simi

## v2.4
- Solucionado un problema que permitía borrar parte de la interfaz
- Nueva función que permite hacer click en una ruta para abrir la carpeta en el explorador de archivos

## v2.3
- Soporte para macOS
- Ahora se puede cambiar de cualquier idioma a inglés o español
- Crea una copia de seguridad del archivo application.xml (en próximas versiones se podrá volver al idioma del backup automáticamente, por ahora es manual)
- Nueva interfaz que debería verse prácticamente igual tanto en Windows como en macOS (salvo por la tipografía y el decorado de las ventanas del sistema operativo)
- Ahora se puede arrastrar y soltar la ruta de una carpeta (sólo en macOS)
- Se escribió todo el código desde cero en Python para hacer la app compatible con Windows y macOS
- Se archivó la versión en PowerShell en la rama [`archive-powershell`](https://github.com/leandroprz/Simi/tree/archive-powershell)

## v2.2
- Mejoras en los paquetes de idioma de Animate

## v2.1
- Cambios en la app para que en próximas versiones sea compatible con Windows y macOS
- Mejoras en los paquetes de idioma de Photoshop

## v2.0
- Compatibilidad con Adobe 2025
- Nueva opción en el menú para reportar un error

## v1.9
- Opción para buscar nuevas versiones de Simi
- Antes de cambiar el idioma pregunta si se desea cerrar el programa de Adobe
- Mejoras en el cambio de idioma para Media Encoder
- Cambios cosméticos

## v1.8
- Compatibilidad con Adobe 2024
- Ahora funciona con Character Animator 2018-2024

## v1.7
- Nueva opción para indicar la ruta donde se instaló el programa de Adobe
- Ahora muestra en pantalla el tamaño exacto del archivo de idioma descargado de Internet
- Corrección de errores cosméticos
- Corrige un error en el cambio de idioma de Illustrator

## v1.6
- Corrige un problema que hacía que InDesign funcione incorrectamente (ahora requiere conexión a Internet para cambiar el idioma)
- Corrige un error en el cambio de idioma de Illustrator
- Agrega soporte para InCopy 2018-2023 (requiere conexión a Internet)

## v1.5
- Ahora funciona con:
    - After Effects 2023, Premiere Pro 2023, Audition 2023, InDesign 2023, Media Encoder 2023, Photoshop 2023 y Animate 2023
    - Illustrator 2018-2023 (requiere conexión a Internet)
- A partir de ahora los idiomas descargados quedan guardados en la carpeta desde donde se ejecuta la aplicación Simi

## v1.4
- Ahora funciona con Animate 2018-2022 (requiere conexión a Internet)
- Mejora en los mensajes de alerta

## v1.3
- Ahora funciona con Photoshop 2018-2022 (requiere conexión a Internet)
- Nuevo ícono
- Los mensajes de error y alerta ahora son más claros de entender
- A partir de ahora es necesario tener instalado PowerShell v5.1 o superior para que Simi funcione correctamente

## v1.2
- Ahora funciona con la versión 2022 de los programas de Adobe
- Corrige un error al cambiar el idioma de Media Encoder

## v1.1
- Los antivirus ya no deberían detectarlo como un falso positivo
- Ahora funciona con español de España (es_ES), español Latinoamericano (es_MX), inglés de Estados Unidos (en_US) e inglés del Reino Unido (en_GB)
- Cambios en la lógica de programacion y optimización del código en general

## v1.0
- Primera versión pública
