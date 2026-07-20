"""
Projection Z : réduit un stack 3D (Z, Y, X) en une image 2D (Y, X).
Plusieurs méthodes disponibles.
"""
import numpy as np


def projection_max(stack: np.ndarray) -> np.ndarray:
    """
    Projection Z maximum — prend le pixel le plus brillant de chaque plan.
    Meilleure pour détecter toutes les structures, même peu focalisées.
    Recommandée pour le comptage des noyaux.
    
    Args:
        stack: array (Z, Y, X)
    Returns:
        image 2D (Y, X)
    """
    return np.max(stack, axis=0)


def projection_mean(stack: np.ndarray) -> np.ndarray:
    """
    Projection Z moyenne — moyenne de tous les plans.
    Image plus douce, réduit le bruit.
    """
    return np.mean(stack, axis=0).astype(stack.dtype)


def projection_sum(stack: np.ndarray) -> np.ndarray:
    """
    Projection Z somme — somme de tous les plans.
    Plus lumineux, bon pour la mesure d'intensité totale.
    """
    return np.sum(stack, axis=0).astype(np.float32)


def projeter(stack: np.ndarray, methode: str = "max") -> np.ndarray:
    """
    Point d'entrée unique pour la projection Z.
    
    Args:
        stack  : array (Z, Y, X)
        methode: "max" | "mean" | "sum"
    Returns:
        image 2D (Y, X)
    """
    methodes = {
        "max":  projection_max,
        "mean": projection_mean,
        "sum":  projection_sum,
    }
    if methode not in methodes:
        raise ValueError(f"Méthode inconnue : {methode}. Choisir parmi {list(methodes.keys())}")

    return methodes[methode](stack)
