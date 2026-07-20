import os

IMAGES_ROOT_WIN = os.environ.get('IMAGES_ROOT', '')
chemin = 'E:\\dataset_stages_bio_inofs\\WT'

print('IMAGES_ROOT_WIN:', IMAGES_ROOT_WIN)
print('chemin:', chemin)
print('startswith:', chemin.startswith(IMAGES_ROOT_WIN))

if IMAGES_ROOT_WIN and chemin.startswith(IMAGES_ROOT_WIN):
    sous_dossier = chemin[len(IMAGES_ROOT_WIN):].replace('\\', '/').lstrip('/')
    resultat = f'/data/images/{sous_dossier}'
    print('sous_dossier:', sous_dossier)
    print('resultat:', resultat)
else:
    print('Pas de conversion !')
