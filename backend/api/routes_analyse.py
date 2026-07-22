from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
import base64
import io
from PIL import Image, ImageDraw
import cache_shared
from modules.chargement.projection_z import projeter
from modules.detection_noyaux.detector_threshold import DetectorThreshold
from modules.intensite.mesure_intensite import mesurer_fuseau

router = APIRouter(prefix="/analyse", tags=["analyse"])

# ── Modèles ──────────────────────────────────────────────────
class AnalyseRequest(BaseModel):
    methode:              str   = "threshold"
    projection:           str   = "max"
    surface_min:          float = 3000
    surface_max:          float = 100000
    rondeur_seuil:        float = 0.7
    elongation_seuil:     float = 1.8
    intensite_percentile: float = 92
    marge_fuseau:         float = 0.3   # élargissement bbox pour le fuseau

class NoyauResult(BaseModel):
    id:                  int
    centroid_x:          float
    centroid_y:          float
    surface:             float
    rondeur:             float
    elongation:          float
    intensite_adn:       float
    intensite_composite: float
    classe:              str
    bbox:                list

class MesureFuseauResult(BaseModel):
    noyau_id:                        int
    bbox_fuseau:                     list
    intensite_acetylation:           float
    intensite_polyglutamylation:     float
    intensite_max_acetylation:       float
    intensite_max_polyglutamylation: float
    ratio_poly_acet:                 float

class AnalyseResponse(BaseModel):
    total:          int
    interphase:     int
    mitose:         int
    inconnu:        int
    noyaux:         list[NoyauResult]
    mesures_fuseau: list[MesureFuseauResult]
    image_b64:      str
    methode:        str

# ── Helpers ──────────────────────────────────────────────────
def dessiner_contours(rgb: np.ndarray, noyaux, mesures_fuseau=[]) -> str:
    img_pil = Image.fromarray(rgb.astype(np.uint8))
    draw    = ImageDraw.Draw(img_pil)
    for n in noyaux:
        x1, y1, x2, y2 = n.bbox
        if n.classe == "interphase":
            couleur = "#00ff88"  # vert
        elif n.classe == "mitose":
            couleur = "#ff4444"  # rouge
        else:
            couleur = "#ffff00"  # jaune → inconnu
        draw.rectangle([x1, y1, x2, y2], outline=couleur, width=2)
        cx, cy = int(n.centroid_x), int(n.centroid_y)
        draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=couleur)
        draw.text((x1+2, y1+2), str(n.id), fill=couleur)

    # Dessiner la zone du fuseau en blanc
    for m in mesures_fuseau:
        x1, y1, x2, y2 = m.bbox_fuseau
        draw.rectangle([x1, y1, x2, y2], outline="#ffffff", width=1)

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

    # ── Canal ADN → détection des noyaux ─────────────────────
    idx_adn   = min(2, n_canaux - 1)
    stack_adn = data[:, idx_adn, :, :]
    image_adn = projeter(stack_adn, methode=body.projection)

    # ── Canal Acétylation ────────────────────────────────────
    idx_acet   = min(1, n_canaux - 1)
    stack_acet = data[:, idx_acet, :, :]
    image_acet = projeter(stack_acet, methode=body.projection)

    # ── Canal Polyglutamylation ───────────────────────────────
    stack_poly = data[:, 0, :, :]
    image_poly = projeter(stack_poly, methode=body.projection)

    # ── Score ADN × Acétylation normalisé → détection mitose ─
    # Normaliser chaque canal entre 0 et 1 avant de multiplier
    # → évite que ADN très fort masque une Acétylation faible
    adn_norm  = stack_adn.astype(np.float32)
    adn_norm  = (adn_norm - adn_norm.min()) / (adn_norm.max() - adn_norm.min() + 1e-6)

    acet_norm = stack_acet.astype(np.float32)
    acet_norm = (acet_norm - acet_norm.min()) / (acet_norm.max() - acet_norm.min() + 1e-6)

    # Produit équilibré → élevé seulement si les 2 canaux sont vraiment brillants
    stack_score  = adn_norm * acet_norm
    image_score  = projeter(stack_score, methode=body.projection)

    if body.methode == "threshold":
        detector = DetectorThreshold(
            surface_min=body.surface_min,
            surface_max=body.surface_max,
            rondeur_seuil=body.rondeur_seuil,
            elongation_seuil=body.elongation_seuil,
            intensite_percentile=body.intensite_percentile,
        )
    else:
        raise HTTPException(status_code=400, detail=f"Méthode non disponible : {body.methode}")

    # Détecter avec canal ADN + score ADN×Acétylation
    resultat = detector.detect(image_adn, image_score)

    # ── Mesure d'intensité dans les fuseaux mitotiques ────────
    noyaux_mitose = [
        {"id": n.id, "bbox": list(n.bbox)}
        for n in resultat.noyaux
        if n.classe == "mitose"
    ]
    mesures = mesurer_fuseau(
        noyaux_mitose=noyaux_mitose,
        image_acet=image_acet,
        image_poly=image_poly,
        marge=body.marge_fuseau,
    )

    # ── Image de visualisation (canal ADN en bleu) ────────────
    img_display = image_adn.astype(np.float32)
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
            elongation=n.elongation,
            intensite_adn=n.intensite_adn,
            intensite_composite=n.intensite_composite,
            classe=n.classe,
            bbox=list(n.bbox),
        )
        for n in resultat.noyaux
    ]

    mesures_result = [
        MesureFuseauResult(
            noyau_id=m.noyau_id,
            bbox_fuseau=list(m.bbox_fuseau),
            intensite_acetylation=m.intensite_acetylation,
            intensite_polyglutamylation=m.intensite_polyglutamylation,
            intensite_max_acetylation=m.intensite_max_acetylation,
            intensite_max_polyglutamylation=m.intensite_max_polyglutamylation,
            ratio_poly_acet=m.ratio_poly_acet,
        )
        for m in mesures
    ]

    inconnu = sum(1 for n in noyaux_result if n.classe == "inconnu")

    return AnalyseResponse(
        total=resultat.total,
        interphase=resultat.interphase,
        mitose=resultat.mitose,
        inconnu=inconnu,
        noyaux=noyaux_result,
        mesures_fuseau=mesures_result,
        image_b64=dessiner_contours(rgb, noyaux_result, mesures_result),
        methode=resultat.methode,
    )

@router.get("/ping")
def ping():
    return {"status": "ok", "module": "analyse"}