# Changelog
All notable changes to CelluleAnalyse are documented here.

## [0.2.0] — 2026-07-22

### Added
- Fluorescence intensity measurement in mitotic spindles (channels 1 & 2)
- Normalized ADN × Acetylation score for mitosis detection
- Multi-criteria classification system with confidence scores (mitosis / interphase / unknown)
- Unknown class for ambiguous cases (yellow overlay)
- Results panel with intensity table per mitotic cell
- Ratio polyglutamylation / acetylation per spindle
- ADN + Acetylation combined channel in viewer
- Methods report v1 (Word document)

### Improved
- Otsu threshold × 0.7 for better nucleus capture
- Gaussian sigma increased to 7 for better noise reduction
- peak_local_max min_distance increased to 40px to reduce double counting
- surface_min increased to 5000 px² to filter artifacts
- Instructions panel replacing metrics grid

### Fixed
- Normalized score prevents strong ADN signal from masking weak acetylation
- Double detection of internal chromatin structures reduced

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
- WT vs KO statistical comparison with report generation
- Zeiss `.czi` format support
- TIFF format support
- Custom model training pipeline (YOLO, fine-tuned Cellpose)
- Batch analysis across all files in a group
- Export results to CSV/Excel
- HTML/PDF report generation