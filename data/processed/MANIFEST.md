# Manifeste — `data/processed`

Généré par `uv run python v2/data/manifest.py` ; contrôlé par `--check`. Données ouvertes seulement.
Reconstruire un fichier : lancer sa commande depuis la racine, après avoir placé les données brutes dans
`data/raw/` ou `v2/data/raw/` (voir le README).

| Fichier | Octets | SHA-256 (16) | Script | Dernier changement du script | Commande | Source |
|---|---:|---|---|---|---|---|
| `checks.csv` | 3 868 | `b9aeeae51ad65420` | `v2/sante/load.py` | 426422c 2026-11-14 | `PYTHONPATH=v2 uv run python -m sante.load` | DREES RPPS 2012–2026 par profession (dép × âge × sexe × mode) ; Insee Omphale 2022, 3 scénarios |
| `population.parquet` | 1 222 951 | `0ae163df52c63047` | `v2/sante/load.py` | 426422c 2026-11-14 | `PYTHONPATH=v2 uv run python -m sante.load` | DREES RPPS 2012–2026 par profession (dép × âge × sexe × mode) ; Insee Omphale 2022, 3 scénarios |
| `stock.parquet` | 2 794 213 | `c73024b1ed61a37e` | `v2/sante/load.py` | 426422c 2026-11-14 | `PYTHONPATH=v2 uv run python -m sante.load` | DREES RPPS 2012–2026 par profession (dép × âge × sexe × mode) ; Insee Omphale 2022, 3 scénarios |
| `stock_ameli.parquet` | 1 601 446 | `98852c8eba3b1e1c` | `v2/sante/ameli.py` | 426422c 2026-11-14 | `PYTHONPATH=v2 uv run python -m sante.ameli` | data.ameli.fr, démographie des professionnels libéraux (modifié le 2026-10-28) |
| `stock_commune.parquet` | 2 428 833 | `2f7b616041698ef0` | `v2/sante/cartosante.py` | 426422c 2026-11-14 | `PYTHONPATH=v2 uv run python -m sante.cartosante` | CartoSanté (Atlasanté), effectifs libéraux par commune × âge, 2004–2025 |
| `stock_nurses_salaried.parquet` | 230 693 | `3fd9f1b743d8a1f1` | `v2/sante/nurses.py` | 426422c 2026-11-14 | `PYTHONPATH=v2 uv run python -m sante.nurses` | DREES, infirmiers salariés (BTS), 2023, ratissés dép × âge × sexe |
