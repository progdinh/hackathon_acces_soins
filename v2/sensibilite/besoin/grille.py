"""Axe 5 du besoin, étape 1 : grille factorielle de Y = log C(p, T, t) (protocole gelé 2026-11-15, SHA-256 10a5b285…).

Par profession :
  politique π   trajectoires du modèle servi (prototype.server.Model, C1) sous les leviers « dd76 », plus L23 (PH)
  estimateur e  M0, M1, M2a (sauf PH), M3 (IDE) ; variantes rapportées : M3 en recoupement, M1 sous P2 (DAMIR)
  Omphale ω     central, pop_basse, pop_haute
  offre k       K tirages de C1 (méthode, privé, dép.), appliqués en écart relatif ρ_k = tirage / moyenne
  transfert j   PH, cellule L23 : J tirages de (s∞, τ, k, μ, a) dans les plages gelées
Écrit v2/sensibilite/besoin/out/grille_<profession>.npz : Y[π, e, ω, k, j, T, année], T = départements + « FR ».

Run (racine) : PYTHONPATH=v2 uv run --with scipy python -W ignore -m sensibilite.besoin.grille [--prof p] [--k 100]
"""
import argparse
import json
import subprocess
import time
from dataclasses import replace
from pathlib import Path

import numpy as np

from besoin.couverture import aligne, offre
from besoin.cube import Cube, Population
from besoin.estimateurs.m0 import M0
from besoin.estimateurs.m1 import M1
from besoin.estimateurs.m2a import M2a
from besoin.estimateurs.m3 import M3
from besoin.transferts import appliquer, l23

OUT = Path("v2/sensibilite/besoin/out")
REF, YEARS = 2026, (2026, 2035, 2050)
SEED, K, J = 20261115, 100, 40
PROFS = ("sages-femmes", "dentistes", "pharmaciens", "kines", "infirmiers")
OMPHALE = ("central", "pop_basse", "pop_haute")
SERVI = {"infirmiers": "M3"}                                     # sinon M1
ESTIMATEURS = {"infirmiers": ("M0", "M1", "M2a", "M3"), "pharmaciens": ("M0", "M1")}   # sinon M0, M1, M2a
VARIANTES = ("M3", "M1-P2")                                     # rapportées, hors ensemble décisif
# L23 central (gel) et plages des tirages : s∞, τ (P-B6 ± 1 é.-t., dérivé), k, μ, a (supposés)
L23_CENTRAL = dict(s_inf=0.74, tau=2.4, k=0.625, mu=0.0, a=0.01)
L23_PLAGES = dict(s_inf=(0.67, 0.81), tau=(1.9, 2.9), k=(0.25, 1.0), mu=(0.0, 0.05), a=(0.005, 0.02))
L23_T0 = 2019            # début de la courbe mesurée (P-B6)
L23_REF = 2026           # année de base : seule la part au-delà de s(2026) agit (décision P1-4, 2026-11-15)
BASE = dict(quotas=1, quotas_region=False, etrangers=1, retraite=0, cumul=1, precoces=1, regul=False, part_zones=0,
            dest="voisine")


def politiques(prof: str, zones: dict) -> dict:
    """Nom -> leviers du modèle servi (amplitudes « dd76 », axe 5 de l'offre) ; L23 : statu quo de l'offre."""
    p = {"statu quo": {}, "quotas x0,8": dict(quotas=0.8), "quotas x1,2": dict(quotas=1.2),
         "retraite +2 ans": dict(retraite=2), "cumul x0,5": dict(cumul=0.5), "cumul x2": dict(cumul=2.0),
         "precoces x0,5": dict(precoces=0.5), "precoces x1,5": dict(precoces=1.5),
         "etrangers x0,5": dict(etrangers=0.5), "etrangers x2": dict(etrangers=2.0)}
    if zones.get(prof):
        p["regulation (toutes zones)"] = dict(regul=True, part_zones=1.0)
    if prof == "pharmaciens":
        p["L23 vaccination en officine"] = {}
    return {k: BASE | v for k, v in p.items()}


def estimateur(name: str):
    return {"M0": M0, "M1": M1, "M2a": M2a, "M3": M3, "M1-P2": lambda: M1(profil="damir")}[name]()


def offres(prof: str, pol: dict):
    """Offre S[π] (Cube, dép.) par politique, et l'état de base (statu quo) pour l'ajustement des estimateurs."""
    from prototype.server import Model, zones
    m = Model(prof)
    base = {m.o: m.est.state, **m.base.states}
    S = {}
    for name, lv in pol(zones()).items():
        tr = m.base if lv == BASE else m.est.trajectory(YEARS[-1], m.scenario(lv))
        S[name] = offre({m.o: m.est.state, **tr.states}, YEARS)
    return S, base, m.o


def tirages_c1(prof: str, territories, k: int) -> np.ndarray:
    """ρ[k, T, année] = tirage / moyenne a posteriori de C1 (méthode, secteur privé) ; 1 pour t ≤ origine."""
    from jumeau.scenario import Scenario
    from methodes.cohortes import COMPOSITION
    from methodes.perimetres import IDE, prive
    from validation import registry
    code = IDE if prof == "infirmiers" else prof
    t = prive()
    t = t[t.profession == code]
    o = int(t.year.max())
    est = registry.get("axe2_cohortes_c1")().fit(t, (2017 if prof == "kines" else 2012, o), o)
    terr = list(territories)
    rho = np.ones((k, len(terr), len(YEARS)))
    after = [i for i, y in enumerate(YEARS) if y > o]
    moy = est.trajectory(YEARS[-1], Scenario(modules=COMPOSITION))
    mean = {YEARS[i]: moy.states[YEARS[i]].total() for i in after}
    for d in range(k):
        tr = est.trajectory(YEARS[-1], Scenario(name=f"t{d}", params={"cohortes.tirage": d}, modules=COMPOSITION))
        for i in after:
            y = YEARS[i]
            v = (tr.states[y].total() / mean[y]).droplevel(0)
            rho[d, :, i] = v.reindex(terr).fillna(1.0).to_numpy()
    return rho, o


def logC(S: Cube, S0: Cube, B: Cube, B0: Cube, prof: str, rho: np.ndarray, terr) -> np.ndarray:
    """Y[k, T, année] pour T = départements de `terr` + FR ; ρ (aligné sur `terr`) multiplie S et S₀ (même tirage),
    C indexé à REF sur (S₀, B₀). Les territoires que `aligne` ajoute (population sans offre) sont retirés."""
    S, B = aligne(S, B)
    S0, B0 = aligne(S0, B0)
    keep = np.searchsorted(S.territories, terr)
    S, B, S0, B0 = (replace(c, territories=c.territories[keep], values=c.values[:, keep]) for c in (S, B, S0, B0))
    i, j = S.p(prof), B.p(prof)
    s, s0 = S.values[i][None] * rho, S0.values[i][None] * rho        # [k, T, année]
    b, b0 = B.values[j][None], B0.values[j][None]
    r = S.y(REF)
    with np.errstate(divide="ignore", invalid="ignore"):
        dep = np.log(s / b) - np.log(s0[:, :, r:r + 1] / b0[:, :, r:r + 1])
        nat = np.log(s.sum(1) / b.sum(1)) - np.log(s0[:, :, r].sum(1) / b0[:, :, r].sum(1))[:, None]
    return np.concatenate([dep, nat[:, None, :]], axis=1)


def l23_tirages(j: int, rng) -> list[dict]:
    return [{k: rng.uniform(*v) for k, v in L23_PLAGES.items()} for _ in range(j)]


def run(prof: str, k: int = K, j: int = J) -> dict:
    t0 = time.time()
    rng = np.random.default_rng(SEED + PROFS.index(prof))
    S, base, o = offres(prof, lambda z: politiques(prof, z))
    print(f"{prof}: {len(S)} politiques ({time.time() - t0:.0f} s)", flush=True)
    S0 = S["statu quo"]
    rho, o_c1 = tirages_c1(prof, S0.territories, k)
    rho0 = np.ones((1,) + rho.shape[1:])
    print(f"{prof}: {k} tirages C1, origine {o_c1} ({time.time() - t0:.0f} s)", flush=True)
    noms_e = ESTIMATEURS.get(prof, ("M0", "M1", "M2a"))
    noms_v = tuple(v for v in VARIANTES if v not in noms_e and not (v == "M3" and prof == "infirmiers"))
    pols = list(S)
    jd = l23_tirages(j, rng) if prof == "pharmaciens" else []
    nj = max(1, len(jd))
    terr = list(S0.territories) + ["FR"]
    Y = np.full((len(pols), len(noms_e), len(OMPHALE), k, nj, len(terr), len(YEARS)), np.nan)
    Yref = np.full((len(pols), len(noms_e) + len(noms_v), len(OMPHALE), len(terr), len(YEARS)), np.nan)  # offre moyenne
    Yl23c = {}                                                    # L23 central, offre moyenne, par (e, ω)
    for w, scen in enumerate(OMPHALE):
        pop = Population.load(scen)
        for ie, en in enumerate(noms_e + noms_v):
            est = estimateur(en).fit(pop, base, REF)
            B0 = est.predict(pop, base, list(YEARS))
            for ip, pn in enumerate(pols):
                if pn.startswith("L23"):
                    if "medecine-generale" not in set(B0.professions):
                        continue                                  # variante sans besoin source : L23 non défini
                    Bc, _ = appliquer(B0, [l23(L23_REF, **L23_CENTRAL)])
                    Yref[ip, ie, w] = logC(S[pn], S0, Bc, B0, prof, rho0, S0.territories)[0]
                    if ie < len(noms_e):
                        for jj, par in enumerate(jd):
                            Bj, _ = appliquer(B0, [l23(L23_REF, **par)])
                            Y[ip, ie, w, :, jj] = logC(S[pn], S0, Bj, B0, prof, rho, S0.territories)
                    continue
                Yref[ip, ie, w] = logC(S[pn], S0, B0, B0, prof, rho0, S0.territories)[0]
                if ie < len(noms_e):
                    Y[ip, ie, w] = logC(S[pn], S0, B0, B0, prof, rho, S0.territories)[:, None]
            print(f"{prof}: {scen} {en} ({time.time() - t0:.0f} s)", flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(OUT / f"grille_{prof}.npz", Y=Y.astype(np.float32), Yref=Yref, politiques=pols,
                        estimateurs=noms_e, variantes=noms_v, omphale=OMPHALE, territoires=terr, annees=YEARS,
                        l23_tirages=json.dumps(jd))
    meta = dict(profession=prof, origine_jumeau=o, origine_c1=o_c1, k=k, j=nj, secondes=round(time.time() - t0, 1),
                commit=subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip())
    (OUT / f"grille_{prof}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    print(f"{prof}: fini ({meta['secondes']} s)", flush=True)
    return meta


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--prof", choices=PROFS)
    a.add_argument("--k", type=int, default=K)
    args = a.parse_args()
    for p in [args.prof] if args.prof else PROFS:
        run(p, args.k)


if __name__ == "__main__":
    main()
