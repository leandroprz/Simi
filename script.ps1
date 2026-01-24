# Simi v2.0
# Cambiá el idioma de los programas de Adobe sin reinstalarlos
# https://leandroperez.art/tienda/productos-gratuitos/simi-cambia-idioma-adobe-sin-reinstalar/
# © Leandro Pérez

# Versión mínima requerida de PowerShell
#Requires -Version 5.1

# Variables GitHub
$script:VersionActualSimi = "2.0"
$script:NombreRelease = "Simi_Leandro_Perez_v"
$script:UltimaVersionTxt

# Cambia nombre del título de la ventana
$host.ui.rawui.WindowTitle = "Simi v$VersionActualSimi"

# Variables versiones y paths
$script:VersionAdobe
$script:FreezeOpcionMenu
$script:RutaInstalCustom
$script:RutaInstalIngresada
$script:RutaInstalacion
$script:RutaInstalAdobe = "$Env:Programfiles\Adobe"

# Variables idiomas
$script:tagIdiomas = '<Data key="installedLanguages">(.*?)</Data>'
$script:XmlEnUs = '<Data key="installedLanguages">en_US</Data>'
$script:XmlEnGb = '<Data key="installedLanguages">en_GB</Data>'
$script:XmlEsEs = '<Data key="installedLanguages">es_ES</Data>'
$script:XmlEsMx = '<Data key="installedLanguages">es_MX</Data>'
$script:LocaleEnUs = 'en_US'
$script:LocaleEnGb = 'en_GB'
$script:LocaleEsEs = 'es_ES'
$script:LocaleEsMx = 'es_MX'

# Locales y releases
$script:UrlLocales = "https://github.com/leandroprz/Simi/raw/main/locales"
$script:UrlUltimaVersionWin = "https://github.com/leandroprz/Simi/raw/main/vcheck/latest-win.txt"
$script:UrlReleases = "https://github.com/leandroprz/Simi/raw/main/bin"
#$script:UrlLocales = "https://lp.local/simi" **DEBUG**

# Variables mensajes
$script:CambioEngSpa = "`n Se cambió el idioma de inglés a español correctamente en la ruta:`n"
$script:CambioSpaEng = "`n Se cambió el idioma de español a inglés correctamente en la ruta:`n"
$script:NoCambio = "`n ¡No se pudo cambiar el idioma!"
$script:Cambiando = "`n Instalando idioma..."
$script:Razones = "`n Puede ser por diferentes razones:
 - El programa de Adobe no está instalado en la ruta que elegiste
 - El programa de Adobe no se instaló usando la aplicación Adobe Creative Cloud
 - La versión de Adobe que elegiste no está instalada en tu computadora
 - Ya tenés instalado el idioma seleccionado"
$script:CambioPs = "`n`n Podés elegir el nuevo idioma desde el menú Editar > Preferencias > Interfaz en Photoshop"
$script:ErrorCambioPs = "`n Ya tenés instalado el idioma seleccionado. Lo podés cambiar desde el menú Editar > Preferencias > Interfaz en Photoshop"
$script:ErrorCambioYaInstalado = " - Ya tenés instalado el idioma seleccionado"
$script:Descargando = "`n Descargando archivo..."
$script:SinConexion = "`n No es posible conectarse a la página de descarga del archivo. Intentando nuevamente en 5s..."
$script:SimiDesc = "`n`n Simi v$VersionActualSimi - © Leandro Pérez`n Cambiá el idioma de Adobe sin reinstalar los programas"
$script:BuscandoVersion = "`n Buscando nueva versión..."
$script:NuevaVDisponible = " ¡Hay una nueva versión disponible!"
$script:DeseaDescargar = "`n ¿Querés descargarla? (S/N)"
$script:DescargaCorrecta = " La nueva versión se descargó correctamente."
$script:DeseaAbrir = "`n ¿Querés abrirla? (S/N)"
$script:NoDescargo = "`n No se pudo descargar la nueva versión. Intentalo nuevamente."
$script:UsandoUltimaVersion = "`n Ya tenés la última versión"
$script:MensajeResenia = "`n`n Gracias por usar Simi.`n ¡No olvides dejarnos una reseña en www.leandroperez.art!`n"
$script:MensajeUrlAyuda = "`n Gracias por usar Simi.`n En breve se abrirá la página de ayuda."
$script:UrlAyudaTienda = "https://leandroperez.art/tienda/productos-gratuitos/simi-cambia-idioma-adobe-sin-reinstalar/"
$script:MensajeRepError = "`n Gracias por usar Simi.`n En breve se abrirá la página para reportar un error."
$script:UrlReportarError = "https://leandroperez.art/contacto/?tu-motivo=Otro"

# Fix for $PSScriptRoot when converting to exe (https://stackoverflow.com/a/60122064/5204005)
$script:ScriptDir = if (-not $PSScriptRoot) {
    Split-Path -Parent (Convert-Path ([environment]::GetCommandLineArgs()[0]))
    } else {
        $PSScriptRoot
    }

# Limpia Consola
function Limpia-Pantalla {
    [System.Console]::Clear()
}

# Menú con opciones
function Menu ($MenuNumero, $MenuCierra, $NombreMenu, $NombreFuncionMenu, $OpcionMenu1, $MenuFuncion1, $OpcionMenu2, $MenuFuncion2, $OpcionMenu3, $MenuFuncion3, $OpcionMenu4, $MenuFuncion4, $OpcionMenu5, $MenuFuncion5, $OpcionMenu6, $MenuFuncion6, $OpcionMenu7, $MenuFuncion7, $OpcionMenu8, $MenuFuncion8, $OpcionMenu9, $MenuFuncion9, $OpcionMenu10, $MenuFuncion10, $OpcionMenu11, $MenuFuncion11, $OpcionMenu12, $MenuFuncion12, $OpcionMenu13, $MenuFuncion13, $OpcionMenu14, $MenuFuncion14) {

    Write-Host $SimiDesc -Fore DarkGray
    Write-Host "`n$NombreMenu`n" -Fore Gray

    if ($OpcionMenu1 -ne $null) { Write-Host " $OpcionMenu1" -Fore Gray }
    if ($OpcionMenu2 -ne $null) { Write-Host " $OpcionMenu2" -Fore Gray }
    if ($OpcionMenu3 -ne $null) { Write-Host " $OpcionMenu3" -Fore Gray }
    if ($OpcionMenu4 -ne $null) { Write-Host " $OpcionMenu4" -Fore Gray }
    if ($OpcionMenu5 -ne $null) { Write-Host " $OpcionMenu5" -Fore Gray }
    if ($OpcionMenu6 -ne $null) { Write-Host " $OpcionMenu6" -Fore Gray }
    if ($OpcionMenu7 -ne $null) { Write-Host " $OpcionMenu7" -Fore Gray }
    if ($OpcionMenu8 -ne $null) { Write-Host " $OpcionMenu8" -Fore Gray }
    if ($OpcionMenu9 -ne $null) { Write-Host " $OpcionMenu9" -Fore Gray }
    if ($OpcionMenu10 -ne $null) { Write-Host " $OpcionMenu10" -Fore Gray }
    if ($OpcionMenu11 -ne $null) { Write-Host " $OpcionMenu11" -Fore Gray }
    if ($OpcionMenu12 -ne $null) { Write-Host " $OpcionMenu12" -Fore Gray }
    if ($OpcionMenu13 -ne $null) { Write-Host " $OpcionMenu13" -Fore Gray }
    if ($OpcionMenu14 -ne $null) { Write-Host " $OpcionMenu14" -Fore Gray }
    
    [int]$OpcionMenu = Read-Host -Prompt "`n Tipeá una opción y presioná Enter"
    # Clear-Host
    Limpia-Pantalla
        
    if ( ($OpcionMenu -lt $MenuNumero) -or ($OpcionMenu -gt $MenuCierra) ) {
        Write-Host "`n Tipeá una opción del menú (en números)." -Fore Red
        #Start-Sleep -Seconds 1
        Invoke-Expression $NombreFuncionMenu
    } else {
        if ($OpcionMenu -eq $MenuNumero) { Invoke-Expression $MenuFuncion1 }
        if ( $OpcionMenu -eq ($MenuNumero + "1") ) { Invoke-Expression $MenuFuncion2 }
        if ( $OpcionMenu -eq ($MenuNumero + "2") ) { Invoke-Expression $MenuFuncion3 }   
        if ( $OpcionMenu -eq ($MenuNumero + "3") ) { Invoke-Expression $MenuFuncion4 } 
        if ( $OpcionMenu -eq ($MenuNumero + "4") ) { Invoke-Expression $MenuFuncion5 } 
        if ( $OpcionMenu -eq ($MenuNumero + "5") ) { Invoke-Expression $MenuFuncion6 } 
        if ( $OpcionMenu -eq ($MenuNumero + "6") ) { Invoke-Expression $MenuFuncion7 } 
        if ( $OpcionMenu -eq ($MenuNumero + "7") ) { Invoke-Expression $MenuFuncion8 }
        if ( $OpcionMenu -eq ($MenuNumero + "8") ) { Invoke-Expression $MenuFuncion9 } 
        if ( $OpcionMenu -eq ($MenuNumero + "9") ) { Invoke-Expression $MenuFuncion10 }
        if ( $OpcionMenu -eq ($MenuNumero + "10") ) { Invoke-Expression $MenuFuncion11 }
        if ( $OpcionMenu -eq ($MenuNumero + "11") ) { Invoke-Expression $MenuFuncion12 }
        if ( $OpcionMenu -eq ($MenuNumero + "12") ) { Invoke-Expression $MenuFuncion13 }
        if ( $OpcionMenu -eq ($MenuNumero + "13") ) { Invoke-Expression $MenuFuncion14 }
    }
}

# Menú principal, muestra idiomas
function MENU_PRINCIPAL {
    Menu 1 6 "`n Menú principal`n --------------" MENU_PRINCIPAL `
        "[1] Cambiar de inglés a español" MENU_ENG_A_SPA_PRINCIPAL `
        "[2] Cambiar de español a inglés" MENU_SPA_A_ENG_PRINCIPAL `
        "[3] Buscar nueva versión de Simi" MENU_UPDATE `
        "[4] Ayuda" MENU_AYUDA `
        "[5] Reportar un error" MENU_REPORTAR_ERROR `
        "[6] Salir" MENU_SALIR
}

# Menú inglés a español
function MENU_ENG_A_SPA_PRINCIPAL {
    Menu 1 12 "`n Cambiar de inglés a español`n ---------------------------" MENU_ENG_A_SPA_PRINCIPAL `
        " [1] Adobe 2025" MENU_ADOBE_ENG_A_SPA `
        " [2] Adobe 2024" MENU_ADOBE_ENG_A_SPA `
        " [3] Adobe 2023" MENU_ADOBE_ENG_A_SPA `
        " [4] Adobe 2022" MENU_ADOBE_ENG_A_SPA `
        " [5] Adobe 2021" MENU_ADOBE_ENG_A_SPA `
        " [6] Adobe 2020" MENU_ADOBE_ENG_A_SPA `
        " [7] Adobe 2019" MENU_ADOBE_ENG_A_SPA `
        " [8] Adobe 2018" MENU_ADOBE_ENG_A_SPA `
        " [9] Menú principal" MENU_PRINCIPAL `
        "[10] Ayuda" MENU_AYUDA `
        "[11] Reportar un error" MENU_REPORTAR_ERROR `
        "[12] Salir" MENU_SALIR `
}

# Menú español a inglés
function MENU_SPA_A_ENG_PRINCIPAL {
    Menu 1 12 "`n Cambiar de español a inglés`n ---------------------------" MENU_SPA_A_ENG_PRINCIPAL `
        " [1] Adobe 2025" MENU_ADOBE_SPA_A_ENG `
        " [2] Adobe 2024" MENU_ADOBE_SPA_A_ENG `
        " [3] Adobe 2023" MENU_ADOBE_SPA_A_ENG `
        " [4] Adobe 2022" MENU_ADOBE_SPA_A_ENG `
        " [5] Adobe 2021" MENU_ADOBE_SPA_A_ENG `
        " [6] Adobe 2020" MENU_ADOBE_SPA_A_ENG `
        " [7] Adobe 2019" MENU_ADOBE_SPA_A_ENG `
        " [8] Adobe 2018" MENU_ADOBE_SPA_A_ENG `
        " [9] Menú principal" MENU_PRINCIPAL `
        "[10] Ayuda" MENU_AYUDA `
        "[11] Reportar un error" MENU_REPORTAR_ERROR `
        "[12] Salir" MENU_SALIR
}

# Chequea si hay conexión a Internet
function Verifica-Conexion {
    while ( !(Test-Connection -computer google.com -count 1 -quiet) ) {
        Write-Host $SinConexion -Fore Red
        Start-Sleep -Seconds 5
    }
}

# Get tamaño archivo de descarga (https://chat.openai.com/chat/75b0de7b-17a3-47bd-9e60-d1639e8c8b58)
function TAMANIO_DESCARGA {
    param([string]$Url)

    $Bytes = (Invoke-WebRequest $Url -Method Head).Headers.'Content-Length'
    if ($Bytes -ge 500000) {
        $Tamanio = $Bytes / 1MB
        $TamanioFormateado = "{0:F2} MB" -f $Tamanio
    } else {
        $Tamanio = $Bytes / 1KB
        $TamanioFormateado = "{0:F2} KB" -f $Tamanio
    }
    #Write-Host "Tamaño de la descarga: $TamanioFormateado"
    Write-Host $Descargando "($TamanioFormateado)" -Fore Yellow
}

# Permite elegir ruta de instalación del programa de Adobe (https://chat.openai.com/chat/461fff1a-71df-425f-9627-a87caa072b90)
function RUTA_INSTALACION {

    #Write-Host $SimiDesc"`n" -Fore DarkGray
    if ( ![string]::IsNullOrWhiteSpace($RutaInstalCustom) ) {
        $RutaInstalIngresada = $RutaInstalCustom.TrimEnd('\')
    } else {
        $RutaInstalCustom = Read-Host "`n Ingresá la ruta donde instalaste el programa`n o presioná Enter para usar la ruta por defecto [$Env:Programfiles\Adobe]"
        if ( ![string]::IsNullOrWhiteSpace($RutaInstalCustom) ) {
            $RutaInstalIngresada = $RutaInstalCustom.TrimEnd('\')
            #Write-Host "`n Se usará la ruta ingresada [$RutaInstalIngresada]." -Fore Yellow
        } else {
            $RutaInstalIngresada = "$Env:Programfiles\Adobe"
            #Write-Host "`n Se usará la ruta por defecto [$RutaInstalIngresada]." -Fore Yellow
        }
    }

    Limpia-Pantalla
    return $RutaInstalIngresada
}

# Menú Adobe inglés a español
function MENU_ADOBE_ENG_A_SPA {

    switch ($OpcionMenu) {
        1 { $VersionAdobe = 2025
            $FreezeOpcionMenu = 1
            break
        }
        2 { $VersionAdobe = 2024
            $FreezeOpcionMenu = 2
            break
        }
        3 { $VersionAdobe = 2023
            $FreezeOpcionMenu = 3
            break
        }
        4 { $VersionAdobe = 2022
            $FreezeOpcionMenu = 4
            break
        }
        5 { $VersionAdobe = 2021
            $FreezeOpcionMenu = 5
            break
        }
        6 { $VersionAdobe = 2020
            $FreezeOpcionMenu = 6
            break
        }
        7 { $VersionAdobe = 2019
            $FreezeOpcionMenu = 7
            break
        }
        8 { $VersionAdobe = 2018
            $FreezeOpcionMenu = 8
            break
        }
        default {
            $VersionAdobe = 2025
            $FreezeOpcionMenu = 1
        }
    }
    #Write-Host "usuario tipeó" $VersionAdobe "**DEBUG**" -Fore Red;

    if ($VersionAdobe -eq 2025) {
    
        Menu 1 13 "`n Adobe $VersionAdobe - Inglés a español`n -----------------------------" MENU_ADOBE_ENG_A_SPA `
            " [1] After Effects" MENU_AE_ENG_A_SPA `
            " [2] Premiere Pro" MENU_PPRO_ENG_A_SPA `
            " [3] Audition" MENU_AUDI_ENG_A_SPA `
            " [4] InDesign" MENU_IND_ENG_A_SPA `
            " [5] Media Encoder" MENU_ME_ENG_A_SPA `
            " [6] Photoshop" MENU_PS_ENG_A_SPA `
            " [7] Illustrator" MENU_ILU_ENG_A_SPA `
            " [8] InCopy" MENU_INC_ENG_A_SPA `
            " [9] Character Animator" MENU_CA_ENG_A_SPA `
            "[10] Menú principal" MENU_PRINCIPAL `
            "[11] Ayuda" MENU_AYUDA `
            "[12] Reportar un error" MENU_REPORTAR_ERROR `
            "[13] Salir" MENU_SALIR
    
    } else {

        Menu 1 14 "`n Adobe $VersionAdobe - Inglés a español`n -----------------------------" MENU_ADOBE_ENG_A_SPA `
            " [1] After Effects" MENU_AE_ENG_A_SPA `
            " [2] Premiere Pro" MENU_PPRO_ENG_A_SPA `
            " [3] Audition" MENU_AUDI_ENG_A_SPA `
            " [4] InDesign" MENU_IND_ENG_A_SPA `
            " [5] Media Encoder" MENU_ME_ENG_A_SPA `
            " [6] Photoshop" MENU_PS_ENG_A_SPA `
            " [7] Animate" MENU_ANI_ENG_A_SPA `
            " [8] Illustrator" MENU_ILU_ENG_A_SPA `
            " [9] InCopy" MENU_INC_ENG_A_SPA `
            "[10] Character Animator" MENU_CA_ENG_A_SPA `
            "[11] Menú principal" MENU_PRINCIPAL `
            "[12] Ayuda" MENU_AYUDA `
            "[13] Reportar un error" MENU_REPORTAR_ERROR `
            "[14] Salir" MENU_SALIR
    }
}

# Menú Adobe español a inglés
function MENU_ADOBE_SPA_A_ENG {

    switch ($OpcionMenu) {
        1 { $VersionAdobe = 2025
            $FreezeOpcionMenu = 1
            break
        }
        2 { $VersionAdobe = 2024
            $FreezeOpcionMenu = 2
            break
        }
        3 { $VersionAdobe = 2023
            $FreezeOpcionMenu = 3
            break
        }
        4 { $VersionAdobe = 2022
            $FreezeOpcionMenu = 4
            break
        }
        5 { $VersionAdobe = 2021
            $FreezeOpcionMenu = 5
            break
        }
        6 { $VersionAdobe = 2020
            $FreezeOpcionMenu = 6
            break
        }
        7 { $VersionAdobe = 2019
            $FreezeOpcionMenu = 7
            break
        }
        8 { $VersionAdobe = 2018
            $FreezeOpcionMenu = 8
            break
        }
        default {
            $VersionAdobe = 2025
            $FreezeOpcionMenu = 1
        }
    }
    #Write-Host "usuario tipeó" $VersionAdobe "**DEBUG**" -Fore Red;

    # Chequea versión porque Animate no está disponible en la 2025
    if ($VersionAdobe -eq 2025) {

        Menu 1 13 "`n Adobe $VersionAdobe - Español a inglés`n -----------------------------" MENU_ADOBE_SPA_A_ENG `
            " [1] After Effects" MENU_AE_SPA_A_ENG `
            " [2] Premiere Pro" MENU_PPRO_SPA_A_ENG `
            " [3] Audition" MENU_AUDI_SPA_A_ENG `
            " [4] InDesign" MENU_IND_SPA_A_ENG `
            " [5] Media Encoder" MENU_ME_SPA_A_ENG `
            " [6] Photoshop" MENU_PS_SPA_A_ENG `
            " [7] Illustrator" MENU_ILU_SPA_A_ENG `
            " [8] InCopy" MENU_INC_SPA_A_ENG `
            " [9] Character Animator" MENU_CA_SPA_A_ENG `
            "[10] Menú principal" MENU_PRINCIPAL `
            "[11] Ayuda" MENU_AYUDA `
            "[12] Reportar un error" MENU_REPORTAR_ERROR `
            "[13] Salir" MENU_SALIR

    } else {

        Menu 1 14 "`n Adobe $VersionAdobe - Español a inglés`n -----------------------------" MENU_ADOBE_SPA_A_ENG `
            " [1] After Effects" MENU_AE_SPA_A_ENG `
            " [2] Premiere Pro" MENU_PPRO_SPA_A_ENG `
            " [3] Audition" MENU_AUDI_SPA_A_ENG `
            " [4] InDesign" MENU_IND_SPA_A_ENG `
            " [5] Media Encoder" MENU_ME_SPA_A_ENG `
            " [6] Photoshop" MENU_PS_SPA_A_ENG `
            " [7] Animate" MENU_ANI_SPA_A_ENG `
            " [8] Illustrator" MENU_ILU_SPA_A_ENG `
            " [9] InCopy" MENU_INC_SPA_A_ENG `
            "[10] Character Animator" MENU_CA_SPA_A_ENG `
            "[11] Menú principal" MENU_PRINCIPAL `
            "[12] Ayuda" MENU_AYUDA `
            "[13] Reportar un error" MENU_REPORTAR_ERROR `
            "[14] Salir" MENU_SALIR
    }
}

# Cierra aplicaciones antes de cambiar el idioma (https://chat.openai.com/share/ef3f3502-4870-41b7-ae5b-81a8e7c43ea5)
function Cerrar-App {
    param ([string]$nombreProceso)
    
    Write-Host $SimiDesc"`n" -Fore DarkGray
    $proceso = Get-Process | Where-Object { $_.ProcessName -eq $nombreProceso }

    if ($proceso) {

        Write-Host "`n ¡$nombreProceso está abierto!`n Es recomendable cerrarlo antes de cambiar el idioma." -Fore Red
        $respuesta = Read-Host "`n ¿Querés cerrarlo? (S/N)"
        
        if ($respuesta -eq "S" -or $respuesta -eq "s") {

            Stop-Process -Name $nombreProceso -Force
            Write-Host "`n Cerrando $nombreProceso..." -Fore Yellow
            Start-Sleep -Seconds 5
            $verificaProceso = Get-Process | Where-Object { $_.ProcessName -eq $nombreProceso }

            if (-not $verificaProceso) {
                Write-Host " $nombreProceso se cerró correctamente." -Fore DarkGreen
            } else {
                Write-Host " Ocurrió un error al intentar cerrar $nombreProceso." -Fore Red
            }
        } else {
            Write-Host "`n Se intentará cambiar el idioma sin cerrar $nombreProceso.`n Es posible que el idioma no se cambie correctamente." -Fore Yellow
        }
    }
}

# Menú After Effects, inglés a español
function MENU_AE_ENG_A_SPA {

    Cerrar-App -nombreProceso "Adobe After Effects"
    
    $RutaInstalAe = "Adobe After Effects $VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalAe"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $Idioma = Get-Content "$RutaInstalacion\Support Files\AMT\application.xml" | Where-Object { ($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb) }
    $Contenido = Get-Content "$RutaInstalacion\Support Files\AMT\application.xml"

    if ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs, $XmlEsEs) | Set-Content "$RutaInstalacion\Support Files\AMT\application.xml"
        Write-Host "$CambioEngSpa [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb, $XmlEsEs) | Set-Content "$RutaInstalacion\Support Files\AMT\application.xml"
        Write-Host "$CambioEngSpa [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }
    
    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu **DEBUG** " $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú After Effects, español a inglés
function MENU_AE_SPA_A_ENG {

    Cerrar-App -nombreProceso "Adobe After Effects"

    $RutaInstalAe = "Adobe After Effects $VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalAe"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $Idioma = Get-Content "$RutaInstalacion\Support Files\AMT\application.xml" | Where-Object { ($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx) }
    $Contenido = Get-Content "$RutaInstalacion\Support Files\AMT\application.xml"

    if ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$RutaInstalacion\Support Files\AMT\application.xml"
        Write-Host "$CambioSpaEng [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$RutaInstalacion\Support Files\AMT\application.xml"
        Write-Host "$CambioSpaEng [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }
    
    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu **DEBUG** " $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Menú Premiere Pro, inglés a español
function MENU_PPRO_ENG_A_SPA {

    Cerrar-App -nombreProceso "Adobe Premiere Pro"

    $RutaInstalPpro = "Adobe Premiere Pro $VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalPpro"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $Idioma = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb) }
    $Contenido = Get-Content "$RutaInstalacion\AMT\application.xml"

    if ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        Write-Host "$CambioEngSpa [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        Write-Host "$CambioEngSpa [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu **DEBUG** " $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú Premiere Pro, español a inglés
function MENU_PPRO_SPA_A_ENG {

    Cerrar-App -nombreProceso "Adobe Premiere Pro"

    $RutaInstalPpro = "Adobe Premiere Pro $VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalPpro"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $Idioma = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx) }
    $Contenido = Get-Content "$RutaInstalacion\AMT\application.xml"

    if ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        Write-Host "$CambioSpaEng [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        Write-Host "$CambioSpaEng [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu **DEBUG** " $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Menú Audition, inglés a español
function MENU_AUDI_ENG_A_SPA {

    Cerrar-App -nombreProceso "Adobe Audition"
    
    $RutaInstalAudi = "Adobe Audition $VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION

    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalAudi"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $Idioma = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb) }
    $Contenido = Get-Content "$RutaInstalacion\AMT\application.xml"

    if ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        Write-Host "$CambioEngSpa [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        Write-Host "$CambioEngSpa [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu **DEBUG** " $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú Audition, español a inglés
function MENU_AUDI_SPA_A_ENG {

    Cerrar-App -nombreProceso "Adobe Audition"

    $RutaInstalAudi = "Adobe Audition $VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalAudi"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }
    
    $Idioma = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx) }
    $Contenido = Get-Content "$RutaInstalacion\AMT\application.xml"

    if ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        Write-Host "$CambioSpaEng [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        Write-Host "$CambioSpaEng [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu **DEBUG** " $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Menú InDesign, inglés a español
function MENU_IND_ENG_A_SPA {

    Cerrar-App -nombreProceso "Adobe InDesign"

    $RutaInstalInd = "Adobe InDesign $VersionAdobe"
    $SourceDescarga = "$UrlLocales/ind/$VersionAdobe/$LocaleEsEs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\ind\$VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalInd"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $IdiomaEng = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb) }
    $IdiomaSpa = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx) }
    $Contenido = Get-Content "$RutaInstalacion\AMT\application.xml"

    if ( ($IdiomaEng -match $XmlEnUs) -or ($IdiomaEng -match $XmlEnGb) ) {

        if ( ( ($IdiomaEng -match $XmlEnUs) -and (Test-Path -Path "$RutaInstalacion\Presets\InDesign_Workspaces\$LocaleEnUs" -PathType Container) ) ) {
            $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        } elseif ( ( ($IdiomaEng -match $XmlEnGb) -and (Test-Path -Path "$RutaInstalacion\Presets\InDesign_Workspaces\$LocaleEnGb" -PathType Container) ) ) {
            $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEsEs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEsMx.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalacion\$LocaleEsEs.zip" -Force
        } else {
            
            Verifica-Conexion
            
            #Write-Host $Descargando "(~97 KB)" -Fore Yellow
            TAMANIO_DESCARGA -Url $SourceDescarga
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEsEs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalacion\$LocaleEsEs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalacion").copyhere($Shell.NameSpace("$RutaInstalacion\$LocaleEsEs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalacion\$LocaleEsEs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host "$CambioEngSpa [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1

    } elseif ( ($IdiomaSpa -match $XmlEsEs) -or ($IdiomaSpa -match $XmlEsMx) ) {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        #Write-Host $ErrorCambioYaInstalado -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú InDesign, español a inglés
function MENU_IND_SPA_A_ENG {

    Cerrar-App -nombreProceso "Adobe InDesign"

    $RutaInstalInd = "Adobe InDesign $VersionAdobe"
    $SourceDescarga = "$UrlLocales/ind/$VersionAdobe/$LocaleEnUs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\ind\$VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalInd"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $IdiomaEng = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb) }
    $IdiomaSpa = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx) }
    $Contenido = Get-Content "$RutaInstalacion\AMT\application.xml"

    if ( ($IdiomaSpa -match $XmlEsEs) -or ($IdiomaSpa -match $XmlEsMx) ) {

        if ( ( ($IdiomaSpa -match $XmlEsEs) -and (Test-Path -Path "$RutaInstalacion\Presets\InDesign_Workspaces\$LocaleEsEs" -PathType Container) ) ) {
            $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        } elseif ( ( ($IdiomaSpa -match $XmlEsMx) -and (Test-Path -Path "$RutaInstalacion\Presets\InDesign_Workspaces\$LocaleEsMx" -PathType Container) ) ) {
            $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEnUs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEnGb.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalacion\$LocaleEnUs.zip" -Force
        } else {

            Verifica-Conexion

            #Write-Host $Descargando "(~95 KB)" -Fore Yellow
            TAMANIO_DESCARGA -Url $SourceDescarga
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEnUs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalacion\$LocaleEnUs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalacion").copyhere($Shell.NameSpace("$RutaInstalacion\$LocaleEnUs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalacion\$LocaleEnUs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host "$CambioSpaEng [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1

    } elseif ( ($IdiomaEng -match $XmlEnUs) -or ($IdiomaEng -match $XmlEnGb) ) {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        #Write-Host $ErrorCambioYaInstalado -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Menú Media Encoder, inglés a español (https://chat.openai.com/share/ca4486b3-6c7d-4385-94bb-fff3db6be04f)
function MENU_ME_ENG_A_SPA {

    Cerrar-App -nombreProceso "Adobe Media Encoder"

    $RutaInstalMe = "Adobe Media Encoder $VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalMe"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $contenidoArchivo = Get-Content -Path "$RutaInstalacion\AMT\application.xml" -Raw

    if ($contenidoArchivo -match $tagIdiomas) {
        $contenidoEncontrado = $matches[1]

        if ($contenidoEncontrado -like $LocaleEsEs -or $contenidoEncontrado -like $LocaleEsMx) {
            Write-Host $NoCambio -Fore Red
            Write-Host $Razones -Fore Yellow
            Start-Sleep -Seconds 1
        } else {
            $nuevoContenido = $contenidoArchivo -replace $tagIdiomas, $XmlEsEs
            Set-Content -Path "$RutaInstalacion\AMT\application.xml" -Value $nuevoContenido
            Write-Host "$CambioEngSpa [$RutaInstalacion]" -Fore DarkGreen
            Start-Sleep -Seconds 1
        }
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu **DEBUG** " $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú Media Encoder, español a inglés
function MENU_ME_SPA_A_ENG {

    Cerrar-App -nombreProceso "Adobe Media Encoder"

    $RutaInstalMe = "Adobe Media Encoder $VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalMe"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $contenidoArchivo = Get-Content -Path "$RutaInstalacion\AMT\application.xml" -Raw

    if ($contenidoArchivo -match $tagIdiomas) {
        $contenidoEncontrado = $matches[1]

        if ($contenidoEncontrado -like $LocaleEnUs -or $contenidoEncontrado -like $LocaleEnGb) {
            Write-Host $NoCambio -Fore Red
            Write-Host $Razones -Fore Yellow
            Start-Sleep -Seconds 1
        } else {
            $nuevoContenido = $contenidoArchivo -replace $tagIdiomas, $XmlEnUs
            Set-Content -Path "$RutaInstalacion\AMT\application.xml" -Value $nuevoContenido
            Write-Host "$CambioSpaEng [$RutaInstalacion]" -Fore DarkGreen
            Start-Sleep -Seconds 1
        }
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu **DEBUG** " $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Menú Photoshop, inglés a español
function MENU_PS_ENG_A_SPA {

    Cerrar-App -nombreProceso "Adobe Photoshop"

    $RutaInstalPs = "Adobe Photoshop $VersionAdobe"
    $SourceDescarga = "$UrlLocales/ps/$VersionAdobe/$LocaleEsEs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\ps\$VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalPs"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }


    if ( -not( (Test-Path -Path "$RutaInstalacion\Locales\$LocaleEsEs" -PathType Container) -or (Test-Path -Path "$RutaInstalacion\Locales\$LocaleEsMx" -PathType Container) ) ) {
        
        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEsEs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEsMx.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalacion\Locales\$LocaleEsEs.zip" -Force
        } else {

            Verifica-Conexion

            #Write-Host $Descargando "(~600 KB)" -Fore Yellow
            TAMANIO_DESCARGA -Url $SourceDescarga
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEsEs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalacion\Locales\$LocaleEsEs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow        
        # Unzip, copy, replace and keeps encoding (https://gist.github.com/PrateekKumarSingh/1dc3765a50e0e0cced63574316382304)
        [void](New-Item -Path "$RutaInstalacion\Locales\$LocaleEsEs" -ItemType Directory -Force)
        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalacion\Locales\$LocaleEsEs").copyhere($Shell.NameSpace("$RutaInstalacion\Locales\$LocaleEsEs.zip").Items(), 0x14) #0x14 overwrite AND silent

        Remove-Item "$RutaInstalacion\Locales\$LocaleEsEs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host "$CambioEngSpa [$RutaInstalacion] $CambioPs" -Fore DarkGreen
        Start-Sleep -Seconds 1

    } elseif ( (Test-Path -Path "$RutaInstalacion\Locales\$LocaleEsEs" -PathType Container) -or (Test-Path -Path "$RutaInstalacion\Locales\$LocaleEsMx" -PathType Container) ) {
        Write-Host $ErrorCambioPs -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú Photoshop, español a inglés
function MENU_PS_SPA_A_ENG {

    Cerrar-App -nombreProceso "Adobe Photoshop"

    $RutaInstalPs = "Adobe Photoshop $VersionAdobe"
    $SourceDescarga = "$UrlLocales/ps/$VersionAdobe/$LocaleEnUs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\ps\$VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalPs"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    if ( -not( (Test-Path -Path "$RutaInstalacion\Locales\$LocaleEnUs" -PathType Container) -or (Test-Path -Path "$RutaInstalacion\Locales\$LocaleEnGb" -PathType Container) ) ) {
        
        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEnUs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEnGb.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalacion\Locales\$LocaleEnUs.zip" -Force
        } else {

            Verifica-Conexion

            #Write-Host $Descargando "(~600 KB)" -Fore Yellow
            TAMANIO_DESCARGA -Url $SourceDescarga
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEnUs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalacion\Locales\$LocaleEnUs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        [void](New-Item -Path "$RutaInstalacion\Locales\$LocaleEnUs" -ItemType Directory -Force)
        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalacion\Locales\$LocaleEnUs").copyhere($Shell.NameSpace("$RutaInstalacion\Locales\$LocaleEnUs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalacion\Locales\$LocaleEnUs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host "$CambioSpaEng [$RutaInstalacion] $CambioPs" -Fore DarkGreen
        Start-Sleep -Seconds 1

    } elseif ( (Test-Path -Path "$RutaInstalacion\Locales\$LocaleEnUs" -PathType Container) -or (Test-Path -Path "$RutaInstalacion\Locales\$LocaleEnGb" -PathType Container) ) {
        Write-Host $ErrorCambioPs -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Menú Animate, inglés a español
function MENU_ANI_ENG_A_SPA {

    Cerrar-App -nombreProceso "Adobe Animate"
    
    $RutaInstalAni = "Adobe Animate $VersionAdobe"
    $SourceDescarga = "$UrlLocales/ani/$VersionAdobe/$LocaleEsEs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\ani\$VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalAni"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $IdiomaEng = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb) }
    $IdiomaSpa = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx) }
    $Contenido = Get-Content "$RutaInstalacion\AMT\application.xml"

    if ( ($IdiomaEng -match $XmlEnUs) -or ($IdiomaEng -match $XmlEnUs) ) {

        if ( ( ($IdiomaEng -match $XmlEnUs) -and (Test-Path -Path "$RutaInstalacion\$LocaleEnUs" -PathType Container) ) ) {
            $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        } elseif ( ( ($IdiomaEng -match $XmlEnGb) -and (Test-Path -Path "$RutaInstalacion\$LocaleEnGb" -PathType Container) ) ) {
            $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEsEs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEsMx.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalacion\$LocaleEsEs.zip" -Force
        } else {

            Verifica-Conexion

            #Write-Host $Descargando "(~4,5 MB)" -Fore Yellow
            TAMANIO_DESCARGA -Url $SourceDescarga
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEsEs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalacion\$LocaleEsEs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        [void](New-Item -Path "$RutaInstalacion\$LocaleEsEs" -ItemType Directory -Force)
        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalacion\$LocaleEsEs").copyhere($Shell.NameSpace("$RutaInstalacion\$LocaleEsEs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalacion\$LocaleEsEs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host "$CambioEngSpa [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1

    } elseif ( ($IdiomaSpa -match $XmlEsEs) -or ($IdiomaSpa -match $XmlEsMx) ) {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        #Write-Host $ErrorCambioYaInstalado -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú Animate, español a inglés
function MENU_ANI_SPA_A_ENG {

    Cerrar-App -nombreProceso "Adobe Animate"

    $RutaInstalAni = "Adobe Animate $VersionAdobe"
    $SourceDescarga = "$UrlLocales/ani/$VersionAdobe/$LocaleEnUs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\ani\$VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalAni"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $IdiomaEng = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb) }
    $IdiomaSpa = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx) }
    $Contenido = Get-Content "$RutaInstalacion\AMT\application.xml"

    if ( ($IdiomaSpa -match $XmlEsEs) -or ($IdiomaSpa -match $XmlEsMx) ) {

        if ( ( ($IdiomaSpa -match $XmlEsEs) -and (Test-Path -Path "$RutaInstalacion\$LocaleEsEs" -PathType Container) ) ) {
            $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        } elseif ( ( ($IdiomaSpa -match $XmlEsMx) -and (Test-Path -Path "$RutaInstalacion\$LocaleEsMx" -PathType Container) ) ) {
            $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEnUs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEnGb.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalacion\$LocaleEnUs.zip" -Force
        } else {

            Verifica-Conexion

            #Write-Host $Descargando "(~4,5 MB)" -Fore Yellow
            TAMANIO_DESCARGA -Url $SourceDescarga
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEnUs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalacion\$LocaleEnUs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        [void](New-Item -Path "$RutaInstalacion\$LocaleEnUs" -ItemType Directory -Force)
        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalacion\$LocaleEnUs").copyhere($Shell.NameSpace("$RutaInstalacion\$LocaleEnUs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalacion\$LocaleEnUs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host "$CambioSpaEng [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1

    } elseif ( ($IdiomaEng -match $XmlEnUs) -or ($IdiomaEng -match $XmlEnGb) ) {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        #Write-Host $ErrorCambioYaInstalado -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Menú Illustrator, inglés a español
function MENU_ILU_ENG_A_SPA {

    Cerrar-App -nombreProceso "Adobe Illustrator"

    $RutaInstalIlu = "Adobe Illustrator $VersionAdobe"
    $SourceDescarga = "$UrlLocales/il/$VersionAdobe/$LocaleEsEs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\il\$VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalIlu"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $IdiomaEng = Get-Content "$RutaInstalacion\Support Files\Contents\Windows\AMT\application.xml" | Where-Object { ($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb) }
    $IdiomaSpa = Get-Content "$RutaInstalacion\Support Files\Contents\Windows\AMT\application.xml" | Where-Object { ($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx) }
    $Contenido = Get-Content "$RutaInstalacion\Support Files\Contents\Windows\AMT\application.xml"

    if ( ($IdiomaEng -match $XmlEnUs) -or ($IdiomaEng -match $XmlEnGb) ) {

        if ( ( ($IdiomaEng -match $XmlEnUs) -and (Test-Path -Path "$RutaInstalacion\Support Files\Contents\Windows\$LocaleEnUs" -PathType Container) ) ) {
            $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content "$RutaInstalacion\Support Files\Contents\Windows\AMT\application.xml"
        } elseif ( ( ($IdiomaEng -match $XmlEnGb) -and (Test-Path -Path "$RutaInstalacion\Support Files\Contents\Windows\$LocaleEnGb" -PathType Container) ) ) {
            $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content "$RutaInstalacion\Support Files\Contents\Windows\AMT\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEsEs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEsMx.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalacion\$LocaleEsEs.zip" -Force
        } else {

            Verifica-Conexion

            #Write-Host $Descargando "(~27,5 MB)" -Fore Yellow
            TAMANIO_DESCARGA -Url $SourceDescarga
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEsEs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalacion\$LocaleEsEs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalacion").copyhere($Shell.NameSpace("$RutaInstalacion\$LocaleEsEs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalacion\$LocaleEsEs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host "$CambioEngSpa [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1

    } elseif ( ($IdiomaSpa -match $XmlEsEs) -or ($IdiomaSpa -match $XmlEsMx) ) {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        #Write-Host $ErrorCambioYaInstalado -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú Illustrator, español a inglés
function MENU_ILU_SPA_A_ENG {

    Cerrar-App -nombreProceso "Adobe Illustrator"

    $RutaInstalIlu = "Adobe Illustrator $VersionAdobe"
    $SourceDescarga = "$UrlLocales/il/$VersionAdobe/$LocaleEnUs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\il\$VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalIlu"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $IdiomaEng = Get-Content "$RutaInstalacion\Support Files\Contents\Windows\AMT\application.xml" | Where-Object { ($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb) }
    $IdiomaSpa = Get-Content "$RutaInstalacion\Support Files\Contents\Windows\AMT\application.xml" | Where-Object { ($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx) }
    $Contenido = Get-Content "$RutaInstalacion\Support Files\Contents\Windows\AMT\application.xml"

    if ( ($IdiomaSpa -match $XmlEsEs) -or ($IdiomaSpa -match $XmlEsMx) ) {

        if ( ( ($IdiomaSpa -match $XmlEsEs) -and (Test-Path -Path "$RutaInstalacion\Support Files\Contents\Windows\$LocaleEsEs" -PathType Container) ) ) {
            $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$RutaInstalacion\Support Files\Contents\Windows\AMT\application.xml"
        } elseif ( ( ($IdiomaSpa -match $XmlEsMx) -and (Test-Path -Path "$RutaInstalacion\Support Files\Contents\Windows\$LocaleEsMx" -PathType Container) ) ) {
            $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$RutaInstalacion\Support Files\Contents\Windows\AMT\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEnUs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEnGb.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalacion\$LocaleEnUs.zip" -Force
        } else {

            Verifica-Conexion

            #Write-Host $Descargando "(~27,5 MB)" -Fore Yellow
            TAMANIO_DESCARGA -Url $SourceDescarga
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEnUs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalacion\$LocaleEnUs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalacion").copyhere($Shell.NameSpace("$RutaInstalacion\$LocaleEnUs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalacion\$LocaleEnUs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host "$CambioSpaEng [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1

    } elseif ( ($IdiomaEng -match $XmlEnUs) -or ($IdiomaEng -match $XmlEnGb) ) {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        #Write-Host $ErrorCambioYaInstalado -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Menú InCopy, inglés a español
function MENU_INC_ENG_A_SPA {

    Cerrar-App -nombreProceso "Adobe InCopy"

    $RutaInstalInc = "Adobe InCopy $VersionAdobe"
    $SourceDescarga = "$UrlLocales/inc/$VersionAdobe/$LocaleEsEs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\inc\$VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalInc"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $IdiomaEng = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb) }
    $IdiomaSpa = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx) }
    $Contenido = Get-Content "$RutaInstalacion\AMT\application.xml"

    if ( ($IdiomaEng -match $XmlEnUs) -or ($IdiomaEng -match $XmlEnGb) ) {

        if ( ( ($IdiomaEng -match $XmlEnUs) -and (Test-Path -Path "$RutaInstalacion\Presets\InCopy_Workspaces\$LocaleEnUs" -PathType Container) ) ) {
            $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        } elseif ( ( ($IdiomaEng -match $XmlEnGb) -and (Test-Path -Path "$RutaInstalacion\Presets\InCopy_Workspaces\$LocaleEnGb" -PathType Container) ) ) {
            $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEsEs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEsMx.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalacion\$LocaleEsEs.zip" -Force
        } else {

            Verifica-Conexion

            #Write-Host $Descargando "(~70 KB)" -Fore Yellow
            TAMANIO_DESCARGA -Url $SourceDescarga
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEsEs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalacion\$LocaleEsEs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalacion").copyhere($Shell.NameSpace("$RutaInstalacion\$LocaleEsEs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalacion\$LocaleEsEs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host "$CambioEngSpa [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1

    } elseif ( ($IdiomaSpa -match $XmlEsEs) -or ($IdiomaSpa -match $XmlEsMx) ) {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        #Write-Host $ErrorCambioYaInstalado -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú InCopy, español a inglés
function MENU_INC_SPA_A_ENG {

    Cerrar-App -nombreProceso "Adobe InCopy"

    $RutaInstalInc = "Adobe InCopy $VersionAdobe"
    $SourceDescarga = "$UrlLocales/inc/$VersionAdobe/$LocaleEnUs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\inc\$VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalInc"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $IdiomaEng = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb) }
    $IdiomaSpa = Get-Content "$RutaInstalacion\AMT\application.xml" | Where-Object { ($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx) }
    $Contenido = Get-Content "$RutaInstalacion\AMT\application.xml"

    if ( ($IdiomaSpa -match $XmlEsEs) -or ($IdiomaSpa -match $XmlEsMx) ) {

        if ( ( ($IdiomaSpa -match $XmlEsEs) -and (Test-Path -Path "$RutaInstalacion\Presets\InCopy_Workspaces\$LocaleEsEs" -PathType Container) ) ) {
            $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        } elseif ( ( ($IdiomaSpa -match $XmlEsMx) -and (Test-Path -Path "$RutaInstalacion\Presets\InCopy_Workspaces\$LocaleEsMx" -PathType Container) ) ) {
            $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$RutaInstalacion\AMT\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEnUs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEnGb.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalacion\$LocaleEnUs.zip" -Force
        } else {

            Verifica-Conexion

            #Write-Host $Descargando "(~75 KB)" -Fore Yellow
            TAMANIO_DESCARGA -Url $SourceDescarga
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEnUs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalacion\$LocaleEnUs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalacion").copyhere($Shell.NameSpace("$RutaInstalacion\$LocaleEnUs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalacion\$LocaleEnUs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host "$CambioSpaEng [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1

    } elseif ( ($IdiomaEng -match $XmlEnUs) -or ($IdiomaEng -match $XmlEnGb) ) {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        #Write-Host $ErrorCambioYaInstalado -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Menú Character Animator, inglés a español
function MENU_CA_ENG_A_SPA {

    Cerrar-App -nombreProceso "Adobe Character Animator"
    
    $RutaInstalCa = "Adobe Character Animator $VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalCa"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $Idioma = Get-Content "$RutaInstalacion\Support Files\AMT\application.xml" | Where-Object { ($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb) }
    $Contenido = Get-Content "$RutaInstalacion\Support Files\AMT\application.xml"

    if ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content "$RutaInstalacion\Support Files\AMT\application.xml"
        Write-Host "$CambioEngSpa [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content "$RutaInstalacion\Support Files\AMT\application.xml"
        Write-Host "$CambioEngSpa [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }
    
    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu **DEBUG** " $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú Character Animator, español a inglés
function MENU_CA_SPA_A_ENG {

    Cerrar-App -nombreProceso "Adobe Character Animator"

    $RutaInstalCa = "Adobe Character Animator $VersionAdobe"
    $RutaInstalacion = RUTA_INSTALACION
    #Write-Host "La ruta que se usará es: [$RutaInstalacion]" **DEBUG**
    
    if ($RutaInstalacion -eq $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalAdobe\$RutaInstalCa"
    } elseif ($RutaInstalacion -ne $RutaInstalAdobe) {
        $RutaInstalacion = "$RutaInstalacion"
    }

    $Idioma = Get-Content "$RutaInstalacion\Support Files\AMT\application.xml" | Where-Object { ($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx) }
    $Contenido = Get-Content "$RutaInstalacion\Support Files\AMT\application.xml"

    if ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$RutaInstalacion\Support Files\AMT\application.xml"
        Write-Host "$CambioSpaEng [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$RutaInstalacion\Support Files\AMT\application.xml"
        Write-Host "$CambioSpaEng [$RutaInstalacion]" -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }
    
    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu **DEBUG** " $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Buscar nueva versión de Simi (https://chat.openai.com/share/0feee147-7748-4da5-b893-6faa5934b276)
function MENU_UPDATE {

    $DestinoDescarga = "$ScriptDir\versiones_simi"
    Write-Host $SimiDesc"`n" -Fore DarkGray
    Verifica-Conexion

    # Chequea última versión
    Write-Host $BuscandoVersion -Fore Yellow
    Start-Sleep -Seconds 2
    $VersionTxt = Invoke-WebRequest -Uri $UrlUltimaVersionWin
    $UltimaVersionTxt = $VersionTxt.Content.Trim()    
    $UrlNuevaVersion = "$UrlReleases/$NombreRelease$UltimaVersionTxt.exe"

    # Compara versión del script con la última online
    if ($UltimaVersionTxt -gt $VersionActualSimi) {
        
        Write-Host $NuevaVDisponible "(v$UltimaVersionTxt)" -Fore DarkGreen
        $DescargaSiNo = Read-Host $DeseaDescargar
        Limpia-Pantalla
        
        if ($DescargaSiNo -eq "S" -or $DescargaSiNo -eq "s") {

            Write-Host $SimiDesc"`n" -Fore DarkGray
            TAMANIO_DESCARGA -Url $UrlNuevaVersion
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $UrlNuevaVersion -OutFile "$DestinoDescarga\$NombreRelease$UltimaVersionTxt.exe"

            # Chequea si el archivo se descargó
            if (Test-Path "$DestinoDescarga\$NombreRelease$UltimaVersionTxt.exe" -PathType Leaf) {

                Write-Host $DescargaCorrecta -Fore DarkGreen
                $EjecutarSiNo = Read-Host $DeseaAbrir
                Limpia-Pantalla
                
                if ($EjecutarSiNo -eq "S" -or $EjecutarSiNo -eq "s") {

                    Start-Process -FilePath "$DestinoDescarga\$NombreRelease$UltimaVersionTxt.exe"
                    Stop-Process -Id $PID

                } else {
                    # Vuelve al menú
                    MENU_PRINCIPAL
                }
            } else {
                Write-Host $NoDescargo -Fore Red
                # Vuelve al menú
                MENU_PRINCIPAL
            }
        } else {
            # Vuelve al menú
            MENU_PRINCIPAL
        }
    } else {
        Limpia-Pantalla
        Write-Host "$UsandoUltimaVersion (v$VersionActualSimi)" -Fore DarkGreen
        # Vuelve al menú
        MENU_PRINCIPAL
    }
}

# Cierra app
function MENU_SALIR {
    Write-Host $SimiDesc -Fore DarkGray
    Write-Host $MensajeResenia -Fore Yellow
    Start-Sleep -Seconds 3
    Stop-Process -Id $PID
}

# Ayuda
function MENU_AYUDA {
    Write-Host $MensajeUrlAyuda -Fore Yellow
    Start-Sleep -Seconds 2
    Start-Process $UrlAyudaTienda
    # Vuelve al menú
    MENU_PRINCIPAL
}

# Reportar error
function MENU_REPORTAR_ERROR {
    Write-Host $MensajeRepError -Fore Yellow
    Start-Sleep -Seconds 2
    Start-Process $UrlReportarError
    # Vuelve al menú
    MENU_PRINCIPAL
}

MENU_PRINCIPAL