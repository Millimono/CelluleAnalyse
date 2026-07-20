# CelluleAnalyse 🔬

A modular, containerized web platform for automated fluorescence microscopy image analysis.

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.11-green)
![React](https://img.shields.io/badge/react-18-61dafb)
![FastAPI](https://img.shields.io/badge/fastapi-0.128-009688)
![Docker](https://img.shields.io/badge/docker-ready-2496ED)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Overview

**CelluleAnalyse** is a production-ready web platform for automated analysis of fluorescence microscopy images (`.nd2`, `.czi`, `.tiff`). It provides a complete pipeline from image loading to statistical reporting, with a modular architecture that supports multiple detection methods — from classical thresholding to deep learning.

| Feature | Description | Status |
|---------|-------------|--------|
| 🔵 Nucleus detection | Automated detection from DAPI/DNA channel | ✅ Stable |
| 🔬 Cell classification | Interphase vs mitosis classification | ✅ Stable |
| 📊 Fluorescence measurement | Intensity quantification in mitotic spindles | 🔄 In development |
| 📈 Group comparison | Statistical comparison between two conditions | 🔄 In development |
| 🧠 ML/DL detection | Cellpose, StarDist integration | 🔄 In development |

---

## 📸 Screenshots

> Dashboard with image viewer, pipeline status, and analysis configuration

![Dashboard](docs/images/dashboard.png)

---

## 🚀 Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed
- `.nd2` image files organized in subfolders:

```
YourImagesFolder/
    GroupA/          ← e.g. WT (wild-type)
        image1.nd2
        image2.nd2
    GroupB/          ← e.g. MAP6_KO
        image1.nd2
        image2.nd2
```

### Windows

```batch
double-click lancer.bat
```

Enter the path to your images folder when prompted. The app opens automatically at **http://localhost**.

### Mac / Linux

```bash
chmod +x lancer.sh
./lancer.sh
```

Enter the path to your images folder when prompted. Open **http://localhost** in your browser.

---

## 🖥️ Usage

### 1. Load your image groups

Click **"Load WT folder"** and enter the full path to your first group.  
Click **"Load KO folder"** and enter the full path to your second group.

### 2. Explore images

Select any file from the sidebar to visualize it in the viewer:
- Switch between **ADN**, **Acetylation**, **Polyglutamylation**, and **Composite** channels
- Navigate Z-planes with the slider or ‹ › buttons
- Open any image **full screen** for detailed inspection
- Images are progressively cached — navigation becomes instantaneous

### 3. Configure and run analysis

In the **Analysis panel**:
- Choose scope: current file or entire group
- Select analyses: cell counting, fluorescence intensity measurement
- Choose detection method: Otsu thresholding, Cellpose (ML), StarDist (DL)
- Click **Launch analysis**

### 4. View results

- Detection overlay appears directly on the image (🔬 Analysis mode toggle)
- Metrics update in the dashboard: total cells, mitoses, % mitosis
- Pipeline status tracks each completed step

---

## 🏗️ Architecture

```
CelluleAnalyse/
├── backend/                          # FastAPI Python backend
│   ├── api/
│   │   ├── routes_chargement.py      # File loading routes
│   │   ├── routes_visualisation.py   # Image rendering routes
│   │   ├── routes_analyse.py         # Analysis routes
│   │   └── routes_rapport.py         # Report generation (coming soon)
│   ├── modules/
│   │   ├── chargement/
│   │   │   ├── loader_nd2.py         # Nikon .nd2 reader
│   │   │   ├── loader_czi.py         # Zeiss .czi reader (coming soon)
│   │   │   └── projection_z.py       # 3D → 2D Z-projection (max/mean/sum)
│   │   ├── detection_noyaux/
│   │   │   ├── base_detector.py      # Abstract detector interface
│   │   │   ├── detector_threshold.py # Otsu thresholding + watershed
│   │   │   ├── detector_cellpose.py  # Cellpose ML (coming soon)
│   │   │   └── detector_stardist.py  # StarDist DL (coming soon)
│   │   ├── classification/
│   │   │   ├── base_classifier.py    # Abstract classifier interface
│   │   │   ├── classifier_shape.py   # Geometric shape classifier
│   │   │   ├── classifier_ml.py      # ML classifier (coming soon)
│   │   │   └── classifier_dl.py      # DL classifier (coming soon)
│   │   ├── detection_fuseau/
│   │   │   ├── base_fuseau.py        # Abstract spindle detector
│   │   │   ├── fuseau_threshold.py   # Threshold-based detection
│   │   │   └── fuseau_ml.py          # ML-based detection (coming soon)
│   │   ├── intensite/
│   │   │   └── mesure_intensite.py   # Fluorescence intensity measurement
│   │   └── statistiques/
│   │       ├── stats_comparaison.py  # WT vs KO statistical comparison
│   │       └── rapport_generator.py  # HTML/PDF report generation
│   ├── cache_shared.py               # Shared in-memory cache
│   ├── main.py                       # FastAPI app entry point
│   └── requirements.txt
│
├── frontend/                         # React frontend
│   └── src/
│       ├── components/
│       │   ├── layout/               # Header, Sidebar, MainContent
│       │   ├── groups/               # Group loader and file list
│       │   ├── pipeline/             # Pipeline status tracker
│       │   ├── viewer/               # Image viewer, channel selector, Z-slider
│       │   ├── metrics/              # Metric cards and grid
│       │   ├── files/                # File list component
│       │   └── analysis/             # Method selector and config panel
│       ├── api/                      # Backend API calls
│       ├── context/                  # Global app state (AppContext)
│       └── styles/                   # CSS variables (light/dark theme)
│
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── nginx.conf
├── lancer.bat                        # Windows launcher
├── lancer.sh                         # Mac/Linux launcher
└── README.md
```

---

## 🔬 Supported Image Formats

| Format | Manufacturer | Status |
|--------|-------------|--------|
| `.nd2` | Nikon | ✅ Supported |
| `.czi` | Zeiss | 🔄 Coming soon |
| `.tiff` | Universal | 🔄 Coming soon |
| `.lif` | Leica | 🔄 Coming soon |
| `.oib` | Olympus | 🔄 Coming soon |

---

## 🧠 Detection Methods

| Module | Method | Status |
|--------|--------|--------|
| Nucleus detection | Otsu thresholding + Watershed | ✅ Available |
| Nucleus detection | Cellpose (ML) | 🔄 Coming soon |
| Nucleus detection | StarDist (DL) | 🔄 Coming soon |
| Nucleus detection | Custom model (YOLO/fine-tuned) | 🔄 Coming soon |
| Classification | Geometric shape (circularity) | ✅ Available |
| Classification | Classical ML | 🔄 Coming soon |
| Classification | Deep Learning | 🔄 Coming soon |
| Spindle detection | Threshold-based | 🔄 Coming soon |
| Spindle detection | ML-based | 🔄 Coming soon |

---

## 🐳 Docker

### Build images

```bash
docker-compose build
```

### Run with launcher (recommended)

```batch
# Windows
lancer.bat

# Mac/Linux
./lancer.sh
```

### Run manually

```bash
IMAGES_ROOT=/path/to/your/images docker-compose up
```

### Stop

```bash
docker-compose down
```

---

## 💻 Local Development

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
# → http://localhost:8000
# → http://localhost:8000/docs (Swagger UI)
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

---

## 🛠️ Technical Stack

| Category | Technology | Version |
|----------|-----------|---------|
| Backend framework | FastAPI | 0.128 |
| ASGI server | Uvicorn | 0.39 |
| Image reading | nd2 | 0.11 |
| Image processing | scikit-image | 0.21 |
| Numerical computing | NumPy | 1.26 |
| Data analysis | Pandas | 2.0 |
| Visualization | Matplotlib, Seaborn | 3.7, 0.12 |
| Frontend framework | React | 18 |
| Build tool | Vite | 8 |
| HTTP client | Axios | 1.4 |
| Web server | Nginx | 1.27 |
| Containerization | Docker + Compose | 28.x |
| Languages | Python, JavaScript, CSS | 3.11, ES2022 |

---

## 📊 Use Case

This platform was developed for the analysis of fluorescence microscopy images comparing:

- **WT cells** (wild-type) — normal cells
- **MAP6 KO cells** — cells depleted of the MAP6 microtubule-associated protein

**Research question:** Does MAP6 depletion affect tubulin modifications (acetylation, polyglutamylation) in mitotic spindles?

**Pipeline:**
1. Load `.nd2` files from both conditions
2. Detect nuclei from DNA/DAPI channel (Z-max projection)
3. Classify cells: interphase (round nucleus) vs mitosis (irregular shape)
4. Measure fluorescence intensity in channels 1 & 2 within mitotic spindles
5. Compare WT vs MAP6 KO — statistical report

---

## 📚 Documentation

- [Backend documentation](backend/README.md)
- [Frontend documentation](frontend/README.md)
- [Contributing guide](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

---

## 📄 Citation

```bibtex
@software{celluleanalyse2026,
  author = {Millimono, Sory},
  title  = {CelluleAnalyse: A modular web platform for automated fluorescence microscopy analysis},
  year   = {2026},
  url    = {https://github.com/Millimono/CelluleAnalyse}
}
```

---

## 👤 Author

**Sory Millimono** — Bioinformatician · AI Researcher  
Université de Montréal

📧 millimono64.sm@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/millimono)  
🔬 [ORCID](https://orcid.org/0009-0005-1960-9136)

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.
