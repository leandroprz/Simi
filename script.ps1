# Simi v1.6
# Cambiá el idioma de los programas de Adobe sin reinstalarlos
# https://leandroperez.art/tienda/productos-gratuitos/simi-cambia-idioma-adobe-sin-reinstalar/
# © Leandro Pérez

# Versión mínima requerida de PowerShell
#Requires -Version 5.1

# Variables versiones y paths
$script:VersionAdobe
$script:FreezeOpcionMenu
$script:RutaInstalAlt
$script:RutaInstalDefault

# Variables idiomas
$script:XmlEnUs = '<Data key="installedLanguages">en_US</Data>'
$script:XmlEnGb = '<Data key="installedLanguages">en_GB</Data>'
$script:XmlEsEs = '<Data key="installedLanguages">es_ES</Data>'
$script:XmlEsMx = '<Data key="installedLanguages">es_MX</Data>'
$script:XmlAllLang1 = '<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>'
$script:XmlAllLang2 = '<Data key="installedLanguages">cs_CZ,da_DK,de_DE,el_GR,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fil_PH,fr_CA,fr_FR,fr_MA,hi_IN,hu_HU,id_ID,it_IT,ja_JP,ko_KR,ms_MY,nb_NO,nl_NL,pl_PL,pt_BR,ro_RO,ru_RU,sv_SE,th_TH,tr_TR,uk_UA,vi_VN,zh_CN,zh_TW</Data>'
$script:LocaleEnUs = 'en_US'
$script:LocaleEnGb = 'en_GB'
$script:LocaleEsEs = 'es_ES'
$script:LocaleEsMx = 'es_MX'

# Locales
$script:UrlLocales = "https://github.com/leandroprz/Simi/raw/main/locales"
#$script:UrlLocales = "https://lp.local/simi" **DEBUG**

# Variables mensajes
$script:CambioEngSpa = "`n Se cambió el idioma de inglés a español correctamente."
$script:CambioSpaEng = "`n Se cambió el idioma de español a inglés correctamente."
$script:AlertaCambio = "`n`n **¡Cerrá el programa de Adobe antes de cambiar el idioma!**"
$script:NoCambio = "`n ¡No se pudo cambiar el idioma!"
$script:Cambiando = "`n Instalando idioma..."
$script:Razones = "`n Puede ser por diferentes razones:
 - El programa de Adobe no está instalado en la ruta por defecto [$Env:Programfiles\Adobe].
 - El programa de Adobe no se instaló usando la aplicación Creative Cloud.
 - La versión de Adobe que elegiste no está instalada en tu computadora.
 - Ya tenés instalado el idioma seleccionado."
$script:CambioPs = "`n ¡Listo! Ya podés elegir el nuevo idioma de Photoshop desde el menú Editar > Preferencias > Interfaz."
$script:ErrorCambioPs = "`n Ya tenés instalado el idioma seleccionado. Lo podés cambiar desde el menú Editar > Preferencias > Interfaz."
$script:ErrorCambioYaInstalado = " - Ya tenés instalado el idioma seleccionado."
$script:Descargando = "`n Descargando archivo de idioma..."
$script:SinConexion = "`n No es posible conectarse a la página de descarga de idiomas. Intentando nuevamente en 5s..."

# Fix for $PSScriptRoot when converting to exe (https://stackoverflow.com/a/60122064/5204005)
$script:ScriptDir = if (-not $PSScriptRoot) {  # $PSScriptRoot not defined?
    # Get the path of the executable *as invoked*, via
    # [environment]::GetCommandLineArgs()[0],
    # resolve it to a full path with Convert-Path, then get its directory path
    Split-Path -Parent (Convert-Path ([environment]::GetCommandLineArgs()[0])) 
    }
    else {
        # Use the automatic variable.
        $PSScriptRoot 
    }

# Menú con opciones
function Menu ($MenuNumero, $MenuCierra, $NombreMenu, $NombreFuncionMenu, $OpcionMenu1, $MenuFuncion1, $OpcionMenu2, $MenuFuncion2, $OpcionMenu3, $MenuFuncion3, $OpcionMenu4, $MenuFuncion4, $OpcionMenu5, $MenuFuncion5, $OpcionMenu6, $MenuFuncion6, $OpcionMenu7, $MenuFuncion7, $OpcionMenu8, $MenuFuncion8, $OpcionMenu9, $MenuFuncion9, $OpcionMenu10, $MenuFuncion10, $OpcionMenu11, $MenuFuncion11, $OpcionMenu12, $MenuFuncion12) {

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
    
    [int]$OpcionMenu = Read-Host -Prompt "`n Tipeá una opción y presioná Enter"
        
    if ( ($OpcionMenu -lt $MenuNumero) -or ($OpcionMenu -gt $MenuCierra) ) {
        Write-Host "`n Tipeá una de las opciones que están arriba.`n" -Fore Red
        Start-Sleep -Seconds 1
        Invoke-Expression $NombreFuncionMenu
    } else {
        if ($OpcionMenu -eq $MenuNumero) { Invoke-Expression $MenuFuncion1 }
        if ($OpcionMenu -eq ($MenuNumero + "1") ) { Invoke-Expression $MenuFuncion2 }
        if ($OpcionMenu -eq ($MenuNumero + "2") ) { Invoke-Expression $MenuFuncion3 }   
        if ($OpcionMenu -eq ($MenuNumero + "3") ) { Invoke-Expression $MenuFuncion4 } 
        if ($OpcionMenu -eq ($MenuNumero + "4") ) { Invoke-Expression $MenuFuncion5 } 
        if ($OpcionMenu -eq ($MenuNumero + "5") ) { Invoke-Expression $MenuFuncion6 } 
        if ($OpcionMenu -eq ($MenuNumero + "6") ) { Invoke-Expression $MenuFuncion7 } 
        if ($OpcionMenu -eq ($MenuNumero + "7") ) { Invoke-Expression $MenuFuncion8 }
        if ($OpcionMenu -eq ($MenuNumero + "8") ) { Invoke-Expression $MenuFuncion9 } 
        if ($OpcionMenu -eq ($MenuNumero + "9") ) { Invoke-Expression $MenuFuncion10 }
        if ($OpcionMenu -eq ($MenuNumero + "10") ) { Invoke-Expression $MenuFuncion11 }
        if ($OpcionMenu -eq ($MenuNumero + "11") ) { Invoke-Expression $MenuFuncion12 }
    }
}

# Menú principal, muestra idiomas
function MENU_PRINCIPAL {
    Write-Host "`n`n Simi v1.6 - © Leandro Pérez`n Cambiá el idioma de Adobe sin reinstalar los programas" -Fore DarkGray
    Menu 1 4 "`n Menú principal`n ==============" MENU_PRINCIPAL `
        "1. Cambiar de inglés a español" MENU_ENG_A_SPA_PRINCIPAL `
        "2. Cambiar de español a inglés" MENU_SPA_A_ENG_PRINCIPAL `
        "3. Salir" MENU_SALIR `
        "4. Ayuda" MENU_AYUDA
}

# Menú inglés a español
function MENU_ENG_A_SPA_PRINCIPAL {
    Menu 1 9 "`n Cambiar de inglés a español`n ===========================" MENU_ENG_A_SPA_PRINCIPAL `
        "1. Adobe 2023" MENU_ADOBE_ENG_A_SPA `
        "2. Adobe 2022" MENU_ADOBE_ENG_A_SPA `
        "3. Adobe 2021" MENU_ADOBE_ENG_A_SPA `
        "4. Adobe 2020" MENU_ADOBE_ENG_A_SPA `
        "5. Adobe 2019" MENU_ADOBE_ENG_A_SPA `
        "6. Adobe 2018" MENU_ADOBE_ENG_A_SPA `
        "7. Menú selección de idioma" MENU_PRINCIPAL `
        "8. Salir" MENU_SALIR `
        "9. Ayuda" MENU_AYUDA
}

# Menú español a inglés
function MENU_SPA_A_ENG_PRINCIPAL {
    Menu 1 9 "`n Cambiar de español a inglés`n ===========================" MENU_SPA_A_ENG_PRINCIPAL `
        "1. Adobe 2023" MENU_ADOBE_SPA_A_ENG `
        "2. Adobe 2022" MENU_ADOBE_SPA_A_ENG `
        "3. Adobe 2021" MENU_ADOBE_SPA_A_ENG `
        "4. Adobe 2020" MENU_ADOBE_SPA_A_ENG `
        "5. Adobe 2019" MENU_ADOBE_SPA_A_ENG `
        "6. Adobe 2018" MENU_ADOBE_SPA_A_ENG `
        "7. Menú selección de idioma" MENU_PRINCIPAL `
        "8. Salir" MENU_SALIR `
        "9. Ayuda" MENU_AYUDA
}

# Pide ingreso de ruta de instalación del programa de Adobe
# function RUTA_INSTALACION {
#     $RutaInstalAlt = Read-Host -Prompt "`n Ingresá la ruta de instalación del programa o presioná Enter para usar la ruta por defecto (C:\Archivos de programa\Adobe)"
#     if ($RutaInstalAlt) {
#         Write-Host "`n Se cambiará el idioma en la ruta [$RutaInstalAlt].`n Si recibís un error, asegurate de que la ruta ingresada no termine en una barra '\'. Ej.: [F:\Programas\After 2022]."
#     } else {
#         Write-Host "`n Se usará la ruta por defecto (C:\Archivos de programa\Adobe\<programa de Adobe>)."
#         $RutaInstalDefault = "$Env:Programfiles\Adobe"
#         $RutaInstalAlt = $RutaInstalDefault
#     }
# }


# Menú Adobe inglés a español
function MENU_ADOBE_ENG_A_SPA {
    switch ($OpcionMenu) {
        1 { $VersionAdobe = 2023
            $FreezeOpcionMenu = 1
            break
        }
        2 { $VersionAdobe = 2022
            $FreezeOpcionMenu = 2
            break
        }
        3 { $VersionAdobe = 2021
            $FreezeOpcionMenu = 3
            break
        }
        4 { $VersionAdobe = 2020
            $FreezeOpcionMenu = 4
            break
        }
        5 { $VersionAdobe = 2019
            $FreezeOpcionMenu = 5
            break
        }
        6 { $VersionAdobe = 2018
            $FreezeOpcionMenu = 6
            break
        }
        default {
            $VersionAdobe = 2023
            $FreezeOpcionMenu = 1
        }
    }
    #Write-Host "usuario tipeó" $VersionAdobe "**DEBUG**" -Fore Red;
    
    Menu 1 12 "`n Adobe $VersionAdobe`n ========== $AlertaCambio" MENU_ADOBE_ENG_A_SPA `
        "1. After Effects" MENU_AE_ENG_A_SPA `
        "2. Premiere Pro" MENU_PPRO_ENG_A_SPA `
        "3. Audition" MENU_AUDI_ENG_A_SPA `
        "4. InDesign" MENU_IND_ENG_A_SPA `
        "5. Media Encoder" MENU_ME_ENG_A_SPA `
        "6. Photoshop" MENU_PS_ENG_A_SPA `
        "7. Animate" MENU_ANI_ENG_A_SPA `
        "8. Illustrator" MENU_ILU_ENG_A_SPA `
        "9. InCopy" MENU_INC_ENG_A_SPA `
        "10. Menú selección de idioma" MENU_PRINCIPAL `
        "11. Salir" MENU_SALIR `
        "12. Ayuda" MENU_AYUDA
}

# Menú Adobe español a inglés
function MENU_ADOBE_SPA_A_ENG {
    switch ($OpcionMenu) {
        1 { $VersionAdobe = 2023
            $FreezeOpcionMenu = 1
            break
        }
        2 { $VersionAdobe = 2022
            $FreezeOpcionMenu = 2
            break
        }
        3 { $VersionAdobe = 2021
            $FreezeOpcionMenu = 3
            break
        }
        4 { $VersionAdobe = 2020
            $FreezeOpcionMenu = 4
            break
        }
        5 { $VersionAdobe = 2019
            $FreezeOpcionMenu = 5
            break
        }
        6 { $VersionAdobe = 2018
            $FreezeOpcionMenu = 6
            break
        }
        default {
            $VersionAdobe = 2023
            $FreezeOpcionMenu = 1
        }
    }
    #Write-Host "usuario tipeó" $VersionAdobe "**DEBUG**" -Fore Red;

    Menu 1 12 "`n Adobe $VersionAdobe`n ========== $AlertaCambio" MENU_ADOBE_SPA_A_ENG `
        "1. After Effects" MENU_AE_SPA_A_ENG `
        "2. Premiere Pro" MENU_PPRO_SPA_A_ENG `
        "3. Audition" MENU_AUDI_SPA_A_ENG `
        "4. InDesign" MENU_IND_SPA_A_ENG `
        "5. Media Encoder" MENU_ME_SPA_A_ENG `
        "6. Photoshop" MENU_PS_SPA_A_ENG `
        "7. Animate" MENU_ANI_SPA_A_ENG `
        "8. Illustrator" MENU_ILU_SPA_A_ENG `
        "9. InCopy" MENU_INC_SPA_A_ENG `
        "10. Menú selección de idioma" MENU_PRINCIPAL `
        "11. Salir" MENU_SALIR `
        "12. Ayuda" MENU_AYUDA
}

# Menú After Effects, inglés a español
function MENU_AE_ENG_A_SPA {

    # #RUTA_INSTALACION

    # $RutaInstalDefault = "$Env:Programfiles\Adobe\Adobe After Effects $VersionAdobe\Support Files\AMT"

    # if ($RutaInstalAlt -ne $RutaInstalDefault) {
    #     cd "$RutaInstalAlt\Support Files\AMT"
    # } elseif ($RutaInstalAlt -eq $RutaInstalDefault) {
    #     cd $RutaInstalDefault
    # }

    $RutaInstalDefault = "Adobe\Adobe After Effects $VersionAdobe\Support Files\AMT"

    $Idioma = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml" | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"

    if ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioEngSpa -Fore DarkGreen
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
    
    $RutaInstalDefault = "Adobe\Adobe After Effects $VersionAdobe\Support Files\AMT"

    $Idioma = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml" | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"

    if ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioSpaEng -Fore DarkGreen
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

    $RutaInstalDefault = "Adobe\Adobe Premiere Pro $VersionAdobe\AMT"

    $Idioma = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml" | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"

    if ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioEngSpa -Fore DarkGreen
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

    $RutaInstalDefault = "Adobe\Adobe Premiere Pro $VersionAdobe\AMT"

    $Idioma = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml" | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"

    if ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioSpaEng -Fore DarkGreen
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
    
    $RutaInstalDefault = "Adobe\Adobe Audition $VersionAdobe\AMT"

    $Idioma = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml" | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"

    if ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioEngSpa -Fore DarkGreen
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
    
    $RutaInstalDefault = "Adobe\Adobe Audition $VersionAdobe\AMT"
    
    $Idioma = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml" | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"

    if ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioSpaEng -Fore DarkGreen
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

    $RutaInstalDefault1 = "Adobe\Adobe InDesign $VersionAdobe\AMT"
    $RutaInstalDefault2 = "$Env:Programfiles\Adobe\Adobe InDesign $VersionAdobe"
    $RutaInstalDefault3 = "$Env:Programfiles\Adobe\Adobe InDesign $VersionAdobe\Presets\InDesign_Workspaces"
    $SourceDescarga = "$UrlLocales/ind/$VersionAdobe/$LocaleEsEs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\ind\$VersionAdobe"

    $IdiomaEng = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $IdiomaSpa = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"

    if ( ($IdiomaEng -match $XmlEnUs) -or ($IdiomaEng -match $XmlEnGb) ) {

        if ( (($IdiomaEng -match $XmlEnUs) -and (Test-Path -Path "$RutaInstalDefault3\$LocaleEnUs" -PathType Container)) ) {
            $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        } elseif ( (($IdiomaEng -match $XmlEnGb) -and (Test-Path -Path "$RutaInstalDefault3\$LocaleEnGb" -PathType Container)) ) {
            $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEsEs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEsMx.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalDefault2\$LocaleEsEs.zip" -Force
        } else {
            # Chequea si hay conexión a Internet
            while (!(Test-Connection -computer google.com -count 1 -quiet)) {
                Write-Host $SinConexion -Fore Red
                Start-Sleep -Seconds 5
            }
            # Hay conexión
            Write-Host $Descargando "(~97 KB)" -Fore Yellow
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEsEs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalDefault2\$LocaleEsEs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalDefault2").copyhere($Shell.NameSpace("$RutaInstalDefault2\$LocaleEsEs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalDefault2\$LocaleEsEs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host $CambioEngSpa -Fore DarkGreen
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

    $RutaInstalDefault1 = "Adobe\Adobe InDesign $VersionAdobe\AMT"
    $RutaInstalDefault2 = "$Env:Programfiles\Adobe\Adobe InDesign $VersionAdobe"
    $RutaInstalDefault3 = "$Env:Programfiles\Adobe\Adobe InDesign $VersionAdobe\Presets\InDesign_Workspaces"
    $SourceDescarga = "$UrlLocales/ind/$VersionAdobe/$LocaleEnUs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\ind\$VersionAdobe"

    $IdiomaEng = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $IdiomaSpa = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"

    if ( ($IdiomaSpa -match $XmlEsEs) -or ($IdiomaSpa -match $XmlEsMx) ) {

        if ( (($IdiomaSpa -match $XmlEsEs) -and (Test-Path -Path "$RutaInstalDefault3\$LocaleEsEs" -PathType Container)) ) {
            $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        } elseif ( (($IdiomaSpa -match $XmlEsMx) -and (Test-Path -Path "$RutaInstalDefault3\$LocaleEsMx" -PathType Container)) ) {
            $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEnUs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEnGb.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalDefault2\$LocaleEnUs.zip" -Force
        } else {
            # Chequea si hay conexión a Internet
            while (!(Test-Connection -computer google.com -count 1 -quiet)) {
                Write-Host $SinConexion -Fore Red
                Start-Sleep -Seconds 5
            }
            # Hay conexión
            Write-Host $Descargando "(~95 KB)" -Fore Yellow
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEnUs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalDefault2\$LocaleEnUs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalDefault2").copyhere($Shell.NameSpace("$RutaInstalDefault2\$LocaleEnUs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalDefault2\$LocaleEnUs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host $CambioSpaEng -Fore DarkGreen
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

# Menú Media Encoder, inglés a español
function MENU_ME_ENG_A_SPA {
    
    $RutaInstalDefault = "Adobe\Adobe Media Encoder $VersionAdobe\AMT"
    
    $Idioma = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml" | Where-Object {($_ -match $XmlAllLang1) -or ($_ -match $XmlAllLang2) -or ($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"

    if ($Idioma -match $XmlAllLang1) {
        $Contenido.replace($XmlAllLang1,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlAllLang2) {
        $Contenido.replace($XmlAllLang2,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioEngSpa -Fore DarkGreen
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

# Menú Media Encoder, español a inglés
function MENU_ME_SPA_A_ENG {

    $RutaInstalDefault = "Adobe\Adobe Media Encoder $VersionAdobe\AMT"
    
    $Idioma = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml" | Where-Object {($_ -match $XmlAllLang1) -or ($_ -match $XmlAllLang2) -or ($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"

    if ($Idioma -match $XmlAllLang1) {
        $Contenido.replace($XmlAllLang1,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlAllLang2) {
        $Contenido.replace($XmlAllLang2,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault\application.xml"
        Write-Host $CambioSpaEng -Fore DarkGreen
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

# Menú Photoshop, inglés a español
function MENU_PS_ENG_A_SPA {

    $SourceDescarga = "$UrlLocales/ps/$VersionAdobe/$LocaleEsEs.zip"
    $RutaInstalDefault = "$Env:Programfiles\Adobe\Adobe Photoshop $VersionAdobe\Locales"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\ps\$VersionAdobe"

    if (-not ((Test-Path -Path "$RutaInstalDefault\$LocaleEsEs" -PathType Container) -or (Test-Path -Path "$RutaInstalDefault\$LocaleEsMx" -PathType Container))) {
        
        if ((Test-Path -Path "$DestinoDescarga\$LocaleEsEs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEsMx.zip" -PathType Leaf)) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalDefault\$LocaleEsEs.zip" -Force
        } else {
            # Chequea si hay conexión a Internet
            while (!(Test-Connection -computer google.com -count 1 -quiet)) {
                Write-Host $SinConexion -Fore Red
                Start-Sleep -Seconds 5
            }
            # Hay conexión
            Write-Host $Descargando "(~600 KB)" -Fore Yellow
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEsEs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalDefault\$LocaleEsEs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow        
        # Unzip, copy, replace and keeps encoding (https://gist.github.com/PrateekKumarSingh/1dc3765a50e0e0cced63574316382304)
        [void](New-Item -Path "$RutaInstalDefault\$LocaleEsEs" -ItemType Directory -Force)
        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalDefault\$LocaleEsEs").copyhere($Shell.NameSpace("$RutaInstalDefault\$LocaleEsEs.zip").Items(), 0x14) #0x14 overwrite AND silent

        Remove-Item "$RutaInstalDefault\$LocaleEsEs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host $CambioPs -Fore DarkGreen
        Start-Sleep -Seconds 1

    } elseif ((Test-Path -Path "$RutaInstalDefault\$LocaleEsEs" -PathType Container) -or (Test-Path -Path "$RutaInstalDefault\$LocaleEsMx" -PathType Container)) {
        Write-Host $ErrorCambioPs -Fore Red
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú Photoshop, español a inglés
function MENU_PS_SPA_A_ENG {

    $SourceDescarga = "$UrlLocales/ps/$VersionAdobe/$LocaleEnUs.zip"
    $RutaInstalDefault = "$Env:Programfiles\Adobe\Adobe Photoshop $VersionAdobe\Locales"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\ps\$VersionAdobe"

    if (-not ((Test-Path -Path "$RutaInstalDefault\$LocaleEnUs" -PathType Container) -or (Test-Path -Path "$RutaInstalDefault\$LocaleEnGb" -PathType Container))) {
        
        if ((Test-Path -Path "$DestinoDescarga\$LocaleEnUs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEnGb.zip" -PathType Leaf)) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalDefault\$LocaleEnUs.zip" -Force
        } else {
            # Chequea si hay conexión a Internet
            while (!(Test-Connection -computer google.com -count 1 -quiet)) {
                Write-Host $SinConexion -Fore Red
                Start-Sleep -Seconds 5
            }
            # Hay conexión
            Write-Host $Descargando "(~600 KB)" -Fore Yellow
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEnUs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalDefault\$LocaleEnUs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        [void](New-Item -Path "$RutaInstalDefault\$LocaleEnUs" -ItemType Directory -Force)
        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalDefault\$LocaleEnUs").copyhere($Shell.NameSpace("$RutaInstalDefault\$LocaleEnUs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalDefault\$LocaleEnUs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host $CambioPs -Fore DarkGreen
        Start-Sleep -Seconds 1

    } elseif ((Test-Path -Path "$RutaInstalDefault\$LocaleEnUs" -PathType Container) -or (Test-Path -Path "$RutaInstalDefault\$LocaleEnGb" -PathType Container)) {
        Write-Host $ErrorCambioPs -Fore Red
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Menú Animate, inglés a español
function MENU_ANI_ENG_A_SPA {

    $RutaInstalDefault1 = "Adobe\Adobe Animate $VersionAdobe\AMT"
    $RutaInstalDefault2 = "$Env:Programfiles\Adobe\Adobe Animate $VersionAdobe"
    $SourceDescarga = "$UrlLocales/ani/$VersionAdobe/$LocaleEsEs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\ani\$VersionAdobe"

    $IdiomaEng = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $IdiomaSpa = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"

    if ( ($IdiomaEng -match $XmlEnUs) -or ($IdiomaEng -match $XmlEnUs) ) {

        if ( (($IdiomaEng -match $XmlEnUs) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEnUs" -PathType Container)) ) {
            $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        } elseif ( (($IdiomaEng -match $XmlEnGb) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEnGb" -PathType Container)) ) {
            $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEsEs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEsMx.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalDefault2\$LocaleEsEs.zip" -Force
        } else {
            # Chequea si hay conexión a Internet
            while (!(Test-Connection -computer google.com -count 1 -quiet)) {
                Write-Host $SinConexion -Fore Red
                Start-Sleep -Seconds 5
            }
            # Hay conexión
            Write-Host $Descargando "(~4,5 MB)" -Fore Yellow
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEsEs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalDefault2\$LocaleEsEs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        [void](New-Item -Path "$RutaInstalDefault2\$LocaleEsEs" -ItemType Directory -Force)
        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalDefault2\$LocaleEsEs").copyhere($Shell.NameSpace("$RutaInstalDefault2\$LocaleEsEs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalDefault2\$LocaleEsEs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host $CambioEngSpa -Fore DarkGreen
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

    $RutaInstalDefault1 = "Adobe\Adobe Animate $VersionAdobe\AMT"
    $RutaInstalDefault2 = "$Env:Programfiles\Adobe\Adobe Animate $VersionAdobe"
    $SourceDescarga = "$UrlLocales/ani/$VersionAdobe/$LocaleEnUs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\ani\$VersionAdobe"

    $IdiomaEng = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $IdiomaSpa = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"

    if ( ($IdiomaSpa -match $XmlEsEs) -or ($IdiomaSpa -match $XmlEsMx) ) {

        if ( (($IdiomaSpa -match $XmlEsEs) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEsEs" -PathType Container)) ) {
            $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        } elseif ( (($IdiomaSpa -match $XmlEsMx) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEsMx" -PathType Container)) ) {
            $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEnUs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEnGb.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalDefault2\$LocaleEnUs.zip" -Force
        } else {
            # Chequea si hay conexión a Internet
            while (!(Test-Connection -computer google.com -count 1 -quiet)) {
                Write-Host $SinConexion -Fore Red
                Start-Sleep -Seconds 5
            }
            # Hay conexión
            Write-Host $Descargando "(~4,5 MB)" -Fore Yellow
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEnUs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalDefault2\$LocaleEnUs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        [void](New-Item -Path "$RutaInstalDefault2\$LocaleEnUs" -ItemType Directory -Force)
        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalDefault2\$LocaleEnUs").copyhere($Shell.NameSpace("$RutaInstalDefault2\$LocaleEnUs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalDefault2\$LocaleEnUs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host $CambioSpaEng -Fore DarkGreen
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

    $RutaInstalDefault1 = "Adobe\Adobe Illustrator $VersionAdobe\Support Files\Contents\Windows\AMT"
    $RutaInstalDefault2 = "$Env:Programfiles\Adobe\Adobe Illustrator $VersionAdobe"
    $RutaInstalDefault3 = "$Env:Programfiles\Adobe\Adobe Illustrator $VersionAdobe\Support Files\Contents\Windows"
    $SourceDescarga = "$UrlLocales/il/$VersionAdobe/$LocaleEsEs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\il\$VersionAdobe"

    $IdiomaEng = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $IdiomaSpa = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"

    if ( ($IdiomaEng -match $XmlEnUs) -or ($IdiomaEng -match $XmlEnGb) ) {

        if ( (($IdiomaEng -match $XmlEnUs) -and (Test-Path -Path "$RutaInstalDefault3\$LocaleEnUs" -PathType Container)) ) {
            $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        } elseif ( (($IdiomaEng -match $XmlEnGb) -and (Test-Path -Path "$RutaInstalDefault3\$LocaleEnGb" -PathType Container)) ) {
            $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEsEs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEsMx.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalDefault2\$LocaleEsEs.zip" -Force
        } else {
            # Chequea si hay conexión a Internet
            while (!(Test-Connection -computer google.com -count 1 -quiet)) {
                Write-Host $SinConexion -Fore Red
                Start-Sleep -Seconds 5
            }
            # Hay conexión
            Write-Host $Descargando "(~27,5 MB)" -Fore Yellow
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEsEs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalDefault2\$LocaleEsEs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalDefault2").copyhere($Shell.NameSpace("$RutaInstalDefault2\$LocaleEsEs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalDefault2\$LocaleEsEs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host $CambioEngSpa -Fore DarkGreen
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

    $RutaInstalDefault1 = "Adobe\Adobe Illustrator $VersionAdobe\Support Files\Contents\Windows\AMT"
    $RutaInstalDefault2 = "$Env:Programfiles\Adobe\Adobe Illustrator $VersionAdobe"
    $RutaInstalDefault3 = "$Env:Programfiles\Adobe\Adobe Illustrator $VersionAdobe\Support Files\Contents\Windows"
    $SourceDescarga = "$UrlLocales/il/$VersionAdobe/$LocaleEnUs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\il\$VersionAdobe"

    $IdiomaEng = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $IdiomaSpa = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"

    if ( ($IdiomaSpa -match $XmlEsEs) -or ($IdiomaSpa -match $XmlEsMx) ) {

        if ( (($IdiomaSpa -match $XmlEsEs) -and (Test-Path -Path "$RutaInstalDefault3\$LocaleEsEs" -PathType Container)) ) {
            $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        } elseif ( (($IdiomaSpa -match $XmlEsMx) -and (Test-Path -Path "$RutaInstalDefault3\$LocaleEsMx" -PathType Container)) ) {
            $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEnUs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEnGb.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalDefault2\$LocaleEnUs.zip" -Force
        } else {
            # Chequea si hay conexión a Internet
            while (!(Test-Connection -computer google.com -count 1 -quiet)) {
                Write-Host $SinConexion -Fore Red
                Start-Sleep -Seconds 5
            }
            # Hay conexión
            Write-Host $Descargando "(~27,5 MB)" -Fore Yellow
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEnUs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalDefault2\$LocaleEnUs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalDefault2").copyhere($Shell.NameSpace("$RutaInstalDefault2\$LocaleEnUs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalDefault2\$LocaleEnUs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host $CambioSpaEng -Fore DarkGreen
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

    $RutaInstalDefault1 = "Adobe\Adobe InCopy $VersionAdobe\AMT"
    $RutaInstalDefault2 = "$Env:Programfiles\Adobe\Adobe InCopy $VersionAdobe"
    $RutaInstalDefault3 = "$Env:Programfiles\Adobe\Adobe InCopy $VersionAdobe\Presets\InCopy_Workspaces"
    $SourceDescarga = "$UrlLocales/inc/$VersionAdobe/$LocaleEsEs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\inc\$VersionAdobe"

    $IdiomaEng = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $IdiomaSpa = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"

    if ( ($IdiomaEng -match $XmlEnUs) -or ($IdiomaEng -match $XmlEnGb) ) {

        if ( (($IdiomaEng -match $XmlEnUs) -and (Test-Path -Path "$RutaInstalDefault3\$LocaleEnUs" -PathType Container)) ) {
            $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        } elseif ( (($IdiomaEng -match $XmlEnGb) -and (Test-Path -Path "$RutaInstalDefault3\$LocaleEnGb" -PathType Container)) ) {
            $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEsEs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEsMx.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalDefault2\$LocaleEsEs.zip" -Force
        } else {
            # Chequea si hay conexión a Internet
            while (!(Test-Connection -computer google.com -count 1 -quiet)) {
                Write-Host $SinConexion -Fore Red
                Start-Sleep -Seconds 5
            }
            # Hay conexión
            Write-Host $Descargando "(~70 KB)" -Fore Yellow
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEsEs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEsEs.zip" -Destination "$RutaInstalDefault2\$LocaleEsEs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalDefault2").copyhere($Shell.NameSpace("$RutaInstalDefault2\$LocaleEsEs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalDefault2\$LocaleEsEs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host $CambioEngSpa -Fore DarkGreen
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

    $RutaInstalDefault1 = "Adobe\Adobe InCopy $VersionAdobe\AMT"
    $RutaInstalDefault2 = "$Env:Programfiles\Adobe\Adobe InCopy $VersionAdobe"
    $RutaInstalDefault3 = "$Env:Programfiles\Adobe\Adobe InCopy $VersionAdobe\Presets\InCopy_Workspaces"
    $SourceDescarga = "$UrlLocales/inc/$VersionAdobe/$LocaleEnUs.zip"
    $DestinoDescarga = "$ScriptDir\idiomas_simi\inc\$VersionAdobe"

    $IdiomaEng = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $IdiomaSpa = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml" | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"

    if ( ($IdiomaSpa -match $XmlEsEs) -or ($IdiomaSpa -match $XmlEsMx) ) {

        if ( (($IdiomaSpa -match $XmlEsEs) -and (Test-Path -Path "$RutaInstalDefault3\$LocaleEsEs" -PathType Container)) ) {
            $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        } elseif ( (($IdiomaSpa -match $XmlEsMx) -and (Test-Path -Path "$RutaInstalDefault3\$LocaleEsMx" -PathType Container)) ) {
            $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content "$Env:Programfiles\$RutaInstalDefault1\application.xml"
        }

        if ( (Test-Path -Path "$DestinoDescarga\$LocaleEnUs.zip" -PathType Leaf) -or (Test-Path -Path "$DestinoDescarga\$LocaleEnGb.zip" -PathType Leaf) ) {
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalDefault2\$LocaleEnUs.zip" -Force
        } else {
            # Chequea si hay conexión a Internet
            while (!(Test-Connection -computer google.com -count 1 -quiet)) {
                Write-Host $SinConexion -Fore Red
                Start-Sleep -Seconds 5
            }
            # Hay conexión
            Write-Host $Descargando "(~75 KB)" -Fore Yellow
            $null = New-Item -Path $DestinoDescarga -ItemType Directory -Force
            Invoke-WebRequest -Uri $SourceDescarga -OutFile "$DestinoDescarga\$LocaleEnUs.zip"
            Copy-Item -Path "$DestinoDescarga\$LocaleEnUs.zip" -Destination "$RutaInstalDefault2\$LocaleEnUs.zip" -Force
        }

        Write-Host $Cambiando -Fore Yellow

        $Shell = New-Object -com Shell.Application
        $Shell.Namespace("$RutaInstalDefault2").copyhere($Shell.NameSpace("$RutaInstalDefault2\$LocaleEnUs.zip").Items(), 0x14)

        Remove-Item "$RutaInstalDefault2\$LocaleEnUs.zip" -Force -ErrorAction SilentlyContinue
        Write-Host $CambioSpaEng -Fore DarkGreen
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

# Cierra app
function MENU_SALIR {
    Write-Host "`n Gracias por usar Simi.`n ¡No olvides dejarnos una reseña en www.leandroperez.art!`n" -Fore Yellow
    Start-Sleep -Seconds 5
    Stop-Process -Id $PID
}

# Ayuda
function MENU_AYUDA {
    Write-Host "`n Gracias por usar Simi.`n En breve se abrirá la página de ayuda.`n" -Fore Yellow
    Start-Sleep -Seconds 2
    Start-Process "https://leandroperez.art/tienda/productos-gratuitos/simi-cambia-idioma-adobe-sin-reinstalar/"
    # Vuelve al menú
    MENU_PRINCIPAL
}

MENU_PRINCIPAL