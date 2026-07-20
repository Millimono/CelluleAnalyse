"""
Détection des noyaux par seuillage Otsu + analyse de régions.
Méthode classique, rapide, sans ML.
"""
import numpy as np
from skimage import filters, measure, morphology, segmentation
from skimage.measure import regionprops
from .base_detector import BaseDetector, Noyau, ResultatDetection


class DetectorThreshold(BaseDetector):
    """
    Détection par seuillage Otsu + watershed.
    
    Paramètres ajustables :
        surface_min  : surface minimale d'un noyau (pixels²)
        surface_max  : surface maximale d'un noyau (pixels²)
        rondeur_seuil: en dessous de ce seuil → mitose (forme irrégulière)
    """

    def __init__(
        self,
        surface_min:   float = 500,
        surface_max:   float = 50000,
        rondeur_seuil: float = 0.7,
    ):
        self.surface_min   = surface_min
        self.surface_max   = surface_max
        self.rondeur_seuil = rondeur_seuil

    def detect(self, image: np.ndarray) -> ResultatDetection:
        """
        Détecte les noyaux dans une image 2D du canal ADN.
        """
        # ── 1. Normaliser l'image ────────────────────────────
        img = image.astype(np.float32)
        if img.max() > 0:
            img = (img - img.min()) / (img.max() - img.min())

        # ── 2. Lisser pour réduire le bruit ─────────────────
        img_lisse = filters.gaussian(img, sigma=2)

        # ── 3. Seuillage Otsu → masque binaire ──────────────
        seuil = filters.threshold_otsu(img_lisse)
        masque = img_lisse > seuil

        # ── 4. Nettoyage morphologique ───────────────────────
        # Remplir les trous dans les noyaux
        masque = morphology.remove_small_holes(masque, area_threshold=500)
        # Supprimer les petits objets (bruit)
        masque = morphology.remove_small_objects(masque, min_size=self.surface_min)

        # ── 5. Séparation des noyaux collés (watershed) ──────
        distance  = morphology.disk(1)
        from scipy import ndimage as ndi
        distance_map = ndi.distance_transform_edt(masque)
        coords    = morphology.local_maxima(distance_map)
        markers   = measure.label(coords)
        labels    = segmentation.watershed(-distance_map, markers, mask=masque)

        # ── 6. Analyser chaque région ─────────────────────────
        regions = regionprops(labels)
        noyaux  = []
        idx     = 0

        for region in regions:
            surface = region.area

            # Filtrer par taille
            if surface < self.surface_min or surface > self.surface_max:
                continue

            # Calculer la rondeur (circularité)
            # rondeur = 4π × surface / périmètre²
            perimetre = region.perimeter
            if perimetre == 0:
                continue
            rondeur = (4 * np.pi * surface) / (perimetre ** 2)
            rondeur = min(1.0, rondeur)  # cap à 1.0

            # Classifier : rond = interphase, irrégulier = mitose
            if rondeur >= self.rondeur_seuil:
                classe = "interphase"
            else:
                classe = "mitose"

            # Bounding box
            min_r, min_c, max_r, max_c = region.bbox

            # Contour simplifié (4 coins du bbox pour l'instant)
            contour = [
                [min_c, min_r],
                [max_c, min_r],
                [max_c, max_r],
                [min_c, max_r],
            ]

            noyaux.append(Noyau(
                id=idx,
                centroid_x=region.centroid[1],
                centroid_y=region.centroid[0],
                surface=surface,
                rondeur=round(rondeur, 3),
                classe=classe,
                bbox=(min_c, min_r, max_c, max_r),
                contour=contour,
            ))
            idx += 1

        # Compter
        total      = len(noyaux)
        interphase = sum(1 for n in noyaux if n.classe == "interphase")
        mitose     = sum(1 for n in noyaux if n.classe == "mitose")

        return ResultatDetection(
            total=total,
            interphase=interphase,
            mitose=mitose,
            noyaux=noyaux,
            masque=masque.astype(np.uint8) * 255,
            methode="threshold_otsu",
        )
