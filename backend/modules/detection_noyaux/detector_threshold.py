"""
Détection des noyaux par seuillage Otsu + analyse de régions.
Méthode classique, rapide, sans ML.
Classification multi-critères : rondeur + elongation + intensité composite.
"""
import numpy as np
from skimage import filters, measure, morphology, segmentation
from skimage.feature import peak_local_max
from skimage.measure import regionprops
from scipy import ndimage as ndi
from .base_detector import BaseDetector, Noyau, ResultatDetection


class DetectorThreshold(BaseDetector):
    """
    Détection par seuillage Otsu + watershed.

    Paramètres ajustables :
        surface_min          : surface minimale d'un noyau (pixels²)
        surface_max          : surface maximale d'un noyau (pixels²)
        rondeur_seuil        : en dessous de ce seuil → mitose (forme irrégulière)
        elongation_seuil     : au dessus de ce seuil → mitose (forme allongée)
        intensite_percentile : percentile composite au dessus duquel → mitose (très brillant)
    """

    def __init__(
        self,
        surface_min:          float = 5000,
        surface_max:          float = 100000,
        rondeur_seuil:        float = 0.7,
        elongation_seuil:     float = 1.8,
        intensite_percentile: float = 92,
    ):
        self.surface_min          = surface_min
        self.surface_max          = surface_max
        self.rondeur_seuil        = rondeur_seuil
        self.elongation_seuil     = elongation_seuil
        self.intensite_percentile = intensite_percentile

    def detect(self, image: np.ndarray, image_composite: np.ndarray = None) -> ResultatDetection:
        """
        Détecte les noyaux dans une image 2D du canal ADN.

        Args:
            image           : array numpy 2D (Y, X) canal ADN
            image_composite : array numpy 2D (Y, X) composite des 3 canaux (optionnel)
        """
        # ── 1. Normaliser l'image ────────────────────────────
        img = image.astype(np.float32)
        if img.max() > 0:
            img = (img - img.min()) / (img.max() - img.min())

        # ── 2. Lisser pour réduire le bruit ─────────────────
        img_lisse = filters.gaussian(img, sigma=7)

        # ── 3. Seuillage Otsu → masque binaire ──────────────
        seuil  = filters.threshold_otsu(img_lisse)* 0.7
        masque = img_lisse > seuil

        # ── 4. Nettoyage morphologique ───────────────────────
        # Remplir les trous dans les noyaux
        masque = morphology.remove_small_holes(masque, area_threshold=500)
        # Supprimer les petits objets (bruit)
        masque = morphology.remove_small_objects(masque, min_size=self.surface_min)

        # ── 5. Séparation des noyaux collés (watershed) ──────
        distance_map = ndi.distance_transform_edt(masque)

        # peak_local_max avec distance minimale → évite les doubles détections
        # min_distance=30 → 2 maxima doivent être à 30px minimum l'un de l'autre
        coords     = peak_local_max(distance_map, min_distance=40, labels=masque)
        mask_peaks = np.zeros(distance_map.shape, dtype=bool)
        mask_peaks[tuple(coords.T)] = True

        markers = measure.label(mask_peaks)
        labels  = segmentation.watershed(-distance_map, markers, mask=masque)

        # ── 6. Seuil d'intensité composite pour mitose ───────
        # Une cellule en mitose brille fortement dans tous les canaux
        # Score ADN × Acétylation → élevé seulement si les 2 canaux sont brillants
        # (passé depuis routes_analyse.py comme image_score)

        if image_composite is not None:
            comp            = image_composite.astype(np.float32)
            seuil_intensite = np.percentile(comp[masque], self.intensite_percentile)
        else:
            seuil_intensite = None

        # ── 7. Analyser chaque région ─────────────────────────
        regions = regionprops(labels, intensity_image=image.astype(np.float32))
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
            rondeur = min(1.0, (4 * np.pi * surface) / (perimetre ** 2))

            # Elongation = rapport grand axe / petit axe
            elongation = region.major_axis_length / (region.minor_axis_length + 1e-6)

            # Intensité moyenne canal ADN
            intensite_adn = region.mean_intensity

            # Intensité moyenne composite dans la même région
            if image_composite is not None:
                intensite_composite = float(np.mean(image_composite[labels == region.label]))
            else:
                intensite_composite = 0.0

            # ── Classification multi-critères ────────────────
            # est_mitose = False

            # # Critère 1 : intensité composite très élevée → mitose brillante
            # if seuil_intensite is not None and intensite_composite > seuil_intensite:
            #     est_mitose = True

            # # Critère 2 : forme irrégulière (rondeur faible) → mitose
            # if rondeur < self.rondeur_seuil:
            #     est_mitose = True

            # # Critère 3 : forme très allongée → mitose
            # if elongation > self.elongation_seuil:
            #     est_mitose = True

            # classe = "mitose" if est_mitose else "interphase"

            # ── Classification multi-critères ────────────────────────
            # est_mitose = False

            # # Une vraie mitose est plus grande qu'un noyau normal
            # # Les petits fragments/artefacts ne peuvent pas être des mitoses
            # SURFACE_MIN_MITOSE = 8000

            # if surface >= SURFACE_MIN_MITOSE:
            #     # Critère 1 : intensité composite très élevée → mitose brillante
            #     if seuil_intensite is not None and intensite_composite > seuil_intensite:
            #         est_mitose = True

            #     # Critère 2 : forme irrégulière (rondeur faible) → mitose
            #     if rondeur < self.rondeur_seuil:
            #         est_mitose = True

            #     # Critère 3 : forme très allongée → mitose
            #     if elongation > self.elongation_seuil:
            #         est_mitose = True

            # classe = "mitose" if est_mitose else "interphase"

            # ── Classification multi-critères avec score de confiance ──
            score_mitose     = 0
            score_interphase = 0

            # Critères mitose
            if seuil_intensite is not None and intensite_composite > seuil_intensite:
                score_mitose += 3  # critère fort → brille dans tous les canaux

            if rondeur < self.rondeur_seuil:
                score_mitose += 1  # forme irrégulière

            if elongation > self.elongation_seuil:
                score_mitose += 1  # forme allongée (haltère)

            # Critères interphase
            if rondeur >= self.rondeur_seuil:
                score_interphase += 2  # très rond → clairement interphase

            if elongation < self.elongation_seuil:
                score_interphase += 0.5  # pas allongé

            # Classification finale
            if score_mitose >= 3:
                classe = "mitose"
            elif score_interphase >= 1:
                classe = "interphase"
            else:
                classe = "inconnu"  # cas résiduel

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
                elongation=round(elongation, 3),
                intensite_adn=round(intensite_adn, 2),
                intensite_composite=round(intensite_composite, 2),
                classe=classe,
                bbox=(min_c, min_r, max_c, max_r),
                contour=contour,
            ))
            idx += 1

        # Compter
        total      = len(noyaux)
        interphase = sum(1 for n in noyaux if n.classe == "interphase")
        mitose     = sum(1 for n in noyaux if n.classe == "mitose")
        inconnu    = sum(1 for n in noyaux if n.classe == "inconnu")

        return ResultatDetection(
            total=total,
            interphase=interphase,
            mitose=mitose,
             inconnu=inconnu,
            noyaux=noyaux,
            masque=masque.astype(np.uint8) * 255,
            methode="threshold_otsu",
        )