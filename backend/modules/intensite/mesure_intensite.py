"""
Mesure d'intensité de fluorescence dans les fuseaux mitotiques.
Pour chaque cellule en mitose détectée, mesure l'intensité
des canaux 1 (acétylation) et 2 (polyglutamylation) dans la zone du fuseau.
"""
import numpy as np
from dataclasses import dataclass


@dataclass
class MesureIntensiteFuseau:
    """Résultat de mesure d'intensité pour une cellule en mitose"""
    noyau_id:                    int
    # Zone du fuseau (bbox élargie)
    bbox_fuseau:                 tuple   # (x1, y1, x2, y2)
    # Intensités moyennes
    intensite_acetylation:       float   # canal 1
    intensite_polyglutamylation: float   # canal 0
    # Intensités max (pic du signal)
    intensite_max_acetylation:       float
    intensite_max_polyglutamylation: float
    # Ratio (polyglutamylation / acétylation)
    ratio_poly_acet:             float


def mesurer_fuseau(
    noyaux_mitose:   list,
    image_acet:      np.ndarray,   # canal acétylation 2D (Y, X)
    image_poly:      np.ndarray,   # canal polyglutamylation 2D (Y, X)
    marge:           float = 0.3,  # élargissement de la bbox en %
) -> list[MesureIntensiteFuseau]:
    """
    Mesure l'intensité de fluorescence dans les fuseaux mitotiques.

    Args:
        noyaux_mitose : liste de noyaux classifiés "mitose"
        image_acet    : image 2D canal acétylation (projection Z)
        image_poly    : image 2D canal polyglutamylation (projection Z)
        marge         : % d'élargissement de la bbox du noyau pour couvrir le fuseau

    Returns:
        Liste de MesureIntensiteFuseau pour chaque mitose
    """
    H, W = image_acet.shape
    mesures = []

    for noyau in noyaux_mitose:
        x1, y1, x2, y2 = noyau["bbox"]

        # ── Élargir la bbox pour couvrir le fuseau ────────────
        # Le fuseau dépasse légèrement le noyau
        largeur_bbox = x2 - x1
        hauteur_bbox = y2 - y1

        x1_f = max(0, int(x1 - marge * largeur_bbox))
        x2_f = min(W, int(x2 + marge * largeur_bbox))
        y1_f = max(0, int(y1 - marge * hauteur_bbox))
        y2_f = min(H, int(y2 + marge * hauteur_bbox))

        # ── Extraire la zone du fuseau ────────────────────────
        zone_acet = image_acet[y1_f:y2_f, x1_f:x2_f].astype(np.float32)
        zone_poly = image_poly[y1_f:y2_f, x1_f:x2_f].astype(np.float32)

        if zone_acet.size == 0:
            continue

        # ── Mesurer l'intensité ───────────────────────────────
        int_acet_mean = float(np.mean(zone_acet))
        int_poly_mean = float(np.mean(zone_poly))
        int_acet_max  = float(np.max(zone_acet))
        int_poly_max  = float(np.max(zone_poly))

        # Ratio polyglutamylation / acétylation
        ratio = int_poly_mean / (int_acet_mean + 1e-6)

        mesures.append(MesureIntensiteFuseau(
            noyau_id=noyau["id"],
            bbox_fuseau=(x1_f, y1_f, x2_f, y2_f),
            intensite_acetylation=round(int_acet_mean, 2),
            intensite_polyglutamylation=round(int_poly_mean, 2),
            intensite_max_acetylation=round(int_acet_max, 2),
            intensite_max_polyglutamylation=round(int_poly_max, 2),
            ratio_poly_acet=round(ratio, 3),
        ))

    return mesures# Mesure d'intensité de fluorescence dans les ROI
