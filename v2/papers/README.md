# Prétirages v2 (format arXiv)

Chaque axe de recherche produit un prétirage : `v2/papers/axeN-<sujet>/main.tex` (+ `refs.bib`, `figures/`).

- Partir de `template/` : copier `main.tex` et `refs.bib` dans le dossier de l'axe. Le préambule commun
  (`template/preamble.tex`) est inclus et n'est pas modifié par un axe.
- Source TeX autonome, compilable en pdfLaTeX : c'est ce qu'arXiv attend. Pas de dépendance hors TeX Live.
- Langue : français. Pas de résumé anglais ni de mention « prétirage » ou « non relu par des pairs » : c'est un récapitulatif scientifique complet de ce qui a été fait, dans la forme d'un article (2026-11-14).
- Chaque nombre porte sa provenance : `\mesure`, `\derive` ou `\suppose`, et vient d'un rapport de `v2/docs/lab/reports/`.
- Seules les références lues et vérifiées entrent dans `refs.bib`. Aucune citation inventée.
- Compilation : `tectonic main.tex` ou `latexmk -pdf main.tex` (aucun moteur TeX n'est installé sur cette machine
  au 2026-11-14 : `brew install tectonic`, à valider).

## Documents d'entrée (2026-11-15)
- **Rapport technique** `rapport-technique/` : document d'entrée unique pour la reprise ; il résume chaque axe et,
  depuis le 2026-11-15, le module de besoin (`ch-besoin.tex`).
- **Article sur le besoin** `besoin/` : version complète et à jour (erratum P1-4 compris), PDF commité.
- **`note-besoin/`** : remplacé par `besoin/` le 2026-11-15 (version antérieure, sans l'erratum P1-4). Conservé, non
  mis à jour.
