# Simi v1.1
# Cambiá el idioma de los programas de Adobe sin reinstalarlos
# https://leandroperez.art/tienda/productos-gratuitos/simi-cambia-idioma-adobe-sin-reinstalar/
# © Leandro Pérez

# Variables versión y menú
$global:VersionAdobe
$global:FreezeOpcionMenu

# Variables idiomas
$global:XmlEnUs = '<Data key="installedLanguages">en_US</Data>'
$global:XmlEnGb = '<Data key="installedLanguages">en_GB</Data>'
$global:XmlEsEs = '<Data key="installedLanguages">es_ES</Data>'
$global:XmlEsMx = '<Data key="installedLanguages">es_MX</Data>'
$global:XmlAllLang = '<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>'
$global:CarpetaEnUs = 'en_US'
$global:CarpetaEnGb = 'en_GB'
$global:CarpetaEsEs = 'es_ES'
$global:CarpetaEsMx = 'es_MX'

# Variables mensajes
$global:CambioEngSpa = "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú.`n"
$global:CambioSpaEng = "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú.`n"
$global:NoCambio = "`n ¡No se pudo cambiar el idioma!"
$global:Razones = "`n Puede ser por diferentes razones:`n - El programa no está instalado en la ruta por defecto (C:\Archivos de programa).`n - El programa no se instaló usando la aplicación Creative Cloud.`n - No abriste esta aplicación como Administrador."

function Menu ($MenuNumero, $MenuCierra, $NombreMenu, $NombreFuncionMenu, $OpcionMenu1, $MenuFuncion1, $OpcionMenu2, $MenuFuncion2, $OpcionMenu3, $MenuFuncion3, $OpcionMenu4, $MenuFuncion4, $OpcionMenu5, $MenuFuncion5, $OpcionMenu6, $MenuFuncion6, $OpcionMenu7, $MenuFuncion7, $OpcionMenu8, $MenuFuncion8, $OpcionMenu9, $MenuFuncion9, $OpcionMenu10, $MenuFuncion10) {

    Write-Host "`n$NombreMenu`n" -Fore Gray;
    if ($OpcionMenu1 -ne $null) { Write-Host " $OpcionMenu1" -Fore Gray; }
    if ($OpcionMenu2 -ne $null) { Write-Host " $OpcionMenu2" -Fore Gray; }
    if ($OpcionMenu3 -ne $null) { Write-Host " $OpcionMenu3" -Fore Gray; }
    if ($OpcionMenu4 -ne $null) { Write-Host " $OpcionMenu4" -Fore Gray; }
    if ($OpcionMenu5 -ne $null) { Write-Host " $OpcionMenu5" -Fore Gray; }
    if ($OpcionMenu6 -ne $null) { Write-Host " $OpcionMenu6" -Fore Gray; }
    if ($OpcionMenu7 -ne $null) { Write-Host " $OpcionMenu7" -Fore Gray; }
    if ($OpcionMenu8 -ne $null) { Write-Host " $OpcionMenu8" -Fore Gray; }
    if ($OpcionMenu9 -ne $null) { Write-Host " $OpcionMenu9" -Fore Gray; }
    if ($OpcionMenu10 -ne $null) { Write-Host " $OpcionMenu9" -Fore Gray; }
    
    [int]$OpcionMenu = Read-Host -Prompt "`n Tipeá una opción y presioná Enter"
        
    if (($OpcionMenu -lt $MenuNumero) -or ($OpcionMenu -gt $MenuCierra)) {
        Write-Host " `nTipeá una de las opciones que están arriba.`n" -Fore Red; Start-Sleep -Seconds 1
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
    }
}

# Menú principal, muestra idiomas
function MENU_PRINCIPAL {
    Write-Host "`n`n Simi v1.1 - © Leandro Pérez`n Cambiá el idioma de Adobe sin reinstalar los programas" -Fore DarkGray;
    Menu 1 4 "`n Menú principal`n ==============" MENU_PRINCIPAL "1. Cambiar de inglés a español" MENU_ENG_A_SPA_PRINCIPAL "2. Cambiar de español a inglés" MENU_SPA_A_ENG_PRINCIPAL "3. Salir" MENU_SALIR "4. Ayuda" MENU_AYUDA
}

# Menú principal inglés a español
function MENU_ENG_A_SPA_PRINCIPAL {
    Menu 1 7 "`n Cambiar de inglés a español`n ===========================" MENU_ENG_A_SPA_PRINCIPAL "1. Adobe 2021" MENU_ADOBE_ENG_A_SPA "2. Adobe 2020" MENU_ADOBE_ENG_A_SPA "3. Adobe 2019" MENU_ADOBE_ENG_A_SPA "4. Adobe 2018" MENU_ADOBE_ENG_A_SPA "5. Menú principal" MENU_PRINCIPAL "6. Salir" MENU_SALIR "7. Ayuda" MENU_AYUDA
}

# Menú principal español a inglés
function MENU_SPA_A_ENG_PRINCIPAL {
    Menu 1 7 "`n Cambiar de español a inglés`n ===========================" MENU_SPA_A_ENG_PRINCIPAL "1. Adobe 2021" MENU_ADOBE_SPA_A_ENG "2. Adobe 2020" MENU_ADOBE_SPA_A_ENG "3. Adobe 2019" MENU_ADOBE_SPA_A_ENG "4. Adobe 2018" MENU_ADOBE_SPA_A_ENG "5. Menú principal" MENU_PRINCIPAL "6. Salir" MENU_SALIR "7. Ayuda" MENU_AYUDA
}

# Menú Adobe inglés a español
function MENU_ADOBE_ENG_A_SPA {
    switch($OpcionMenu) {
        1 { $VersionAdobe = 2021
            $FreezeOpcionMenu = 1
            break
        }
        2 { $VersionAdobe = 2020
            $FreezeOpcionMenu = 2
            break
        }
        3 { $VersionAdobe = 2019
            $FreezeOpcionMenu = 3
            break
        }
        4 { $VersionAdobe = 2018
            $FreezeOpcionMenu = 4
            break
        }
        default {
            $VersionAdobe = 2021
            $FreezeOpcionMenu = 1
        }
    }
    #Write-Host "usuario tipeó" $VersionAdobe "*****DELETE" -Fore Red;
    
    Menu 1 8 "`n Adobe $VersionAdobe`n ==========" MENU_ADOBE_ENG_A_SPA "1. After Effects" MENU_AE_ENG_A_SPA "2. Premiere Pro" MENU_PPRO_ENG_A_SPA "3. Audition" MENU_AUDI_ENG_A_SPA "4. InDesign" MENU_IND_ENG_A_SPA "5. Media Encoder" MENU_ME_ENG_A_SPA "6. Menú principal" MENU_PRINCIPAL "7. Salir" MENU_SALIR "8. Ayuda" MENU_AYUDA
}

# Menú Adobe español a inglés
function MENU_ADOBE_SPA_A_ENG {
    switch($OpcionMenu) {
        1 { $VersionAdobe = 2021
            $FreezeOpcionMenu = 1
            break
        }
        2 { $VersionAdobe = 2020
            $FreezeOpcionMenu = 2
            break
        }
        3 { $VersionAdobe = 2019
            $FreezeOpcionMenu = 3
            break
        }
        4 { $VersionAdobe = 2018
            $FreezeOpcionMenu = 4
            break
        }
        default {
            $VersionAdobe = 2021
            $FreezeOpcionMenu = 1
        }
    }
    #Write-Host "usuario tipeó" $VersionAdobe "******DELETE" -Fore Red;

    Menu 1 8 "`n Adobe $VersionAdobe`n ==========" MENU_ADOBE_SPA_A_ENG "1. After Effects" MENU_AE_SPA_A_ENG "2. Premiere Pro" MENU_PPRO_SPA_A_ENG "3. Audition" MENU_AUDI_SPA_A_ENG "4. InDesign" MENU_IND_SPA_A_ENG "5. Media Encoder" MENU_ME_SPA_A_ENG "6. Menú principal" MENU_PRINCIPAL "7. Salir" MENU_SALIR "8. Ayuda" MENU_AYUDA
}

# Menú After Effects, inglés a español
function MENU_AE_ENG_A_SPA {
    $RutaInstalacion = ".\Adobe\Adobe After Effects $VersionAdobe\Support Files\AMT"
    cd $Env:Programfiles
    cd $RutaInstalacion

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red;
        Write-Host $Razones -Fore Yellow;
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
    $RutaInstalacion = ".\Adobe\Adobe After Effects $VersionAdobe\Support Files\AMT"
    cd $Env:Programfiles
    cd $RutaInstalacion

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red;
        Write-Host $Razones -Fore Yellow;
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
    $RutaInstalacion = ".\Adobe\Adobe Premiere Pro $VersionAdobe\AMT"
    cd $Env:Programfiles
    cd $RutaInstalacion

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red;
        Write-Host $Razones -Fore Yellow;
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
    $RutaInstalacion = ".\Adobe\Adobe Premiere Pro $VersionAdobe\AMT"
    cd $Env:Programfiles
    cd $RutaInstalacion

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red;
        Write-Host $Razones -Fore Yellow;
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
    $RutaInstalacion = ".\Adobe\Adobe Audition $VersionAdobe\AMT"
    cd $Env:Programfiles
    cd $RutaInstalacion

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red;
        Write-Host $Razones -Fore Yellow;
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
    $RutaInstalacion = ".\Adobe\Adobe Audition $VersionAdobe\AMT"
    cd $Env:Programfiles
    cd $RutaInstalacion

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red;
        Write-Host $Razones -Fore Yellow;
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
    $RutaInstalacion1 = ".\Adobe\Adobe InDesign $VersionAdobe\Presets\InDesign Shortcut Sets"
    cd $Env:Programfiles
    cd $RutaInstalacion1

    if (Test-Path -Path $CarpetaEnUs -PathType Container) {
        Rename-Item -Path $CarpetaEnUs -NewName $CarpetaEsEs
    } elseif (Test-Path -Path $CarpetaEnGb -PathType Container) {
        Rename-Item -Path $CarpetaEnGb -NewName $CarpetaEsEs
    }

    $RutaInstalacion2 = ".\Adobe\Adobe InDesign $VersionAdobe\Presets\InDesign_Workspaces"
    cd $Env:Programfiles
    cd $RutaInstalacion2

    if (Test-Path -Path $CarpetaEnUs -PathType Container) {
        Rename-Item -Path $CarpetaEnUs -NewName $CarpetaEsEs
        Write-Host $CambioEngSpa -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } elseif (Test-Path -Path $CarpetaEnGb -PathType Container) {
        Rename-Item -Path $CarpetaEnGb -NewName $CarpetaEsEs
        Write-Host $CambioEngSpa -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red;
        Write-Host $Razones -Fore Yellow;
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
    $RutaInstalacion1 = ".\Adobe\Adobe InDesign $VersionAdobe\Presets\InDesign Shortcut Sets"
    cd $Env:Programfiles
    cd $RutaInstalacion1

    if (Test-Path -Path $CarpetaEsEs -PathType Container) {
        Rename-Item -Path $CarpetaEsEs -NewName $CarpetaEnUs
    } elseif (Test-Path -Path $CarpetaEsMx -PathType Container) {
        Rename-Item -Path $CarpetaEsMx -NewName $CarpetaEnUs
    }

    $RutaInstalacion2 = ".\Adobe\Adobe InDesign $VersionAdobe\Presets\InDesign_Workspaces"
    cd $Env:Programfiles
    cd $RutaInstalacion2

    if (Test-Path -Path $CarpetaEsEs -PathType Container) {
        Rename-Item -Path $CarpetaEsEs -NewName $CarpetaEnUs
        Write-Host $CambioSpaEng -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } elseif (Test-Path -Path $CarpetaEsMx -PathType Container) {
        Rename-Item -Path $CarpetaEsMx -NewName $CarpetaEnUs
        Write-Host $CambioSpaEng -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red;
        Write-Host $Razones -Fore Yellow;
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
    $RutaInstalacion = ".\Adobe\Adobe Media Encoder $VersionAdobe\AMT"
    cd $Env:Programfiles
    cd $RutaInstalacion

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlAllLang) -or ($_ -match $XmlEnUs) -or ($_ -match $XmlEnGb)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlAllLang) {
        $Contenido.replace($XmlAllLang,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnUs) {
        $Contenido.replace($XmlEnUs,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEnGb) {
        $Contenido.replace($XmlEnGb,$XmlEsEs) | Set-Content application.xml
        Write-Host $CambioEngSpa -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red;
        Write-Host $Razones -Fore Yellow;
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
    $RutaInstalacion = ".\Adobe\Adobe Media Encoder $VersionAdobe\AMT"
    cd $Env:Programfiles
    cd $RutaInstalacion

    $Idioma = Get-Content application.xml | Where-Object {($_ -match $XmlAllLang) -or ($_ -match $XmlEsEs) -or ($_ -match $XmlEsMx)}
    $Contenido = Get-Content application.xml

    if ($Idioma -match $XmlAllLang) {
        $Contenido.replace($XmlAllLang,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsEs) {
        $Contenido.replace($XmlEsEs,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } elseif ($Idioma -match $XmlEsMx) {
        $Contenido.replace($XmlEsMx,$XmlEnUs) | Set-Content application.xml
        Write-Host $CambioSpaEng -Fore DarkGreen;
        Start-Sleep -Seconds 1
    } else {
        Write-Host $NoCambio -Fore Red;
        Write-Host $Razones -Fore Yellow;
        Start-Sleep -Seconds 1
    }

    # Mantiene última versión elegida por el usuario en menú Adobe
    $OpcionMenu = $FreezeOpcionMenu
    #Write-Host "version elegida antes de salir del menu" $OpcionMenu -Fore Yellow;

    # Vuelve al menú
    MENU_ADOBE_SPA_A_ENG
}

# Cierra
function MENU_SALIR {
    Write-Host "`n Gracias por usar Simi.`n ¡No olvides dejarnos una reseña en www.leandroperez.art!`n" -Fore Yellow;
    Start-Sleep -Seconds 5
    Stop-Process -Id $PID
}

# Ayuda
function MENU_AYUDA {
    Write-Host "`n Gracias por usar Simi.`n En breve se abrirá la página de ayuda.`n" -Fore Yellow;
    Start-Sleep -Seconds 2
    Start-Process "https://leandroperez.art/tienda/productos-gratuitos/simi-cambia-idioma-adobe-sin-reinstalar/"
    # Vuelve al menú
    MENU_PRINCIPAL
}

MENU_PRINCIPAL