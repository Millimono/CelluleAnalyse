# CelluleAnalyse — Frontend ⚛️

React web interface for fluorescence microscopy image analysis.

## Overview

The frontend provides an interactive dashboard for:
- Loading and managing image groups (WT, KO, or any two conditions)
- Visualizing `.nd2` images channel by channel with Z-plane navigation
- Configuring and launching analysis pipelines
- Displaying detection results overlaid on images
- Monitoring pipeline progress in real time

## Architecture

```
frontend/src/
│
├── App.jsx                        # Root component — wraps everything in AppProvider
├── main.jsx                       # React DOM entry point
│
├── context/
│   └── AppContext.jsx             # Global state (groups, viewer, pipeline, metrics)
│
├── styles/
│   ├── variables.css              # CSS custom properties (light + dark theme)
│   └── global.css                 # Reset, base styles, reusable classes
│
├── api/
│   ├── api_chargement.js          # scannerDossier()
│   ├── api_visualisation.js       # chargerFichier(), getImage()
│   └── api_analyse.js             # detecterNoyaux()
│
└── components/
    ├── layout/
    │   ├── Header.jsx             # Top bar — logo, theme toggle
    │   ├── Sidebar.jsx            # Left panel — groups + pipeline
    │   └── MainContent.jsx        # Right panel — viewer + metrics + analysis
    │
    ├── groups/
    │   └── GroupeList.jsx         # Group cards with file list
    │
    ├── pipeline/
    │   └── PipelineStatus.jsx     # Step-by-step pipeline tracker
    │
    ├── metrics/
    │   ├── MetricCard.jsx         # Single metric display card
    │   └── MetricsGrid.jsx        # 4-card metrics row
    │
    ├── viewer/
    │   ├── ImageViewer.jsx        # Main image canvas with progressive cache
    │   ├── ChannelSelector.jsx    # ADN / Acetylation / PolyGlu / Composite
    │   └── ZSlider.jsx            # Z-plane navigation slider + buttons
    │
    ├── files/
    │   └── FileList.jsx           # File list for active group
    │
    └── analysis/
        └── MethodSelector.jsx     # Scope + analyses + method config + launch button
```

## Key Design Decisions

### Global State — Context API
All shared state lives in `AppContext.jsx`:
- Active group, file, channel, Z-plane
- Groups with their file lists
- Pipeline step statuses
- Analysis metrics
- Theme (light/dark)

To add new state: edit `AppContext.jsx` only — no other files need changing.

### CSS Modules
Every component has its own `.module.css` file — styles are scoped and cannot leak between components.

To update a component's style: edit its `.module.css` only.

### Theme System
All colors are CSS custom properties in `variables.css`:

```css
:root { --surface-0: #f5f5f3; --text-primary: #1a1a18; ... }
[data-theme="dark"] { --surface-0: #1a1a18; --text-primary: #f0efea; ... }
```

To change a color: edit `variables.css` only — it propagates everywhere.

### Progressive Image Cache
The image viewer uses a two-phase loading strategy:

1. **Phase 1** — Load current Z-plane of composite channel → display immediately
2. **Phase 2** — Background preload all channels × all Z-planes in smart order

After preloading is complete, all channel/Z navigation is instantaneous (0ms).

Cache is stored in a `useRef` object (not React state) to avoid re-renders.

## Component Props

| Component | Key Props |
|-----------|-----------|
| `GroupeList` | `onSelectFolder(groupName)` |
| `MethodSelector` | `onResultat(resultat)` — called with detection results |
| `ImageViewer` | `imageAnalyse` — base64 overlay from analysis |
| `MetricCard` | `label`, `value`, `unit` |

## Adding a New Component

1. Create `src/components/mymodule/MyComponent.jsx`
2. Create `src/components/mymodule/MyComponent.module.css`
3. Use `useApp()` hook to access global state
4. Import and add to the relevant layout component

## Installation

```bash
npm install
npm run dev       # Development server → http://localhost:5173
npm run build     # Production build → dist/
npm run preview   # Preview production build
npm run lint      # ESLint check
```

## Environment Variables

Create `.env.production` for Docker builds:

```
VITE_API_URL=http://localhost
```

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend base URL | `http://localhost:8000` |

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| react | 18 | UI framework |
| react-dom | 18 | DOM rendering |
| axios | 1.4 | HTTP client |
| react-router-dom | 6 | Client-side routing |
| vite | 8 | Build tool |
| @vitejs/plugin-react | 6 | React Vite plugin |
| eslint | 10 | Code linting |
