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
set /p IMAGES_ROOT="Chemin de votre dossier d'images (ex: C:\Users\MonNom\Images): "

echo.
echo Lancement en cours...
echo.

docker-compose up -d

timeout /t 5 /nobreak > nul

start http://localhost

echo.
echo ========================================
echo  Application lancee sur http://localhost
echo  Dans l'app, entrez vos chemins normalement
echo  Ex: %IMAGES_ROOT%\WT
echo      %IMAGES_ROOT%\KO
echo ========================================
pause