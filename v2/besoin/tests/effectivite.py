"""Contrôles de l'outil d'effectivité des transferts (O3).

Run : PYTHONPATH=v2 uv run python -m besoin.tests.effectivite
  E1  s ≡ 0 : couvertures identiques avec et sans transfert, à 1e-12 ; aucun ETP libéré
  E2  source : C'_A / C_A = 1 / (1 − s·a) exactement (l'offre MG ne bouge pas, seul le besoin baisse)
  E3  k ne change pas le gain de la source, et la perte de la cible croît avec k
  E4  offre MG lue en entrée : 66 503 généralistes libéraux et mixtes en 2026 (RPPS, hors dép. 999 « inconnu », 3 personnes), à l'unité
"""
import numpy as np

from besoin.effectivite import evaluer
from besoin.offre_mg import stock_mg

ok = True


def check(nom, cond, mesure):
    global ok
    ok &= bool(cond)
    print(f"{'OK ' if cond else 'ÉCHEC'} {nom} : {mesure}")


r0 = evaluer("L23", s_inf=0.0)
d = r0["par_k"][max(r0["k"])]
ecart = max(np.nanmax(abs(d["couverture_cible"] - r0["C0_cible"])), np.nanmax(abs(d["couverture_source"] - r0["C0_source"])))
check("E1 s ≡ 0", ecart < 1e-12 and np.allclose(d["etp_liberes"], 0), f"écart max {ecart:.1e}")

r = evaluer("L23")
tr = r["transfert"]
sa = tr.s(r["years"]) * tr.a
d = r["par_k"][max(r["k"])]
attendu = r["C0_source"] / (1 - sa[None, :])
e2 = np.nanmax(abs(d["couverture_source"] - attendu))
check("E2 source = 1 / (1 − s·a)", e2 < 1e-12, f"écart max {e2:.1e}")

lo, hi = r["par_k"][min(r["k"])], r["par_k"][max(r["k"])]
same = np.nanmax(abs(lo["gain_source"] - hi["gain_source"]))
mono = np.nanmin(lo["perte_cible"] - hi["perte_cible"])
check("E3 k : gain source inchangé, perte cible croissante", same < 1e-12 and mono >= -1e-12,
      f"écart de gain {same:.1e}, min(perte(k bas) − perte(k haut)) {mono:.1e}")

n = stock_mg().sum()
check("E4 offre MG 2026", round(n) == 66503, f"{n:.0f} généralistes libéraux et mixtes")
raise SystemExit(0 if ok else 1)
