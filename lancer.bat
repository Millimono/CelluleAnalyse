@echo off
echo ========================================
echo     CelluleAnalyse - Lancement
echo ========================================
echo.
echo Votre dossier doit etre organise ainsi :
echo.
echo  MonDossier/
echo      WT/
echo          fichier1.nd2
echo      KO/
echo          fichier1.nd2
echo.
set /p IMAGES_ROOT="Chemin de votre dossier d'images (ex: E:\MesImages): "
set IMAGES_ROOT=%IMAGES_ROOT:"=%

:: Extraire la lettre du lecteur et la convertir en minuscule
set DRIVE_UP=%IMAGES_ROOT:~0,1%
for %%a in (A B C D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if /I "%DRIVE_UP%"=="%%a" (
        set DRIVE_LOW=%%a
    )
)
:: Convertir en minuscule manuellement
set DRIVE_LOW=%DRIVE_UP%
if "%DRIVE_UP%"=="A" set DRIVE_LOW=a
if "%DRIVE_UP%"=="B" set DRIVE_LOW=b
if "%DRIVE_UP%"=="C" set DRIVE_LOW=c
if "%DRIVE_UP%"=="D" set DRIVE_LOW=d
if "%DRIVE_UP%"=="E" set DRIVE_LOW=e
if "%DRIVE_UP%"=="F" set DRIVE_LOW=f
if "%DRIVE_UP%"=="G" set DRIVE_LOW=g
if "%DRIVE_UP%"=="H" set DRIVE_LOW=h
if "%DRIVE_UP%"=="I" set DRIVE_LOW=i
if "%DRIVE_UP%"=="J" set DRIVE_LOW=j
if "%DRIVE_UP%"=="K" set DRIVE_LOW=k
if "%DRIVE_UP%"=="L" set DRIVE_LOW=l
if "%DRIVE_UP%"=="M" set DRIVE_LOW=m
if "%DRIVE_UP%"=="N" set DRIVE_LOW=n
if "%DRIVE_UP%"=="O" set DRIVE_LOW=o
if "%DRIVE_UP%"=="P" set DRIVE_LOW=p
if "%DRIVE_UP%"=="Q" set DRIVE_LOW=q
if "%DRIVE_UP%"=="R" set DRIVE_LOW=r
if "%DRIVE_UP%"=="S" set DRIVE_LOW=s
if "%DRIVE_UP%"=="T" set DRIVE_LOW=t
if "%DRIVE_UP%"=="U" set DRIVE_LOW=u
if "%DRIVE_UP%"=="V" set DRIVE_LOW=v
if "%DRIVE_UP%"=="W" set DRIVE_LOW=w
if "%DRIVE_UP%"=="X" set DRIVE_LOW=x
if "%DRIVE_UP%"=="Y" set DRIVE_LOW=y
if "%DRIVE_UP%"=="Z" set DRIVE_LOW=z

:: Extraire le chemin sans la lettre de lecteur (ex: E:\MesImages → MesImages)
set PATH_ONLY=%IMAGES_ROOT:~3%

:: Remplacer les backslashes par des slashes
set PATH_ONLY=%PATH_ONLY:\=/%

:: Construire le chemin Docker
set DOCKER_PATH=/mnt/host/%DRIVE_LOW%/%PATH_ONLY%

echo.
echo Chemin Windows  : %IMAGES_ROOT%
echo Chemin Docker   : %DOCKER_PATH%
echo.

:: Ecrire dans .env
echo IMAGES_ROOT=%IMAGES_ROOT%> .env
echo DOCKER_PATH=%DOCKER_PATH%>> .env

echo Lancement en cours...
echo.

docker-compose down
docker-compose up -d

timeout /t 5 /nobreak > nul

start http://localhost

echo.
echo ========================================
echo  Application lancee sur http://localhost
echo  Dans l'app, entrez vos chemins :
echo  Ex: %IMAGES_ROOT%\WT
echo      %IMAGES_ROOT%\KO
echo ========================================
pause