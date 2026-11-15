"""Effectivité d'un transfert de tâches : couverture de la source et de la cible, avec et sans transfert (O3).

Pour un transfert A → B (ex. L23 : médecine générale → pharmaciens) et chaque territoire T, année t :
  C_B(T,t), C'_B(T,t)   couverture de la cible sans et avec transfert (offre du jumeau, besoin M1), indexée sur 2026
  C_A(T,t), C'_A(T,t)   couverture de la source, avec l'offre MG lue en entrée (offre_mg) ; même indexation
  gain_A = C'_A − C_A,  perte_B = C'_B − C_B
Le calcul est refait pour k aux bornes de sa plage (k est supposé, [0,25 ; 1]) : k change la charge reçue par B, pas
le temps libéré chez A.

Critère d'effectivité (décision du 2026-11-15, remplace le « critère par défaut » ; statut : supposé, fixé avant
le recalcul) : on juge l'effet du transfert seul, pas la tendance de la cible.
  effectif(T,t, k)  ⇔  gain_A(T,t) > 0  et  perte_B(T,t, k) ≥ −SEUIL_CIBLE   (SEUIL_CIBLE = 1 point d'indice, supposé)
  La position de la cible par rapport à 2026 (C_B < 1 sans transfert) est rendue à côté, comme contexte.
  verdict(T,t) = « effectif » si vrai pour toute la plage de k, « non effectif » si faux pour toute la plage,
                 « dépend de k » sinon.
Les effectifs ne changent jamais (pas de rétroaction, N9) ; seule la répartition du besoin bouge.
"""
from dataclasses import replace
from functools import lru_cache

import numpy as np

from besoin.couverture import couverture, offre
from besoin.cube import Population
from besoin.offre_mg import MG, fournisseur
from besoin.transferts import appliquer, l23

K_PLAGE = (0.25, 1.0)          # fiches de l'axe 1, statut supposé
SEUIL_CIBLE = 0.01             # perte de couverture acceptée chez la cible, en indice (1 point) ; supposé
CRITERE = ("effectif si le transfert fait progresser la couverture de la source et ne fait pas perdre plus d'1 point de "
           "couverture à la cible, sur toute la plage de k ; effet du transfert seul, la tendance de la cible est donnée à "
           "part (critère supposé, décision du 2026-11-15)")
TRANSFERTS = {"L23": l23}
# s_∞ et τ mesurés au national par P-B6 (vaccination antigrippale en officine, 2021-22 → 2024-25) ; a et k restent
# ceux de la fiche (placeholders supposés) tant que la branche des fiches de l'axe 1 n'est pas fusionnée.
MESURE_PB6 = {"L23": dict(s_inf=0.74, tau=2.4)}


@lru_cache(maxsize=None)
def etat_tendanciel(profs: tuple, horizon: int = 2050) -> dict:
    """Trajectoire tendancielle du jumeau pour `profs` (stock-flux à taux locaux), origine comprise."""
    from sante import estimators as V1
    from jumeau.estimators import twin_of
    from jumeau.history import sector_table
    t = sector_table(list(profs))
    o = int(t.year.max())
    est = twin_of(V1.StockFlowLocal)().fit(t, (o - 5, o), o)
    return {o: est.state, **est.trajectory(horizon).states}


def _c_source(S, B0, B1, ref):
    j = S.y(ref)
    with np.errstate(divide="ignore", invalid="ignore"):
        base = S.values[0, :, j] / B0.values[0, :, j]
        return (S.values[0] / B0.values[0]) / base[:, None], (S.values[0] / B1.values[0]) / base[:, None]


def evaluer(transfert: str = "L23", years=None, etat: dict | None = None, pop: Population | None = None,
            estimateur: str = "M1", offre_mg: str = "constante", ref: int = 2026, k_plage=K_PLAGE,
            **override) -> dict:
    """Couvertures source et cible, avec et sans transfert, pour k aux bornes et à la valeur centrale ; verdicts."""
    tr = TRANSFERTS[transfert](**(MESURE_PB6.get(transfert, {}) | override))
    etat = etat_tendanciel((tr.cible,)) if etat is None else etat
    pop = Population.load() if pop is None else pop
    years = [y for y in sorted(etat) if y >= ref] if years is None else list(years)
    import importlib                                       # import ciblé : discover() chargerait M4 (scipy)
    est = getattr(importlib.import_module(f"besoin.estimateurs.{estimateur.lower()}"), estimateur)().fit(pop, etat, ref)
    B0 = est.predict(pop, etat, years)
    S_B = offre(etat, years).sel(professions=[tr.cible])
    terr = S_B.territories
    mg = fournisseur(offre_mg)
    S_A = mg.cube(terr, years)
    B0 = replace(B0, territories=B0.territories)            # B porte source et cible (M1 sert la MG comme source)
    B0A, B0B = B0.sel(professions=[tr.source]), B0.sel(professions=[tr.cible])
    if not (B0A.territories == terr).all():
        raise ValueError("territoires du besoin et de l'offre non alignés")

    ks = sorted({k_plage[0], tr.k, k_plage[1]})
    par_k, verdict = {}, None
    C0B = couverture(S_B, B0B, ref).values[0]
    for k in ks:
        B1, detail = appliquer(B0, [replace(tr, k=k)])
        B1A, B1B = B1.sel(professions=[tr.source]), B1.sel(professions=[tr.cible])
        C0A, C1A = _c_source(S_A, B0A, B1A, ref)
        C1B = couverture(S_B, B1B, ref, S_B, B0B).values[0]
        ok = (C1A - C0A > 0) & (C1B - C0B >= -SEUIL_CIBLE)
        verdict = ok[None] if verdict is None else np.concatenate([verdict, ok[None]])
        par_k[k] = dict(couverture_cible=C1B, couverture_source=C1A, gain_source=C1A - C0A, perte_cible=C1B - C0B,
                        etp_liberes=detail[0]["libere"], etp_recus=detail[0]["recu"])
    tout, aucun = verdict.all(axis=0), (~verdict).all(axis=0)
    v = np.where(tout, "effectif", np.where(aucun, "non effectif", "dépend de k"))
    return dict(transfert=tr, k=ks, territories=terr, years=np.asarray(years), C0_cible=C0B, C0_source=C0A,
                par_k=par_k, verdict=v, offre_mg=mg.info(), estimateur=est.name, grandeur=est.grandeur,
                critere=CRITERE, population=pop.source)


def resume(res: dict, territoire: str | None, annee: int) -> dict:
    """Une ligne lisible pour l'API et l'assistant : un territoire (ou la France, par sommes) et une année."""
    j = int(np.flatnonzero(res["years"] == annee)[0])
    terr = res["territories"]
    tr = res["transfert"]
    if territoire is None:
        idx, nom = slice(None), "France"
    else:
        hit = np.flatnonzero(terr == territoire)
        if not len(hit):
            raise KeyError(f"territoire {territoire!r} absent")
        idx, nom = int(hit[0]), territoire

    def val(a):
        x = np.asarray(a)[idx, j]
        return float(np.nanmedian(x)) if np.ndim(x) else float(x)

    def somme(a):
        return float(np.asarray(a)[idx, j].sum()) if territoire is None else float(np.asarray(a)[idx, j])

    lignes = {f"{k:g}": dict(couverture_cible=round(val(d["couverture_cible"]), 4),
                             couverture_source=round(val(d["couverture_source"]), 4),
                             gain_source_points=round(100 * val(d["gain_source"]), 2),
                             perte_cible_points=round(100 * val(d["perte_cible"]), 2),
                             etp_liberes_source=round(somme(d["etp_liberes"]), 1),
                             etp_recus_cible=round(somme(d["etp_recus"]), 1))
              for k, d in res["par_k"].items()}
    if territoire is None:
        vs, n = np.unique(res["verdict"][:, j], return_counts=True)
        verdict = {str(a): int(b) for a, b in zip(vs, n)}
    else:
        verdict = str(res["verdict"][idx, j])
    return dict(
        transfert=tr.name, source=tr.source, cible=tr.cible, territoire=nom, annee=annee,
        couverture_cible_sans=round(val(res["C0_cible"]), 4), couverture_source_sans=round(val(res["C0_source"]), 4),
        par_k=lignes, verdict=verdict, critere=res["critere"],
        contexte_cible=("sans transfert, la cible est sous son niveau de 2026 : la tendance pèse plus que le transfert"
                        if val(res["C0_cible"]) < 1 else "sans transfert, la cible reste au moins à son niveau de 2026"),
        agregat="médiane des départements" if territoire is None else "département",
        parametres=dict(a=tr.a, k_plage=res["k"], s_inf=tr.s_inf, tau=tr.tau, t0=tr.t0, mu=tr.mu,
                        statut="a et k : supposés (placeholders de la fiche L23) ; s_∞ et τ : mesurés au national (P-B6)"),
        offre_mg=res["offre_mg"], estimateur=res["estimateur"], grandeur=res["grandeur"],
        limites=["les effectifs ne changent pas : seule la répartition du besoin bouge (N9)",
                 "k est supposé : la plage donne l'incertitude sur la charge reçue par la cible",
                 "au-delà de 2036 environ, scénario conditionnel et non prévision"],
    )
