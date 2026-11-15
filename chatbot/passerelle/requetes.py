"""Requêtes en LECTURE SEULE sur le jumeau numérique (dépôt hackathon_acces_soins, épinglé en sous-module).

C'est le SEUL module du dépôt qui importe le code du modèle. Il ne fait qu'appeler `Model.answer` et lire des
fichiers de résultats ; il n'écrit rien, n'exécute rien d'autre, et n'expose ni chemin ni attribut arbitraire.
Le processus du chatbot n'importe jamais ce module : il passe par passerelle/server.py (HTTP, GET seulement).

Chemin du modèle : variable JUMEAU_REPO (défaut : vendor/hackathon_acces_soins).
"""
from __future__ import annotations

import csv
import importlib.util
import json
import os
import subprocess
import sys
import time
from functools import lru_cache
from pathlib import Path

import numpy as np

REPO = Path(os.environ.get("JUMEAU_REPO", Path(__file__).resolve().parents[1] / "vendor" / "hackathon_acces_soins")).resolve()
V2 = REPO / "v2"


def version_modele() -> dict:
    """Commit du modèle et état « modifié / propre » : chaque réponse est rattachée à une version exacte."""
    try:
        sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True, timeout=5).stdout.strip()
        sale = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=REPO, capture_output=True,
                              text=True, timeout=5).stdout.strip()
    except Exception:
        sha, sale = "", ""
    return {"commit": sha[:12] or "?", "code_modifie_localement": bool(sale), "chemin": str(REPO.name)}


@lru_cache(maxsize=1)
def S():
    """Serveur du prototype V1 importé sans le lancer (fait le chdir vers la racine du dépôt)."""
    spec = importlib.util.spec_from_file_location("proto_v1", V2 / "prototype" / "server.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Compilateur : celui du dépôt qui contient chatbot/ quand il existe (le glossaire évolue plus vite que la copie du modèle :
# transferts de tâches L23 du 2026-11-15), sinon celui de la copie épinglée. LANGAGE_DIR force un dossier.
_LIVE = Path(__file__).resolve().parents[2] / "v2" / "langage"
LANGAGE = Path(os.environ.get("LANGAGE_DIR") or (_LIVE if (_LIVE / "compilateur.py").exists() else V2 / "langage")).resolve()


@lru_cache(maxsize=1)
def NL():
    """Compilateur déterministe de v2/langage, branché sur le même module serveur (pas de second jumeau)."""
    spec = importlib.util.spec_from_file_location("compilateur", LANGAGE / "compilateur.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.serveur = S
    return mod


@lru_cache(maxsize=1)
def PH():
    sys.modules.setdefault("compilateur", NL())   # phrases.py fait « from compilateur import serveur » : même instance
    spec = importlib.util.spec_from_file_location("phrases", LANGAGE / "phrases.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ErreurOutil(ValueError):
    """Erreur renvoyée au modèle de langage (tool_result is_error) pour qu'il corrige son appel."""


# ------------------------------------------------------------------ résolution des entrées

def profession(p: str) -> str:
    srv = S()
    if p in srv.PROFS:
        return p
    found = NL().detecter_profession(NL().norm(p))
    if found:
        return found[0]
    raise ErreurOutil(f"profession inconnue {p!r} ; valeurs : {', '.join(srv.PROFS)} "
                      "(la médecine générale et les spécialistes sont hors périmètre de la phase 1)")


def territoire(t: str | None) -> str:
    """Code serveur (FR, R84, D63) à partir d'un code ou d'un nom (région, département, ville du glossaire, sigle)."""
    srv = S()
    t = (t or "FR").strip()
    g = srv.geo()
    if t == "FR" or (t[:1] == "R" and t[1:] in srv.REGIONS) or (t[:1] == "D" and t[1:] in g.index):
        return t
    if t in g.index:                       # « 63 »
        return "D" + t
    n = NL().norm(t)
    for forme, code, _ in NL()._territoires():
        if forme == n:
            return code
    found, _ = NL().detecter_territoire(n)
    if found:
        return found[0][1]
    cand = [nom for nom in list(srv.REGIONS.values()) + list(g.dep_name) if n[:4] in NL().norm(str(nom))][:6]
    raise ErreurOutil(f"territoire non reconnu {t!r}" + (f" ; voulez-vous dire : {', '.join(cand)} ?" if cand else
                      " ; donner une région, un département (nom ou numéro) ou « France »"))


def nom_territoire(code: str) -> str:
    srv = S()
    if code == "FR":
        return "France"
    if code.startswith("R"):
        return srv.REGIONS.get(code[1:], code)
    return str(srv.geo().loc[code[1:], "dep_name"])


def leviers(lv: dict | None) -> dict:
    """Réglage validé par parse_levers (mêmes bornes que l'écran de décision) ; erreur explicite sinon."""
    srv = S()
    lv = lv or {}
    inconnus = set(lv) - set(srv.UI)
    if inconnus:
        raise ErreurOutil(f"leviers inconnus : {sorted(inconnus)} ; leviers disponibles : {sorted(srv.UI)}")
    q = {k: ("1" if v is True else "0" if v is False else str(v)) for k, v in lv.items()}
    out, err = srv.parse_levers(q)
    if err:
        raise ErreurOutil(err)
    return out


def _fmt_levier(k: str, v) -> str:
    l = S().UI[k]
    if l["type"] == "toggle":
        return f"{l['label']} : {'oui' if v else 'non'}"
    if l["type"] == "select":
        return f"{l['label']} : {l['options'][v]}"
    f = l.get("fmt")
    s = {"pct": f"{(v - 1) * 100:+.0f} %", "pct0": f"{v * 100:.0f} %", "x": f"× {v:g}", "ans": f"+{v:g} an" + ("s" if v >= 2 else "")}.get(f, f"{v:g}")
    s = s.replace(".", ",")                    # décimales à la française
    return f"{l['label']} : {s}"


def resume_leviers(lv: dict) -> list[str]:
    d = {l["k"]: l["default"] for l in S().LEVIERS_UI}
    return [_fmt_levier(k, v) for k, v in lv.items() if v != d[k] and not (isinstance(d[k], int) and bool(v) == bool(d[k]) and S().UI[k]["type"] == "toggle")]


# ------------------------------------------------------------------ calcul (toujours le jumeau)

_CACHE: dict = {}


def _answer(prof: str, lv: dict, terr: str) -> dict:
    key = (prof, terr, json.dumps(lv, sort_keys=True))
    if key not in _CACHE:
        _CACHE[key] = S().model(prof).answer(lv, terr)
        if len(_CACHE) > 256:
            _CACHE.pop(next(iter(_CACHE)))
    return _CACHE[key]


def _annees(annees, r) -> list[int]:
    ys = sorted({int(a) for a in (annees or [2030, 2035, 2040, 2050])})
    bad = [a for a in ys if a < r["origin"] or a > S().H]
    if bad:
        raise ErreurOutil(f"années hors de la projection [{r['origin']} ; {S().H}] : {bad}")
    return ys


# ------------------------------------------------------------------ vocabulaire des grandeurs (v2/docs/lab/lexicon.md)
# Un mot par plage, calculé ici et jamais par le modèle de langage ; seuils supposés, à changer avec lexicon.md.

def q_variation(pct: float | None) -> str | None:
    if pct is None:
        return None
    a, sens = abs(pct), ("hausse" if pct > 0 else "baisse")
    if a < 1:
        return "stable"
    return f"légère {sens}" if a < 5 else f"{sens} marquée" if a < 15 else f"forte {sens}"


def q_densite(pct: float | None) -> str | None:
    if pct is None:
        return None
    if pct < -25:
        return "nettement inférieure à la moyenne nationale"
    if pct < -10:
        return "inférieure à la moyenne nationale"
    if pct <= 10:
        return "proche de la moyenne nationale"
    return "supérieure à la moyenne nationale" if pct <= 25 else "nettement supérieure à la moyenne nationale"


def q_incertitude(demi_pct: float, horizon: int) -> str:
    m = "incertitude faible" if demi_pct < 5 else "incertitude modérée" if demi_pct <= 15 else "incertitude élevée"
    return m + (" (extrapolée)" if horizon > 10 else "")


def q_delai(ans: int) -> str:
    return "court terme" if ans < 3 else "moyen terme" if ans <= 6 else "long terme"


def _ligne(r: dict, y: int, dens_fr: float | None = None) -> dict:
    i = r["years"].index(y)
    v, lo, hi = PH().fourchette(r, y)
    b = r["base"][i]
    ecart_pct = round((r["scn"][i] / b - 1) * 100, 2) if b else None
    evo = round((r["scn"][i] / r["scn"][0] - 1) * 100, 1) if r["scn"][0] else None
    demi = round((hi - lo) / 2 / v * 100, 1) if v else 0.0
    q = {"evolution_depuis_origine": q_variation(evo), "ecart_au_tendanciel": q_variation(ecart_pct),
         "incertitude": q_incertitude(demi, y - r["origin"])}
    out = {"annee": y, "tendanciel": round(b), "scenario": round(r["scn"][i]),
           "ecart": round(r["scn"][i] - b), "ecart_pct": ecart_pct, "evolution_pct_depuis_origine": evo,
           "fourchette_scenario": [round(lo), round(hi)], "fourchette_demi_largeur_pct": demi,
           "densite_100k_tendanciel": _r1(r["dens_base"][i]), "densite_100k_scenario": _r1(r["dens_scn"][i]),
           "ecart_densite_100k": _r1(r["dens_scn"][i] - r["dens_base"][i]) if r["dens_scn"][i] and r["dens_base"][i] else None,
           "population": round(r["pop"][i]) if r["pop"][i] == r["pop"][i] else None}
    d = r["dens_scn"][i]
    if dens_fr and d and d == d:
        out["densite_100k_france_scenario"] = _r1(dens_fr)
        out["densite_ecart_a_la_france_pct"] = round((d / dens_fr - 1) * 100, 1)
        q["densite"] = q_densite(out["densite_ecart_a_la_france_pct"])
    out["qualificatifs"] = q
    return out


def _dens_fr(p: str, lv: dict, y: int) -> float | None:
    """Densité France au même réglage ; une hausse des places limitée à une région n'a pas de sens au niveau national :
    la référence nationale est alors calculée sans elle."""
    if lv.get("quotas_region"):
        lv = {**lv, "quotas_region": False, "quotas": 1.0}
    r = _answer(p, lv, "FR")
    x = r["dens_scn"][r["years"].index(y)]
    return x if x and x == x else None


def _r1(x):
    return None if x is None or x != x else round(x, 1)


_DELAI_ANS = {"etrangers": 2}   # « moyen : 1 à 3 ans » (LEVIERS_UI) ; quotas : durée des études + 1 ; autres : « rapide », 1 an


def _provenance(lv: dict, p: str | None = None) -> list[dict]:
    meta = {m["k"]: m for m in S().lever_meta()}
    d = {l["k"]: l["default"] for l in S().LEVIERS_UI}
    out = []
    for k, v in lv.items():
        if v == d[k]:
            continue
        ans = S().LAG[p] + 1 if k == "quotas" and p else _DELAI_ANS.get(k, 1)
        x = {"levier": k, "reglage": _fmt_levier(k, v), "statut": meta[k]["status"], "source": meta[k]["source"],
             "delai": meta[k]["delai"], "delai_ans": ans, "delai_qualificatif": q_delai(ans)}
        if k == "retraite" and v:      # montée de 3 mois par an (LEVIERS_UI) : le report complet est atteint après v / 0,25 ans
            x["effet_complet_apres_ans"] = int(round(v / 0.25))
        out.append(x)
    return out


PERIMETRE = ("Effectif « libéral » = secteur privé (lucratif ou non), tout employeur public exclu. Grain : département. "
             "Projection sous hypothèses, pas une prévision ; aucun backtest au-delà d'environ 10 ans.")


def projeter(profession_: str, territoire_: str = "FR", leviers_: dict | None = None, annees: list[int] | None = None) -> dict:
    p, t, lv = profession(profession_), territoire(territoire_), leviers(leviers_)
    t0 = time.perf_counter()
    r = _answer(p, lv, t)
    ys = _annees(annees, r)
    flux = {f: round(v[r["years"].index(ys[-1])]) for f, v in r["flows"].items()}
    extra = {}
    if lv["regul"]:
        g, zs = S().geo(), r["regul_deps"]
        deps = [t[1:]] if t.startswith("D") else list(g.index[g.region == t[1:]]) if t.startswith("R") else list(g.index)
        n = int(round(lv["part_zones"] * len(zs)))
        extra["regulation"] = {"departements_regules_dans_territoire": [str(g.loc[d, "dep_name"]) for d in zs[:n] if d in deps],
                               "regle": "un département est régulé si ≥ 50 % de ses communes sont en « remplacement seul » "
                                        "(zonage actuel) ; ailleurs la régulation est sans effet au grain départemental"}
    return {
        "profession": r["label"], "territoire": nom_territoire(t), "code_territoire": t,
        "origine": r["origin"], "observe_origine": round(r["base"][0]),
        "leviers": resume_leviers(lv) or ["aucun levier : scénario tendanciel"],
        "premier_effet": r["first_effect"] if lv["quotas"] != 1 else None,
        "annees": [_ligne(r, y, _dens_fr(p, lv, y)) for y in ys],
        f"ecart_par_flux_cumule_{ys[-1]}": flux,
        "provenance_leviers": _provenance(lv, p), **extra,
        **({"melange_de_politiques": m} if (m := _contributions(p, t, lv, ys[-1])) else {}),
        "fourchette_methode": f"scénario × (1 ± {r['k']:.4f} × années depuis {r['origin']}) : erreur de backtest extrapolée, ~8 cas sur 10",
        "perimetre": PERIMETRE, "calcul_ms": round((time.perf_counter() - t0) * 1000, 1),
        "_serie": {"annees": r["years"], "tendanciel": r["base"], "scenario": r["scn"], "k": r["k"],
                   "origine": r["origin"], "observe": r["obs"]},
    }


# Un levier de politique = un groupe de réglages (la hausse des places et sa restriction régionale vont ensemble).
_GROUPES = {"quotas": ("quotas", "quotas_region"), "etrangers": ("etrangers",), "regul": ("regul", "part_zones", "dest"),
            "retraite": ("retraite",), "cumul": ("cumul",), "precoces": ("precoces",)}


def _contributions(p: str, t: str, lv: dict, y: int) -> dict | None:
    """Mélange de politiques : effet de chaque levier seul, effet combiné, et interaction (combiné − somme des seuls).
    Tout est calculé par le jumeau, sur le même état de départ ; rien n'est additionné à la main."""
    d = {l["k"]: l["default"] for l in S().LEVIERS_UI}
    ctx = {k: lv[k] for k in ("pop_scen", "activite")}
    actifs = [g for g, ks in _GROUPES.items() if any(lv[k] != d[k] for k in ks) and lv[ks[0]] != d[ks[0]]]
    if len(actifs) < 2:
        return None
    base = _answer(p, leviers(ctx), t)
    i = base["years"].index(y)
    b = base["base"][i]
    tout = _answer(p, lv, t)["scn"][i] - b
    out, somme = [], 0.0
    for g in actifs:
        seul = leviers({**ctx, **{k: lv[k] for k in _GROUPES[g]}})
        e = _answer(p, seul, t)["scn"][i] - b
        somme += e
        out.append({"levier": "; ".join(resume_leviers(seul)), "ecart_seul": round(e),
                    "ecart_seul_pct": round(e / b * 100, 2) if b else None,
                    "qualificatif": q_variation(e / b * 100 if b else None),
                    "part_de_l_ecart_combine_pct": round(e / tout * 100, 1) if abs(tout) > 0.5 else None})
    out.sort(key=lambda x: -abs(x["ecart_seul"]))
    return {"annee": y, "leviers": out, "ecart_combine": round(tout), "somme_des_effets_seuls": round(somme),
            "interaction": round(tout - somme),
            "lecture": "écart au tendanciel de chaque levier seul, puis de tous ensemble ; l'interaction est la différence "
                       "entre l'effet combiné et la somme des effets seuls (la régulation, par exemple, peut absorber des entrées "
                       "supplémentaires)"}


# Réglages de référence pour comparer les leviers entre eux (supposés : des ordres de grandeur, pas des recommandations).
_REFERENCE = {"quotas": {"quotas": 1.2}, "etrangers": {"etrangers": 1.5}, "retraite": {"retraite": 2.0},
              "cumul": {"cumul": 1.5}, "precoces": {"precoces": 0.7}, "regul": {"regul": True}}


def effets_des_leviers(profession_: str, territoire_: str = "FR", annee: int = 2040) -> dict:
    """Chaque levier seul, à un réglage de référence, puis tous ensemble : écart au tendanciel à l'année demandée."""
    p, t = profession(profession_), territoire(territoire_)
    base = _answer(p, leviers({}), t)
    y = _annees([annee], base)[0]
    i = base["years"].index(y)
    b = base["base"][i]
    meta = {m["k"]: m for m in S().lever_meta()}
    rows = []
    for k, reg in _REFERENCE.items():
        lv = leviers(reg)
        r = _answer(p, lv, t)
        e = r["scn"][i] - b
        ans = S().LAG[p] + 1 if k == "quotas" else _DELAI_ANS.get(k, 1)
        rows.append({"levier": "; ".join(resume_leviers(lv)), "ecart": round(e), "ecart_pct": round(e / b * 100, 2) if b else None,
                     "qualificatif": q_variation(e / b * 100 if b else None), "delai_qualificatif": q_delai(ans),
                     "statut": meta[k]["status"], "source": meta[k]["source"]})
    rows.sort(key=lambda x: -abs(x["ecart"]))
    tous = leviers({k: v for reg in _REFERENCE.values() for k, v in reg.items()})
    e = _answer(p, tous, t)["scn"][i] - b
    return {"profession": S().PROFS[p], "territoire": nom_territoire(t), "code_territoire": t, "annee": y,
            "tendanciel": round(b), "leviers_seuls": rows,
            "tous_ensemble": {"ecart": round(e), "ecart_pct": round(e / b * 100, 2) if b else None,
                              "qualificatif": q_variation(e / b * 100 if b else None)},
            "methode": "réglages de référence supposés (ordres de grandeur dans les bornes, pas des recommandations) ; "
                       "classement par écart projeté au tendanciel ; le choix revient au décideur",
            "perimetre": PERIMETRE}


def comparer(profession_: str, territoire_: str, scenarios: list[dict], annee: int = 2050) -> dict:
    if not scenarios or len(scenarios) > 6:
        raise ErreurOutil("donner de 1 à 6 scénarios")
    p, t = profession(profession_), territoire(territoire_)
    rows, series = [], []
    for s in scenarios:
        lv = leviers(s.get("leviers"))
        r = _answer(p, lv, t)
        ys = _annees([annee], r)
        rows.append({"nom": s.get("nom") or ", ".join(resume_leviers(lv)) or "tendanciel",
                     "leviers": resume_leviers(lv), **_ligne(r, ys[0], _dens_fr(p, lv, ys[0]))})
        series.append({"nom": rows[-1]["nom"], "annees": r["years"], "valeurs": r["scn"]})
    prov = {x["levier"]: x for sc in scenarios for x in _provenance(leviers(sc.get("leviers")), p)}
    return {"profession": S().PROFS[p], "territoire": nom_territoire(t), "code_territoire": t, "annee": annee, "scenarios": rows,
            "provenance_leviers": list(prov.values()), "perimetre": PERIMETRE, "_series": {"tendanciel": {"annees": r["years"], "valeurs": r["base"]}, "scenarios": series}}


def balayer(profession_: str, territoire_: str, levier: str, valeurs: list, annee: int = 2050,
            autres_leviers: dict | None = None) -> dict:
    p, t = profession(profession_), territoire(territoire_)
    if levier not in S().UI or S().UI[levier]["type"] not in ("range", "toggle", "select"):
        raise ErreurOutil(f"levier inconnu {levier!r}")
    if not valeurs or len(valeurs) > 9:
        raise ErreurOutil("donner de 1 à 9 valeurs")
    out = []
    for v in valeurs:
        lv = leviers({**(autres_leviers or {}), levier: v})
        r = _answer(p, lv, t)
        y = _annees([annee], r)[0]
        out.append({"valeur": v, "reglage": _fmt_levier(levier, lv[levier]), **_ligne(r, y, _dens_fr(p, lv, y))})
    return {"profession": S().PROFS[p], "territoire": nom_territoire(t), "levier": S().UI[levier]["label"],
            "annee": annee, "points": out, "perimetre": PERIMETRE}


def classer(profession_: str, region: str | None = None, leviers_: dict | None = None, annee: int = 2050,
            critere: str = "densite_100k_scenario", n: int = 10, ordre: str = "croissant") -> dict:
    """Départements d'une région (ou de France) classés ; densités Insee Omphale (scénario choisi)."""
    srv, p, lv = S(), profession(profession_), leviers(leviers_)
    g = srv.geo()
    terr = territoire(region) if region else "FR"
    if terr.startswith("D"):
        terr = "R" + g.loc[terr[1:], "region"]
    deps = list(g.index) if terr == "FR" else list(g.index[g.region == terr[1:]])
    rows = []
    dfr = _dens_fr(p, lv, annee)
    for d in deps:
        try:
            r = _answer(p, lv, "D" + d)
        except Exception:
            continue
        if annee not in r["years"]:
            raise ErreurOutil(f"année hors projection : {annee}")
        x = _ligne(r, annee, dfr)
        rows.append({"departement": str(g.loc[d, "dep_name"]), "code": d, **x})
    if critere not in ("densite_100k_scenario", "ecart_pct", "evolution_pct_depuis_origine", "scenario"):
        raise ErreurOutil("critère : densite_100k_scenario, ecart_pct, evolution_pct_depuis_origine ou scenario")
    rows = [r for r in rows if r.get(critere) is not None]
    rows.sort(key=lambda r: r[critere], reverse=(ordre == "decroissant"))
    return {"profession": srv.PROFS[p], "perimetre_classement": nom_territoire(terr), "annee": annee, "critere": critere,
            "leviers": resume_leviers(lv) or ["tendanciel"], "nb_departements": len(rows), "departements": rows[:max(1, min(n, 30))],
            "moyenne_simple_des_departements_densite": _r1(float(np.mean([r["densite_100k_scenario"] for r in rows if r["densite_100k_scenario"]]))) if rows else None,
            "densite_100k_france_scenario": _r1(dfr),
            "perimetre": PERIMETRE}


def decrire_leviers() -> dict:  # noqa: D103
    G = NL().glossaire()
    return {"leviers": [{k: m.get(k) for k in ("k", "famille", "label", "type", "min", "max", "step", "default", "options",
                                                 "delai", "status", "source", "unit")} for m in S().lever_meta()],
            "non_modelise": [{"id": k, "libelle": v["libelle"], "raison": v["raison"]} for k, v in G["non_modelises"].items()],
            "professions": S().PROFS, "delai_formation_ans": S().LAG, "annee_decision": S().DECISION, "horizon": S().H}


@lru_cache(maxsize=1)
def _classement():
    f = V2 / "sensibilite" / "out" / "classement.csv"
    return list(csv.DictReader(f.open(encoding="utf-8"))) if f.exists() else []


def incertitude(profession_: str, annee: int = 2050) -> dict:
    p = profession(profession_)
    rows = [r for r in _classement() if r["profession"] == p and int(r["annee"]) == int(annee)]
    if not rows:
        raise ErreurOutil(f"pas d'indice de Sobol pour {p} en {annee} (années : 2030, 2040, 2050)")
    fam = {}
    for r in rows:
        fam.setdefault(r["famille"], []).append({"facteur": r["facteur"], "ST": round(float(r["ST"]), 2),
                                                  "ST_IC95": [round(float(r["ST_lo"]), 2), round(float(r["ST_hi"]), 2)],
                                                  "mu_star_pct": round(float(r["mu_star_pct"]), 1)})
    for v in fam.values():
        v.sort(key=lambda x: -x["ST"])
    return {"profession": S().PROFS[p], "annee": annee, "methode": "Morris puis Sobol (axe 5), sortie nationale, secteur privé",
            "familles": {"incertitude": "choix d'estimation et données (hors leviers)", "tout": "facteurs + leviers"},
            "indices": {k: v[:6] for k, v in fam.items()}}


def interpreter(texte: str) -> dict:
    r = NL().compile(texte)
    out = {k: r[k] for k in ("leviers", "profession", "territoire", "compris", "non_modelise", "non_compris",
                              "avertissements", "reformulations")}
    out["transferts"] = [{k: x[k] for k in ("id", "libelle", "t0", "cible", "statut")} for x in r.get("transferts", [])]
    out["transferts_hypothetiques"] = [{k: x[k] for k in ("id", "libelle", "source", "cible", "mode", "p", "acte", "t0",
                                                          "parametres_api", "balayage", "statut")}
                                       for x in r.get("transferts_hypothetiques", [])]
    out["o2_cible"] = bool(r.get("o2_cible"))
    return out


# ------------------------------------------------------------------ couverture (module de besoin, via l'API de la carte)
# API réelle : v2/prototype-carte/server.py, GET /api/couverture?prof=…&<leviers>&l23=1 (branche claude/besoin-carte-api-6d9504).
# Réponse : years ; fr / regs["R84"] / deps["63"] = {cb, cs, ecart, min, max} par année (cb tendanciel, cs scénario, 2026 = 1) ;
# fourchette_visible (règle des 5 % entre estimateurs) ; l23 = {params, transferts[{etp_liberes_source, actes_mg_liberes…}]}.
# L'API date L23 à l'année de décision de la carte (2026) : une autre date est signalée, pas appliquée.
CARTE_URL = os.environ.get("CARTE_URL", "http://127.0.0.1:8767")
SANS_COUVERTURE = {"medecine-generale", "medecins-generalistes", "generalistes", "specialistes", "medecins-specialistes"}  # O2


def q_ecart_couverture(pct: float) -> str:
    """Vocabulaire neutre de l'écart de couverture au tendanciel (mêmes seuils que q_variation)."""
    a = abs(pct)
    if a < 1:
        return "couverture proche du tendanciel"
    sens = "supérieure au" if pct > 0 else "moindre qu'au"
    return f"couverture légèrement {sens} tendanciel" if a < 5 else f"couverture {sens} tendanciel"


def _carte_couverture(q: dict) -> dict:
    import urllib.error
    import urllib.request
    from urllib.parse import urlencode
    url = f"{CARTE_URL}/api/couverture?{urlencode(q)}"
    try:
        with urllib.request.urlopen(url, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise ErreurOutil(f"l'API de couverture refuse la requête (HTTP {e.code})") from e
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        raise ErreurOutil(f"API de couverture injoignable ({CARTE_URL}/api/couverture) : indice non disponible") from e


TR_API = {"source": "tr_src", "cible": "tr_cible", "a": "tr_a", "s_inf": "tr_sinf", "k": "tr_k", "tau": "tr_tau", "t0": "tr_t0"}


def couverture(profession_: str, territoire_: str = "FR", leviers_: dict | None = None, l23: bool = False,
               l23_t0: int = 2026, annees: list[int] | None = None, transfert: dict | None = None,
               effectivite: bool = False, offre_mg: str = "constante") -> dict:
    """Indice de couverture C (base 2026 = 1) d'une des cinq professions, tendanciel et scénario, écart relatif, fourchette.
    transfert : transfert de tâches hypothétique (paramètres de l'utilisateur·rice), forme de L23 ; la MG et les
    spécialistes n'y sont admis qu'en source (O2)."""
    if str(profession_) in SANS_COUVERTURE:
        raise ErreurOutil("règle O2 : aucun indice de couverture pour la médecine générale ni les spécialistes ; "
                          "ils n'apparaissent que comme source d'un transfert (temps libéré, France entière)")
    p, t = profession(profession_), territoire(territoire_)
    lv = dict(leviers_ or {})
    leviers(lv)                                                     # mêmes bornes que projeter
    q = {"prof": p, **{k: ("1" if v is True else "0" if v is False else v) for k, v in lv.items()}, "l23": int(bool(l23))}
    pts = []
    if transfert:
        if transfert.get("cible") in SANS_COUVERTURE:
            raise ErreurOutil("règle O2 : la médecine générale et les spécialistes ne sont admis qu'en source d'un transfert")
        # a : poids de l'acte, rarement connu ; balayé ici (jamais un chiffre unique), le point médian sert de réponse
        a0 = transfert.get("a")
        pts = [round(min(0.5, x * a0), 4) for x in (0.5, 1, 2)] if a0 is not None else [0.05, 0.10, 0.20]
        q |= {TR_API[k]: v for k, v in (transfert | {"a": pts[1]}).items()}
    j = _carte_couverture(q)
    ys = [int(y) for y in j["years"]]
    z = j["fr"] if t == "FR" else (j.get("regs") or {}).get(t) if t[0] == "R" else \
        (j.get("deps") or {}).get(t[1:], (j.get("deps") or {}).get(t))
    if not z:
        raise ErreurOutil(f"pas d'indice de couverture pour {p} / {t} dans la réponse de l'API")
    ref = int(j.get("ref", 2026))
    annees = annees or [y for y in (2030, 2035, 2040, 2050) if y in ys]
    rows = []
    for y in annees:
        if y not in ys:
            raise ErreurOutil(f"année {y} absente de l'API de couverture (années : {ys[0]} à {ys[-1]})")
        i = ys.index(y)
        e = 100 * z["ecart"][i]
        row = {"annee": y, "indice_tendanciel": round(z["cb"][i], 3), "indice_scenario": round(z["cs"][i], 3),
               "ecart_tendanciel_pct": round(e, 2 if abs(e) < 0.1 else 1),   # très petit écart : pas « −0,0 % »
               "qualificatifs": {"ecart": q_ecart_couverture(e)}}
        if j.get("fourchette_visible"):                            # règle des 5 % de la carte (décision axe 5)
            row["fourchette_estimateurs"] = [round(z["min"][i], 3), round(z["max"][i], 3)]
        rows.append(row)
    blk = j.get("l23") or {}
    ia = ys.index(annees[-1])
    tr = [{"transfert": x.get("transfert"), "source": x.get("source"), "cible": x.get("cible"), "annee": annees[-1],
           "etp_liberes_source_france": round(x["etp_liberes_source"][ia]) if x.get("etp_liberes_source") else None,
           "actes_mg_liberes_france": x["actes_mg_liberes"][ia] if x.get("actes_mg_liberes") else None}
          for x in blk.get("transferts", []) if x.get("cible") not in SANS_COUVERTURE]
    params = [{"nom": h.get("name"), "statut": h.get("status"), "source": h.get("source")}
              for h in blk.get("params", []) if h.get("name") in ("a", "k", "s_inf", "tau", "mu")]
    out = {"profession": S().PROFS[p], "territoire": nom_territoire(t), "code_territoire": t,
           "grandeur": "indice de couverture (offre / demande de soins de ville, base 2026 = 1)",
           "reference": ref, "estimateur_central": j.get("central"), "estimateurs": j.get("estimateurs"),
           "effectif": "inchangé dans le modèle par un transfert de tâches (L23 ou hypothétique)",
           "l23": {"actif": bool(l23), "t0": ref}, "annees": rows, "transferts": tr, "parametres_l23": params,
           "lecture": "1 = couverture de 2026 ; l'écart se lit par rapport au tendanciel de la même année, jamais comme une part du besoin couvert"}
    if l23 and l23_t0 != ref:
        out["avertissement"] = f"l'API date la vaccination en officine à {ref} ; la date demandée ({l23_t0}) n'est pas appliquée"
    if blk.get("note"):
        out["note_l23"] = blk["note"]
    h = j.get("transfert_hypothetique")
    if h:
        out["transfert_hypothetique"] = {
            "statut": h["statut"], "source": h["source"], "cible": h["cible"],
            "parametres": [{"nom": x["name"], "valeur": x["value"], "unite": x["unit"], "statut": x["status"]} for x in h["params"]],
            "besoin_source": h["besoin_source"], "etp_source_transferes_france": round(h["etp_source_transferes"][ia]),
            "note": h["note"]}
        for x in out["transfert_hypothetique"]["parametres"]:
            if x["nom"] == "a":
                x["statut"] = ("balayé autour de la valeur donnée (hypothèse de l'utilisateur)" if transfert.get("a") is not None
                               else "inconnu, balayé à 5, 10 et 20 % (supposé)")
        bal = []
        for a in pts:                                   # même territoire, même dernière année ; le point médian est `j`
            jj = j if a == pts[1] else _carte_couverture(q | {"tr_a": a})
            zz = jj["fr"] if t == "FR" else (jj.get("regs") or {}).get(t) if t[0] == "R" else \
                (jj.get("deps") or {}).get(t[1:], (jj.get("deps") or {}).get(t))
            e = 100 * zz["ecart"][ia]
            pt = {"a": a, "indice_scenario": round(zz["cs"][ia], 3), "indice_tendanciel": round(zz["cb"][ia], 3),
                  "ecart_tendanciel_pct": round(e, 2), "qualificatifs": {"ecart": q_ecart_couverture(e)},
                  "temps_plein_source_transferes_france": round(jj["transfert_hypothetique"]["etp_source_transferes"][ia])}
            if jj.get("fourchette_visible"):
                pt["fourchette_estimateurs"] = [round(zz["min"][ia], 3), round(zz["max"][ia], 3)]
            bal.append(pt)
        out["balayage_a"] = bal
        out["effectif"] = "inchangé dans le modèle (transfert de tâches hypothétique)"
        out["lecture_transfert"] = ("transfert hypothétique, paramètres de l'utilisateur·rice : citer les trois valeurs de "
                                    "balayage_a, jamais un seul chiffre ; ce n'est pas un levier de la carte")
    if effectivite:                                     # O3 : seulement pour le transfert sourcé (L23), cible pharmaciens
        if not l23 or p != "pharmaciens":
            raise ErreurOutil("l'effectivité ne se calcule que pour la vaccination en officine (l23 vrai, profession pharmaciens)")
        out["effectivite"] = _effectivite_bloc(_TRANSFERTS["vaccination_officine"], t, annees[-1], offre_mg)
    return out


# Ce que le modèle ne sait PAS faire, d'après sa documentation (synthèse du 2026-11-14, README, ROADMAP).
# Le glossaire du modèle (non_modelises) complète cette liste pour les politiques publiques.
HORS_PERIMETRE = [
    {"id": "medecins", "sujet": "Médecins généralistes et médecins spécialistes",
     "raison": "La médecine générale et les médecins spécialistes ne sont pas projetés : la médecine générale est hors du sujet, les spécialistes sont une amélioration possible, hors plan. Ils entrent seulement comme source d'un transfert de tâches (temps libéré), jamais comme profession projetée ni pour un indice de couverture (règle O2)."},
    {"id": "autres_professions", "sujet": "Autres professions (orthophonistes, aides-soignants, psychologues…)",
     "raison": "Le modèle couvre cinq professions seulement."},
    {"id": "secteur_public", "sujet": "Effectifs salariés du public (hôpital public, PMI, centres de santé municipaux…)",
     "raison": "La sortie est l'effectif « libéral » au sens du secteur privé ; le public n'est pas une sortie publiée."},
    {"id": "commune", "sujet": "Projection à la commune, au quartier, à l'EPCI ou au bassin de vie",
     "raison": "Le grain servi est le département ; une ville est ramenée à son département. La commune est en cours (≈ 6,8 s par scénario)."},
    {"id": "horizon", "sujet": "Années après 2050 ; passé avant les données (2012)",
     "raison": "Projection de l'origine (2026 ; 2023 pour les infirmiers) à 2050 ; historique observé depuis 2012."},
    {"id": "besoin", "sujet": "Besoin en valeur absolue, part du besoin couvert, délais d'attente, patients par professionnel, « combien en manque »",
     "raison": "Le modèle projette l'offre (effectifs). Le module de besoin ne fournit qu'un indice de couverture relatif "
               "(outil couverture : base 2026 = 1, écart au tendanciel), pour les cinq professions seulement."},
    {"id": "couverture_medecins", "sujet": "Couverture, besoin ou indice pour la médecine générale ou les spécialistes",
     "raison": "Règle O2 : la médecine générale et les spécialistes n'entrent que comme source d'un transfert de tâches ; "
               "aucun indice de couverture n'est calculé pour eux."},
    {"id": "activite_reelle", "sujet": "Temps de travail, équivalents temps plein, volume de soins",
     "raison": "L'activité par professionnel est une hypothèse supposée (curseur), pas une donnée mesurée."},
    {"id": "couts", "sujet": "Coûts, budget, rentabilité d'une politique",
     "raison": "Le modèle ne contient aucune donnée de coût."},
    {"id": "causalite", "sujet": "Causes (« pourquoi les kinés partent ») hors des leviers modélisés",
     "raison": "Le modèle décompose l'écart par flux (entrées, sorties, régulation) ; il n'estime pas les motivations individuelles."},
    {"id": "autres_pays", "sujet": "Autres pays", "raison": "France seulement (métropole et DROM)."},
    {"id": "prevision_exacte", "sujet": "Un chiffre exact, certain ou une prévision",
     "raison": "Projection sous hypothèses, toujours avec une fourchette ; aucun backtest au-delà d'environ 10 ans."},
    {"id": "jugement", "sujet": "Recommandation ou jugement de valeur (« la meilleure politique », « le pire département »)",
     "raison": "Le modèle décrit et compare ; le choix revient au décideur (lexique neutre du projet)."},
]


# Modèle servi (v2/prototype/server.py, Model : C1 par défaut, A0 par JUMEAU_MODELE=A0) ; chiffres mesurés, cités des articles.
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


# ------------------------------------------------------------------ planifier : objectif chiffré -> mélanges de leviers datés
# Recherche dans les bornes du modèle (curseurs de la carte). Seuls les leviers qui peuvent augmenter l'effectif sont
# cherchés (la régulation déplace ou retire des entrées). Kill test d'additivité (2026-11-14) : écart médian 0,2 %, 1 mélange
# sur 20 au-delà de 10 % (avec régulation) : la somme des effets seuls sert à chercher, le jumeau recalcule chaque mélange montré.
# Zones plausibles retirées le 2026-11-14 (demande de l'utilisateur·rice) : le critère « le plus simple » préfère déjà les
# petits réglages.
_BORNES = {"quotas": (1.0, 1.5, 0.05), "etrangers": (1.0, 2.0, 0.1), "retraite": (0.0, 3.0, 0.5), "cumul": (1.0, 2.0, 0.1),
           "precoces": (1.0, 0.5, -0.1)}


def _grille(a, b, pas):
    n = int(round((b - a) / pas))
    return [round(a + i * pas, 2) for i in range(n + 1)]


def planifier(profession_: str, territoire_: str = "FR", annee: int = 2040, grandeur: str = "effectif",
              hausse_pct: float | None = None, valeur_cible: float | None = None, reference: str = "tendanciel",
              leviers_exclus: list | None = None, n_max_leviers: int = 3) -> dict:
    """Objectif chiffré à un horizon -> mélanges de leviers qui l'atteignent, recalculés par le jumeau, avec délais."""
    import itertools
    p, t = profession(profession_), territoire(territoire_)
    cle = "densite_100k_scenario" if grandeur == "densite" else "scenario"
    base = _answer(p, leviers({}), t)
    y = _annees([annee], base)[0]
    lb = _ligne(base, y, _dens_fr(p, leviers({}), y))
    o = base["origin"]
    v_tend = lb["densite_100k_tendanciel"] if grandeur == "densite" else lb["tendanciel"]
    v_orig = _r1(base["dens_base"][0]) if grandeur == "densite" else round(base["base"][0])
    if valeur_cible is not None:
        cible, ref, objectif = float(valeur_cible), None, f"{valeur_cible:g} {'pour 100 000 habitants' if grandeur == 'densite' else 'professionnels'} en {y}"
    elif hausse_pct is not None:
        ref = v_tend if reference == "tendanciel" else v_orig
        cible = ref * (1 + hausse_pct / 100)
        objectif = (f"+{hausse_pct:g} % {'de densité' if grandeur == 'densite' else "d'effectif"} par rapport "
                    + (f"au tendanciel {y}" if reference == "tendanciel" else f"à {o} (aujourd'hui)"))
    else:
        raise ErreurOutil("donner hausse_pct (avec reference) ou valeur_cible")
    tete = {"profession": S().PROFS[p], "territoire": nom_territoire(t), "code_territoire": t, "annee": y,
            "grandeur": grandeur, "objectif": objectif, "cible": round(cible, 1),
            "ecart_cible_moins_tendanciel": _r1(cible - v_tend) if grandeur == "densite" else round(cible - v_tend),
            "aujourd_hui": {"annee": o, "valeur": v_orig},
            "tendanciel_annee": {"valeur": v_tend, "evolution_depuis_aujourd_hui_pct": round((v_tend / v_orig - 1) * 100, 1) if v_orig else None,
                                 "fourchette_effectif": lb["fourchette_scenario"]},
            "annee_decision_du_modele": S().DECISION}
    if hausse_pct is not None:     # les deux lectures de « +X % » : par rapport à aujourd'hui et par rapport à la tendance
        tete["lectures"] = {
            "par_rapport_a_aujourd_hui": {"cible": round(v_orig * (1 + hausse_pct / 100), 1),
                                          "ecart_cible_moins_tendanciel": round(v_orig * (1 + hausse_pct / 100) - v_tend, 1),
                                          "deja_atteint_sans_politique": v_tend >= v_orig * (1 + hausse_pct / 100)},
            "par_rapport_a_la_tendance": {"cible": round(v_tend * (1 + hausse_pct / 100), 1),
                                          "ecart_cible_moins_tendanciel": round(v_tend * hausse_pct / 100, 1),
                                          "deja_atteint_sans_politique": False}}
    if v_tend >= cible:
        return {**tete, "deja_atteint_sans_politique": True, "melanges": [],
                "lecture": "la tendance, sans nouvelle politique, atteint déjà la cible : aucun levier n'est nécessaire"}
    exclus = set(leviers_exclus or [])
    ks = [k for k in _BORNES if k not in exclus]
    meta = {m["k"]: m for m in S().lever_meta()}
    val = lambda r: (r["dens_scn"] if grandeur == "densite" else r["scn"])[r["years"].index(y)]
    v0 = val(base)
    demi = lb["fourchette_demi_largeur_pct"] / 100

    def courbe(k, grille):        # effet de chaque levier seul, sur sa grille (jumeau)
        return {g: val(_answer(p, leviers({k: g}), t)) - v0 for g in grille}

    def delai(k):
        return S().LAG[p] + 1 if k == "quotas" else _DELAI_ANS.get(k, 1)

    def chercher(zones):
        grilles = {k: _grille(*zones[k]) for k in ks}
        eff = {k: courbe(k, grilles[k]) for k in ks}
        neutre = {k: grilles[k][0] for k in ks}
        cands = []
        for combo in itertools.product(*[grilles[k] for k in ks]):
            ch = {k: g for k, g in zip(ks, combo) if g != neutre[k]}
            if not ch or len(ch) > n_max_leviers:
                continue
            gain = sum(eff[k][g] for k, g in ch.items())
            if v0 + gain < cible:
                continue
            depl = sum(abs(g - neutre[k]) / abs(_BORNES[k][1] - _BORNES[k][0]) for k, g in ch.items())
            cands.append((ch, gain, depl, max(delai(k) for k in ch)))
        return cands, eff, grilles

    def verifier(ch):
        r = _answer(p, leviers(ch), t)
        v = val(r)
        li = _ligne(r, y)
        return v, li

    cands, eff, grilles = chercher(_BORNES)
    criteres = [("le plus simple", lambda c: (len(c[0]), c[2])), ("effet le plus tôt", lambda c: (c[3], len(c[0]), c[2])),
                ("prudent (cible atteinte au bas de la fourchette)", lambda c: (len(c[0]), c[2]))]
    out, vus = [], set()
    for nom, cle_tri in criteres:
        prudent = nom.startswith("prudent")
        for ch, gain, depl, dmax in sorted(cands, key=cle_tri)[:40]:
            if prudent and (v0 + gain) * (1 - demi) < cible:
                continue
            key = tuple(sorted(ch.items()))
            v, li = verifier(ch)
            if v < cible or (prudent and v * (1 - demi) < cible):
                continue                      # l'interaction fait manquer la cible : candidat suivant
            if key in vus:
                break
            vus.add(key)
            lev = []
            for k, g in ch.items():
                d = delai(k)
                lev.append({"levier": _fmt_levier(k, g), "delai_ans": d, "delai_qualificatif": q_delai(d),
                            "decision_dans_le_modele": S().DECISION, "premier_effet": S().DECISION + d,
                            "dernier_moment_pour_un_premier_effet_avant_l_horizon": y - d,
                            "statut": meta[k]["status"], "source": meta[k]["source"]})
            out.append({"critere": nom, "leviers": lev, "reglage_carte": ch,
                        "valeur_obtenue": _r1(v) if grandeur == "densite" else round(v),
                        "ecart_au_tendanciel": _r1(v - v_tend) if grandeur == "densite" else round(v - v_tend),
                        "qualificatif": q_variation((v / v_tend - 1) * 100 if v_tend else None),
                        "fourchette_effectif": li["fourchette_scenario"],
                        "atteint_au_bas_de_la_fourchette": v * (1 - demi) >= cible})
            break
    if not out:
        tout = {k: grilles[k][-1] for k in ks}
        v, li = verifier(tout)
        return {**tete, "deja_atteint_sans_politique": False, "atteignable": False, "melanges": [],
                "meilleur_atteignable": {"leviers": resume_leviers(leviers(tout)), "valeur": _r1(v) if grandeur == "densite" else round(v),
                                         "ecart_a_la_cible_pct": round((v / cible - 1) * 100, 1)},
                "lecture": "cible hors d'atteinte avec les leviers du modèle, même aux bornes : horizon trop court ou objectif trop haut",
                "methode": _METHODE_PLAN}
    return {**tete, "deja_atteint_sans_politique": False, "atteignable": True, "melanges": out,
            "methode": _METHODE_PLAN}


# ------------------------------------------------------------------ politique hors modèle -> leviers (traduction supposée)
_ESSAIS = {"precoces": (0.9, 0.8), "cumul": (1.2, 1.5), "etrangers": (1.2, 1.5), "quotas": (1.1, 1.2), "retraite": (0.5, 1.0)}


@lru_cache(maxsize=1)
def _correspondances() -> dict:
    import yaml
    return yaml.safe_load((Path(__file__).resolve().parent / "correspondances.yaml").read_text())


def traduire_politique(politique: str, profession_: str, territoire_: str = "FR", annee: int = 2040) -> dict:
    """Politique non modélisée -> leviers du même mécanisme (SUPPOSÉ), essayés à deux ampleurs d'essai (supposées) : une
    fourchette de traduction, pas une estimation de la politique."""
    G = NL().glossaire()["non_modelises"]
    C = _correspondances()
    if politique not in G or politique not in C:
        raise ErreurOutil(f"politique inconnue {politique!r} ; valeurs : {', '.join(C)}")
    g, c = G[politique], C[politique]
    tete = {"politique": g["libelle"], "pourquoi_hors_modele": g["raison"], "traduction": c["traduction"],
            "statut": "supposé (aucune élasticité estimée sur données ouvertes)", "limite": c.get("limite")}
    if c["traduction"] == "aucune":
        if c.get("outil") == "couverture":
            return {**tete, "lecture": "effectif inchangé dans le modèle ; effet calculé sur l'indice de couverture des "
                                       "pharmaciens : appeler l'outil couverture avec l23"}
        return {**tete, "lecture": "pas dans le modèle : aucun levier du jumeau ne porte ce mécanisme"}
    p, t = profession(profession_), territoire(territoire_)
    base = _answer(p, leviers({}), t)
    y = _annees([annee], base)[0]
    i = base["years"].index(y)
    b = base["base"][i]
    essais = []
    for niveau, j in (("ampleur basse", 0), ("ampleur haute", 1)):
        reg = {}
        for l in c["leviers"]:
            reg.update(l.get("reglage") or {l["levier"]: _ESSAIS[l["levier"]][j]})
        lv = leviers(reg)
        e = _answer(p, lv, t)["scn"][i] - b
        essais.append({"niveau": niveau, "reglage": resume_leviers(lv), "reglage_carte": reg, "ecart_au_tendanciel": round(e),
                       "ecart_pct": round(e / b * 100, 2) if b else None, "qualificatif": q_variation(e / b * 100 if b else None)})
    if any(l["levier"] == "regul" for l in c["leviers"]) and all(abs(e["ecart_au_tendanciel"]) < 1 for e in essais):
        tete["note_effet_nul"] = ("effet nul ici parce qu'aucun département de ce territoire n'est en zone « remplacement seul » "
                                  "(zonage actuel) : le jumeau ne peut pas représenter la politique ici, ce n'est pas une "
                                  "absence d'effet de la politique")
    return {**tete, "profession": S().PROFS[p], "territoire": nom_territoire(t), "code_territoire": t, "annee": y,
            "tendanciel": round(b),
            "leviers_du_meme_mecanisme": [{k: l[k] for k in ("levier", "sens", "mecanisme")} for l in c["leviers"]],
            "essais": essais,
            "lecture": "traduction supposée : l'ampleur réelle de la politique est inconnue ; les deux essais encadrent un effet "
                       "possible si la politique agit par ce mécanisme, à ces deux ampleurs d'essai (supposées)"}


_METHODE_PLAN = ("effet de chaque levier seul calculé par le jumeau sur sa grille, dans les bornes du modèle ; mélanges "
                 "cherchés sur la somme des effets (additivité vérifiée : écart médian 0,2 % sur 20 mélanges), chaque mélange "
                 "montré recalculé par le jumeau ; décision en 2026 dans le modèle")


_TRANSFERTS = {"vaccination_officine": "L23"}


@lru_cache(maxsize=4)
def _effectivite(code: str, offre_mg: str):
    S()                                                   # chdir vers la racine du dépôt (chemins de données relatifs)
    if str(V2) not in sys.path:
        sys.path.insert(0, str(V2))
    from besoin.effectivite import evaluer
    return evaluer(code, offre_mg=offre_mg)


def _effectivite_bloc(code: str, t: str, annee: int, offre_mg: str) -> dict:
    """Effectivité d'un transfert sourcé (O3) : couverture de la source et de la cible, avec et sans transfert."""
    if t[:1] == "R":
        raise ErreurOutil("l'effectivité se lit au département ou pour la France : donner un département de la région")
    try:
        res = _effectivite(code, offre_mg)
    except FileNotFoundError as e:
        raise ErreurOutil(f"offre de médecine générale « {offre_mg} » indisponible : {e}") from None
    from besoin.effectivite import resume
    if annee not in set(int(y) for y in res["years"]):
        raise ErreurOutil(f"année {annee} hors de la trajectoire ({int(res['years'].min())}–{int(res['years'].max())})")
    out = resume(res, None if t == "FR" else t[1:], annee)
    out["lecture"] = ("couverture = offre / demande, indexée sur 2026 (1 = niveau de 2026) ; le transfert déplace une part de "
                      "la demande de la source vers la cible, sans changer les effectifs ; la couverture de la source n'existe "
                      "que dans ce bloc (O3), avec une offre de médecine générale lue en entrée")
    return out


def perimetre() -> dict:
    G = NL().glossaire()
    srv = S()
    return {
        "couvert": {
            "professions": srv.PROFS,
            "sortie": "effectif « libéral » = secteur privé (lucratif ou non), tout employeur public exclu",
            "grain": "France, région, département",
            "annees": {"historique_observe": "2012 à l'origine", "projection": f"origine (2026 ; infirmiers 2023) à {srv.H}"},
            "questions": ["effectif projeté et sa fourchette",
                          "indice de couverture (base 2026 = 1) et effet de la vaccination en officine (L23) sur celui des pharmaciens", "effet d'un ou plusieurs leviers (écart au tendanciel, par flux)",
                          "comparaison de scénarios", "sensibilité d'un levier sur une plage", "classement de départements (densité, écart, évolution)",
                          "paramètres qui pèsent le plus sur l'incertitude (Sobol)", "délai d'effet et niveau de preuve des leviers"],
            "leviers": [m["label"] for m in srv.LEVIERS_UI],
        },
        "hors_perimetre": HORS_PERIMETRE,
        "politiques_non_modelisees": [{"id": k, "libelle": v["libelle"], "raison": v["raison"]} for k, v in G["non_modelises"].items()],
        "modele_de_projection": MODELE,
        "version_modele": version_modele(),
    }


# ------------------------------------------------------------------ objectif -> leviers (problème inverse)

# Leviers de politique testés, dans le sens qui augmente l'effectif, sur la grille de pas du modèle (LEVIERS_UI).
# Exclus : activite et pop_scen (hypothèses de contexte, pas des politiques) ; regul (ne peut que déplacer ou retirer).
_GRILLES = [("quotas", {}, [round(1 + 0.05 * i, 2) for i in range(1, 11)]),
            ("quotas", {"quotas_region": True}, [round(1 + 0.05 * i, 2) for i in range(1, 11)]),
            ("etrangers", {}, [round(1 + 0.1 * i, 1) for i in range(1, 11)]),
            ("retraite", {}, [0.5 * i for i in range(1, 7)]),
            ("cumul", {}, [round(1 + 0.1 * i, 1) for i in range(1, 11)]),
            ("precoces", {}, [round(1 - 0.1 * i, 1) for i in range(1, 6)])]
_MAX = {"quotas": 1.5, "etrangers": 2.0, "retraite": 3.0, "cumul": 2.0, "precoces": 0.5}


def atteindre(profession_: str, territoire_: str, hausse_pct: float, annee: int = 2050, grandeur: str = "densite",
              reference: str = "tendanciel") -> dict:
    """Pour atteindre +hausse_pct % de `grandeur` en `annee` (par rapport au tendanciel de la même année, ou à
    l'origine), quelle valeur de chaque levier faut-il, seul, dans ses bornes ? Et tous les leviers au maximum ?
    Recherche par dichotomie sur la grille de pas de chaque levier (effet supposé monotone, vérifié aux extrémités)."""
    p, t = profession(profession_), territoire(territoire_)
    cle = "densite_100k_scenario" if grandeur == "densite" else "scenario"
    base = _answer(p, leviers({}), t)
    y = _annees([annee], base)[0]
    lb = _ligne(base, y)
    ref = (lb[cle] if reference == "tendanciel" else
           (_r1(base["dens_base"][0]) if grandeur == "densite" else round(base["base"][0])))
    if ref is None:
        raise ErreurOutil("densité indisponible pour ce territoire (population manquante)")
    cible = ref * (1 + hausse_pct / 100)
    if lb[cle] is not None and lb[cle] >= cible:
        return {"profession": S().PROFS[p], "territoire": nom_territoire(t), "code_territoire": t, "annee": y,
                "objectif": f"+{hausse_pct:g} % par rapport {'au tendanciel ' + str(y) if reference == 'tendanciel' else 'à ' + str(base['origin'])}",
                "reference": ref, "cible": round(cible, 1), "deja_atteint_sans_politique": True,
                "tendanciel_annee": {"effectif": lb["tendanciel"], "densite_100k": lb["densite_100k_tendanciel"]},
                "lecture": "la tendance, sans nouvelle politique, atteint déjà la cible : aucun levier n'est nécessaire"}

    def valeur(lv):
        r = _answer(p, leviers(lv), t)
        return _ligne(r, y)

    out = []
    for k, extra, grille in _GRILLES:
        if extra.get("quotas_region") and t == "FR":
            continue
        if extra.get("quotas_region") and t.startswith("R"):
            continue                       # région affichée : la hausse limitée à la région donne la même valeur que la hausse partout
        suf = " (région seulement)" if extra else ""
        lab = S().UI[k]["label"] + suf
        haut = valeur({k: grille[-1], **extra})
        if haut[cle] < cible:
            out.append({"levier": lab, "suffit_seul": False, "valeur_max": _fmt_levier(k, grille[-1]) + suf,
                        "atteint_au_max": haut[cle], "ecart_a_la_cible_pct": round((haut[cle] / cible - 1) * 100, 1)})
            continue
        lo, hi, best = 0, len(grille) - 1, (grille[-1], haut)
        while lo <= hi:
            m = (lo + hi) // 2
            v = valeur({k: grille[m], **extra})
            if v[cle] >= cible:
                best, hi = (grille[m], v), m - 1
            else:
                lo = m + 1
        out.append({"levier": lab, "suffit_seul": True, "reglage_necessaire": _fmt_levier(k, best[0]) + suf,
                    "valeur_obtenue": best[1][cle], "fourchette_effectif": best[1]["fourchette_scenario"],
                    "delai": S().UI[k]["delai"]})
    tout = valeur(dict(_MAX))
    meta = {m["k"]: m for m in S().lever_meta()}
    return {
        "profession": S().PROFS[p], "territoire": nom_territoire(t), "code_territoire": t, "annee": y,
        "objectif": f"+{hausse_pct:g} % de {'densité pour 100 000 habitants' if grandeur == 'densite' else 'effectif'} "
                    f"par rapport {'au tendanciel ' + str(y) if reference == 'tendanciel' else 'à ' + str(base['origin'])}",
        "reference": ref, "cible": round(cible, 1),
        "tendanciel_annee": {"effectif": lb["tendanciel"], "densite_100k": lb["densite_100k_tendanciel"]},
        "origine": {"annee": base["origin"], "effectif": round(base["base"][0]), "densite_100k": _r1(base["dens_base"][0])},
        "leviers_seuls": out,
        "tous_leviers_au_maximum": {"valeur": tout[cle], "atteint": tout[cle] >= cible,
                                    "reglage": resume_leviers(leviers(dict(_MAX)))},
        "statut_des_leviers": {meta[k]["label"]: meta[k]["status"] for k in _MAX},
        "methode": "chaque levier testé seul sur sa grille de pas, dans ses bornes ; aucune combinaison optimisée, "
                   "sauf « tous au maximum » ; densité à population Insee Omphale centrale et activité constante ; "
                   "seuls les leviers du modèle sont testés (d'autres politiques peuvent exister hors du modèle)",
        "perimetre": PERIMETRE,
    }
