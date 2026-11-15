"""C5 : la région de formation (université -> ARS) prédit-elle la région d'installation ? (exploratoire)

Étudiants : MESR SISE, données ouvertes (v2/data/processed/sise_sante_region.parquet, v2/data/build_sise.py),
région de l'établissement, DE années 2 à 6 (année 6 = année 5 de la rentrée précédente, comme sante.pipeline),
moyenne des rentrées 2020–2024. Jusqu'au 2026-11-15, le script lisait un fichier d'inscrits fourni à l'équipe
sous accord de confidentialité (colonne ARS) ; sortie de cette version : v2/methodes/out/c5_990.csv. Entrées : flux net I des tranches d'entrée calibré sur le
périmètre privé (fenêtre 2019–2026), sommé par région. On compare deux prédicteurs de la part régionale
des entrées : la part des étudiants et la part du stock actuel. Si la part étudiante n'ajoute rien à la
part du stock, répartir les entrées par région de formation n'améliorera pas la prévision.
Lancer : PYTHONPATH=v2 uv run python -m methodes.c5"""
import numpy as np
import pandas as pd

from methodes.calibrage import dep_to_region, fit
from methodes.perimetres import prive

PROFS = ["dentistes", "pharmaciens"]

f = pd.read_parquet("v2/data/processed/sise_sante_region.parquet")
f = f[f.k.between(2, 5)]
f = pd.concat([f, f[f.k == 5].assign(k=6, year=lambda x: x.year + 1)])        # année 6 dérivée
f = f[f.year.between(2020, 2024)]
reg = dep_to_region().replace({"01": "AG", "02": "AG", "03": "AG", "04": "OI", "06": "OI", "94": "93"})
t = prive()
rows = []
for p in PROFS:
    st = f[f.profession == p].groupby(["region", "year"]).n.sum().groupby("region").mean()
    tp = t[t.profession == p]
    c = fit(tp, (2019, 2026), shrink=200)
    inflow = pd.Series(c["inflow"].sum(1), index=c["cells"].dep).groupby(lambda d: reg.get(d)).sum()
    stock = tp[tp.year == 2026].groupby("dep").n.sum().groupby(lambda d: reg.get(d)).sum()
    d = pd.DataFrame({"etudiants": st, "entrees": inflow, "stock": stock}).dropna()
    sh = d / d.sum()
    for x in ("etudiants", "stock"):
        r = np.corrcoef(sh[x], sh.entrees)[0, 1]
        mae = (sh[x] - sh.entrees).abs().mean() * 100
        rows.append({"profession": p, "predicteur": x, "r": round(r, 3), "erreur_abs_moy_pts_part": round(mae, 2),
                     "regions": len(d)})
    sh.assign(profession=p).to_csv(f"v2/methodes/out/c5_{p}.csv")
out = pd.DataFrame(rows)
print(out.to_string(index=False))
out.to_csv("v2/methodes/out/c5.csv", index=False)
