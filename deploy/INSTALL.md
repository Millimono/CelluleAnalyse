# 🐳 Guide d'installation — Docker Desktop

Ce guide vous explique comment installer Docker Desktop pour utiliser CelluleAnalyse.

---

## Windows

### Étape 1 — Activer la virtualisation dans le BIOS

Avant d'installer Docker, vérifiez que la virtualisation est activée :

1. Redémarrez votre PC
2. Au démarrage, appuyez sur la touche BIOS selon votre marque :

| Marque | Touche |
|--------|--------|
| Lenovo | F1 ou F2 |
| Dell | F2 |
| HP | F10 ou F2 |
| Asus | DEL ou F2 |
| Acer | F2 |

3. Allez dans **Security → Virtualization**
4. Activez **Intel Virtualization Technology** → `[Enabled]`
5. Appuyez sur **F10** pour sauvegarder et redémarrer

### Étape 2 — Installer WSL2

Ouvrez **cmd en administrateur** (clic droit sur cmd → Exécuter en tant qu'administrateur) et lancez :

```
wsl --install --no-distribution
```

Redémarrez le PC, puis :

```
wsl --install -d Ubuntu
```

Attendez la fin de l'installation et créez un nom d'utilisateur/mot de passe Ubuntu quand demandé.

### Étape 3 — Installer Docker Desktop

1. Téléchargez **[Docker Desktop pour Windows](https://www.docker.com/products/docker-desktop)**
2. Lancez l'installateur
3. Lors de l'installation, sélectionnez **"Use WSL 2"** ✅ (recommandé)
4. Terminez l'installation et redémarrez si demandé

### Étape 4 — Vérifier l'installation

Ouvrez Docker Desktop depuis le menu démarrer et attendez que l'icône baleine soit **stable** dans la barre des tâches.

Ensuite dans cmd :
```
docker --version
```

Si vous voyez un numéro de version → Docker est prêt !

---

## Mac

### Étape 1 — Installer Docker Desktop

1. Téléchargez **[Docker Desktop pour Mac](https://www.docker.com/products/docker-desktop)**
2. Choisissez la version selon votre processeur :
   - **Apple Silicon (M1/M2/M3)** → Docker Desktop for Mac (Apple Silicon)
   - **Intel** → Docker Desktop for Mac (Intel)
3. Glissez Docker dans le dossier Applications
4. Ouvrez Docker Desktop et attendez que l'icône soit stable

### Étape 2 — Vérifier l'installation

Dans le Terminal :
```bash
docker --version
```

---

## Linux

### Ubuntu / Debian

```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl start docker
sudo usermod -aG docker $USER
```

Déconnectez-vous et reconnectez-vous pour appliquer les permissions.

---

## ✅ Docker est installé — retourner au guide principal

Une fois Docker installé et démarré, retournez sur la page principale :

👉 **[Retour au Quick Start](https://github.com/Millimono/CelluleAnalyse#-quick-start--for-end-users-no-coding-required)**

Et téléchargez les 3 fichiers de lancement !
