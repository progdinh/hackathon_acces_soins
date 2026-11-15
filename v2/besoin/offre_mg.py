"""Offre de médecine générale lue en entrée (décision O3 du 2026-11-15, qui remplace O2).

Le jumeau ne projette pas la médecine générale : elle est modélisée ailleurs (DGOS, programme Junior ; DREES, modèle
Hippocrate). Le projet prolonge ce travail aux cinq autres professions et le relie par les transferts de tâches. Pour
lire l'effet d'un transfert chez la source, on prend donc l'offre MG comme une **donnée d'entrée**, jamais calculée ici.

Trois fournisseurs, du plus pauvre au plus riche ; chacun déclare son statut :
  constante     S_MG(T, t) = S_MG(T, 2026), RPPS (DREES), généralistes libéraux et mixtes.          statut : supposé
  nationale     S_MG(T, t) = S_MG(T, 2026) · I(t) / I(2026), I = trajectoire nationale publiée (fichier
                MG_NATIONALE, colonnes year, effectif, source) ; la répartition entre territoires est figée
                à 2026.                                                                             statut : supposé
                (répartition) ; sourcé (trajectoire)
  externe       table territoire × année fournie par le porteur (DGOS / Junior), lue depuis le chemin de la
                variable d'environnement BESOIN_MG_OFFRE (colonnes dep, year, effectif). Le fichier reste hors
                du dépôt : il peut être sous accord.                                                  statut : sourcé

Sortie : Cube à une profession (« medecine-generale »), au département, en ETP (= effectif × activité).
"""
import os
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from besoin.couverture import ACTIVITE
from besoin.cube import Cube

STOCK = "data/processed/stock.parquet"                     # DREES, RPPS 2012–2026, dep × âge × sexe × mode
MG_NATIONALE = "v2/besoin/donnees/mg_projection_nationale.csv"
REF = 2026
MG = "medecine-generale"


@lru_cache(maxsize=1)
def stock_mg(year: int = REF) -> pd.Series:
    """Généralistes libéraux et mixtes par département, RPPS (DREES), année `year`."""
    d = pd.read_parquet(STOCK, columns=["profession", "specialty", "mode3", "year", "dep", "n"])
    d = d[(d.profession == "medecins") & (d.specialty == "Médecine générale") & (d.mode3 == "liberal_mixte")
          & (d.year == year) & (d.dep != "999")]
    s = d.groupby("dep").n.sum()
    if s.empty:
        raise ValueError(f"aucun généraliste libéral dans {STOCK} pour {year}")
    return s


def _cube(table: pd.DataFrame, territories, years, activite: float) -> Cube:
    """table : index dep, colonnes années (effectifs)."""
    t = table.reindex(index=list(territories), columns=list(years))
    if t.isna().any().any():
        manq = t.index[t.isna().any(axis=1)].tolist()
        raise ValueError(f"offre MG absente pour {len(manq)} territoires, ex. {manq[:5]}")
    return Cube(np.array([MG]), np.asarray(territories), np.asarray(years),
                t.to_numpy(float)[None] * activite, "dep", "ETP")


class OffreMG:
    name = ""
    statut = ""
    source = ""

    def cube(self, territories, years, activite: float | None = None) -> Cube:
        raise NotImplementedError

    def info(self) -> dict:
        return dict(fournisseur=self.name, statut=self.statut, source=self.source)


class Constante(OffreMG):
    name = "constante"
    statut = "supposé"
    source = "DREES, RPPS 2026 (généralistes libéraux et mixtes), tenu constant : aucune projection"

    def cube(self, territories, years, activite=None):
        s = stock_mg()
        q = ACTIVITE.value if activite is None else activite
        return _cube(pd.DataFrame({y: s for y in years}), territories, years, q)


class Nationale(OffreMG):
    name = "nationale"
    statut = "supposé (répartition figée à 2026) ; sourcé (trajectoire nationale)"

    def __init__(self, path: str = MG_NATIONALE):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"{path} absent : déposer la trajectoire nationale publiée (year, effectif, source)")
        self.traj = pd.read_csv(self.path)
        self.source = "; ".join(sorted(self.traj.source.astype(str).unique())) + " ; répartition RPPS 2026"

    def cube(self, territories, years, activite=None):
        i = self.traj.set_index("year").effectif.astype(float)
        if REF not in i.index or not set(years) <= set(i.index):
            i = i.reindex(range(int(i.index.min()), int(i.index.max()) + 1)).interpolate()
        manq = [y for y in years if y not in i.index]
        if manq or REF not in i.index:
            raise ValueError(f"trajectoire nationale MG sans les années {manq or [REF]}")
        s = stock_mg()
        q = ACTIVITE.value if activite is None else activite
        return _cube(pd.DataFrame({y: s * (i[y] / i[REF]) for y in years}), territories, years, q)


class Externe(OffreMG):
    name = "externe"
    statut = "sourcé (fichier du porteur)"

    def __init__(self, path: str | None = None):
        path = path or os.environ.get("BESOIN_MG_OFFRE")
        if not path or not Path(path).exists():
            raise FileNotFoundError("offre MG externe : définir BESOIN_MG_OFFRE (fichier dep, year, effectif)")
        self.path = Path(path)
        self.source = f"fichier du porteur ({self.path.name}), hors dépôt"

    def cube(self, territories, years, activite=None):
        t = pd.read_csv(self.path, dtype={"dep": str}).pivot_table(index="dep", columns="year", values="effectif",
                                                                    aggfunc="sum")
        q = ACTIVITE.value if activite is None else activite
        return _cube(t, territories, years, q)


FOURNISSEURS = {"constante": Constante, "nationale": Nationale, "externe": Externe}


def fournisseur(name: str = "constante") -> OffreMG:
    if name not in FOURNISSEURS:
        raise ValueError(f"offre MG {name!r} inconnue ({sorted(FOURNISSEURS)})")
    return FOURNISSEURS[name]()
