"""
Interface commune (Pattern Strategy) pour tous les détecteurs de noyaux.
Chaque nouveau détecteur doit hériter de BaseDetector et implémenter detect().
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import numpy as np


@dataclass
class Noyau:
    """Représente un noyau détecté"""
    id:            int
    centroid_x:    float          # coordonnée X du centre (pixels)
    centroid_y:    float          # coordonnée Y du centre (pixels)
    surface:       float          # surface en pixels²
    rondeur:       float          # 0-1 (1 = cercle parfait)
    classe:        str            # "interphase" | "mitose" | "inconnu"
    bbox:          tuple          # (x_min, y_min, x_max, y_max)
    contour:       list = field(default_factory=list)  # points du contour


@dataclass
class ResultatDetection:
    """Résultat complet d'une détection"""
    total:         int
    interphase:    int
    mitose:        int
    noyaux:        list[Noyau]
    masque:        np.ndarray     # image binaire de la segmentation
    methode:       str            # nom du détecteur utilisé


class BaseDetector(ABC):
    """
    Interface commune pour tous les détecteurs de noyaux.
    
    Usage :
        detector = DetectorThreshold()
        resultat = detector.detect(image_adn_2d)
    """

    @abstractmethod
    def detect(self, image: np.ndarray) -> ResultatDetection:
        """
        Détecte les noyaux dans une image 2D du canal ADN.
        
        Args:
            image: array numpy 2D (Y, X) en uint16
            
        Returns:
            ResultatDetection avec tous les noyaux détectés
        """
        pass

    def nom(self) -> str:
        return self.__class__.__name__
