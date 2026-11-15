"""Écran de décision V2 (carte plein écran) : sert index.html, /geo et /api/* du prototype V1.

Run (racine du dépôt) : uv run python v2/prototype-carte/server.py [port]   -> http://localhost:8767

Réutilise v2/prototype/server.py (Model, leviers par famille, parse_levers : mêmes bornes que /api/scenario).
Ajouts : /geo (contours départementaux, coordonnées arrondies à 1e-3°, gzip) et /api/carte
(une valeur 2026 / 2050 par département, tendanciel et scénario, en un seul appel), /api/interpret
(phrase d'un·e élu·e -> réglage des leviers, par le compilateur déterministe de v2/langage),
/api/agent (POST : question -> relais vers le chatbot de chatbot/, port 8768, qui explique les sorties sans calculer ;
la clé ANTHROPIC_API_KEY reste dans son processus) et /api/agent/etat.
"""
import gzip
import importlib.util
import json
import os
import re
import sys
import time
from functools import lru_cache
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("proto_v1", HERE.parent / "prototype" / "server.py")
V1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V1)   # fait le chdir vers la racine et charge le jumeau

# Compilateur langage naturel (v2/langage) : il réutilise le module V1 déjà chargé, pas de second jumeau
spec = importlib.util.spec_from_file_location("compilateur", HERE.parent / "langage" / "compilateur.py")
NL = importlib.util.module_from_spec(spec)
spec.loader.exec_module(NL)
NL.serveur = lambda: V1

GEO = HERE / "assets" / "departements-avec-outre-mer.geojson"


def _round(c):
    return [_round(x) for x in c] if isinstance(c[0], list) else [round(c[0], 3), round(c[1], 3)]


_GEO: bytes = b""
# DROM en encarts près de la métropole (comme les cartes Insee) : centre cible (lon, lat) et facteur d'échelle.
# Positions schématiques, pas géographiques ; le survol et la fiche donnent le vrai nom.
ENCARTS = {"971": (-6.9, 48.1, 0.9), "972": (-6.9, 47.1, 1.4), "973": (-6.9, 45.9, 0.3),
           "974": (-6.9, 44.7, 1.0), "976": (-6.9, 43.7, 1.6)}


def _encart(f):
    code = f["properties"]["code"]
    if code not in ENCARTS:
        return
    tx, ty, k = ENCARTS[code]
    pts = []
    def walk(c):
        if isinstance(c[0], list):
            for x in c:
                walk(x)
        else:
            pts.append(c)
    walk(f["geometry"]["coordinates"])
    cx = (min(p[0] for p in pts) + max(p[0] for p in pts)) / 2
    cy = (min(p[1] for p in pts) + max(p[1] for p in pts)) / 2
    for p in pts:
        p[0], p[1] = tx + (p[0] - cx) * k, ty + (p[1] - cy) * k


def geo_bytes() -> bytes:
    global _GEO
    if not _GEO:
        g = json.loads(GEO.read_text())
        for f in g["features"]:
            _encart(f)
            f["geometry"]["coordinates"] = _round(f["geometry"]["coordinates"])
        _GEO = gzip.compress(json.dumps(g, separators=(",", ":")).encode(), 6)
    return _GEO


_REG: bytes = b""


def regions_bytes() -> bytes:
    """Limites régionales sans géométrie externe : arêtes des départements dont les deux côtés sont
    dans deux régions différentes (les côtes se lisent sur le fond). Coordonnées arrondies : les arêtes communes coïncident."""
    global _REG
    if not _REG:
        g = json.loads(gzip.decompress(geo_bytes()))
        reg = V1.geo().region.to_dict()
        seen: dict = {}
        n: dict = {}
        for f in g["features"]:
            r = reg.get(f["properties"]["code"], f["properties"]["code"])
            polys = f["geometry"]["coordinates"] if f["geometry"]["type"] == "MultiPolygon" else [f["geometry"]["coordinates"]]
            for poly in polys:
                for ring in poly:
                    for a, b in zip(ring, ring[1:]):
                        if a != b:
                            k = tuple(sorted((tuple(a), tuple(b))))
                            seen.setdefault(k, set()).add(r)
                            n[k] = n.get(k, 0) + 1
        lines = [list(map(list, k)) for k, rs in seen.items() if len(rs) > 1]
        cote = [list(map(list, k)) for k in seen if n[k] == 1]   # arête d'un seul département : côte ou frontière
        out = {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {},
               "geometry": {"type": "MultiLineString", "coordinates": lines}},
               {"type": "Feature", "properties": {"cote": 1}, "geometry": {"type": "MultiLineString", "coordinates": cote}}]}
        _REG = gzip.compress(json.dumps(out, separators=(",", ":")).encode(), 6)
    return _REG


def carte(prof: str, lv: dict, terr: str = "FR") -> dict:
    """Effectif libéral par département : observé à l'origine, tendanciel et scénario en 2026 et 2050."""
    m = V1.model(prof)
    t0 = time.perf_counter()
    scn = m.est.trajectory(V1.H, m.scenario(lv, terr))
    codes = np.unique(m.cells.territory.to_numpy()[(m.cells.sector == "prive").to_numpy()])

    def agg(tr, y):
        # cellules propres à chaque trajectoire : la régulation ajoute un secteur « bloques » au scénario
        st = tr.states[y]
        pr = (st.cells.sector == "prive").to_numpy()
        tot = pd.Series(np.asarray(st.N)[pr].reshape(int(pr.sum()), -1).sum(1), index=st.cells.territory.to_numpy()[pr])
        return tot.groupby(level=0).sum().reindex(codes).fillna(0).to_numpy()
    obs = m.obs.xs(m.o, level=1).reindex(codes).fillna(0).to_numpy()
    y26 = max(V1.DECISION, m.o)   # 2026 = origine actuelle : valeur observée
    b26, s26 = (obs, obs) if y26 <= m.o else (agg(m.base, y26), agg(scn, y26))
    b50, s50 = agg(m.base, V1.H), agg(scn, V1.H)
    P = V1.population().loc[lv["pop_scen"]]          # habitants, Insee Omphale 2022, scénario choisi
    pp = lambda d, y: float(P.loc[y, d]) if d in P.columns else 0.0
    # séries annuelles y26..H pour le curseur d'année (le moteur garde déjà chaque année)
    years = list(range(y26, V1.H + 1))
    B = np.column_stack([b26 if y == y26 else agg(m.base, y) for y in years])
    S_ = np.column_stack([s26 if y == y26 else agg(scn, y) for y in years])
    r = lambda v: round(float(v), 1)
    out = {d: {"o": float(obs[i]), "b26": float(b26[i]), "s26": float(s26[i]), "b50": float(b50[i]), "s50": float(s50[i]),
               "p26": pp(d, y26), "p50": pp(d, V1.H),
               "b": [r(v) for v in B[i]], "s": [r(v) for v in S_[i]], "p": [round(pp(d, y)) for y in years]}
           for i, d in enumerate(codes)}
    return {"prof": prof, "origin": m.o, "y26": y26, "years": years, "k": m.k, "deps": out, "activite": lv["activite"], "pop_scen": lv["pop_scen"],
            "regul_deps": V1.zones().get(prof, []), "ms": round((time.perf_counter() - t0) * 1000, 1)}


# --- Besoin et indice de couverture (plan v2/docs/lab/derivations/2026-11-15-besoin-carte-plan.md) ----------------
# C(T,t) = [S(T,t) / B(T,t)] / [S_base(T,2026) / B_base(T,2026)] : indice relatif, 2026 = 1, jamais un « % du besoin
# couvert ». S = séries b/s de carte() (aucun second passage du jumeau) ; B = besoin_api sur les états de base, mis en
# cache (le besoin ne dépend que de la population, pas des leviers d'offre). O2 : aucune clé pour la MG ni les spécialistes.
sys.path.insert(0, str(HERE.parent))
from besoin.couverture import SANS_COUVERTURE  # noqa: E402
from besoin.cube import Population  # noqa: E402
from besoin.interface import discover  # noqa: E402
from besoin.sortie import besoin_api  # noqa: E402
from besoin.transferts import L23_PARAMS, Transfert, l23  # noqa: E402
from jumeau.state import State  # noqa: E402

# Estimateurs servis par profession : survivants des protocoles (M1 socle P-B1/P-B5, M2a, M3 pour IDE seulement ; M2b tué).
SURVIVANTS = {"infirmiers": ("M1", "M2a", "M3"), "kines": ("M1", "M2a"), "dentistes": ("M1", "M2a"),
              "sages-femmes": ("M1", "M2a"), "pharmaciens": ("M1",)}
CENTRAL = "M1"
EN_ATTENTE = [{"estimateur": "M4", "actif": False, "statut": "en attente de validation (P-B4)",
               "doc": "2SFCA (famille de l'APL), à la commune ; servi quand P-B4 sera tranché"}]
SEUIL_FOURCHETTE = 0.05      # (max − min) / central en 2050 : au-delà, la fourchette de modèle est montrée (supposé, plan)
INJ_MG_2018 = 2.6e6          # injections antigrippales en consultation de médecin, 2018 (Cour des comptes, G10.csv ; fiche L23)
L23_BORNES = {"a": (0.0, 0.05), "k": (0.25, 1.0)}   # plages des fiches (k : fiche L23) ; a : en temps de MG, supposé
# Transfert hypothétique (plan v2/docs/lab/derivations/2026-11-15-transfert-hypothetique-plan.md) : forme de L23, paramètres
# de l'utilisateur·rice, jamais un levier sourcé. Défauts supposés ; τ = forme de L23 (P-B6), empruntée.
TR_BORNES = {"a": (0.0, 0.5), "sinf": (0.0, 1.0), "k": (0.1, 3.0), "tau": (0.1, 20.0), "t0": (2026, 2050)}
TR_DEFAUT = {"a": 0.10, "sinf": 1.0, "k": 1.0, "tau": 2.4, "t0": 2026}
TR_UNITES = {"a": "part de la demande de la source concernée par l'acte", "sinf": "part de l'acte transférée à terme",
             "k": "temps de la cible par unité de temps de la source", "tau": "années (montée en charge)", "t0": "année d'autorisation"}
TR_SOURCES = ("medecine-generale", "specialistes") + tuple(SURVIVANTS)
# Niveau de la demande des sources hors des 5 (transfert hypothétique seulement ; L23 garde le niveau de M1) : effectif
# libéral France au 1er janvier 2025, ameli « Démographie des professionnels de santé » (data/raw/ameli/…, classe
# tout_age, tout sexe, région FRANCE), 1 professionnel = 1 temps plein comme pour les cibles. Mesuré.
NIVEAU_SOURCE = {"medecine-generale": 56005, "specialistes": 57346}
_BES: dict = {}
_CAR: dict = {}
_BSRC: dict = {}


@lru_cache(maxsize=1)
def _pop() -> Population:
    return Population.load()


def _etats(prof: str) -> dict:
    """Année -> State de base, de 2026 à H ; 2026 observé quand c'est l'origine du jumeau."""
    m = V1.model(prof)
    e = {y: s for y, s in m.base.states.items() if y >= V1.DECISION}
    if V1.DECISION not in e:
        e[V1.DECISION] = State.from_table(m.t, m.o, "dep")
    return dict(sorted(e.items()))


def _l23_params(q: dict) -> tuple[dict | None, str | None]:
    """l23=0|1 et, en mode expert, l23_a, l23_k dans les plages des fiches."""
    if str(q.get("l23", "0")) not in ("1", "true"):
        return None, None
    ov = {}
    for k, (lo, hi) in L23_BORNES.items():
        if f"l23_{k}" in q:
            try:
                v = float(q[f"l23_{k}"])
            except ValueError:
                return None, f"l23_{k} : valeur non numérique"
            if not lo <= v <= hi:
                return None, f"l23_{k} hors bornes [{lo} ; {hi}] : {v}"
            ov[k] = v
    return ov, None


def _tr_params(q: dict, prof: str) -> tuple[tuple | None, str | None]:
    """tr_src, tr_cible et, facultatifs, tr_a, tr_sinf, tr_k, tr_tau, tr_t0 -> (Transfert, paramètres réglés).
    O2 : la cible est l'une des 5 professions ; la MG et les spécialistes ne sont admis qu'en source."""
    if "tr_src" not in q and "tr_cible" not in q:
        return None, None
    src, cib = q.get("tr_src"), q.get("tr_cible")
    if cib not in SURVIVANTS:
        return None, f"tr_cible {cib!r} : l'une de {', '.join(SURVIVANTS)} (O2 : MG et spécialistes en source seulement)"
    if src not in TR_SOURCES:
        return None, f"tr_src {src!r} : l'une de {', '.join(TR_SOURCES)}"
    if src == cib:
        return None, "tr_src = tr_cible"
    if prof not in (src, cib):
        return None, f"transfert {src} → {cib} sans effet sur {prof} : afficher la cible ou la source"
    v, regles = dict(TR_DEFAUT), []
    for k, (lo, hi) in TR_BORNES.items():
        if f"tr_{k}" in q:
            try:
                x = float(q[f"tr_{k}"])
            except ValueError:
                return None, f"tr_{k} : valeur non numérique"
            if not lo <= x <= hi:
                return None, f"tr_{k} hors bornes [{lo} ; {hi}] : {x}"
            v[k], regles = x, regles + [k]
    try:
        tr = Transfert("transfert hypothétique (paramètres de l'utilisateur)", src, cib, v["a"], v["k"], v["sinf"], v["tau"],
                       int(v["t0"]))
    except ValueError as e:
        return None, str(e)
    return (tr, regles), None


def besoin_source(src: str, cible: str, est: str) -> tuple[list, list, np.ndarray, str]:
    """B de la source d'un transfert hypothétique : (territoires, années, B [territoire, année], estimateur).
    Une des 5 : son propre besoin (même estimateur s'il survit pour elle, sinon M1). MG : M1 (profil DAMIR), pour tous
    les estimateurs de la cible (M2a et M3 n'ont pas de MG). Spécialistes : M0 (population). Niveau national des deux
    ramené à l'effectif libéral mesuré (NIVEAU_SOURCE, ameli 2025) à l'année de référence."""
    if src in SURVIVANTS:
        e = est if est in SURVIVANTS[src] else CENTRAL
        r = besoin_cache(src, e, None)
        return r["territories"], r["years"], np.asarray(r["besoin"][src]), e
    e = "M1" if src == "medecine-generale" else "M0"
    if (src, cible) not in _BSRC:
        E = _etats(cible)
        years = [y for y in sorted(E) if y >= V1.DECISION]
        B = discover()[e]().fit(_pop(), E, V1.DECISION).predict(_pop(), E, years)
        V = B.values[B.p(src)]
        f = NIVEAU_SOURCE[src] / V[:, list(B.years).index(V1.DECISION)].sum()        # niveau national mesuré à la référence
        _BSRC[(src, cible)] = ([str(t) for t in B.territories], [int(y) for y in B.years], V * f, e, f)
    return _BSRC[(src, cible)][:4]


def facteur_niveau(src: str, cible: str) -> float:
    """Rapport du niveau mesuré (NIVEAU_SOURCE) au niveau de l'estimateur seul ; 1 pour une des 5 professions."""
    return 1.0 if src in SURVIVANTS else _BSRC[(src, cible)][4]


def besoin_cache(prof: str, est: str, ov: dict | None) -> dict:
    """besoin_api sur les états de base ; ov = paramètres de L23 (None : sans transfert). L23 n'agit que sur les
    estimateurs qui portent la MG (source) et la profession (cible)."""
    ov = ov if prof == "pharmaciens" else None          # L23 : cible pharmaciens ; ailleurs, besoin inchangé
    key = (prof, est, None if ov is None else tuple(sorted(ov.items())))
    if key not in _BES:
        tr = (l23(V1.DECISION, **ov),) if ov is not None and prof == "pharmaciens" else ()
        _BES[key] = besoin_api(_etats(prof), _pop(), est, transferts=tr, ref=V1.DECISION)
    return _BES[key]


def _param_l23(p) -> dict:
    return dict(name=p.name, value=p.value, unit=p.unit, source=p.source, vintage=p.vintage, status=p.status)


def couverture_carte(prof: str, lv: dict, ov: dict | None, trh: tuple | None = None) -> dict:
    """Indice de couverture par département et pour la France, base et scénario, par estimateur survivant.
    trh = (Transfert, paramètres réglés) : transfert hypothétique de l'utilisateur·rice, appliqué après L23."""
    if prof in SANS_COUVERTURE or prof not in SURVIVANTS:
        raise ValueError(f"pas d'indice de couverture pour {prof!r} (O2 : sources de transferts seulement)")
    ck = (prof, tuple(sorted(lv.items())))
    car = _CAR.get(ck) or _CAR.setdefault(ck, carte(prof, lv))
    t0 = time.perf_counter()
    years, codes = car["years"], list(car["deps"])
    Sb = np.array([car["deps"][d]["b"] for d in codes])
    Ss = np.array([car["deps"][d]["s"] for d in codes])
    par = {}
    for est in SURVIVANTS[prof]:
        r0 = besoin_cache(prof, est, None)
        r1 = besoin_cache(prof, est, ov) if ov is not None else r0
        ti = {t: i for i, t in enumerate(r0["territories"])}
        yi = [r0["years"].index(y) for y in years]
        rows = [ti[d] for d in codes]
        B0 = np.asarray(r0["besoin"][prof])[rows][:, yi]
        B1 = np.asarray(r1["besoin"][prof])[rows][:, yi]
        src_info = None
        if trh is not None:                 # même opérateur que besoin.transferts.appliquer, sur les tableaux en cache
            tr = trh[0]
            sa = tr.s(years) * tr.a
            T, Y, Bs, e_src = besoin_source(tr.source, tr.cible, est)
            t2 = {t: i for i, t in enumerate(T)}
            Bsrc = Bs[[t2[d] for d in codes]][:, [Y.index(y) for y in years]]
            if prof == tr.cible:
                B1 = B1 + sa[None, :] * tr.k * (1 + tr.mu) * Bsrc
            else:
                B1 = B1 * (1 - sa[None, :])
            src_info = dict(estimateur=e_src, temps_source=(sa[None, :] * Bsrc).sum(0))
        with np.errstate(divide="ignore", invalid="ignore"):
            ref = Sb[:, 0] / B0[:, 0]
            Cb, Cs = (Sb / B0) / ref[:, None], (Ss / B1) / ref[:, None]
            nat = lambda S, B: (S.sum(0) / B.sum(0)) / (Sb[:, 0].sum() / B0[:, 0].sum())
            par[est] = dict(b=Cb, s=Cs, fb=nat(Sb, B0), fs=nat(Ss, B1), r1=r1, B0=B0, B1=B1, src=src_info)
    c = par[CENTRAL]
    lo = np.nanmin([p["s"] for p in par.values()], 0)
    hi = np.nanmax([p["s"] for p in par.values()], 0)
    flo = np.min([p["fs"] for p in par.values()], 0)
    fhi = np.max([p["fs"] for p in par.values()], 0)
    r4 = lambda a: [None if not np.isfinite(v) else round(float(v), 4) for v in a]
    deps = {d: {"cb": r4(c["b"][i]), "cs": r4(c["s"][i]), "ecart": r4(c["s"][i] / c["b"][i] - 1),
                "min": r4(lo[i]), "max": r4(hi[i])} for i, d in enumerate(codes)}
    # régions : rapport des sommes (C n'est pas additif), même formule que agrege()
    reg = V1.geo().region.to_dict()
    regs = {}
    for r in sorted({reg[d] for d in codes if d in reg}):
        ix = [i for i, d in enumerate(codes) if reg.get(d) == r]
        with np.errstate(divide="ignore", invalid="ignore"):
            C = {e: ((Sb[ix].sum(0) / p["B0"][ix].sum(0)), (Ss[ix].sum(0) / p["B1"][ix].sum(0)),
                     Sb[ix, 0].sum() / p["B0"][ix, 0].sum()) for e, p in par.items()}
            Cs_ = {e: v[1] / v[2] for e, v in C.items()}
            cb, cs = C[CENTRAL][0] / C[CENTRAL][2], Cs_[CENTRAL]
        regs["R" + r] = {"cb": r4(cb), "cs": r4(cs), "ecart": r4(cs / cb - 1),
                         "min": r4(np.min(list(Cs_.values()), 0)), "max": r4(np.max(list(Cs_.values()), 0))}
    with np.errstate(divide="ignore", invalid="ignore"):
        e50 = (hi[:, -1] - lo[:, -1]) / c["s"][:, -1]
    tr = [t | {"actes_mg_liberes": [round(INJ_MG_2018 * s) for s in l23(V1.DECISION, **(ov or {})).s(years)]}
          for t in c["r1"]["transferts"]] if ov is not None and prof == "pharmaciens" else []
    params = [_param_l23(p) for p in L23_PARAMS] + [dict(name="actes_mg_base", value=INJ_MG_2018, unit="injections / an",
              source="Cour des comptes, « La politique de vaccination depuis 2018 », G10.csv (fiche param-besoin-l23-vaccination)",
              vintage="2018", status="sourcé")]
    for p in params:
        if ov and p["name"] in ov:
            p |= {"value": ov[p["name"]], "status": "supposé", "source": "réglage expert de la carte"}
    return {"prof": prof, "ref": V1.DECISION, "years": years, "unite": f"indice, {V1.DECISION} = 1",
            "grandeur": c["r1"]["grandeur"], "central": CENTRAL, "estimateurs": list(par), "en_attente": EN_ATTENTE,
            "deps": deps, "regs": regs, "fr": {"cb": r4(c["fb"]), "cs": r4(c["fs"]), "ecart": r4(c["fs"] / c["fb"] - 1),
                                 "min": r4(flo), "max": r4(fhi)},
            "fourchette_visible": bool(np.nanmax(e50) > SEUIL_FOURCHETTE) if len(par) > 1 else False,
            "ecart_modeles_2050": round(float(np.nanmedian(e50)), 4) if len(par) > 1 else 0.0,
            "seuil_fourchette": SEUIL_FOURCHETTE,
            "l23": None if ov is None else {"actif": True, "params": params, "transferts": tr,
                                            "note": "a et k supposés : effet illustratif ; s(t) : forme mesurée (P-B6, depuis 2019) ; seule la part "
                                                    "au-delà de celle déjà atteinte en 2026 (≈ 0,70) agit"},
            "transfert_hypothetique": None if trh is None else _trh_bloc(trh, years, c["src"]),
            "hypotheses": {"norme": c["r1"]["norme"], "estimateurs": {e: besoin_cache(prof, e, None)["norme"] for e in par},
                           "population": c["r1"]["hypotheses"]["population"], "sources": [
                               "offre : jumeau v2, secteur privé (RPPS / Hippocrate, DREES)",
                               "besoin : v2/besoin (M1 poids APL DREES, DCIR ; M2a, M3 : fiches de l'axe 1)",
                               "population : Insee Omphale 2022"]},
            "ms": round((time.perf_counter() - t0) * 1000, 1)}


def _trh_bloc(trh: tuple, years: list, src: dict) -> dict:
    tr, regles = trh
    v = {"a": tr.a, "sinf": tr.s_inf, "k": tr.k, "tau": tr.tau, "t0": tr.t0}
    st = {"medecine-generale": "niveau mesuré : 56 005 médecins généralistes libéraux en France au 1er janvier 2025 "
                               "(ameli) ; répartition par âge mesurée (Open DAMIR 2025)",
          "specialistes": "niveau mesuré : 57 346 médecins spécialistes libéraux en France au 1er janvier 2025 "
                          "(ameli) ; répartition selon la population seule, sans effet de l'âge (supposé)"}
    return {"actif": True, "statut": "hypothèse de l'utilisateur", "source": tr.source, "cible": tr.cible,
            "params": [dict(name=k, value=v[k], unit=TR_UNITES[k], status="hypothèse de l'utilisateur" if k in regles
                            else "supposé (défaut, hypothèse de l'utilisateur)") for k in TR_DEFAUT],
            "besoin_source": {"estimateur": src["estimateur"], "statut": st.get(tr.source, "comme la profession source"),
                              "facteur_niveau": round(facteur_niveau(tr.source, tr.cible), 12)},
            "etp_source_transferes": [round(float(x), 1) for x in src["temps_source"]],
            "note": "transfert proposé par l'utilisateur·rice, pas un levier de la carte : ni le volume de l'acte ni la part "
                    "du temps de la source qu'il occupe ne sont publiés en données ouvertes ; effet illustratif"}


class Handler(V1.Handler):
    def __init__(self, *a, **k):
        super(V1.Handler, self).__init__(*a, directory=str(HERE), **k)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path in ("/geo", "/geo-regions"):
            b = geo_bytes() if u.path == "/geo" else regions_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "application/geo+json")
            self.send_header("Content-Encoding", "gzip")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            return self.wfile.write(b)
        if u.path == "/api/carte":
            q = {k: v[0] for k, v in parse_qs(u.query).items()}
            prof = q.get("prof", "kines")
            if prof not in V1.PROFS:
                return self.send_json({"error": f"profession inconnue {prof!r}"}, 400)
            lv, err = V1.parse_levers(q)          # mêmes leviers, mêmes bornes que /api/scenario
            if err:
                return self.send_json({"error": err}, 400)
            try:
                return self.send_json(carte(prof, lv, q.get("terr", "FR")))
            except Exception as e:
                return self.send_json({"error": f"{type(e).__name__}: {e}"}, 500)
        if u.path == "/api/couverture":
            q = {k: v[0] for k, v in parse_qs(u.query).items()}
            prof = q.get("prof", "pharmaciens")
            if prof in SANS_COUVERTURE:
                return self.send_json({"error": f"pas d'indice de couverture pour {prof!r} (sources de transferts seulement)"}, 400)
            if prof not in SURVIVANTS:      # profession inconnue : ne pas la confondre avec une source O2
                return self.send_json({"error": f"profession inconnue : {prof!r} (attendu : {', '.join(SURVIVANTS)})"}, 400)
            lv, err = V1.parse_levers(q)
            ov, err2 = _l23_params(q)
            trh, err3 = _tr_params(q, prof)
            if err or err2 or err3:
                return self.send_json({"error": err or err2 or err3}, 400)
            try:
                return self.send_json(couverture_carte(prof, lv, ov, trh))
            except Exception as e:
                return self.send_json({"error": f"{type(e).__name__}: {e}"}, 500)
        if u.path == "/api/interpret":     # texte -> leviers ; traduit, ne calcule rien (v2/langage/README.md)
            q = {k: v[0] for k, v in parse_qs(u.query).items()}
            texte = q.get("q", "").strip()[:500]
            if not texte:
                return self.send_json({"error": "texte vide"}, 400)
            try:
                return self.send_json(NL.compile(texte, q.get("prof"), q.get("terr")))
            except Exception as e:
                return self.send_json({"error": f"{type(e).__name__}: {e}"}, 500)
        if u.path == "/api/agent/etat":
            code, j = _chatbot("GET", "/api/etat")
            if code != 200:
                return self.send_json({"disponible": False, "message": "Assistant non lancé (chatbot/, port 8768) : "
                                       "la carte reste utilisable. Voir le README, « Chatbot ».", "modele": MODELE})
            mode = "IA (" + j.get("modele", "?") + ")" if j.get("mode") == "llm" else "sans IA (glossaire de l'équipe)"
            return self.send_json({"disponible": True, "mode": j.get("mode"), "message": f"Assistant prêt, mode {mode}.",
                                   "modele": MODELE})
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/agent":
            return self.send_json({"error": "inconnu"}, 404)
        n = int(self.headers.get("Content-Length") or 0)
        if not 0 < n <= 65536:
            return self.send_json({"error": "requête vide ou trop longue"}, 400)
        try:
            body = json.loads(self.rfile.read(n))
            q = str(body.get("question", "")).strip()[:1000]
        except (ValueError, AttributeError):
            return self.send_json({"error": "JSON invalide"}, 400)
        if not q:
            return self.send_json({"error": "question vide"}, 400)
        ctx = body.get("contexte") or {}
        sid = str(body.get("session") or "carte")[:64]
        msg = q
        if ctx.get("prof"):        # contexte de la carte : rattache « et si… » à ce qui est affiché ; mode IA seulement
            lv = ", ".join(f"{k}={v}" for k, v in (ctx.get("leviers") or {}).items()) or "aucun (tendanciel)"
            msg = (f"{q}\n\n[Contexte de la carte, pas une question : profession {ctx['prof']} ; territoire "
                   f"{ctx.get('territoire') or ctx.get('terr')} ; leviers modifiés : {lv} ; année affichée "
                   f"{ctx.get('annee') or 2050} ; densités exprimées pour 100 000 habitants.]")
        code, j = _chatbot("GET", "/api/etat")
        if code == 200 and j.get("mode") != "llm":
            msg = q                # le glossaire lit la phrase seule ; il garde profession et territoire d'un tour à l'autre
        code, r = _chatbot("POST", "/api/chat", {"session": sid, "message": msg})
        if code != 200 or "erreur" in r:
            return self.send_json({"error": r.get("erreur") or "Chatbot non lancé (port 8768)."}, 503)
        lx = _lexique(r.get("texte", ""))
        return self.send_json({"reponse": r.get("texte", ""), "mode": r.get("mode"), "verification": r.get("verification"),
                               "carte": _scenario_carte(r.get("appels", [])), "objectif": _objectif(r.get("appels", [])),
                               "graphiques": (r.get("graphiques") or [])[:2],   # construits par le chatbot à partir des résultats
                               "lexique": lx, "appels": [{"outil": a["outil"], "resume": a.get("resume"), "entree": a.get("entree")} for a in r.get("appels", [])],
                               "secondes": r.get("duree_s")})


CHATBOT = os.environ.get("CHATBOT_URL", "http://127.0.0.1:8768")

# Modèle servi par la carte (V1.Model : C1 par défaut, A0 par JUMEAU_MODELE=A0) : affiché sous chaque réponse de l'assistant.
# Même texte que MODELE dans chatbot/passerelle/requetes.py (périmètre du chatbot) ; chiffres cités des articles.
MODELES = {
    "C1": {
        "nom": "Modèle bayésien hiérarchique (cohortes, entrées comprises ; C1, axe 2)",
        "equation": "N(t+1) = rétention × vieillissement de N(t) + entrées, par profession × département × sexe × tranche d'âge de 5 ans ; rétention nette en âge-période-cohorte, entrées = niveau national (filtre de Kalman) × parts départementales",
        "estimation": "Bayes empirique, moyenne a posteriori ; fenêtre de 2012 (kinés 2017) à la dernière année ; effets département et région rétrécis ; secteur privé seulement, le salariat public garde les taux de A0",
        "leviers": "événements datés du jumeau (modules entrées, sorties, diplômés étrangers, régulation) appliqués aux taux de C1, au même état de départ ; état à 2 secteurs (libéral = privé, salarié)",
        "precision": "MAPE 7,73 % par département à 5 ans, secteur privé, contre 8,68 % pour le modèle stock-flux multi-échelle (A0) et 9,30 % pour la tendance linéaire (mesuré, article axe 2) ; gain plus faible sur les origines récentes (dentistes, pharmaciens)",
        "fourchette": "± pente de l'erreur nationale de C1 au banc × horizon × 1,6, environ 8 cas sur 10 (même méthode que A0) ; extrapolée au-delà d'environ 10 ans ; la bande probabiliste propre de C1 n'est calibrée qu'au département (77,6 %) et n'est pas publiée au national",
        "approximation": "rétention de C1 tenue à sa moyenne sur l'horizon : écart de −1,1 à +1,2 % sur le total privé national à 5 ans (mesuré) ; infirmiers : C1 mesuré au banc sur les libéraux, la carte sert la table privée de l'axe 4",
        "alternative": "Modèle stock-flux multi-échelle (A0, MAPE 8,68 %) : servi si JUMEAU_MODELE=A0",
        "sources": "v2/papers/axe2-methodes/main.pdf ; v2/methodes/cohortes.py ; v2/methodes/c1_jumeau.py ; v2/jumeau/ ; v2/prototype/server.py (Model)",
    },
    "A0": {
        "nom": "Modèle stock-flux multi-échelle (taux départementaux rétrécis vers le national ; A0, axe 2)",
        "equation": "N(t+1) = rétention × vieillissement de N(t) + entrées, par profession × département × sexe × tranche d'âge de 5 ans",
        "estimation": "rétention nette et entrées ajustées sur les 5 dernières années observées ; taux départementaux rétrécis vers le national (poids 200 personnes, supposé)",
        "leviers": "événements datés du jumeau (modules entrées, sorties, diplômés étrangers, régulation) appliqués au même état de départ ; état à 2 secteurs (libéral = privé, salarié)",
        "precision": "MAPE 8,68 % par département à 5 ans, secteur privé, contre 9,30 % pour la tendance linéaire (mesuré, article axe 2, tableau 1)",
        "fourchette": "± pente de l'erreur de backtest × horizon × 1,6, environ 8 cas sur 10 (facteur cité, non reproduit ; article axe 5) ; extrapolée au-delà d'environ 10 ans",
        "alternative": "Modèle bayésien hiérarchique (C1, MAPE 7,73 % au même banc) : servi par défaut (JUMEAU_MODELE=C1)",
        "sources": "v2/papers/axe2-methodes/main.pdf ; v2/sante/estimators.py (StockFlowLocal) ; v2/jumeau/ ; v2/prototype/server.py (Model)",
    },
}
# Modèle servi : même variable que v2/prototype/server.py (MODELE_CHOIX), C1 par défaut.
MODELE = MODELES[os.environ.get("JUMEAU_MODELE", "C1").upper()]


def _objectif(appels: list) -> dict | None:
    """Question d'objectif : ce que l'assistant a compris (cible, horizon, territoire, référence), lu dans l'appel planifier."""
    for a in reversed(appels):
        e = a.get("entree") or {}
        if a.get("outil") in ("planifier", "atteindre") and not a.get("erreur") and e.get("profession") in V1.PROFS:
            t = a.get("code_territoire") or e.get("territoire")
            return {"prof": e["profession"], "terr": t if isinstance(t, str) and re.fullmatch(r"FR|R\d\d|D[0-9AB]{2,3}", t) else "FR", "annee": e.get("annee"),
                    "grandeur": e.get("grandeur", "effectif"), "hausse_pct": e.get("hausse_pct"),
                    "valeur_cible": e.get("valeur_cible"), "reference": e.get("reference", "tendanciel"),
                    "exclus": e.get("leviers_exclus") or []}
    return None


def _scenario_carte(appels: list) -> dict | None:
    """Scénario simulé par le chatbot, au format de la carte (profession, territoire, leviers, année) : le panneau propose
    de l'afficher, rien n'est appliqué sans clic. Parmi les calculs réussis, on préfère ceux qui ont des leviers, puis
    un territoire plus fin que la France (les appels « France » servent souvent de référence), puis le dernier."""
    cands = []
    trh_i = [i for i, a in enumerate(appels) if a.get("outil") == "couverture" and (a.get("entree") or {}).get("transfert")
             and not a.get("erreur")]
    trh_mid = trh_i[len(trh_i) // 2] if trh_i else None
    for i, a in enumerate(appels):
        e = a.get("entree") or {}
        if e.get("transfert") and a.get("outil") == "couverture" and i != trh_mid:
            continue       # transfert hypothétique balayé : la carte reçoit le point médian du balayage
        if a.get("erreur") or a.get("outil") not in ("projeter", "comparer", "balayer", "planifier", "traduire_politique", "couverture") or not a.get("code_territoire"):
            continue
        lv = dict(e.get("leviers") or {})
        if a["outil"] in ("planifier", "traduire_politique"):      # premier mélange vérifié / essai d'ampleur basse
            lv = dict(a.get("reglage_carte") or {})
        if a["outil"] == "comparer":       # le dernier scénario comparé
            sc = e.get("scenarios") or []
            lv = dict((sc[-1] or {}).get("leviers") or {}) if sc else {}
        if a["outil"] == "balayer":
            lv = dict(e.get("autres_leviers") or {})
        ans = e.get("annees") or ([e["annee"]] if e.get("annee") else [])
        if e.get("profession") not in V1.PROFS:
            continue
        c = {"prof": e["profession"], "terr": a["code_territoire"], "leviers": lv, "annee": max(ans) if ans else 2050}
        if a["outil"] == "couverture":     # étape 5 du plan besoin-carte : L23 vu par l'assistant -> vue couverture, l23=1
            c |= {"vue": "couverture", "l23": 1 if e.get("l23") else 0}
            if e.get("transfert"):        # bandeau « transfert hypothétique » de la carte ; paramètres tr_* de /api/couverture
                t = e["transfert"]
                c["tr"] = {"p": {TR_Q[k]: v for k, v in t.items()}, "libelle": _trh_libelle(t),
                           "resume": _trh_resume(t)}
        cands.append(((bool(lv) or bool(c.get("l23")) or "tr" in c, a["outil"] == "couverture", c["terr"] != "FR", i), c))
    return max(cands, key=lambda x: x[0])[1] if cands else None


TR_Q = {"source": "tr_src", "cible": "tr_cible", "a": "tr_a", "s_inf": "tr_sinf", "k": "tr_k", "tau": "tr_tau", "t0": "tr_t0"}
NOMS_SOURCES = {"medecine-generale": "médecins généralistes", "specialistes": "médecins spécialistes"}


def _trh_libelle(t: dict) -> str:
    nom = lambda p: NOMS_SOURCES.get(p) or V1.PROFS.get(p, p).lower()
    return f"une part de la demande des {nom(t['source'])} passe aux {nom(t['cible'])}"


def _trh_resume(t: dict) -> str:
    """Réglage du transfert hypothétique en langue courante (point médian du balayage de a)."""
    pc = lambda x: f"{100 * x:.3g} %".replace(".", ",")
    out = [f"part de la demande concernée {pc(t.get('a', TR_DEFAUT['a']))} (point médian du balayage"
           + (")" if "a" in t else ", supposée)")]
    out += [f"part de l'acte transférée {pc(t['s_inf'])}"] if "s_inf" in t else []
    out += [f"à partir de {t['t0']}"] if "t0" in t else []
    return ", ".join(out)


def _chatbot(methode: str, chemin: str, corps: dict | None = None) -> tuple[int, dict]:
    """Relais vers le chatbot de chatbot/ (moteur unique, décision du 2026-11-14) ; la clé reste dans son processus."""
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen
    data = json.dumps(corps).encode() if corps is not None else None
    req = Request(CHATBOT + chemin, data=data, method=methode, headers={"Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=120) as r:
            return r.status, json.load(r)
    except HTTPError as e:
        try:
            return e.code, json.load(e)
        except ValueError:
            return e.code, {}
    except (URLError, OSError):
        return 0, {}


_LX = None


def _lexique(texte: str) -> dict:
    """Contrôle du lexique neutre (v2/agent/garde_fous.py) appliqué à la réponse du chatbot."""
    global _LX
    if _LX is None:
        sp = importlib.util.spec_from_file_location("garde_fous", HERE.parent / "agent" / "garde_fous.py")
        _LX = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(_LX)
    return _LX.lexique(texte)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8767
    os.environ.setdefault("AGENT_CARTE_URL", f"http://127.0.0.1:{port}")   # l'agent interroge ce serveur-ci
    t0 = time.perf_counter()
    geo_bytes()
    regions_bytes()
    for p in V1.PROFS:
        V1.model(p)
        print(f"{p}: origine {V1.MODELS[p].o} ({time.perf_counter() - t0:.1f} s)", flush=True)
    for p in SURVIVANTS:       # besoin précalculé (ne dépend pas des leviers d'offre) : la vue couverture répond à chaud
        for e in SURVIVANTS[p]:
            besoin_cache(p, e, None)
        if p == "pharmaciens":
            besoin_cache(p, CENTRAL, {})
    print(f"besoin : {len(_BES)} estimations en cache ({time.perf_counter() - t0:.1f} s)", flush=True)
    print(f"prêt : http://localhost:{port}", flush=True)
    V1.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
