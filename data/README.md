# À propos des données

## Provenance

- https://donnees.montreal.ca/dataset/arbres
  - Inventaire arbres publics - Fichier consolidé
    - Date de téléchargement : 2026-07-09
  - État de l'inventaire d'arbres par arrondissement
    - Date de téléchargement : 2026-07-09
- https://donnees.montreal.ca/dataset/cyclistes
  - Vélos - comptage sur les pistes cyclables, 2025
    - Date de téléchargement : 2026-07-08
  - Localisation des compteurs (2009-2025)
    - Date de téléchargement : 2026-07-08
- https://donnees.montreal.ca/dataset/mesure-impact-projets-verdissement
  - Mesure de l'impact des projets de verdissement (2023)
  - Mesure de l'impact des projets de verdissement (2024)
  - Mesure de l'impact des projets de verdissement - janvier à juin (2025)
  - Mesure de l'impact des projets de verdissement - Juillet à décembre (2025)
    - Date de téléchargement : 2026-08-05
- https://donnees.montreal.ca/dataset/permis-construction
  - Statistiques sur les permis de construction, transformation et démolition
    - Date de téléchargement : 2026-08-04

## Création des fichiers

Mesures de température et d'humidité relative de l'air :
* `air_par_date.csv`
* `air_points_rosee.csv`
* `air_stations.csv`
```Bash
python preparer_air.py
```

Inventaire des arbres dans les parcs :
* `arbres_emplacements.csv`
* `arbres_essences.csv`
* `arbres_inv.csv`
* `arbres_parcs.csv`
* `mtl_arrondissements.csv`
```Bash
python preparer_arbres.py
```

Permis de construction :
* `construction_permis.csv`
* `mtl_arrondissements.csv` (réutilisation)
```Bash
python preparer_construction.py
```

Passages de vélos :
* `compteurs_velo.csv` (copie des données brutes)
* `velos_par_date.csv`
* `velos_par_heure.csv`
```Bash
python preparer_velos.py
```
