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

# Construire le chemin Docker selon l'OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    DOCKER_PATH="/host_mnt${IMAGES_ROOT}"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    DOCKER_PATH="$IMAGES_ROOT"
else
    DOCKER_PATH="$IMAGES_ROOT"
fi

export DOCKER_PATH="$DOCKER_PATH"

# Ecrire dans .env
echo "IMAGES_ROOT=$IMAGES_ROOT" > .env
echo "DOCKER_PATH=$DOCKER_PATH" >> .env

echo ""
echo "Chemin images  : $IMAGES_ROOT"
echo "Chemin Docker  : $DOCKER_PATH"
echo "Lancement en cours..."
echo ""

# Vérifier si Docker est démarré
echo "Vérification de Docker Desktop..."
if ! docker info > /dev/null 2>&1; then
    echo ""
    echo "========================================"
    echo " ERREUR : Docker Desktop n'est pas demarre !"
    echo " Veuillez :"
    echo " 1. Ouvrir Docker Desktop"
    echo " 2. Attendre que l'icone soit stable"
    echo " 3. Relancer ce script"
    echo "========================================"
    exit 1
fi
echo "Docker Desktop est actif."
echo ""

docker-compose -f docker-compose.yml down
docker-compose -f docker-compose.yml pull
docker-compose -f docker-compose.yml up -d

sleep 5

if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://localhost
fi

echo ""
echo "========================================"
echo " Application lancee sur http://localhost"
echo " Dans l'app, entrez vos chemins :"
echo " Ex: $IMAGES_ROOT/WT"
echo "     $IMAGES_ROOT/KO"
echo "========================================"
