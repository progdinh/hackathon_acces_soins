"""Entrées nettes : N <- N + k(t) · m · (I + pente · h).

I = flux annuel net ajusté dans les tranches où la rétention brute dépasse 1 (entrées, retours,
arrivées d'autres territoires). k(t) = taille relative de la cohorte en formation (DREES, inscrits)
si `filiere` est activé, sinon 1. m = multiplicateur de scénario (quotas) : evenement_quotas()
construit l'événement daté. Convention v1 (v2/sante/levers_v1.project_flow) : les entrées de l'année
origine + L_p sont encore au niveau de base ; m s'applique à partir de origine + L_p + 1.
"""
import numpy as np

from jumeau.history import SOURCE_RPPS, stock_flow_rates
from jumeau.module import Add, Module, Param, register
from jumeau.scenario import Event
from sante.pipeline import scale


def evenement_quotas(m: float, origin: int, lag: int, selector: dict | None = None, source: str = "") -> Event:
    """Quotas × m décidés à l'origine : effet sur les entrées à partir de origin + lag + 1 (convention v1)."""
    return Event("entrees.multiplicateur", origin + lag + 1, m, "set", selector=selector or {}, source=source)


def selecteur_region(region: str, cells, profession=None) -> dict:
    """Sélecteur d'événement pour une région (code Insee) : ses départements présents dans l'état (RPPS dep → région)."""
    import pandas as pd
    reg = pd.read_parquet("data/processed/stock.parquet", columns=["dep", "region"]).drop_duplicates()
    deps = sorted(set(reg.loc[reg.region == region, "dep"]) & set(cells.territory))
    if not deps:
        raise ValueError(f"région {region!r} : aucun département dans l'état")
    sel = {"territory": deps}
    if profession is not None:
        sel["profession"] = profession
    return sel


@register
class Entrees(Module):
    name = "entrees"
    order = 30
    params = (
        Param("flux", None, "personnes/an", SOURCE_RPPS, "fenêtre d'ajustement", "mesuré",
              "Entrées nettes annuelles par cellule × âge (moyenne de la fenêtre, ou des dernières années)."),
        Param("filiere", False, "booléen", "MESR SISE, inscrits par année d'étude (données ouvertes)", "rentrées 2017–2024", "mesuré",
              "Entrées proportionnelles à la cohorte en formation (CD, PH, spécialistes)."),
        Param("multiplicateur", 1.0, "× niveau actuel", "Loi OTSS 2019 ; arrêtés d'objectifs 2021 et 2026", "2026",
              "supposé", "Quotas : multiplie les entrées après le délai de formation. Par profession et par région "
              "via le sélecteur (selecteur_region). Plage DD76 : × [0,8 ; 1,2].", (0.0, 3.0), "former"),
    )

    def fit(self, hist):
        self.hist = hist

    def step(self, state, ctx):
        _, fitted, slope = stock_flow_rates(self.hist, state)
        inflow = ctx.param(self, "flux", base=fitted)
        k = 1.0
        if ctx.param(self, "filiere"):
            kp = {p: scale(p, ctx.origin, ctx.h)[-1] for p in state.cells["profession"].unique()}
            k = state.cells["profession"].map(kp).to_numpy(dtype=float)[:, None]
        m = ctx.param(self, "multiplicateur")
        if np.ndim(k) == 0 and inflow is fitted and not np.any(slope):   # entrées constantes : calculées une fois
            ekey = np.asarray(m, float).tobytes()
            ec = self.__dict__.setdefault("_amount", {})
            if ekey not in ec or ec[ekey][0] is not fitted:
                if len(ec) > 32:
                    ec.clear()
                a = k * (inflow + slope * ctx.h)
                ec[ekey] = (fitted, a * (np.reshape(m, (-1, 1)) if np.ndim(m) else m) if np.any(m != 1) else a)
            return [Add(self.name, ec[ekey][1], src="entrees")]
        amount = k * (inflow + slope * ctx.h)
        if np.any(m != 1):
            amount = amount * (np.reshape(m, (-1, 1)) if np.ndim(m) else m)
        return [Add(self.name, amount, src="entrees")]
