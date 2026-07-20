# CelluleAnalyse — Backend 🐍

FastAPI backend for fluorescence microscopy image analysis.

## Overview

The backend provides a REST API for:
- Loading `.nd2` image files into memory cache
- Rendering individual Z-planes per channel as base64 PNG
- Detecting nuclei using pluggable detection methods
- Classifying cells (interphase vs mitosis)
- Measuring fluorescence intensity in mitotic spindles

## Architecture

```
backend/
├── main.py                        # FastAPI app entry point
├── cache_shared.py                # Shared in-memory file cache
├── requirements.txt
│
├── api/
│   ├── routes_chargement.py       # POST /chargement/scanner
│   ├── routes_visualisation.py    # POST /visualisation/charger
│   │                              # POST /visualisation/image
│   ├── routes_analyse.py          # POST /analyse/detecter_noyaux
│   └── routes_rapport.py          # Coming soon
│
└── modules/
    ├── chargement/
    │   ├── loader_nd2.py          # Nikon .nd2 reader
    │   └── projection_z.py        # Z-projection (max/mean/sum)
    │
    ├── detection_noyaux/
    │   ├── base_detector.py       # Abstract interface (Strategy pattern)
    │   ├── detector_threshold.py  # Otsu + Watershed
    │   ├── detector_cellpose.py   # Cellpose ML (coming soon)
    │   └── detector_stardist.py   # StarDist DL (coming soon)
    │
    ├── classification/
    │   ├── base_classifier.py     # Abstract interface
    │   ├── classifier_shape.py    # Circularity-based
    │   ├── classifier_ml.py       # Coming soon
    │   └── classifier_dl.py       # Coming soon
    │
    ├── detection_fuseau/
    │   ├── base_fuseau.py         # Abstract interface
    │   ├── fuseau_threshold.py    # Threshold-based
    │   └── fuseau_ml.py           # Coming soon
    │
    ├── intensite/
    │   └── mesure_intensite.py    # Fluorescence measurement
    │
    └── statistiques/
        ├── stats_comparaison.py   # WT vs KO comparison
        └── rapport_generator.py   # Report generation
```

## API Reference

### Chargement

```
POST /chargement/scanner
Body: { "chemin": "/path/to/folder" }
Returns: { chemin, groupe, fichiers[], total }
```

### Visualisation

```
POST /visualisation/charger
Body: { "chemin": "/path/to/file.nd2" }
Returns: { chemin, total_z, n_canaux, hauteur, largeur }

POST /visualisation/image
Body: { "canal": "adn|acetylation|polyglutamylation|composite", "plan_z": 1 }
Returns: { image_b64, canal, plan_z }
```

### Analyse

```
POST /analyse/detecter_noyaux
Body: { "methode": "threshold", "projection": "max", "surface_min": 500, "surface_max": 50000, "rondeur_seuil": 0.7 }
Returns: { total, interphase, mitose, noyaux[], image_b64, methode }
```

## Design Pattern — Strategy

Each detection module follows the Strategy pattern — all detectors implement the same `BaseDetector` interface:

```python
class BaseDetector(ABC):
    @abstractmethod
    def detect(self, image: np.ndarray) -> ResultatDetection:
        pass
```

To add a new detector:
1. Create `detector_mymethod.py`
2. Inherit from `BaseDetector`
3. Implement `detect()`
4. Register in `routes_analyse.py`

No other code changes needed.

## In-memory Cache

The backend keeps one `.nd2` file loaded in RAM at a time via `cache_shared.py`.

```
File selected → charger() → full array in RAM (Z, C, Y, X)
Channel/Z change → read from RAM → instantaneous
New file selected → flush cache → reload
```

This avoids re-reading the disk on every channel/Z change.

## Installation

```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

API documentation available at **http://localhost:8000/docs**

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `IMAGES_ROOT` | Root path of images folder (Docker) | — |

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.128 | REST API framework |
| uvicorn | 0.39 | ASGI server |
| nd2 | 0.11 | Nikon .nd2 file reader |
| numpy | 1.26 | Array computation |
| scikit-image | 0.21 | Image processing, segmentation |
| scipy | 1.13 | Distance transforms |
| Pillow | 10.0 | Image encoding (PNG/base64) |
| pandas | 2.0 | Data analysis |
| matplotlib | 3.7 | Plotting |
| seaborn | 0.12 | Statistical visualization |
| python-multipart | 0.0.20 | File upload support |
