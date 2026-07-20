# Changelog

All notable changes to CelluleAnalyse are documented here.

## [0.1.0] — 2026-07-20

### Added
- FastAPI backend with modular architecture
- React frontend with dark/light theme support
- `.nd2` file support (Nikon format) via `nd2` library
- Multi-channel visualization: ADN, Acetylation, Polyglutamylation, Composite
- Z-plane navigation with slider and ‹ › buttons
- Progressive image cache — composite Z1 displayed immediately, full cache built in background
- Nucleus detection via Otsu thresholding + Watershed
- Cell classification: interphase (round) vs mitosis (irregular)
- Detection overlay on image with green (interphase) and red (mitosis) bounding boxes
- Dashboard metrics: total cells, mitoses, % mitosis, files analyzed
- Pipeline status tracker with step-by-step progress
- Analysis scope: current file or group (WT/KO)
- Full-screen image viewer
- Docker deployment with `lancer.bat` (Windows) and `lancer.sh` (Mac/Linux)
- Shared in-memory cache between visualisation and analysis modules
- Nginx reverse proxy for production Docker setup

### Architecture
- Strategy pattern for detection methods (pluggable detectors)
- CSS Modules for scoped component styles
- Global state via React Context API
- Z-projection module (max/mean/sum)

## [Unreleased]

### Planned
- Cellpose ML nucleus detection
- StarDist DL nucleus detection
- Fluorescence intensity measurement in mitotic spindles
- WT vs KO statistical comparison with report generation
- Zeiss `.czi` format support
- TIFF format support
- Custom model training pipeline (YOLO, fine-tuned Cellpose)
- Batch analysis across all files in a group
- Export results to CSV/Excel
- HTML/PDF report generation
