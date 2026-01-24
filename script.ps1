# Simi v1.4
# Cambiá el idioma de los programas de Adobe sin reinstalarlos
# https://leandroperez.art/tienda/productos-gratuitos/simi-cambia-idioma-adobe-sin-reinstalar/
# © Leandro Pérez

# Versión mínima requerida de PowerShell
#Requires -Version 5.1

# Variables versión, menú y ruta instalación
$global:VersionAdobe
$global:FreezeOpcionMenu
$global:RutaInstalAlt
$global:RutaInstalDefault

# Variables idiomas
$global:XmlEnUs = '<Data key="installedLanguages">en_US</Data>'
$global:XmlEnGb = '<Data key="installedLanguages">en_GB</Data>'
$global:XmlEsEs = '<Data key="installedLanguages">es_ES</Data>'
$global:XmlEsMx = '<Data key="installedLanguages">es_MX</Data>'
$global:XmlAllLang1 = '<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>'
$global:XmlAllLang2 = '<Data key="installedLanguages">cs_CZ,da_DK,de_DE,el_GR,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fil_PH,fr_CA,fr_FR,fr_MA,hi_IN,hu_HU,id_ID,it_IT,ja_JP,ko_KR,ms_MY,nb_NO,nl_NL,pl_PL,pt_BR,ro_RO,ru_RU,sv_SE,th_TH,tr_TR,uk_UA,vi_VN,zh_CN,zh_TW</Data>'
$global:LocaleEnUs = 'en_US'
$global:LocaleEnGb = 'en_GB'
$global:LocaleEsEs = 'es_ES'
$global:LocaleEsMx = 'es_MX'

# Locales
#$global:UrlLocales = "http://localhost/lp/simi"
$global:UrlLocales = "https://leandroperez.art/go/simi/locales"

# Variables mensajes
$global:CambioEngSpa = "`n Se cambió el idioma de inglés a español correctamente.`n"
$global:CambioSpaEng = "`n Se cambió el idioma de español a inglés correctamente.`n"
$global:AlertaCambio = "`n`n ¡Cerrá el programa de Adobe antes de cambiar el idioma!"
$global:NoCambio = "`n ¡No se pudo cambiar el idioma!"
$global:Razones = "`n Puede ser por diferentes razones:`n - El programa de Adobe no está instalado en la ruta por defecto (C:\Archivos de programa).`n - El programa de Adobe no se instaló usando la aplicación Creative Cloud.`n - La versión de Adobe que elegiste no está instalada en tu computadora."
$global:CambioPs = "`n ¡Listo! Ya podés cambiar el idioma de Photoshop desde el menú Editar > Preferencias > Interfaz."
$global:ErrorCambioPs = "`n Ya tenés instalado el idioma español. Lo podés cambiar desde el menú Editar > Preferencias > Interfaz."
$global:ErrorCambioYaInstalado = " - Ya tenés instalado el idioma seleccionado."
$global:Descargando = "`n Descargando archivo de idioma..."
$global:SinConexion = "`n No es posible conectarse a la página de descarga de idiomas. Intentando nuevamente en 5s..."

# Menú con opciones
function Menu ($MenuNumero, $MenuCierra, $NombreMenu, $NombreFuncionMenu, $OpcionMenu1, $MenuFuncion1, $OpcionMenu2, $MenuFuncion2, $OpcionMenu3, $MenuFuncion3, $OpcionMenu4, $MenuFuncion4, $OpcionMenu5, $MenuFuncion5, $OpcionMenu6, $MenuFuncion6, $OpcionMenu7, $MenuFuncion7, $OpcionMenu8, $MenuFuncion8, $OpcionMenu9, $MenuFuncion9, $OpcionMenu10, $MenuFuncion10, $OpcionMenu11, $MenuFuncion11) {

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
    
    [int]$OpcionMenu = Read-Host -Prompt "`n Tipeá una opción y presioná Enter"
        
    if (($OpcionMenu -lt $MenuNumero) -or ($OpcionMenu -gt $MenuCierra)) {
        Write-Host " `nTipeá una de las opciones que están arriba.`n" -Fore Red
        Start-Sleep -Seconds 1
        Invoke-Expression $NombreFuncionMenu
    } else {
        if ($OpcionMenu -eq $MenuNumero) { Invoke-Expression $MenuFuncion1 }
        if ($OpcionMenu -eq ($MenuNumero + "1")) { Invoke-Expression $MenuFuncion2 }
        if ($OpcionMenu -eq ($MenuNumero + "2")) { Invoke-Expression $MenuFuncion3 }   
        if ($OpcionMenu -eq ($MenuNumero + "3")) { Invoke-Expression $MenuFuncion4 } 
        if ($OpcionMenu -eq ($MenuNumero + "4")) { Invoke-Expression $MenuFuncion5 } 
        if ($OpcionMenu -eq ($MenuNumero + "5")) { Invoke-Expression $MenuFuncion6 } 
        if ($OpcionMenu -eq ($MenuNumero + "6")) { Invoke-Expression $MenuFuncion7 } 
        if ($OpcionMenu -eq ($MenuNumero + "7")) { Invoke-Expression $MenuFuncion8 }
        if ($OpcionMenu -eq ($MenuNumero + "8")) { Invoke-Expression $MenuFuncion9 } 
        if ($OpcionMenu -eq ($MenuNumero + "9")) { Invoke-Expression $MenuFuncion10 }
        if ($OpcionMenu -eq ($MenuNumero + "10")) { Invoke-Expression $MenuFuncion11 }
    }
}

# Menú principal, muestra idiomas
function MENU_PRINCIPAL {
    Write-Host "`n`n Simi v1.4 - © Leandro Pérez`n Cambiá el idioma de Adobe sin reinstalar los programas" -Fore DarkGray
    Menu 1 4 "`n Menú principal`n ==============" MENU_PRINCIPAL "1. Cambiar de inglés a español" MENU_ENG_A_SPA_PRINCIPAL "2. Cambiar de español a inglés" MENU_SPA_A_ENG_PRINCIPAL "3. Salir" MENU_SALIR "4. Ayuda" MENU_AYUDA
}

# Menú principal inglés a español
function MENU_ENG_A_SPA_PRINCIPAL {
    Menu 1 8 "`n Cambiar de inglés a español`n ===========================" MENU_ENG_A_SPA_PRINCIPAL "1. Adobe 2022" MENU_ADOBE_ENG_A_SPA "2. Adobe 2021" MENU_ADOBE_ENG_A_SPA "3. Adobe 2020" MENU_ADOBE_ENG_A_SPA "4. Adobe 2019" MENU_ADOBE_ENG_A_SPA "5. Adobe 2018" MENU_ADOBE_ENG_A_SPA "6. Menú selección de idioma" MENU_PRINCIPAL "7. Salir" MENU_SALIR "8. Ayuda" MENU_AYUDA
}

# Menú principal español a inglés
function MENU_SPA_A_ENG_PRINCIPAL {
    Menu 1 8 "`n Cambiar de español a inglés`n ===========================" MENU_SPA_A_ENG_PRINCIPAL "1. Adobe 2022" MENU_ADOBE_SPA_A_ENG "2. Adobe 2021" MENU_ADOBE_SPA_A_ENG "3. Adobe 2020" MENU_ADOBE_SPA_A_ENG "4. Adobe 2019" MENU_ADOBE_SPA_A_ENG "5. Adobe 2018" MENU_ADOBE_SPA_A_ENG "6. Menú selección de idioma" MENU_PRINCIPAL "7. Salir" MENU_SALIR "8. Ayuda" MENU_AYUDA
}

# Pide ingreso de ruta de instalación del programa de Adobe
function RUTA_INSTALACION {
    $RutaInstalAlt = Read-Host -Prompt "`n Ingresá la ruta de instalación del programa o presioná Enter para usar la ruta por defecto (C:\Archivos de programa\Adobe)"
    if ($RutaInstalAlt) {
        Write-Host "`n Se cambiará el idioma en la ruta [$RutaInstalAlt].`n Si recibís un error, asegurate de que la ruta ingresada no termine en una barra '\'. Ej.: [F:\Programas\After 2022]."
    } else {
        Write-Host "`n Se usará la ruta por defecto (C:\Archivos de programa\Adobe\<programa de Adobe>)."
        $RutaInstalDefault = "$Env:Programfiles\Adobe"
        $RutaInstalAlt = $RutaInstalDefault
    }
}

# # Guarda valores para la versión de Adobe elegida por el usuario
# function VERSION_ADOBE {

# }

# Menú Adobe inglés a español
function MENU_ADOBE_ENG_A_SPA {
    switch($OpcionMenu) {
        1 { $VersionAdobe = 2022
            $FreezeOpcionMenu = 1
            break
        }
        2 { $VersionAdobe = 2021
            $FreezeOpcionMenu = 2
            break
        }
        3 { $VersionAdobe = 2020
            $FreezeOpcionMenu = 3
            break
        }
        4 { $VersionAdobe = 2019
            $FreezeOpcionMenu = 4
            break
        }
        5 { $VersionAdobe = 2018
            $FreezeOpcionMenu = 5
            break
        }
        default {
            $VersionAdobe = 2022
            $FreezeOpcionMenu = 1
        }
    }
    #Write-Host "usuario tipeó" $VersionAdobe "*****DELETE" -Fore Red;
    
    Menu 1 10 "`n Adobe $VersionAdobe`n ========== $AlertaCambio" MENU_ADOBE_ENG_A_SPA "1. After Effects" MENU_AE_ENG_A_SPA "2. Premiere Pro" MENU_PPRO_ENG_A_SPA "3. Audition" MENU_AUDI_ENG_A_SPA "4. InDesign" MENU_IND_ENG_A_SPA "5. Media Encoder" MENU_ME_ENG_A_SPA "6. Photoshop" MENU_PS_ENG_A_SPA "7. Animate" MENU_ANI_ENG_A_SPA "8. Menú selección de idioma" MENU_PRINCIPAL "9. Salir" MENU_SALIR "10. Ayuda" MENU_AYUDA
}

# Menú Adobe español a inglés
function MENU_ADOBE_SPA_A_ENG {
    switch($OpcionMenu) {
        1 { $VersionAdobe = 2022
            $FreezeOpcionMenu = 1
            break
        }
        2 { $VersionAdobe = 2021
            $FreezeOpcionMenu = 2
            break
        }
        3 { $VersionAdobe = 2020
            $FreezeOpcionMenu = 3
            break
        }
        4 { $VersionAdobe = 2019
            $FreezeOpcionMenu = 4
            break
        }
        5 { $VersionAdobe = 2018
            $FreezeOpcionMenu = 5
            break
        }
        default {
            $VersionAdobe = 2022
            $FreezeOpcionMenu = 1
        }
    }
    #Write-Host "usuario tipeó" $VersionAdobe "******DELETE" -Fore Red;

    Menu 1 10 "`n Adobe $VersionAdobe`n ========== $AlertaCambio" MENU_ADOBE_SPA_A_ENG "1. After Effects" MENU_AE_SPA_A_ENG "2. Premiere Pro" MENU_PPRO_SPA_A_ENG "3. Audition" MENU_AUDI_SPA_A_ENG "4. InDesign" MENU_IND_SPA_A_ENG "5. Media Encoder" MENU_ME_SPA_A_ENG "6. Photoshop" MENU_PS_SPA_A_ENG "7. Animate" MENU_ANI_SPA_A_ENG "8. Menú selección de idioma" MENU_PRINCIPAL "9. Salir" MENU_SALIR "10. Ayuda" MENU_AYUDA
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

    $RutaInstalDefault = ".\Adobe\Adobe After Effects $VersionAdobe\Support Files\AMT"
    cd $Env:Programfiles
    cd $RutaInstalDefault

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }
    
    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu" $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú After Effects, español a inglés
function MENU_AE_SPA_A_ENG {
    $RutaInstalDefault = ".\Adobe\Adobe After Effects $VersionAdobe\Support Files\AMT"
    cd $Env:Programfiles
    cd $RutaInstalDefault

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }
    
    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu" $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Menú Premiere Pro, inglés a español
function MENU_PPRO_ENG_A_SPA {
    $RutaInstalDefault = ".\Adobe\Adobe Premiere Pro $VersionAdobe\AMT"
    cd $Env:Programfiles
    cd $RutaInstalDefault

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu" $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú Premiere Pro, español a inglés
function MENU_PPRO_SPA_A_ENG {
    $RutaInstalDefault = ".\Adobe\Adobe Premiere Pro $VersionAdobe\AMT"
    cd $Env:Programfiles
    cd $RutaInstalDefault

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu" $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Menú Audition, inglés a español
function MENU_AUDI_ENG_A_SPA {
    $RutaInstalDefault = ".\Adobe\Adobe Audition $VersionAdobe\AMT"
    cd $Env:Programfiles
    cd $RutaInstalDefault

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu" $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú Audition, español a inglés
function MENU_AUDI_SPA_A_ENG {
    $RutaInstalDefault = ".\Adobe\Adobe Audition $VersionAdobe\AMT"
    cd $Env:Programfiles
    cd $RutaInstalDefault

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu" $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Menú InDesign, inglés a español
function MENU_IND_ENG_A_SPA {
    $RutaInstalDefault1 = ".\Adobe\Adobe InDesign $VersionAdobe\Presets\InDesign Shortcut Sets"
    cd $Env:Programfiles
    cd $RutaInstalDefault1

    if (Test-Path -Path $LocaleEnUs -PathType Container) {
        Rename-Item -Path $LocaleEnUs -NewName $LocaleEsEs
    } elseif (Test-Path -Path $LocaleEnGb -PathType Container) {
        Rename-Item -Path $LocaleEnGb -NewName $LocaleEsEs
    }

    $RutaInstalDefault2 = ".\Adobe\Adobe InDesign $VersionAdobe\Presets\InDesign_Workspaces"
    cd $Env:Programfiles
    cd $RutaInstalDefault2

    if (Test-Path -Path $LocaleEnUs -PathType Container) {
        Rename-Item -Path $LocaleEnUs -NewName $LocaleEsEs
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif (Test-Path -Path $LocaleEnGb -PathType Container) {
        Rename-Item -Path $LocaleEnGb -NewName $LocaleEsEs
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu" $OpcionMenu -Fore Yellow;
    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú InDesign, español a inglés
function MENU_IND_SPA_A_ENG {
    $RutaInstalDefault1 = ".\Adobe\Adobe InDesign $VersionAdobe\Presets\InDesign Shortcut Sets"
    cd $Env:Programfiles
    cd $RutaInstalDefault1

    if (Test-Path -Path $LocaleEsEs -PathType Container) {
        Rename-Item -Path $LocaleEsEs -NewName $LocaleEnUs
    } elseif (Test-Path -Path $LocaleEsMx -PathType Container) {
        Rename-Item -Path $LocaleEsMx -NewName $LocaleEnUs
    }

    $RutaInstalDefault2 = ".\Adobe\Adobe InDesign $VersionAdobe\Presets\InDesign_Workspaces"
    cd $Env:Programfiles
    cd $RutaInstalDefault2

    if (Test-Path -Path $LocaleEsEs -PathType Container) {
        Rename-Item -Path $LocaleEsEs -NewName $LocaleEnUs
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif (Test-Path -Path $LocaleEsMx -PathType Container) {
        Rename-Item -Path $LocaleEsMx -NewName $LocaleEnUs
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu" $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Menú Media Encoder, inglés a español
function MENU_ME_ENG_A_SPA {
    $RutaInstalDefault = ".\Adobe\Adobe Media Encoder $VersionAdobe\AMT"
    cd $Env:Programfiles
    cd $RutaInstalDefault

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlAllLang1) -or ($_ -match $XmlAllLang2) -or ($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlAllLang1) {
        $Contenido.replace($XmlAllLang1,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlAllLang2) {
        $Contenido.replace($XmlAllLang2,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu" $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú Media Encoder, español a inglés
function MENU_ME_SPA_A_ENG {
    $RutaInstalDefault = ".\Adobe\Adobe Media Encoder $VersionAdobe\AMT"
    cd $Env:Programfiles
    cd $RutaInstalDefault

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlAllLang1) -or ($_ -match $XmlAllLang2) -or ($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlAllLang1) {
        $Contenido.replace($XmlAllLang1,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlAllLang2) {
        $Contenido.replace($XmlAllLang2,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu" $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Menú Photoshop, inglés a español
function MENU_PS_ENG_A_SPA {
    $SourceDescarga = "$UrlLocales/ps/$VersionAdobe/$LocaleEsEs"
    $RutaInstalDefault = "$Env:Programfiles\Adobe\Adobe Photoshop $VersionAdobe\Locales"
    $DestinoDescarga = "$LocaleEsEs.zip"

    if (-not((Test-Path -Path "$RutaInstalDefault\$LocaleEsEs" -PathType Container) -or (Test-Path -Path "$RutaInstalDefault\$LocaleEsMx" -PathType Container)) ) {
        cd $RutaInstalDefault
        # Chequea si hay conexión a Internet
        while (!(Test-Connection -computer leandroperez.art -count 1 -quiet)) {
            Write-Host $SinConexion -Fore Red
            Start-Sleep -Seconds 5
        }
        # Hay conexión
        Write-Host $Descargando -Fore Yellow
        Invoke-WebRequest -Uri $SourceDescarga -OutFile "$RutaInstalDefault\$DestinoDescarga"
        Expand-Archive "$LocaleEsEs.zip" -DestinationPath "$RutaInstalDefault\$LocaleEsEs" -Force
        Remove-Item "$LocaleEsEs.zip"
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
    $SourceDescarga = "$UrlLocales/ps/$VersionAdobe/$LocaleEnUs"
    $RutaInstalDefault = "$Env:Programfiles\Adobe\Adobe Photoshop $VersionAdobe\Locales"
    $DestinoDescarga = "$LocaleEnUs.zip"

    if (-not((Test-Path -Path "$RutaInstalDefault\$LocaleEnUs" -PathType Container) -or (Test-Path -Path "$RutaInstalDefault\$LocaleEnGb" -PathType Container)) ) {
        cd $RutaInstalDefault
        # Chequea si hay conexión a Internet
        while (!(Test-Connection -computer leandroperez.art -count 1 -quiet)) {
            Write-Host $SinConexion -Fore Red
            Start-Sleep -Seconds 5
        }
        # Hay conexión
        Write-Host $Descargando -Fore Yellow
        Invoke-WebRequest -Uri $SourceDescarga -OutFile "$RutaInstalDefault\$DestinoDescarga"
        Expand-Archive "$LocaleEnUs.zip" -DestinationPath "$RutaInstalDefault\$LocaleEnUs" -Force
        Remove-Item "$LocaleEnUs.zip"
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
    $RutaInstalDefault1 = ".\Adobe\Adobe Animate $VersionAdobe\AMT"
    $RutaInstalDefault2 = "$Env:Programfiles\Adobe\Adobe Animate $VersionAdobe"
    $SourceDescarga = "$UrlLocales/ani/$VersionAdobe/$LocaleEsEs"
    $DestinoDescarga = "$LocaleEsEs.zip"

    cd $Env:Programfiles
    cd $RutaInstalDefault1

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $Contenido = Get-Content application.xml

    if ( ( ($Idioma -match $XmlEnUs) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEnUs" -PathType Container) ) -or ( ($Idioma -match $XmlEnGb) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEnGb" -PathType Container) ) ) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content application.xml
        cd $RutaInstalDefault2
        # Chequea si hay conexión a Internet
        while (!(Test-Connection -computer leandroperez.art -count 1 -quiet)) {
            Write-Host $SinConexion -Fore Red
            Start-Sleep -Seconds 5
        }
        # Hay conexión
        Write-Host $Descargando -Fore Yellow
        Invoke-WebRequest -Uri $SourceDescarga -OutFile "$RutaInstalDefault2\$DestinoDescarga"
        Expand-Archive "$LocaleEsEs.zip" -DestinationPath "$RutaInstalDefault2\$LocaleEsEs" -Force
        Remove-Item "$LocaleEsEs.zip"
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ( ( ($Idioma -match $XmlEsEs) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEsEs" -PathType Container) ) -or ( ($Idioma -match $XmlEsMx) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEsMx" -PathType Container) ) ) {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Write-Host $ErrorCambioYaInstalado -Fore Yellow
        Start-Sleep -Seconds 1
    } elseif ( ( ($Idioma -match $XmlEnGb) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEnGb" -PathType Container) ) -or ( ($Idioma -match $XmlEnUs) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEnUs" -PathType Container) ) ) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content application.xml
        cd $RutaInstalDefault2
        while (!(Test-Connection -computer leandroperez.art -count 1 -quiet)) {
            Write-Host $SinConexion -Fore Red
            Start-Sleep -Seconds 5
        }
        # Hay conexión
        Write-Host $Descargando -Fore Yellow
        Invoke-WebRequest -Uri $SourceDescarga -OutFile "$RutaInstalDefault2\$DestinoDescarga"
        Expand-Archive "$LocaleEsEs.zip" -DestinationPath "$RutaInstalDefault2\$LocaleEsEs" -Force
        Remove-Item "$LocaleEsEs.zip"
        Write-Host $CambioEngSpa -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ( ( ($Idioma -match $XmlEsEs) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEsEs" -PathType Container) ) -or ( ($Idioma -match $XmlEsMx) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEsMx" -PathType Container) ) ) {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Write-Host $ErrorCambioYaInstalado -Fore Yellow
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Write-Host $ErrorCambioYaInstalado -Fore Yellow
        Start-Sleep -Seconds 1
    }
    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu

    # Vuelve al menú
    MENU_ADOBE_ENG_A_SPA
}

# Menú Animate, español a inglés
function MENU_ANI_SPA_A_ENG {
    $RutaInstalDefault1 = ".\Adobe\Adobe Animate $VersionAdobe\AMT"
    $RutaInstalDefault2 = "$Env:Programfiles\Adobe\Adobe Animate $VersionAdobe"
    $SourceDescarga = "$UrlLocales/ani/$VersionAdobe/$LocaleEnUs"
    $DestinoDescarga = "$LocaleEnUs.zip"

    cd $Env:Programfiles
    cd $RutaInstalDefault1

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content application.xml

    if ( ( ($Idioma -match $XmlEsEs) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEsEs" -PathType Container) ) -or ( ($Idioma -match $XmlEsMx) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEsMx" -PathType Container) ) ) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content application.xml
        cd $RutaInstalDefault2
        # Chequea si hay conexión a Internet
        while (!(Test-Connection -computer leandroperez.art -count 1 -quiet)) {
            Write-Host $SinConexion -Fore Red
            Start-Sleep -Seconds 5
        }
        # Hay conexión
        Write-Host $Descargando -Fore Yellow
        Invoke-WebRequest -Uri $SourceDescarga -OutFile "$RutaInstalDefault2\$DestinoDescarga"
        Expand-Archive "$LocaleEnUs.zip" -DestinationPath "$RutaInstalDefault2\$LocaleEnUs" -Force
        Remove-Item "$LocaleEnUs.zip"
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ( ( ($Idioma -match $XmlEsMx) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEsMx" -PathType Container) ) -or ( ($Idioma -match $XmlEsEs) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEsEs" -PathType Container) ) ) {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Write-Host $ErrorCambioYaInstalado -Fore Yellow
        Start-Sleep -Seconds 1
    } elseif ( ( ($Idioma -match $XmlEsMx) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEsMx" -PathType Container) ) -or ( ($Idioma -match $XmlEsEs) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEsEs" -PathType Container) ) ) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content application.xml
        cd $RutaInstalDefault2
        # Chequea si hay conexión a Internet
        while (!(Test-Connection -computer leandroperez.art -count 1 -quiet)) {
            Write-Host $SinConexion -Fore Red
            Start-Sleep -Seconds 5
        }
        # Hay conexión
        Write-Host $Descargando -Fore Yellow
        Invoke-WebRequest -Uri $SourceDescarga -OutFile "$RutaInstalDefault2\$DestinoDescarga"
        Expand-Archive "$LocaleEnUs.zip" -DestinationPath "$RutaInstalDefault2\$LocaleEnUs" -Force
        Remove-Item "$LocaleEnUs.zip"
        Write-Host $CambioSpaEng -Fore DarkGreen
        Start-Sleep -Seconds 1
    } elseif ( ( ($Idioma -match $XmlEsEs) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEsEs" -PathType Container) ) -or ( ($Idioma -match $XmlEsMx) -and (Test-Path -Path "$RutaInstalDefault2\$LocaleEsMx" -PathType Container) ) ) {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Write-Host $ErrorCambioYaInstalado -Fore Yellow
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red
        Write-Host $Razones -Fore Yellow
        Write-Host $ErrorCambioYaInstalado -Fore Yellow
        Start-Sleep -Seconds 1
    }
    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Cierra
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