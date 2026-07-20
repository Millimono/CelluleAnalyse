from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import os

router = APIRouter(prefix="/chargement", tags=["chargement"])

# Chemin racine des images (défini par variable d'environnement)
IMAGES_ROOT_WIN = os.environ.get("IMAGES_ROOT", "")
IMAGES_ROOT_DOCKER = "/data/images"

def convertir_chemin(chemin: str) -> str:
    """
    Convertit un chemin Windows en chemin Docker si nécessaire.
    Ex: C:\MonLabo\Images\WT → /data/images/WT
    """
    if IMAGES_ROOT_WIN and chemin.startswith(IMAGES_ROOT_WIN):
        sous_dossier = chemin[len(IMAGES_ROOT_WIN):].replace("\\", "/").lstrip("/")
        return f"{IMAGES_ROOT_DOCKER}/{sous_dossier}"
    return chemin

class DossierRequest(BaseModel):
    chemin: str

class FichierInfo(BaseModel):
    nom: str
    chemin: str
    taille_mb: float

class DossierResponse(BaseModel):
    chemin: str
    groupe: str
    fichiers: list[FichierInfo]
    total: int

@router.post("/scanner", response_model=DossierResponse)
def scanner_dossier(body: DossierRequest):
    chemin_converti = convertir_chemin(body.chemin)
    dossier = Path(chemin_converti)

    if not dossier.exists():
        raise HTTPException(status_code=404, detail=f"Dossier introuvable : {body.chemin}")

    if not dossier.is_dir():
        raise HTTPException(status_code=400, detail=f"Ce chemin n'est pas un dossier : {body.chemin}")

    fichiers = []
    for f in sorted(dossier.glob("*.nd2")):
        taille_mb = round(f.stat().st_size / (1024 * 1024), 1)
        fichiers.append(FichierInfo(
            nom=f.name,
            chemin=str(f),
            taille_mb=taille_mb,
        ))

    if not fichiers:
        raise HTTPException(status_code=404, detail="Aucun fichier .nd2 trouvé dans ce dossier")

    return DossierResponse(
        chemin=str(dossier),
        groupe=dossier.name,
        fichiers=fichiers,
        total=len(fichiers),
    )

@router.get("/ping")
def ping():
    return {"status": "ok", "module": "chargement"}