"""
Cache partagé entre tous les modules backend.
Un seul endroit pour stocker le fichier en cours.
"""

cache = {
    "chemin":   None,
    "data":     None,
    "total_z":  0,
    "n_canaux": 0,
    "hauteur":  0,
    "largeur":  0,
}
