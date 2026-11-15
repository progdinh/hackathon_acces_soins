"""Manifeste des données traitées commitées (data/processed/ et v2/data/processed/) et garde-fou.

Run (racine du dépôt) :
    uv run python v2/data/manifest.py           # réécrit MANIFEST.md dans les deux dossiers
    uv run python v2/data/manifest.py --check   # échoue si un fichier a changé sans manifeste, ou si un script
                                                # de construction lit un fichier des organisateurs

Les fichiers traités sont commités (décision du 2026-11-14) pour éviter de retélécharger ~3,6 Go de données brutes.
Ils ne viennent que de données ouvertes. Les fichiers fournis par les organisateurs (inscrits par université, sous
accord de confidentialité) ne doivent jamais entrer dans un fichier traité : le contrôle le vérifie sur le code.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIRS = [ROOT / "data" / "processed", ROOT / "v2" / "data" / "processed"]
# noms des fichiers des organisateurs (data/raw/, non commités) : aucun script de construction ni aucun code
# exécuté par le jumeau, la carte, l'assistant ou l'analyse de sensibilité ne doit les lire (contrôle étendu le
# 2026-11-15, après le passage du vivier CD/PH du fichier 990 à SISE)
INTERDITS = ["990_drees_mmop2", "Base inscrits", "Données médecine", "Données odontologie", "Données pharma",
             "Medicale Junior", "pipeline"]
# code du dépôt (outil, bancs, validation, construction) : contrôlé ligne à ligne
EXECUTE = ["v2/jumeau", "v2/sante", "v2/prototype", "v2/prototype-carte", "v2/sensibilite", "v2/agent", "v2/langage",
           "v2/methodes", "v2/validation", "v2/data", "chatbot/passerelle", "chatbot/chat"]
# fichier -> (script qui l'écrit, commande, source et millésime)
V1 = ("v2/sante/load.py", "PYTHONPATH=v2 uv run python -m sante.load",
      "DREES RPPS 2012–2026 par profession (dép × âge × sexe × mode) ; Insee Omphale 2022, 3 scénarios")
B = {
    "checks.csv": V1, "population.parquet": V1, "stock.parquet": V1,
    "stock_ameli.parquet": ("v2/sante/ameli.py", "PYTHONPATH=v2 uv run python -m sante.ameli",
                            "data.ameli.fr, démographie des professionnels libéraux (modifié le 2026-10-28)"),
    "stock_commune.parquet": ("v2/sante/cartosante.py", "PYTHONPATH=v2 uv run python -m sante.cartosante",
                              "CartoSanté (Atlasanté), effectifs libéraux par commune × âge, 2004–2025"),
    "stock_nurses_salaried.parquet": ("v2/sante/nurses.py", "PYTHONPATH=v2 uv run python -m sante.nurses",
                                      "DREES, infirmiers salariés (BTS), 2023, ratissés dép × âge × sexe"),
}
for f, s in {
    "build_secteur.py": ["secteur_checks.csv", "secteur_finess_shares.csv", "secteur_split.parquet", "secteur_stock.parquet"],
    "build_annuaire.py": ["annuaire_checks.csv", "annuaire_commune.parquet"],
    "build_commune.py": ["annuaire_checks_dep.csv", "commune_checks.csv", "commune_geo.parquet", "commune_stock.parquet",
                         "grain_bruit.csv", "grain_petits_effectifs.csv"],
    "build_attributs.py": ["commune_attributs.parquet", "commune_attributs_checks.csv"],
    "build_finess_histo.py": ["finess_commune_annee.parquet", "finess_histo_checks.csv", "officines_flux_commune.parquet"],
    "build_flux.py": ["flux_checks.csv", "flux_installations_commune.parquet"],
    "build_infirmiers.py": ["infirmiers_secteur_age_sexe.parquet", "infirmiers_test_hind.csv"],
    "build_passage.py": ["passage_commune.parquet", "petits_effectifs.parquet", "petits_effectifs_classes.csv"],
    "build_pharmaciens.py": ["pharmaciens_checks.csv", "pharmaciens_checks_dep.csv", "pharmaciens_commune_annee.parquet"],
    "build_zonage.py": ["zonage_commune.parquet"],
    "build_sise.py": ["sise_sante.parquet", "sise_sante_region.parquet"],
}.items():
    for x in s:
        B[x] = (f"v2/data/{f}", f"uv run python v2/data/{f}", "voir l'en-tête du script (sources et millésimes)")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def commit(path: str) -> str:
    r = subprocess.run(["git", "log", "-1", "--format=%h %ad", "--date=short", "--", path],
                       capture_output=True, text=True, cwd=ROOT)
    return r.stdout.strip() or "non commité"


def lignes(d: Path) -> list[tuple]:
    return [(p.name, p.stat().st_size, sha(p)) for p in sorted(d.iterdir()) if p.is_file() and p.name != "MANIFEST.md"]


def ecrire():
    for d in DIRS:
        out = [f"# Manifeste — `{d.relative_to(ROOT)}`", "",
               "Généré par `uv run python v2/data/manifest.py` ; contrôlé par `--check`. Données ouvertes seulement.",
               "Reconstruire un fichier : lancer sa commande depuis la racine, après avoir placé les données brutes dans",
               "`data/raw/` ou `v2/data/raw/` (voir le README).", "",
               "| Fichier | Octets | SHA-256 (16) | Script | Dernier changement du script | Commande | Source |",
               "|---|---:|---|---|---|---|---|"]
        for name, size, h in lignes(d):
            s, cmd, src = B.get(name, ("?", "?", "?"))
            n = f"{size:,}".replace(",", " ")
            out.append(f"| `{name}` | {n} | `{h}` | `{s}` | {commit(s) if s != '?' else '?'} | `{cmd}` | {src} |")
        (d / "MANIFEST.md").write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"{d.relative_to(ROOT)}/MANIFEST.md : {len(out) - 8} fichiers")


def verifier() -> int:
    err = []
    for d in DIRS:
        m = (d / "MANIFEST.md").read_text(encoding="utf-8") if (d / "MANIFEST.md").exists() else ""
        for name, _, h in lignes(d):
            if name not in B:
                err.append(f"{name} : aucun script de construction déclaré")
            if f"`{name}`" not in m or f"`{h}`" not in m:
                err.append(f"{d.relative_to(ROOT)}/{name} : absent du manifeste ou contenu changé (relancer manifest.py)")
    for s in {v[0] for v in B.values()}:
        t = (ROOT / s).read_text(encoding="utf-8")
        err += [f"{s} lit un fichier des organisateurs ({x})" for x in INTERDITS if x in t]
    lecture = re.compile(r"(read_\w+|open|Path)\([^)\n]*(" + "|".join(map(re.escape, INTERDITS)) + ")")
    for d in EXECUTE:
        for p in sorted((ROOT / d).rglob("*.py")):
            for i, ligne in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if lecture.search(ligne):
                    err.append(f"{p.relative_to(ROOT)}:{i} lit un fichier des organisateurs à l'exécution")
    print("\n".join(err) or "OK : manifestes à jour, aucun fichier des organisateurs dans la construction")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(verifier() if "--check" in sys.argv else (ecrire() or 0))
