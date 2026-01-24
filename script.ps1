# Simi v1.0
# Cambiá el idioma de los programas de Adobe sin reinstalarlos
# https://leandroperez.art/tienda/productos-gratuitos/simi-cambia-idioma-adobe-sin-reinstalar/
# © Leandro Pérez
# Por el momento sólo funciona con español de España e inglés de Estados Unidos

Function Menu ($MenuNumero, $MenuCierra, $NombreMenu, $NombreFuncionMenu, $OpcionMenu1, $MenuFuncion1, $OpcionMenu2, $MenuFuncion2, $OpcionMenu3, $MenuFuncion3, $OpcionMenu4, $MenuFuncion4, $OpcionMenu5, $MenuFuncion5, $OpcionMenu6, $MenuFuncion6, $OpcionMenu7, $MenuFuncion7, $OpcionMenu8, $MenuFuncion8, $OpcionMenu9, $MenuFuncion9, $OpcionMenu10, $MenuFuncion10)
{
    Write-Host "`n$NombreMenu`n" -Fore Gray;
    if($OpcionMenu1 -ne $null){Write-Host " $OpcionMenu1" -Fore Gray;}
    if($OpcionMenu2 -ne $null){Write-Host " $OpcionMenu2" -Fore Gray;}
    if($OpcionMenu3 -ne $null){Write-Host " $OpcionMenu3" -Fore Gray;}
    if($OpcionMenu4 -ne $null){Write-Host " $OpcionMenu4" -Fore Gray;}
    if($OpcionMenu5 -ne $null){Write-Host " $OpcionMenu5" -Fore Gray;}
    if($OpcionMenu6 -ne $null){Write-Host " $OpcionMenu6" -Fore Gray;}
    if($OpcionMenu7 -ne $null){Write-Host " $OpcionMenu7" -Fore Gray;}
    if($OpcionMenu8 -ne $null){Write-Host " $OpcionMenu8" -Fore Gray;}
    if($OpcionMenu9 -ne $null){Write-Host " $OpcionMenu9" -Fore Gray;}
    if($OpcionMenu10 -ne $null){Write-Host " $OpcionMenu9" -Fore Gray;}
   [int]$OpcionMenu = Read-Host "`n Tipeá una opción y presioná Enter"
        
        if(($OpcionMenu -lt $MenuNumero) -or ($OpcionMenu -gt $MenuCierra))
        {
            Write-Host " `nTipeá una de las opciones que están arriba.`n" -Fore Red;Start-Sleep -Seconds 1
            Invoke-Expression $NombreFuncionMenu
        }
        else
        {
            if($OpcionMenu -eq $MenuNumero) {Invoke-Expression $MenuFuncion1}
            if($OpcionMenu -eq ($MenuNumero + "1")) {Invoke-Expression $MenuFuncion2}
            if($OpcionMenu -eq ($MenuNumero + "2")) {Invoke-Expression $MenuFuncion3}   
            if($OpcionMenu -eq ($MenuNumero + "3")) {Invoke-Expression $MenuFuncion4} 
            if($OpcionMenu -eq ($MenuNumero + "4")) {Invoke-Expression $MenuFuncion5} 
            if($OpcionMenu -eq ($MenuNumero + "5")) {Invoke-Expression $MenuFuncion6} 
            if($OpcionMenu -eq ($MenuNumero + "6")) {Invoke-Expression $MenuFuncion7} 
            if($OpcionMenu -eq ($MenuNumero + "7")) {Invoke-Expression $MenuFuncion8}
            if($OpcionMenu -eq ($MenuNumero + "8")) {Invoke-Expression $MenuFuncion9} 
            if($OpcionMenu -eq ($MenuNumero + "9")) {Invoke-Expression $MenuFuncion10}
        }
}

# Menú principal, elige idiomas
function MENU_PRINCIPAL
{
Write-Host "`n`n Simi v1.0 - © Leandro Pérez`n Cambiá el idioma de Adobe sin reinstalar los programas" -Fore DarkGray;
Menu 1 4 "`n Menú principal`n ==============" MENU_PRINCIPAL "1. Cambiar de inglés a español" MENU_ENG_A_SPA_PRINCIPAL "2. Cambiar de español a inglés" MENU_SPA_A_ENG_PRINCIPAL "3. Salir" MENU_SALIR "4. Ayuda" MENU_AYUDA
}

# Menú inglés a español
function MENU_ENG_A_SPA_PRINCIPAL
{
Menu 1 7 "`n Cambiar de inglés a español`n ===========================" MENU_ENG_A_SPA_PRINCIPAL "1. Adobe 2021" MENU_ADOBE_2021_ENG_A_SPA "2. Adobe 2020" MENU_ADOBE_2020_ENG_A_SPA "3. Adobe 2019" MENU_ADOBE_2019_ENG_A_SPA "4. Adobe 2018" MENU_ADOBE_2018_ENG_A_SPA "5. Menú principal" MENU_PRINCIPAL "6. Salir" MENU_SALIR "7. Ayuda" MENU_AYUDA
}

# Menú español a inglés
function MENU_SPA_A_ENG_PRINCIPAL
{
Menu 1 7 "`n Cambiar de español a inglés`n ===========================" MENU_SPA_A_ENG_PRINCIPAL "1. Adobe 2021" MENU_ADOBE_2021_SPA_A_ENG "2. Adobe 2020" MENU_ADOBE_2020_SPA_A_ENG "3. Adobe 2019" MENU_ADOBE_2019_SPA_A_ENG "4. Adobe 2018" MENU_ADOBE_2018_SPA_A_ENG "5. Menú principal" MENU_PRINCIPAL "6. Salir" MENU_SALIR "7. Ayuda" MENU_AYUDA
}

# Menú Adobe 2021, inglés a español
function MENU_ADOBE_2021_ENG_A_SPA
{
Menu 1 8 "`n Adobe 2021`n ==========" MENU_ADOBE_2021_ENG_A_SPA "1. After Effects" MENU_AE_2021_ENG_A_SPA "2. Premiere Pro" MENU_PPRO_2021_ENG_A_SPA "3. Audition" MENU_AUDI_2021_ENG_A_SPA "4. InDesign" MENU_IND_2021_ENG_A_SPA "5. Media Encoder" MENU_ME_2021_ENG_A_SPA "6. Menú principal" MENU_PRINCIPAL "7. Salir" MENU_SALIR "8. Ayuda" MENU_AYUDA
}

# Menú Adobe 2021, español a inglés
function MENU_ADOBE_2021_SPA_A_ENG
{
Menu 1 8 "`n Adobe 2021`n ==========" MENU_ADOBE_2021_SPA_A_ENG "1. After Effects" MENU_AE_2021_SPA_A_ENG "2. Premiere Pro" MENU_PPRO_2021_SPA_A_ENG "3. Audition" MENU_AUDI_2021_SPA_A_ENG "4. InDesign" MENU_IND_2021_SPA_A_ENG "5. Media Encoder" MENU_ME_2021_SPA_A_ENG "6. Menú principal" MENU_PRINCIPAL "7. Salir" MENU_SALIR "8. Ayuda" MENU_AYUDA
}

# Menú Adobe 2020, inglés a español
function MENU_ADOBE_2020_ENG_A_SPA
{
Menu 1 8 "`n Adobe 2020`n ==========" MENU_ADOBE_2020_ENG_A_SPA "1. After Effects" MENU_AE_2020_ENG_A_SPA "2. Premiere Pro" MENU_PPRO_2020_ENG_A_SPA "3. Audition" MENU_AUDI_2020_ENG_A_SPA "4. InDesign" MENU_IND_2020_ENG_A_SPA "5. Media Encoder" MENU_ME_2020_ENG_A_SPA "6. Menú principal" MENU_PRINCIPAL "7. Salir" MENU_SALIR "8. Ayuda" MENU_AYUDA
}

# Menú Adobe 2020, español a inglés
function MENU_ADOBE_2020_SPA_A_ENG
{
Menu 1 8 "`n Adobe 2020`n ==========" MENU_ADOBE_2020_SPA_A_ENG "1. After Effects" MENU_AE_2020_SPA_A_ENG "2. Premiere Pro" MENU_PPRO_2020_SPA_A_ENG "3. Audition" MENU_AUDI_2020_SPA_A_ENG "4. InDesign" MENU_IND_2020_SPA_A_ENG "5. Media Encoder" MENU_ME_2020_SPA_A_ENG "6. Menú principal" MENU_PRINCIPAL "7. Salir" MENU_SALIR "8. Ayuda" MENU_AYUDA
}

# Menú Adobe 2019, inglés a español
function MENU_ADOBE_2019_ENG_A_SPA
{
Menu 1 8 "`n Adobe 2019`n ==========" MENU_ADOBE_2019_ENG_A_SPA "1. After Effects" MENU_AE_2019_ENG_A_SPA "2. Premiere Pro" MENU_PPRO_2019_ENG_A_SPA "3. Audition" MENU_AUDI_2019_ENG_A_SPA "4. InDesign" MENU_IND_2019_ENG_A_SPA "5. Media Encoder" MENU_ME_2019_ENG_A_SPA "6. Menú principal" MENU_PRINCIPAL "7. Salir" MENU_SALIR "8. Ayuda" MENU_AYUDA
}

# Menú Adobe 2019, español a inglés
function MENU_ADOBE_2019_SPA_A_ENG
{
Menu 1 8 "`n Adobe 2019`n ==========" MENU_ADOBE_2019_SPA_A_ENG "1. After Effects" MENU_AE_2019_SPA_A_ENG "2. Premiere Pro" MENU_PPRO_2019_SPA_A_ENG "3. Audition" MENU_AUDI_2019_SPA_A_ENG "4. InDesign" MENU_IND_2019_SPA_A_ENG "5. Media Encoder" MENU_ME_2019_SPA_A_ENG "6. Menú principal" MENU_PRINCIPAL "7. Salir" MENU_SALIR "8. Ayuda" MENU_AYUDA
}

# Menú Adobe 2018, inglés a español
function MENU_ADOBE_2018_ENG_A_SPA
{
Menu 1 8 "`n Adobe 2018`n ==========" MENU_ADOBE_2018_ENG_A_SPA "1. After Effects" MENU_AE_2018_ENG_A_SPA "2. Premiere Pro" MENU_PPRO_2018_ENG_A_SPA "3. Audition" MENU_AUDI_2018_ENG_A_SPA "4. InDesign" MENU_IND_2018_ENG_A_SPA "5. Media Encoder" MENU_ME_2018_ENG_A_SPA "6. Menú principal" MENU_PRINCIPAL "7. Salir" MENU_SALIR "8. Ayuda" MENU_AYUDA
}

# Menú Adobe 2018, español a inglés
function MENU_ADOBE_2018_SPA_A_ENG
{
Menu 1 8 "`n Adobe 2018`n ==========" MENU_ADOBE_2018_SPA_A_ENG "1. After Effects" MENU_AE_2018_SPA_A_ENG "2. Premiere Pro" MENU_PPRO_2018_SPA_A_ENG "3. Audition" MENU_AUDI_2018_SPA_A_ENG "4. InDesign" MENU_IND_2018_SPA_A_ENG "5. Media Encoder" MENU_ME_2018_SPA_A_ENG "6. Menú principal" MENU_PRINCIPAL "7. Salir" MENU_SALIR "8. Ayuda" MENU_AYUDA
}

# Menú After Effects 2021, inglés a español
function MENU_AE_2021_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe After Effects 2021\Support Files\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2021.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de After Effects 2021!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2021_ENG_A_SPA
}

# Menú After Effects 2021, español a inglés
function MENU_AE_2021_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe After Effects 2021\Support Files\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2021.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de After Effects 2021!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2021_SPA_A_ENG
}

# Menú Premiere Pro 2021, inglés a español
function MENU_PPRO_2021_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Premiere Pro 2021\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2021.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Premiere Pro 2021!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2021_ENG_A_SPA
}

# Menú Premiere Pro 2021, español a inglés
function MENU_PPRO_2021_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Premiere Pro 2021\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2021.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Premiere Pro 2021!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2021_SPA_A_ENG
}

# Menú Audition 2021, inglés a español
function MENU_AUDI_2021_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Audition 2021\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2021.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Audition 2021!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2021_ENG_A_SPA
}

# Menú Audition 2021, español a inglés
function MENU_AUDI_2021_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Audition 2021\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2021.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Audition 2021!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2021_SPA_A_ENG
}

# Menú InDesign 2021, inglés a español
function MENU_IND_2021_ENG_A_SPA
{
$Carpeta = 'en_US'

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2021\Presets\InDesign Shortcut Sets'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item en_US es_ES
}

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2021\Presets\InDesign_Workspaces'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item en_US es_ES
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2021.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
} else {
    Write-Host "`n ¡No se pudo cambiar el idioma de InDesign 2021!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2021_ENG_A_SPA
}

# Menú InDesign 2021, español a inglés
function MENU_IND_2021_SPA_A_ENG
{
$Carpeta = 'es_ES'

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2021\Presets\InDesign Shortcut Sets'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item es_ES en_US
}

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2021\Presets\InDesign_Workspaces'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item es_ES en_US
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2021.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
} else {
    Write-Host "`n ¡No se pudo cambiar el idioma de InDesign 2021!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2021_SPA_A_ENG
}

# Menú Media Encoder 2021, inglés a español
function MENU_ME_2021_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Media Encoder 2021\AMT'

$Idioma1 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*'}
$Idioma2 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma1 -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2021.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
elseif ( $Idioma2 -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2021.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Media Encoder 2021!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2021_ENG_A_SPA
}

# Menú Media Encoder 2021, español a inglés
function MENU_ME_2021_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Media Encoder 2021\AMT'

$Idioma1 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*'}
$Idioma2 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma1 -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2021.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
elseif ( $Idioma2 -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2021.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Media Encoder 2021!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2021_SPA_A_ENG
}

# Menú After Effects 2020, inglés a español
function MENU_AE_2020_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe After Effects 2020\Support Files\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2020.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de After Effects 2020!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2020_ENG_A_SPA
}

# Menú After Effects 2020, español a inglés
function MENU_AE_2020_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe After Effects 2020\Support Files\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2020.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de After Effects 2020!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2020_SPA_A_ENG
}

# Menú Premiere Pro 2020, inglés a español
function MENU_PPRO_2020_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Premiere Pro 2020\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2020.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Premiere Pro 2020!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2020_ENG_A_SPA
}

# Menú Premiere Pro 2020, español a inglés
function MENU_PPRO_2020_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Premiere Pro 2020\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2020.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Premiere Pro 2020!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2020_SPA_A_ENG
}

# Menú Audition 2020, inglés a español
function MENU_AUDI_2020_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Audition 2020\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2020.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Audition 2020!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2020_ENG_A_SPA
}

# Menú Audition 2020, español a inglés
function MENU_AUDI_2020_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Audition 2020\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2020.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Audition 2020!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2020_SPA_A_ENG
}

# Menú InDesign 2020, inglés a español
function MENU_IND_2020_ENG_A_SPA
{
$Carpeta = 'en_US'

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2020\Presets\InDesign Shortcut Sets'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item en_US es_ES
}

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2020\Presets\InDesign_Workspaces'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item en_US es_ES
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2020.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
} else {
    Write-Host "`n ¡No se pudo cambiar el idioma de InDesign 2020!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2020_ENG_A_SPA
}

# Menú InDesign 2020, español a inglés
function MENU_IND_2020_SPA_A_ENG
{
$Carpeta = 'es_ES'

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2020\Presets\InDesign Shortcut Sets'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item es_ES en_US
}

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2020\Presets\InDesign_Workspaces'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item es_ES en_US
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2020.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
} else {
    Write-Host "`n ¡No se pudo cambiar el idioma de InDesign 2020!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2020_SPA_A_ENG
}

# Menú Media Encoder 2020, inglés a español
function MENU_ME_2020_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Media Encoder 2020\AMT'

$Idioma1 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*'}
$Idioma2 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma1 -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2020.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
elseif ( $Idioma2 -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2020.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Media Encoder 2020!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2020_ENG_A_SPA
}

# Menú Media Encoder 2020, español a inglés
function MENU_ME_2020_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Media Encoder 2020\AMT'

$Idioma1 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*'}
$Idioma2 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma1 -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2020.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
elseif ( $Idioma2 -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2020.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Media Encoder 2020!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2020_SPA_A_ENG
}

# Menú After Effects 2019, inglés a español
function MENU_AE_2019_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe After Effects 2019\Support Files\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2019.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de After Effects 2019!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2019_ENG_A_SPA
}

# Menú After Effects 2019, español a inglés
function MENU_AE_2019_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe After Effects 2019\Support Files\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2019.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de After Effects 2019!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2019_SPA_A_ENG
}

# Menú Premiere Pro 2019, inglés a español
function MENU_PPRO_2019_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Premiere Pro 2019\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2019.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Premiere Pro 2019!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2019_ENG_A_SPA
}

# Menú Premiere Pro 2019, español a inglés
function MENU_PPRO_2019_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Premiere Pro 2019\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2019.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Premiere Pro 2019!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2019_SPA_A_ENG
}

# Menú Audition 2019, inglés a español
function MENU_AUDI_2019_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Audition 2019\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2019.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Audition 2019!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2019_ENG_A_SPA
}

# Menú Audition 2019, español a inglés
function MENU_AUDI_2019_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Audition 2019\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2019.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Audition 2019!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2019_SPA_A_ENG
}

# Menú InDesign 2019, inglés a español
function MENU_IND_2019_ENG_A_SPA
{
$Carpeta = 'en_US'

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2019\Presets\InDesign Shortcut Sets'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item en_US es_ES
}

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2019\Presets\InDesign_Workspaces'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item en_US es_ES
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2019.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
} else {
    Write-Host "`n ¡No se pudo cambiar el idioma de InDesign 2019!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2019_ENG_A_SPA
}

# Menú InDesign 2019, español a inglés
function MENU_IND_2019_SPA_A_ENG
{
$Carpeta = 'es_ES'

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2019\Presets\InDesign Shortcut Sets'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item es_ES en_US
}

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2019\Presets\InDesign_Workspaces'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item es_ES en_US
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2019.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
} else {
    Write-Host "`n ¡No se pudo cambiar el idioma de InDesign 2019!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2019_SPA_A_ENG
}

# Menú Media Encoder 2019, inglés a español
function MENU_ME_2019_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Media Encoder 2019\AMT'

$Idioma1 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*'}
$Idioma2 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma1 -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2019.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
elseif ( $Idioma2 -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2019.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Media Encoder 2019!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2019_ENG_A_SPA
}

# Menú Media Encoder 2019, español a inglés
function MENU_ME_2019_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Media Encoder 2019\AMT'

$Idioma1 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*'}
$Idioma2 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma1 -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2019.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
elseif ( $Idioma2 -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2019.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Media Encoder 2019!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2019_SPA_A_ENG
}

# Menú After Effects 2018, inglés a español
function MENU_AE_2018_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe After Effects 2018\Support Files\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2018.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de After Effects 2018!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2018_ENG_A_SPA
}

# Menú After Effects 2018, español a inglés
function MENU_AE_2018_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe After Effects 2018\Support Files\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2018.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de After Effects 2018!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2018_SPA_A_ENG
}

# Menú Premiere Pro 2018, inglés a español
function MENU_PPRO_2018_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Premiere Pro 2018\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2018.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Premiere Pro 2018!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2018_ENG_A_SPA
}

# Menú Premiere Pro 2018, español a inglés
function MENU_PPRO_2018_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Premiere Pro 2018\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2018.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Premiere Pro 2018!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2018_SPA_A_ENG
}

# Menú Audition 2018, inglés a español
function MENU_AUDI_2018_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Audition 2018\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2018.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Audition 2018!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2018_ENG_A_SPA
}

# Menú Audition 2018, español a inglés
function MENU_AUDI_2018_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Audition 2018\AMT'

$Idioma = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2018.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
    else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Audition 2018!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2018_SPA_A_ENG
}

# Menú InDesign 2018, inglés a español
function MENU_IND_2018_ENG_A_SPA
{
$Carpeta = 'en_US'

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2018\Presets\InDesign Shortcut Sets'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item en_US es_ES
}

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2018\Presets\InDesign_Workspaces'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item en_US es_ES
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2018.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
} else {
    Write-Host "`n ¡No se pudo cambiar el idioma de InDesign 2018!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2018_ENG_A_SPA
}

# Menú InDesign 2018, español a inglés
function MENU_IND_2018_SPA_A_ENG
{
$Carpeta = 'es_ES'

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2018\Presets\InDesign Shortcut Sets'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item es_ES en_US
}

cd $Env:Programfiles
cd '.\Adobe\Adobe InDesign 2018\Presets\InDesign_Workspaces'

if ( Test-Path -Path $Carpeta ) {
    Rename-Item es_ES en_US
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2018.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
} else {
    Write-Host "`n ¡No se pudo cambiar el idioma de InDesign 2018!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2018_SPA_A_ENG
}

# Menú Media Encoder 2018, inglés a español
function MENU_ME_2018_ENG_A_SPA
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Media Encoder 2018\AMT'

$Idioma1 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*'}
$Idioma2 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">en_US</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma1 -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2018.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
elseif ( $Idioma2 -like '*<Data key="installedLanguages">en_US</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">en_US</Data>','<Data key="installedLanguages">es_ES</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de inglés a español correctamente.`n Ahora regresarás al menú Adobe 2018.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Media Encoder 2018!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el inglés de Estados Unidos (en_US).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2018_ENG_A_SPA
}

# Menú Media Encoder 2018, español a inglés
function MENU_ME_2018_SPA_A_ENG
{
cd $Env:Programfiles
cd '.\Adobe\Adobe Media Encoder 2018\AMT'

$Idioma1 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*'}
$Idioma2 = Get-Content application.xml | Where-Object {$_ -like '*<Data key="installedLanguages">es_ES</Data>*'}
$Contenido = Get-Content application.xml

if ( $Idioma1 -like '*<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">cs_CZ,da_DK,de_DE,en_AE,en_GB,en_IL,en_US,es_ES,es_MX,fi_FI,fr_CA,fr_FR,fr_MA,hu_HU,it_IT,ja_JP,ko_KR,nb_NO,nl_NL,pl_PL,pt_BR,ru_RU,sv_SE,tr_TR,uk_UA,zh_CN,zh_TW</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2018.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
elseif ( $Idioma2 -like '*<Data key="installedLanguages">es_ES</Data>*' )
{
    $Contenido.replace('<Data key="installedLanguages">es_ES</Data>','<Data key="installedLanguages">en_US</Data>') | Set-Content application.xml
    Write-Host "`n Se cambió el idioma de español a inglés correctamente.`n Ahora regresarás al menú Adobe 2018.`n" -Fore DarkGreen;
    Start-Sleep -Seconds 1
}
else
{
    Write-Host "`n ¡No se pudo cambiar el idioma de Media Encoder 2018!" -Fore Red;
    Write-Host "`n Puede ser por diferentes razones:`n - El programa no está configurado con el español de España (es_ES).`n - El programa no se instaló usando la aplicación Creative Cloud." -Fore Yellow;
    Start-Sleep -Seconds 1
}

MENU_ADOBE_2018_SPA_A_ENG
}

function MENU_SALIR
{
Write-Host "`n Gracias por usar Simi.`n ¡No olvides dejarme una reseña en www.leandroperez.art!`n" -Fore Yellow;
Start-Sleep -Seconds 5
Stop-Process -Id $PID
}

function MENU_AYUDA
{
Write-Host "`n Gracias por usar Simi.`n En breve se abrirá la página de ayuda.`n" -Fore Yellow;
Start-Sleep -Seconds 2
Start-Process "https://leandroperez.art/tienda/productos-gratuitos/simi-cambia-idioma-adobe-sin-reinstalar/"

MENU_PRINCIPAL
}

MENU_PRINCIPAL