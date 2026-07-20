# 🐳 Docker Desktop Installation Guide

This guide explains how to install Docker Desktop to use CelluleAnalyse.

---

## Windows

### Step 1 — Enable virtualization in BIOS

Before installing Docker, make sure virtualization is enabled:

1. Restart your PC
2. At startup, press the BIOS key for your brand:

| Brand | Key |
|-------|-----|
| Lenovo | F1 or F2 |
| Dell | F2 |
| HP | F10 or F2 |
| Asus | DEL or F2 |
| Acer | F2 |

3. Go to **Security → Virtualization**
4. Enable **Intel Virtualization Technology** → `[Enabled]`
5. Press **F10** to save and restart

### Step 2 — Install WSL2

Open **cmd as administrator** (right-click on cmd → Run as administrator) and run:

```
wsl --install --no-distribution
```

Restart your PC, then:

```
wsl --install -d Ubuntu
```

Wait for the installation to complete and create a Ubuntu username/password when prompted.

### Step 3 — Install Docker Desktop

1. Download **[Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)**
2. Run the installer
3. During installation, select **"Use WSL 2"** ✅ (recommended)
4. Complete the installation and restart if prompted

### Step 4 — Verify installation

Open Docker Desktop from the Start menu and wait until the whale icon is **stable** in the taskbar.

Then in cmd:
```
docker --version
```

If you see a version number → Docker is ready!

---

## Mac

### Step 1 — Install Docker Desktop

1. Download **[Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)**
2. Choose the version for your processor:
   - **Apple Silicon (M1/M2/M3)** → Docker Desktop for Mac (Apple Silicon)
   - **Intel** → Docker Desktop for Mac (Intel)
3. Drag Docker into the Applications folder
4. Open Docker Desktop and wait until the icon is stable

### Step 2 — Verify installation

In Terminal:
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

Log out and log back in to apply permissions.

---

## ✅ Docker is installed — back to the main guide

Once Docker is installed and running, go back to the main page:

👉 **[Back to Quick Start](https://github.com/Millimono/CelluleAnalyse#-quick-start--for-end-users-no-coding-required)**

And download the 3 launcher files!
