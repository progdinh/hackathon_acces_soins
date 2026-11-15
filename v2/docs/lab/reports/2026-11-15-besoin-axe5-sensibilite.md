---
type: analysis
date: 2026-11-15
author: session besoin-axe5-sensibilite
question: "L'effet d'une politique sur l'indice de couverture C(p, T, 2050) se distingue-t-il de la dispersion due au choix du modèle de besoin ?"
headline: "Ratio national R = effet de quotas × 1,2 / étendue entre estimateurs, en 2050 : SF 1,91, CD 40, PH 1,14 (distinguables), MK 0,77, IDE 0,34 (non distinguables) ; règle d'affichage en fourchette déclenchée pour MK et IDE. L'étendue vient presque toute de M0 (sans M0 : ≤ 0,004 en log). Les tirages de l'offre C1 portent 52 à 92 % de la variance de log C"
status: done
professions: [sages-femmes, dentistes, pharmaciens, kines, infirmiers]
hypothesis: "H-S5 : pour au moins une profession, le choix du modèle de besoin déplace C(2050) plus que la politique de référence (R < 1)"
sources: [protocole gelé 2026-11-15-besoin-axe5-sensibilite (SHA-256 10a5b285…cd87834, FreeTSA 05:28:15 UTC), jumeau servi (prototype.server.Model, C1), tirages C1 (methodes.cohortes), Insee Omphale 2022, estimateurs M0 M1 M2a M3 (v2/besoin), L23 (P-B6, fiche param-besoin-l23-vaccination)]
tags: [besoin, axe5, sensibilite, couverture, 2050]
---

> **Erratum 2026-11-15 (P1-4, double compte de L23).** La grille appelait `l23(2019, …)` et rejouait toute la courbe
> de 2019. Elle appelle maintenant `l23(2026, …)` : seule la part au-delà de celle atteinte en 2026 agit (commit
> b35a380, rapport [L23, marge](2026-11-15-l23-p1-4-marge.md)). La grille des pharmaciens a été relancée ; les quatre
> autres professions ne dépendent pas de L23 et ne changent pas. Nouveaux chiffres, pharmaciens, France (mesurés) :
> - L23 en 2050 : E = 0,0002 et R = 0,002, au lieu de 0,004 et 0,05 ;
> - L23 en 2035 : E = 0,0002 et R = 0,004, au lieu de 0,004 et 0,08 ;
> - étendue P5–P95 due aux paramètres de transfert : 0,0005 au lieu de 0,006.
>
> Le verdict ne change pas (non distinguable), et les autres politiques non plus (quotas × 1,2 : R = 1,14). Les
> anciens chiffres restent ci-dessous, annotés « dépassé ».

# Axe 5 du besoin — sensibilité de l'indice de couverture C(p, T, 2050)

> **Headline :**
> - **Ratio R = effet de quotas × 1,2 / étendue de log C entre estimateurs survivants**, France, 2050 (m) :
>   SF **1,91**, CD **40**, PH **1,14** : distinguables ; MK **0,77**, IDE **0,34** : **non distinguables**.
> - **La règle d'affichage se déclenche pour les kinés et les infirmiers** : C en fourchette entre estimateurs,
>   jamais un seul chiffre.
> - *Mise à jour du 2026-11-15 (après résultat, décision de l'utilisateur·rice) : M0, réfuté par P-B1, est retiré
>   de la fourchette affichée. C est servi par M1 (M3 pour les IDE) ; l'écart M0 → M1 est montré comme l'effet du
>   vieillissement ; l'incertitude affichée est la bande de l'offre C1. Le verdict gelé ci-dessus ne change pas.*
> - **Cette étendue tient presque toute à M0** (besoin ∝ population, sans âge). Entre M1, M2a et M3, elle vaut au
>   plus 0,004 en log (m). Or P-B1 a déjà retenu l'âge pour les cinq professions.
> - **La première source de variance est l'offre** : les tirages de C1 portent 52 à 92 % de la variance de log C
>   au national (m). Viennent ensuite la politique (CD 0,43, MK 0,15) ou l'estimateur (IDE 0,18).

Provenance : (m) mesuré sur la grille ; (s) sourcé ; (d) dérivé ; (h) supposé. Protocole gelé avant tout calcul de
B ou de C : [`2026-11-15-besoin-axe5-sensibilite.md`](../../../validation/preregistered/2026-11-15-besoin-axe5-sensibilite.md),
jetons RFC 3161 FreeTSA 05:28:15 UTC et DigiCert 05:28:16 UTC (accord de l'utilisateur·rice : « Oui, horodater »),
OpenTimestamps soumis. Aucun seuil n'a été changé.

## Question
Le plan du besoin ([axe 5](../derivations/2026-11-15-besoin-plan.md)) demande si l'effet d'une politique sur C se
lit au-delà de la dispersion due au choix du modèle de besoin. C'est le pendant, côté besoin, du ratio « décision /
connaissance » de l'[axe 5 de l'offre](2026-11-14-axe5-sensibilite.md). Seuil gelé : R < 1 ⇒ « non distinguable ».

## Result

### Ratio politique / choix du modèle, France, 2050 (m)

`Y = log C`. E = |Y(politique) − Y(statu quo)| ; D = max − min de Y entre estimateurs survivants. Point de
référence : estimateur servi (M1 ; M3 pour les IDE), Omphale central, offre moyenne de C1.

| Profession | Estimateurs | C 2050 (statu quo) par estimateur | D (log) | E quotas × 1,2 | **R quotas × 1,2** | Départements R ≥ 1 | Meilleur levier : R | D sans M0 |
|---|---|---|---|---|---|---|---|---|
| Sages-femmes | M0, M1, M2a | 1,46 / 1,54 / 1,54 | 0,054 | 0,103 | **1,91** distinguable | 93 % | quotas × 0,8 : 2,13 | 0,000 |
| Dentistes | M0, M1, M2a | 1,405 / 1,404 / 1,408 | 0,003 | 0,114 | **40,4** distinguable | 100 % | étrangers × 2 : 120 | 0,003 |
| Pharmaciens | M0, M1 | 1,11 / 1,01 | 0,096 | 0,108 | **1,14** distinguable | 63 % | quotas × 0,8 : 1,27 | — |
| Kinés | M0, M1, M2a | 1,54 / 1,34 / 1,34 | 0,142 | 0,109 | **0,77** non distinguable | 5 % | étrangers × 2 : 1,73 | 0,001 |
| Infirmiers | M0, M1, M2a, M3 | 1,14 / 0,83 / 0,83 / 0,83 | 0,321 | 0,110 | **0,34** non distinguable | 0 % (100 dép.) | quotas × 0,8 : 0,38 | 0,004 |

- **Autres leviers en 2050, R national (m).**
  - Report de la retraite + 2 ans : de 0,16 (IDE) à 0,59 (SF) ; CD 10,6.
  - Départs précoces × 0,5 ou × 1,5 : de 0,03 (IDE) à 0,78 (SF) ; CD 24–28.
  - Diplômés étrangers × 2 : MK 1,73, SF 0,75, PH 0,59, IDE 0,05 ; CD 120.
  - Cumul emploi-retraite × 0,5 ou × 2 : ≤ 0,01, sauf CD (0,33–0,72).
  - **L23** (vaccination en officine, PH) : ~~E = 0,004, **R = 0,05**~~ (dépassé, erratum P1-4 : E = 0,0002, R = 0,002) ; aucun département distinguable.
  - Régulation à l'installation : E = 0 au national **et** au département (voir ⚑).
- **En 2035** (m) : D = 0,012 (SF), 0,004 (CD), 0,056 (PH), 0,064 (MK), 0,142 (IDE). Rapporté seulement :
  `out/resultats.json`.
- **Au département** (101 ; IDE 100) : D médian 0,006 (CD) à 0,337 (IDE), P10–P90 dans `out/resultats.json` ;
  R par département dans [`out/ratio_dep.csv`](../../../sensibilite/besoin/out/ratio_dep.csv).

### Décomposition de la variance de log C(2050), France (m)

Effets principaux sur la grille complète politique × estimateur × Omphale × 100 tirages C1 (× 40 tirages de
transfert pour les PH), niveaux équiprobables.

| Profession | Politique S_π | Estimateur S_e | Omphale S_ω | Offre (C1) S_k | Transfert S_j | Interactions |
|---|---|---|---|---|---|---|
| Sages-femmes | 0,04 | 0,01 | 0,03 | **0,92** | — | 0,00 |
| Dentistes | **0,43** | 0,00 | 0,05 | **0,52** | — | 0,00 |
| Pharmaciens | 0,05 | 0,03 | 0,04 | **0,88** | 0,000 | 0,00 |
| Kinés | 0,15 | 0,06 | 0,05 | **0,74** | — | 0,00 |
| Infirmiers | 0,02 | **0,18** | 0,06 | **0,74** | — | 0,00 |

- **Au département**, les médianes suivent le national (`out/variance_dep.csv`) : S_k de 0,65 (CD) à 0,96 (SF),
  S_e de 0,00 (CD) à 0,16 (IDE ; P10–P90 0,12–0,21).
- **Interactions ≈ 0** : au log, l'effet d'un levier sur l'offre et celui de l'estimateur sur le besoin
  s'additionnent exactement (d). C = [S/B](2050) / [S/B](2026), le levier ne touche que S, l'estimateur que B.
- **Échelles de comparaison**, France, 2050, en log (m) :

  | | SF | CD | PH | MK | IDE |
  |---|---|---|---|---|---|
  | Étendue Omphale | 0,11 | 0,11 | 0,13 | 0,15 | 0,22 |
  | Offre, P5–P95 des tirages C1 | 0,83 | 0,45 | 0,78 | 0,74 | 0,99 |
  | Transfert L23, P5–P95 | — | — | ~~0,006~~ 0,0005 (erratum P1-4) | — | — |

  À l'aune de l'offre, aucun levier n'est distinguable : la bande P5–P95 de C1 vaut 4 à 9 fois l'effet de quotas
  × 1,2.

### Règle d'affichage (gelée)
Déclenchée si, au national en 2050, R(quotas × 1,2) < 1 ou S_e > S_π :
- **kinés** (R 0,77) et **infirmiers** (R 0,34 ; S_e 0,18 > S_π 0,02) : **déclenchée** ;
- SF, CD, PH : non déclenchée.

## How
- **Data :** offre du modèle servi (`prototype.server.Model`, C1, composition LEVIERS) ; tirages C1 du registre de
  méthodes (`axe2_cohortes_c1`, privé, origine 2026 ; IDE libéraux 2023) ; Omphale 2022 (central, bas, haut) ;
  estimateurs de `v2/besoin/estimateurs/` sans modification.
- **Method :** [`grille.py`](../../../sensibilite/besoin/grille.py) calcule Y[π, e, ω, k, j, T, t] (~80 s de
  machine pour les 5 professions, mesuré) ; [`stats.py`](../../../sensibilite/besoin/stats.py) applique les
  statistiques gelées. Graine 20261115.
- **Run :** `PYTHONPATH=v2 uv run --with scipy python -W ignore -m sensibilite.besoin.grille && PYTHONPATH=v2 uv run python -m sensibilite.besoin.stats`.
  Les grilles `.npz` (~70 Mo) restent hors dépôt ; les sorties `json` et `csv` sont commitées.
- **Écarts au protocole :** aucun sur les seuils et les statistiques. Le jumeau sert 100 départements IDE (pas
  101) : un département où la population existe mais pas l'offre est retiré par `logC` (détail de code, pas de
  choix).

## ⚑ What could make it wrong
- **D, c'est la question de l'âge.** Sans M0, l'étendue entre M1, M2a et M3 vaut 0,000 à 0,004 en log, et R
  dépasse 25 partout. M0 figure dans l'ensemble gelé (consigne et rapport d'étape : « cas limite »), mais P-B1 a
  retenu l'âge contre lui pour les cinq professions. Le verdict « non distinguable » des MK et des IDE revient donc
  à dire : l'effet des quotas est plus petit que l'effet du vieillissement sur le besoin. Ce n'est pas une
  incertitude entre modèles plausibles.
- **M2a ≡ M1 au département par construction** (d) : M2a = r̄ · B₁ · M^γ avec M figé à 2024, donc M^γ s'annule
  dans l'indexation. Il n'ajoute rien à D (écart national ≤ 0,004, dû aux poids départementaux). M3 est presque
  confondu avec M1 (prévalences figées, profil d'âge voisin).
- **Séparabilité de l'offre supposée (h)** : le tirage C1 est appliqué en écart relatif à chaque trajectoire de
  politique. Le test prévu (un tirage rejoué avec le levier dans la méthode) n'est pas fait : voir le ledger.
- **La bande C1 domine, et sa couverture est imparfaite** : 73,5 % à 80 % à h = 5 (décision du 2026-11-15
  « C1 : ni prévision conforme ni réconciliation MinT »), extrapolée ici à h = 24. Les parts S_k dépendent de cette
  extrapolation.
- **Régulation : E = 0 au département**, alors qu'elle redistribue entre territoires dans l'axe 5 de l'offre. Soit
  le modèle servi ne la déclenche pas dans ce chemin, soit l'effet reste sous le département (communes, secteur
  « bloques »). Non vérifié : voir le ledger.
- **L23** repose sur `a` et `k` supposés ; même aux bornes hautes (a = 0,02, k = 1), sa P5–P95 reste à ~~0,006~~ 0,0005 (erratum P1-4) en
  log. Le verdict « L23 non distinguable » tient à la petitesse de `a` en temps de MG, qui reste supposée.
- **IDE** : tirages C1 sur les libéraux (origine 2023), offre servie sur le périmètre du modèle servi.
- **Capacité de formation et abandon IFSI** ne sont pas joués (absents du modèle servi).

## → What it changes
- **Affichage de C** : ~~fourchette entre estimateurs pour les kinés et les infirmiers~~ (règle gelée, remplacée le
  2026-11-15 pour l'affichage). M0 est retiré de la fourchette : C est servi par M1 (M3 pour les IDE), l'écart
  M0 → M1 est montré comme l'effet du vieillissement (IDE 2050 : 0,83 avec l'âge, 1,14 sans ; quotas × 1,2 : +11 %),
  et l'incertitude affichée est la bande de l'offre C1. Décisions au [registre](../decisions.md), 2026-11-15.
- **Branchement dans la carte** ([plan](../derivations/2026-11-15-besoin-carte-plan.md)) : C par l'estimateur servi,
  avec la bande de l'offre et, à côté, l'effet du vieillissement (M0 → M1).
- **Priorité de recherche** : la largeur de C vient de l'offre (C1), pas du besoin. Resserrer la bande de C1 (choc
  commun national, décision du 2026-11-15) vaut plus que tout raffinement de M1–M3.
- [`Home.md`](../../../../Home.md) (journal, Status) et [`README.md`](../../../../README.md) mis à jour.

## ? Next
| Item | Cost |
|---|---|
| Tester la séparabilité : 10 tirages C1 rejoués avec quotas × 1,2 dans la méthode | ~20 min Claude, ~2 min machine |
| Régulation à E = 0 au département : vérifier le déclenchement dans `Model.scenario` | ~15 min Claude |
| Sensibilité de l'indice M4 (accessibilité, à part) aux leviers, à la commune | ~45 min Claude, offre communale requise |
