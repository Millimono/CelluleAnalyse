from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import nd2
import numpy as np
from PIL import Image
import base64
import io
import cache_shared

router = APIRouter(prefix="/visualisation", tags=["visualisation"])

# ── Modèles ──────────────────────────────────────────────────
class ChargerRequest(BaseModel):
    chemin: str

class ChargerResponse(BaseModel):
    chemin:   str
    total_z:  int
    n_canaux: int
    hauteur:  int
    largeur:  int

class ImageRequest(BaseModel):
    canal:  str
    plan_z: int = 1

class ImageResponse(BaseModel):
    image_b64: str
    canal:     str
    plan_z:    int

# ── Helpers ──────────────────────────────────────────────────
def normaliser_canal(arr: np.ndarray) -> np.ndarray:
    p1, p99 = np.percentile(arr, 1), np.percentile(arr, 99)
    if p99 == p1:
        return np.zeros_like(arr, dtype=np.uint8)
    return ((np.clip(arr, p1, p99) - p1) / (p99 - p1) * 255).astype(np.uint8)

def extraire_rgb(plan: np.ndarray, canal: str, n_canaux: int, h: int, w: int) -> np.ndarray:
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    if canal == "adn":
        rgb[:,:,2] = normaliser_canal(plan[min(2, n_canaux-1)])
    elif canal == "acetylation":
        rgb[:,:,1] = normaliser_canal(plan[min(1, n_canaux-1)])
    elif canal == "polyglutamylation":
        a = normaliser_canal(plan[0])
        rgb[:,:,0] = a; rgb[:,:,2] = a
    elif canal == "composite":
        if n_canaux >= 1:
            a = normaliser_canal(plan[0])
            rgb[:,:,0] = np.maximum(rgb[:,:,0], a)
            rgb[:,:,2] = np.maximum(rgb[:,:,2], a)
        if n_canaux >= 2:
            a = normaliser_canal(plan[1])
            rgb[:,:,1] = np.maximum(rgb[:,:,1], a)
        if n_canaux >= 3:
            a = normaliser_canal(plan[2])
            rgb[:,:,2] = np.maximum(rgb[:,:,2], a)
    return rgb

def array_vers_b64(arr: np.ndarray) -> str:
    buf = io.BytesIO()
    Image.fromarray(arr).save(buf, format="PNG")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

# ── Routes ───────────────────────────────────────────────────
@router.post("/charger", response_model=ChargerResponse)
def charger_fichier(body: ChargerRequest):
    chemin = Path(body.chemin)

    if not chemin.exists():
        raise HTTPException(status_code=404, detail=f"Fichier introuvable : {body.chemin}")

    if cache_shared.cache["chemin"] == str(chemin):
        return ChargerResponse(
            chemin=str(chemin),
            total_z=cache_shared.cache["total_z"],
            n_canaux=cache_shared.cache["n_canaux"],
            hauteur=cache_shared.cache["hauteur"],
            largeur=cache_shared.cache["largeur"],
        )

    try:
        with nd2.ND2File(chemin) as f:
            img = f.asarray()

        data = img if img.ndim == 4 else img[np.newaxis]
        total_z, n_canaux, hauteur, largeur = data.shape

        cache_shared.cache["chemin"]   = str(chemin)
        cache_shared.cache["data"]     = data
        cache_shared.cache["total_z"]  = total_z
        cache_shared.cache["n_canaux"] = n_canaux
        cache_shared.cache["hauteur"]  = hauteur
        cache_shared.cache["largeur"]  = largeur

        return ChargerResponse(
            chemin=str(chemin),
            total_z=total_z,
            n_canaux=n_canaux,
            hauteur=hauteur,
            largeur=largeur,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lecture : {str(e)}")


@router.post("/image", response_model=ImageResponse)
def get_image(body: ImageRequest):
    if cache_shared.cache["data"] is None:
        raise HTTPException(status_code=400, detail="Aucun fichier chargé.")

    total_z  = cache_shared.cache["total_z"]
    n_canaux = cache_shared.cache["n_canaux"]
    hauteur  = cache_shared.cache["hauteur"]
    largeur  = cache_shared.cache["largeur"]

    plan_z = max(1, min(body.plan_z, total_z))
    plan   = cache_shared.cache["data"][plan_z - 1]
    rgb    = extraire_rgb(plan, body.canal, n_canaux, hauteur, largeur)

    return ImageResponse(
        image_b64=array_vers_b64(rgb),
        canal=body.canal,
        plan_z=plan_z,
    )

@router.get("/ping")
def ping():
    return {"status": "ok", "cache": cache_shared.cache["chemin"]}
