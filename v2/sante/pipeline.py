"""Training pipeline -> national cohort index of yearly entries, per profession.

Source (since 2026-11-15): MESR SISE open data, enrolments in odontology and pharmacy by year of study and
academic year (v2/data/processed/sise_sante.parquet, built by v2/data/build_sise.py, Licence Ouverte v2.0,
rentrées 2017-2024). It replaces the team-provided DREES file 990_drees_mmop2 (non-disclosure agreement), which
SISE reproduces exactly for years of study 2-5 (2020-2024, max gap 0 for dentists; one PH year-2 value differs
by 163). SISE's « BAC + 6 et plus » mixes year 6 with internship and theses, so year 6 is derived as year 5 of
the previous academic year (observed ratio in the 990 file: 0.86-1.07, median about 1.0).
A cohort in year of study k in academic year y is expected to start working in y + (last_k + 1 - k).
Each year-of-study series is divided by its own mean (removes attrition differences),
then the index for an entry year is the mean of the relative estimates available for it.

Clean cohorts only:
  dentistes    : DE DOCTEUR EN CHIRURGIE DENTAIRE years 2-6
  pharmaciens  : DE DOCTEUR EN PHARMACIE years 2-6
  specialistes : no open series by DES year (the 990 file gave DES MEDECINE year 4): index = None (phase 2)
Other professions have no pipeline data here: index = None.
"""
from functools import lru_cache

import pandas as pd

from pathlib import Path

SISE = Path(__file__).resolve().parents[1] / "data" / "processed" / "sise_sante.parquet"
SPEC = {  # profession -> (diploma, years of study used, last year of study)
    "dentistes": ("DE DOCTEUR EN CHIRURGIE DENTAIRE", [2, 3, 4, 5, 6], 6),
    "pharmaciens": ("DE DOCTEUR EN PHARMACIE", [2, 3, 4, 5, 6], 6),
}


@lru_cache
def enrolments() -> pd.DataFrame:
    """type_de_diplome, k, year, n : open SISE counts, year 6 derived as year 5 of the previous academic year."""
    s = pd.read_parquet(SISE)
    s = s[s.k.between(2, 5)]
    k6 = s[s.k == 5].assign(k=6, year=lambda x: x.year + 1)
    s = pd.concat([s, k6])
    dip = {p: d for p, (d, _, _) in SPEC.items()}
    return (s.assign(type_de_diplome=s.profession.map(dip))[["type_de_diplome", "k", "year", "n"]]
            .astype({"k": float, "year": float}).reset_index(drop=True))


@lru_cache
def cohort_index(profession: str) -> pd.Series | None:
    """entry year -> expected cohort size (students), or None if no pipeline data."""
    if profession not in SPEC:
        return None
    diploma, ks, last = SPEC[profession]
    e = enrolments()
    e = e[(e.type_de_diplome == diploma) & e.k.isin(ks) & (e.n > 0)]
    est = e.assign(entry=e.year + (last + 1 - e.k))
    est["rel"] = est.n / est.groupby("k").n.transform("mean")          # each year of study on its own scale
    return est.groupby("entry").rel.mean().rename("cohort")             # relative index (mean ~1)


def scale(profession: str, origin: int, horizon: int) -> list[float]:
    """Multiplier on yearly entries for origin+1..origin+horizon, relative to the origin's cohort.
    Reference = the origin cohort, or the first known cohort after it. Years past the last known cohort hold
    the last known ratio; no data -> 1.0."""
    c = cohort_index(profession)
    if c is None or c.index.max() <= origin:
        return [1.0] * horizon
    ref = c[origin] if origin in c.index else c[c.index > origin].iloc[0]   # first known cohort after origin
    out, last = [], 1.0
    for h in range(1, horizon + 1):
        y = origin + h
        last = c[y] / ref if y in c.index else last
        out.append(float(last))
    return out
