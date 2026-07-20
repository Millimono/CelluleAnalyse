# Contributing to CelluleAnalyse

Thank you for your interest in contributing! This guide explains how to add new features, detection methods, or image format support.

## Project Philosophy

CelluleAnalyse is built around modularity — every analysis method is a plugin. You can add a new nucleus detector, a new image format reader, or a new classification method without touching any existing code.

## Adding a New Detection Method

1. Create `backend/modules/detection_noyaux/detector_mymethod.py`
2. Inherit from `BaseDetector` and implement `detect()`:

```python
from .base_detector import BaseDetector, ResultatDetection

class DetectorMyMethod(BaseDetector):
    def detect(self, image: np.ndarray) -> ResultatDetection:
        # Your implementation here
        ...
```

3. Register it in `backend/api/routes_analyse.py`:

```python
elif body.methode == "mymethod":
    detector = DetectorMyMethod()
```

4. Add it to the frontend dropdown in `frontend/src/components/analysis/MethodSelector.jsx`:

```javascript
const DETECTION_METHODS = [
  ...
  { id: "mymethod", label: "My Method (description)" },
];
```

## Adding a New Image Format

1. Create `backend/modules/chargement/loader_myformat.py`
2. Implement a `charger(chemin)` function that returns a numpy array `(Z, C, Y, X)`
3. Add format detection in `routes_visualisation.py`

## Code Style

- **Python**: follow PEP 8, use type hints, docstrings for all public functions
- **JavaScript**: ESLint config is included — run `npm run lint` before committing
- **CSS**: use CSS custom properties from `variables.css`, never hardcode colors

## Pull Request Process

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test locally (backend + frontend)
5. Open a Pull Request with a clear description

## Reporting Issues

Open a GitHub Issue with:
- Your OS and Docker version
- Steps to reproduce
- Expected vs actual behavior
- Relevant error messages or screenshots
