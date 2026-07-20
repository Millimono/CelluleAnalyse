from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
import base64
import io
from PIL import Image, ImageDraw
import cache_shared
from modules.chargement.projection_z import projeter
from modules.detection_noyaux.detector_threshold import DetectorThreshold

router = APIRouter(prefix="/analyse", tags=["analyse"])

# ── Modèles ──────────────────────────────────────────────────
class AnalyseRequest(BaseModel):
    methode:       str   = "threshold"
    projection:    str   = "max"
    surface_min:   float = 500
    surface_max:   float = 50000
    rondeur_seuil: float = 0.7

class NoyauResult(BaseModel):
    id:         int
    centroid_x: float
    centroid_y: float
    surface:    float
    rondeur:    float
    classe:     str
    bbox:       list

class AnalyseResponse(BaseModel):
    total:      int
    interphase: int
    mitose:     int
    noyaux:     list[NoyauResult]
    image_b64:  str
    methode:    str

# ── Helpers ──────────────────────────────────────────────────
def dessiner_contours(rgb: np.ndarray, noyaux) -> str:
    img_pil = Image.fromarray(rgb.astype(np.uint8))
    draw    = ImageDraw.Draw(img_pil)
    for n in noyaux:
        x1, y1, x2, y2 = n.bbox
        couleur = "#00ff88" if n.classe == "interphase" else "#ff4444"
        draw.rectangle([x1, y1, x2, y2], outline=couleur, width=2)
        cx, cy = int(n.centroid_x), int(n.centroid_y)
        draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=couleur)
        draw.text((x1+2, y1+2), str(n.id), fill=couleur)
    buf = io.BytesIO()
    img_pil.save(buf, format="PNG")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

# ── Route principale ─────────────────────────────────────────
@router.post("/detecter_noyaux", response_model=AnalyseResponse)
def detecter_noyaux(body: AnalyseRequest):
    if cache_shared.cache["data"] is None:
        raise HTTPException(status_code=400, detail="Aucun fichier chargé. Ouvre un fichier d'abord.")

    data     = cache_shared.cache["data"]
    n_canaux = cache_shared.cache["n_canaux"]
    hauteur  = cache_shared.cache["hauteur"]
    largeur  = cache_shared.cache["largeur"]

    idx_adn   = min(2, n_canaux - 1)
    stack_adn = data[:, idx_adn, :, :]
    image_2d  = projeter(stack_adn, methode=body.projection)

    if body.methode == "threshold":
        detector = DetectorThreshold(
            surface_min=body.surface_min,
            surface_max=body.surface_max,
            rondeur_seuil=body.rondeur_seuil,
        )
    else:
        raise HTTPException(status_code=400, detail=f"Méthode non disponible : {body.methode}")

    resultat = detector.detect(image_2d)

    img_display = image_2d.astype(np.float32)
    if img_display.max() > 0:
        img_display = (img_display / img_display.max() * 255).astype(np.uint8)
    rgb = np.zeros((hauteur, largeur, 3), dtype=np.uint8)
    rgb[:,:,2] = img_display

    noyaux_result = [
        NoyauResult(
            id=n.id,
            centroid_x=n.centroid_x,
            centroid_y=n.centroid_y,
            surface=n.surface,
            rondeur=n.rondeur,
            classe=n.classe,
            bbox=list(n.bbox),
        )
        for n in resultat.noyaux
    ]

    return AnalyseResponse(
        total=resultat.total,
        interphase=resultat.interphase,
        mitose=resultat.mitose,
        noyaux=noyaux_result,
        image_b64=dessiner_contours(rgb, noyaux_result),
        methode=resultat.methode,
    )

@router.get("/ping")
def ping():
    return {"status": "ok", "module": "analyse"}
