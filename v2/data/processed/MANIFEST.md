# Manifeste — `v2/data/processed`

Généré par `uv run python v2/data/manifest.py` ; contrôlé par `--check`. Données ouvertes seulement.
Reconstruire un fichier : lancer sa commande depuis la racine, après avoir placé les données brutes dans
`data/raw/` ou `v2/data/raw/` (voir le README).

| Fichier | Octets | SHA-256 (16) | Script | Dernier changement du script | Commande | Source |
|---|---:|---|---|---|---|---|
| `annuaire_checks.csv` | 1 152 | `ad4d3ebfea80d593` | `v2/data/build_annuaire.py` | 3713802 2026-11-14 | `uv run python v2/data/build_annuaire.py` | voir l'en-tête du script (sources et millésimes) |
| `annuaire_checks_dep.csv` | 56 499 | `361e1b359d265571` | `v2/data/build_commune.py` | 426422c 2026-11-14 | `uv run python v2/data/build_commune.py` | voir l'en-tête du script (sources et millésimes) |
| `annuaire_commune.parquet` | 571 220 | `149c232eb8bd3906` | `v2/data/build_annuaire.py` | 3713802 2026-11-14 | `uv run python v2/data/build_annuaire.py` | voir l'en-tête du script (sources et millésimes) |
| `commune_attributs.parquet` | 15 561 151 | `91c09ae6e126efb9` | `v2/data/build_attributs.py` | 5fbca72 2026-11-14 | `uv run python v2/data/build_attributs.py` | voir l'en-tête du script (sources et millésimes) |
| `commune_attributs_checks.csv` | 2 366 | `b08b01477428c697` | `v2/data/build_attributs.py` | 5fbca72 2026-11-14 | `uv run python v2/data/build_attributs.py` | voir l'en-tête du script (sources et millésimes) |
| `commune_checks.csv` | 532 637 | `ce2cb06004f6d012` | `v2/data/build_commune.py` | 426422c 2026-11-14 | `uv run python v2/data/build_commune.py` | voir l'en-tête du script (sources et millésimes) |
| `commune_geo.parquet` | 1 080 788 | `35033f7479faaee0` | `v2/data/build_commune.py` | 426422c 2026-11-14 | `uv run python v2/data/build_commune.py` | voir l'en-tête du script (sources et millésimes) |
| `commune_stock.parquet` | 1 750 725 | `933533c9ca117930` | `v2/data/build_commune.py` | 426422c 2026-11-14 | `uv run python v2/data/build_commune.py` | voir l'en-tête du script (sources et millésimes) |
| `finess_commune_annee.parquet` | 159 391 | `adabdf965c3bd3f5` | `v2/data/build_finess_histo.py` | 5fbca72 2026-11-14 | `uv run python v2/data/build_finess_histo.py` | voir l'en-tête du script (sources et millésimes) |
| `finess_histo_checks.csv` | 1 202 | `04d24590b60d173b` | `v2/data/build_finess_histo.py` | 5fbca72 2026-11-14 | `uv run python v2/data/build_finess_histo.py` | voir l'en-tête du script (sources et millésimes) |
| `flux_checks.csv` | 4 306 | `5c1f46f6ab5fb684` | `v2/data/build_flux.py` | 426422c 2026-11-14 | `uv run python v2/data/build_flux.py` | voir l'en-tête du script (sources et millésimes) |
| `flux_installations_commune.parquet` | 1 938 934 | `46f2205f7655304c` | `v2/data/build_flux.py` | 426422c 2026-11-14 | `uv run python v2/data/build_flux.py` | voir l'en-tête du script (sources et millésimes) |
| `grain_bruit.csv` | 975 | `b9b230f67ae83390` | `v2/data/build_commune.py` | 426422c 2026-11-14 | `uv run python v2/data/build_commune.py` | voir l'en-tête du script (sources et millésimes) |
| `grain_petits_effectifs.csv` | 1 700 | `ca11ea0e5c27ff4c` | `v2/data/build_commune.py` | 426422c 2026-11-14 | `uv run python v2/data/build_commune.py` | voir l'en-tête du script (sources et millésimes) |
| `infirmiers_secteur_age_sexe.parquet` | 951 901 | `43ad2c589b3b6d45` | `v2/data/build_infirmiers.py` | 3713802 2026-11-14 | `uv run python v2/data/build_infirmiers.py` | voir l'en-tête du script (sources et millésimes) |
| `infirmiers_test_hind.csv` | 6 113 | `057a4955e7a21c97` | `v2/data/build_infirmiers.py` | 3713802 2026-11-14 | `uv run python v2/data/build_infirmiers.py` | voir l'en-tête du script (sources et millésimes) |
| `officines_flux_commune.parquet` | 22 578 | `4399b0383595e40b` | `v2/data/build_finess_histo.py` | 5fbca72 2026-11-14 | `uv run python v2/data/build_finess_histo.py` | voir l'en-tête du script (sources et millésimes) |
| `passage_commune.parquet` | 887 029 | `5b92b68b91595abf` | `v2/data/build_passage.py` | 526e044 2026-11-14 | `uv run python v2/data/build_passage.py` | voir l'en-tête du script (sources et millésimes) |
| `petits_effectifs.parquet` | 1 126 154 | `88a396e5b91108a7` | `v2/data/build_passage.py` | 526e044 2026-11-14 | `uv run python v2/data/build_passage.py` | voir l'en-tête du script (sources et millésimes) |
| `petits_effectifs_classes.csv` | 3 815 | `0e20cf6914c4ad8d` | `v2/data/build_passage.py` | 526e044 2026-11-14 | `uv run python v2/data/build_passage.py` | voir l'en-tête du script (sources et millésimes) |
| `pharmaciens_checks.csv` | 304 | `c8427b572c64a6f2` | `v2/data/build_pharmaciens.py` | 526e044 2026-11-14 | `uv run python v2/data/build_pharmaciens.py` | voir l'en-tête du script (sources et millésimes) |
| `pharmaciens_checks_dep.csv` | 39 719 | `21cefe08468ab350` | `v2/data/build_pharmaciens.py` | 526e044 2026-11-14 | `uv run python v2/data/build_pharmaciens.py` | voir l'en-tête du script (sources et millésimes) |
| `pharmaciens_commune_annee.parquet` | 764 932 | `17aabc1e5e2313e6` | `v2/data/build_pharmaciens.py` | 526e044 2026-11-14 | `uv run python v2/data/build_pharmaciens.py` | voir l'en-tête du script (sources et millésimes) |
| `secteur_checks.csv` | 3 275 | `ce9b96739f76e14a` | `v2/data/build_secteur.py` | 426422c 2026-11-14 | `uv run python v2/data/build_secteur.py` | voir l'en-tête du script (sources et millésimes) |
| `secteur_finess_shares.csv` | 234 | `078447b103c1e4a5` | `v2/data/build_secteur.py` | 426422c 2026-11-14 | `uv run python v2/data/build_secteur.py` | voir l'en-tête du script (sources et millésimes) |
| `secteur_split.parquet` | 726 974 | `47a2f38638fa3907` | `v2/data/build_secteur.py` | 426422c 2026-11-14 | `uv run python v2/data/build_secteur.py` | voir l'en-tête du script (sources et millésimes) |
| `secteur_stock.parquet` | 1 537 834 | `c784b1a8bad55cbd` | `v2/data/build_secteur.py` | 426422c 2026-11-14 | `uv run python v2/data/build_secteur.py` | voir l'en-tête du script (sources et millésimes) |
| `sise_sante.parquet` | 3 291 | `cabeddf8b1059e2c` | `v2/data/build_sise.py` | f072f9e 2026-11-15 | `uv run python v2/data/build_sise.py` | voir l'en-tête du script (sources et millésimes) |
| `sise_sante_region.parquet` | 6 235 | `196c1b0a39b43258` | `v2/data/build_sise.py` | f072f9e 2026-11-15 | `uv run python v2/data/build_sise.py` | voir l'en-tête du script (sources et millésimes) |
| `zonage_commune.parquet` | 909 372 | `4e5da69f54064415` | `v2/data/build_zonage.py` | a0c02a3 2026-11-14 | `uv run python v2/data/build_zonage.py` | voir l'en-tête du script (sources et millésimes) |
