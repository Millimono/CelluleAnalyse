#!/bin/bash

echo "========================================"
echo "    CelluleAnalyse - Lancement"
echo "========================================"
echo ""
echo "Votre dossier doit etre organise ainsi :"
echo ""
echo "  MonDossier/"
echo "      WT/"
echo "          fichier1.nd2"
echo "      KO/"
echo "          fichier1.nd2"
echo ""
read -p "Chemin de votre dossier d'images (ex: /Users/MonNom/Images): " IMAGES_ROOT

export IMAGES_ROOT="$IMAGES_ROOT"

echo ""
echo "Lancement en cours..."
echo ""

docker-compose up -d

sleep 5

# Ouvrir le navigateur selon l'OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://localhost
fi

echo ""
echo "========================================"
echo " Application lancee sur http://localhost"
echo " Dans l'app, entrez vos chemins normalement"
echo " Ex: $IMAGES_ROOT/WT"
echo "     $IMAGES_ROOT/KO"
echo "========================================"
