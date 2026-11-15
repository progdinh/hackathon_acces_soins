---
type: decisions
aliases: [Décisions v2]
---

# Décisions — v2 (jumeau numérique de l'offre de soins)

Chaque choix fait, inversé ou rejeté, avec son *pourquoi*. Format :
**Décision** / **Pourquoi** / **Ce qui le renverserait**. On remplace,
on n'efface jamais.

- Les entrées du 2026-11-14 ci-dessous sont copiées de la v1
  (`../../../docs/lab/decisions.md`), où elles restent aussi.
- Les décisions v1 antérieures restent valables tant qu'une entrée ici ne
  les remplace pas.

## 2026-11-14 — Recadrage en recherche : jumeau numérique des professions « libérales »

**Décision.**
- **Objectif.** Simuler des politiques publiques nationales, chacune
  exprimée comme un réglage d'hyperparamètres sourcés, et mesurer leur effet
  sur l'effectif « libéral » à une date future t.
  - Les hyperparamètres viennent d'Omphale, d'Hippocrate et du Dossier DREES
    n°76, plus des spécificités par profession : régulation de
    l'installation, filières en pharmacie, spécialisation en odontologie,
    abandon en études infirmières.
  - Les effectifs couvrent les sages-femmes, les chirurgiens-dentistes, les
    pharmaciens, les masseurs-kinésithérapeutes et les infirmiers.
- **Phase 2** : cardiologie, dermatologie, ophtalmologie (appui : rapport
  HCAAM sur les dépassements d'honoraires).
- **Démarche.** Mode de recherche quantitative : reproductible,
  falsifiable, interprétable, sans boîte noire. Code en briques (plug-ins
  par flux).
- **Feuille de route et axes de recherche** : [ROADMAP.md](../../ROADMAP.md).

**Pourquoi.** L'utilisateur·rice, 2026-11-14.
**Ce qui le renverserait.** Un nouveau cadrage du jury ou de l'équipe.

## 2026-11-14 — « Libéral » = secteur privé, lucratif ou non (tout employeur public exclu)

**Décision.**
- Une personne compte comme « libérale » si elle n'exerce pas chez un
  employeur public.
  - **Inclus :** libéraux et mixtes, pharmaciens adjoints salariés
    d'officine, salariés de cliniques privées et d'établissements privés
    non lucratifs, industrie, laboratoires privés.
  - **Exclus :** hôpital public, PMI, Éducation nationale, EHPAD publics,
    centres de santé municipaux, et tout autre employeur public.
- Dans le code, le nom est explicite (`prive`, hors public). Dans les
  textes, on rappelle la définition, car les sources (RPPS, ameli)
  emploient « libéral » au sens d'exercice indépendant.

**Pourquoi.** L'utilisateur·rice, 2026-11-14. Le second point (autres
employeurs publics exclus, industrie incluse) a été choisi parmi des options
proposées.

**Conséquence mesurée.** Effectifs de la dernière année, ancienne
définition (libéral + mixte) → nouvelle. Le minimum compte zéro salarié
hospitalier privé ; le maximum les compte tous :
| Profession | Ancienne | Minimum | Maximum |
|---|---|---|---|
| Pharmaciens 2026 | 27 294 | 65 344 | 75 335 |
| Sages-femmes 2026 | 9 615 | 12 475 | 26 428 |
| Kinés 2026 | 92 836 | 98 348 | 111 237 |
| Dentistes 2026 | 40 083 | 48 143 | 48 690 |
- Le RPPS de la DREES ne sépare pas le public du privé dans « salarié
  hospitalier ».
- « Autre salarié » mélange aussi des employeurs publics (PMI…) et
  privés.

Il manque donc une donnée (voir le ledger). Les résultats K1 et
« entrées par la filière » sont **mesurés sur l'ancien périmètre**.

**Ce qui le renverserait.** Aucune source ouverte ne permettant de séparer
public et privé. Dans ce cas, la sortie serait donnée sous forme de
fourchette, ou la définition révisée.

## 2026-11-14 — Les modèles tournent à toutes les granularités, jusqu'à la commune ; horizon de référence 2050

**Décision.**
- **Granularité.** Les modèles s'appliquent à chaque niveau : commune,
  groupes de communes, département, région, national.
  - La régulation de l'installation est une **liste de géocodes** par
    profession : zones où l'installation est limitée au remplacement d'un
    départ, et zones où l'exercice est obligatoire.
  - Une même profession peut relever des deux statuts selon la zone
    (kinés).
  - Le DG de l'ARS doit avoir la visibilité maximale.
- **Horizon de référence : 2050.**

**Pourquoi.** L'utilisateur·rice, 2026-11-14.
**Conséquences.**
- 2050 = 24 ans après 2026. Avec des données de 2012 à 2026, un backtest
  ne couvre qu'environ 10 ans, donc **aucune précision ne peut être annoncée
  à 2050**. On peut seulement reproduire le tendanciel de la DREES à 2050
  (Dossier n°76) et vérifier les cas limites.
- À 24 ans, l'horizon dépasse toutes les durées de formation : les quotas
  deviennent des leviers de premier ordre.
- À l'échelle de la commune, le bruit sur les petits effectifs (environ
  ±45 % pour N = 5, dérivé) se cumule sur l'horizon.

**Ferme** deux points de « En attente » : « Demo horizon » et « Projection
grain ».

## 2026-11-14 — Les nouveaux modèles ne sont pas tenus d'être des stock-flux

**Décision.**
- Le stock-flux (H1) est le **modèle de départ à battre**, pas la méthode
  imposée.
- Toute méthode peut entrer sur le banc si elle remplit trois conditions :
  - elle est interprétable, sans boîte noire ;
  - chaque levier y modifie un paramètre nommé et sourcé ;
  - elle respecte le contrat des modules.

  Par exemple : microsimulation, modèles bayésiens hiérarchiques ou
  espace-état, choix discret de l'installation, dynamique des systèmes,
  GAM, modèles spatiaux.
- C'est l'axe 2 de [ROADMAP.md](../../ROADMAP.md).

**Pourquoi.** L'utilisateur·rice, 2026-11-14.
**Ce qui le renverserait.** Aucun.

## 2026-11-14 — L'axe 0 est le jumeau numérique de l'offre de soins en France

**Décision.**
- Le socle commun qui relie les axes de recherche est un **jumeau numérique
  de l'offre de soins**. Il comprend trois composants :
  1. un **état unique** : N[profession, secteur, âge, sexe, commune, t],
     plus le vivier en formation ;
  2. des **modules de flux** en plug-ins, chacun avec ses paramètres
     sourcés ;
  3. des **scénarios** : jeux d'hyperparamètres et d'événements datés. Une
     politique publique est un scénario.
- Les axes 1 à 5 s'y branchent.
- L'état comprend le **secteur public**. C'est dérivé : un entrant bloqué
  par la régulation, ou une transition privé ↔ public, doit avoir où aller
  pour que les effectifs se conservent. La sortie étudiée reste le
  « libéral » (privé).

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « le liant de l'axe 0 c'est
un jumeau numérique de l'offre de soins en France ».
**Ce qui le renverserait.** Le secteur public ne pouvant pas être estimé à
la commune. Dans ce cas, il serait tenu à une échelle plus grossière et
ventilé.

## 2026-11-14 — Axe 5 adopté ; ordre de travail et format des fiches

**Décision.**
- **L'axe 5 est adopté** : analyse de sensibilité (Morris, puis Sobol) et
  incertitude à 2050.
- **Ordre de travail.**
  - Les axes 0, 1, 3 et 4 démarrent tout de suite, en parallèle :
    - axe 0 : le jumeau, en code ;
    - axe 1 : fiches de paramètres ;
    - axe 3 : protocoles de validation ;
    - axe 4 : données, avec en tête la séparation public / privé.
  - Les axes 2 et 5 démarrent quand le contrat du jumeau (axe 0) tourne.
    Ils ont besoin de son interface.
- **Format commun des fiches** (axes 1 et 4) : `docs/lab/fiches/<id>.md`,
  avec un frontmatter qui contient :
  - `parametre`, `profession`, `module` (le flux du jumeau visé) ;
  - `valeur`, `unite`, `incertitude` ;
  - `source`, `millesime` ;
  - `statut` : mesuré / sourcé / supposé / non mesurable.
- **Règle de partage du dépôt.** Le dépôt n'a encore aucun commit, donc les
  sessions travaillent dans le même dossier. Chacune ne touche que ses
  fichiers et ne commite rien. Seule l'axe 0 modifie `sante/`. *(Remplacé le 2026-11-14 : voir « Dossier v2 » plus bas.)*

**Pourquoi.** L'utilisateur·rice valide l'axe 5 et l'ordre, 2026-11-14.
L'ordre « axe 0 d'abord, puis le reste » est affiné : les axes 1, 3 et 4
produisent des documents et des données, pas du code qui dépend du contrat.
Les attendre ferait perdre du temps de hackathon.
**Ce qui le renverserait.** Le contrat de l'axe 0 exigeant un format de
fiche différent. Dans ce cas, on convertit les fiches, qui sont du texte.

## 2026-11-14 — Dossier v2 : code et docs séparés, v1 figée

**Décision.**
- Tout le nouveau travail va dans `v2/` :
  - le code du jumeau, dans un paquet sous `v2/` ;
  - `v2/ROADMAP.md` ;
  - `v2/docs/lab/` : `decisions.md`, `open.md`, `reports/`, `fiches/`,
    `figures/`.
- La v1 est **figée** et sert de référence en lecture seule : `sante/`,
  `app/`, `docs/lab/` à la racine.
  - On peut importer `sante` et lire `data/processed/`.
  - Les données brutes et traitées restent dans `data/`, partagées.
- Ceci remplace « seule l'axe 0 modifie `sante/` » (entrée « Axe 5 adopté »
  plus haut).

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « crée même un dossier v2 ».
Choix « code + docs séparés » parmi les options proposées.
**Ce qui le renverserait.** Un besoin de corriger un bug de la v1 dont la
v2 dépend. On le corrigerait alors en v1 avec une entrée datée.

## 2026-11-14 — Contrat du jumeau (axe 0) : état à cellules, modules à flux typés, scénario à événements

*Complété le 2026-11-14 par « Corrections du contrat du jumeau après la revue adversariale », plus bas. Les critères « module factice », « levier » et « agrégation » mesurés ci-dessous étaient en partie vrais par construction : remplacés par les critères C1–C10.*

**Décision.** Le jumeau est le paquet `v2/jumeau/`.
- **État** (`state.py`) : N[cellule, âge], avec cellule = (profession,
  secteur, territoire, sexe), plus un vivier national (profession × année
  d'étude).
  - Le secteur est un axe de l'état, pas un filtre. `ensure_sector` crée
    une destination vide (ex. `public`).
  - `level` dit ce qu'est le territoire. `Geography` agrège commune →
    département → région → national, uniquement vers le haut.
- **Modules** (`module.py`) : `name`, `order`, des `params` (des `Param`
  avec valeur, unité, source, millésime et statut, dans le format des
  fiches), `fit(hist)` et `step(state, ctx)` → une liste de flux typés :
  Shift, Rate, Add, Move, Pool.
  - Le moteur applique les flux module par module (séparation
    d'opérateurs), puis un plancher à 0. Chaque flux est inscrit au
    registre, par cellule.
  - Un module s'enregistre par `@register`, dans `jumeau/modules/` ou dans
    un dossier passé à `discover()`.
  - Une méthode qui n'est pas un stock-flux est un module qui rend ses
    résultats sous forme de flux. Elle peut aussi remplacer la composition
    entière derrière `Estimator`.
- **Scénario** (`scenario.py`) : des surcharges « module.param » et des
  `Event(param, start, value, op, end, selector)`. C'est la forme retenue
  de `Perturbation(slot, selector, profile)` (v1, § Open) : le slot est le
  paramètre, le profil est start, end et op (set, mul, add), le sélecteur
  porte sur les axes de l'état. La composition (`modules`) fait partie du
  scénario.
- **Modules livrés :** `vieillissement`, `sorties` (rétention, plus les
  leviers retraite et cumul), `entrees` (flux, filière, multiplicateur de
  quotas), `regulation` (géocodes : remplacement seul, excédent déplacé
  vers `destination`), `formation` (vivier, abandon, capacité ; les
  diplômés ne sont pas encore injectés dans N).

**Challenge de l'incumbent (challenge-design).** Contraintes, en unités :
- écart à `predict` : 0 personne ;
- coût d'un nouveau mécanisme : 1 fichier, 0 édition ;
- recalcul : < 2 s (supposé) ;
- agrégation : 0 personne d'écart.

Verdict :
- `sante.estimators.Estimator` (`fit` / `predict` / `assumptions`)
  **survit** comme couche du banc. Le jumeau s'y branche par
  `jumeau.estimators.twin_of`.
- `sante.model.project` et la perturbation de `app/levers.py` sont
  **remplacés** pour le travail par scénario. Les mécanismes y étaient
  fusionnés et les leviers patchaient le tuple `rates` de l'extérieur :
  ajouter un mécanisme demandait d'éditer deux fichiers.
- L'ajustement `fit_rates` est **réutilisé tel quel** (`history.py`). La
  v1 reste l'oracle.

**Mesuré** (`PYTHONPATH=v2 uv run python -m jumeau.check`,
[rapport](reports/2026-11-14-jumeau-axe0.md)) :
- **Reproduction.** Écart 0,0 sur 140 comparaisons `predict` (5 variantes
  stock-flux × banc K1 + origine récente jusqu'en 2050). Écart 0,0 aussi
  par cellule × âge × année jusqu'en 2050, pour 7 professions.
- **Levier.** Retraite + 1 an : écart 0,0 avec la v1 en 2050.
- **Module factice.** Ajouté depuis un dossier temporaire ; empreinte de
  `v2/jumeau/` et de `sante/` inchangée.
- **Agrégation.** 13 147 communes → national : écart 0 à chaque niveau.
- **Temps.** 18 ms par scénario pour 7 professions au département
  jusqu'en 2050. 0,29 s pour une profession à la taille commune
  (35 047 territoires).

**Rejeté :**
- des modules qui rendent des deltas additifs seulement : le Rate
  multiplicatif est nécessaire pour reproduire `s · base` à l'identique ;
- un plug-in au niveau du modèle entier seulement (statu quo) : les
  leviers ne pourraient pas viser un mécanisme sans éditer le modèle.

**Ce qui le renverserait.**
- Un module de l'axe 2 qui ne s'exprime pas en flux par cellule. Par
  exemple, une microsimulation qui doit garder des individus entre deux
  années : il faudrait un état auxiliaire propre au module.
- Un recalcul à la commune pour 5 professions × 2 secteurs au-delà de
  2 s : ~0,3 s × 10 ≈ 3 s, extrapolé ; à mesurer quand l'état communal
  existera.
- Un ordre des modules qui change les résultats de plus que le bruit.
  L'ordre est fixé par `order` ; sa sensibilité n'est pas mesurée.

## 2026-11-14 — Qui possède quoi dans v2 (sessions en parallèle)

**Décision.** Les sessions de recherche travaillent dans le même dossier,
sans commit. Chacune ne modifie que ce qui lui appartient :

| Axe | Session | Possède |
|---|---|---|
| 0 | jumeau | `v2/jumeau/` |
| 1 | hyperparamètres | `v2/docs/lab/fiches/param-*.md` |
| 3 | validation | `v2/validation/` |
| 4 | données | `v2/data/`, `v2/docs/lab/fiches/data-*.md` |

- Toutes peuvent ajouter leurs rapports dans `v2/docs/lab/reports/`, et
  ajouter des lignes dans `decisions.md` et `open.md` sans réécrire celles
  des autres.
- La v1 se consulte en lecture seule.
- Les axes 2 et 5 démarreront quand le contrat de l'axe 0 tournera.

**Pourquoi.** Le lancement des axes 1, 3 et 4, décidé par
l'utilisateur·rice le 2026-11-14. Sans commit ni worktree, seule la
séparation des fichiers empêche que deux sessions s'écrasent.
**Ce qui le renverserait.** Un premier commit, qui permettrait des
worktrees par axe.

## 2026-11-14 — Axe 3 : protocoles de validation pré-enregistrés et gelés par empreinte

**Décision.**
- Chaque niveau de validation a un protocole écrit **avant** tout calcul :
  [plan](reports/2026-11-14-axe3-plan-validation.md),
  [N1](reports/2026-11-14-axe3-n1-prevision.md),
  [N2](reports/2026-11-14-axe3-n2-long-terme.md),
  [N3](reports/2026-11-14-axe3-n3-leviers-did.md),
  [N4](reports/2026-11-14-axe3-n4-echelle-fine.md).
- Gel à 02:54, copies immuables dans `v2/validation/preregistered/`,
  SHA-256 (12 premiers caractères) : plan `0108455d34aa`, N1 `eb527ecb06a0`,
  N2 `bc5df3083cc5`, N3 `c37e36457f12`, N4 `91f897cc5071`.
- Tout écart ultérieur au protocole est une nouvelle entrée datée, marquée
  « écart au protocole » ; une analyse hors protocole est *exploratoire*.
- Les protocoles s'appliquent à **tout estimateur** exposant `fit` /
  `predict` (et `trajectory` pour N2), pas seulement au jumeau.

**Pourquoi.** K1 v1 a choisi la meilleure de 3 variantes après avoir vu les
résultats (biais de sélection, rapport K1 § correction). La ROADMAP (axe 3)
exige un protocole fixé avant les résultats.
**Ce qui le renverserait.** Rien sur le principe ; un protocole peut être
remplacé avant son premier passage, jamais après.

## 2026-11-14 — Axe 3, N1 : grille, métrique, seuil et variante par défaut du backtest

**Décision.**
- Origines glissantes, fenêtre d'ajustement élargie depuis 2012 (kinés
  2017), ≥ 5 ans ; horizons h ∈ {1, 3, 5, 8, 10}.
- **Métrique principale unique : MAPE par département à h = 5**,
  départements à **N ≥ 30** à l'origine, moyenne à poids égal sur les
  cellules profession × origine. WAPE, biais national signé, h ≠ 5 :
  secondaires.
- **Critère :** borne haute de l'IC 95 % (bootstrap des départements,
  2 000 tirages, graine 20261114) de MAPE(candidat) − MAPE(meilleure
  naïve) < 0.
- **Variante par défaut, seule confirmatoire :** stock-flux à taux locaux
  (poids 200, entrées plates, rétention ≤ 1), sur le jumeau
  `twin_of(StockFlowLocal)`. Toute autre variante s'inscrit, datée, dans
  `v2/validation/registry.py` avant son premier passage.
- **Dépôt de prévisions** origine 2026 → 2027, 2028, 2030, avec empreinte,
  scoré à la publication du RPPS 2027 : seul test non contaminé par K1.

**Pourquoi.** MAPE : chaque département compte pour un DG d'ARS, et c'est
la métrique de K1. h = 5 : seul horizon commun aux 5 professions sur
plusieurs origines. Meilleure naïve après coup : choix défavorable au
candidat.
**Ce qui le renverserait.** Un classement instable entre origines, qui
rendrait la moyenne poolée trompeuse (rapporté, sans changer le critère).

## 2026-11-14 — Axe 3, N2 : validation à 2050 par reproduction DD76 (en ratios) et cas limites

**Décision.**
- Reproduction du tendanciel DREES n°76 (CD, SF, PH), origine 2020, en
  **ratios N(t)/N(2020)**, hypothèses DD76 imposées, sans réglage libre.
  **Tolérance choisie : ±2 % en 2030, ±3 % en 2040 et 2050**, plus la
  forme (creux PH, plateau SF).
- Cas limites : L1 h → 0 exact (1e-9) ; L2 N* = Q·C à 1 % à o + 200 ans,
  indépendant de l'état initial ; L3 aucun effet d'un quota avant t0 + L ;
  L4 conservation (axe 0).
- Un seul échec bloque tout chiffre 2050 pour la profession concernée.

**Pourquoi.** Ratios : notre périmètre 2020 dépasse DD76 de 0,8 à 2,5 %.
3 % : quatre fois moins que l'effet d'un quota ±20 % publié par la DREES
(±12–13 % en 2050), donc le levier reste lisible. C'est un choix, pas une
dérivation.
**Ce qui le renverserait.** L'axe 5 montrant une bande à 2050 bien plus
large que 3 %, qui rendrait la tolérance trop stricte pour être
informative.

## 2026-11-14 — Axe 3, N3 : différence de différences sur le zonage infirmier (expérience naturelle)

**Décision.**
- **Expérience principale E1 (IDE) :** zone `z_infi` = 5 (sur-dotée,
  conventionnement en remplacement seulement) vs 3 (intermédiaire), zonage
  Atlasanté uuid c987d0e2 (génération 2012). Cellule = département × zone,
  ≥ 10 infirmiers en 2008 dans chaque cellule. Avant 2004–2008 (référence
  2008), transition 2009–2011 exclue, après 2012–2019.
- Estimateur : D = log Y₅ − log Y₃ par département, moyenne non pondérée,
  grappes = départements, Student G − 1.
- Tests fixés : T1 tendances parallèles (Hotelling, p ≥ 0,10), T2 placebo
  de date 2006, T3 placebo dentistes, T4 placebo zone 4 vs 3, T5 effet.
- **Validation du module `regulation` de bout en bout :** θ = β_obs / β_mod,
  où β_mod est l'effet d'un plafond parfaitement contraignant. IC de θ
  contient 1 → le module survit ; IC dans ]0, 1[ → remplacé par un plafond
  qui fuit, de paramètre θ.
- **E2 (kinés), secondaire :** marche 2012–2014, arrêt après l'annulation
  par le Conseil d'État (17 mars 2014), jusqu'en 2017.

**Pourquoi.** Seul levier de la liste avec une date d'effet, un zonage
ouvert par commune et une série communale qui couvre l'avant (2004–2008).
L'agrégation département × zone retire le bruit de Poisson communal et suit
l'échelle de décision de l'ARS. 2009–2011 est exclu car régi par un zonage
de 1re génération qu'on n'a pas.
**Ce qui le renverserait.** La preuve que le jeu Atlasanté n'est pas le
zonage de 2012 (une révision construite sur des densités postérieures).

## 2026-11-14 — Axe 3, N4 : taille minimale d'affichage communal sans bande

**Décision.**
- Origines 2014, 2016, 2018, 2020 ; h = 5. Estimateur par défaut :
  projection départementale × part communale tenue (oracle départemental
  tant que N1 n'a pas tourné).
- Classes de taille {1–2, 3–5, 6–10, 11–20, 21–50, 51–100, 101–200, > 200}.
- **N_min** = plus petite classe à partir de laquelle **P80 |erreur| ≤ 25 %**,
  pour IDE, MK et CD, dans ≥ 3 origines sur 4. Sous N_min : bande
  empirique P10–P90 obligatoire, ou agrégation.
- Bande calibrée sur 2014–2018, testée sur 2020 : couverture 75–85 %.

**Pourquoi.** Le bruit de Poisson seul donne P80 ≤ 25 % pour N ≥ 26
(dérivé). 25 % est un choix : l'écart entre deux classes de densité
usuelles.
**Ce qui le renverserait.** Une erreur non monotone en N (la taille ne
serait pas le bon critère).

## 2026-11-14 — Axe 4 : public / privé lu dans le « secteur d'activité » des fichiers DREES, ambiguïtés réparties par FINESS

**Décision.**
- **Source principale : les fichiers DREES déjà sur disque** (`data/raw/drees/*_rpps_2012_2026.xlsx`,
  ADELI kinés 2012–2016). Ils croisent dép × **secteur d'activité** (9 à 12 modalités) × mode × âge × sexe ;
  le loader v1 gardait le secteur à « Ensemble ». Aucune extraction RPPS supplémentaire.
- **Infirmiers : BTS DREES/Insee** (secteur déjà public / privé, 6 modalités) + SNDS libéraux (tous privés).
- **Règle de classement** (`v2/data/build_secteur.py`, table `SECTEUR`) :
  - libéral et mixte → privé, quel que soit le secteur (cohérent avec la décision « libéral = privé ») ;
  - salarié : hôpital public → public ; ESPIC, privé lucratif, officine, laboratoire, médicament,
    cabinets → privé ;
  - salarié des secteurs mixtes (centres de santé, prévention, médico-social, « autre ») → **ambigu**,
    bornes 0 et 1, part privée centrale prise dans **FINESS** (statut juridique des établissements de la
    catégorie, extraction au 2026-05-04) ; « autre secteur » et, pour les pharmaciens, « prévention et
    établissement de santé » → 0,5 **supposé** (pas de source ouverte).
  - Statuts juridiques FINESS 40–46 (organismes de sécurité sociale, ex. centres de santé CPAM) comptés
    **publics** (administrations de sécurité sociale).
- La sortie « libéral » se donne en **trois valeurs** : minimum (ambigus publics), centrale, maximum.

**Pourquoi.** Mesuré : Σ des cellules détaillées = total France du fichier à 0 % près (SF, CD, PH, ADELI),
0,22 % pour les kinés RPPS (incohérence interne du fichier source en 2017–2018). La SAE et les rapports de
l'Ordre ne donnent pas dép × âge × sexe ; ce fichier si.

**Conséquence mesurée (2026, nouvelle fourchette « libéral » = privé) :**
| Profession | Ancienne fourchette | Min | Centrale | Max |
|---|---|---|---|---|
| Sages-femmes | 12 475 – 26 428 | 12 059 | 12 912 | 14 660 |
| Pharmaciens | 65 344 – 75 335 | 60 005 | 63 612 | 67 219 |
| Dentistes | 48 143 – 48 690 | 40 784 | 47 349 | 47 894 |
| Kinés | 98 348 – 111 237 | 98 828 | 101 951 | 103 986 |
| Infirmiers (2023) | — | 277 788 | 277 788 | 277 788 |
- Les anciennes bornes basses n'étaient pas des minima : elles comptaient tout « autre salarié » comme
  privé (PMI, centres de santé municipaux inclus).

**Rejeté :** extraction de l'annuaire santé (RPPS individuel) — inutile tant que le fichier DREES croise
déjà le secteur ; SAE — pas de libéraux, pas de dép × âge × sexe pour ces professions.

**Ce qui le renverserait.** Une source qui ventile « autre secteur » des pharmaciens (5 805 salariés en
2026, 7,7 % de l'effectif) ; un écart > 5 % entre la part FINESS (établissements) et une part en effectifs
salariés (SAE / DADS) pour les centres de santé ou le médico-social.

## 2026-11-14 — Axe 4 : zonage par commune = CartoSanté `zonage_conv` (actuel) + Atlasanté c987d0e2 (génération 2012)

**Décision.**
- **Millésime actuel :** service TJS CartoSanté `zonage_conv`, référentiel COG 2026, attributs `z_sf`,
  `z_dent`, `z_kine`, `z_infi` (sources CNAMTS – ARS). 34 877 communes par profession. La date des arrêtés
  n'est pas servie : millésime = date d'extraction (2026-11-14).
- **Historique :** jeu Atlasanté uuid c987d0e2 (`z_infi`, `z_kine`, `z_dent`, pas de SF), 36 700 communes,
  codes région d'avant 2016 → génération 2012, comme l'a lu l'axe 3 (entrée N3 ci-dessus). Pas d'autre
  millésime ouvert trouvé.
- **Statut lu par le modèle** (`v2/data/build_zonage.py`) :
  - `remplacement_seul` = « sur-dotée » (ancien zonage) ou « non prioritaire » (nouveau zonage kinés,
    dentistes) ;
  - `incitation` = très sous-dotée ou sous-dotée ;
  - `autre` = intermédiaire, très dotée, non renseigné.
  - Les deux régimes coexistent chez les kinés (2 800 communes « non prioritaires », 10 « sur-dotées »).
- **« Obligation d'exercice » n'est pas une classe de zonage** dans ces fichiers : elle n'est pas codée
  par commune (voir open.md).
- Paris, Lyon et Marseille sont zonés par arrondissement ; le référentiel `com2026` ne les porte pas
  (« non renseigné », 2,5 à 6,5 % de la population selon la profession).
  - **Remplacé le 2026-11-14 (même session) :** on lit le référentiel `arm2026` du même service, qui
    remplace les trois communes par leurs 45 arrondissements, zonés. Table : 34 919 géocodes par
    profession (colonne `niveau` = com / arm). Restent « non renseignés » : 2 à 26 communes des DROM
    selon la profession.

**Pourquoi.** Seules sources ouvertes par commune ; CartoSanté couvre aussi les DROM et les SF.
**Ce qui le renverserait.** Les arrêtés ARS datés (par région) montrant que le service CartoSanté mélange
des générations ; un référentiel arrondissement pour PLM.

## 2026-11-14 — Les axes 2 et 5 attendent la correction des défauts bloquants du jumeau

**Décision.**
- Les axes 2 et 5 ne démarrent pas avant que les 4 défauts bloquants de la
  [revue adversariale](reports/2026-11-14-revue-adversariale-axe0.md)
  soient corrigés :
  - modules du scénario ignorés par `twin_of` ;
  - secteur public sans sorties ;
  - dépendances entre modules non déclarées ;
  - scénario non validé et non sérialisable.
- Les critères d'acceptation de l'axe 0 sont réécrits pour pouvoir échouer.
- Les défauts sont transmis à la session de l'axe 0, qui possède
  `v2/jumeau/`.

**Pourquoi.** La revue a confirmé 6 défauts sur 6 soumis à réfutation
(mesuré). Plusieurs critères annoncés étaient vrais par construction.
**Ce qui le renverserait.** Une nouvelle revue qui ne trouve plus de
défaut bloquant.

## 2026-11-14 — Axe 3, N3 lancé : régulation IDE non validée (T1 échoue) ; prédiction kinés confirmée

**Décision.**
- **IDE : le levier « régulation en zone sur-dotée » n'est pas validé.**
  L'effet mesuré est −30 % [−34 ; −26] sur 2012–2019, et les trois placebos
  passent. Mais le test de tendances parallèles pré-enregistré échoue
  (p = 0,043 < 0,10). On applique le protocole tel quel, sans changer le
  seuil après coup.
- **Kinés : la prédiction marche / arrêt pré-enregistrée est confirmée**
  (écart des pentes +3,1 pts/an [1,1 ; 5,1], tendances parallèles
  p = 0,24). Ce n'est pas encore une validation du module, θ n'étant pas
  pré-enregistré pour E2.
- **θ ≈ 0,80 [0,74 ; 0,87]** (part contraignante du plafond, IDE) est
  **exploratoire** : à transmettre à l'axe 1 comme valeur *supposée*, pas
  mesurée. Il suggère un plafond qui fuit plutôt que le plafond strict du
  module `regulation`.
- Toute nouvelle analyse IDE (borne de Rambachan & Roth, contrôle
  synthétique) sera un **second test**, pré-enregistré avant passage.
- Rapport : [N3](reports/2026-11-14-axe3-n3-leviers-did.md), section
  Résultat.

**Pourquoi.** Pré-enregistrement (entrée « protocoles gelés » ci-dessus) :
relâcher un seuil après avoir vu p = 0,043 recréerait le biais de K1.
**Ce qui le renverserait.** Un second test pré-enregistré qui passe, ou la
preuve que le zonage Atlasanté n'est pas celui de 2012 (qui invaliderait
aussi E2).

## 2026-11-14 — Axe 1 : sources retenues pour les hyperparamètres par profession

**Décision.** Une source primaire par famille de paramètres. Fiches dans
`fiches/param-*.md`, synthèse dans
[le rapport axe 1](reports/2026-11-14-axe1-hyperparametres.md).

**Sources retenues.**
- **Régulation, règle.** Le texte conventionnel lui-même :
  - IDE : avenant 6 (JORF du 13/06/2019) ;
  - SF : avenant 4 (JORF du 10/08/2018), reconduit par l'avenant 7 (2023) ;
  - MK : avenant 7 (arrêté du 21/08/2023) ;
  - CD : convention du 21/07/2023 (arrêté du 23/08/2023), effet au
    01/01/2025.

  Les guides ARS et les syndicats ne servent qu'à confirmer.
- **Régulation, zonage de référence pour l'axe 1.** data.gouv « Zonages des
  professionnels de santé libéraux » (`t-zonages-com.csv`, avec la date des
  arrêtés). Il concorde avec la source CartoSanté de l'axe 4 (±10
  communes) : pas de conflit avec la décision « Axe 4 : zonage par
  commune ».
- **Régulation, effet.** IRDES QES n° 270 (seule estimation causale
  publiée). Il sert de **cible de validation**, pas de paramètre à ajouter
  au plafond. θ = 0,80 de l'axe 3 est classé *supposé*, comme l'axe 3 le
  demande.
- **Filières pharmacie.** Ordre national des pharmaciens, Panorama annuel :
  primo-inscrits par section. Pour la part privée de H, conflit avec la
  DREES (17 % contre 28,6 %) : **défaut proposé = DREES**, l'Ordre en borne
  haute. Choix final au ledger.
- **Odontologie.**
  - Postes de DES : arrêtés annuels du CNG au JORF, et statistiques du CNG
    pour 2008-2018.
  - Stocks par spécialité : rapports d'activité de l'Ordre (ONCD).
- **Abandon IFSI.** DREES, enquête Écoles, jeu 491 (« Séries longues
  1966-2025 »). Le modèle lit le **rendement ρ = diplômés(t+3) / inscrits en
  1re année(t)**, qui est *mesuré*, plutôt qu'un taux d'abandon.
- **Sorties.** DD76 et ER 1062, 1075 et 1319 pour les définitions ; CNOMK
  pour l'âge de retraite des MK ; COR 2016 pour le cumul emploi-retraite.
  La mortalité n'est pas séparée de la cessation.

**Rejeté.**
- « 30 % d'abandon par an » en IFSI : aucune source primaire (QO AN n° 101,
  2023, sans source) et incompatible avec la DREES.
- « Obligation de 2 ans pour les dentistes » : elle n'existe pas. Il s'agit
  des kinés (avenant 7, art. 4.1.1).

**Pourquoi.** Le principe « aucun nombre sans source primaire et millésime »
(ROADMAP § 1). Le rendement ρ_IDE est choisi parce qu'il est calculable
chaque année sur une donnée ouverte. Il englobe abandon, redoublement et
passerelles, ce qui le rend directement utilisable par le module
`formation`.

**Ce qui le renverserait.**
- Un bilan Cnam publié sur les avenants SF et MK.
- Un suivi individuel IFSI (cohortes).
- Une publication de l'Ordre ventilant les primo-inscrits H par
  public / privé.

## 2026-11-14 — Corrections du contrat du jumeau après la revue adversariale

*Complété le 2026-11-14 par « Seconde série de corrections » : destination par défaut `bloques` (remplace `public`), levier retraite B1 (remplace la parité v1 du test C7).*

**Décision.** Ces règles complètent le contrat (`v2/jumeau/`). Elles
corrigent les 6 défauts de la
[revue](reports/2026-11-14-revue-adversariale-axe0.md) et 2 des 3
constats non vérifiés.
1. **La composition fait partie du scénario.**
   `TwinEstimator.trajectory(until, scenario)` construit et calibre les
   modules du scénario passé, avec un cache par composition. Un paramètre
   d'un module absent de la composition est une erreur.
2. **Une cellule sans historique a une règle de repli explicite**
   (`supposé`).
   - Elle prend la rétention de la cellule de même (profession,
     territoire, sexe) dans le secteur `repli` (privé par défaut), avec
     I = 0.
   - Sans cellule de repli, c'est une erreur ; s = 1 n'est plus donné en
     silence.
   - Le secteur public a désormais un historique réel :
     `history.sector_table` lit `v2/data/processed/secteur_stock.parquet`
     (axe 4), où les salariés ambigus sont répartis par leur part privée,
     avec trois variantes (centrale, min, max).
3. **Les dépendances entre modules sont déclarées.** Chaque module a un
   `needs` (les flux de l'année qu'il lit via `ctx.delta`) et un
   `produces`.
   - `build()` refuse un besoin que ne produit aucun module placé avant,
     ainsi que deux producteurs du même flux.
   - `ctx.delta` refuse une lecture non déclarée, et `run()` refuse un flux
     rendu mais non déclaré.
   - La régulation refuse des zones qui ne touchent aucune cellule du
     secteur régulé.
4. **Le scénario est validé et sérialisable.** `Scenario.validate` refuse
   une clé, une opération, un axe de sélecteur ou une composition inconnus.
   `to_json` / `from_json` portent un `format` égal à 1 et une `seed`
   (`ctx.rng`).
5. **Convention des quotas = v1.** Les entrées × m s'appliquent à partir de
   origine + L_p + 1 (`entrees.evenement_quotas`). Cela suit
   `app/levers.project_flow`, où l'année origine + L_p reste au niveau de
   base.
6. **Les unités sont rattachées strictement.** `Geography.up` refuse une
   unité non rattachée ou rattachée deux fois. L'écart externe
   CartoSanté / RPPS est mesuré et publié ; il n'est pas corrigé.
7. **Vieillissement et reproductibilité.**
   - Le vieillissement accepte une fraction par tranche
     (`vieillissement.fractions`, pour les tranches CartoSanté).
   - Un module remet son état à zéro dans `begin()` à chaque run
     (formation).
   - `run(floor=False)` retire le plancher à 0 pour les tests de
     conservation.

**Critères d'acceptation réécrits pour pouvoir échouer** (C1–C10,
`PYTHONPATH=v2 uv run python -m jumeau.check`, code de sortie 1 en cas
d'échec). Chaque critère porte la valeur « avant » mesurée par la revue.
Deux mutations ont été vérifiées :
- remettre s = 1 au public fait échouer C4 (+838 personnes) ;
- avancer les quotas d'un an fait échouer C7 (écart de 15 par
  département).

**Pourquoi.** La revue adversariale a confirmé 6 défauts sur 6, mesurés.
Les critères d'origine passaient par construction.
**Rejeté :** mettre les dépendances dans l'ordre (`order`) seulement : un
module renommé ou absent fausserait le résultat sans erreur. Corriger la
convention des quotas côté v1 : la v1 est figée et sert d'oracle.
**Ce qui le renverserait.**
- Une nouvelle revue qui trouve un critère vrai par construction.
- Un module de l'axe 2 qui doit lire autre chose que des flux de l'année :
  il faudrait déclarer aussi les lectures d'état.

## 2026-11-14 — Axe 4 : registre d'événements `v2/data/events.csv` ; le saut d'inscrits 2025 est un artefact

**Décision.**
- Le registre est un CSV, une ligne par texte ou fait observé : `id, date_effet, profession, flux_touche,
  type, description, source, millesime, confiance`. 30 lignes (2009–2028), 23 `verifie`, 7 `partiel`.
  Chaque ligne a sa fiche `fiches/data-ev-*.md`.
- Sources : texte primaire quand il a pu être ouvert (Légifrance, ameli, Conseil d'État, DREES, ARS) ;
  sinon une source secondaire nommée (12 lignes), à remplacer.
- Date inconnue au jour près → rentrée (01/09) ou fin d'année universitaire, dit dans la description.
- **Le saut d'inscrits 2025-26 (odontologie 2e année : 2 083) est traité comme un artefact de fichier,
  pas comme une réforme** : Université Paris Cité vaut 683 contre 188–215 les années précédentes.
  Valeur à utiliser : 1 588 (fichier compilé « Base inscrits 2ème cycle MOP »), ou Paris Cité ≈ 190.
- Rejeté : un registre qui n'a que les réformes de la liste de départ. On y ajoute les ruptures de données
  (ADELI → RPPS 2017, artefact 2025), qui déplacent les séries autant qu'une réforme.

**Pourquoi.** Mesuré : l'année blanche MK 2018 se voit dans le RPPS (moins de 25 ans, 5 637 → 3 681 au
1er janvier 2019, −35 %) ; la part de population des zones dentaires non prioritaires (5 %, ARS PACA) se
retrouve dans la table de zonage (4,8 %).
**Ce qui le renverserait.** Une notice DREES expliquant la ligne Paris Cité comme un vrai changement de
périmètre (par exemple des entrants par une nouvelle voie) ; dans ce cas, l'événement devient une réforme.

## 2026-11-14 — Reprise de l'observatoire de l'équipe : 19 éléments adoptés, sous la ROADMAP

**Décision.**
- On reprend 19 éléments de l'observatoire (Pierreafeu181), détaillés dans
  [le rapport de reprise](reports/2026-11-14-reprise-observatoire.md) :
  - pour la validation : mondes simulés, backtest toutes origines, métrique
    de classement, ER1319 ;
  - pour le modèle : levier retraite corrigé (+n ans en 65+), année de
    décision et convention de date unique, shrinkage hiérarchique, levier
    incitatif à total constant, tests de propriétés ;
  - pour les données : zonage data.gouv en contrôle croisé, estimations de
    population 1975–2026, scénario « Population âgée », cellules masquées,
    règle sur les fichiers étudiants, correspondance université → ARS.
- **Pas repris :** sa définition de « libéral », son grain, son horizon, le
  modèle unique, le vieillissement uniforme, le seuil d'alerte relatif, les
  diplômés étrangers non sourcés.
- **Réservé** à la couche personas : son site, ses conventions
  d'affichage, la densité ajustée aux besoins.

**Pourquoi.** Demande de l'utilisateur·rice, 2026-11-14 : « rapport
exhaustif de ce qu'on reprend de son travail ». `v2/ROADMAP.md` prime.
**Ce qui le renverserait.** Un élément repris qui contredit un résultat du
banc ou un monde simulé.

## 2026-11-14 — Axes 2 et 5 lancés ; skills de design installés ; trois directions pour l'observatoire

**Décision.**
- **Axes 2 et 5 lancés**, à la demande de l'utilisateur·rice. Cela remplace
  « les axes 2 et 5 attendent la correction des défauts bloquants ».
  - La session de l'axe 0 dit avoir corrigé les 6 défauts. Ses 10 critères
    réécrits passent, et deux mutations échouent comme prévu.
  - Ces corrections n'ont **pas été revues de façon indépendante**. Une
    nouvelle revue adversariale reste à faire (ledger).
- **Skills installés** dans `.claude/skills/` :
  - `impeccable` 4.9.1 (pbakaus, Apache-2.0) ;
  - `design-taste-frontend` / taste-skill 2.5.1 (Leonxlnx, MIT).

  Le binaire que télécharge impeccable n'est **pas exécuté** : on suit ses
  consignes à la main. Aucun hook n'est installé. taste-skill vise les
  sites vitrines, pas les tableaux de bord, et pèse 39 Mo dans le dépôt.
- **Trois directions artistiques proposées** pour l'observatoire
  (`v2/docs/lab/design/2026-11-14-da-observatoire.html`) :
  - **A**, sémiologie graphique (Bertin), recommandée ;
  - **B**, gamme de signalisation ;
  - **C**, topographie en isolignes ;
  - l'option standard, le DSFR, est réservée aux services de l'État.

  Aucune n'est encore choisie. Ce travail d'interface relève de la couche
  personas et ne prend pas la place des axes de recherche.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « lance les axes 2 et 5
après », « oui, les deux » pour les skills, et « le site fait trop
claude ».
**Ce qui le renverserait.** Une revue indépendante qui trouve un défaut
bloquant restant dans le jumeau. Dans ce cas, les axes 2 et 5 s'arrêtent
sur ce point.

## 2026-11-14 — Axe 5 : sortie, facteurs, plages, N et graine de l'analyse de sensibilité

**Décision.**
- **Sortie Y** : N « libéral » (secteur privé), total national, par
  profession, en 2030, 2040 et 2050. Le jumeau tourne au département, sur le
  privé seul : sans régulation ni transition, aucun flux ne relie le privé
  et le public.
- **Infirmiers** : `secteur_stock` n'a ni âge ni sexe. On utilise donc
  `infirmiers-liberaux` (v1, SNDS par âge, 2012–2023), soit 98 854 en 2023
  contre 277 788 dans tout le privé. C'est un écart de périmètre, signalé
  dans chaque sortie.
- **Facteurs et plages** (tirage uniforme ; les niveaux discrets sont
  équiprobables) :
  - E, fenêtre d'ajustement : {2, 3, 5, 8} ans ;
  - E, shrink : {20, 200, 2000, national} ;
  - E, entrées : {plates, récentes sur 2 ans} ;
  - E, filière : {non, oui}, pour CD et PH seulement ;
  - D, part privée des salariés ambigus : {min, centrale, max} (axe 4),
    sauf pour les IDE ;
  - P, `vieillissement.fraction` : [0,18 ; 0,22] (supposé, ±10 %) ;
  - P, `sorties.part_cumul` : valeur de la fiche cumul (SF 0,8 %, CD
    4,7 %, PH 1,8 %, MK et IDE 1,5 %) × [0,5 ; 2] (supposé autour d'un
    sourcé de 2015) ;
  - L, `decalage_retraite` : [0, 2] ans ;
  - L, `cumul_multiplicateur` : [1, 2] ;
  - L, quotas × [0,8 ; 1,2] après L_p (DD76 ±20 % ; L_p de la v1, supposé).
- **Deux familles** :
  - « tout » (leviers compris) classe ce qui déplace Y ;
  - « incertitude » (leviers au tendanciel) donne la fourchette (a).
- **Variante d'entrées « tendance » exclue du plan de Sobol.** Elle
  multiplie N(2050) par 2 à 10 (SF, fenêtre de 2 ans : 183 200 contre
  19 000, mesuré). Elle est rapportée à part, sur une grille.
- **Méthodes.**
  - Morris : r = 30 trajectoires, p = 4 niveaux, pas Δ = 2/3.
  - Sobol : estimateurs Saltelli 2010 (S1) et Jansen (ST), N = 2048,
    soit N(k + 2) runs.
  - Intervalles bootstrap à 95 %, 500 tirages.
  - Graine 20261114, celle du protocole N1.
  - Tout est implémenté en numpy (ni SALib ni scipy dans l'environnement).
- **Hors analyse par construction** : `formation.*` (le vivier n'alimente
  pas N), la régulation (zones communales, non activables au département)
  et les fiches sans point d'entrée dans le jumeau. Effet nul **par lecture
  du code**, non mesuré.

**Pourquoi.** La tâche de l'axe 5 (`v2/ROADMAP.md`) : mettre un prix sur
l'axe 1 et donner les fourchettes à 2050. Les leviers ne sont pas des
incertitudes : les mélanger à la fourchette la rendrait dépendante de la
politique choisie.
**Ce qui le renverserait.**
- Un indice ST dont l'intervalle bootstrap est plus large que l'indice
  lui-même : il faudrait augmenter N.
- Un module de l'axe 2 qui branche formation ou régulation : à refaire.

## 2026-11-14 — Dépôt git autonome, commits sans mention de Claude

**Décision.**
- Le projet est un dépôt git autonome, nommé `hackathon_acces_soins`,
  indépendant de sevel.
- Les commits sont découpés par thème.
- Les messages de commit ne mentionnent pas Claude (règle inscrite dans
  `CLAUDE.md`).
- Restent hors du dépôt : les données brutes et traitées, le mémoire
  EHESP (document tiers) et le skill taste-skill (39 Mo, réinstallable).

**Pourquoi.** L'utilisateur·rice, 2026-11-14.
**Ce qui le renverserait.** Un besoin de versionner les données traitées.
Dans ce cas, on passerait par Git LFS ou un dépôt de données séparé.

## 2026-11-14 — Prototype de l'écran de décision (direction A), servi par le jumeau

**Décision.**
- Prototype dans `v2/prototype/` : `server.py`, un serveur Python qui
  appelle le jumeau, et `index.html`, en direction A.
- **Pas de moteur dupliqué en TypeScript.** La fluidité vient de requêtes
  annulables et de courbes interpolées. Mesuré : 3 à 32 ms dans le jumeau,
  50 à 120 ms aller-retour.
- Simplifications assumées et affichées dans l'écran : grain
  départemental ; régulation approchée au département (≥ 50 % des
  communes en « remplacement seul ») ; fourchette par pente nationale ;
  infirmiers exclus.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « prototype A ». Ce
prototype répond aux critères d'interface inscrits plus bas sous Open.
**Ce qui le renverserait.** Un recalcul au-dessus d'environ 200 ms à
l'échelle communale. Il faudrait alors une grille précalculée.

## 2026-11-14 — Le jumeau ne passe pas la seconde revue : leviers retraite et régulation non citables

**Décision.**
- Les chiffres du jumeau qui dépendent des leviers **retraite** ou
  **régulation**, ou d'un scénario passé à `trajectory()` sur une variante
  filière, **ne sont pas cités** tant que les 4 défauts bloquants de la
  [seconde revue](reports/2026-11-14-revue-adversariale-axe0-v2.md) restent
  ouverts.
- Le tendanciel et le levier quotas sur StockFlowLocal restent
  utilisables.
- **Écart avec une décision inscrite** : l'entrée « Reprise de
  l'observatoire » a adopté le correctif retraite e/(1+Δe), et le code ne
  l'applique pas. La décision reste valable ; le code est en retard.

**Pourquoi.** Seconde revue : 6 constats sur 6 confirmés (mesuré).
**Ce qui le renverserait.** Une troisième revue sans défaut bloquant.

## 2026-11-14 — Prototype : leviers retraite et régulation suspendus, quotas bornés

**Décision.**
- Dans `v2/prototype/`, les leviers retraite et régulation sont désactivés
  dans l'interface, avec leur raison affichée, et refusés par le serveur
  (code 400).
- Les quotas sont bornés à [0,7 ; 1,5]. Une profession inconnue est
  refusée.
- Vérifié dans le navigateur : retraite, régulation, quotas = 110 et
  « dentiste » sont rejetés ; quotas 1,2 sur le Puy-de-Dôme est accepté.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 (« oui, borner »), après la
seconde revue du jumeau.
**Ce qui le renverserait.** Les défauts 1 et 2 de la seconde revue
corrigés et confirmés par une troisième revue. On réactive alors les deux
leviers.

## 2026-11-14 — Seconde série de corrections du jumeau (seconde revue adversariale)

**Décision.** Corrige les 4 défauts bloquants de la
[seconde revue](reports/2026-11-14-revue-adversariale-axe0-v2.md) et ses
2 constats non vérifiés. Le code est dans `v2/jumeau/` ; chaque correction
a un test qui échoue avant et passe après (mutations rejouées).
1. **Levier retraite = B1** (décision « Reprise de l'observatoire »), dans
   `modules/sorties.py` :
   - 65 ans et plus : e' = e/(1 + Δe) ;
   - 60–64 : e × (1 − Δ/5) ; 55–59 : e × (1 − Δ/10) ;
   - tranches à solde positif inchangées ;
   - montée en charge de 3 mois par an via `evenement_retraite(Δ,
     décision)`.
   - **Remplace** le masque v1 `e[60–69] × (1 − Δ/5)`. La parité avec la
     v1 est abandonnée pour ce levier, parce que la v1 porte le défaut. Le
     test C7 compare au séjour attendu (+Δ ans en 65+), plus à la v1.
2. **Destination par défaut de la régulation : secteur `bloques`.**
   - Il est créé vide par `Regulation.prepare`. Ses cellules suivent la
     démographie du privé (règle de repli), si bien que la régulation
     déplace sans créer ni supprimer.
   - **Remplace** la destination `public` : avec un historique public, les
     taux publics faisaient varier le total (+254 dentistes, −474 kinés),
     un écart qui venait de l'hypothèse de destination et non du
     mécanisme.
   - `destination = "public"` reste possible et son effet est publié (C2).
   - La sortie « libéral » (privé) ne compte pas `bloques`.
3. **Un scénario se pose sur le scénario de base.** `Scenario.over(base)`
   fusionne les paramètres (le scénario passé prime) et ajoute ses
   événements à ceux de la base. `trajectory()` et `twin_of(…, scenario)`
   l'utilisent, si bien que la filière d'une variante n'est plus perdue.
4. **Le scénario est validé sur ses valeurs.**
   - Chaque valeur de sélecteur doit exister dans l'état, par exemple
     `'dentiste'` ou `6` sont refusés.
   - `Param.bounds` borne les valeurs, et `validate` refuse une valeur hors
     plage, y compris le résultat d'un `mul` ou d'un `add`. Bornes posées :
     - quotas [0, 3] ;
     - `decalage_retraite` [0, 5] ;
     - `cumul_multiplicateur` [0, 5] ;
     - parts [0, 1].
5. **Constats non vérifiés, traités :**
   - `ctx.delta` d'un producteur muet rend 0, et celui d'un flux Pool lève
     une TypeError explicite ; `ctx.pool_out` donne accès aux comptes du
     vivier, dont les diplômés.
   - `fit_rates` suppose toujours un vieillissement de 1/5 : c'est noté
     dans le ledger, non corrigé.

**Pourquoi.** La seconde revue a confirmé ses 6 constats en exécutant le
code. Le masque retraite contredisait une décision inscrite.
**Rejeté :**
- Garder `public` comme destination par défaut : le total dépendrait
  d'une hypothèse non sourcée.
- Corriger le levier retraite côté v1 : la v1 est figée.

**Ce qui le renverserait.**
- Une source sur la destination réelle des entrants bloqués (axe 1).
- Une troisième revue qui trouve un défaut bloquant.

**Conséquences pour les autres axes.**
- Les chiffres retraite de l'axe 5 et du prototype sont à recalculer. Le
  module `sensibilite/retraite_b1.py` est désormais le comportement par
  défaut, à la montée en charge près.
- La régulation du prototype conserve désormais le total.

## 2026-11-14 — Chaque axe de recherche produit un prétirage au format arXiv

**Décision.**
- Le livrable de chaque axe est un **article de recherche mis en forme
  comme un prétirage arXiv** : `v2/papers/axeN-<sujet>/main.tex`, avec ses
  `refs.bib` et `figures/`.
- Format commun : `v2/papers/template/` (préambule partagé, plan,
  bibliographie vérifiée). Source TeX autonome (pdfLaTeX), en français
  avec un résumé anglais.
- Chaque nombre porte sa provenance (mesuré, dérivé, supposé) et vient
  d'un rapport de `v2/docs/lab/reports/`. Les rapports restent le
  registre ; l'article les met en forme.
- **Défauts retenus sans demande explicite, à confirmer** : la langue
  (français) et les auteurs (« Équipe hackathon-santé » et Claude comme
  assistant de recherche). *Corrigé le 2026-11-14 à la demande de l'utilisateur·rice : Claude n'est plus cité comme auteur, ni dans le gabarit ni dans les six prétirages.*
- Aucun moteur TeX n'est installé : la compilation attend
  `brew install tectonic` (accord à demander).

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « le but de chaque axe de
recherche est de construire des sortes de papier de recherche […] comme un
preprint arXiV ».
**Ce qui le renverserait.** Une autre cible : revue, mémoire ou rapport
DREES.

## 2026-11-14 — Écran de décision V2 : carte plein écran (`v2/prototype-carte/`)

**Décision.**
- Nouvel écran dans `v2/prototype-carte/`, modèle d'interaction
  d'InvestHub HCMC : carte MapLibre plein écran, recherche, leviers
  repliables, fiche flottante au clic, comparer / lien / export CSV.
- Serveur : importe `v2/prototype/server.py` sans le modifier ; ajoute
  `/geo` et `/api/carte` (101 départements en un appel), quotas bornés par
  la même règle [0,7 ; 1,5] ; retraite et régulation restent refusés.
- Couleur « évolution » lue en points d'écart à l'évolution nationale
  (sinon carte monochrome) ; gamme ocre ↔ bleu, ni rouge ni vert ; une
  couleur fixe par profession.
- Mesuré : réponse perçue p50 53 ms, p95 66 ms, max 87 ms (n = 35).

**Pourquoi.** Demande de l'utilisateur·rice (V1 « trop proche d'un PDF »),
via la session v2. Rapport :
[2026-11-14-prototype-carte](reports/2026-11-14-prototype-carte.md).
**Ce qui le renverserait.** Une réponse perçue au-dessus de 150 ms au
grain communal : il faudrait une grille précalculée.
- **Ajout du 2026-11-14 (retour UAT, « better zooming on the regions…,
  boxes slightly bigger »)** : limites régionales tracées dès la vue
  France ; premier clic = région, second = département (Maj + clic :
  département) ; panneaux et textes agrandis. Latence non re-mesurée.
- **Ajout du 2026-11-14 (retour UAT n° 2, « on voit tout et c'est très
  difficile de s'en sortir »)** : vue France colorée par région ARS
  (agrégat), limites départementales masquées sous le zoom 6,3, liseré
  d'espacement entre régions ; départements visibles en zoomant ou dans la
  région ouverte.
- **Ajout du 2026-11-14 (retour UAT n° 3)** : DROM en encarts
  schématiques à l'ouest de la métropole (géométrie déplacée et remise à
  l'échelle côté serveur).
- **Écart signalé** : la décision « Troisième revue … leviers du prototype
  réactivés » réactive retraite et régulation dans `v2/prototype/` ;
  `v2/prototype-carte/` les garde désactivés (consigne de départ de la
  session). À trancher par la session v2.
- **Ajout du 2026-11-14 (retour UAT n° 4)** : fond de mer gris bleuté
  #D5DADF, milieu de gamme gris chaud #C4C2B8, trait de côte tracé,
  limites départementales à 35 % en vue France.
- **Ajout du 2026-11-14 (retour UAT n° 5, « les autres devraient se
  blur »)** : régions non ouvertes estompées (opacité 0,3) plutôt que
  floutées ; Échap / clic hors carte → vue France.
- **Ajout du 2026-11-14 (utilisateur·rice : « the other regions should
  become gray »)** : l'estompage est remplacé par un gris uni #ECEDEE pour
  tout ce qui est hors du territoire ouvert (région ou département ; la
  commune s'y ajoutera). Un dépôt de hash avec `t=` vole vers le
  territoire.
- **Ajout du 2026-11-14 (retour UAT n° 6)** : plancher de texte 14 px dans
  les panneaux, fiche min(520 px, 36 vw), chiffres clés 34 px, bouton
  A/A+ inscrit dans l'URL.
- **Ajout du 2026-11-14 (retour UAT n° 7)** : fil d'Ariane France ›
  région › département, cliquable ; Échap / Retour arrière remontent d'un
  niveau ; historique du navigateur actif.
- **Ajout du 2026-11-14 (utilisateur·rice : « couleurs plus continues »)** :
  classes remplacées par un dégradé continu sur les mêmes 7 teintes,
  borné à ±B ; légende en barre dégradée. Chiffre exact au survol.
- **Ajout du 2026-11-14 (utilisateur·rice : « zoom more…, boxes bigger »)** :
  leviers repliés à l'ouverture d'un territoire, cadrage serré (marge
  gauche 150 px, zoom max 8,5 / 10), panneaux de données ×1,15 par défaut,
  ×1,32 en A+.

## 2026-11-14 — Axe 3, N5 : mondes simulés à vérité connue, ajoutés au protocole (gel 03:46)

**Décision.**
- Un 5e niveau de validation : 7 mondes simulés (reprise de l'observatoire,
  A1), générateur en âges simples agrégé comme le RPPS, 20 réplications,
  graine 20261114 + réplication.
- Critère : dans un monde qui respecte les hypothèses de l'estimateur
  (M1 équilibre, M3 bruit), |erreur nationale| ≤ 1 % à 15 ans ; dans un
  monde qui les viole (M4–M7), le signe du biais prédit d'avance est
  observé dans ≥ 16 réplications sur 20.
- Protocole : [N5](reports/2026-11-14-axe3-n5-mondes-simules.md), copie
  immuable dans `v2/validation/preregistered/`, SHA-256 `1046545b17c0`.
- Il est gelé **après** le lancement de N3 mais **avant** tout calcul sur
  un monde simulé. L'article de l'axe 3 le dit.
- **Accepte** l'inscription des variantes de l'axe 2 en fin de
  `registry.py` (entrée « Axe 2 : 5 variantes pré-inscrites ») : le
  protocole N1 l'impose, et les lignes de l'axe 3 sont intactes.

**Pourquoi.** Consigne de la session v2 (2026-11-14) : ajouter les mondes
simulés. Un backtest ne sépare pas erreur de modèle, bruit et changement du
monde ; un monde simulé, si.
**Ce qui le renverserait.** Le kill test de l'axe 2 (18 mondes) montre que
le biais d'âge n'a pas de signe fixe : la prédiction de signe de M4 peut
tomber. Ce serait un résultat, pas une raison de changer le protocole.

## 2026-11-14 — Troisième revue : plus de défaut bloquant dans le jumeau ; leviers du prototype réactivés

**Décision.**
- Les leviers retraite et régulation sont réactivés dans le prototype,
  avec des bornes côté serveur : quotas [0,7 ; 1,5], retraite [−2 ; 3],
  NaN refusé. Cela remplace l'entrée « leviers suspendus ».
- Leurs chiffres redeviennent citables avec deux réserves écrites :
  - la régulation est approchée au département ;
  - le test de la règle « entrées ≤ sorties » reste non vérifié (troisième
    revue, constat non réfuté), à lever avant tout prétirage.
- La règle « les axes 2 et 5 attendent » est levée.

**Pourquoi.** [Troisième revue](reports/2026-11-14-revue-adversariale-axe0-v3.md) :
aucun défaut bloquant dans le jumeau, conservation mesurée (≤ 0,5
personne). Le défaut bloquant du prototype est corrigé.
**Ce qui le renverserait.** Un défaut bloquant trouvé par une revue
ultérieure ou par le banc de l'axe 3.

## 2026-11-14 — Axe 1 : panel de 14 politiques jouables, avec plages proposées

**Décision.**
- Le catalogue de l'axe 1 est traduit en un **panel de 14 politiques
  publiques**. Chacune donne :
  - l'hyperparamètre qu'elle déplace et le paramètre du jumeau visé ;
  - le statu quo ;
  - une plage jouable proposée ;
  - la preuve de l'effet.
- Le panel figure dans le [rapport axe 1](reports/2026-11-14-axe1-hyperparametres.md),
  § « Panel de politiques jouables », et dans le prétirage
  `v2/papers/axe1-hyperparametres/`.
- **Plages sourcées ou dérivées :**
  - abandon IFSI de 0,056 à 0,105 par an (dérivé de ρ) ;
  - places × [0,8 ; 1,2] (DD76) ;
  - cumul × [0,5 ; 2] (plan de l'axe 5) ;
  - report de la retraite de 0 à 2 ans.
- **Plages supposées :** postes d'internat ±20 %, DES odontologie de 100 à
  160, diplômés étrangers × [0,5 ; 2], durée d'obligation de 0 à 3 ans,
  θ ∈ [0,5 ; 1].
- Les défauts de `formation.abandon` (0 → 0,105 pour les IDE) et de
  `sorties.part_cumul` (0,10 médecins → valeurs par profession) sont
  **proposés** à l'axe 0, qui possède le code, par message du 2026-11-14.
  L'axe 1 ne modifie pas `v2/jumeau/`.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : le but est de permettre au
décideur de « jouer dans l'interface graphique sur un grand panel de
politiques publiques applicables ».
**Ce qui le renverserait.** L'axe 5 montrant qu'une politique ne déplace
pas N(2050) : elle resterait au panel, mais sans priorité de sourçage.

## 2026-11-14 — Axe 3 : prétirage `v2/papers/axe3-validation/` (choix de rédaction)

**Décision.**
- L'article présente les **cinq** niveaux (N1–N4 gelés à 02:54, N5 à 03:46)
  et dit que N5 a été gelé après le lancement de N3.
- **N3 IDE est rapporté tel quel : levier non validé** (T1, p = 0,043).
  Les analyses de Rambachan & Roth et de tendance prolongée sont dans une
  sous-section marquée exploratoire.
- **N1 :** le premier passage confirmatoire est celui de l'axe 2 (rapport
  axe 2), cité comme tel ; l'axe 3 ne l'a pas relancé.
- **Comparateur externe de N3 :** IRDES QES n° 270 (DiD sur le zonage 2011,
  2006–2016), lu par l'axe 1.
- **Références vérifiées en texte intégral dans cette session :**
  Conseil d'État n° 357594 et Rambachan & Roth (2023, RES 90(5), 2555–2591,
  définition de Δ^RM(M̄) lue p. 9). Les autres viennent de bibliographies
  déjà vérifiées par les autres axes.
- Figure en pgfplots dans la source (pas d'image), avec `\usetikzlibrary{babel}`
  ajouté dans `main.tex` ; le préambule commun n'est pas modifié.
- Source non compilée (aucun moteur TeX installé).

**Pourquoi.** Consigne de la session v2 (2026-11-14) : un prétirage par axe,
chaque nombre avec sa provenance, références lues seulement.
**Ce qui le renverserait.** Une compilation qui échoue, ou un second test
N3 pré-enregistré qui passe (l'article serait alors révisé).

## 2026-11-14 — Programme de l'axe 2 : modèles en boîte blanche sur la structure par cohortes

**Décision.**
- L'axe 2 suit le programme de
  [l'état de l'art](explorations/2026-11-14-etat-de-lart-methodes.md), dans
  cet ordre :
  1. modèle âge-période-cohorte bayésien des sorties ;
  2. cohortes par composantes en bayésien hiérarchique (commune ⊂
     département ⊂ région) ;
  3. logit conditionnel d'installation, la régulation devenant un ensemble
     de choix restreint ;
  4. réconciliation MinT entre échelles ;
  5. validation par CRPS, PIT, calibration par simulation et mondes
     simulés.
- **Critère d'acceptation de chaque modèle** : un statisticien extérieur
  le vérifie en une demi-journée à partir du prétirage seul. Pour cela :
  - les équations tiennent sur une page ;
  - chaque paramètre a un a priori écrit, une source de données et un
    sens ;
  - la calibration par simulation est faite ;
  - les contrôles prédictifs a posteriori sont faits ;
  - le modèle est évalué hors échantillon contre les références naïves,
    selon le protocole de l'axe 3 ;
  - le code, les graines et les données sont ouverts.
- Toute référence est lue en texte intégral avant d'être citée.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « recherche méthodologique
poussée […] SURTOUT PAS BOITE NOIRE, vérifiable et validable par n'importe
quel statisticien », puis « Oui, axe 2 ».
**Ce qui le renverserait.** Un modèle du programme qui ne bat pas le
stock-flux à taux locaux sur le banc. Dans ce cas, il reste comme variante
documentée, sans devenir le défaut.

## 2026-11-14 — Règle de commit des sessions de recherche

**Décision.** Chaque session commite son travail dès qu'il est **validé**,
c'est-à-dire dès qu'une de ces conditions est remplie :
- ses critères d'acceptation passent ;
- un rapport est classé ;
- un prétirage compile ;
- pour le jumeau, une revue est passée.

Règles, parce que toutes les sessions partagent la même copie de travail
sur `main` :
- `git add` **uniquement des chemins nommés que la session possède**
  (table « Qui possède quoi »), avec ses rapports, ses fiches et son
  dossier `v2/papers/axeN-…/`. **Jamais** `git add -A` ni `git add .`.
- Les fichiers partagés (`v2/docs/lab/decisions.md`, `open.md`,
  `Home.md`, `v2/ROADMAP.md`, `.claude/`) sont commités par la session
  coordinatrice (v2).
- Avant chaque commit, `git diff --cached --stat` vérifie que rien de
  `data/`, `v2/data/raw|processed/` ni aucun fichier des organisateurs
  n'est indexé. Le `.gitignore` les exclut déjà ; on vérifie quand même.
- ~~Message en français, `axeN : …`, avec la ligne d'attribution
  Co-Authored-By.~~ **Corrigé le 2026-11-14** : message en français,
  `axeN : …`, **sans aucune mention de Claude ni ligne Co-Authored-By**
  (`CLAUDE.md` § Git, et la décision « Dépôt git autonome, commits sans
  mention de Claude »). Mon erreur : la règle contredisait une décision
  déjà inscrite, ce que l'axe 3 a relevé. Les commits 3849a4e, 5a9718b,
  aa265cf et 7e427b6 portent la ligne. Ils ne sont pas poussés ; les
  réécrire dépend de l'utilisateur·rice. **Réécrits le 2026-11-14 avec l'accord de
  l'utilisateur·rice** (commit-tree + update-ref atomique, arbres
  identiques, non poussés) : 3849a4e→d44c6d4, 5a9718b→66179d3,
  aa265cf→5c16a3a, 7e427b6→ad2e98f, b2756d8→72812c8.
- **Pas de push** sans demande explicite. Pas de changement de branche.
- Si `.git/index.lock` existe : attendre et réessayer, ne jamais le
  supprimer.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « pour chaque sous-session,
quand qqch est validé, n'hésite pas à commit ».
**Ce qui le renverserait.** Un conflit d'index répété entre sessions. On
passerait alors à des worktrees par axe.

## 2026-11-14 — Jumeau : défauts sourcés de l'axe 1 (abandon IDE, cumul par profession, régulation θ et destination)

**Décision.** Les valeurs des fiches de l'axe 1 deviennent les défauts du jumeau (`v2/jumeau/`).
- **`formation.abandon`** : il devient une valeur par profession.
  - IDE : 1 − 0,718^(1/3) ≈ 0,105 par an. Le chiffre est dérivé du
    rendement ρ = 0,718, mesuré sur l'entrée 2022 (DREES, jeu 491 ;
    fiches `param-ide-rendement-diplomes` et `param-ide-abandon-1a`).
  - Autres professions : 0, supposé.
  - **Remplace** 0,0 avec la mention « IDE ≈ 30 % à vérifier », qui
    n'avait pas de source primaire.
- **`sorties.part_cumul`** : il devient une valeur par profession.
  - SF 0,008 · CD 0,047 · PH 0,018 · MK et IDE 0,015 (COR 2016, doc. 11,
    données au 30/06/2015, fiche `param-cumul-emploi-retraite`).
  - Spécialistes : 0,10 (ER 1097).
  - **Remplace** 0,10 pour toutes les professions.
- **Régulation.**
  - Nouveau paramètre `theta` = 0,80, supposé (axe 3, N3, fiche
    `param-regul-theta-fuite`) : seule cette part de l'excédent est
    bloquée.
  - Les entrants bloqués se répartissent selon `repartition` (voisine,
    salariat, sortie). Défaut : **100 % voisine**, supposé (fiche
    `param-regul-report-entrants`, statut non mesurable).
  - **Remplace** la destination unique `bloques`, qui ne reçoit plus que
    la part « salariat ».
  - Au département et au-dessus, la part « voisine » reste dans sa
    cellule, si bien que **la régulation par défaut n'a aucun effet à ce
    grain**. À la commune, elle exige une table `voisins` (sinon,
    erreur).
  - La part « sortie » est inscrite au compte `regulation_sortie`.
  - `part_exemptee` par profession : les dentistes spécialistes (ODF, CO,
    MBD) sont exemptés (convention 2023, art. 35.5), mais leur part n'est
    pas mesurée dans nos données. Défaut 0, non mesurable.
- **Non codé** :
  - la règle IDE des 2/3 d'activité en périphérie : c'est une contrainte
    d'activité, pas d'effectif, donc hors du modèle ;
  - l'obligation de 2 ans en zone sous-dotée pour les kinés diplômés à
    partir de 2027 : il faudrait suivre l'ancienneté d'installation (ledger).

**Pourquoi.** Fiches de l'axe 1, transmises le 2026-11-14. Un paramètre
sourcé remplace un défaut supposé. La destination par défaut suit la
proposition de l'axe 1 (commune voisine).
**Conséquence.** La régulation avec ses paramètres par défaut ne produit
aucun effet au département. Pour voir le mécanisme à ce grain, il faut une
répartition avec « salariat » ou « sortie » (les tests C2 et C4 utilisent
100 % salariat). Le prototype et l'axe 5 sont concernés.
**Ce qui le renverserait.**
- Une source qui chiffre la destination des entrants bloqués.
- Une table de voisinage communale (axe 4), qui rendrait la part
  « voisine » visible à la commune.

## 2026-11-14 — Jumeau : corrections après la troisième revue (bornes composées, JSON, retraite multi-tranches, règle de régulation testée)

**Décision.** Le code est dans `v2/jumeau/`, et le critère C13 de
`jumeau.check` couvre ces règles.
- **Bornes sur la valeur composée.**
  - `Scenario.validate` calcule la valeur résolue aux années où elle
    change, si bien que des événements `mul`/`add` empilés sont bornés
    ensemble. Il refuse aussi toute valeur non finie (NaN, ∞).
  - `Context.param` borne à l'exécution toute valeur touchée par le
    scénario, y compris un paramètre ajusté (`sorties.retention` × 1,3 est
    refusé).
- **Événements réservés aux paramètres numériques.** Un paramètre dict,
  chaîne ou booléen (`regulation.zones`, `repartition`…) se fixe par
  `params`.
- **JSON.** `to_dict` écrit `modules = None` quand le scénario n'a pas de
  composition propre : après un aller-retour, `over()` garde la
  composition de la base.
- **Retraite avec plusieurs tranches ≥ 65.** On applique e' = e/(1+λe) à
  toutes les tranches ≥ 65, avec λ calculé par cellule.
  - λ est choisi pour que le temps espéré en 65+ d'une personne qui entre
    en 65–69 augmente de Δ exactement. Le calcul passe par une chaîne de
    Markov, avec le vieillissement f et la rétention s, dans l'ordre du
    moteur.
  - Avec une seule tranche ouverte, λ = Δ (B1 inchangé).
- **Régulation.** Seules les entrées positives de l'année comptent comme
  entrées : une entrée nette négative n'est pas « bloquée ».
- **Règle « entrées ≤ sorties » testée contre une formule indépendante.**
  On rejoue une année à la main, puis on compare au calcul
  θ · max(Σ entrées⁺ − Σ sorties, 0).
- **Une mutation par défaut.** Les mutations sont rejouées dans le
  scratchpad de la session, et chacune fait échouer C13.

**Pourquoi.** La troisième revue (rapport
`reports/2026-11-14-revue-adversariale-axe0-v3.md`) ne trouve plus de
défaut bloquant, mais confirme 4 défauts importants et 3 constats non
vérifiés, dont « C2 et C4 ne testent pas la règle ».
**Ce qui le renverserait.** Une quatrième revue qui trouve une valeur
composée hors bornes atteignable.

**Écart signalé.**
- Le prototype borne la retraite à [−2 ; 3] côté serveur.
- Le jumeau borne `decalage_retraite` à [0 ; 5] : un report négatif n'est
  pas défini par B1, et il est refusé.

## 2026-11-14 — Axe 3, N6 : prévision probabiliste (CRPS, PIT, SBC), ajoutée par un nouveau protocole (gel 03:53)

**Décision.**
- Nouveau protocole daté, qui **ne modifie ni N1 ni N5** :
  [N6](reports/2026-11-14-axe3-n6-probabiliste.md), copie immuable dans
  `v2/validation/preregistered/`, SHA-256 `d1cc665cb864`. Les empreintes de
  N1 à N5 ont été revérifiées, intactes.
- **Score :** CRPS sous sa forme par échantillon, sur **log N** (diviser par
  y le rendrait impropre), à h = 5, avec le critère bootstrap de N1.
- **Distribution prédictive d'un estimateur ponctuel :** prédiction ×
  exp(e), e tiré dans ses erreurs log passées (cible ≤ origine courante), au
  moins 20 erreurs.
- **Calibration :** couverture à 80 % dans [75 ; 85] % et à 50 % dans
  [44 ; 56] %. L'histogramme PIT et son χ² sont rapportés sans être
  décisifs (départements non indépendants). Une bande qui échoue est
  affichée avec sa couverture mesurée.
- **SBC** sur 200 mondes N5 (M3), L = 99, χ² sur 20 classes, p ≥ 0,01 avec
  Bonferroni.
- Conséquence dérivée : à h = 5, seule l'origine 2021 est jugeable, et
  seulement pour SF, CD et PH.
- Références lues dans le texte : Gneiting & Raftery 2007 (JASA 102(477),
  359–378, CRPS éq. 20–21 p. 367), Gneiting, Balabdaoui & Raftery 2007
  (JRSS-B 69(2), 243–268), Talts et al. 2018 (arXiv 1804.06788, § 4.1).
- Le prétirage `v2/papers/axe3-validation/` compile avec tectonic 0.17.0,
  sans citation indéfinie ni débordement.

**Pourquoi.** État de l'art de l'axe 2 (§ 3.6), transmis par la session v2 :
la MAPE ponctuelle ne juge pas les bandes que le jumeau affichera.
**Ce qui le renverserait.** Trop peu d'erreurs passées pour bâtir la
distribution empirique : N6 attendrait alors les tirages de l'axe 5.

## 2026-11-14 — Chantier « brancher les leviers » : formation, diplômés étrangers, sorties, installation

**Décision.**
- L'axe 0 branche dans le jumeau les leviers dont l'effet est sourcé, dans
  cet ordre :
  1. **formation** : quotas par profession et par région, abandon et
     capacité avec les valeurs sourcées par l'axe 1, et un lien entre
     diplômés et entrées ;
  2. **diplômés étrangers** : un flux séparé, par profession ;
  3. **sorties** : cumul emploi-retraite avec les taux par profession,
     départs précoces ;
  4. **installation** : la régulation étendue par profession et par part
     de zones, l'exemption on/off. L'obligation d'exercice et les aides
     incitatives attendent le logit d'installation de l'axe 2 ; on ne
     leur invente pas d'effet.
- La session v2 expose ensuite ces leviers dans le prototype.
- Chaque levier doit avoir :
  - un `Param` avec sa source, son unité, ses bornes et son statut ;
  - un test qui échoue si l'effet est retiré ;
  - quand une source chiffre l'effet, une comparaison à ce chiffre.
- **Hors du chantier, pour l'instant** : les leviers de demande (transferts
  de tâches). Ils demandent un module de besoin, et les sorties actuelles
  sont des effectifs. La question reste ouverte.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « pas assez de leviers
d'action », puis « Oui, lancer ».
**Ce qui le renverserait.** Un levier dont l'effet n'a aucune source ni
aucun mécanisme : il reste au catalogue et n'est pas branché.

## 2026-11-14 — Axe 4 : grain communal — Annuaire Santé pour l'instantané, CartoSanté pour l'histoire, projection au bassin de vie / EPCI ou au département

**Décision.**
- **Annuaire Santé (ANS, extraction libre accès du 2026-11-13) = source de l'instantané communal** pour les
  5 professions, y compris pharmaciens et sages-femmes : commune de chaque activité, civilité (sexe), mode,
  secteur, FINESS, section de l'Ordre, origine du diplôme. Pas d'âge, pas d'archive ouverte trouvée.
  - **Statut par personne** (décision « libéral = privé ») : une activité libérale → privé (mixtes inclus) ;
    sinon une activité publique → public ; sinon ambigu ; sinon privé. Statut d'une activité : FINESS juridique
    si présent (47 % des lignes), sinon code secteur RPPS. Le lieu se répartit 1/k sur les k activités.
  - Code département vide dans l'extraction : dérivé du code commune.
- **CartoSanté `*_popage` = source de l'histoire communale** (IDE, MK, CD, 2004/05/06–2025, 5 tranches d'âge).
  Marseille ajoutée par ses arrondissements (2010–2025, ordre croissant, contrôlé). **SF rejetées** : les
  modalités `age_sf` sont libellées en années et les lignes cassent la grille après 10 ans.
- **CartoSanté `*_flux` ne sont pas des installations** : ce sont des « pôles d'attraction » (patients). Aucune
  source ouverte de flux d'installation par commune n'a été trouvée ; le proxy est la variation nette du stock
  communal par tranche d'âge (CartoSanté).
- **Infirmiers dans le jumeau :** BTS dép × secteur croisé avec les salariés dép × âge × sexe sous H_ind
  (secteur indépendant de l'âge et du sexe dans un dép.). Test posé avant : part de femmes privé − public
  ≤ 3 points en médiane → **non rejetée** (2,1 points, Annuaire). L'âge n'est pas testable.
- **Grain projetable recommandé** (seuil : médiane ≥ 30 professionnels privés par unité, soit un bruit de
  Poisson ≤ 18 %) :
  | Profession | Médiane commune / BV / EPCI / dép. | Grain projetable |
  |---|---|---|
  | Infirmiers | 0 / 35,5 / 53 / 1 644 | bassin de vie ou EPCI |
  | Kinés | 0 / 17 / 23 / 615 | EPCI avec emprunt de force (hiérarchique) ; sinon dép. |
  | Pharmaciens | 0 / 11 / 16,5 / 444 | dép. ; EPCI seulement en hiérarchique |
  | Dentistes | 0 / 6 / 8 / 261 | dép. |
  | Sages-femmes | 0 / 1,5 / 2,5 / 78 | dép. |
  La commune reste un grain **d'observation et de répartition** (part du dép. ou de l'EPCI), avec bande.
  - **Remplacé le 2026-11-14 par N10 (axe 3)** pour l'affichage : aucun grain infra-départemental n'est fiable
    avec les estimateurs actuels ; projection au département, observé seulement à la commune. Les médianes
    ci-dessus restent valides comme description des petits effectifs ; le grain « projetable » n'est plus
    qu'une condition nécessaire, que le modèle hiérarchique doit confirmer par N10.

**Pourquoi.** Mesuré : 30,6 % (IDE) à 69,8 % (SF) des professionnels privés exercent dans une commune de moins
de 30 confrères ; au bassin de vie, 5,8 % (IDE) à 38,6 % (SF). Contrôles : CartoSanté Σ communes vs RPPS
libéral + mixte, même année, kinés −3,2 % et dentistes −0,8 % en 2025, infirmiers vs SNDS +4,7 % en 2023 ;
Annuaire privé vs centrale DREES 2026 par dép., écart médian −3,2 % (PH) à −14,6 % (IDE, BTS 2023).

**Rejeté :** projeter à la commune sans modèle hiérarchique ; lire SF dans CartoSanté par position.
**Ce qui le renverserait.** Un modèle hiérarchique (axe 2) dont l'erreur par commune, sur le banc, reste
sous celle du dép. réparti ; une archive datée de l'Annuaire (flux individuels).

## 2026-11-14 — Jumeau : leviers branchés (former, attirer, installer, retenir)

*Correction du 2026-11-14, d'après l'audit des sources de l'axe 1 :*
- *DD76 donne ±9 % en 2050 pour ±20 % de quotas, et non ±12-13 % : notre
  +9,1 % concorde.*
- *Les ≈ +14 % d'ER 1319 sont des places. Leur équivalent en effectifs
  est d'environ +7,9 % en 2050, contre +15,6 % dans le jumeau : c'est un
  écart.*
- *Le repère retraite de la DREES (≈ +1 %) n'est pas comparable à notre
  mesure.*
- *Les « comparaisons » ci-dessous sont remplacées par ces trois points.*

**Décision.** Ce qui est livré dans `v2/jumeau/`, couvert par le critère
C14 et par une mutation par levier.
- **Greffons qui ajoutent un écart au tendanciel.** `entrees` n'est pas
  réécrit. Les nouveaux leviers ajoutent l'écart qu'ils produisent :
  ils valent l'identité exacte à leur défaut (composition `LEVIERS`,
  écart 0,0 mesuré), et C1 est intact.
- **Former.**
  - `formation.capacite` : places en 1re année, avec un sélecteur
    `profession`.
  - `formation.abandon` : par profession ; IDE 1 − 0,718^(1/3) par an.
  - `lien_formation` (nouveau module) ajoute
    (1 − part étrangère) · entrées⁺ · (k − 1), où k = diplômés /
    diplômés d'un vivier de référence suivi en parallèle, ce qui donne
    k = 1 au tendanciel.
  - Le vivier est relatif et stationnaire quand l'état n'en fournit pas
    (L_p de la v1, supposé).
  - Quotas régionaux : `entrees.multiplicateur` avec
    `selecteur_region(code)`. Le délai suit la convention v1 :
    origine + L_p + 1.
- **Attirer.** `etrangers` (nouveau module) isole la part étrangère des
  entrées positives :
  - part = flux cité / Σ I⁺ (SF 70, CD 665, MK 1 175 par an ; PH et IDE
    non publiés, donc 0) ;
  - le module multiplie cette part, et `lien_formation` ne touche que le
    reste. Il n'y a donc pas de double compte.
- **Retenir.**
  - `sorties.multiplicateur_precoces` : e[âge < 60] × m (supposé) ;
  - `decalage_retraite` et `cumul_multiplicateur` reçoivent leur famille.
- **Installer.**
  - `regulation.part_zones` : part des zones listées, prises dans l'ordre
    de priorité de la liste ; 0 retire la régulation.
  - `regulation.part_exemptee` : 0 à 1, à la place d'un interrupteur, car
    la part des dentistes spécialistes n'est pas mesurée.
  - La régulation plafonne aussi les entrées ajoutées par `lien_formation`
    et `etrangers` (flux optionnels, nouveau champ `Module.optional`).
- **Pas branchés, faute d'effet sourcé :**
  - l'obligation d'exercice ;
  - les aides incitatives, qui attendent le logit d'installation de
    l'axe 2 ;
  - les filières en pharmacie et les postes de DES, faute de module.
- **Métadonnée.** `Param.famille` ∈ {former, attirer, installer, retenir}
  (provisoire, à confirmer par l'utilisateur·rice).

**Comparaisons aux chiffres cités** (C14 ; « cité » = repris de l'axe 1,
non relu ici) :
- capacité dentistes × 1,2 décidée en 2026 : 0 jusqu'en 2032, puis +9,1 %
  en 2050 (mesuré). DD76 cite ±12-13 % pour ±20 % de quotas. Notre effet
  est plus faible parce que l'exposition est plus courte : 17 ans
  d'entrants supplémentaires contre environ 25.
- IFSI, perte divisée par deux : diplômés × 1,196 (mesuré), soit
  +15,6 % d'IDE libéraux en 2050. ER 1319 cite environ +14 % de places :
  un rendement de base de 0,77 au lieu de 0,718 donnerait +14,9 %.
- retraite + 1 an en 2050 : kinés +1,55 %, IDE libéraux +3,02 %
  (mesuré). Le repère DREES cite environ +1 % ; l'écart pour les IDE est
  à expliquer (ledger).

**Pourquoi.** Décision « Chantier brancher les leviers ».
**Ce qui le renverserait.**
- Une source qui chiffre l'effet des départs précoces ou de l'exemption.
- Un logit d'installation de l'axe 2, qui remplacerait la répartition
  supposée des entrants bloqués.

## 2026-11-14 — Axe 5 : calcul sur un instantané figé du jumeau ; S1 sur Y centré ; levier retraite non marqué « biaisé »

**Décision.**
- **Instantané figé.** L'analyse de sensibilité tourne sur un instantané de
  `v2/jumeau/` pris à 04:14.
  - Empreinte SHA-256 des `.py` concaténés dans l'ordre trié :
    `c2dc760126b34239`.
  - Les critères C1–C14 de `jumeau.check` passent sur cet instantané.
  - L'instantané est placé en tête de `PYTHONPATH`.
  - **Remplace** l'exécution sur le dossier vivant : un calcul a planté le
    2026-11-14 à 04:14, car `module.py` changeait pendant le run.
  - Le jumeau avait déjà changé deux fois pendant l'analyse.
- **S1 est calculé sur Y centré.** Sur Y brut, l'estimateur S1 de Saltelli
  2010 donnait des valeurs de −0,34 à 1,78 (mesuré). ST (Jansen) est
  invariant par translation : il ne change pas.
- **Le levier retraite n'est plus marqué « biaisé ».** Après le correctif
  de l'axe 0, l'effet vaut 1,08 à 1,16 fois la variante B1 (mesuré),
  l'écart venant du demi-effet sur 55–59 ans. La troisième revue ne trouve
  plus de défaut bloquant. Avant le correctif, le rapport allait de 0,7 à
  1,85.

**Pourquoi.** Reproductibilité : un chiffre doit pouvoir être relancé sur
le même code. Consigne de la session v2 (2026-11-14) sur l'étiquette
retraite.
**Ce qui le renverserait.** Un correctif de l'axe 0 postérieur à 04:14 qui
touche `sorties`, `entrees` ou `vieillissement`. Il faudrait alors relancer
(≈ 15–25 min de machine).

## 2026-11-14 — Prototype : 9 leviers du jumeau exposés, rangés en 4 familles

**Décision.**
- `v2/prototype/` expose les leviers branchés par l'axe 0 (commit 063c192),
  rangés en **4 familles repliables** : Former, Attirer, Installer,
  Retenir. C'est la proposition faite à l'utilisateur·rice, et la même
  étiquette `Param.famille` existe dans le jumeau.
  - **Former** : places en formation, avec une option limitée à la région
    affichée.
  - **Attirer** : diplômés étrangers (sans effet pour les pharmaciens).
  - **Installer** : régulation, part des zones, destination des entrants
    bloqués.
  - **Retenir** : report de la cessation, cumul emploi-retraite, départs
    avant 60 ans.
- Chaque levier affiche deux badges : son délai d'effet, et sa preuve
  (sourcé ou supposé, lue dans le statut du `Param`).
- Les bornes sont validées par le serveur.
- Vérifié dans le navigateur : kinés, quotas +20 %, étrangers ×1,5,
  retraite +1 an, régulation vers le salariat → +25 007 en 2050 (+15,6 %),
  décomposé en entrées +20 665, étrangers +14 765, régulation −10 773,
  sorties +339. Recalcul : 77 ms aller-retour.
- **Limites affichées.** La destination « zone voisine » n'a aucun effet
  au département. Une part de zones qui arrondit à 0 zone revient à ne pas
  réguler : c'est le même arrondi que le jumeau, qui, lui, lève une erreur
  si la part est non nulle (défaut mineur signalé à l'axe 0).

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « Oui, lancer » (« … puis
expose-les dans le prototype ») et « devrait-on catégoriser les leviers
pour simplifier l'UX ? ».
**Ce qui le renverserait.** Un autre découpage choisi par
l'utilisateur·rice ; la question reste ouverte de son côté.

## 2026-11-14 — Axe 4 : flux communaux — proxy d'installations nettes (2012–2025) et archivage de l'Annuaire

**Décision.**
- **Proxy d'installations libérales par commune** (IDE, MK, CD ; `v2/data/build_flux.py`) :
  I_net(c, t) = ΔN_<40(c, t) + a_dep(t−1) · N_<40(c, t−1), avec a_dep = N_35–39 / 5 / N_<40 dans la
  pyramide du département (RPPS libéral + mixte ; SNDS pour les IDE). C'est un **solde** (entrées − sorties
  avant 40 ans, déménagements compris), pas un flux brut.
  - **Utilisable à partir de 2012 seulement :** T1 (Σ communes = même formule sur le pull départemental) passe
    à ≤ 0,2 % (MK, CD) et ≤ 1,6 % (IDE) en 2012–2025, échoue en 2006–2011 (jusqu'à 199 % pour CD 2009).
    *Corrigé le 2026-11-14 après l'ajout de Paris et Lyon par arrondissement :* ≤ 0,28 % (CD), ≤ 0,34 % (MK),
    ≤ 1,69 % (IDE) en 2012–2025 ; T2 inchangé (0,90).
  - **T2 échoue tel que pré-enregistré :** l'année sans diplômés kinés (2018) ne fait baisser I_net national
    qu'à 0,90 × la référence (seuil 0,8) ; minimum 0,87 en 2019. Le proxy ne voit qu'une fraction des
    promotions françaises. Explication possible, non mesurée : un tiers des kinés ont un diplôme UE.
  - Usage retenu : la **répartition** des installations nettes entre communes (variable dépendante du logit
    en parts), pas leur niveau national.
- **Archivage de l'Annuaire** (`v2/data/archive_annuaire.py`) : instantané réduit daté, sans nom, dans
  `v2/data/raw/annuaire/archive/` (non versionné), et flux agrégés entre deux instantanés (entrée, sortie,
  arrivée, départ, stable). Premier instantané : 2026-11-13. **Aucune tâche planifiée** : la fréquence est
  à décider (open.md).

**Pourquoi.** Aucune source ouverte de flux d'installation par commune (rapport grain communal).
**Ce qui le renverserait.** Deux instantanés de l'Annuaire espacés d'un an : ils donnent des entrées brutes
par commune, contre lesquelles on validera ou remplacera I_net.

## 2026-11-14 — Prétirage de synthèse ; un chantier long par axe pendant la nuit ; push sur GitHub

**Décision.**
- **Synthèse** : `v2/papers/synthese/`, régénérée par `build.py` à partir des six prétirages
  d'axe (étiquettes, citations et figures préfixées par axe, bibliographies fusionnées). Elle
  contient :
  - l'introduction, qui reprend la feuille de route ;
  - les parties « Interface et tests utilisateurs » et « Ce qui reste à faire ».

  Compile avec tectonic, sans référence indéfinie. Le PDF n'est pas versionné.
- **Chantiers de nuit envoyés aux six axes** :
  - axe 0 : vitesse à la commune et vivier réel ;
  - axe 1 : audit des sources en texte intégral et flux de diplômés étrangers ;
  - axe 2 : étape 2, bayésien hiérarchique ;
  - axe 3 : N6, SBC, N1 multi-origines, réconciliation DREES, DiD communale ;
  - axe 4 : flux d'installation communaux, FINESS, attributs des communes, script d'archivage
    de l'Annuaire ;
  - axe 5 : Sobol sur les 12 leviers, part décision / ignorance, carte des fourchettes.

  Garde-fous :
  - commits limités à leurs chemins, sans mention de Claude, sans push ;
  - téléchargements de données ouvertes de moins de 500 Mo ;
  - pas d'installation système ;
  - aucune tâche planifiée créée.
- **Push sur `origin/main`** (dépôt privé `progdinh/hackathon_acces_soins`), à la demande de
  l'utilisateur·rice. Les commits de la nuit seront poussés par la session v2 quand les axes
  auront rendu compte.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « create a big aggregate of all 5 axis paper work
until now with a big introduction that is the roadmap », « for each axis, launch a chronophage
work », « then push everything to github », « in the aggregated paper, tell the main things that
needs to be done next, and also the work on UAT ».
**Ce qui le renverserait.** —

## 2026-11-14 — Jumeau : chemin rapide à la commune (5 professions en ≤ 2 s)

*Remesuré le 2026-11-14 au matin, en isolant le test : 10 lancements de 3
runs, plus les opérations en place (`np.multiply(..., out=N)`, même
arithmétique, écart 0 vérifié). La machine était chargée par les
calculs des autres sessions (charge moyenne de 9 à 14). Résultats :
médianes de 2,0 à 4,6 s en temps réel et de 1,9 à 2,6 s en temps CPU.
**C15 échoue sous charge.** Les 1,35 à 1,57 s plus bas avaient été
mesurées sans relever la charge ; elles ne sont pas reproduites ce
matin. Il faut remesurer sur une machine au repos avant de déclarer
l'objectif atteint.*

**Décision.**
- `run(..., ledger=False, keep=…)` est le chemin rapide : il ne tient
  pas le registre des flux et garde les seules années demandées. Les ΔN
  ne sont calculés que pour les flux qu'un module lit (needs, optional).
  Le chemin complet reste celui par défaut, pour les tests.
- **Mêmes opérations flottantes, moins de passes :**
  - le vieillissement se fait sans `np.roll` ;
  - le facteur de sortie est mis en cache quand la rétention est
    l'objet ajusté et que les leviers ne changent pas ;
  - les entrées constantes sont calculées une seule fois.
- **Banc** `v2/jumeau/bench_commune.py`.
  - État communal ventilé par la population Insee, pour la mesure de
    temps uniquement : 5 professions, 2 secteurs, 698 212 cellules,
    24 ans, scénario retraite + quotas.
  - Mesure : **3,99 s avant, 1,35 à 1,57 s après** (médianes de 3 runs,
    sur une machine partagée avec d'autres sessions). Chemin rapide et
    chemin complet donnent le même état (écart 0). Critère C15.
- **Rejeté :**
  - passer en float32 : C1 perdrait l'écart nul ;
  - une grille précalculée : inutile sous 2 s.

**Pourquoi.** Chantier de nuit (session v2), objectif ≤ 2 s mesurées.
Profil mesuré avant tout changement (perf-investigation) :
- registre des flux, différences et sommes : 1,1 s ;
- passes `apply` : 1,0 s ;
- sorties recalculées : 0,8 s ;
- entrées : 0,5 s.

**Ce qui le renverserait.**
- Un état communal réel plus grand, par exemple avec des tranches d'âge
  fines.
- Une machine plus lente que 2 s. La marge est faible : un run isolé a
  pris 1,98 s.

## 2026-11-14 — Axe 5, partie 2 : Sobol sur les leviers branchés, part « décision » contre part « connaissance »

**Décision.**
- **Code.** Composition `LEVIERS` du jumeau, instantané tiré de `git
  archive` à HEAD, avec `v2/jumeau` au commit 4721268 (empreinte
  `a8cb275013495f8e`).
- **Groupes de facteurs.** Les indices de Sobol sont calculés par groupe,
  avec un plan A_B^(G) par groupe.
  - **Décision.** Facteurs que le décideur règle :
    - quotas × [0,8 ; 1,2] après L_p ;
    - `formation.capacite` × [0,8 ; 1,2] ;
    - `decalage_retraite` [0, 2] ans ;
    - `cumul_multiplicateur` [0,5 ; 2] ;
    - `multiplicateur_precoces` [0,5 ; 1,5] ;
    - abandon IFSI [0,056 ; 0,105] (IDE) ;
    - diplômés étrangers × [0,5 ; 2] (SF, CD, MK) ;
    - `part_zones` [0, 1] (0 = pas de régulation).
  - **Connaissance.** Facteurs de la partie 1, plus la réponse des acteurs
    à la régulation :
    - θ [0,5 ; 1] ;
    - destination des entrants bloqués {voisine, salariat, sortie},
      équiprobable ;
    - part exemptée [0 ; 0,06] (CD).
  - **Quotas et capacité** sont deux mécanismes d'une même politique
    (entrées × m contre vivier → entrées). On les garde tous les deux,
    séparés, et c'est signalé dans le rapport.
  - **Abandon IFSI** : il est classé « décision » (politique contre le
    décrochage). Sa plage vient pourtant de la donnée 2009–2022.
- **Zones de régulation au département** : départements où au moins 50 %
  des communes sont en « remplacement seul » (zonage actuel), même règle
  que `v2/prototype/server.py`. Pharmaciens : pas de zones, donc pas de
  facteur de régulation.
- **Statu quo** : `part_zones` = 0, ce qui correspond au tendanciel du
  jumeau.
- **Infirmiers.** Le périmètre passe au privé complet : table de l'axe 4
  `infirmiers_secteur_age_sexe.parquet`, statut privé, sous l'hypothèse
  H_ind. Il remplace, pour la partie 2, les libéraux seuls de la partie 1.
- **Taille.**
  - N = 512 : un run coûte 0,12 à 0,28 s (mesuré), dominé par le vivier
    en pandas du module `formation`.
  - 5 processus en parallèle, graine 20261114.
  - Fourchettes départementales : 500 tirages Monte-Carlo de la
    connaissance seule, décisions au statu quo.
- **Critère de convergence.** N suffit si, à 2050, chaque facteur de ST
  ≥ 0,05 vérifie deux conditions : son IC à 95 % est plus étroit que ST, et
  l'écart à la valeur à N max est inférieur à 0,05.
  - Partie 1 : le critère est atteint à N = 1024 partout (écart max 0,021,
    mesuré).
  - À N = 512, il échoue pour les IDE « incertitude » (écart 0,097).
  - Si la partie 2 échoue, on prolonge le plan par un second lot de lignes
    indépendantes.

**Pourquoi.** Consigne de la session v2 (2026-11-14), pour le chantier de
nuit : séparer la variance qui vient de la décision de celle qui vient de
la connaissance, puis prioriser la recherche.
**Ce qui le renverserait.**
- Des plages de leviers fixées autrement par le prototype ou l'axe 1, par
  exemple des quotas de 0,7 à 1,5 dans l'interface : la part « décision »
  dépend de l'amplitude jouable.
- Un module formation vectorisé, qui permettrait N = 2048.

## 2026-11-14 — Jumeau : vivier réel (DREES 491) et âge d'entrée des diplômés à l'étranger

**Décision.**
- **Source.** Le jeu DREES 491 (enquête Écoles, séries longues
  1966-2025 : inscrits en 1re année et diplômés) est téléchargé dans
  `data/raw/drees/491_formation_series_longues_1966_2025.xlsx`
  (121 774 octets, data.drees, données ouvertes). Le loader est
  `v2/jumeau/vivier.py`.
- **Durées en école :** IDE 3 ans, MK 4, SF 4 (réglementation).
- **Abandon annuel dérivé** du rendement ρ = diplômés(t) / inscrits 1re
  année(t − L), diplômés 2023-2025 :
  - IDE 0,101 par an, cohérent avec le 0,105 sourcé par l'axe 1, qui
    reste le défaut ;
  - **MK 0,016 et SF 0,033 par an**, nouveaux défauts (dérivés),
    remplaçant 0 (supposé).
- **`formation.vivier`** = `relatif` (défaut) | `reel`.
  - `reel` part des inscrits observés : 491 pour IDE, MK et SF, 990
    pour CD et PH.
  - Mesure : le modèle donne 25 385 diplômés IDE en 2024 (observé
    25 249) et 26 005 en 2025 (observé 26 020).
- **`lien_formation.mode`** = `levier` (défaut, identité au tendanciel)
  | `vivier`.
  - En mode `vivier`, k = diplômés du vivier / diplômés observés en
    moyenne sur la fenêtre d'ajustement, pour IDE, MK et SF.
  - Ce mode est une **variante d'estimateur, pas le défaut**. IDE
    libéraux en 2050 : +5,9 % par rapport au tendanciel.
- **Diplômés à l'étranger.** L'ajout entre dans la tranche qui contient
  `etrangers.age_entree` = 28 ans (DD76). Le total par cellule est
  inchangé.

**Mesures qui limitent la portée** (C16, exploratoire, non
pré-enregistré) :
- **Diplômés 2019-2025, abandon calibré sur 2016-2018 :** la
  persistance fait mieux que le vivier (MAPE IDE 3,2 % contre 8,4 % ;
  MK 3,1 % contre 5,9 % ; SF 4,1 % contre 4,4 %). L'abandon IDE a
  augmenté après 2018, et le vivier projette un rendement constant.
- **Stock d'IDE libéraux, 2018 → 2023 :** le mode `vivier` fait un peu
  mieux que le stock-flux local (MAPE par département 7,40 % contre
  7,82 %). Ce résultat repose sur une seule origine et n'a pas été
  pré-enregistré : il n'est pas encore une preuve. Il est à mettre au
  banc N1 de l'axe 3.

**Pourquoi.** Chantier de nuit (session v2). Le vivier relatif ne
servait qu'aux leviers. Les cohortes réelles sont l'information
publique la plus directe sur les entrées des 3 à 5 années suivantes.
**Ce qui le renverserait.** Le banc N1 (axe 3) départageant `vivier` et
le stock-flux local sur plusieurs origines.

## 2026-11-14 — Les « prétirages » sont des récapitulatifs scientifiques complets, sans les codes arXiv

**Décision.**
- Les articles d'axe et la synthèse gardent la forme d'un article (plan, équations, résultats
  étiquetés, bibliographie vérifiée). On retire :
  - le résumé anglais ;
  - la mention « prétirage » ;
  - la mention « non relu par des pairs ».

  La date devient « Version du … ». Cela remplace la partie « en français avec un résumé anglais »
  de la décision « Chaque axe de recherche produit un prétirage au format arXiv ».
- Gabarit et synthèse modifiés ici. Chaque axe applique le changement à son `main.tex` à sa
  prochaine mise à jour : les sessions travaillent en ce moment sur ces fichiers, et une
  modification croisée écraserait leur travail.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « quand je dis "comme un preprint", pas besoin
d'un abstract en anglais, ni de relu par les pairs etc, juste c'est un recap scientifique
complet de ce qui a été fait ».
**Ce qui le renverserait.** Une soumission réelle à arXiv ou à une revue.

## 2026-11-14 — Axe 5 : fourchettes départementales et seuil « assez sûr pour décider »

**Décision.**
- **Composante (a) au département** : (P95 − P5) / N tendanciel à 2050,
  sur 500 tirages de la connaissance seule, décisions au statu quo.
- **Composante (b) au département** : pente de l'APE ∝ h, par
  département, sur le banc N1 (N ≥ 30 à l'origine), × 1,6 × h. Les deux
  composantes ne sont jamais additionnées.
- **Seuil « assez sûr pour décider »** (dérivé) : la largeur (a) d'un
  département est inférieure à deux fois l'effet national à 2050 de
  quotas × 1,2, mesuré par profession. Le levier le plus fort se distingue
  alors de la bande de connaissance.
  - Quatre classes : < seuil, 1–2×, 2–4×, > 4×.
  - Le seuil porte sur (a) seulement : (b) n'existe pas au-delà de
    h = 10.
- **Carte.**
  - Fond v1 `app/assets/departements-avec-outre-mer.geojson`, hexagone
    seulement (DROM dans le tableau).
  - Rampe bleue ordinale (skill dataviz).
  - Formats : SVG pour le rapport, TikZ pour le prétirage, car pdfLaTeX
    n'inclut pas le SVG.

**Pourquoi.** Consigne de la session v2 : une carte de la largeur relative
qui montre où le modèle est assez sûr pour décider. Le seuil se rattache à
l'effet d'un levier mesuré, plutôt qu'à un pourcentage arbitraire.
**Ce qui le renverserait.** Un autre levier de référence que les quotas
± 20 %, par exemple l'amplitude de l'interface (0,7 à 1,5) : le seuil
changerait.

## 2026-11-14 — Axe 1 : SAE et PMI comme sources de recoupement de la part privée des salariés

**Décision.**
- La part privée des salariés hospitaliers est recoupée avec deux sources
  indépendantes du RPPS :
  - la **SAE** de la DREES (bases statistiques 2023-2025, bordereaux Q20 et
    Q23, statut juridique de l'établissement) ;
  - les **séries longues des salariés hospitaliers** (SIASP + BTS).
- Les sages-femmes de la catégorie RPPS « Prévention » sont rapprochées de
  l'enquête PMI de la DREES.
- Résultats, *mesurés* (fiche `param-part-privee-salaries-sae`) :

  | Profession | RPPS | SAE |
  |---|---|---|
  | Sages-femmes | 17,4 % | 19,8 % |
  | Kinés | 44,4 % | 44,3 % |
  | Pharmaciens | 17,4 % | 29,4 % |

  « Prévention » compte 1 383 sages-femmes, contre 1 423 en PMI.
- **Ce n'est pas un changement de la source du jumeau.** Celle-ci reste
  la décision de l'axe 4. Deux propositions lui sont faites (open.md) :
  - pharmaciens : retenir la SAE ou l'Ordre plutôt que le RPPS ;
  - sages-femmes : classer « Prévention » en public, ce qui réduit l'écart
    de 2 601 à 1 272.

**Pourquoi.** L'axe 5 classe la part privée des salariés ambigus en premier
facteur d'incertitude (ST 0,91 SF, 0,48 PH à 2050).
**Ce qui le renverserait.** Un appariement individuel RPPS × employeur
montrant que la SAE double-compte les multi-employeurs du privé.

## 2026-11-14 — Axe 3, N7 : addendum pré-enregistré (gel 04:37), DiD dans les bassins de vie, stabilité, bande « pente », réconciliation DREES

**Décision.**
- Protocole [N7](reports/2026-11-14-axe3-n7-addendum.md), SHA-256
  `06ba47b91647`, gelé avant tout calcul qui le concerne ; N1 à N6
  inchangés (empreintes revérifiées).
- **A.** DiD au grain du **bassin de vie 2022** (cellule BV × zone, Y ≥ 5
  en 2008, grappes = départements, CR1). Déclaré **second test** du levier
  IDE. Mêmes tests et seuils que N3.
- **B.** Verdict N1 par origine (2016, 2018, 2021), tous les estimateurs
  du registre ; « stable » = même signe de Δ aux trois origines ; τ de
  Kendall rapporté. Le verdict poolé de N1 reste celui qui compte.
- **C.** Bande « pente d'erreur » à armes égales : log N ~ N(log prédit,
  (s·h)²), s = RMS(e/h′) sur les paires passées ; CRPS gaussien.
- **D.** Cible ER 1319 (infirmiers libéraux, tendanciel) ; réconciliation
  des dentistes par valeurs de Shapley sur 3 facteurs (périmètre, origine
  et fenêtre, niveau des entrées), résidu ≤ 25 %.

**Pourquoi.** Consigne de nuit de la session v2 ; un ajout se fait par un
nouveau protocole daté.
**Ce qui le renverserait.** Rien sur la forme ; chaque ajout ultérieur sera
un nouveau protocole.

## 2026-11-14 — Axe 3, nuit : levier IDE toujours non validé ; aucune bande calibrée ; moteur biaisé par le bruit ; aucun chiffre 2050 citable

**Décision (verdicts des protocoles, appliqués tels quels).**
- **N3 second test (BV)** : T1 p = 0,025 et placebo de date +2,6 %
  [+0,1 ; +5,1] → design invalide ; effet −32 % [−37 ; −27]. Le levier IDE
  **reste non validé**. Kinés : tendances p = 0,059 au BV (échoue), écart
  des pentes +3,3 pts/an [+0,8 ; +5,8].
- **N1 stabilité** : au privé, le défaut gagne seulement à l'origine 2021
  (égalité en 2016 et 2018) ; τ ≤ 0,29. Affirmation admise : « meilleur que
  la tendance à l'origine 2021, égal ailleurs ». Ancien périmètre : stable.
- **N5** échoue : bruit de Poisson → MAPE dép. 10,2 % contre 5,7 % de
  plancher, biais national positif ; cohorte nombreuse lue comme des
  entrées (60+ −34 % à h = 5). M1, M6, M7 passent ; M5 de bon signe mais
  −19,8 % (prédit −12,4 ± 3).
- **N6** : aucune bande calibrée (bande empirique trop étroite, couverture
  « 80 % » de 56 à 70 %) ; à l'origine 2021, la persistance a le meilleur
  CRPS. **SBC** : rétention sans biais, **entrées biaisées vers le haut**
  (p = 3·10⁻⁴⁶).
- **N7-C** : tous les modèles battent la naïve en CRPS, mais la bande
  linéaire en h est **trop large** (« 80 % » couvre ~96 %).
- **N2-A** (forme affaiblie, entrées plates) échoue : −14 à −17 % sous DD76
  en 2050 ; la variante filière (exploratoire) le dépasse de 14–15 %.
  **ER 1319** échoue (−25 % en 2050), mais l'observé 2023 est déjà 5,9 %
  sous ER 1319. **Dentistes** : écart à DD76 expliqué (Shapley : origine
  et fenêtre +13,1 k, entrées récentes +11,7 k, périmètre −1,9 k ; résidu
  16 %).
- Conséquences : **aucun chiffre 2050 citable** ; **aucune bande publiable
  sous son niveau nominal** ; le mécanisme `min(r, 1)` + excédent en
  entrées est la cause commune de M3, M4 et de l'échec SBC.

**Pourquoi.** Rapports [N5](reports/2026-11-14-axe3-n5-mondes-simules.md),
[N6](reports/2026-11-14-axe3-n6-probabiliste.md),
[N7](reports/2026-11-14-axe3-n7-addendum.md),
[N2](reports/2026-11-14-axe3-n2-long-terme.md).
**Ce qui le renverserait.** Un nouveau protocole qui passe (bande en √h,
entrées séparées de la rétention, contrôle synthétique pour N3).

## 2026-11-14 — Tests des boucles de rétroaction : tester le signe avant de modéliser

**Décision.**
- **Axe 3** : pré-enregistrer (gel SHA-256) puis exécuter deux tests de signe, avec les données
  communales de l'axe 4.
  - **B2, densité → installations nettes** : les communes et bassins de vie peu denses
    attirent-ils plus d'installations des moins de 40 ans, à population et zonage contrôlés,
    pour IDE, MK et CD, sur 2012-2025 ?
  - **B1, densité → départs avant 60 ans** : la rétention des 45-59 ans est-elle plus faible
    là où la densité est faible, par département, avec le RPPS de 2012 à 2026 ?
  - Pour chacun : effet, intervalle et test placebo, puis un verdict (signe confirmé, nul ou
    contraire).
- **Axe 2** : si B2 est confirmé, la densité entre comme covariable estimée du logit
  d'installation (étape 3). Pas de sigmoïde supposée.
- **B1 confirmé ou non** : la boucle charge → départs reste un scénario de stress étiqueté
  « supposé », jamais dans le tendanciel. La charge suppose un module de besoin, toujours en
  question ouverte.
- **Contraintes pour toute boucle** : conservation du total national (K-cons), réallocation
  bornée par le flux d'entrants (≈ 3 %/an, H3), test d'oscillation (K-osc).

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « en fait si si », après la revue de l'analyse
transmise.
**Ce qui le renverserait.** Un signe nul ou contraire : la boucle n'est alors pas branchée.

## 2026-11-14 — Jumeau : flux de diplômés à l'étranger mis à jour (axe 1), variante basse gardée

**Décision.**
- **Nouveaux défauts de `etrangers.flux`** (fiche axe 1
  `param-diplomes-etrangers-flux`), par an :
  - CD 1 300, sourcé (Ordre 2022) ;
  - MK 2 200, dérivé (CNOMK 2024) ;
  - PH 240, dérivé ;
  - IDE 400, sourcé, confiance faible (ER 1319) ;
  - SF 80, dérivé.
- **Variante basse `FLUX_BAS`** (DD76, ER 1075, données 2015-2020) : SF
  70, CD 665, MK 1 175, PH et IDE 0.
- Les deux définitions diffèrent (reconnaissance ou primo-inscription
  contre entrée en activité). Le nouveau défaut est donc probablement un
  majorant.

**Conséquence mesurée.** La part étrangère des entrées positives
augmente : 0,47 pour les dentistes, contre 0,24 avant. Comme
`lien_formation` ne multiplie que la part formée en France, les autres
leviers baissent :
- capacité dentistes × 1,2 : **+6,3 % en 2050**, contre +9,1 % avec le
  flux bas. DD76 donne ±9 % : la concordance ne tient qu'avec le flux
  bas ;
- abandon IFSI divisé par deux : +14,1 % d'IDE libéraux, contre
  +15,6 % ;
- diplômés étrangers × 2 : +37,2 % de dentistes en 2050, contre +18,1 %.

**Pourquoi.** Valeurs plus récentes et sourcées. L'axe 5 mesure que ce
levier pèse beaucoup (ST 0,27 pour les MK, 0,17 pour les CD).
**Ce qui le renverserait.** Un flux d'entrées en activité (RPPS, par
année de première inscription) plus bas que les reconnaissances. Dans
ce cas, le défaut redeviendrait la variante basse, ou un point entre les
deux.

## 2026-11-14 — Axe 3, matin : cas limites L1–L3 passent ; N_min communal = 51 ; bande en √h calibrée (N8, gel 08:06)

**Décision.**
- **N2-B (cas limites, jumeau par défaut, privé)** : L1, L2 (N(o+200) = Q·C
  à −0,05 à −0,46 %, état initial sans effet) et L3 (1re année d'effet d'un
  quota = o + L_p + 1) **passent** pour les 5 professions. N2 reste en échec
  pour sa partie A (DREES à 2050).
- **N4** : **N_min = 51 professionnels**, fixé par les kinés (origines 2018
  et 2020) ; 21 pour CD et IDE seuls. Sous 51, une projection communale
  n'est pas affichée sans bande P10–P90, ou elle est agrégée. Bande calibrée
  dans 14 classes sur 21.
- **N8 (nouveau protocole, SHA-256 `97ef367fd221`)** : bande
  log N ~ N(log prédit, s²·h), s² = moyenne de e²/h′. Pour la variante par
  défaut : couverture 49,2 % (50 %) et 75,9 % (80 %) → **calibrée**, et
  gagne contre la tendance en CRPS (−0,0045 [−0,0070 ; −0,0020]). Forme
  suggérée par N7-C sur les mêmes origines : **à confirmer** sur le dépôt
  2027. C'est la seule bande qui peut être affichée sous son niveau nominal,
  avec cette réserve.
- N6, tirages propres de l'APC : 100 tirages au lieu de 200 (écart déclaré) ;
  égalité avec la persistance, couverture « 80 % » de 54 %.

**Pourquoi.** Rapports [N2](reports/2026-11-14-axe3-n2-long-terme.md),
[N4](reports/2026-11-14-axe3-n4-echelle-fine.md),
[N8](reports/2026-11-14-axe3-n8-bande-racine.md).
**Ce qui le renverserait.** Le dépôt 2027 hors de la bande en √h au-delà de
la tolérance de N6 ; une projection départementale réelle (au lieu de
l'oracle) qui relève N_min.

## 2026-11-14 — Axe 1 : flux de diplômés étrangers par profession, sources récentes plutôt que DD76

**Décision.**
- La fiche `param-diplomes-etrangers-flux` propose des flux récents :
  - CD **1 300 par an** : Ordre 2022, recoupé par les décisions de
    reconnaissance UE ;
  - MK **2 200 par an** : autorisations 2023 et hausse du stock ;
  - IDE **400 par an** : hypothèse DREES ER 1319 ;
  - PH **240** et SF **80** par an : dérivés de l'Ordre et de la DD76.
- Ces flux remplacent les valeurs DD76 / ER 1075 (CD 665, MK 1 175), qui
  datent de 2015-2020 et restent la variante basse.
- **Le défaut du jumeau reste la décision de l'axe 0** : proposition
  envoyée le 2026-11-14.

**Pourquoi.** L'axe 5 (partie 2) mesure ST 0,27 (MK) et 0,17 (CD) pour ce
levier à 2050. Les sources récentes donnent environ le double des valeurs
DD76.
**Ce qui le renverserait.** Une série d'entrées en activité (RPPS) par pays
de diplôme, qui donnerait un flux réel plus bas que les autorisations.

## 2026-11-14 — Axe 3 : prévisions 2027–2030 déposées avant le RPPS 2027

**Décision.** Dépôt prévu par N1 et N8 : variante par défaut, privé, origine
2026, cibles 2027, 2028 et 2030 par profession × département, avec les
quantiles 10–90 % de la bande en √h.
`v2/validation/depot/jumeau_taux_locaux_2026-11-14.parquet`, SHA-256
`ca036374d216`. Infirmiers libéraux exclus (série arrêtée en 2023). Totaux
nationaux 2027 : CD 47 835, MK 104 755, PH 63 311, SF 13 301. Le score sera
calculé à la publication du RPPS 2027 (vers juillet 2027), avec les critères
de N1 et N8, sans toucher au fichier.

**Pourquoi.** Seul test hors échantillon non contaminé par K1 ni par le choix
de la bande en √h.
**Ce qui le renverserait.** Rien : un dépôt ne se modifie pas ; une nouvelle
variante fait un nouveau dépôt.

## 2026-11-14 — Axe 4 : SF « Prévention » = public ; variante SAE pour les pharmaciens hospitaliers ; PLM et COG 2026 dans les tables communales

**Décision.**
- **Sages-femmes salariées en « Prévention » → public** (`OVERRIDE` de `build_secteur.py`), au lieu d'une
  part FINESS PMI de 0,07. Mesuré par l'axe 1 : 1 423 SF en PMI au 31/12/2024 (DREES, séries du personnel de
  PMI) pour 1 383 SF en « Prévention » au RPPS 2026. Fourchette « libéral » SF 2026 :
  **12 059 – 13 331 (centrale 12 819)**, largeur 2 601 → 1 272. *Remplace* la ligne SF de l'entrée
  « public / privé lu dans le secteur d'activité » (12 059 – 14 660, centrale 12 912).
- **Pharmaciens hospitaliers : la centrale reste celle du RPPS** (16,6 % de privés sûrs, 19,8 % au plus), car
  elle est par personne et croisée dép × âge × sexe. La SAE (29,4 %, axe 1) et l'Ordre (28,6 %) sont donnés en
  **variante mesurée** : +1 116 pharmaciens privés (63 612 → 64 728), dans la fourchette (max 67 219). L'écart
  RPPS / SAE n'est pas réconcilié (open.md).
- **Paris et Lyon par arrondissement** dans `commune_stock.parquet`, comme Marseille : séries complètes lues
  par position (ordre croissant jusqu'en 2025), reste « commune − arrondissements complets » donné aux
  arrondissements à série partielle. Contrôle : la nouvelle table = la table v1 + exactement l'écart du
  dép. 13 (2025 : CD +780, MK +1 886, IDE +2 695).
- **Codes commune anciens → COG 2026** (FINESS historique) par le fichier Insee des événements depuis 1943,
  appliqué transitivement, et conversion des codes FINESS DROM (9A…9F → 97…). Officines rattachées :
  96,2–97,3 % → **99,9 %** chaque année.

**Pourquoi.** Mesures de l'axe 1 (SAE, PMI) ; contrôles ci-dessus.
**Ce qui le renverserait.** Une source qui explique l'écart RPPS / SAE chez les pharmaciens (PUI des
établissements médico-sociaux, multi-inscriptions) : la variante deviendrait la centrale.

## 2026-11-14 — L'observatoire d'un collègue n'est plus cité comme dépôt : ses arguments sont intégrés au texte

**Décision.**
- Les articles ne citent plus le dépôt `evolutionsoin2026`. Il s'agit du
  travail d'un collègue, et le dépôt est privé. Sont concernés
  `papers/axe2-methodes`, `papers/axe3-validation` et
  `papers/synthese/parts.tex`.
- Ses arguments sont repris dans le texte comme hypothèses à tester, et
  présentés comme un « travail interne d'un membre de l'équipe, non
  publié » :
  - shrinkage département → région → national de poids 200 ;
  - taux de maintien bornés à [0,5 ; 1,2] ;
  - biais du vieillissement uniforme ;
  - sept mondes simulés.
- Les chiffres que nous n'avons pas reproduits (+8 à +19 % sur l'effectif
  des 60 ans et plus, −12,4 % à 15 ans) sont dits « rapportés par son
  auteur ». Leur étiquette « mesuré » est retirée.
- Les entrées bibliographiques sont supprimées. Les trois documents
  compilent (tectonic, sans erreur).

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « evolutionsoin2026 est un
travail fait par un collègue. Prends juste les arguments et intègre-les
dedans. »
**Ce qui le renverserait.** La publication du dépôt, qui permettrait de le
citer.

## 2026-11-14 — Axe 3, N9 : boucle densité → installations sans signe établi ; densité → départs confirmée pour les IDE seulement

**Décision.**
- Protocole [N9](reports/2026-11-14-axe3-n9-boucles.md), gelé à 08:10
  (SHA-256 `96a39bc087bb`) avant calcul.
- **B2** (BV × année, 2014–2025, densité décalée de 2 ans, effets fixes
  département et année, contrôles population, âge, zonages) : **nul** pour
  IDE (−1,52 [−4,05 ; +1,01]), MK (−1,66 [−3,43 ; +0,11]) et CD
  (+0,17 [−0,05 ; +0,39]). La densité des autres professions pèse autant ou
  plus : attractivité générale, pas saturation propre.
- **B1** (département × année, rétention 45–54 → 50–59 à 5 ans) :
  **confirmé pour les infirmiers libéraux** (+0,11 [+0,05 ; +0,18], placebo
  nul) ; nul pour SF, CD, PH, MK.
- Conséquences : l'axe 2 n'ajoute pas la densité comme covariable
  **confirmée** du logit d'installation ; la boucle charge → départs reste un
  scénario de stress « supposé » (seul le signe IDE est mesuré).
- **Corrections de citation dans l'article** (audit des sources, axe 1),
  sans toucher aux protocoles gelés : quotas DD76 ±9 / 12 / 13 % (la
  tolérance de N2 reste « au moins trois fois plus petite ») ; l'impropreté
  d'un score divisé par y n'est plus attribuée à Gneiting & Raftery 2007, et
  sa source (Gneiting & Ranjan 2011 ou Lerch et al. 2017) reste à vérifier.

**Pourquoi.** Décision « Tests des boucles de rétroaction » ; consigne de la
session v2.
**Ce qui le renverserait.** Des flux bruts d'installation (et non des
soldes), ou un instrument de la densité, qui feraient apparaître un signe.

## 2026-11-14 — Résultat des tests de boucles (N9) : densité → installations nulle ; densité → rétention confirmée pour les IDE seuls

**Décision.**
- **B2, densité → installations nettes : nul** pour les IDE, MK et CD (bassin de vie × année,
  2014-2025, protocole N9 gelé, SHA 96a39bc087bb).
  - Effets estimés : IDE −1,52 [−4,05 ; +1,01], MK −1,66 [−3,43 ; +0,11],
    CD +0,17 [−0,05 ; +0,39].
  - La densité des autres professions pèse autant ou plus : c'est une attractivité générale,
    pas une saturation.
  - → Le logit d'installation de l'axe 2 n'a **pas de covariable « densité » confirmée**. La
    densité y entre au plus comme covariable estimée, **sans a priori de signe**. Pas de
    sigmoïde.
- **B1, densité → rétention des 45-54 ans à 5 ans : confirmé pour les IDE libéraux seuls**.
  - Effet : +0,11 [+0,05 ; +0,18], placebo nul, soit ≈ +8 % de rétention quand la densité
    double (mesuré, corrélationnel).
  - Nul pour SF, CD, PH et MK.
  - → La boucle « départs plus fréquents là où la densité est faible » n'a une base
    empirique que pour les IDE. On la garde en **scénario étiqueté « estimé, IDE seuls,
    corrélationnel »**, pas dans le tendanciel. La brancher dans le tendanciel est une
    décision ouverte.

**Pourquoi.** [Rapport N9](reports/2026-11-14-axe3-n9-boucles.md), commit f1f4f41.
**Ce qui le renverserait.** Un test causal (expérience naturelle) qui contredit la
corrélation.

## 2026-11-14 — Axe 4 : corrections de l'audit des sources (axe 1) reportées ; double compte maïeutique marqué

**Décision.**
- Le registre `v2/data/events.csv` reprend les corrections de l'audit (lot C1) : 5 dates d'effet (IDE 2018 →
  20/07/2018 ; MK 2012 → 15/07/2012 ; objectifs 2021–2025 → 18/09/2021, bornes 76 655 – 85 455 ; plafonds →
  JO du 14/05/2026 ; officines → 31/07/2018) et 3 contenus (IFSI 2019, avenant 6 IDE, vaccination 2019).
  Registre : 24 lignes vérifiées, 6 partielles.
- **ev-sf-2023 (loi) et ev-sf-2024 (décret) sont le même choc** : on garde les deux lignes, qui sont deux
  textes distincts, mais la seconde est marquée « texte d'application, ne pas appliquer deux fois ». Un
  scénario n'en active qu'une.
- Article et rapports : chiffres corrigés d'après le lot C2 (moins de 25 ans MK 5 634 → 3 687, 5 137 ; 84 449 ;
  8 à 12 secteurs ; COM 977 / 978 ; 2 secteurs supposés à 0,5, soit 5 cellules) ; bibliographie (ER 1159 =
  Croguennec 2020 ; Atlasanté = ARS Aquitaine 2014 ; PS_LibreAcces.zip ; BTS / SNDS). « Génération 2012 » du
  zonage Atlasanté : présentée comme déduite.

**Pourquoi.** Audit des sources de l'axe 1 (`reports/2026-11-14-audit-sources.md`, lots C1 et C2).
**Ce qui le renverserait.** Un texte primaire contredisant l'audit sur une date d'effet.

## 2026-11-14 — Infirmiers branchés dans le jumeau et le prototype

**Décision.**
- `jumeau.history.sector_table(["infirmiers"])` lit la table de
  l'axe 4 `v2/data/processed/infirmiers_secteur_age_sexe.parquet` :
  - libéraux : SNDS, tous privés ;
  - salariés : BTS, ventilés public / privé, puis croisés avec âge ×
    sexe sous indépendance (H_ind).
- **Années 2013 à 2023 seulement.** En 2012, les salariés ne sont pas
  observés (le BTS commence en 2013).
- `variant` (min / central / max) est sans effet pour les infirmiers : le
  BTS tranche déjà le secteur.
- **Contrôle C18.** Le total par dep × année égale SNDS libéraux + BTS
  salariés (v1) à 7·10⁻¹² près, sur 1 100 dep × années. Le privé
  contient bien tous les libéraux. Mesure en 2023 : 277 788 dans le
  privé, 329 856 dans le public. Projection : 336 422 dans le privé en
  2050 (tendanciel).
- **Prototype** (`v2/prototype/server.py`) : `infirmiers` passe de
  MISSING à PROFS. `/api/scenario` et `/api/carte` répondent pour
  `prof=infirmiers` (vérifié par un serveur de test).

**Pourquoi.** Demande de l'utilisateur·rice (via la session v2),
2026-11-14.
**Ce qui le renverserait.** L'hypothèse d'indépendance âge × sexe ×
secteur pour les salariés (H_ind, axe 4) rejetée sur l'âge : la
répartition par âge du public et du privé serait alors à revoir.

## 2026-11-14 — Chantier « projection communale fiable » : l'axe 2 porte, l'axe 3 juge, l'axe 4 alimente

**Décision.**
- **Définition de « fiable »** à la commune : **calibrée**, c'est-à-dire que la bande à 80 %
  contient la valeur observée dans environ 80 % des cas au backtest, et pas « étroite ». Le
  bruit de Poisson est irréductible (≈ ±45 % pour N = 5, dérivé).
- **Axe 3** : lancer N4, le protocole d'échelle fine, déjà gelé. Il fixe le seuil N_min
  d'affichage sans bande, et le contrôle de couverture par classe de taille et par
  profession, à la commune, à l'EPCI et au bassin de vie.
- **Axe 2** : étendre le modèle de cohortes bayésien hiérarchique de l'étape 2 à
  commune ⊂ EPCI ⊂ département ⊂ région, avec rétrécissement partiel. Le juger sur N4.
- **Axe 4** : fournir les historiques communaux manquants :
  - pharmaciens, reconstitués à partir de FINESS et de l'Annuaire ;
  - sages-femmes, si une source ouverte existe ;

  ainsi que les tables de passage commune → EPCI / bassin de vie.
- **Affichage** : pour chaque profession, le grain le plus fin qui passe N4. En dessous, la
  carte montre l'observé à la commune avec la projection de l'échelon supérieur, et le dit.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « trouver l'axe qui nous permettra d'avoir
une projection fiable à l'échelle des communes », puis « Oui, lancer ».
**Ce qui le renverserait.** N4 montre qu'aucun modèle n'est calibré à la commune pour une
profession : elle reste alors à l'EPCI ou au département.

## 2026-11-14 — Axe 3, N10 : aucun grain infra-départemental n'est calibré pour IDE, MK et CD

**Décision.**
- Protocole [N10](reports/2026-11-14-axe3-n10-grain-couverture.md), gelé à
  08:31 (SHA-256 `d86d27c7a750`) : 3 grains (commune, bassin de vie, EPCI),
  bande P10–P90 empirique par classe de taille tirée des seules erreurs
  passées, « fiable » = couverture dans [75 ; 85] % dans chaque classe.
- **Verdict : aucun grain fin n'est fiable**, pour aucune profession ni
  aucun estimateur (persistance, tendance, répartition-tendance, oracle).
  En moyenne la couverture est proche de 80 % (IDE 81–84 %, MK 80–81 %,
  CD 72–79 %), mais par classe elle est trop large pour les très petites
  communes et trop étroite au-delà de 50 à 100 professionnels (22 à 59 %).
- **Grain d'affichage : le département** pour IDE, MK et CD, jusqu'à ce
  qu'un modèle (axe 2) passe N10. À la commune : l'observé, avec la
  projection de l'échelon supérieur, et la carte le dit.
- N_min (règle N4) par grain, estimateur principal : CD 21 partout ; IDE 51
  (commune), 11 (BV) ; MK 21 partout.

**Pourquoi.** Décision « Chantier projection communale fiable » : fiable =
calibrée, pas étroite.
**Ce qui le renverserait.** Le modèle hiérarchique de l'axe 2 qui passe N10
à un grain fin.

## 2026-11-14 — N10 : aucun grain infra-départemental n'est fiable avec les estimateurs actuels ; affichage au département

**Décision.**
- **Protocole N10** (axe 3, gelé à 08:31, SHA d86d27c7a750, commit 167d15d) :
  - grains commune, bassin de vie et EPCI ; professions IDE, MK et CD ; origines 2014–2020 ;
  - bande P10–P90 empirique par classe de taille ;
  - « fiable » = couverture dans [75 ; 85] % dans **chaque** classe de taille.
- **Verdict sur les estimateurs actuels** (persistance, tendance, répartition-tendance,
  oracle) : **aucun grain sous le département n'est fiable**, pour aucune profession.
  - La couverture moyenne est proche de 80 % : IDE 81–84 %, MK 80–81 %, CD 72–79 %.
  - Mais elle est mal répartie : 94 % pour les communes de 1 ou 2 professionnels, 22 à 59 %
    au-delà de 50 à 100 professionnels.
- **Affichage, jusqu'à nouvel ordre** :
  - projection au **département** pour IDE, MK et CD ;
  - à la commune, l'**observé** seulement.
- Le modèle hiérarchique de l'axe 2 est soumis au même protocole N10. Il ne change
  l'affichage que s'il passe.

**Pourquoi.** Le chantier « projection communale fiable » et sa définition de « fiable »
(calibrée).
**Ce qui le renverserait.** Le modèle de l'axe 2 passe N10 à un grain infra-départemental.

## 2026-11-14 — Axe 4 : données de la projection communale (pharmaciens reconstitués, SF non disponible, passage COG 2026)

**Décision.**
- **Pharmaciens par commune 2012–2026, reconstitués** (`v2/data/build_pharmaciens.py`) :
  - officine = officines FINESS (31/12/t−1) × ratio départemental DREES (pharmaciens d'officine / officines),
    Σ communes = DREES dép. par construction ;
  - hors officine = DREES dép. par statut × parts communales de l'Annuaire 2026, **tenues fixes** (supposé) ;
    repli sur les parts tous statuts quand un statut manque dans le dép.
  - Test posé avant : erreur absolue relative médiane ≤ 25 % (communes ≥ 5) et ≤ 10 % (EPCI) contre les
    pharmaciens d'officine de l'Annuaire. Mesuré : **16,1 % à la commune (passe), 10,7 % à l'EPCI (échoue de
    peu)** ; corrélation 0,98 ; total officine 50 196 contre 50 664 (−0,9 %). Verdict : **échec tel que
    pré-enregistré** ; utilisable avec une bande de ±11 % à l'EPCI (p90 33 %).
  - Mayotte 2012–2013 : pas d'officines FINESS, composante officine manquante (−62 à −71 % du dép.).
- **Sages-femmes : historique communal non disponible** en données ouvertes. Routes testées : CartoSanté
  `sf_popage` (métadonnées erronées), `sf_datcom.actifs` (sommes par position 6 896–7 549, incompatibles avec
  ameli 5 773 → 8 490 sur 2017–2025), `offre_ps.dens_sf` (lignes sans ordre, même pour les kinés), ameli
  (département seulement), Annuaire (instantané seul). Coût de la recherche : ~40 min. Repli : parts communales
  de l'Annuaire 2026 × série départementale, **modélisé, non observé**.
- **Table de passage** (`v2/data/build_passage.py`) : tout code commune (34 966 communes 2026, 45 arrondissements,
  4 213 anciens codes) → géocode du jumeau → EPCI → bassin de vie 2022 → dép. → région. Sans EPCI : COM hors champ
  et 4 communes insulaires sans EPCI (22, 29, 85).

**Pourquoi.** Chantier « projection communale fiable » (decisions.md) : l'axe 4 fournit les données à l'axe 2.
**Ce qui le renverserait.** Une archive datée de l'Annuaire ou une source SF communale datée.

## 2026-11-14 — Axe 5 : relance sur le jumeau b64ce56 et les données de 08:08 ; flux étranger en facteur « connaissance » ; IDE à partir de 2013

**Décision.**
- **Les deux phases sont relancées sur le jumeau `b64ce56`** (`git
  archive`, 19 critères au vert) et sur les données de 08:08.
  - Empreintes SHA-256 tronquées : `secteur_stock` `c784b1a8`,
    `infirmiers_secteur_age_sexe` `43ad2c58`, `zonage_commune`
    `4e5da69f`.
  - Elles remplacent les calculs sur `c2dc7601` (phase 1) et `a8cb2750`
    (phase 2).
  - Raison, mesurée : depuis `4721268`, l'effet du levier « étrangers × 2 »
    à 2050 a doublé (dentistes +19 → +38 %, MK +16 → +29 %). Le tendanciel
    SF passe de 19 124 à 21 176, et les SF de PMI sont classées publiques
    par l'axe 4.
  - Les anciens résultats sont gardés dans `out/avant_b64ce56/`.
- **Flux de diplômés à l'étranger : nouveau facteur « connaissance »**,
  {bas, haut}, avec les valeurs `FLUX_BAS` et `FLUX` du jumeau (CD 665 ou
  1 300 par an). Le levier « étrangers » s'applique désormais aux 5
  professions.
- **Infirmiers privés : années à partir de 2013.** En 2012, la table ne
  contient que les libéraux, d'où un saut fictif de +190 %. C'est la cause
  de la bande backtest départementale de ±460 %. Le défaut était dans
  `leviers.table`, pas dans `sector_table` du jumeau, qui commence en
  2013.
- **Amplitude des leviers : les deux variantes sont calculées**, pour
  éclairer la décision ouverte sans la prendre.
  - « dd76 » : quotas et capacité × [0,8 ; 1,2], retraite [0, 2] ans.
  - « interface » : quotas et capacité × [0,7 ; 1,5], retraite [0, 3] ans
    (`v2/prototype/server.py`).
  - Le choix reste à l'utilisateur·rice (open.md).

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « lance ce qui te semble
circonspect ». Les résultats publiés reposaient sur un code et des
données qui ont changé depuis.
**Ce qui le renverserait.** Un nouveau changement du jumeau ou des données
`secteur_stock`. Relancer coûte environ 1 h 30 de machine.

## 2026-11-14 — Langage naturel pour l'élu·e : un compilateur déterministe à glossaire, qui traduit sans jamais calculer

**Décision.**
- `v2/langage/` contient :
  - un glossaire contrôlé (termes politiques et juridiques → leviers, neutralisation du
    lexique, politiques non modélisées avec leur raison) ;
  - un compilateur **déterministe**, texte → scénario validé par `parse_levers` ;
  - au moins 30 cas de test écrits avant le code, avec un taux de correspondance mesuré ;
  - des gabarits de phrases de sortie remplis par le jumeau.
- **Pas de modèle de langage pour l'instant**, et c'est voulu : aucune clé d'API n'est
  disponible, et un glossaire relisible reste en boîte blanche. Un modèle de langage
  pourra plus tard remplacer l'étape d'analyse, jamais le calcul. Il passerait alors par le
  même jeu de test (question Mistral toujours ouverte).
- L'écran de confirmation (« ce que j'ai compris / ce qui n'est pas modélisé ») est ajouté
  à la carte **après l'UAT en cours**.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « oui fais ça », après la proposition
glossaire → compilateur → phrases.
**Ce qui le renverserait.** Un taux de correspondance trop bas sur les cas de test. Dans ce
cas, on ajoute une étape de modèle de langage, évaluée sur le même jeu de test.

## 2026-11-14 — Axe 3 : K3 (axe 2) jugé sur N10 — aucun grain ne passe, kinés à l'EPCI à une classe près

**Décision.**
- K3 (inscrit à 08:41, soumission a042415) est jugé sur N10 sans
  modification du protocole : **aucun grain ne passe**, pour aucune
  profession. **L'affichage reste au département** pour IDE, MK et CD.
- K3 corrige la sous-couverture des grandes unités (référence : 22 à 59 %
  au-delà de 100). Défauts restants : IDE trop larges (85–91 % dans les
  classes moyennes), CD trop étroits (69–73 %).
- Cas le plus proche : **kinés à l'EPCI**, une seule classe hors bande
  (1–2 professionnels : 73,0 %, 259 EPCI).
- Une variante corrigée (K4) doit être inscrite avant passage ; comme ce
  jugement montre la cible, un succès devra être confirmé hors des origines
  2014–2020 (origines 2021+ ou dépôt 2027).

**Pourquoi.** Rapport [N10](reports/2026-11-14-axe3-n10-grain-couverture.md),
section « Jugement du modèle K3 ».
**Ce qui le renverserait.** Une variante inscrite avant passage qui passe
N10 et le confirme hors échantillon.

## 2026-11-14 — Refonte « élu·e » du panneau Leviers : faite dans une page à part, bascule après l'UAT

**Décision.**
- Périmètre confirmé, priorités 1, 2 et 5, plus 4 et 6 au passage :
  - une question par famille, avec les valeurs en phrase ;
  - trois niveaux (fermé : état et effet 2050 ; ouvert : le levier principal ;
    « Préciser » : les réglages avancés), une seule famille ouverte à la fois ;
  - un résumé du scénario en tête, avec trois préréglages ;
  - les leviers sans effet pour la profession masqués et listés, plus « Pas encore dans le
    modèle » ;
  - la couleur de la carte dans la légende.
- **Commencée sans attendre la fin de l'UAT**, dans `v2/prototype-carte/index-refonte.html`,
  servie par le même serveur. La page testée par l'UAT (`index.html`) n'est pas touchée. On
  bascule une fois l'UAT terminée.
- Vérifié dans un onglet séparé :
  - le préréglage « Former 20 % de plus » donne +19 110 en France en 2050, dont la famille
    Former +20 665 ;
  - pharmaciens : la famille Attirer est masquée et expliquée.
- Le mode Expert (décideur technique) est cadré à part. Il viendra après, sur le même modèle.

**Pourquoi.** La session UAT : « confirme le périmètre (priorités 1, 2, 5) et indique si
elle peut commencer sans attendre la fin de l'UAT », relayé par l'utilisateur·rice.
**Ce qui le renverserait.** L'UAT en cours demande des changements incompatibles avec la
refonte.

## 2026-11-14 — N10 sur K3 (axe 2) : aucun grain infra-départemental ne passe ; K4 sous deux conditions

**Décision.**
- **K3** (erreur départementale commune + erreur locale) jugé sur N10 (commit 7b8c8d6) :
  **aucun grain ne passe**, pour aucune profession. L'affichage reste au département.
- **Couverture** commune / bassin de vie / EPCI :
  - CD : 72 / 75 / 76 % ;
  - IDE : 83 / 85 / 85 %, trop larges dans les classes moyennes (85-91 %) ;
  - MK : 76 / 78 / 78 %. C'est le plus proche : à l'EPCI, seule la classe 1–2
    professionnels sort de la bande (73,0 %, 259 EPCI).
- **K4** est autorisé à deux conditions :
  1. il est inscrit avant passage ;
  2. son succès est confirmé hors des origines 2014–2020, car le jugement de K3 a révélé
     la cible (risque de sur-ajustement au juge).

**Pourquoi.** Le protocole N10 et la règle de pré-enregistrement de l'axe 3.
**Ce qui le renverserait.** K4 passe N10 et sa confirmation hors échantillon.

## 2026-11-14 — Axe 3 : K4 (axe 2) non confirmé — échoue N10 et l'origine réservée 2021

**Décision.**
- Protocole [N11](reports/2026-11-14-axe3-n11-confirmation-k4.md), gelé à
  08:50 (SHA-256 `4bf54ad0587a`) avant que K4 existe.
- **K4 échoue l'étape 1** (N10, 2014–2020) à tous les grains, sans faire
  mieux que K3 (kinés EPCI : 3 classes hors bande contre 1), **et l'étape
  2** (origine réservée 2021, h = 4) à tous les grains. **K4 n'est confirmé
  nulle part.**
- Sur 2021/h4, la tendance naïve des unités calibre 8 classes sur 8 pour les
  kinés au bassin de vie, alors qu'elle échoue N10 : la période 2021 → 2025
  est facile pour les kinés, d'où l'exigence de deux étapes.
- **Affichage au département maintenu** (IDE, MK, CD). Défaut de forme
  persistant : IDE trop larges, CD trop étroits dans les grandes unités.

**Pourquoi.** Décision « Chantier projection communale fiable » ; N11.
**Ce qui le renverserait.** Une variante inscrite avant passage qui passe
N10 et une origine réservée, puis le dépôt 2027.

## 2026-11-14 — Dépôt 2027 : collision de nom entre l'axe 2 et l'axe 3, dépôt A0 de l'axe 2 restauré

**Décision.**
- Le dépôt A0 de l'axe 2 (`jumeau_taux_locaux_2026-11-14.parquet`, 08:07,
  SHA-256 `4f7400845340`, commit 470acf1) a été **écrasé** une minute plus
  tard par le dépôt de l'axe 3 au même chemin (08:08, SHA-256
  `ca036374d216`, commit 03a67d8). Les deux sessions écrivaient sans se
  voir.
- **Restauration** : le fichier de l'axe 2 est repris tel quel de 470acf1
  sous `v2/validation/depot/axe2_a0_jumeau_taux_locaux_2026-11-14.parquet` ;
  son empreinte est inchangée (`4f7400845340`, vérifiée). Le chemin
  `jumeau_taux_locaux_2026-11-14.parquet` désigne désormais le dépôt de
  l'axe 3 (`ca036374d216`, avec bande √h).
- Les deux dépôts portent sur la même variante (A0) ; ils sont scorés
  séparément, chacun selon son empreinte. L'entrée « Axe 2 : dépôt des
  prévisions 2027–2030 de A0 et C1 » est à lire avec le nouveau chemin.
- Règle : un dépôt porte le préfixe de l'axe qui le fait (`axe2_…`,
  `axe3_…`) ; l'axe 2 prévient avant d'écrire dans `v2/validation/depot/`.

**Pourquoi.** Deux empreintes différentes pour un même chemin rendaient l'un
des deux dépôts invérifiable.
**Ce qui le renverserait.** Rien : un dépôt ne se modifie pas.

## 2026-11-14 — Axe 3 : K5 (axe 2) non confirmé — moins bien calibré que K3 et K4

**Décision.**
- Protocole [N12](reports/2026-11-14-axe3-n12-confirmation-k5.md), gelé à
  09:05 (SHA-256 `ad08357a48fe`) avant d'ouvrir les fichiers ; origine
  réservée 2022, h = 3 (proposée par l'axe 2, confirmation partielle).
- **K5 échoue l'étape 1** (N10) à tous les grains, plus nettement que K3 et K4 :
  bandes trop étroites (IDE au BV 65,9 %, à l'EPCI 59,1 %) ; **et l'étape 2**
  à tous les grains (le plus proche : kinés au BV, une classe sur 8 hors
  bande). **Non confirmé.**
- Sur 2022/h3, la tendance naïve calibre 8 classes sur 8 pour les IDE à la
  commune : période facile, comme 2021.
- Dépôt communal de K5 écrit avant le verdict : `axe2_k5_communes_2026-11-14.parquet`,
  SHA-256 `0169b97d4fac`.
- **Affichage au département maintenu** pour IDE, MK et CD. Bilan : K3, K4 et
  K5 n'ont calibré aucun grain fin ; K3 reste le moins mal calibré.

**Pourquoi.** Décision « Chantier projection communale fiable » ; N12.
**Ce qui le renverserait.** Une variante qui passe N10 et une origine
réservée, puis son dépôt.

## 2026-11-14 — Axe 5 : statu quo SF et MK corrigé (abandon de formation du jumeau gardé)

**Décision.**
- **Défaut corrigé.** `leviers.py` forçait `formation.abandon` à 0 hors
  IDE.
  - Le jumeau `b64ce56` a pourtant des abandons sourcés : SF 0,033 et MK
    0,016 par an.
  - Le statu quo de l'axe 5 ajoutait donc des diplômés : +11,5 % pour les
    SF (21 176 contre 18 991) et +3,3 % pour les MK en 2050 (mesuré).
  - Correctif : hors IDE, l'abandon reste à la valeur du jumeau. Seul
    l'abandon IFSI est un levier.
  - Les sorties SF et MK de la relance de 08:33 sont remplacées. CD, PH et
    IDE ne sont pas touchés.
- **Constat après la correction de 2013 (IDE).** La bande backtest
  départementale des IDE passe de ±460 % à ±37 % (médiane, mesuré).

**Pourquoi.** Un statu quo qui n'égale pas le tendanciel du jumeau fausse
les niveaux et les effets relatifs. Le contrôle est désormais explicite :
le statu quo de `leviers.Model` égale `trajectory(LEVIERS)` à 1 personne
près.
**Ce qui le renverserait.** Un nouveau paramètre par profession dans le
jumeau, réécrit à tort par le scénario de l'axe 5. À vérifier à chaque
relance.

## 2026-11-14 — Axe 5 : l'amplitude de référence des leviers est celle de DD76 (quotas ±20 %)

**Décision.** La part « décision / connaissance » et le seuil « assez sûr
pour décider » se rapportent à l'amplitude **DD76** :
- quotas et capacité de formation × [0,8 ; 1,2] ;
- report de la retraite de 0 à 2 ans ;
- autres leviers inchangés.

La variante « interface » (quotas de 0,7 à 1,5, retraite de 0 à 3 ans)
reste publiée comme sensibilité. Elle ne sert pas de référence.

**Pourquoi.** Choix de l'utilisateur·rice, 2026-11-14 : « DD76 (±20 %) ».
L'amplitude DD76 est sourcée (DREES, Dossiers n° 76) ; celle de
l'interface est un choix d'ergonomie.
- Conséquence en 2050 : la décision pèse plus que la connaissance pour les
  IDE, les MK et les SF.
- Les CD sont à égalité.
- Les PH penchent du côté de la connaissance (0,38 contre 0,61).
**Ce qui le renverserait.** Une source qui fixe une autre plage plausible
pour les quotas, par exemple les arrêtés d'objectifs 2026–2030.

## Open / not yet decided

- ~~**M0 reste-t-il une borne de la fourchette de C ?**~~ **Tranché le 2026-11-15** : M0 retiré, voir l'entrée datée « axe 5 : M0 retiré de la fourchette affichée ». (ouvert le 2026-11-15, session besoin-axe5-sensibilite,
  [rapport](reports/2026-11-15-besoin-axe5-sensibilite.md))
  - **Question** : M0 (besoin ∝ population) est « cas limite » au rapport d'étape et figure dans l'ensemble gelé
    de l'axe 5. P-B1 a retenu l'âge (M1) contre lui pour les cinq professions. Avec M0, la fourchette MK et IDE est large
    (C 2050 : MK 1,34–1,54, IDE 0,83–1,14) ; sans lui, elle se réduit à ≤ 0,4 % et la règle d'affichage ne se
    déclencherait plus.
  - **Avis de la session** : retirer M0 de la fourchette affichée et le rapporter comme « sans effet de l'âge », car
    il est réfuté par P-B1, pas plausible. Non appliqué : la règle gelée prime tant que l'utilisateur·rice n'a pas
    tranché.
- **Cible externe de M4 pharmaciens** (ouvert le 2026-11-15, session besoin-cible-pharmaciens). Proposé : APL DREES
  « Méthode initiale V0 » aux pharmacies, commune, 2013 (2010 en secondaire), Licence Ouverte 2.0, offre = officines
  sans ETP, paliers 0–5 / 5–10 / 10–15 min (s, Notice). Écartés comme cible : IRDES QES 308 (pas d'APL des pharmacies,
  distance Insee seulement) ; temps Insee à la pharmacie la plus proche (autre grandeur, gardé en contrôle du
  distancier). Protocole [P-B4-PH](../../validation/preregistered/2026-11-15-besoin-p-b4-ph-apl-v0.md) rédigé,
  **non gelé** : gel par jeton sur accord de l'utilisateur·rice. Reste à choisir la source d'offre 2013 (BPE ou FINESS).
  Voir [exploration](explorations/2026-11-15-besoin-cible-pharmaciens.md).

- ~~**Mise en service du GBM de P-B5**~~ **Tranché le 2026-11-15** : option (a), voir l'entrée datée « P-B5 : le GBM servi comme prédicteur du recours seulement ». (ouvert le 2026-11-15, [rapport](reports/2026-11-15-besoin-pb5-backtest.md)).
  Par la règle gelée (borne haute de l'IC de Δ_GBM < 0), il qualifie pour IDE (−1,9 pt de MAPE), CD (−3,2) et SF
  (−45,8) ; pas pour MK. Mais son gain suit la croissance de l'offre (corrélation 0,54 à 0,71 entre sa cible et la
  croissance de l'effectif 2016 → 2025, diagnostic a posteriori), et il n'est validé qu'à h = 9. Options :
  (a) **le servir comme prédicteur du recours seulement**, jamais comme besoin (avis) ; (b) le servir comme
  estimateur de besoin pour IDE, CD, SF, ce qui rend B dépendant de l'offre ; (c) ne pas le servir. Prix : (a)
  ~30 min, (b) ~45 min, (c) 0.
- **Brancher le module de besoin dans la carte** (ouvert le 2026-11-15, axe 0 du besoin). `besoin.sortie.besoin_api`
  rend `besoin`, `couverture` et `couverture_base` en 0,72 ms au 95ᵉ centile au département (mesuré). Rien n'est
  branché dans `/api/carte` sans accord. Tant que l'axe 1 n'a pas remplacé les placeholders, un effet de transfert
  affiché serait « supposé » de bout en bout. Options : attendre l'axe 1 (avis) ; brancher C de M0 seul, sans transfert.
- **Âge d'entrée des diplômés à l'étranger par profession** (ouvert le 2026-11-15, relecture des sources de l'axe 1).
  Aujourd'hui `etrangers.age_entree` est unique, à 28 ans. Les sources donnent : MK 26 ans (ER 1075) ; PH 31 ans (DD76,
  tab. 13) ; CD 28 ans (DD76) ou 32 ans (ER 1026), qui se contredisent.
  Effet mesuré sur N(2050), scénario « étrangers × 2 » : MK 0, PH −191 (−0,2 %), CD −1 369 (−1,3 %). Le tendanciel ne
  change pas.
  Options : garder 28 ans ; passer à un dictionnaire par profession, ce qui demande de réécrire C17. Prix ≈ 30 min.
- **Conformité : seuil de diffusion des tables communales publiées, habillage DSFR, licence du code** (ouvert le 2026-11-15, [audit RGPD/AIPD/2017-745](reports/2026-11-15-audit-rgpd-aipd-dm.md)). Constat mesuré : 52,5 % des cellules commune × âge de `commune_stock.parquet`, sur le dépôt public, valent 1 personne (âge d'un professionnel nommable via l'Annuaire Santé). Verdicts dérivés, non juridiques : pas un dispositif médical (2017/745, aucune finalité médicale individuelle) ; AIPD probablement non obligatoire (1 à 2 critères G29), note de non-applicabilité recommandée si un seuil de diffusion est appliqué. Options pour le seuil : masquer ou regrouper les cellules < 5 (≈ 30 min) ; retirer les tables communales du dépôt public et les reconstruire localement (≈ 20 min, mais le clone neuf ne les a plus). ~~DSFR : porteur public réel, ou habillage neutre hors .gouv.fr.~~ **Levé le 2026-11-15** : le projet est porté par le Ministère chargé de la santé (information de l'utilisateur·rice) ; le DSFR est gardé, structure porteuse à nommer. Licence : EUPL 1.2 proposée. À trancher par l'équipe.
  - *Recommandation ajoutée le 2026-11-15 (session besoin-axe0-interface, [brouillon](reports/2026-11-15-licences-brouillon.md)), entrée non fermée :* licence du code **EUPL 1.2** (projet porté par le Ministère, copyleft réseau, texte officiel en français) ; MIT si l'équipe veut la réutilisation sans condition ; Apache 2.0 sans apport ici. Brouillon `LICENSE.draft` non activé. La licence du code ne couvre pas les données (LO 2.0 et ODbL suivent leurs fichiers).
- **Taux d'installation des diplômés au-dessus de 100 % (kinés 107 %)** (ouvert le 2026-11-15). Options : renommer
  en « entrées en libéral pour 100 diplômés » ; ne compter que les premières entrées (à dériver du RPPS) ; masquer au-delà
  de 100 %. Prix : renommage ≈ 10 min ; premières entrées ≈ 2 h.
- ~~**Carte : afficher la définition des indicateurs, de manière facultative**~~ **Tranchée le 2026-11-14 : encadré
  dépliable sous la légende** (entrée « Carte : définition des indicateurs dans un encadré facultatif »).
- ~~**Assistant : objectif chiffré → leviers**~~ **Construit le 2026-11-14** (entrée « Assistant : objectifs → mélanges de leviers… »).
- ~~**Carte option 1 : chat fermé derrière une icône, ou ouvert au chargement**~~ **Tranchée le 2026-11-14 : ouvert
  au chargement** (entrée « Option 1 : la conversation ouverte au chargement… »). (relevé le 2026-11-14 en fusionnant
  `main` dans la PR #3). `index-option1.html` ouvre le chat par une icône sur la carte (demande de l'utilisateur·rice) ;
  la décision « Squelette : la conversation est ouverte au chargement de la carte » ouvre le panneau au chargement de
  `index.html`, interface principale. Non reporté sur l'option 1 en attendant l'arbitrage. Prix : ≈ 15 min.
- ~~**Refonte de l'interface de la carte, à fonctions égales**~~ **Tranchée le 2026-11-14** : option 1,
  direction A (voir l'entrée « Carte : option 1 en direction A (Bertin) retenue »). (Question posée le 2026-11-14 :
  « proposer d'autres solutions capables de reprendre iso fonctionnel l'existant avec des
  améliorations UI »). Options proposées, aucune choisie :
  - **1. Même pile (HTML + MapLibre, sans build), coque ancrée** : leviers à gauche, carte au
    centre, un panneau droit à onglets (Territoire, Comparer, Expert). Recommandée (≈ 4 à 6 h).
  - **2. Svelte 5 + Vite + MapLibre** : même contrat, composants testables ; utile pour la
    couche personas, risqué avant H-6 (≈ 1,5 à 2 jours).
  - **Habillage**, au choix sur 1 ou 2 : l'actuel, ou la direction A (Bertin) du
    2026-11-14. Le DSFR reste réservé à un hébergement par un service de l'État. **Levé le 2026-11-14** :
    habillage DSFR adopté (entrée « Carte : habillage DSFR »).
  - **Écartées** : Dash ou Panel (aller-retour serveur à chaque réglage ; Streamlit déjà
    supprimé) et deck.gl (utile seulement au grain communal, que l'affichage n'a pas encore).
  - Le curseur d'année sur la carte n'est pas iso-fonctionnel : `/api/carte` ne rend que 2026
    et 2050. Il demande une extension de l'API.
  - **Maquettes, 2026-11-14** : faites dans Claude Design (canevas privé
    https://claude.ai/artifact/3VNzVPT3qTK3XLPja1dKxg), à la demande de l'utilisateur·rice
    (« oui, lance les maquettes dans Claude Design »).
    - Sans système de design : ceux du compte (Deviseur, Vroomly) sont des chartes d'entreprise.
    - Chiffres réels du jumeau (version e127749), pas d'exemple : kinés, préréglage « Former
      20 % de plus », Puy-de-Dôme ouvert.
    - Fonds de carte : SVG simplifiés à partir de `/geo` et `/geo-regions`.
    - Cinq écrans : l'actuel et l'option 1 sur ordinateur et sur mobile, plus l'option 1 en
      direction A.
- **Interprétation conversationnelle : agent LLM ou réponses déterministes, et un seul moteur** (challenge du 2026-11-14,
  `lab:challenge-design`). Choix contesté : l'agent LLM `v2/agent/` (décision du 2026-11-14 « Agent conversationnel… »)
  comme moteur d'interprétation, en parallèle de `julietteknp/AI_interface_acces_soin_hackaton` (`jumeau-chat`, même
  rôle, dépôt séparé, sous-module figé sur `426422c`).
  - **Contrainte, en unités.** Ce que la couche sert : part des réponses utiles (chiffre + fourchette + flux quand on
    demande pourquoi, « pas dans le modèle » quand il faut), part des nombres ancrés (cible 100 %), latence (< 30 s),
    coût (< 0,20 $ par question), et surtout des **heures-personnes** (budget 480 h) : le profil (recadrage du
    2026-11-14) range les personas et l'application en couche ultérieure ; la couche ne sert aucun des trois
    indicateurs principaux (backtest, reproduction DREES, validité des leviers).
  - **Dérivé de zéro.** Le moins cher qui répond : compilateur à glossaire + phrases à trous sur les sorties du
    jumeau. Ancrage 100 % par construction, 0 $, sans clé. Il **existe déjà et est testé** : mode déterministe de
    `jumeau-chat` (projection, objectif « atteindre », hors périmètre, ville → département). Il ne sait pas répondre
    aux questions libres (« pourquoi », « quelle confiance », comparaison ouverte) ; le compilateur seul plafonne à
    environ 77 % de phrases bien comprises (décision « tour 6 »).
  - **Comparaison.** Aucun des deux modes LLM n'est mesuré (pas de clé). Deux moteurs LLM font double emploi.
    `jumeau-chat` est plus isolé et testé et a plus d'outils ; `v2/agent` a la vérification à la précision affichée
    (la tolérance ±6 % de `jumeau-chat` accepte tout entier entre ≈ 12 450 et 20 000 pour kinés ARA 2035, dérivé),
    le contrôle du lexique et le contexte de la carte.
  - **Verdict : indécidable sans mesure** sur LLM contre déterministe. Mesure : les 22 questions de
    `v2/agent/questions.yaml` dans les deux modes, notées sur l'utilité (grille ci-dessus) avec la règle d'ancrage
    stricte. Prix : ~30 min Claude + ~10 min machine + ~3 $, une clé d'API, l'accord pour lancer `jumeau-chat`.
    Issues : déterministe à 10 points ou moins du LLM en utilité → la carte branche le déterministe, pas de LLM ;
    LLM nettement meilleur → un seul moteur LLM (`jumeau-chat` + règle stricte + lexique), `v2/agent` réduit au panneau.
  - **En attendant :** aucun travail nouveau sur le moteur de `v2/agent` ; quelle que soit l'issue, un seul moteur.
- **Refonte du panneau Leviers de la carte**, transmise le 2026-11-14 par la session UAT et
  dite validée par l'utilisateur·rice. Le panneau est jugé « un peu cryptique et crowded ».
  Les points :
  - partir de la question, et lire les valeurs en phrase ;
  - trois niveaux d'affichage ;
  - des badges discrets ;
  - les leviers indisponibles regroupés ;
  - un résumé du scénario en tête ;
  - la couleur de la carte déplacée dans la légende.

  En file : elle sera appliquée **après la fin de l'UAT agentique en cours**, pour ne pas
  fausser la recette (leçon de l'UAT précédente). Priorités : 1, 2, 5.
- **Brancher la rétention dépendante de la densité pour les IDE dans le tendanciel ?**
  L'effet est mesuré (N9 : +0,11 [+0,05 ; +0,18]) mais corrélationnel. Question posée le
  2026-11-14.
- **Boucles de rétroaction non linéaires** (analyse transmise le 2026-11-14 :
  [inputs/2026-11-14-analyse-boucles-retroaction.md](inputs/2026-11-14-analyse-boucles-retroaction.md)).
  ~~Gardée comme référence ; « pas maintenant ».~~ **Lancée le 2026-11-14** (« en fait si si »),
  voir l'entrée « Tests des boucles de rétroaction ». La conduite proposée est notée dans le fichier :
  - tester le signe empiriquement d'abord ;
  - estimer la boucle densité → installations dans le logit plutôt que de la supposer ;
  - garder la boucle charge → départs en scénario de stress.
- **Leviers de demande (transferts de tâches : vaccination en officine,
  IPA, accès direct au kiné)** : ajouter un module de besoin, ou les
  laisser hors du périmètre ? Question posée le 2026-11-14.
  *Plan proposé le 2026-11-14 (non construit, accord attendu) :*
  [derivations/2026-11-14-module-besoin.md](derivations/2026-11-14-module-besoin.md).
  Besoin = habitants × profil de recours par âge (Open DAMIR) ; indice de couverture
  indexé à 2026 ; transferts de tâches L23, L25 et L27 comme déplacement d'une part du
  besoin ; effectifs inchangés. Test d'abandon de ~30 min avant de construire.
  *Complété le 2026-11-15 (non construit, accord attendu) :* le plan du 2026-11-14 est **remplacé comme plan de
  travail** par la [dérivation du besoin](derivations/2026-11-15-besoin-derivation.md) et le
  [plan par axes](derivations/2026-11-15-besoin-plan.md). Il survit comme M1 + transferts, avec cinq corrections
  (dérivation §9). Le plan du 2026-11-14 reste en place, marqué remplacé.
- ~~**Médecine générale comme profession source des transferts de tâches**~~ *décidé le 2026-11-15 : O2, voir l'entrée « Module de besoin : médecine générale comme source seulement (O2) ; plan accepté ».* (ouvert le 2026-11-15, dérivation du
  besoin §7). Les transferts du pitch (vaccination, tension et diabète en officine, IPA, accès direct au kiné)
  prennent surtout des actes à la MG, exclue du sujet.
  - Options :
    - **O1** hors modèle : seule la part IDE de L23 est calculable ;
    - **O2** source seulement : `B_MG` par M1, aucune offre MG projetée, aucun indice de couverture MG affiché,
      seulement les actes et les ETP de MG libérés ; coût ≈ 30 min ;
    - **O3** O2 plus la projection DREES des médecins lue en contexte ;
    - **O4** MG pleinement modélisée, contraire au sujet.
  - Avis de la session besoin-derivation : **O2**. Le profil du laboratoire (`docs/lab/profile.md`, règles maison) le
    permet déjà : « GPs may appear only as context, for example when demand shifts from GPs to pharmacists. They are
    never a projected output. » Mais rien n'est acté pour le module.
  - À trancher par l'utilisateur·rice. Bloque l'axe 1 du plan de besoin.
- ~~**Licence des tables dérivées de jeux ODbL**~~ *décidé le 2026-11-15 : commitées sous ODbL, voir l'entrée « Tables dérivées ODbL commitées sous ODbL ».* (ouvert le 2026-11-15, [exploration](explorations/2026-11-15-besoin-sources.md)).
  Les jeux data.ameli.fr (pathologies, patientèle, honoraires) et une matrice de temps OpenStreetMap sont sous
  **ODbL** : une base dérivée redistribuée doit rester sous ODbL. Or le dépôt public commite les données traitées
  (décision du 2026-11-14).
  - Options :
    - commiter ces tables sous ODbL, avec mention, et un `NOTICE` ;
    - ne commiter que le script de reconstruction.
  - Prix ≈ 10 min de décision + 15 min de mise en œuvre. Lié à la question de la licence du code (EUPL 1.2 proposée).
  - *Recommandation ajoutée le 2026-11-15 (session besoin-axe0-interface, [brouillon](reports/2026-11-15-licences-brouillon.md)), entrée non fermée :* **commiter sous ODbL** dans `v2/data/odbl/` séparé, avec son `LICENSE` ODbL et un `NOTICE` racine (brouillon `NOTICE.draft`), si la taille mesurée tient sous 100 Mo par fichier. Raisons : décision du 2026-11-14 de commiter les données traitées, reproductibilité du backtest. Carte, fiches et réponses ponctuelles = œuvres produites (mention seule). À trancher par l'utilisateur·rice.

### 2026-11-14 — Accueil de la carte V2 : point d'entrée territorial ou national ?
Le challenge par les trois personas
([rapport](reports/2026-11-14-accueil-personas.md)) converge sur quatre
points : un chiffre-phrase dès l'ouverture, les leviers repliés, la
fourchette toujours visible, le périmètre dit en clair. Il diverge sur le
point d'entrée. La synthèse proposée est un champ « Quel territoire ? » au
centre et « ou voir la France » en dessous, avec un mode Simple par défaut
et un mode Expert. À valider par l'utilisateur·rice avant de construire
(~30 à 45 min de Claude).
- ~~**Programme méthodologique « boîte blanche »**~~ *décidé le 2026-11-14, voir l'entrée « Programme de l'axe 2 ».* (proposé le 2026-11-14,
  [état de l'art](explorations/2026-11-14-etat-de-lart-methodes.md)).**
  Même structure par cohortes, mais estimée en bayésien hiérarchique :
  - APC de Poisson pour les sorties ;
  - logit conditionnel pour l'installation ;
  - réconciliation MinT entre échelles ;
  - CRPS, PIT et SBC pour la validation.

  En attente de l'accord de l'utilisateur·rice pour en faire le programme
  de l'axe 2.
- **Exigence d'interface (utilisateur·rice, 2026-11-14) : « très fluide
  visuellement, un véritable outil d'aide à la décision ».** Traduction
  proposée, en critères vérifiables :
  1. l'objet principal est l'**écart du scénario au tendanciel**, pas deux
     courbes de niveau ;
  2. chaque écart est **expliqué par flux** (entrées, sorties, régulation,
     transitions) ;
  3. le **délai d'effet** d'un levier est visible (quotas : rien avant la
     durée des études) ;
  4. réponse aux leviers en moins de **100 ms** perçus, avec des
     transitions animées entre échelles et entre états, et sans
     rechargement. Le jumeau met 17 ms au département, mais environ 3 s à
     la commune : il faudra précalculer ;
  5. l'incertitude est toujours affichée ;
  6. une fiche de synthèse par territoire, exportable.
- **La DA doit rester modifiable dans Figma** par les designers UX de
  l'équipe (demande de l'utilisateur·rice, 2026-11-14). Proposé, pas encore
  fait :
  - une source unique de tokens au format W3C Design Tokens (JSON) ;
  - les directions A, B et C deviennent trois *modes* d'une même collection
    de variables Figma ;
  - le site ne lit que des variables CSS générées depuis ce JSON ;
  - aller-retour avec Figma par le plugin Tokens Studio (synchronisé avec le
    dépôt) ou par le connecteur Figma MCP (lecture de `get_variable_defs`).
    L'import natif de variables JSON dans Figma reste à vérifier ;
  - règles d'encodage des données non modifiables dans Figma : une gamme par
    variable, pas de rouge/vert, hachures pour l'incertitude, lexique
    neutre.
- **Articulation avec l'observatoire de l'équipe** (dépôt
  Pierreafeu181/Hackathon-Evolution-soin, membre de l'équipe, présenté le
  2026-11-14). Il fournit déjà une interface Next.js, des leviers en
  direct et un « besoin » pondéré par âge, par département, jusqu'en 2040.
  - Proposé, pas encore décidé : la v2 est le **moteur de recherche** (le
    jumeau, la validation, les paramètres sourcés), et l'observatoire est
    la **future couche personas et restitution**.
  - **Précisé le 2026-11-14 par l'utilisateur·rice : `v2/ROADMAP.md`
    prime.** L'observatoire est une ressource de l'équipe, pas une
    contrainte : il n'impose ni la définition de « libéral », ni le grain,
    ni l'horizon, ni la méthode.
  - Une interface d'échange reste à définir (export de scénarios du jumeau
    vers ses JSON).
  - L'application Streamlit v1 ne serait alors plus reprise.
- Unité de l'offre : effectif ou équivalent temps plein (taux d'activité α).
  Question héritée de la v1.
- Quels « groupes de communes » utiliser : territoires de démocratie
  sanitaire, zonage ARS, bassins de vie ou EPCI. Question héritée de la v1.
- Mistral : le hackathon impose-t-il un modèle Mistral ? Question héritée
  de la v1.
- Ordre d'application des modules (séparation d'opérateurs) : fixé par
  `order` (formation 5, vieillissement 10, sorties 20, entrées 30,
  régulation 40). La sensibilité de N(2050) à cet ordre n'est pas mesurée
  (voir open.md).
- Part privée des pharmaciens hospitaliers (section H) : DREES 17 % ou Ordre
  28,6 % ? Défaut proposé : DREES (axe 1, 2026-11-14). Voir open.md.

## 2026-11-14 — Axe 2 : 5 variantes pré-inscrites au banc N1 avant tout passage ; périmètre confirmatoire = privé

**Décision.**
- Inscrites à 03:25 dans `v2/validation/registry.py`, **avant** tout
  passage sur le banc :
  - confirmatoires : `axe2_ages_interp` (A1a), `axe2_ages_simples` (A1b),
    `axe2_shrink_hier` (A2), `axe2_retention60` (A3), `axe2_combine`
    (A1a + A2 + A3) ;
  - diagnostic : `axe2_obs_r12` (B4).
- Dérivation et prédictions écrites avant le banc :
  [derivations/2026-11-14-axe2-methodes.md](derivations/2026-11-14-axe2-methodes.md),
  SHA-256 `1c324f5795b0`.
- **Périmètre confirmatoire : privé**, part centrale de l'axe 4.
  - N1 prévoyait l'ancien périmètre seulement « tant que la séparation
    n'existe pas ».
  - Infirmiers : libéraux du RPPS (l'âge des salariés privés manque).
  - L'ancien périmètre (libéral + mixte) est rapporté en secondaire, pour
    la comparaison avec K1.
- Code dans `v2/methodes/`, branché par le registre du jumeau (3 modules
  `methodes_*`). Aucun fichier de `v2/jumeau/` n'est modifié.
- **Contrôles** (`PYTHONPATH=v2 uv run python -m methodes.verif`) :
  - aux options v1, la composition reproduit `twin_of(StockFlowLocal)` à
    9e-13 personne près ;
  - le recalcul jusqu'en 2050 prend 14 à 40 ms (5 professions,
    département).
- **Écart de propriété signalé :** `registry.py` appartient à l'axe 3.
  - On n'y fait qu'un ajout en fin de fichier, parce que le protocole N1
    gelé impose d'y inscrire les variantes.
  - Les lignes existantes ne sont pas touchées.

**Pourquoi.** Le protocole N1 (SHA `eb527ecb06a0`, vérifié intact) rend
confirmatoire seulement une variante inscrite avant son premier passage.
**Rejeté :** régler k (shrinkage) ou la largeur des tranches ouvertes sur
le banc, parce que ce serait choisir après avoir vu.
**Ce qui le renverserait.** L'axe 3 qui refuse l'inscription hors de son
fichier. On déplacerait alors les entrées, avec leur heure.

## 2026-11-14 — Axe 2 : shrinkage hiérarchique dép → région → national adopté (A2)

**Décision.** Le calibrage par défaut rétrécit les taux du département
vers la région, puis la région vers le national, avec k = 200 aux deux
niveaux (`methodes`, option `hier`). C'est l'ingrédient d'estimation par
défaut des prochaines variantes. Les leviers restent ceux de `sorties` et
`entrees` ; k est un réglage d'estimation, pas un levier.
**Pourquoi.** Banc N1, MAPE dép. h = 5
([rapport](reports/2026-11-14-axe2-methodes.md)) :
- privé : 8,57 % contre 8,68 % (A0), Δ −0,11 pt, IC 95 %
  [−0,21 ; −0,02] ;
- ancien périmètre : −0,10 [−0,21 ; −0,002].

C'est le seul gain reproduit sur les deux périmètres. Il bat aussi la
tendance (gagne, IC 99 % compris).
**Rejeté :** régler k sur le banc, parce que ce serait choisir après avoir
vu.
**Ce qui le renverserait.**
- Le dépôt 2027 où A2 ne bat pas A0.
- Un IC qui tient compte de la corrélation entre origines et qui couvre 0.

## 2026-11-14 — Axe 2 : âges fins (A1a, A1b) à égalité au banc ; A1b adopté pour la structure par âge, A1a réservé au département

**Décision.**
- **A1b**, l'état en âges simples (20 à 74 ans et plus) désagrégé à
  l'origine, est la variante d'âges retenue.
  - Au banc, il est à égalité avec A0 sur le total : +0,03 au privé,
    −0,03 sur l'ancien périmètre, IC couvrant 0.
  - Sur 18 mondes simulés, il divise par 3 l'erreur sur les 60 ans et
    plus : 2,1 % contre 7,0 % à h = 5, et 5,9 % contre 18,9 % au pire.
- **A1a**, désagrégé chaque année, est un peu moins bon que A0 au privé
  (+0,09 [+0,01 ; +0,18]) et coûte +1,23 s par profession à la commune.
  Il n'est pas retenu.
- Hypothèses supposées :
  - tranche « moins de 25 » = 20–24 ans ;
  - tranche 65+ de largeur 10 ;
  - entrées uniformes dans la tranche.

**Pourquoi.** Le vieillissement uniforme biaise la part des seniors
jusqu'à 19 % (mesuré, ordre de grandeur cité par l'observatoire, E4). Ce
biais ne se voit pas sur le total à 5 ans, parce que la rétention ajustée
l'absorbe dans la fenêtre. Les leviers retraite, eux, agissent sur les
âges.
**Ce qui le renverserait.** Une source en âges simples (RPPS individuel)
qui contredit la désagrégation linéaire.

## 2026-11-14 — Axe 2 : rejetés pour la prévision (A3, combinaison, B4, C5) ; en attente (A4, A5) ; tuée pour N1 (A6)

**Décision.**
- **Rejetée, A3** (rétention des 60 ans et plus en tendance) : pire
  qu'A0, +0,33 pt au privé et +0,76 pt sur l'ancien périmètre. La
  prédiction « réduit le biais national PH et CD » est falsifiée (PH
  −0,15 → +2,28 %).
  - Les variantes adoptées n'ont pas de tendance (`trend60` désactivé) :
    la rétention y est stationnaire.
  - Le levier `methodes_sorties.tendance_60plus` (λ, 1 dans la variante
    A3 inscrite) reste disponible quand `trend60` est activé. Il sert de
    scénario « on travaille plus longtemps » ; ce n'est pas une
    hypothèse de prévision.
- **Rejetée, la combinaison A123** : égale au privé (+0,06), pire sur
  l'ancien périmètre (+0,50), entraînée par A3.
- **Rejeté, B4** (borne r ≤ 1,2 de l'observatoire) :
  - meilleur au privé (−0,35), pire sur l'ancien périmètre (+0,53) ;
  - 27 à 47 % des cellules de 35 ans et plus y ont r > 1, d'où une
    croissance composée de +0,1 à +0,9 pt/an d'ici 2050 (dentistes : +23 %
    d'effectif en 2050 par rapport à A0) ;
  - c'est un piège partiel, pas l'emballement de K1 (+3,5 %/an).
- **Rejeté pour la prévision, C5** (entrées par région de formation) : la
  part du stock prédit la part régionale des entrées avec r = 0,996,
  contre 0,64 (CD) et 0,94 (PH) pour la part étudiante. On le garde comme
  futur mécanisme de levier régional.
- **En attente :**
  - A4, logit de l'installation : avec effets fixes, il égale les parts
    observées ; il faut un attribut daté ;
  - A5, modèle bayésien ou espace-état : au département, il ≈ A2 ; il
    relève de N4.
- **Tuée pour N1, A6** (microsimulation) : même espérance que le
  stock-flux.
- **Non testés, diplômés étrangers CD** : aucune série ouverte par lieu de
  diplôme.

**Pourquoi.** Banc N1 et diagnostics du
[rapport](reports/2026-11-14-axe2-methodes.md). Les verdicts a priori
viennent de la [dérivation](derivations/2026-11-14-axe2-methodes.md).
**Ce qui le renverserait.**
- Pour B4 : N2 (DD76 à 2050) favorable à B4.
- Pour C5 : une série d'inscrits par université avant 2020 qui prédit les
  *variations* d'entrées.

## 2026-11-14 — Axe 2, étape 1 : sorties en APC gaussien sur la rétention nette (pas de Poisson) ; inscrit avant le banc

**Décision.**
- **Vraisemblance : gaussienne sur y = log(rétention nette de cohorte).**
  - La variance vaut σ_e²/B + ω², avec B l'effectif exposé.
  - Le Poisson sur des sorties reconstruites est rejeté. Le RPPS ne donne
    que des stocks, et la sortie nette est négative dans 27 à 47 % des
    cellules de 35 ans et plus (mesuré). Un Poisson inventerait des
    cessations qu'on n'observe pas.
- **Structure.** η = μ_âge + π_{groupe d'âge, période} + γ_cohorte +
  v_{région×âge} + w_{dép×âge}.
  - π et γ sont des marches aléatoires d'ordre 1 ; v et w sont i.i.d.
    normaux.
  - Hyperparamètres : maximum de la vraisemblance marginale (Bayes
    empirique). La loi a posteriori est exacte et gaussienne sachant θ̂,
    sans MCMC (numpy et scipy, installables par uv).
- **Projection.** Les marches d'ordre 1 sont prolongées à plat.
  L'ordre 2, qui prolongerait la pente, est rejeté a priori parce qu'A3 a
  échoué au banc.
- **Identification déclarée.** Âge, période et cohorte sont liés
  linéairement : seules les courbures sont identifiées.
  - L'effet cohorte est faiblement contraint : écart-type a posteriori /
    a priori = 0,98 (médiane, dentistes, origine 2021, mesuré).
- **Levier :** `apc_sorties.periode_60plus`, un choc additif sur le log de
  la rétention des 60 ans et plus.
- **Inscription.** `axe2_apc` a été inscrit dans `v2/validation/registry.py`
  à 03:58, avant tout passage.
  - Dérivation : SHA-256 `a933da1958e2`.
  - Périmètre privé.
  - CRPS, PIT et couverture à h = 5 en secondaire.
- Le code est dans `v2/methodes/apc.py` (module `apc_sorties`).

**Pourquoi.** Programme de l'axe 2, étape 1 ; consigne du 2026-11-14 :
choisir entre gaussien et Poisson « honnêtement ».
**Ce qui le renverserait.**
- La calibration par simulation, si elle échoue avec θ connu.
- Une source qui sépare cessations et reprises (RPPS individuel), qui
  rendrait le Poisson possible.

## 2026-11-14 — Axe 2, étape 1 : l'APC égale le stock-flux en ponctuel ; adopté pour l'incertitude des sorties, il remplace A3

**Décision.**
- **Le modèle APC des sorties (`axe2_apc`) est adopté** quand on veut une
  incertitude sur les sorties. A0 reste le défaut ponctuel.
- **A3 est remplacé** par l'APC et son levier de période
  `apc_sorties.periode_60plus` ; il ne garde plus de pente prolongée.
- La bande prédictive de l'APC **n'est pas publiable telle quelle** :
  couverture de 50 % pour 80 % nominal, PIT en U. Elle ne porte pas
  l'incertitude des entrées.

**Pourquoi.** Banc N1 au privé ([rapport](reports/2026-11-14-axe2-apc-sorties.md)) :
- MAPE dép. h = 5 de 8,74 % contre 8,68 % : Δ +0,07, IC [−0,03 ; +0,16],
  égalité ;
- A3 est à 9,00 % ;
- le CRPS relatif des tirages est de 6,82 % ;
- la calibration par simulation réussit (KS p de 0,20 à 0,80), et la
  couverture dans l'échantillon est de 91 %.

**Ce qui le renverserait.** Une version avec des entrées probabilistes
(étape 2) dont la bande est calibrée et qui bat A0 en MAPE.

## 2026-11-14 — Axe 2, étape 2 : cohortes bayésiennes (C1) adoptées comme prévision par défaut proposée ; Laplace sur θ (C2) rejeté

**Décision.**
- **C1 est la variante par défaut proposée**, pour le point comme pour la
  bande. C1 = APC des sorties, plus des entrées en niveau local national ×
  des parts départementales hiérarchiques, avec θ fixé. A0 reste la
  référence.
- **C2 est rejeté.** La propagation de θ par Laplace ne gagne rien : la
  couverture à 80 % passe de 77,6 à 76,0 %, pour un ajustement environ
  2 fois plus coûteux.
- Le MCMC complet reste fermé tant que la calibration par simulation ne
  montre pas d'échec.

**Pourquoi.** Banc ([rapport](reports/2026-11-14-axe2-cohortes-bayesiennes.md)),
inscrit à 04:41 :
- **N1.** 7,73 % contre 8,68 %, Δ −0,95 [−1,51 ; −0,47]. Le gain tient sans
  les cellules vues par le pilote (7,52 contre 8,52). C1 bat A0 dans 17
  cellules sur 22.
- **N6.** Égalité en CRPS avec la persistance probabiliste. Couverture à
  80 % de 73,5 % (juste sous [75 ; 85]) et à 50 % de 45,9 % (dans la
  bande).
- **Toutes origines (hors protocole).** Couverture à 80 % de 77,6 %, à
  50 % de 50,0 %.
- **Verdicts par profession.**
  - CD, IDE, SF : bat.
  - MK, PH : égale.
  - En N6, PH échoue.

**Écart signalé.** Le pilote a vu les cibles 2026 (origine 2021) des CD et
des SF avant l'inscription, et la forme des variances du niveau a été
corrigée ensuite (dérivation § Écart).
**Ce qui le renverserait.**
- Le dépôt 2027–2030 où C1 ne bat pas A0.
- Le gain qui continue de décroître sur les origines récentes (CD, PH).

## 2026-11-14 — Axe 2 : dépôt des prévisions 2027–2030 de A0 et C1 (protocole N1), avant la publication du RPPS 2027

**Décision.**
- Deux fichiers sont déposés, avant toute donnée 2027 :
  - `v2/validation/depot/axe2_a0_jumeau_taux_locaux_2026-11-14.parquet` (chemin corrigé le 2026-11-14 après la collision de nom, voir « Dépôt 2027 : collision de nom » ; l'ancien chemin désigne le dépôt de l'axe 3), SHA-256
    `4f7400845340` ;
  - `v2/validation/depot/axe2_cohortes_c1_2026-11-14.parquet`, SHA-256
    `689b230b5b50`.
  - Code : `v2/methodes/depot.py`.
- **Contenu.** Les prévisions portent sur 2027, 2028 et 2030, par
  profession × département, au périmètre privé central.
  - L'origine est 2026, et 2023 pour les infirmiers libéraux.
  - C1 donne la moyenne a posteriori, plus les quantiles 10, 50 et 90 de
    200 tirages.
- **Divergence déposée.** Infirmiers libéraux en 2030 : A0 prévoit
  111 200, C1 96 687.
  - C1 suit la stagnation récente des entrées (98 854 en 2023).
  - C'est le test le plus discriminant du dépôt.

**Pourquoi.** C'est le seul test hors échantillon non contaminé (N1 ; le
pilote de l'étape 2 a vu l'origine 2021). Score à la publication du RPPS
2027, avec le critère de N1.
**Ce qui le renverserait.** Rien : un dépôt ne se modifie pas. Une erreur
de code donne un nouveau dépôt daté, et l'ancien reste.

## 2026-11-14 — Axe 2, étape 2 : la calibration par simulation échoue sur le niveau national des entrées ; bande nationale de C1 non publiable, traitement bayésien complet rouvert

**Décision.**
- On ne publie **que la bande départementale de C1**, avec sa couverture
  mesurée (77,6 % pour 80 % nominal, toutes origines).
- **Aucune bande nationale de C1** n'est publiée.
- **On rouvre le traitement bayésien complet** de σ_u, σ_v (niveau
  national) et τ_r (écart régional), avec des a priori demi-normaux écrits.
  Cela applique la règle pré-écrite dans la dérivation.

**Pourquoi.** Calibration par simulation, 5 × 2 × 200, θ ré-estimé
([rapport](reports/2026-11-14-axe2-cohortes-bayesiennes.md)) :
- APC : 0 échec sur 30 tests.
- Niveau national des entrées L_T : 10 échecs sur 10, rangs en U ; la loi
  a posteriori est trop étroite sachant σ̂.
- Écarts régionaux δ : 3 sur 10, dans les petites cellules masculines,
  où τ̂_r ≈ 0.

**Ce qui le renverserait.** Une nouvelle calibration par simulation, avec
σ et τ intégrés, qui passe.

## 2026-11-14 — Axe 2 : dynamique des systèmes, modèles à agents et multi-états, verdicts a priori

**Décision** ([dérivation](derivations/2026-11-14-axe2-familles-sd-abm.md)).
- **Tué : modèle à agents à règles calées.** Sans trajectoires
  individuelles ouvertes, ses règles ne sont pas identifiables à partir
  des stocks agrégés. Ce serait une boîte noire par calibration.
- **Promu : multi-états de Markov privé ↔ public ↔ sortie.**
  - Transitions nettes estimables grâce à la séparation de l'axe 4.
  - A priori hiérarchique ; kill test N1 sur le total privé.
- **En attente :**
  - le modèle à agents à règles estimées (logit), après l'étape 3. Il
    sert à la régulation par commune et doit reproduire le signe de N3 ;
  - la boucle B1 (infirmiers libéraux), en scénario de stress
    seulement, sur décision de l'utilisateur·rice.
- **Ordre proposé :**
  1. variances en bayésien complet ;
  2. logit d'installation ;
  3. multi-états ;
  4. agents à règles estimées ;
  5. B1.

**Pourquoi.**
- Question de l'utilisateur·rice, 2026-11-14 : « y a-t-il d'autres modèles
  comme les ABM, les systèmes dynamiques et boucles de rétroaction ? »,
  puis « oui » pour la dérivation.
- Par linéarité, un modèle à agents sans non-linéarité a la même
  espérance que le stock-flux.
- N9 : B2 est nul, et B1 n'est confirmé que pour les infirmiers libéraux.

**Ce qui le renverserait.** Un panel individuel ouvert (au moins 3
instantanés de l'Annuaire Santé, ou un RPPS individuel daté), qui
rendrait les règles d'agents estimables.

## 2026-11-14 — Projection communale : modèle K inscrit avant le banc N4 (08:35)

**Décision.**
- Le modèle K est inscrit avant tout passage sur le banc N4 :
  - cohortes communales ;
  - rétention rétrécie nat → région → dép → EPCI → commune (k = 200) ;
  - entrées en niveau local départemental × part communale hiérarchique
    (k_q = 20) ;
  - variance prédictive α_h·μ + β_h·μ², mesurée dans la fenêtre par
    pseudo-prévisions.
  - Dérivation [communes](derivations/2026-11-14-axe2-communes.md), SHA-256
    `0240e9fb2311`.
- **Banc.** `v2/methodes/banc_communes.py` : IDE, MK, CD ; origines 2014 à
  2020 ; h = 5. Fonctions de `validation.fine_scale`, inchangées.
- **Critère.** Couverture de la bande à 80 % dans [75 ; 85] % par classe
  (≥ 3–5). Le modèle meurt si plus de 2 classes sur 7 échouent pour une
  profession.
- Le pilote n'a regardé aucune cible du banc : origine 2010 seulement, pour
  le temps de calcul.

**Pourquoi.** Chantier « projection communale fiable », dont l'axe 2 est le
porteur.
**Ce qui le renverserait.** Le banc N4.

## 2026-11-14 — Projection communale : K rejeté au banc N4 ; repli K2 inscrit avant son passage (08:38)

**Décision.**
- **K est rejeté**, selon son critère pré-écrit.
  - Sa bande est trop large : couverture à 80 % de 90 à 100 % chez les
    IDE (8 classes sur 8 hors de [75 ; 85]) et de 92 à 95 % chez les CD
    (7 sur 8). Les MK passent dans 5 classes sur 8.
  - Son point est moins bon que la part tenue dans les petites classes :
    P80 de 84 % contre 43 % pour les IDE de 1–2.
- **K2 est inscrit avant son passage**, comme variante unique de repli. On
  s'arrête à son résultat.
  - Point : part communale tenue × total départemental projeté par K.
  - Bande : quantiles 10 et 90 % de log((réel + ½)/(prédit + ½)) par classe
    de taille, sur des pseudo-prévisions de K2 dans la fenêtre (cibles ≤
    origine).
  - Critère identique à celui de K.

**Pourquoi.** Le diagnostic de K a trouvé deux causes :
- la variance en moments (NNLS), dominée par quelques communes extrêmes
  (β = 1 chez les CD) ;
- la mécanique de cohortes, trop bruitée sous 10 personnes.

**Ce qui le renverserait.** Le banc de K2.

## 2026-11-14 — Projection communale : K2 rejeté aussi ; règle d'affichage provisoire ; pas de branchement sur le jumeau

**Décision.**
- **K2 est rejeté**, selon son critère pré-écrit : plus de 2 classes sur 7
  hors de [75 ; 85] % pour chaque profession.
  - Il calibre les IDE de 1 à 50 professionnels (81 à 83 % ; 75 à 85 %
    sur l'origine 2020).
  - Il est trop étroit au-dessus de 50 et pour les CD (68 à 73 %).
- **Règle d'affichage provisoire.**
  - IDE : projection communale avec la bande K2 pour les communes de 1 à
    50 professionnels ; au-dessus, l'échelon EPCI ou le département.
  - MK et CD : pas de projection communale calibrée. On affiche l'observé
    à la commune et la projection du département, en le disant.
- **Aucun branchement sur le jumeau.** L'axe 0 garde sa répartition
  communale (C15).
- **Prochaine variante, K3 (à inscrire avant).** La bande additionne une
  partie locale (K2) et la part × les tirages du total départemental de
  C1, avec un passage RPPS privé → CartoSanté libéral.

**Pourquoi.** Banc N4 ([rapport](reports/2026-11-14-axe2-communes.md)) :
l'erreur commune à tout le département domine dans les grandes communes,
et une bande par classe ne la porte pas.
**Ce qui le renverserait.** K3 calibré dans toutes les classes.

## 2026-11-14 — Projection communale : K3 inscrit avant tout passage (08:41), soumis au jugement N10 de l'axe 3

**Décision.**
- K3 est inscrit avant tout passage. Sa bande combine deux erreurs :
  - l'erreur du total départemental, tirée une fois par département et
    commune à ses communes ;
  - l'erreur locale, tirée par classe de taille.
  - Dérivation [communes, § K3](derivations/2026-11-14-axe2-communes.md),
    SHA-256 `1a4d308d7402`.
- La soumission à N10 porte sur les grains commune, bv2022 et EPCI, sur les
  origines 2014 à 2020 à h = 5. C'est l'axe 3 qui juge.

**Pourquoi.** K et K2 ont été rejetés : l'erreur du total départemental
domine dans les grandes communes. N10 montre la même forme sur les
estimateurs de référence.
**Ce qui le renverserait.** Le verdict de N10.

## 2026-11-14 — Projection communale : K4 inscrit avant tout passage (08:50), avec une confirmation réservée (origine 2021, h = 4)

**Décision.**
- K4 = K3 avec deux changements de mécanisme, sans facteur réglé sur N10 :
  - les erreurs viennent des 2 pseudo-origines les plus récentes ;
  - l'erreur départementale et l'erreur locale sont tirées conjointement,
    dans la même pseudo-origine.
  - Dérivation [communes, § K4](derivations/2026-11-14-axe2-communes.md),
    SHA-256 `1e801a5a9cdd`.
- **Soumissions.**
  - `n10_soumission_k4.parquet` : 2014–2020, h = 5.
  - `n10_confirmation_k4_2021h4.parquet` : origine 2021, h = 4, réservée.
    Elle n'est pas regardée par l'axe 2 ; seul l'axe 3 la juge.
- **Règle.** Un passage sur 2014–2020 ne vaut que s'il est confirmé sur
  2021 (h = 4) ou par le dépôt 2027.

**Pourquoi.** Le jugement N10 de K3 (axe 3) montre la cible. Il faut
contenir le sur-ajustement (consigne v2 du 2026-11-14).
**Ce qui le renverserait.** Les jugements N10 et de confirmation.

## 2026-11-14 — Projection communale : dépôt de K4 (origine 2025 → 2027, 2028), confirmation définitive selon N11

**Décision.**
- **Dépôt.** `v2/validation/depot/k4_communes_2026-11-14.parquet`,
  SHA-256 `039d21878b7a`, 84 084 lignes. Code : `communes_k4.depot()`.
  - Grains : commune, bv2022, EPCI.
  - Professions : IDE, MK, CD.
  - Colonnes : pred, q10, q90.
  - L'origine est **2025**, et non 2026 : c'est la dernière année
    CartoSanté.
- **Règle N11** (axe 3, SHA `4bf54ad0587a`). K4 n'est « confirmé » à un
  grain que s'il passe N10 (2014–2020) et 2021/h4. La confirmation
  définitive viendra de ce dépôt, quand les données 2027 et 2028 seront
  publiées.

**Pourquoi.** L'axe 3 a noté que 2025 a déjà été vue comme cible de
l'origine 2020 : la confirmation 2021/h4 n'est donc que partielle.
**Ce qui le renverserait.** Rien : un dépôt ne se modifie pas.

## 2026-11-14 — Projection communale : K4 non confirmé (N11) ; l'affichage reste au département ; pas de K5 sans décision

**Décision.**
- **K4 n'est pas confirmé.**
  - N10 échoue à tous les grains, sans progrès sur K3.
  - 2021/h4 échoue partout.
- **L'affichage reste au département** pour IDE, MK et CD. Il suit la
  règle du chantier : l'observé à la commune, avec la projection du
  département, et on le dit.
- **Pas de K5 sans décision de l'utilisateur·rice.** Quatre variantes ont
  été jugées. Chaque nouvelle variante qui voit le jugement précédent
  augmente le risque de sur-ajustement.
  - Une K5 devrait modéliser la largeur par profession × taille avec une
    loi explicite, et non par rééchantillonnage d'erreurs passées.
  - Elle ne compterait que par le dépôt 2027.

**Pourquoi.** Verdict N11 de l'axe 3 (commit 1d9545c). Les erreurs passées
ne prédisent pas l'échelle de l'erreur future, par profession.
**Ce qui le renverserait.** Le dépôt K4 (2027, 2028) calibré, ou une
décision de l'utilisateur·rice de lancer K5.

## 2026-11-14 — Correction : le dépôt communal de K4 mesure la couverture hors échantillon, il ne peut plus confirmer K4

**Décision.** Ceci corrige l'entrée « dépôt de K4 … confirmation définitive
selon N11 ».
- K4 a échoué aux étapes 1 et 2 de N11. Le dépôt
  (`039d21878b7a`, enregistré dans N11, commit cfc3b95) **mesurera la
  couverture hors échantillon** à la publication de CartoSanté 2027. Il ne
  peut plus confirmer K4.
- L'écart sur l'origine (2025 au lieu de 2026) est accepté par l'axe 3.
- **Règle de partage.** `v2/validation/depot/` appartient à l'axe 3. L'axe 2
  le prévient avant d'y écrire un dépôt.
  - Les dépôts A0 et C1 du 2026-11-14 y ont été écrits sans préavis, comme
    celui de K4.

**Pourquoi.** Message de l'axe 3, 2026-11-14.

## 2026-11-14 — Projection communale : K5 inscrit avant tout passage (09:01), à la demande de l'utilisateur·rice

**Décision.**
- **K5 donne une loi explicite à la largeur.** L'erreur relative suit une
  loi log-normale. Sa variance additionne trois termes :
  - le carré de l'écart-type départemental (terme commun au département) ;
  - φ/(n0 + ½), un terme de type Poisson ;
  - un plancher κ.
- Ces paramètres sont estimés dans la fenêtre, puis **rétrécis de moitié
  vers la moyenne des trois professions** (log σ_D, log φ, log κ).
- Dérivation [communes, § K5](derivations/2026-11-14-axe2-communes.md),
  SHA-256 `835537655204`.
- **Jugement.**
  - N10.
  - Puis l'origine réservée 2022, h = 3, proposée à l'axe 3 ; l'axe 2 ne
    la regarde pas.
  - Puis un dépôt préfixé `axe2_`, avec préavis à l'axe 3.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « Lancer K5 ». Les
jugements de K3 et K4 montrent un niveau d'erreur propre à la profession,
instable d'une période à l'autre.
**Ce qui le renverserait.** Les jugements de l'axe 3.
- *Écart avant passage (même jour).* Dans K5, σ_D devient un écart-type
  robuste (1,4826 × MAD) et b la médiane. Le diagnostic des paramètres
  avait montré σ_D = 1,74 pour les CD en 2018, à cause de départements à
  très petit total. Aucune couverture n'a été regardée avant l'écart.
  Dérivation avec l'écart : SHA-256 `0b87c9809dc6`.

## 2026-11-14 — Projection communale : dépôt de K5 écrit avant son verdict (accord de l'axe 3, N12)

**Décision.**
- **Dépôt.** `v2/validation/depot/axe2_k5_communes_2026-11-14.parquet`,
  SHA-256 `0169b97d4fac`, 84 084 lignes. Code : `communes_k5.depot()`.
  - L'origine est 2025 (dernière année CartoSanté), les cibles sont 2027 et
    2028.
  - Il couvre les grains commune, bv2022 et EPCI, pour les IDE, MK et CD.
- **Il est écrit avant le jugement de K5 par l'axe 3**, pour ne pas
  dépendre du résultat.
- La confirmation partielle se fait sur 2022, h = 3 (N12, SHA
  `ad08357a48fe`).

**Pourquoi.** Demande de l'axe 3, 2026-11-14 ; le dossier de dépôt lui
appartient.
**Ce qui le renverserait.** Rien : un dépôt ne se modifie pas.

## 2026-11-14 — Projection communale : K5 non confirmé (N12) ; fin des variantes ; affichage au département jusqu'au score des dépôts 2027

**Décision.**
- **K5 n'est pas confirmé.** Ses bandes sont trop étroites : l'écart-type
  robuste sous-estime une erreur départementale à queues lourdes.
- **Fin des variantes communales K à K5.** Aucun grain fin n'est
  calibré, et K3 reste le moins mal calibré.
- **L'affichage reste au département** pour IDE, MK et CD.
- **Les dépôts K4, K5 et C1 seront scorés en 2027**, comme mesure hors
  échantillon.
- **Une K6 n'est envisagée qu'avec une source nouvelle** : des flux
  d'installation par commune, ou une série plus longue.

**Pourquoi.** Verdicts N10, N11 et N12 de l'axe 3 (commits 1d9545c et
1e1f4c6). Chaque nouvelle variante qui a vu le verdict précédent augmente
le risque de sur-ajustement.
**Ce qui le renverserait.** Un dépôt 2027 calibré, ou une nouvelle source
de données communales.

## 2026-11-14 — Carte : bascule de `index.html` sur la refonte, après correction des P0 et P1 de l'UAT

**Décision.** La page refondue (`index-refonte.html`) remplace `index.html` ; le fichier à part est retiré.
Avant la bascule, les défauts confirmés de l'UAT agentique (rapport `2026-11-14-uat-agentique-carte.md`) sont corrigés :
- **P0** : la fiche est reconstruite quand la profession change, et une réponse périmée (autre territoire ouvert entre-temps) est ignorée ;
  mobile (≤ 700 px) : barre des professions défilante, leviers repliés à l'ouverture, fiche en panneau bas ;
  l'export marche aussi au niveau France et porte la définition de « libéral », les sources et millésimes, la version du code
  (`/api/meta` → `version`), les leviers modifiés en phrases avec leur statut et leur source, la méthode de la fourchette et les limites.
- **P1** : panneau des leviers défilant ; fiche raccourcie quand le bandeau de comparaison est affiché ; la fiche de région dit combien
  de ses départements sont régulés (« 0 sur 12 — la régulation n'a pas d'effet ici ») ; repères 2030 / 2035 / 2040 / 2050 dans la fiche ;
  axes du graphique élargis ; en-tête au-dessus de la carte pour les suggestions de recherche ; lien invalide → profession par défaut et
  leviers remis à zéro avec un message ; retour à la France avec des quotas régionaux → hausse retirée, avec un message.

**Pourquoi.** L'UAT est terminée (décision du 2026-11-14 : « on bascule une fois l'UAT terminée ») et l'utilisateur·rice a demandé
« Oui, corriger » puis la bascule. Vérifié en Chromium headless (1440×900 et 390×844) : changement de profession, fiche de région,
export régional et France, lien invalide, rendu mobile ; aucune erreur JavaScript.
**Non vérifié.** Pas de nouvelle recette par personas ; la légende des couleurs est masquée sur mobile.
**Ce qui le renverserait.** Une recette rejouée qui trouve un P0 sur la page basculée.

## 2026-11-14 — Langage naturel branché dans la carte : une phrase = un scénario complet, rien sans confirmation

**Décision.**
- `GET /api/interpret` dans `v2/prototype-carte/server.py` appelle le compilateur de `v2/langage` sur le jumeau déjà chargé
  (pas de second chargement). La profession et le territoire affichés servent de défaut.
- La carte ajoute « Décrire une politique en une phrase » en tête du panneau Leviers et un écran de confirmation : ce que j'ai
  compris, pas encore dans le modèle (avec la raison), pas compris, à noter, formulation neutre. **Rien n'est appliqué avant
  « Appliquer ce scénario ».**
- **Une phrase décrit un scénario complet** : elle remplace les leviers déjà réglés, et l'écran le dit. Les leviers restent
  réglables à la main ensuite.
- Glossaire étendu après un essai hors échantillon : formes verbales de « réguler », marqueurs de négation (« ne pas »,
  « supprimer », « renoncer à »…), entrée non modélisée `exercice_coordonne` (maisons et centres de santé, CPTS). Cas de test
  inchangés : 35/36 (en échantillon).

**Pourquoi.** L'utilisateur·rice : « continue the compiler for the politician ». « Ne pas réguler » activait la régulation :
un contresens qui doit être impossible avant la démo.
**Ce qui le renverserait.** Un jeu de cas écrit par une autre personne avec un taux trop bas : ajouter une étape de modèle de
langage évaluée sur ce jeu (décision du 2026-11-14 sur le compilateur).

## 2026-11-14 — Carte : corrections UAT en double (session v2 et fork v2-fork-6) fusionnées dans `index.html`

**Décision.** Les deux séries de corrections des P0/P1 de l'UAT sont gardées ensemble ; celles du fork priment là où elles
font mieux : sélecteur natif de profession sous 600 px, attente d'image bornée à 100 ms (rAF suspendu en arrière-plan),
validation complète du lien (leviers hors bornes, territoire inconnu, quotas régionaux sans région), `dropRegional()`,
panneau Leviers en colonne défilante, fiche en feuille du bas sous 600 px, export listant tous les leviers avec millésimes.
**Exception :** le fork masquait la légende tant que le panneau est ouvert, donc toujours sur ordinateur. Sur ordinateur, la
légende passe à droite (masquée seulement quand la fiche occupe ce côté) ; elle reste masquée sous 700 px.
**Pourquoi.** Le fork a signalé le doublon et rendu la main sur le fichier. Mesuré en Chromium headless : légende et panneau
se chevauchaient à 1280×720, 1440×900 et 1920×1080 ; plus aucun chevauchement après déplacement. Tests de non-régression
(profession, région, export France, lien invalide, mobile, phrases) : aucune erreur JavaScript.
**Limite.** À 1280×720, la légende à droite couvre le sud-est et la Corse.

## 2026-11-14 — Compilateur langage naturel : 47 % hors échantillon ; seuil de la décision atteint, choix laissé à l'utilisateur·rice

**Décision.** Le taux à citer est **14/30 (47 %)** sur 30 phrases écrites à l'aveugle (agent sans accès au glossaire ni au
compilateur), et non 35/36 (97 %, en échantillon). Le glossaire n'est pas ajusté sur ce jeu, qui reste hors échantillon.
Territoire 30/30 et négations 4/4 tiennent ; les leviers (17/30) échouent surtout sur des tournures absentes du glossaire et
sur le second levier des phrases combinées. L'écran de confirmation de la carte reste obligatoire : rien n'est appliqué sans
relecture.
**Pourquoi.** La décision du compilateur prévoyait : « un taux de correspondance trop bas → ajouter une étape de modèle de
langage, évaluée sur le même jeu ». 47 % est trop bas pour une démo sans confirmation.
**Ouvert.** Étendre le glossaire (puis un nouveau jeu à l'aveugle) ou ajouter une étape de modèle de langage pour l'analyse
seulement : à décider.

## 2026-11-14 — Carte : mode expert (flux par année, leviers bruts, 3 scénarios épinglés, export JSON)

**Décision.** Un bouton « Expert » ouvre un tiroir à droite, sur les mêmes réponses du jumeau : (1) écart au tendanciel par
flux en 2030–2050, avec tendanciel, scénario et fourchette ; (2) chaque levier avec valeur, unité, paramètre du jumeau,
délai, statut et source ; (3) jusqu'à 3 scénarios épinglés côte à côte, toutes professions et tous territoires ; (4) un
export JSON (scénario affiché, épinglés, métadonnées des leviers, version du code).
**Non fait, et dit dans l'écran :** territoire par levier (seules les places peuvent être limitées à la région ouverte),
verrou d'estimateur (un seul estimateur branché sur la carte), rampe réglable (les délais sont ceux du jumeau).
**Pourquoi.** Périmètre « décideur technique » demandé par l'utilisateur·rice ; vérifié en Chromium headless (onglets,
épinglage France + Puy-de-Dôme, JSON téléchargé, aucune erreur JavaScript).

## 2026-11-14 — Correction : l'écart dentistes « 76 000 contre 62 000 » n'existe pas

**Décision.** 76 000 était la projection tendancielle 2050 ; l'effectif privé 2026 est 47 347, sous le total RPPS tous modes
de 48 690 (1er janvier 2026, mesuré). Aucun double compte (rapport `reports/2026-11-14-reconciliation-dentistes.md`). Les
quatre autres professions ont aussi un privé 2026 inférieur à leur total. La phrase de la synthèse est corrigée ; le chiffre de
62 000 n'a pas de source retrouvée.
**Pourquoi.** L'erreur venait de la session v2 (comparaison d'une valeur 2050 à un total 2026).

## 2026-11-14 — Compilateur : glossaire étendu par classes d'erreurs, 70 % sur un troisième jeu à l'aveugle

**Décision.** Le glossaire et le compilateur sont étendus en deux passes, chacune guidée par les échecs d'un jeu à l'aveugle et
mesurée sur le suivant, jamais vu : 47 % (jeu 1, version d'origine) → 53 % (jeu 2) → **70 % (jeu 3, chiffre à citer)**.
Changements par classe : synonymes et formes conjuguées (racines), fractions (« un bon tiers »), demi-années, quantité
cherchée selon le type du levier (« avant 60 ans » n'est plus une durée), sens pris au mot le plus proche de la quantité,
arrondi au pas du levier, « emploi et retraite » non coupé, « multiplié par N », « combien de X » pour la profession,
politiques de rémunération non modélisées. Cas d'origine inchangés (35/36).
**Convention gardée :** deux professions ou deux territoires → le premier cité, avec un avertissement (les jeux 1 et 2
attendaient « aucun » : écart de convention, pas d'erreur ; le jeu 3 a été écrit avec la convention du compilateur).
**Pourquoi.** L'utilisateur·rice : « Extend glossary ». Mesurer sur un jeu jamais vu à chaque version évite de se tromper
sur des cas déjà corrigés.
**Ouvert.** Gentilés de ville (6 échecs sur 9 au jeu 3), négation partielle, « remplacer un confrère qui part » ; un jeu 4 pour mesurer.

## 2026-11-14 — Compilateur, tour 4 : 80 % sur un quatrième jeu à l'aveugle

**Décision.** Ajouts par classe : gentilés de villes et de régions (avec accords), « remplacer un confrère / un départ » pour
la régulation, « % des territoires / communes » pour la part des zones, « réservée à la région » et sa négation, comparatif
placé après la quantité prioritaire sur le verbe (« accueillir 30 % … en moins »), « doublement ». Mesure sur le jeu 4, jamais
vu : **24/30 (80 %, chiffre à citer)** ; territoire et profession 30/30, leviers 25/30. Jeux 1 à 3 : 29/30, 27/30, 30/30
(en échantillon, non citables) ; cas d'origine 35/36.
**À signaler :** une erreur de mauvais levier (« formés hors de France » → places en formation). L'écran de confirmation la
rend visible ; c'est la première classe à corriger au tour suivant.
**Pourquoi.** L'utilisateur·rice : « Yes, round 4 ».

## 2026-11-14 — Compilateur, tour 5 : 83 % sur un cinquième jeu à l'aveugle

**Décision.** Ajouts par classe : « formés / diplômés hors de France » vers les diplômés étrangers (corrige le mauvais levier
du tour 4), verbes multiplicateurs conjugués (« doublait », « triplerait »), « diviser par N », durée des études (internat)
non modélisée, racines « facilit-, assoupl-, élarg-, étend- », suppression d'un terme qui avalait la quantité (« an de
travail »). Mesure sur le jeu 5, jamais vu : **25/30 (83 %, chiffre à citer)** ; profession 30/30, territoire 29/30, leviers
26/30. Jeux 1 à 4 sans régression (29, 27, 30, 30 sur 30, en échantillon) ; cas d'origine 35/36.
**À signaler :** deux erreurs de mauvais levier subsistent (« diplômées européennes », « se former en Belgique » → places en
formation) ; l'écran de confirmation les rend visibles.
**Pourquoi.** L'utilisateur·rice : « Yes, round 5 ».

## 2026-11-14 — Compilateur, tour 6 : 70 % sur le jeu 6 ; plateau d'environ 77 % pour l'approche glossaire

**Décision.** Ajouts par classe : un diplôme obtenu hors de France (Europe comprise) l'emporte sur les places en formation
dans une même proposition, sigles de régions (PACA, IDF, AURA…), écart entre deux âges (« 67 ans au lieu de 65 et demi »),
verbes familiers (« grimper », « raboter »). Mesure sur le jeu 6, jamais vu : **21/30 (70 %)**. Jeux 1 à 5 sans régression.
**Chiffre à citer : environ 77 %**, moyenne des jeux 5 et 6 (46/60) ; erreur type d'un jeu de 30 ≈ ±8 points.
**Constat.** Le gain par tour a plafonné (80 → 83 → 70) : les échecs restants sont des formes conjuguées de termes multi-mots
et des propositions combinées, que des termes exacts couvrent mal. Selon la décision du compilateur, l'étape suivante serait
un modèle de langage pour l'analyse seule (jamais le calcul), évalué sur les jeux 5 et 6 ; non engagé sans accord.
**Aussi.** « Auvergne » et « Rhône-Alpes » renvoient à Auvergne-Rhône-Alpes : l'exemple du champ de saisie de la carte
(« former 20 % de kinés en plus en Auvergne ») se compile désormais en places +20 %, kinés, R84 (signalé par une session sœur).

## 2026-11-14 — Carte : curseurs principaux visibles sous la phrase (remplace « tout replié » pour le panneau)

*Remplacé en partie le 2026-11-15 : les familles sont repliées au chargement (entrée « familles de leviers repliées »).*
**Décision.** Dans le panneau Leviers, sous « Décrire une politique en une phrase », chaque famille est dépliée et montre son
curseur principal (places, diplômés étrangers, régulation, retraite) ; les réglages secondaires restent sous « Plus de réglages ».
L'accordéon (une seule famille ouverte) est retiré. Sur mobile, le panneau reste replié à l'ouverture.
**Remplace** la règle de la refonte élu·e « leviers repliés » pour l'intérieur du panneau (refonte du 2026-11-14, gardée par ailleurs).
**Pourquoi.** L'utilisateur·rice, relayé par une session sœur : garder les deux façons de régler une politique, la phrase et
les curseurs ; repliés, les curseurs semblaient avoir disparu. Vérifié en Chromium headless (1440×900 : 4 familles ouvertes,
curseur fonctionnel ; 390×844 : panneau replié ; aucune erreur JavaScript).

## 2026-11-14 — Population, densité pour 100 000 et activité par professionnel dans la carte (v1 L32 et L14 repris)

**Décision.**
- **Population** : Insee Omphale 2022 par département (`data/processed/population.parquet`, chargeur v1), 3 scénarios
  (central, basse, haute ; 2050 : 69,2 / 63,9 / 74,7 M). Exposée comme hypothèse de contexte `pop_scen` (reprend L32 de la v1).
- **Densité** = effectif libéral × activité / habitants × 100 000, pour le tendanciel et le scénario, par territoire et par
  année (`/api/scenario` : `pop`, `dens_base`, `dens_scn` ; `/api/carte` : `p26`, `p50`). Carte : troisième variable
  « Densité 2050 », en écart à la densité France (lexique : au-dessus / en dessous de la moyenne). Kinés 2026 : 150,7 pour
  100 000 (mesuré, central).
- **Activité** : hypothèse `activite` (0,8 à 1,1, défaut 1), « × activité d'aujourd'hui », **supposée** : aucune série
  ouverte d'équivalents temps plein n'a été vérifiée, donc aucune valeur de base par profession n'est inventée. Elle ne
  change que la densité (offre en équivalents temps plein), pas l'effectif (reprend L14 de la v1).
- Les deux sont des **hypothèses de contexte**, pas des politiques : elles ne comptent pas dans « N leviers modifiés », sont
  rappelées sous le résumé, et une phrase du compilateur ne les modifie pas.
**Pourquoi.** L'utilisateur·rice : « /go 1 4 » (densité, priorité 3 des tests utilisateurs ; étape 1 du sujet : offre +
population → densité). Vérifié en Chromium headless : vue densité, changement de scénario de population et d'activité,
repères de la fiche, mode expert ; aucune erreur JavaScript.
**Non fait.** Densité à la commune (population communale non chargée) ; besoin (module de demande) toujours ouvert.

## 2026-11-14 — Données traitées commitées (data/processed/, v2/data/processed/), données brutes toujours exclues

**Décision.** Les deux dossiers de données traitées (≈ 37 Mo, 34 fichiers, le plus gros 15,6 Mo) sont commités ; ils étaient
ignorés depuis le premier commit. Les données brutes (≈ 3,6 Go) restent ignorées. Chaque dossier a un `MANIFEST.md` généré par
`v2/data/manifest.py` : taille, empreinte SHA-256, script de construction et son dernier commit, commande, source.
`manifest.py --check` échoue si un fichier change sans manifeste ou si un script de construction cite un fichier des
organisateurs (inscrits par université, `990_drees_mmop2`, sous accord de confidentialité).
**Pourquoi.** L'utilisateur·rice : « ok go ahead », pour que l'équipe n'ait pas à tout reconstruire. Vérifié : aucun script
qui écrit un fichier traité ne lit un fichier des organisateurs (ils ne servent qu'au module de formation, à la volée).
Toutes les sources sont ouvertes (DREES, Insee, ameli, CartoSanté, Annuaire Santé, FINESS, zonage data.gouv).
**Remplace** l'exclusion de `data/processed/` et `v2/data/processed/` du `.gitignore` du premier commit.
**Ce qui le renverserait.** Un fichier traité dérivé d'une donnée non ouverte, ou une taille qui dépasserait les limites de
GitHub (100 Mo par fichier).

## 2026-11-14 — La v1 est absorbée dans v2 ; README réécrit autour du démarrage sans données brutes

**Décision.**
- **Code** : `sante/` → `v2/sante/` (chargeurs, modèle, estimateurs ; 21 fichiers v2 l'importent) ; `app/levers.py` →
  `v2/sante/levers_v1.py` (référence du critère C7) ; contours `app/assets/…geojson` → `v2/prototype-carte/assets/`.
  L'application Streamlit `app/` est **supprimée**, avec les dépendances `streamlit` et `plotly`.
- **Registre v1** (décisions, ledger, rapports, dérivations, explorations, présentations, figures, ROADMAP v1, artifacts,
  scripts) → `v2/docs/lab/archive-v1/`, en lecture seule ; lexique → `v2/docs/lab/lexicon.md` ; catalogue des leviers →
  `v2/docs/lab/levers-catalogue-v1.md` ; modèles Obsidian → `v2/docs/templates/`. Les liens relatifs sont recalculés.
- **Restent à la racine**, et c'est voulu : `data/` (données de base, 38 fichiers y lisent `data/processed` ou `data/raw`,
  et chaque poste y garde ses fichiers bruts) et `docs/lab/profile.md` (chemin lu par les skills de `.claude/`).
- **Protocoles gelés non touchés** : `v2/validation/preregistered/` garde ses liens (certains étaient déjà cassés) ; le
  gel par SHA-256 prime.
- **README réécrit** : « Démarrer en 5 minutes » en tête (clone, `uv sync`, serveur de la carte), sans données brutes ;
  état des axes à jour ; reconstruction des données à part. `CLAUDE.md`, `Home.md`, le profil, le crochet de cohérence,
  `.claude/launch.json` (entrées v1 et chemins absolus retirés) et `Records.base` suivent.
**Pourquoi.** L'utilisateur·rice : « enlève la v1, mets à jour toute la readme », option « absorber la v1 dans v2 »,
après des erreurs de lancement chez des coéquipiers (fichiers de `data/raw/` absents).
**Vérifié.** Critères du jumeau 18/18 ; carte relancée (5 professions, 101 départements, contours) ; **copie des seuls
fichiers suivis, sans aucune donnée brute** : serveur prêt en 10 s, `/api/carte`, `/api/scenario` (densité),
`/api/interpret`, page et contours répondent ; `manifest.py --check` OK.
**Remplace** « La v1 (`sante/`, `app/`, `docs/lab/`) est figée et se consulte en lecture seule ».

## 2026-11-14 — Carte : option 1 en direction A (Bertin) retenue, trois panneaux dépliables

**Décision.**
- La refonte de la carte suit l'**option 1** (même pile HTML + MapLibre, sans build, colonnes
  fixes) avec l'habillage de la **direction A** :
  - ~~fond blanc, encre noire, police Atkinson Hyperlegible ;~~ **remplacé le 2026-11-14** par l'habillage DSFR
    (entrée « Carte : habillage DSFR ») ;
  - ~~gamme bistre ↔ bleu pétrole, jamais rouge ni vert (gardée pour les données).~~ **Remplacé le 2026-11-15** pour la
    carte par la gamme DSFR orange ↔ vert (entrée « Carte : dégradé DSFR orange ↔ vert »).
- **Trois panneaux dépliables** :
  - **Scénario** à gauche ; replié, il devient une barre de 60 px avec le nombre de leviers
    modifiés ;
  - ~~**Liste classée** sous la carte, avec une bascule **Départements / Régions** ;~~ **retirée le
    2026-11-14** (voir « Carte : panneau de classement retiré ») ;
  - **Territoire** à droite, avec les onglets Territoire, Comparer et Expert ; replié, il
    garde le nom et l'écart 2050.
  - Replier un panneau agrandit la carte.
- Mêmes fonctions que la page actuelle, aucune perdue. ~~Le curseur d'année reste hors périmètre.~~
  **Remplacé le 2026-11-14** : le curseur d'année a été livré par l'équipe (entrée « Curseur d'année sur la carte ») ;
  il est repris dans la refonte, comme le panneau « Questions » (entrée « Carte option 1 : ajustements »).
- Maquette de référence : écran « Option 1 — direction A (Bertin) · retenue » du canevas
  https://claude.ai/artifact/3VNzVPT3qTK3XLPja1dKxg.
- Remplace l'entrée « Refonte de l'interface de la carte, à fonctions égales » de la section
  Open.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « Option 1 A Bertin. Avec menu Scénario,
Département/Région, territoire dépliable ».
**Interprétation à confirmer.** « Département/Région » est lu comme la bascule d'échelle de la
liste classée, et non comme un quatrième panneau.
**Ce qui le renverserait.** La recette iso-fonctionnelle montre qu'une fonction de la page
actuelle n'a pas de place dans les trois panneaux.

## 2026-11-14 — Agent conversationnel qui interprète les sorties du jumeau (v2/agent), branché dans la carte

**Décision.**
- `v2/agent/` : agent à outils (SDK `anthropic`, boucle manuelle), modèle `claude-opus-5-5` par défaut (`AGENT_MODEL`),
  effort `medium` (`AGENT_EFFORT`), repli serveur `fallbacks: "default"` en cas de refus. Il **explique, il ne calcule pas** :
  5 outils (`meta`, `territoire`, `scenario`, `carte`, `interpreter`) appellent le serveur de la carte et renvoient des
  digests **déjà arrondis et déjà dérivés par du code déterministe** (écart, écart en %, évolution, fourchette
  s × (1 ± k × horizon) comme le résumé de la carte, flux cumulés). Le modèle choisit et explique.
- **Garde-fous mesurés** (`garde_fous.py`) : ancrage (chaque nombre de la réponse se retrouve, à la précision affichée,
  dans une sortie d'outil, la question ou le contexte de la carte) et lexique neutre (termes de `lexicon.md`). Le panneau
  affiche le résultat du contrôle sous chaque réponse ; une réponse non ancrée est signalée, pas masquée.
- **Clé** : `ANTHROPIC_API_KEY` dans l'environnement du serveur, ou dans un `.env` local à la racine (ajouté au
  `.gitignore`). Jamais dans le dépôt, jamais renvoyée au navigateur. Sans clé : `/api/agent/etat` le dit, la carte reste
  entière.
- Carte : bouton « Questions », panneau à droite (feuille en bas sur mobile), `POST /api/agent` (contexte = profession,
  territoire, leviers affichés ; historique texte des 8 derniers tours). L'agent ne modifie pas les leviers de la carte.
- Jeu de 22 questions écrit avant le code (`v2/agent/questions.yaml`) ; plan dans
  `v2/docs/lab/derivations/2026-11-14-agent-interprete.md`.
**Pourquoi.** Demande relayée par la session principale : un agent qui interprète les résultats bruts pour un public non
technique. Conforme à la décision du compilateur (« un modèle de langage pour l'analyse seule, jamais le calcul »).
Alternative la moins chère (gabarit de phrases à trous) gardée comme sol : les digests en sont la partie chiffrée.
**Ce qui le renverserait.** Moins de 90 % de réponses entièrement ancrées sur le jeu de 22 questions : repli sur le gabarit
déterministe pour tous les chiffres.
**Mesures.** Aucune pour l'instant : pas de clé d'API dans l'environnement de la session. Commit sans mesure à la demande
de l'utilisateur·rice (« Commit sans mesure »). Vérifié sans clé : `/api/agent/etat` et `POST /api/agent` répondent
« indisponible », panneau ouvert sur ordinateur et mobile, aucune erreur JavaScript ; test unitaire des garde-fous
(`uv run python v2/agent/garde_fous.py`). Mesure ouverte dans `open.md`.

## 2026-11-14 — Vidéo de présentation : Remotion + video-shotcraft, 3 fonctions, voix off IA

**Décision.**
- Vidéo motion de 57 s pour le jury, en 16:9, dans `v2/video/` (projet Remotion, rendu local).
- Elle montre trois fonctions de la carte :
  1. explorer un territoire (France → Auvergne-Rhône-Alpes → Puy-de-Dôme, fiche kinés : 1 071 en 2026, 1 731 en 2050, fourchette de 1 244 à 2 219) ;
  2. simuler une politique (préréglage « Former 20 % de plus » : +19 110 kinés en France en 2050 par rapport à la tendance) ;
  3. décrire une politique en une phrase (« Ce que j'ai compris », puis confirmation).
- Le backtest et le mode expert ne sont pas montrés.
- Images : de vraies captures de la carte en 2x (`v2/video/capture/capture.mjs`, Puppeteer) animées par une caméra 2D, plus des scènes de typographie et une carte des départements tracée (contours IGN/Etalab simplifiés).
- Habillage : les tokens de la carte (IBM Plex Sans/Mono, fond `#F4F5F2`, encre `#16181A`, sélection `#1B3A8C`, couleurs des professions).
- Voix off IA française : ElevenLabs, voix « Perle », modèle eleven_v4, via le connecteur. Le minutage des scènes et les sous-titres viennent de la transcription mot à mot (Scribe, `src/voix-words.json`).
- Musique : une piste Mixkit (licence libre, sans attribution), en sourdine. Une version sans musique est aussi rendue.
- Skills installés : `remotion-dev/skills` (commités) et `video-shotcraft`, en mode autonome. Shotcraft pèse 54 Mo : il est ignoré par git et se réinstalle avec `npx skills add Vincentwei1021/video-shotcraft`.

**Pourquoi.** L'utilisateur·rice a choisi : jury, 60 à 75 s au plus, voix off IA, Remotion + shotcraft, visuels mixtes, et ces trois fonctions.
- La voix dit « plus dix-neuf mille » (arrondi), l'écran affiche +19 110.
- La styleframe HTML de shotcraft n'a pas été faite : la carte a déjà un système visuel figé (direction A, « sémiologie graphique »), repris tel quel.

**Non fait.**
- Pas de bruitages Freesound.
- Pas de vraie capture vidéo du vol de caméra MapLibre : il est simulé par des fondus et des zooms entre captures.

**Ce qui le renverserait.** Des chiffres de la carte qui changent (recapturer et mettre à jour les encarts), ou une durée imposée différente.

## 2026-11-14 — Curseur d'année sur la carte : 2026 à 2050, pas annuel, défaut 2050

**Décision.**
- La carte a un curseur d'année (barre du haut, 2026 → 2050, pas de 1 an, repères 2030 · 2035 · 2040 · 2045 · 2050) et un bouton ▶ qui fait défiler les années.
- **Valeur par défaut : 2050.** Sans toucher au curseur, l'écran est identique à avant.
- L'année pilote la coloration, la légende, l'infobulle, le résumé « Tendance / Scénario », l'effet par famille de leviers, la fiche territoire (effectif, fourchette, écart et flux à l'année) et la comparaison. Le graphique garde l'axe jusqu'en 2050 et marque l'année d'un trait vertical.
- `/api/carte` renvoie toutes les années en un appel : par département, des séries `b[]`, `s[]`, `p[]` sur `years` = 2026…2050. Les anciennes clés (`b26`, `s26`, `b50`, `s50`, `p26`, `p50`) sont conservées. Bouger le curseur ne refait aucun appel au serveur.
- Les bornes de couleur de « Écart au tendanciel » sont calculées sur 2050 : les teintes restent comparables d'une année à l'autre.
- L'année entre dans le lien partagé (`y=`, omis à 2050) et dans le contexte envoyé à l'agent. L'outil `carte` de l'agent prend un paramètre `annee` (défaut 2050).
- Infirmiers (origine 2023) : la légende précise « observé jusqu'en 2023, 2026 déjà projeté ».

**Pourquoi.** Demande de l'utilisateur·rice : lire 2030, 2035, 2045… et pas seulement 2050. Le jumeau calcule déjà chaque année (`engine.run` garde tous les états) : seul `/api/carte` réduisait à deux dates. Les années proches sont aussi les plus défendables : le backtest couvre environ 10 ans (décision « horizon de référence 2050 »).

**Mesures.** `carte()` passe à environ 100 ms (kinés 106 ms, infirmiers 98 ms, toutes années), réponse 78 ko. Sous le seuil de 150 ms de la décision « écran carte ». Valeur 2050 inchangée (Puy-de-Dôme, kinés : 1 731).

**Ce qui le renverserait.** Un passage au grain communal (le volume × 25 années imposerait une grille précalculée), ou un retour UAT montrant que le curseur fait lire les années lointaines comme plus sûres que les proches.

## 2026-11-14 — Carte option 1 : recette iso-fonctionnelle, page `index-option1.html`, ajustements

**Décision.**
- **Recette** `v2/prototype-carte/recette.mjs` : Node pilote Chrome headless, sans dépendance, avec WebGL logiciel
  (SwiftShader).
  - 30 contrôles portent sur la page actuelle, plus R31 (curseur d'année) et R32 (panneau Questions).
  - 5 contrôles O01–O05 sont propres à la refonte : leviers ouverts, 3 panneaux, liste Dép./Rég., repère, onglets.
- **Page** `index-option1.html` : option 1 en direction A. La logique et les identifiants de `index.html` sont repris,
  y compris le curseur d'année et l'agent ajoutés par la PR #2. `server.py` n'est pas touché. `index.html` reste la
  page servie jusqu'à la bascule.
- **Ajustements demandés par l'utilisateur·rice**, le 2026-11-14 :
  - titre « Offre de soins libérale » retiré ;
  - bouton A+ retiré ;
  - chat accessible par une icône sur la carte, à gauche des boutons de zoom (le panneau « Questions » n'est plus un
    onglet) ;
  - panneau Scénario réduit à un curseur par paramètre ;
  - légende réduite aux boutons d'indicateur et à la gamme, le titre restant lisible par les lecteurs d'écran.
- **Choix pris sans demande explicite.** Le panneau simplifié ne supprime rien : phrase, résumé et préréglages,
  réglages fins, hypothèses et sources sont repliés dans « Plus ». La recette garde ainsi toutes ses fonctions.

**Mesures.**
- Page actuelle : 30/30 (avant la PR #2), recalcul p95 160 ms.
- Refonte avant le curseur d'année et les ajustements : 35/35, recalcul p95 83 ms.
- **Non mesuré** après le report du curseur, de l'agent et des ajustements : l'utilisateur·rice a demandé de ne pas
  relancer la recette. Seule la syntaxe JavaScript est vérifiée (`node --check`).

**Pourquoi.** « oui, écris la recette puis code l'option 1 », « Prends en compte les changements liés à la feature du
curseur », puis les demandes d'ajustement ci-dessus.

**Ce qui le renverserait.** La recette relancée trouve un contrôle en échec sur la page ajustée.

## 2026-11-14 — Chatbot intégré à la carte (prototype) : relais vers `chatbot/`, Claude Haiku 5.5, glossaire sans clé

**Décision.**
- Le panneau « Questions » de la carte relaie vers le chatbot de `chatbot/` (passerelle en lecture seule, port 8770, et
  agent, port 8768 ; code de Juliette Konop, poussé dans le dépôt le 2026-11-14). **Un seul moteur** : `v2/agent/` est
  gelé, la carte ne l'appelle plus ; seul son contrôle du lexique (`garde_fous.lexique`) est appliqué aux réponses.
- La passerelle interroge **le dépôt actuel** (`JUMEAU_REPO=..`), pas la copie figée `chatbot/vendor/` (`426422c`).
- **Modèle : `claude-haiku-5-5`** (choix de l'utilisateur·rice), `CHAT_FALLBACKS=0` (pas de repli serveur pour Haiku).
  Sans clé : mode glossaire (sans IA) du chatbot.
- Contexte de la carte (profession, territoire, leviers modifiés, année, « densités pour 100 000 habitants ») ajouté à la
  question en mode IA seulement ; le glossaire lit la phrase seule.
- Lexique : « pas une prévision » et ses variantes ne sont plus signalés (formule recommandée par le lexique).
**Pourquoi.** L'utilisateur·rice : « commençons un premier prototype de chatbot intégré », puis « on utilisera haiku5.5 ».
Le challenge du même jour (§ Open) demandait un seul moteur ; celui de `chatbot/` est le plus isolé et testé.
**Vérifié.** Sans clé : kinés ARA 2035 +20 % → « environ 17 100, entre 15 300 et 18 900 » (glossaire, 0,1 s). Avec clé
(Haiku 5.5) : même question en 12,7 s ; depuis la carte, « Pourquoi ce résultat ? » rattaché au scénario affiché, 6,9 s,
écart par flux (+525 entrées, −2 sorties), délai (2032), statut « supposé » et sources ; vérification « ok » ; ordinateur
et mobile, sans erreur JavaScript. Trois questions, pas une mesure.
**Non fait.** Taux sur les 22 questions (`open.md`) ; nettoyage de `chatbot/vendor/` (77 Mo) et du `.bundle`, à voir avec
Juliette ; la tolérance ±6 % de `chatbot/chat/verif.py` reste en place.
**Remplace** l'usage de `v2/agent/` par la carte (décision « Agent conversationnel… » du 2026-11-14).

## 2026-11-14 — L'agent conversationnel devient l'interface principale ; squelette fonctionnel en attendant l'UX

**Décision.** L'agent conversationnel (chatbot de `chatbot/`, relayé par la carte) est l'**interface principale** avec
l'utilisateur·rice. La mise en page (conversation au centre, à côté, ou seule) **attend les propositions des UX designers
de l'équipe** ; d'ici là, le panneau « Questions » de la carte reste le squelette fonctionnel, sans refonte.
**Remplace** « personas et application : couche ultérieure » (recadrage du 2026-11-14, `docs/lab/profile.md`, annoté) et
la ligne « En attendant : aucun travail nouveau sur le moteur » du challenge (§ Open) : la qualité des réponses compte
désormais pour l'usage. La question « LLM ou glossaire » reste mesurable (§ Open), mais le mode IA est le mode par défaut.
**Pourquoi.** L'utilisateur·rice : « maintenant l'agent conversationnel est l'interface avec l'utilisateur principale »,
puis « on va attendre les propositions des ux designers de la team, on va juste avoir pour l'instant un squelette
fonctionnel ».

## 2026-11-14 — Chatbot intégré : première mesure sur les 22 questions (Claude Haiku 5.5)

**Mesure** (`v2/agent/evaluer_chatbot.py`, relais de la carte → `chatbot/`, mode IA, une session par question ;
`v2/agent/score_chatbot.txt`, réponses dans `reponses_chatbot.jsonl`) :
| Critère | Résultat |
|---|---|
| Réponses entièrement ancrées, règle stricte (précision affichée) | **21/22** ; nombres ancrés 260/261 (99,6 %) |
| Non bloquées par la vérification du chatbot (±6 %) | 22/22 (12 « ok », 10 « corrigée ») |
| Sans terme du lexique interdit | 18/22 ; les 4 occurrences sont des négations ou des refus (« pas des « déserts médicaux » », « non des prévisions », « ne peut pas dire si … un manque », « pas d'avis sur ce qu'il faut faire ») : **0 jugement** à la relecture |
| Hors périmètre signalé quand attendu | 5/5 |
| Flux nommés quand attendu | 5/5 |
| Latence | médiane 7,4 s, max 15,6 s |
Le seul nombre non ancré : « 2040 » dans un exemple de question suggéré (q20).
**Premier passage** (16:55, même jeu) : 13/22 ancrées. Les écarts venaient de la mesure, pas des réponses : « 100 000 »
(unité « pour 100 000 habitants ») et les nombres du périmètre (prompt système du chatbot) n'étaient pas comptés comme
sources. Corrigé dans `evaluer_chatbot.py` avant le second passage ; lexique : « non (d')une prévision » ajouté aux
formules permises.
**Défaut observé.** Sans contexte de la carte, la vérification du chatbot (±6 %) retire « 100 000 » des réponses et la
densité devient « 201,4 kinés par habitant rapporté à la population » (q01, premier passage). Le relais de la carte
ajoute « densités pour 100 000 habitants » au contexte en mode IA, ce qui l'évite dans la carte ; correctif durable dans
`chatbot/chat/verif.py` (unité de référence), à voir avec Juliette.
**Limites.** Un seul passage par configuration, sur un jeu écrit par l'auteur de l'agent ; la justesse qualitative
(phrases) n'est pas mesurée, seulement relue pour le lexique ; coût non mesuré (le chatbot ne renvoie pas l'usage).

## 2026-11-14 — Squelette : la conversation est ouverte au chargement de la carte

**Remplacé le 2026-11-14** par l'entrée « Carte : panneau Résultat à modes de visualisation, assistant en fenêtre modale » : l'assistant s'ouvre dans une fenêtre modale par un bouton sur la carte, fermée au chargement.

**Décision.** Le panneau « Questions » s'ouvre au chargement (ordinateur : à droite ; mobile : en bas), refermable par
le bouton « Questions » ou la croix. Aucun autre changement de mise en page : la refonte attend l'équipe UX.
**Pourquoi.** L'utilisateur·rice : « on avait dit que c'était la nouvelle interface principale pour l'utilisateur » ; un
panneau fermé par défaut contredisait la décision précédente. Vérifié dans le navigateur (ordinateur et mobile).

## 2026-11-14 — Carte option 1 : chat relayé vers `chatbot/`, comme `index.html` (fusion de `main`)

**Décision.** `index-option1.html` reprend le relais du panneau « Questions » vers le chatbot de `chatbot/` (décision
« Chatbot intégré à la carte (prototype) » du même jour) : session par onglet au lieu de l'historique, statut de
vérification (`ok`, `corrigee`, `bloquee`), mode glossaire sans IA, gras rendu. Le libellé garde le style de la page
(« Contrôle : … », sans pictogramme). L'accès par l'icône sur la carte ne change pas.
**Pourquoi.** Résolution des conflits de la PR #3 : `/api/agent` ne renvoie plus `ancrage` ; sans ce report, le chat
de la page option 1 afficherait « Serveur injoignable. ».
**Non mesuré.** Recette non relancée (demande de l'utilisateur·rice) ; seule la syntaxe JavaScript est vérifiée
(`node --check`).
**Ce qui le renverserait.** La mise en page du chat proposée par les UX designers (décision « L'agent conversationnel
devient l'interface principale »).

## 2026-11-14 — Option 1 : la conversation ouverte au chargement, premier onglet, colonne élargie

**Remplacé le 2026-11-14** par l'entrée « Carte : panneau Résultat à modes de visualisation, assistant en fenêtre modale » : l'assistant s'ouvre dans une fenêtre modale par un bouton sur la carte, fermée au chargement.

**Décision.** Dans `index-option1.html`, l'onglet **Questions** est le premier de la colonne de droite et il est ouvert
au chargement ; quand il est affiché, la colonne passe de 27 rem à `max(27 rem, min(34 rem, 38 vw))`. L'icône sur la
carte reste (elle bascule entre Questions et Territoire). Pas de focus automatique, pour ne pas ouvrir le clavier sur
mobile. Le reste de la mise en page attend les maquettes de l'équipe UX.
**Tranche** la question ouverte « Carte option 1 : chat fermé derrière une icône, ou ouvert au chargement ».
**Pourquoi.** L'utilisateur·rice : « c'est bof » (conversation secondaire alors qu'elle est l'interface principale), puis
« go ahead » sur cette option (15 min) plutôt qu'une mise en page centrée sur la conversation, qui préempterait l'UX.
**Vérifié.** Recette `recette.mjs --option1` : 35/37 ; R25 (A+) échoue aussi sur la version d'avant (pas de bouton A+
dans l'option 1) ; R14 (748 ms) était du bruit : relancé deux fois, 161 et 178 ms. R32 (panneau Questions) et O05
(onglets) passent.
**Non vérifié.** Dans le panneau navigateur de l'application, la carte de l'option 1 reste grise, avant comme après ce
changement (la recette, elle, la voit dessinée) ; non diagnostiqué.

## 2026-11-14 — Conversation pilote : vocabulaire des grandeurs calculé par le code, scénario affichable sur la carte

**Décision.**
- **Vocabulaire des grandeurs** (`v2/docs/lab/lexicon.md`, nouvelle section) : évolution et écart (stable · légère ·
  marquée · forte hausse / baisse), densité comparée à la France (nettement inférieure · inférieure · proche ·
  supérieure · nettement supérieure à la moyenne nationale), incertitude (faible · modérée · élevée, « extrapolée »
  au-delà de 10 ans), délai d'effet (court · moyen · long terme). Seuils **supposés**, à valider par l'équipe.
- Les mots sont **calculés par la passerelle** (`chatbot/passerelle/requetes.py` : champ `qualificatifs` de chaque
  ligne, `delai_qualificatif` de chaque levier), jamais choisis par le modèle de langage. Le prompt
  (`chatbot/chat/agent.py`, règle 9) impose ces mots ; `chatbot/chat/verif.py` (`qualifs_non_rattaches`) refuse un
  qualificatif absent des résultats et une liste d'adjectifs hors vocabulaire (modeste, significatif, considérable…),
  dans la même boucle « correction puis blocage » que les nombres.
- **Densité France** jointe aux résultats (`densite_100k_france_scenario`, `densite_ecart_a_la_france_pct`) ; dans
  `classer`, la moyenne simple des départements est renommée `moyenne_simple_des_departements_densite` (elle n'est pas la
  densité nationale). Une hausse de places limitée à une région est retirée du calcul de la référence nationale.
- **La carte suit la conversation, sur clic** : le relais renvoie le scénario simulé (profession, territoire, leviers,
  année ; préférence aux appels avec leviers, puis à un territoire plus fin que la France), et le panneau propose
  « Afficher ce scénario sur la carte » (`index.html` et `index-option1.html`). Le territoire est ouvert avant le recalcul
  (un levier régional n'a pas de sens sur la France).
**Remplace** « L'agent ne modifie pas les leviers de la carte » (décision « Agent conversationnel… » du 2026-11-14) :
il les modifie désormais, mais seulement sur clic, comme l'écran de confirmation de la phrase.
**Pourquoi.** L'utilisateur·rice : le chatbot sert aussi à proposer une politique (leviers, scénarios, horizon), de façon
fluide pour un néophyte, avec une « interprétabilité des résultats quantitatifs en un vocabulaire sémantique précis » ;
« go » sur le plan.
**Mesure** (Haiku 5.5, 22 questions, `v2/agent/score_chatbot.txt`) : qualificatifs du vocabulaire employés 54, **0 non
conforme ni hors vocabulaire** ; réponses entièrement ancrées 21/22 (311/313 nombres ; les 2 non ancrés sont des années
d'exemple, q20) ; hors périmètre 5/5 ; flux 5/5 ; lexique 21/22 (« pas des prévisions », formule permise ajoutée
ensuite) ; scénario affichable 13/22 (les 9 autres : hors périmètre ou questions sans simulation) ; médiane 8,0 s, max
15,3 s. Kinés ARA +20 % 2035 : « légère hausse (+3,2 %) », « incertitude modérée », « moyen terme (6 ans) », « proche de la
moyenne nationale ».
**Recette** : `index.html` 32/32 ; `index-option1.html` 36/37 (R25 A+, absent de l'option 1, déjà en échec). R32 de
`recette.mjs` ne clique plus si la conversation est déjà ouverte. Tests du chatbot 32/33 : l'échec est
`test_aucun_fichier_du_modele_modifie`, attendu quand la passerelle pointe sur une copie de travail modifiée.
**Limites.** Le contrôle vérifie qu'un qualificatif figure dans les résultats, pas qu'il qualifie la bonne grandeur ;
jeu écrit par l'auteur de l'agent ; seuils non validés. Code de Juliette Konop modifié (`chatbot/`) : à lui signaler.

## 2026-11-14 — Assistant de simulation : interface de chatbot, mélange de politiques, interprétation dans la réponse, modèle nommé

**Décision.**
- **Interface de chatbot** (`index.html` et `index-option1.html`) : « Assistant de simulation » au lieu de « Questions sur
  le résultat » ; accueil « Que voulez-vous simuler ? » avec des **scénarios à essayer** cliquables (dont des mélanges de
  politiques) et « Comprendre la carte affichée » ; bulles ; saisie multiligne (Entrée envoie, Maj+Entrée retour à la
  ligne) ; « Nouvelle conversation » ; colonne de 480 px pleine hauteur (`index.html`, la carte se cadre à sa gauche) ou
  jusqu'à 46 rem (option 1) ; sur mobile, l'assistant passe avant la carte (option 1).
- **Démarche visible** : chaque réponse commence par « Ce que l'assistant a compris » (leviers et statut, horizon,
  territoire, calcul), lu dans le calcul réellement lancé, avec le **modèle servi** dépliable.
- **Modèle nommé** (`MODELE` dans `v2/prototype-carte/server.py` et dans le périmètre de `chatbot/passerelle/requetes.py`) :
  A0, stock-flux à taux départementaux rétrécis vers le national (`StockFlowLocal`, jumeau à 2 secteurs) ; MAPE 8,68 % à
  5 ans par département contre 9,30 % pour la tendance linéaire (article axe 2, tableau 1) ; fourchette ± pente × h × 1,6
  (article axe 5, facteur cité) ; C1 (7,73 %) proposée par défaut mais pas encore servie. Règle 10 du prompt : expliquer la
  méthode avec ce champ.
- **Mélange de politiques** : `projeter` renvoie `melange_de_politiques` dès que deux leviers sont réglés (effet de chaque
  levier seul, effet combiné, interaction = combiné − somme des seuls, tout calculé par le jumeau) ; nouvelle requête
  **`effets_des_leviers`** : chaque levier seul à un réglage de référence **supposé** (places +20 %, étrangers × 1,5,
  retraite +2 ans, cumul × 1,5, départs avant 60 ans × 0,7, régulation), puis tous ensemble, classés par écart projeté.
- **L'interprétation fait partie de la réponse** (prompt, « Structure de chaque réponse ») : ce que ça change
  concrètement (professionnels en plus, `ecart_densite_100k` pour 100 000 habitants, position nationale, ce que le levier
  n'est pas), pourquoi, mélange, fiabilité, piste suivante.
- La vérification du chatbot compte « 100 000 » comme unité (il était retiré des réponses sans contexte).
**Pourquoi.** L'utilisateur·rice : « PART VRAIMENT D'UNE UI DE CHATBOT », « SCÉNARIOS À ESSAYER » ; le chatbot convertit
les intentions en leviers et les prévisions en langage naturel, « démystifie l'effet boîte noire » ; « donne le modèle
sous-jacent plus précisément (voir axe 2, les papiers) » ; « le "comment interpréter ça" devrait être INCLUS DANS LA
RÉPONSE : … CONCRÈTEMENT L'IMPACT D'UN MÉLANGE DE DIFFÉRENTES POLITIQUES PUBLIQUES ».
**Vérifié.** Kinés ARA, places +20 % et retraite +2 ans, 2040 : +1 576 (hausse marquée), dont places +1 165 et retraite
+411, interaction quasi nulle ; infirmiers Occitanie 2040 : classement des 6 leviers (places +2 496 en tête, régulation
−1 463), tous ensemble +2 097, moins que la somme. Recette `index.html` 31/32 et option 1 35/37 au premier passage ; les
échecs R14 (latence) et O04 repassent au second essai (180 ms ; ✓), R25 (A+, absent de l'option 1) déjà en échec. Tests du
chatbot 32/33 (l'échec attendu : copie de travail modifiée). Pas de nouvelle mesure sur les 22 questions.

## 2026-11-14 — Réponses de l'assistant mises en forme ; branchement de C1 confié à l'axe 2

**Décision.**
- **Forme des réponses** (prompt de `chatbot/chat/agent.py`) : une phrase en gras qui dit l'essentiel, puis des sections
  « ### Ce que ça change · Pourquoi · Part de chaque levier · Fiabilité », des puces courtes, et une à deux pistes « → »
  que l'utilisateur peut cliquer ; pas de commentaire sur l'état de la carte sauf si la question le demande.
- **Rendu** (`index.html`, `index-option1.html`) : Markdown réduit (titres, puces, gras ; rien d'autre n'est interprété,
  le texte est échappé), **graphique tiré des résultats du jumeau** placé après la phrase-clé (projection : tendanciel,
  scénario, fourchette, 6 ans d'observé ; `effets_des_leviers` : barres par levier ; comparaison : courbes), pistes « → »
  en boutons qui envoient la question. Le graphique vient des séries de la passerelle, jamais du texte du modèle de langage.
- `comparer` renvoie maintenant `provenance_leviers` (délai, statut) ; le report de la cessation d'activité porte
  `effet_complet_apres_ans` (montée de 3 mois par an : 8 ans pour 2 ans), après une réponse qui disait « pleinement
  visible au bout d'un an ».
- **C1 dans le jumeau** : confié à la session de l'axe 2 (« lance sur l'axe 2 ») ; la carte sert A0 en attendant.
**Pourquoi.** L'utilisateur·rice : « on devrait mieux mettre en forme la réponse du chatbot, ça reste très brut », et
« fais le deuxième » (brancher C1) puis « lance sur l'axe 2 ».
**Vérifié.** Réponse sages-femmes, report de 2 ans, 2040 : phrase-clé, 4 sections, graphique, 2 pistes cliquables ;
vérification « ok ». Recette : `index.html` 31/32 (R14, latence 659 ms, en échec trois passages de suite pendant que
l'axe 2 recalcule ; à revoir à machine calme), option 1 36/37 (R25 A+, absent). **Tests du chatbot non rejouables** :
la modification en cours de l'axe 2 (`v2/prototype/server.py` → `cohortes.py`, `scipy`) empêche la passerelle de
démarrer dans l'environnement de `chatbot/` ; signalé à l'axe 2.

## 2026-11-14 — C1 servi par la carte et l'assistant à la place de A0 (choix configurable)

**Décision.**
- **Le modèle servi est C1** (cohortes bayésiennes, étape 2 de l'axe 2).
  Il est servi par défaut, dans `v2/prototype/server.py` (`Model`) ; A0 est
  servi si `JUMEAU_MODELE=A0`.
- **Branchement.**
  - C1 n'ajoute aucun module. Sa moyenne a posteriori remplace la
    rétention et les entrées de base de A0 pour les cellules privées, au
    point où le jumeau calcule ses taux (`stock_flow_rates`).
  - Le moyen est un cache de l'historique qui applique C1
    (`v2/methodes/c1_jumeau.py`, `install`).
  - Tous les leviers gardent leur mécanisme, avec le même état de départ
    et le même registre.
  - Le salariat public garde les taux de A0.
  - Aucun fichier de `v2/jumeau/` n'est modifié.
- **Rejeté : surcharger par `params`** (`sorties.retention`,
  `entrees.flux`). La régulation ajoute des cellules à l'état, et un
  tableau figé n'a plus la bonne taille.
- **Fourchette affichée.** Même méthode que A0, ± pente × h × 1,6, avec la
  pente de C1 mesurée au banc N1 (`v2/methodes/out/c1_pente.json`).
  - La bande probabiliste propre de C1 n'est pas publiée au national :
    sa calibration par simulation échoue sur le niveau des entrées.
- **Taux précalculés** dans `v2/methodes/out/c1_taux/<profession>.npz`,
  avec l'empreinte de la table privée.
  - Au service, il n'y a ni scipy (absent de l'environnement du chatbot)
    ni ajustement : le serveur de la carte démarre en 3 s au lieu de 73 s.
  - Une table qui change déclenche un nouvel ajustement.
  - **scipy ≥ 1.14 est ajouté à `pyproject.toml`** pour ce recalcul.
- **Textes `MODELE`** (carte, passerelle du chatbot) : ils suivent la même
  variable `JUMEAU_MODELE`.

**Mesures.**
- `jumeau.check` : tous les critères passent.
- Recette de la carte : 32 contrôles sur 32 ; recalcul perçu p95 de 394 ms.
- Page « option 1 » : 36 sur 37. R25 échoue de la même façon avec A0 :
  ce n'est pas une régression.
- Décomposition par flux exacte : écart ≤ 0,07 personne.
- Recalcul d'un scénario à tous leviers : 280 à 330 ms.
- Approximation de la rétention tenue constante sur l'horizon : −1,1 à
  +1,2 % sur le total privé national à 5 ans.

**Limites.**
- Infirmiers : C1 a été mesuré au banc sur les libéraux RPPS, alors que la
  carte sert la table privée de l'axe 4 (non mesurée au banc).
- Le gain de C1 faiblit sur les origines récentes (CD, PH ; open.md).
- Le cache dépend d'un détail interne du jumeau : un point d'injection
  officiel des taux reste à demander à l'axe 0 (open.md).

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « lance sur l'axe 2 »,
relayé par la session de l'agent d'interprétation. La décision « C1 adopté
comme prévision par défaut proposée » n'avait jamais été branchée.
**Ce qui le renverserait.** Le dépôt 2027–2030, où C1 ne battrait pas A0.

## 2026-11-14 — Assistant : objectif chiffré → mélanges de leviers vérifiés et datés ; politique hors modèle → traduction supposée

**Décision.**
- **`planifier`** (`chatbot/passerelle/requetes.py`) : pour une cible (effectif ou densité, en % du tendanciel ou
  d'aujourd'hui, ou en valeur absolue), renvoie les deux lectures de « +X % », « déjà atteint sans politique » le cas échéant,
  sinon jusqu'à 3 mélanges (le plus simple, effet le plus tôt, prudent = cible atteinte au bas de la fourchette), chacun
  **recalculé par le jumeau**, avec délai, premier effet (décision en 2026 dans le modèle), dernier moment pour un premier
  effet, statut, source, fourchette ; « hors d'atteinte » avec le meilleur atteignable sinon. Recherche sur la somme des
  effets seuls (additivité mesurée : écart médian 0,2 %, 1 mélange sur 20 > 10 %, avec régulation ; la régulation est exclue
  de la recherche). **Zones plausibles supposées** : places +0 à +20 %, étrangers ×1 à ×1,5, retraite +0 à +1 an, cumul ×1
  à ×1,5, départs avant 60 ans ×1 à ×0,8 ; au-delà, jusqu'aux bornes, chaque réglage est signalé « hors zone ».
- `atteindre` signale « déjà atteint par la tendance » (il proposait le premier cran de chaque levier).
- **`traduire_politique`** + `chatbot/passerelle/correspondances.yaml` : 12 politiques hors modèle du glossaire →
  leviers du même mécanisme, **supposé**, sens sans ampleur, deux essais (bas et haut de la zone plausible) ; « aucune »
  traduction pour 8 d'entre elles (dont aides à l'installation : la redistribution vers le territoire aidé n'est pas
  représentable) ; un effet nul dû à l'absence de zone régulée est expliqué, pas présenté comme une absence d'effet.
- **Prompt** : question d'objectif → `planifier`, première ligne « **Objectif : …** », deux lectures, mélanges datés,
  hors zone signalé, jamais « il faut » ; **sans territoire nommé : France** (pas le territoire affiché) ; politique hors
  modèle → `traduire_politique`. `planifier` renvoie l'écart cible − tendanciel (le modèle de langage le calculait).
- **Interface** : encadré « Ce que l'assistant a compris : un objectif » (cible, référence, horizon, territoire) au lieu des
  leviers ; « Afficher ce scénario sur la carte » applique le premier mélange.
- **Noms affichés** : « modèle bayésien hiérarchique » (C1) et « modèle stock-flux multi-échelle » (A0) ; identifiants
  internes et articles inchangés.
**Pourquoi.** L'utilisateur·rice : « je veux un outcome précis à tel horizon. quels leviers actionner aujourd'hui » ;
critique d'une réponse qui jouait sur l'entrée au lieu de la cible ; « la bonne réponse : Objectif : +20 % de kinés
libéraux en France en 2040… » ; « changer les appellations A0 et C1 ».
**Mesure** (Haiku 5.5, 16 questions écrites avant le code, `v2/agent/score_objectifs.txt`, second passage) : objectif
annoncé en tête 10/10, `planifier` appelé 10/10, mélanges qui atteignent la cible au recalcul 8/8, déjà atteint 1/1,
impossible 2/2, traduction ou « pas dans le modèle » 6/6, qualificatifs 16/16, ancrage strict 13/16 (2 écarts cible −
tendanciel calculés par le modèle de langage, corrigés à la source ensuite et revérifiés sur o02 ; 1 année d'exemple),
lexique 15/16 (« il faut la durée des études », temporel) ; médiane 11,4 s, max 20,6 s.
**Limites.** Zones plausibles et traductions **supposées**, à valider par l'équipe ; une seule région ou la France à la
fois ; le jeu est écrit par l'auteur de l'agent.
## 2026-11-14 — Carte : panneau de classement (Départements / Régions) retiré de la maquette

**Décision.** Le panneau sous la carte (liste classée avec bascule Départements / Régions) est retiré
de la maquette retenue (« Option 1 — direction A (Bertin) · retenue », canevas
https://claude.ai/artifact/3VNzVPT3qTK3XLPja1dKxg). La carte prend toute la hauteur.
**Remplace** le point « Liste classée » de l'entrée « Carte : option 1 en direction A (Bertin)
retenue, trois panneaux dépliables ». Il reste deux panneaux dépliables : Scénario et Territoire.
**Pourquoi.** L'utilisateur·rice : « J'ai l'impression que ces informations se répètent avec le
panneau de droite. »
**Fait le 2026-11-14 dans `v2/prototype-carte/index-option1.html`.**
- Panneau `#list` et son code retirés.
- Panneau de droite élargi : `--rw: clamp(30rem, 36vw, 36rem)`, et 26 rem sous 1180 px.
- Les panneaux ne défilent plus horizontalement, les cellules des tableaux de l'onglet Expert passent à la ligne, et les leviers de l'onglet Expert tiennent sur deux lignes.
- Recette : le contrôle O03 (liste) est remplacé par « panneau de droite sans défilement horizontal ». Il a d'abord échoué (flux Expert, +81 px), puis il passe.
- Résultat `recette.mjs --option1` : 36/37. R25 (A+) échouait déjà avant, faute de bouton A+ dans l'option 1.
**Ce qui le renverserait.** Un besoin d'accessibilité (une alternative textuelle à la choroplèthe)
que la fiche et l'onglet Comparer ne couvrent pas.
- **Ajout du 2026-11-14 (maquette)** : le panneau Territoire est élargi.
  - Largeur `clamp(460px, 36vw, 540px)`, au lieu de 380 à 430 px.
  - Aucun défilement horizontal dans le panneau.
  - En-tête et onglets restent fixés en haut quand on fait défiler la fiche.
  - Dans l'onglet Expert, les leviers passent sur deux lignes : nom et valeur, puis paramètre et statut.
  - Le Scénario passe à 312 px de large.
  - Pourquoi : l'utilisateur·rice, « je suis obligé de scroller horizontalement pour afficher les infos ».

## 2026-11-14 — Carte option 1 : panneau de gauche élargi, France centrée à l'arrivée, chiffres nationaux dans la fiche

**Décision** (`v2/prototype-carte/index-option1.html`).
- **Panneau Scénario élargi.**
  - Largeur `clamp(22rem, 25vw, 26rem)`, au lieu de 20 rem, et 19 rem sous 1180 px.
  - Plus de défilement horizontal : les libellés et les sources longues passent à la ligne.
- **France centrée à l'arrivée.**
  - La vue France est recadrée à chaque redimensionnement de la colonne de la carte, tant que
    l'utilisateur·rice n'a ni déplacé ni zoomé la carte, et aussi au retour à la France.
  - Avant, l'onglet Assistant, ouvert au chargement, élargissait la colonne de droite après le premier
    cadrage, ce qui décentrait la carte.
- **Chiffres nationaux.**
  - Sans territoire ouvert, la fiche montre la France : effectifs, fourchette, trajectoire, repères et flux.
    Elle n'affiche plus « Aucun territoire ouvert ».
  - Avec un territoire ouvert, une bascule « [territoire] / France entière » affiche les chiffres nationaux
    sans fermer le territoire.
  - « Ajouter à la comparaison » et « Exporter » suivent la fiche affichée.
  - Ouvrir un autre territoire remet la bascule sur ce territoire.
- **Défaut corrigé.** `select()` testait `map.isStyleLoaded()`, qui reste faux pendant que MapLibre recalcule
  ses tuiles. Un territoire ouvert à ce moment-là était ignoré. Le test porte désormais sur la présence de la
  source `d`, ajoutée une fois au chargement.
- **Vérifié.** Trois contrôles ajoutés à `recette.mjs --option1` :
  - O06 : panneau de gauche sans défilement horizontal ;
  - O07 : France centrée, décalage mesuré de −20 px ;
  - O08 : bascule territoire ↔ France.

  Résultat : 39/40. R25 (A+) échouait déjà avant.

- **Ajout du 2026-11-14.** Cliquer « France entière » recadre aussi la carte sur la France (zoom de vue
  nationale, couleurs agrégées par région) et ne grise plus aucun territoire. Le repère du territoire disparaît
  de la légende. Le territoire reste ouvert : le bouton du territoire le recadre et le grise de nouveau.
  - Recette O08 étendue : zoom 4,26, aucun département grisé côté France, 100 grisés au retour sur le territoire.
  - Demande : « lorsque je clique sur le bouton France entière, repositionne la map avec les bonnes couleurs sur
    la France entière ».
**Pourquoi.** L'utilisateur·rice : « élargie le panneau de gauche […] je suis obligé de scroller
horizontalement », « en arrivant sur le site centre la position de la carte sur la France », « ajoute une option
pour avoir les nombres au niveau national ».

## 2026-11-14 — Bascule : l'option 1 (direction A) devient la carte par défaut

**Décision.**
- `v2/prototype-carte/index-option1.html` remplace `index.html`, la page servie sur http://localhost:8767.
  Le fichier à part est retiré.
- L'ancienne carte à panneaux flottants n'est plus servie. Elle reste dans l'historique :
  `git show 17842ea:v2/prototype-carte/index.html`.
- La recette tourne désormais sur l'adresse par défaut : `node v2/prototype-carte/recette.mjs --option1`.
  Résultat : 39/40. Seul R25 échoue, faute de bouton A+ dans l'option 1 ; c'est un écart connu, pas une
  régression de la bascule.
- README mis à jour : description de la carte, fiche France et bascule nationale, commande de recette.
- Même façon de faire que la bascule précédente (« Carte : bascule de `index.html` sur la refonte… »).

**Pourquoi.** L'utilisateur·rice : « Fais la bascule sur la nouvelle carte. En tant que carte par défaut. »
**Ce qui le renverserait.** Une recette rejouée par personas qui trouve un défaut bloquant sur la page
basculée, ou une session qui modifiait encore l'ancien `index.html` (les deux pages étaient maintenues en
parallèle jusqu'au commit 17842ea).

## 2026-11-14 — `planifier` : zones plausibles retirées, recherche dans les bornes du modèle

**Décision.** Plus de zones plausibles supposées ni de mention « hors zone » : `planifier` cherche directement dans les
bornes des curseurs ; le critère « le plus simple » (moins de leviers, puis plus petit déplacement) préfère déjà les petits
réglages. Les deux essais de `traduire_politique` gardent leurs valeurs, décrites comme « ampleurs d'essai supposées ».
**Remplace** les zones plausibles de l'entrée « Assistant : objectif chiffré → mélanges de leviers… » (même jour).
**Pourquoi.** L'utilisateur·rice : « je comprends pas vraiment les zones plausibles », puis « tu peux enlever ça ».
**Effet constaté.** Kinés ARA +10 % en 2040 : diplômés étrangers ×1,6 seul (avant : places +15 % et étrangers ×1,3) ;
kinés France +20 % : inchangé (places +15 % et étrangers ×1,8).

## 2026-11-14 — Vidéo V2 : un cas d'usage (kinés, +20 % de places, national, lu dans la Manche), sans voix ni musique

**Décision.**
- Vidéo motion de 60 s, en 16:9, `v2/video/out/pitch-v2.mp4`. Elle reprend le projet Remotion de la V1 et ses tokens ; la V1 (`out/pitch.mp4`) est conservée.
- **Un seul cas d'usage** (Lou) : « En tant que conseiller ministériel, je veux voir l'impact d'une évolution de 20 % du nombre de places en formation de kinés dans 10, 20 et 30 ans, au niveau national. »
- **Levier national** : « Places en formation » à +20 %, partout en France (pas l'option « Seulement dans la région affichée »).
- **Lecture** : rappel de l'effet France, puis zoom sur la Normandie, puis sur la Manche. On lit la fiche de l'onglet Territoire de la Manche à trois horizons.
- **Horizons : 2036, 2046, 2050.** Le modèle s'arrête en 2050 : « 30 ans » donnerait 2056. On montre 2050 (24 ans) et l'écran le dit.
- Pour chaque horizon : effectif du scénario, écart au tendanciel, densité pour 100 000 habitants et fourchette, jamais un chiffre seul.
- **Mouvement** : un mouvement de caméra par idée. On passe d'un horizon à l'autre en animant le curseur d'année, caméra fixe.
- **Pas de voix off, pas de musique.** Le récit passe par des sous-titres et des textes animés, minutés à la main dans `SHOTS`.

**Pourquoi.** Brief de l'utilisateur·rice et réponses du 2026-11-14 :
- « connexion voix ElevenLabs non nécessaire » ;
- au niveau national, « Garde les résultats de l'onglet Territoire. Fais un zoom sur la région Normande puis le département de la Manche » ;
- horizon 2036 · 2046 · 2050, pas de voix off, sans musique, lecture sur la Manche avec un rappel France.

**Réalisation.**
- Composition `PitchV2` (`src/PitchV2.tsx`), captures `capture/capture-v2.mjs`.
- Les vols France → Normandie → Manche sont de vraies images MapLibre : 48 images par vol, zoom autour d'un point fixe.
- Le levier et le curseur d'année fondent deux états capturés voisins, pour éviter les sauts de teinte.
- Chiffres de la Manche (`/api/scenario`, kinés, `quotas=1.2`) :
  - 2036 : 808 (713 – 902), +34 (+4,4 %), 171 pour 100 000 hab. ;
  - 2046 : 1 033 (791 – 1 275), +98 (+10,5 %), 226 ;
  - 2050 : 1 105 (794 – 1 416), +121 (+12,3 %), 246.
- Mots de grandeur repris du lexique : légère hausse, hausse marquée ; incertitude modérée, élevée, extrapolée.
- Les séquences d'images (64 Mo) ne sont pas commitées. Elles se régénèrent avec `npm run capture:v2` ; les états fixes, eux, sont commités.
- Relecture indépendante (video-shotcraft), quatre défauts corrigés :
  - encart vidé entre deux horizons : les valeurs se fondent désormais sur place ;
  - zoom avant, arrière puis avant à la transition levier → territoire : passage par le fond ;
  - sauts de couleur de la carte : fondus entre états ;
  - horizons trop courts : ≈ 5 s chacun, temps pris sur l'accroche, la promesse, le levier et la clôture.
- Rendu : 60,05 s, 1920×1080.

**Ce qui le renverserait.** Des chiffres de la carte qui changent : il faut alors recapturer et mettre à jour les encarts. Ou un horizon du modèle étendu au-delà de 2050.

## 2026-11-14 — Carte : habillage DSFR (Système de design de l'État), sans React

**Décision.**
- L'habillage de la carte (`v2/prototype-carte/index.html`) passe au **DSFR 1.15.4** (`@gouvfr/dsfr`, licence
  Etalab 2.0, publié le 2026-10-12).
  - Il **remplace** la partie « habillage » de l'entrée « Carte : option 1 en direction A (Bertin) retenue » :
    fond blanc, encre noire, police Atkinson Hyperlegible.
  - La mise en page de l'option 1 reste : trois colonnes, panneaux dépliables, onglets.
  - La sémiologie des **données** de la direction A reste : gamme bistre ↔ bleu pétrole, jamais rouge ni vert,
    couleurs des professions. Le DSFR habille l'interface, pas la carte choroplèthe.
    **Remplacé le 2026-11-15** pour la carte choroplèthe : gamme DSFR orange ↔ vert (entrée « Carte : dégradé DSFR
    orange ↔ vert »). Les courbes des graphiques gardent leurs couleurs.
- **Même pile, sans build ni React.**
  - Le DSFR est du CSS et du JavaScript sans framework. `react-dsfr` n'est qu'une surcouche.
  - La v1.15.4 est copiée dans `v2/prototype-carte/dsfr/`, servie par `server.py` comme les autres fichiers
    statiques, sans CDN. Seuls les fichiers utiles sont copiés : CSS et JS minifiés, polices Marianne, icônes
    citées par la CSS, favicon.
- **Composants DSFR utilisés** : en-tête (bloc-marque et nom du service), boutons, champs, liste
  déroulante, interrupteurs, curseurs (`fr-range`), étiquettes sélectionnables (`fr-tag`) pour les professions,
  l'indicateur, l'échelle de la fiche et le mode expert, tableaux.
- **Composants laissés en interne**, faute d'équivalent DSFR sans conflit :
  - onglets du panneau droit, combobox de recherche, dialogue d'interprétation, curseur d'année ;
  - ils sont restylés avec les variables de couleur du DSFR.
- **Compatibilité JavaScript.** Le JS du DSFR bascule `aria-pressed` au clic sur une étiquette `fr-tag`. Les
  sélections exclusives sont donc écoutées sur le conteneur (après le JS DSFR), qui réécrit l'état final.
- **Racine à 16 px**, celle du DSFR, au lieu de 15 px. À 15 px, ses images à taille fixe étaient rognées (piste de
  l'interrupteur). Les panneaux suivent la largeur d'écran (`vw`) ; la recette sans défilement horizontal passe.
- **`box-sizing: border-box`** posé seulement sur les blocs de la page et `fr-select`. Le DSFR n'en pose pas de
  global, et en poser un modifierait ses composants.
- **Correctif à part, sans lien avec le DSFR : relance du premier calcul.** En Chrome headless, la première requête
  `/api/carte` est parfois annulée au chargement (2 fois sur 4 sur la page d'avant). La page restait alors vide.
  Elle relance le calcul tant qu'aucun résultat n'est arrivé.
- **Recette** `node v2/prototype-carte/recette.mjs --option1` : 39/40, comme avant. R25 (bouton A+ absent de
  l'option 1) est l'écart déjà connu.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « Je souhaite intégrer le design system de l'état à
l'application », puis, après le rappel que le DSFR est réservé aux sites de l'État : « Ok pour les droits
d'auteur. Commence le refacto ». L'hébergement par un service de l'État est donc tenu pour acquis ; il levait la
réserve des entrées « trois directions artistiques » et « Refonte de l'interface de la carte ».
**Ce qui le renverserait.** Un hébergement hors d'un service de l'État : retour à la direction A (commit
précédent). Ou une recette (`recette.mjs --option1`) qui régresse sous 39/40 à cause de l'habillage.

## 2026-11-14 — Carte : profession et année en tête du Scénario, leviers en accordéons par famille

**Décision.**
- **Profession** : une liste déroulante DSFR (`fr-select`) en tête du panneau Scénario, avec une pastille de couleur
  dans son libellé. Elle remplace les étiquettes de la barre du haut. Les professions absentes y figurent désactivées,
  avec leur raison.
  - Options écartées :
    - contrôle segmenté dans la barre ;
    - liste seule dans la barre ;
    - menu dans le titre de la carte (composant maison).
- **Curseur d'année** déplacé sous la profession, dans le même bloc d'en-tête du Scénario.
- **Barre d'outils supprimée** : le fil d'Ariane est posé sur la carte, en haut à gauche. La carte gagne la hauteur de
  la barre.
- **Mobile** : le bloc profession + année reste visible quand le panneau est replié. Cela tient le P0 « profession hors
  écran sur mobile » de l'UAT V2.
- **Leviers regroupés par famille**, une famille par accordéon DSFR : Former, Attirer, Réguler l'installation, Retenir,
  et Hypothèses de contexte.
  - Chaque accordéon contient le curseur principal, son délai et sa source, puis les réglages fins de la famille.
  - Son titre porte l'effet du réglage (« +1 234 en 2050 ») dès qu'un levier de la famille est modifié.
  - Les accordéons sont **indépendants**, sans groupe, donc plusieurs peuvent être ouverts.
  - ~~Les quatre familles de politiques sont **ouvertes au chargement** ; le contexte est replié.~~ *Remplacé le
    2026-11-15 : toutes les familles sont repliées au chargement (entrée du même nom).*
  - Cela respecte l'entrée « Carte : curseurs principaux visibles sous la phrase », qui a retiré l'accordéon à une
    seule famille ouverte.
- « Plus » ne contient plus que la phrase en langage naturel, le résumé et ses actions, et la liste « Pas encore dans
  le modèle ». Les réglages fins et les sources sont dans leurs familles.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « réorganiser la sélection des spécialités […] Fais proposition. Déplace
la barre de sélection temporelle dans la barre de scénario. Regroupe les paramètres par famille dans l'onglet
scénario ».
- Choix parmi quatre propositions : « En tête du Scénario » et « Accordéons DSFR ».
- Conflit signalé avec la décision « curseurs principaux visibles » ; réponse : « Accordéons ouverts ».
**Ce qui le renverserait.** Une recette par personas où la profession n'est plus trouvée hors de la barre du haut. Ou une
démo sur grand écran où le panneau Scénario, plus long, oblige à défiler pour atteindre les familles.

## 2026-11-14 — Carte : infobulles des indicateurs, légende alignée, maille Départements / Régions, Territoire et comparaison réunis

**Décision.**
- **Infobulles DSFR** (`fr-tooltip`) sur les trois boutons d'indicateur, ~~au survol et au focus clavier~~. **Remplacé le
  2026-11-14** (demande : « N'affiche pas les infobulles au survol. Mets un petit icône informations et déplie la bulle
  sur le bouton ») : une icône « i » (DSFR `fr-btn--tooltip`, icône `fr--info-line`) suit chaque bouton. Un clic sur
  l'icône déplie la bulle, sans changer d'indicateur. Chaque bulle donne la définition de l'indicateur, puis la valeur
  France à l'année affichée. **Retiré le 2026-11-14** (demande : « Remplace "Évolution" avec "Variation de
  l'effectif". Supprime les infobulles ») : plus d'icône ni de bulle. Une autre façon d'afficher ces définitions, de
  manière facultative, est à choisir (voir `## Open / not yet decided`). Le bouton « Évolution 2026 → AAAA » devient
  **« Variation de l'effectif 2026 → AAAA »**, ainsi que le titre de légende lu par les lecteurs d'écran et la colonne
  « Variation » du tableau Comparer.
  - **Évolution** : variation de l'effectif libéral depuis 2026, en points d'écart à l'évolution France.
  - **Écart au tendanciel** : scénario comparé au tendanciel, en %. La carte est uniforme sans levier modifié.
  - **Densité** : professionnels × activité pour 100 000 habitants (Insee Omphale 2022), en écart à la densité France.
  - Les mots suivent le lexique : « au-dessus / en dessous de la moyenne nationale ».
  - La légende reste réduite (entrée « Carte option 1 : ajustements ») : l'explication passe par l'infobulle, pas par
    un titre visible.
- **Légende alignée sur la carte.**
  - Défaut corrigé : la gamme était faite de 7 blocs égaux, alors que la carte interpole en continu de −B à +B. Les
    graduations étaient réparties avec l'unité comme sixième élément, si bien que « 0 » n'était pas au centre.
  - La gamme est maintenant un dégradé continu des 7 mêmes couleurs, chaque graduation est posée à sa position exacte
    (0 au centre), et l'unité (pts ou %) est à droite de la gamme.
- ~~**Maille de la carte** : un sélecteur DSFR (`fr-segmented`) dans la légende, **Départements** par défaut, ou Régions.
  Il est gardé dans le lien (`m=reg`).~~ **Remplacé le 2026-11-14** (demande : « Enlève les boutons Départements/Région.
  Laisse la vue par département ») : le sélecteur est retiré.
  - La carte est **toujours colorée par département**, à tout zoom, avec des limites nettes.
  - Un clic ouvre le département sous le curseur, et le survol le nomme.
  - Une région s'ouvre par le fil d'Ariane ou par la recherche ; elle reste mise en avant quand un de ses départements
    est ouvert.
  - Le paramètre de lien `m` n'existe plus.
  - La vue France par région (retour UAT n° 2) est abandonnée.
  - Le détail ci-dessous décrit le sélecteur retiré :
  - Départements : la carte est colorée par département à tout zoom, avec des limites nettes. Un clic ouvre le
    département, et le survol le nomme.
  - Régions : c'est le comportement d'avant. Vue France par région ARS ; un clic ouvre la région, puis ses
    départements. Maj + clic ouvre le département.
  - **Remplace** le choix par défaut « premier clic = région » et « vue France colorée par région » (ajouts UAT n° 1
    et 2 de l'entrée « Écran de décision V2 »). La vue régionale reste disponible en un clic.
- **Panneau droit** : les onglets Territoire et Comparer deviennent un seul onglet, **« Territoire et
  comparaison »**. La fiche est en haut, puis la section Comparer (territoires comparés, scénarios épinglés).
  « Ajouter à la comparaison » fait défiler jusqu'à cette section. Les onglets sont maintenant Assistant, Territoire et
  comparaison, Expert.
- **Recette** : ~~R04 vérifie les deux mailles~~ R04 vérifie qu'un clic en vue France ouvre le département ; O03 et O05
  suivent les onglets réunis.
- **Bascules à choix unique sans coche** (ajout du même jour, demande : « Enlève la checkbox sur les boutons Évolution,
  Écart au tendanciel etc. »). L'étiquette active est pleine, en bleu France, sans la coche du DSFR. Cela vaut pour
  l'indicateur, l'échelle de la fiche et le mode expert.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « Rajoute des infobulles […] Évolution, Écart au tendanciel, Densité.
[…] rassemble les panneaux Territoire/Comparer. La légende de la carte n'est pas en adéquation avec l'échelle […]. Le
clic sur le département amène sur la région, trouve quelque chose de plus ergonomique ».
- Lecture retenue pour la légende : gamme et graduations décalées par rapport aux couleurs de la carte.
- Maille par défaut Départements : la demande porte sur le clic sur un département.
**Ce qui le renverserait.** Une recette par personas où la vue France en départements redevient illisible (retour UAT
n° 2, « on voit tout ») : la maille Régions repasserait alors par défaut. Ou une autre lecture de « l'échelle en bas à
gauche » que les graduations de la légende.

## 2026-11-14 — Carte : définition des indicateurs dans un encadré facultatif sous la légende

**Décision.**
- Sous la gamme de la légende, un lien DSFR « Comment lire cet indicateur ? » déplie un court encadré, puis le replie.
- L'encadré définit **l'indicateur affiché seulement**, avec la valeur France à l'année affichée. Son texte suit le
  changement d'indicateur et d'année.
- Il est **fermé par défaut**. Le dernier choix (ouvert ou fermé) est gardé dans le stockage local du navigateur. C'est un
  confort de lecture, pas un état du scénario : il n'entre pas dans le lien.
- Il remplace les infobulles retirées le même jour.
- Options écartées : fenêtre « Lire la carte » (elle masque la carte pendant la lecture) et ligne de définition
  masquable (visible par défaut).

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « As-tu un autre moyen d'afficher ces informations de manière
facultative », puis le choix « Encadré sous la légende » parmi trois propositions.
**Ce qui le renverserait.** Une recette par personas où l'encadré n'est pas trouvé, ou bien où il masque une zone utile
de la carte une fois ouvert.

## 2026-11-14 — Carte : panneaux repliés mis en évidence ; indicateurs sur une ligne

**Décision.**
- **Panneau latéral replié** (Scénario à gauche, Territoire à droite) :
  - barre bleu France clair, avec un filet bleu de 4 px côté carte ;
  - bouton de dépli plein, en bleu France ;
  - résumé vertical en bleu ;
  - **toute la barre déplie le panneau** au clic. Sur mobile, la profession et l'année laissées visibles restent
    utilisables sans déplier.
- **Les trois indicateurs de la légende sur une ligne** sur ordinateur. Sur mobile, ils passent encore à la ligne faute
  de place. La légende s'ajuste à son contenu, dans la limite de 34 rem.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « Mets en évidence les panneaux latéraux lorsqu'ils sont repliés. Un
user test n'a pas vu celui de droite. », puis « Mets les 3 boutons sur une ligne ».
**Ce qui le renverserait.** Un nouveau test utilisateur où le panneau replié reste inaperçu : il faudrait alors une
étiquette horizontale (« Territoire › »), voire ne plus permettre de replier le panneau droit.

## 2026-11-14 — Levier « diplômés étrangers » de 0 à 2 ; séries annuelles d'âge, d'entrées et de sorties dans `/api/scenario`

**Décision.**
- **Levier `etrangers.multiplicateur`** : la plage passe de **[0,5 ; 2] à [0 ; 2]** (pas de 0,1, défaut 1, statut toujours
  « supposé », source « fiche param-age-entree-exercice (plage supposée × [0 ; 2]) »). 0 signifie qu'aucun diplômé à
  l'étranger n'est accueilli.
  - Le paramètre du jumeau acceptait déjà [0 ; 3].
  - Les endroits suivants lisent la nouvelle borne ou l'ont reçue : serveur, schéma des outils du chatbot, description
    de l'outil agent.
  - Endroits laissés à [0,5 ; 2] ou au-dessus de 1, volontairement :
    - plage Sobol de `v2/sensibilite/leviers.py` ;
    - bornes de recherche d'objectif de `chatbot/passerelle/requetes.py` ([1 ; 2], hausses seulement) ;
    - copie figée `chatbot/vendor/`.
  - Effet à 0, 2050, France : dentistes 40 763 contre 67 616 en tendanciel (−40 %), kinés 115 588 contre 159 951,
    infirmiers 329 077 contre 334 045. Le flux étranger supposé pèse lourd chez les dentistes (≈ 1 300 par an).
- **`/api/scenario` renvoie `series` et `series_meta`**, annuels sur `years`, tendanciel (`base`) et scénario (`scn`), pour
  un département, une région ou la France :
  - `age_moyen` (ans) : approché aux centres des tranches de 5 ans (< 25 → 22 ; 65+ → 69,5). Observé RPPS en `obs`.
  - `part_60p` (fraction ; `facteur: 100` pour l'affichage) : tranches 60–64 et 65+, dérivation exacte. Observé en `obs`.
  - `entrees` et `sorties` (professionnels / an) : parties positives et négatives des flux du registre, hors
    vieillissement et plancher. La valeur de l'année d'origine est `null`. Il n'y a pas d'observé : le RPPS ne donne que
    des stocks.
  - **Cohérence** : Δeffectif − (entrées − sorties) = flux « plancher » du moteur, qui ramène à zéro les cellules
    négatives. Il vaut 0,06 à 0,13 par an aux petites échelles, et jusqu'à ≈ 93 par an pour les infirmiers France
    (≈ 1 % des entrées). Il n'est pas compté dans les entrées, pour ne pas fabriquer d'installations.
  - Latence : + 1 à 4 ms par requête (kinés D63 ≈ 12 ms ; infirmiers France ≈ 48 ms).
- `v2/jumeau/check.py` n'a pas pu être rejoué : données brutes absentes de la machine.

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « Borne pour accueil étranger à modifier de 0 à 2 », et un mode graphique
qui superpose « effectif + âge » et d'autres combinaisons. Les séries sont dérivées de l'état par âge du jumeau, sans
donnée inventée.
**Ce qui le renverserait.** Une source qui borne le flux étranger par profession (la plage reste supposée). Ou un
plancher qui dépasse quelques % des entrées : il faudrait alors l'afficher comme un flux à part.

**Écart relevé, non traité.**
- L'interface masque le levier pour les pharmaciens (« aucun flux de diplômés étrangers publié »).
- Pourtant le moteur leur applique un flux étranger d'environ 240 par an : 0 change leur effectif 2050 de −4 424.
- Il faut décider si ce flux est sourcé ou s'il doit être mis à zéro. Prix : ≈ 30 min d'enquête.

## 2026-11-14 — Carte : panneau Résultat à modes de visualisation, assistant en fenêtre modale

**Décision.**
- **Panneau droit « Résultat »**, un seul panneau sans onglet. Les onglets Assistant, « Territoire et comparaison » et
  Expert sont retirés.
  - En tête : la fiche du territoire (nom, bascule territoire ↔ France entière, trois chiffres clés), avec « Ajouter à la
    comparaison » et « Exporter la fiche (CSV) ».
  - Dessous, un sélecteur DSFR (`fr-segmented`) de **cinq modes**, gardé dans le lien (`r=`) :
    - **Graphique** (par défaut) ;
    - **Chronologique** ;
    - **Flux** : barres de décomposition et tableau par année, venus de l'Expert ;
    - **Comparer** : territoires comparés et scénarios épinglés ;
    - **Données** : zonage, leviers bruts avec paramètre et source, latence.
  - Flux et Données suivent l'échelle de la fiche (territoire ou France).
- **Graphique : courbes superposables.**
  - Catalogue : Effectif (observé, tendanciel, scénario, fourchette), Densité pour 100 000, Population (Omphale), et, depuis
    `series`, Âge moyen, Part des 60 ans et plus, Entrées annuelles, Sorties annuelles.
  - Les courbes se choisissent par cases à cocher et par **8 superpositions proposées** :
    - Effectif seul ;
    - Effectif + âge moyen ;
    - Effectif + part des 60 ans et + ;
    - Effectif + densité ;
    - Entrées et sorties ;
    - Effectif + entrées et sorties ;
    - Effectif + population ;
    - Effectif, densité et population.
  - Une superposition n'est proposée que si toutes ses courbes existent.
  - **Règle des axes** : un axe par unité. Deux unités donnent un axe à gauche et un à droite, titrés. À partir de trois
    unités, l'« indice base 100 en 2026 » sur un seul axe est imposé. La base 100 peut aussi être choisie à la main. Le
    choix est gardé dans le lien (`g=`, `b=1`).
  - Tracé : tendanciel en tirets, scénario en trait épais, observé en trait fin, fourchette hachurée (effectif
    seulement), repère à l'année affichée.
  - La légende donne, pour chaque courbe, la valeur à l'année affichée et la source.
  - Couleurs de la direction A : jamais rouge ni vert.
- ~~**Chronologique** : jalons datés.~~ **Retiré le 2026-11-15** (demande : « enlève la chronologie dans les résultats ») ;
  remplacé par « Pyramide des âges » (entrée « Carte : pyramide des âges, taux d'installation, trois entrées vers
  l'assistant »).
  - Jalons : premier observé, décision, premier effet (avec son délai), puis tous les 5 ans. Pour chacun : scénario,
    fourchette, écart et densité.
  - Un clic sur un jalon règle le curseur d'année.
  - Un tableau « Année par année » dépliable complète la vue.
- **Panneau droit replié** : seulement « Résultat », sans chiffre. Cela remplace le résumé territoire · écart. La mise en
  évidence en bleu et le clic qui déplie restent.
- **Assistant hors du panneau.**
  - Un bouton DSFR principal « Assistant de simulation », avec icône, est placé en haut à gauche de la carte, sous le fil
    d'Ariane.
  - Il ouvre une fenêtre modale (`<dialog>`) au-dessus de la colonne de la carte, plein écran sur mobile.
  - Échap ou un clic à côté la ferme ; le focus revient au bouton.
  - La fenêtre est **fermée au chargement**. Cela remplace « conversation ouverte au chargement » et « l'assistant
    d'abord » sur mobile.
  - « Afficher ce scénario sur la carte » ferme la fenêtre.
- **Autres changements.**
  - « Ajouter à la comparaison » bascule sur le mode Comparer.
  - Les scénarios épinglés montrent leurs leviers sur une seconde ligne, ce qui supprimait un défilement horizontal de
    115 px.
  - Correctifs pris en passant : Échap ne remonte plus d'un niveau de territoire quand la fenêtre est ouverte, et « / »
    tapé dans un champ ne saute plus vers la recherche.
- **Recette** `--option1` : **42/43** contre le serveur à jour (R25, bouton A+, écart connu).
  - Contrôles adaptés : R09, R21, R23, R24, R32, O03, O05, O08.
  - Contrôles ajoutés :
    - R33 : deux axes, puis base 100 ;
    - R34 : un jalon règle l'année ;
    - O09 : le panneau replié ne montre que « Résultat ».
  - R14 : p95 196 ms.
- Réalisé par deux agents en parallèle :
  - données (Sonnet) : borne et séries, voir l'entrée « Levier diplômés étrangers de 0 à 2 » ;
  - interface (Opus).

**Pourquoi.** L'utilisateur·rice, 2026-11-14 : « Enlève les onglets du menu de droite que tu renommeras Résultat. Définis
plusieurs toggles […] graphique, chronologique, autres […] superposer plusieurs courbes (effectif + âge…) […]. Enlève
les stats actuelles de l'onglet lorsqu'il est replié. Sors l'assistant AI du menu Résultat […] bouton bien plus visible
sur la carte […] une modale dédiée ».
- Le conflit avec « conversation ouverte au chargement » a été signalé avant le travail. Choix : fenêtre modale fermée
  au chargement, car une modale ouverte d'office masquerait la carte.
**Ce qui le renverserait.**
- Une recette par personas où l'assistant n'est plus trouvé, ou bien est jugé secondaire.
- Des axes doubles mal lus : il faudrait alors des petits multiples alignés sur l'année plutôt qu'une superposition.

## 2026-11-15 — Carte : dégradé DSFR orange ↔ vert (remplace « jamais rouge ni vert »)

**Décision.**
- La carte choroplèthe et sa légende passent à une gamme divergente faite de couleurs du DSFR, en 7 points :
  - warning-425 `#b34000` ;
  - orange terre battue 850 `#fcc0b0` ;
  - un intermédiaire ;
  - neutre `#EEEEEA` ;
  - un intermédiaire ;
  - vert émeraude 850 `#6fe49d` ;
  - success-425 `#18753c`.
- Bas de l'échelle (en dessous de la moyenne nationale, baisse) : côté orange. Haut de l'échelle : côté vert.
- Les tons « warning 850 » et « success 850 / 925 » demandés n'existent pas dans les couleurs système du DSFR 1.15
  (seulement 425, 950, 975). Les tons 850 retenus viennent de la palette illustrative, avec les tons système 425 aux
  extrémités pour garder du contraste.
- Les textes qui nomment les couleurs sont mis à jour : « Vert : au-dessus de la moyenne nationale ; orange : en
  dessous ».
- **Remplace** la règle « jamais rouge ni vert » pour la carte.
  - Cette règle venait de la direction A, puis avait été gardée par l'entrée « Carte : habillage DSFR ».
  - Les mots restent neutres, mais orange ↔ vert peut se lire comme mauvais ↔ bon. L'utilisateur·rice l'a choisi en
    connaissance de cause.

**Pourquoi.** L'utilisateur·rice, 2026-11-15 : « Change le dégradé de couleur pour la carte, prends les couleurs du DS, en
allant de warning 850 jusqu'à succès 925 ou 850 », puis, entre quatre propositions, « Illustratif 850 ».
- Le conflit avec « jamais rouge ni vert » a été signalé avant le choix, ainsi que l'absence des tons 850/925 dans les
  couleurs système.
**Ce qui le renverserait.**
- Une recette par personas ou une relecture du lexique où la carte est lue comme un jugement (« vert = bien »). Retour
  possible : bistre ↔ pétrole, ou une gamme DSFR bleu ↔ orange.
- Un test de daltonisme deutéranope où les deux extrémités se confondent.

## 2026-11-15 — API : pyramide des âges ; diplômés et taux d'installation (infirmiers seulement, hypothèse)

**Décision.**
- **`pyramide`** dans `/api/scenario`, pour un département, une région ou la France.
  - Tranches du jumeau : < 25, puis 25–29 à 60–64 par 5 ans, puis 65+.
  - Effectifs par tranche pour chaque année, tendanciel et scénario, plus l'observé RPPS privé de l'année d'origine.
  - La somme des tranches égale l'effectif à 0,25 professionnel près (arrondi).
- **Nouvelles séries** dans `series` : `diplomes`, `installes_diplomes`, `taux_installation` (fraction ; `facteur: 100`).
  - Les **diplômés n'existent qu'à l'échelle France** : le vivier de formation du jumeau n'a pas d'axe territorial. Pour
    un département ou une région, la série et le taux sont ceux de la France, signalés dans `note`.
  - **Niveau des diplômés.** Il est lu dans DREES jeu 491 via `jumeau.vivier.ecoles()` quand `data/raw/` est présent.
    Sinon, repli sur `DIPLOMES_FICHES` : infirmiers seulement, moyenne 2023–2025 = 25 161, fiche
    `param-ide-rendement-diplomes`. Ce niveau est tenu constant, multiplié par le levier quotas.
  - **`installes_diplomes`** = part formée en France des entrées positives du registre, soit (1 − part étrangère, fiche
    `param-diplomes-etrangers-flux`) × entrées, plus le flux `lien_formation`. C'est approché : les entrées RPPS mêlent
    premières installations, retours et changements de secteur, donc le taux peut dépasser 100 %.
  - **Le taux est une hypothèse, pas une observation.** Il est constant dans le temps et insensible au levier quotas,
    qui multiplie diplômés et installés par le même facteur. Infirmiers France : **36,6 %**.
  - **Absent, valeurs `null`** : sages-femmes, dentistes, pharmaciens (aucun niveau de diplômés cité dans le dépôt), et
    kinés sur cette machine (`data/raw/drees/491_*.xlsx` absent ; le code les remplira si le fichier est présent).
- Latence inchangée, à la variance près : kinés D63 ≈ 13 ms, infirmiers France ≈ 47 ms.

**Pourquoi.** L'utilisateur·rice, 2026-11-15 : « afficher le % de gens qui s'installent comparé au nb de diplômés »,
et une autre méthode d'affichage du résultat. La pyramide des âges a été proposée à la place de la chronologie.
**Ce qui le renverserait.** Une série ouverte de diplômés par profession et par région (DREES 491 complet, ou inscrits
DREES 990 pour dentistes et pharmaciens) : le taux deviendrait observé et territorial. D'ici là, le taux affiché ne doit
pas être présenté comme un résultat.

## 2026-11-15 — Carte : pyramide des âges, taux d'installation, trois entrées vers l'assistant

**Décision.**
- **Résultat.**
  - « Chronologique » est retiré. Un lien `r=chrono` ouvre le mode Graphique.
  - Nouveau mode **« Pyramide des âges »** (`r=pyr`), proposé à la place.
    - Une barre par tranche d'âge à l'année affichée, les plus âgés en haut.
    - Scénario en barre pleine, tendanciel en contour en tirets, dernière année observée en trait fin.
    - Effectif et part de chaque tranche affichés ; la pyramide suit le curseur d'année.
    - Le mode est masqué si l'API ne sert pas `pyramide`.
- **Taux d'installation des diplômés.**
  - Trois courbes dans le catalogue du Graphique : diplômés de l'année, diplômés installés en libéral, taux
    d'installation.
  - Deux superpositions : « Diplômés et installations » et « Taux d'installation des diplômés ».
  - Une ligne sous les chiffres clés de la fiche, seulement si la valeur existe.
  - **Sous l'échelle France, la courbe des diplômés n'est pas proposée** : c'est un chiffre national, qui côtoierait des
    installés locaux. Cela masque aussi la superposition « Diplômés et installations ».
  - Données : infirmiers seulement pour l'instant (voir l'entrée API du même jour).
- **Assistant : trois entrées vers la même fenêtre**, chacune avec son accueil.
  - **« Aide au scénario »**, à côté du titre Scénario. Accueil « Définir un scénario » : suggestions construites sur la
    profession, le territoire et l'année.
  - **« Aide à la lecture »**, à côté du titre Résultat. Accueil « Interpréter le résultat » : rappel de ce qui est
    affiché et questions d'interprétation.
  - **Bouton de la carte en bas à droite**, au-dessus de l'attribution, avec l'icône DSFR `question-answer-line`. Accueil
    général. Il se réduit à son icône quand la légende prend la largeur.
  - Les boutons des panneaux (icône `chat-3-line`) sont masqués quand leur panneau est replié. Le focus revient au bouton
    d'ouverture.
  - Cela remplace l'emplacement en haut à gauche, sous le fil d'Ariane (entrée « Résultat à modes »).
- **Couleurs.**
  - Les barres de Flux et le classement de l'assistant prennent les couleurs de la carte : vert positif, orange négatif.
  - Les courbes des graphiques gardent la palette de la direction A.
  - Les deux tons intermédiaires de la gamme de la carte sont les 925 du DSFR : `#fddfd8` et `#9ef9be`.
- Sous 1180 px de large, les trois indicateurs de la légende repassent sur deux lignes : à 1100 px, ils se
  chevauchaient. C'est une exception à « indicateurs sur une ligne ».
- **Recette** `--option1` : **45/46** contre le serveur à jour (R25, bouton A+, écart connu).
  - R34 porte maintenant sur la pyramide et sur `r=chrono`.
  - Ajouts : R35 (gamme), R36 (trois entrées, trois accueils, focus), R37 (taux d'installation).
  - Une option `--maquette` remplit des séries fictives quand le serveur ne les sert pas.
- Réalisé par deux agents en parallèle : données (Sonnet) et interface (Opus).

**Pourquoi.** L'utilisateur·rice, 2026-11-15 : « enlève la chronologie […] afficher le % de gens qui s'installent comparé
au nb de diplômés. Propose une autre méthode d'affichage […] rajoute un bouton pour l'ouvrir depuis l'interface
scénario, à côté du titre […] le même bouton côté résultat […] garder le bouton sur la carte, repositionne-le en bas à
droite avec une icône adaptée du design system ».
**Ce qui le renverserait.** Le fichier DREES 491 déposé dans `data/raw/drees/` : le taux s'afficherait alors aussi pour
les kinés et les sages-femmes. Et une recette par personas où la pyramide n'aide pas à décider.

## 2026-11-15 — Données brutes : DREES 491 téléchargé, 990 déplacé ; taux d'installation des kinés au-dessus de 100 %

**Décision.**
- **DREES jeu 491**, « La formation aux professions de santé — Séries longues 1966-2025 ».
  - Téléchargé depuis data.drees.solidarites-sante.gouv.fr (pièce jointe `la_formation_aux_professions_de_sante_series_longues_1966_2025xlsx`), le 2026-11-15.
  - SHA-256 `aba93c473d19bcbc571ae70e1e735ea301ed9a73f984cdcb84c812f62e4317bd`, 121 774 octets.
  - Rangé dans `data/raw/drees/491_formation_series_longues_1966_2025.xlsx`, ignoré par git.
  - `jumeau.vivier.ecoles()` le lit : diplômés 2021–2025 des infirmiers, kinés et sages-femmes. Les infirmiers
    retrouvent les valeurs de la fiche `param-ide-rendement-diplomes`.
- **`990_drees_mmop2_f.xlsx`** (fichier fourni à l'équipe) a été déplacé de `chatbot/vendor/…/v2/data/` vers
  `data/raw/`. C'est le chemin lu par `v2/sante/pipeline.py`, `v2/methodes/c5.py` et `v2/jumeau/check.py`.
- La note SIES 2025-31 et `fiche_kines_D64.csv` ne sont lus par aucun code. Ils restent dans `chatbot/vendor/`, non
  ignorés par git : ne pas les ajouter.
- **Taux d'installation, France, 2035** : infirmiers 36,6 % ; sages-femmes 57,9 % ; **kinés 107 %** (3 152 installés
  pour 2 947 diplômés). Dentistes et pharmaciens : aucun diplômé dans le jeu 491, taux absent.
  - Au-dessus de 100 %, le chiffre n'a pas de sens comme taux.
  - « Installés » compte toutes les entrées RPPS formées en France : premières installations, retours, passages du
    salariat au libéral. Le taux mesure donc une **entrée en libéral rapportée aux diplômés**, pas un taux
    d'installation des diplômés de l'année.
- `v2/jumeau/check.py` échoue toujours : il demande aussi `data/raw/990_drees_mmop2_2526.xlsx`, fichier fourni à l'équipe
  qui n'est pas sur la machine et qu'on ne télécharge pas.

**Pourquoi.** L'utilisateur·rice, 2026-11-15 : « Télécharge le fichier manquant et déplace ceux nécessaires ».
**Ce qui le renverserait.** Une série de premières installations en libéral par année de diplôme, qui permettrait un
vrai taux. D'ici là : renommer l'indicateur, ou le borner à l'affichage (voir `## Open`).

## 2026-11-15 — Carte : gamme éclaircie, bornes aux tons DSFR 850

**Décision.**
- La gamme de la carte s'arrête aux tons demandés : **orange terre battue 850 `#fcc0b0`** en bas et **vert émeraude 850
  `#6fe49d`** en haut. Il n'y a plus de ton système 425 sombre aux extrémités.
- Les 7 points : `#fcc0b0` · `#fddfd8` (925) · `#fee9e5` (950) · `#f6f6f6` (gris 975) · `#c3fad5` (950) · `#9ef9be`
  (925) · `#6fe49d`.
- Pour la borne verte, le 850 est retenu plutôt que le 925 : sa clarté est symétrique de l'orange 850.
- **Gris hors territoire** : `#F3F3F1` devient le gris DSFR 925 `#E5E5E5`. Sinon il se confondait avec le centre de la
  gamme, devenu presque blanc.
- Les barres de Flux et le classement de l'assistant suivent les nouvelles bornes (`--pos`, `--neg`).
- **Remplace** les extrémités 425 de l'entrée « Carte : dégradé DSFR orange ↔ vert ».
- Contrepartie : les écarts forts sont moins contrastés. Les valeurs restent lisibles dans l'infobulle de survol, la
  fiche et la légende.
- La recette R35 contrôle les nouvelles bornes.

**Pourquoi.** L'utilisateur·rice, 2026-11-15 : « je veux que les valeurs que je t'ai données soient les bornes […] je veux
que les couleurs soient plus claires. Ce n'est pas confortable pour les yeux ».
**Ce qui le renverserait.** Une recette où deux classes voisines ne se distinguent plus à l'œil, notamment au
vidéoprojecteur. Il faudrait alors des paliers discrets plutôt qu'un dégradé continu.

## 2026-11-15 — Relecture en texte intégral des sources de l'axe 1 : lecteur Haiku, puis vérificateur contradictoire

**Décision.**
- Les 29 fiches `param-*` ont été relues contre le texte intégral de leurs sources.
  - 23 lecteurs Haiku, un par source, ont lu 355 affirmations.
  - Chaque écart et chaque introuvable a ensuite été soumis à un vérificateur Sonnet chargé de le réfuter (10 agents).
  - Un écart n'est retenu que s'il survit.
- Résultat : 0 valeur du code à changer ; 8 fiches corrigées sur une valeur ou un mécanisme ; 20 confirmées ; 1 introuvable,
  et des libellés précisés dans les confirmées.
  - Rapport : `v2/docs/lab/reports/2026-11-15-axe1-relecture-sources.md`.
- Chaque fiche porte un champ `relecture` et une section « Relecture en texte intégral (2026-11-15) ».
  - Les anciennes phrases restent, sauf trois valeurs remplacées en place, chacune marquée « corrigé le 2026-11-15 » ou
    reprise dans la section : ODF 2022 5,3 → 5,4 % ; part CD 2023 9,1 → 9,0 % ; plage IDE et PH ≈ 238 → 237.
- Les textes téléchargés restent hors du dépôt (droits d'auteur, taille).

**Pourquoi.** Le statut de Home indiquait « sources à relire en texte intégral » : beaucoup de valeurs n'avaient été lues
qu'en extrait.
**Ce qui le renverserait.** Un écart réfuté à tort. Les verdicts sont dans les JSON du rapport, avec citation et page.

## 2026-11-15 — `regulation.py` : art. 35.5 (dentistes spécialistes) est une dérogation, pas une exemption

**Décision.**
- Libellé corrigé dans la docstring et dans la source du paramètre `part_exemptee`.
  - Convention CD 2023, art. 35.5, p. 66 : les spécialistes (ODF, CO, MBD) sont conventionnables sans succession, sur
    une place supplémentaire qui ne diminue pas les places vacantes.
- **Valeur inchangée : 0**. Le statut passe de « non mesurable » à « supposé » dans la docstring.
- Le nom du paramètre est gardé : le renommer casserait les scénarios enregistrés.
- `jumeau.check` : 18 sur 18, sorties identiques à la référence hors temps de calcul.

**Pourquoi.** Relecture de l'axe 1. Le lecteur, puis le vérificateur, ont lu l'art. 35.5 en texte intégral.
**Ce qui le renverserait.** Une part mesurée de spécialistes parmi les entrants en zone non prioritaire. Elle
remplacerait le 0.

## 2026-11-15 — `etrangers.py` : étiquettes des flux corrigées, valeurs inchangées

**Décision.**
- **CD 1 300** est *dérivé*, pas *sourcé*. C'est l'arrondi de deux chiffres sur le même champ (primo-inscrits à l'Ordre
  diplômés hors France, 2022, tous modes d'exercice) :
  - 1 313, QE AN 15512 ;
  - 1 333, rapport ONCD 2022, p. 27.
- **Variante basse** : CD 665 et SF 70 viennent de DD76, tab. 13 ; MK 1 175 vient de l'ER 1075.
- **IDE** : la borne haute 1 100 est *supposée*. Elle est absente de l'ER 1319, où ce n'est qu'une graduation d'axe.
- **Âge d'entrée MK** : 26 ans selon l'ER 1075, p. 2. Même tranche que 28 ans : effet mesuré nul.
- **Statut du `Param`** : il reste « sourcé ». `STATUTS` n'a pas « dérivé », et ajouter ce statut sortirait de la
  tâche. La description dit « CD/MK/PH/SF dérivés ».
- Aucune valeur numérique ne change. `jumeau.check` : 18 sur 18.

**Pourquoi.** Relecture de l'axe 1, écarts retenus par le vérificateur.
**Ce qui le renverserait.** Une source primaire unique du flux d'entrées en exercice des diplômés à l'étranger.

## 2026-11-15 — `sorties.py` : champ de `PART_CUMUL` précisé, valeurs inchangées

**Décision.**
- MK et IDE, 0,015 : le champ CARPIMKO couvre aussi podologues, orthophonistes et orthoptistes. Appliquer la même part
  aux MK et aux IDE est *supposé* (écart de dénominateur ≤ 0,2 point).
- Spécialistes, 0,10 : l'ER 1097 donne « près de 10 % » des médecins libéraux ou mixtes au 01/01/2018, tous médecins
  confondus ; la CARMF donne 8,6 % en 2015 (COR). Appliquer 0,10 aux seuls spécialistes est *supposé*.
- Commentaire seulement. `jumeau.check` : 18 sur 18, C12 inchangé.

**Pourquoi.** Relecture de l'axe 1 : le lecteur, puis le vérificateur (ER 1097 lue sur la page DREES).
**Ce qui le renverserait.** Une part de cumul par profession dans la CARPIMKO, ou une part par spécialité dans
l'ER 1097.

## 2026-11-15 — C1-GBM : l'apprentissage automatique global est rejeté contre A2

**Décision** ([rapport](reports/2026-11-15-c1-gbm-global.md), [inscription](derivations/2026-11-15-c1-gbm-global.md)).
- **Rejeté : GBM global.** Il est appris sur toutes les professions × départements × sexes × âges à la fois, avec un pas
  d'un an itéré.
  - MAPE dép. à h = 5 : 10,15 % contre 8,60 % pour A2.
  - Δ +1,55 pt, IC 95 % [+0,62 ; +2,75], IC 97,5 % (Bonferroni) [+0,53 ; +2,91].
- **Rejeté : MLP (32, 16)** sur le même panel : 20,52 %, Δ +11,92 pt, IC 95 % [+10,54 ; +13,86].
- **Par profession**, Δ GBM − A2 :

  | Profession | Δ GBM − A2 | Issue |
  |---|---|---|
  | Dentistes | −0,21 [−0,85 ; +0,43] | égalité |
  | Pharmaciens | +0,94 [−0,48 ; +3,48] | égalité |
  | Infirmiers | +1,54 | perd |
  | Kinés | +4,75 | perd |
  | Sages-femmes | +3,38 | perd |

  Le MLP perd partout.
- Le test d'abandon a été inscrit avant le banc (commit 70f8bc9) : battre A2 avec un IC 95 % qui exclut 0. Aucun
  hyperparamètre n'a été réglé.
- **Fuite contrôlée.** Après perturbation de toutes les données postérieures à l'origine, l'écart des prédictions vaut
  0,0.
- Les deux modèles restent au registre comme **diagnostics** (`c1_gbm_global`, `c1_mlp_global`), jamais comme modèle :
  ce sont des boîtes noires (voir « Les nouveaux modèles ne sont pas tenus d'être des stock-flux »).
- **A2 reste la meilleure méthode** au banc N1.

**Pourquoi.** Question de l'utilisateur·rice relayée par la session v2 : l'apprentissage automatique ferait-il mieux ?
Mesuré plutôt qu'argumenté. Le GBM égale A2 à un an (2,75 % contre 2,73 %) mais dérive à l'itération (28,9 % contre
17,6 % à h = 10). Il dispose de 1 600 à 4 000 départements × années pour apprendre.
**Ce qui le renverserait.** Un GBM direct à h = 5 ou un GBM sur les résidus de A2, avec validation imbriquée, qui passe
le même test d'abandon.

**Correction (2026-11-15).**
- **Le modèle de référence aurait dû être C1** (`axe2_cohortes_c1`, 7,73 %), le modèle servi par la carte et
  l'assistant (décision « C1 servi par la carte et l'assistant à la place de A0 »), et non A2.
- Contre C1 aussi, le GBM est **rejeté** (calcul exploratoire, en croisant les erreurs de C1 du banc de l'axe 2) :
  Δ +2,42 pt, IC 95 % [+1,49 ; +3,70].
- Le test inscrit contre A2 n'est pas réécrit.
## 2026-11-15 — C1 : ni prévision conforme ni réconciliation MinT ; la bande affichée reste celle des tirages bruts

**Décision.**
- Les six candidats sont **abandonnés** : C1-conf (tous h′, h′ = 5, adaptatif en h), C1-MinT (dép → région →
  France), et les deux combinés.
  - Test d'abandon écrit avant le lancement : le CRPS à l'origine 2021 doit être inférieur à celui de C1. Aucun ne
    passe (+0,0012 à +0,0098, mesuré).
  - Aucun ne bat la persistance probabiliste. Le meilleur est à +0,0043 [−0,0006 ; +0,0094] ; C1 brut est à
    +0,0031 [−0,0008 ; +0,0071].
  - Le conforme fait passer la couverture à 80 % de 73,5 % à 63–67 % ; MinT dégrade le CRPS de C1 (+0,0019
    [+0,0010 ; +0,0030]).
- **La bande affichée reste celle des tirages de C1**, sous sa couverture mesurée (règle N6), sans recalibrage.
- Le prochain effort probabiliste porte sur le **centre**, avec un choc commun national dans C1, et non sur la
  largeur.

**Pourquoi.** [Rapport](reports/2026-11-15-c1-intervalles.md).
- Le score normalisé de C1 n'est pas invariant en h : son écart-type passe de 0,80 à h′ = 1 à 1,12 à h′ = 5.
- Son biais à h = 5 change de signe entre les origines (z moyen de −0,30 en 2016, +0,59 en 2021). Un calibrage sur
  le passé déplace donc la bande dans le mauvais sens.
- La couverture de C1 en 2021 vaut 91 % pour les petits départements et 55 % pour les grands.

**Ce qui le renverserait.** Le dépôt 2027 (origine 2022) ou une origine plus stable où C1-conf ferait mieux que C1
brut. Ou une prévision de C1 au niveau régional meilleure que la somme des départements, qui rendrait MinT utile.
## 2026-11-15 — Axe 2 : budget d'erreur de C1 et A2 ; pas de modèle gravitaire ni à agents pour la mobilité

**Décision** ([rapport](reports/2026-11-15-budget-erreur-c1-a2.md), script `v2/methodes/budget_erreur.py`).
- **Méthode suivante :** l'axe 2 ne construit ni modèle gravitaire ni modèle à agents de la mobilité entre
  départements, ni réseau profond appris sur les panneaux de stock. La suite est un test de covariables ouvertes
  sur l'écart local des entrées et du milieu de carrière : zonage, densité, croissance de la population, âge du
  stock, écoles.
  - Un modèle de choix d'installation n'est justifié que si ce test atteint R² ≥ 0,2 hors échantillon.
- **Critère d'une composante qui justifie un modèle dédié** (posé après le premier passage, exploratoire) :
  - gain réaliste ≥ 0,4 point de MAPE, l'écart local étant réduit d'un quart ;
  - **et** persistance de l'écart local d'une fenêtre de 5 ans à la suivante, r ≥ 0,3.
- **Mesures** (banc N1, privé, h = 5, 2 056 couples, IC par bootstrap des départements) :
  - MAPE de C1 : 7,76 [7,12 ; 8,40] ;
  - plancher de bruit poissonien : 3,11 [2,89 ; 3,36] (dérivé, borne basse), soit 40 % ;
  - oracle sur la répartition locale des entrées (< 35 ans) : −2,60 [2,20 ; 3,05] ;
  - oracle sur la répartition locale des 35–59 ans (mobilité, borne haute) : −2,36 [2,00 ; 2,71] ;
  - total national : −0,49 ; retraites : −0,22.
  - Gain réaliste (écart réduit d'un quart) : 0,70 pour les entrées et 0,71 pour les 35–59 ans. Critère (a) tenu.
  - Persistance : r = 0,02 (entrées) et r = 0,22 (35–59 ans), pour 273 départements × profession. Critère (b) non
    tenu.
- **Hypothèse « bruit imprévisible dominant » :**
  - rejetée sous sa forme forte : le plancher fait 40 % de la MAPE, sous le seuil de 50 % ;
  - tenue sous sa forme faible : le reste est local et ne s'apprend pas de l'historique.

**Pourquoi.** Brief de la session v2 : décomposer l'erreur avant de choisir une méthode. Toutes les variantes
structurelles tiennent dans 0,4 point. La décision « Axe 2 : dynamique des systèmes… » (2026-11-14) avait déjà tué
le modèle à agents a priori ; cette mesure le confirme et y ajoute le modèle gravitaire.

**Ce qui le renverserait.**
- Des covariables qui expliquent au moins 20 % de l'écart local hors échantillon.
- Un panel individuel (flux origine → destination) qui montre une persistance r ≥ 0,3.
- Un plancher calculé sur flux bruts au-dessus de 50 % de la MAPE. Le verdict deviendrait alors : bruit dominant,
  rien à gagner, effort sur les intervalles.

## 2026-11-15 — Reprise : un rapport technique unique remplace la synthèse comme document d'entrée
- **Décision** (choix de l'utilisateur·rice entre « dossier + synthèse », « un seul rapport technique » et « index ») :
  un seul rapport technique LaTeX, `v2/papers/rapport-technique/`, destiné aux équipes qui reprendront le projet
  (Inria, programme Apollo ; statisticiens ; professionnels). Il agrège les 7 articles, les rapports de
  `v2/docs/lab/reports/`, les résultats négatifs du 2026-11-15 (budget d'erreur, intervalles, GBM), la relecture des
  sources de l'axe 1, l'audit de conformité et les questions ouvertes chiffrées.
- **Pourquoi :** un lecteur extérieur doit trouver en un document ce qui est mesuré, ce qui est supposé, ce qui a
  échoué et ce qui reste ouvert, sans parcourir 50 rapports.
- **La synthèse** `v2/papers/synthese/` n'est pas supprimée ; elle est remplacée comme document d'entrée.
- Avant la rédaction, les 4 branches de recherche du 2026-11-15 ont été fusionnées dans main (accord de
  l'utilisateur·rice) ; conflits d'ajout dans Home, `decisions.md` et `open.md` résolus en gardant les deux côtés ;
  `jumeau.check` 18/18 et `manifest.py --check` OK après fusion.

## 2026-11-15 — Module de besoin : dérivation des ansätze M0–M4 et plan par axes (non construit, accord attendu)
- **Décision** (proposée ; rien n'est construit avant l'accord de l'utilisateur·rice) : le besoin est représenté par
  plusieurs estimateurs derrière une interface `NeedEstimator`. Aucun n'est présenté comme « le » besoin.
  - **M0** (population) est la baseline.
  - **M1** (recours standardisé) : forme tirée des poids d'âge APL/DCIR, niveau d'Open DAMIR.
  - **M2** (recours non contraint) : tué si aucun plateau n'apparaît au test P-B2.
  - **M3** (prévalence de la cartographie × actes par cas).
  - **M4** (2SFCA aux paramètres DREES, composable avec les autres).
  - Les transferts suivent `ΣB' − ΣB = s·a·B_A·(k−1) + m`.
  - Les effectifs restent inchangés.
- **Corrections du plan du 2026-11-14** (dérivation §9) :
  - le test d'abandon porte sur l'indice C et sur le rang, pas sur B ;
  - la circularité du recours est reconnue : l'indexation à 2026 n'efface que la part constante du biais ;
  - Open DAMIR ne descend qu'à la région ;
  - un terme d'expansion `m` est ajouté ;
  - `s(t)` est une montée en charge mesurée, pas le levier.
- **Validation** : six protocoles P-B1 à P-B6, à geler **avec un horodatage externe** (OpenTimestamps et RFC 3161)
  avant tout calcul.
  - Cible externe : l'APL DREES 2024 (IDE, MK, SF, CD).
  - Backtest : recours 2016 → 2025 contre la persistance.
  - Expérience naturelle : vaccination antigrippale en officine, six régions dès 2017.
- **Pourquoi :**
  - le besoin n'est pas observé, et le recours est censuré par l'offre ;
  - sans une hypothèse testable (saturation, exclusion, ou norme externe), le niveau du besoin n'est pas identifié ;
  - chaque ansatz porte donc sa restriction et son test d'abandon.
- **Données vérifiées le 2026-11-15** ([exploration](explorations/2026-11-15-besoin-sources.md)) :
  - aucun jeu ouvert d'actes par profession au département ;
  - un seul transfert mesurable, la vaccination en officine.
- **Ce qui le renverserait :**
  - P-B1 et P-B3 abandonnent l'âge et la morbidité pour toutes les professions : le module se réduit alors à M0 et aux
    transferts ;
  - l'utilisateur·rice refuse le plan ;
  - O1 est retenue pour la médecine générale : il ne reste plus qu'un seul transfert partiel.

## 2026-11-15 — Module de besoin : fenêtre d'Open DAMIR réduite à ~37–49 fichiers mensuels
- **Décision** (sur proposition de l'utilisateur·rice : « se limiter à la période du jumeau », affinée) :
  - profils de M1 : 2025, et 2024 pour la stabilité ;
  - P-B6 : mois d'octobre à février des saisons 2015-16 à 2019-20 seulement ;
  - aucun fichier avant 2015, aucun après février 2020 pour P-B6.
- **Pourquoi :**
  - avant 2015, DAMIR est en 9 ZEAT, incompatibles avec les régions de l'expérimentation de 2017 ;
  - le COVID fausse les saisons à partir de 2020 ;
  - le backtest P-B5 repose sur la patientèle, pas sur DAMIR ;
  - Open DAMIR n'a pas d'API de requête (vérifié) : chaque fichier (~0,95 Go) se lit en entier.
- **Correction :** le plan annonçait ~80 Go ; les années prévues faisaient ~100 Go. On passe à ~35–47 Go (dérivé).
- **Résidu :** deux saisons seulement avant l'expérimentation, donc des tendances parallèles peu testables dans P-B6 ;
  la menace est écrite dans le protocole.
- **Ce qui le renverserait :** un besoin de profils plus anciens (dérive du recours, L31), ou une liste des régions
  traitées qui commence avant 2017.


## 2026-11-15 — Module de besoin : Open DAMIR lu en flux, aucun fichier brut stocké
- **Décision** (accord de l'utilisateur·rice, 2026-11-15) :
  - chaque fichier mensuel est lu en flux (`curl | gunzip | filtre`), et seuls les agrégats sont écrits, quelques Mo ;
  - aucun téléchargement avant l'accord sur le plan ;
  - un pilote d'un fichier est lancé d'abord.
- **Pourquoi :** 35 à 47 Go à faire transiter sur la machine locale ; le disque ne doit pas les porter.
- **Ce qui le renverserait :** un débit trop lent en flux (pilote), ou une ingestion déplacée sur une autre machine.

## 2026-11-15 — Module de besoin : passe de littérature ; M2 dédoublé (AREA / saturation) ; ML seulement comme candidat au backtest
- **Décision** (dérivation révisée, rien n'est construit) :
  - **M2 dédoublé.**
    - **M2a « AREA »** : l'offre est fixée à sa moyenne nationale, méthode établie (York 1994, Gravelle et coll.
      2003). Il est ajouté comme repli.
    - **M2b « saturation »** : notre extension, toujours soumise à P-B2, avec un a priori défavorable (Delattre et
      Dormont 2003 ; Léonard et coll. 2009).
  - **M4 projeté avec des poids d'âge figés à une année de base.** La DREES les renormalise à chaque millésime et ne
    voit donc pas le vieillissement.
  - **Le ML n'est pas un estimateur du besoin.** Le besoin n'a pas d'étiquette, et un modèle appris sur le recours
    reproduit la censure. Un GBM entre seulement comme candidat concurrent dans le backtest P-B5. Il n'est servi que
    s'il bat M1 au-delà de l'IC, même règle que C1-GBM (rejeté le 2026-11-15).
- **Pourquoi :** [passe de littérature](explorations/2026-11-15-besoin-litterature.md), trois lecteurs, surtout des
  résumés. Le cœur de M2 est connu sous le nom de formules de capitation fondées sur le recours. Le point de
  saturation, l'APL projetée sous scénarios conjoints, la reproduction de l'APL en données ouvertes et l'opérateur de
  transfert explicite n'ont pas été trouvés.
- **Résidu :**
  - les revendications de nouveauté exigent une recherche journalisée (~30 min) avant d'être écrites ;
  - l'expérimentation de 2017 compte 4 régions selon les arrêtés, 6 selon la Cour des comptes : à lever avant le gel
    de P-B6.
- **Ce qui le renverserait :**
  - un texte intégral (Birch, Gibson et McBride 2020 ; MacKenzie 2019) qui contient déjà `k`, `m` et l'identité ;
  - une projection de l'APL déjà publiée.

## 2026-11-15 — Module de besoin : médecine générale comme source seulement (O2) ; plan accepté, vague 1 lancée
- **Décision** (choix de l'utilisateur·rice : « okay go O2 », après la recommandation de la session) :
  - **O2 retenu** : la médecine générale entre dans le module de besoin **comme profession source des transferts
    seulement**. `B_MG` est calculé par M1.
  - **Interdits :** aucune offre de MG projetée, et **aucun indice de couverture MG**, nulle part (API, carte, rapport).
  - **Affichage :** seulement « actes / ETP de MG libérés ».
  - **Spécialistes :** même règle tant qu'ils sont en phase 2.
  - **Plan accepté :** le [plan par axes](derivations/2026-11-15-besoin-plan.md) est accepté. La vague 1 est lancée
    en quatre sous-sessions : axe 3 (protocoles), axe 4 (données), axe 1 (fiches), axe 0 (interface).
- **Pourquoi :**
  - seule option qui rend calculables les transferts du pitch sans projeter la MG ;
  - conforme au profil du laboratoire (« GPs may appear only as context… never a projected output ») ;
  - coût d'environ 30 min ;
  - réversible.
- **Ce qui le renverserait :** les organisateurs jugent que même le besoin de MG en contexte sort du sujet. On passe
  alors à O1, en retirant `B_MG`.


## ~~2026-11-15 — Module de besoin : règle d'attente pour les tables dérivées ODbL~~
*Remplacé le 2026-11-15 par « Tables dérivées ODbL commitées sous ODbL ».*
- **Décision** (provisoire, posée par la session besoin-derivation au lancement de la vague 1) : tant que la question
  « Licence des tables dérivées de jeux ODbL » reste ouverte, aucune table dérivée des jeux data.ameli.fr ou d'OSM
  n'est commitée. Elles sont écrites dans un chemin ignoré par git ; seuls le script de reconstruction et le
  manifeste sont commités.
- **Pourquoi :** une table ODbL commitée sur le dépôt public engage la licence avant la décision. Ce choix est
  réversible : on commitera les tables une fois la décision prise.
- **Ce qui le renverserait :** la décision de licence (§ Open).

## 2026-11-15 — Module de besoin, axe 0 : le besoin est lu sur la trajectoire, pas rendu comme flux ; indexation sur la base
- **Décision** (session besoin-axe0-interface, dans le cadre du plan accepté) :
  - **Lecteur, pas module de flux.** `v2/besoin/` lit les états d'une trajectoire du jumeau après le run. Il ne
    s'insère pas dans la composition du moteur, qui applique à N tout flux rendu. `v2/jumeau/` n'est pas modifié.
  - **Interface** `besoin.interface.NeedEstimator` : `fit(pop, etat, ref)`, `predict(pop, etat, years) → Cube`
    `B[p, T, t]` en ETP-équivalents, `norme`, `assumptions`, `params` (des `jumeau.module.Param`, donc avec statut).
    Un estimateur par fichier dans `v2/besoin/estimateurs/`, décoré par `@register`, servi par son nom.
  - **Indice de couverture** : `C = [S/B](t) / [S₀/B₀](2026)`, où `(S₀, B₀)` est la base, sans transfert. Un
    transfert actif dès 2026 se lit donc contre la même référence. C au-dessus du département = rapport des sommes,
    jamais une moyenne de C.
  - **Expansion** : `m = μ · s·a·B_A·k`, en temps de la cible, μ = 0 par défaut (supposé).
  - **O2 appliqué en code** : `SANS_COUVERTURE = {médecine générale, spécialistes}`. L'offre, la couverture et
    l'agrégat les refusent, et un transfert ne peut pas les prendre pour cible. La sortie d'API ne rapporte pour eux
    que les « ETP libérés ».
  - **Norme de M0** : r̄ des professions de sortie = offre nationale / population nationale en 2026 (supposé). Il
    s'annule dans C. r̄ de la MG et des spécialistes : 0,9 × 10⁻³ ETP/hab, placeholder (supposé, axe 1).
- **Pourquoi :** le besoin n'est pas un flux sur N ; un lecteur rend « n'écrit jamais dans les effectifs » vrai par
  construction. Indexer sur la base garde une référence unique entre scénarios.
- **Mesures** ([rapport](reports/2026-11-15-besoin-axe0-interface.md)) : 7/7 critères ; 0,72 ms au 95ᵉ centile.
- **Correction :** la première version mesurait 10,5 ms au 95ᵉ centile (critère 5 échoué) : tri de chaînes à chaque
  année. Codes entiers mis en cache par table de cellules : 0,72 ms.
- **Ce qui le renverserait :** un estimateur qui doit rétroagir sur l'offre (hors périmètre, N9) ; un besoin
  qu'il faudrait connaître pendant le run (par exemple une installation guidée par C), qui demanderait un flux.

## 2026-11-15 — Module de besoin, axe 1 : fiches d'hyperparamètres ; L23 seul transfert sourcé ; expérimentation sur 4 régions
- **Décision** (session besoin-axe1-fiches, après relecture contradictoire) :
  - **Format :** une fiche par paramètre pour `ω_a`, `r̄`, `q_p`, `B_MG` et `n_grossesse`, et **une fiche par
    transfert** qui porte ses cinq paramètres `a`, `k`, `s_∞`, `τ`, `m`, chacun avec sa propre étiquette.
  - **`ω_a`** : colonne 2024 (DCIR 2022) pour IDE, CD et SF. Pour les MK, colonne **2023** (DCIR 2021), faute de
    colonne 2024 publiée. Poids figés à l'année de base, comme décidé pour M4.
  - **`q_p`** : unité de la DREES (1 ETP = activité libérale médiane). La valeur n'est pas mesurable en données
    ouvertes : les sorties du module restent en **indice** tant qu'un substitut n'est pas étiqueté.
  - **L23** :
    - `a` : parts des injections en 2018 (Cour des comptes, open data G10) ;
    - `s(t)` : `s_∞` = 0,70 et `τ` = 2,8 ans pour t₀ = 2018 (dérivés), avec les plages [0,63 ; 0,77] et
      [1,6 ; 3,7] ;
    - `m` = 0 par défaut, plage [0 ; +5 %] ;
    - `k` supposé, plage [0,25 ; 1].
  - **Tension / diabète et L25 :** non mesurables, donc hors modèle ou entièrement supposés. Le volume IPA global
    (codes DAMIR 1654, 3129, 3130) sert au plus de borne haute.
  - **L27 :** `k` = 0 par construction ; `a` et `s` supposés.
  - **`n_grossesse`** = 10 contacts réglementaires par défaut (CSP) ; variante HAS à 10 ou 11.
  - **Expérimentation de la vaccination en officine : 4 régions**, d'après l'arrêté du 8 juin 2018 et la HAS 2018
    p. 11. La Cour des comptes en compte 6 (p. 43). Le résidu « 4 ou 6 » de l'entrée du 2026-11-15 (passe de
    littérature) est levé.
- **Pourquoi :**
  - sources primaires lues, puis 142 affirmations relues : 12 écarts retenus et corrigés, 0 faux confirmé sur 11
    contrôles ([rapport](reports/2026-11-15-besoin-axe1-fiches.md)) ;
  - le résultat suit l'attendu du plan.
- **Ce qui le renverserait :**
  - un code DAMIR qui isole l'accès direct (IPA ou kiné) ;
  - une durée publiée de l'acte de vaccination ;
  - la note méthodologique de la Cour qui expliquerait le 0 en officine en 2018 et déplacerait t₀ ;
  - la publication des poids MK 2022.

## 2026-11-15 — Module de besoin : P-B1 à P-B6 gelés avec horodatage externe ; 4 régions pour l'expérimentation de 2017
- **Décision** (axe 3, [rapport](reports/2026-11-15-besoin-axe3-protocoles.md)) :
  - **Six protocoles gelés avant tout calcul** dans `v2/validation/preregistered/2026-11-15-besoin-p-b*.md`.
  - **Gel hors de git, une première pour ce dépôt.** Le manifeste SHA-256 `f0936ab2be34…` est horodaté par deux
    autorités RFC 3161 : FreeTSA à 02:17:19 UTC et DigiCert à 02:17:20 UTC, le 2026-11-15. Il est aussi soumis à
    OpenTimestamps, dont l'ancrage est en attente.
  - Seule l'empreinte est partie, avec l'accord de l'utilisateur·rice dans la session. `ots` a été installé par
    `uv tool`, avec son accord.
  - **Heure de gel citée : celle du jeton.** Aucun croisement recours × offre avant 02:17:19 UTC.
  - **Multiplicité :** Bonferroni par profession dans chaque protocole (IC à 98,75 % pour 4 professions). P-B1 et
    l'indice de P-B3 sont sans inférence. P-B6 a un seul test décisif.
  - **Règles communes :**
    - bootstrap des départements, B = 2 000, graine 20261115 ;
    - P-B6 : bootstrap sauvage par région (12 grappes) et permutation exacte ;
    - le GBM de P-B5 n'entre que si la borne haute de l'IC de Δ(GBM − M1) est < 0 (règle de C1-GBM), avec des
      hyperparamètres figés.
  - **Écarts à la dérivation, déclarés dans les protocoles :**
    - P-B5 juge 4 professions (pas de pharmaciens dans la patientèle), barre à 3 ;
    - P-B6 : 12 zones métropolitaines ; `m` sur Open Medic 2014–2018 ; `s(t)` sur DAMIR jusqu'en 2019-20.
  - **P-B6, régions traitées : 4, pas 6** (Légifrance lu, arrêté du 10/05/2017, NOR AFSS1713194A) :
    - Auvergne-Rhône-Alpes et Nouvelle-Aquitaine dès 2017-18 ;
    - Hauts-de-France et Occitanie dès 2018-19, par l'arrêté du **8 juin 2018**, en vigueur le 15/06/2018.
- **Correction de la passe de littérature.** L'arrêté du 25/09/2018 élargit la **population cible** (art. 3) ; il
  n'ajoute pas de régions. Le chiffre « six régions » de la Cour des comptes n'est retenu nulle part.
- **Pourquoi :** le plan (axe 3) et le rapport technique (§ Intégrité) exigent une antériorité opposable hors de git.
  P-B6 ne pouvait pas être gelé sans la liste des régions traitées.
- **Ce qui le renverserait :**
  - un texte qui ajoute d'autres régions avant 2019 ;
  - un jeton RFC 3161 invalide à la vérification de la chaîne de certificats.

## 2026-11-15 — Module de besoin, P-B1 : l'âge (M1) est retenu pour IDE, MK et SF ; dentistes et pharmaciens attendent P2
- **Décision** (session besoin-v2-m1-m3, passage du protocole gelé P-B1,
  [rapport](reports/2026-11-15-besoin-pb1-age.md)) :
  - **M1 retenu** (dénominateur servi) pour les **infirmiers** (S₁ = 0 %, ρ = 0,835), les **kinés** (0 %, 0,984) et
    les **sages-femmes** (1 %, 0,989), sous le profil APL (P1). Le protocole n'abandonne l'âge que si P1 **et** P2
    concluent à l'abandon : ces trois verdicts sont définitifs.
  - **Dentistes : en attente de P2.** P1 conclut à l'abandon (S₁ = 93,1 % > 90 %, ρ = 0,998 ≥ 0,98). M1 reste
    calculé ; si P2 confirme, M0 suffit pour eux.
  - **Pharmaciens : aucun verdict.** Pas de poids APL ; P2 (Open DAMIR) seul, en attente de l'axe 4. M1 ne les sert
    pas d'ici là.
  - **Le module n'est pas réduit à M0** : M2 et M3 sont construits.
  - **Écarts au protocole, écrits et commités avant calcul** (commit `404d251`) : P2 absent ; N = trajectoire C1
    servie déterministe (pas une médiane de tirages) ; tranches Omphale 90–94 et 95+ au poids « 90 et plus » ;
    MK colonne 2023 ; départements à C non fini retirés (1, IDE).
  - **M1 :** `B₁ = r̄ · Σ pop·ω`, ω APL figé ; r̄ = offre nationale / population standardisée nationale en 2026
    (supposé, s'annule dans C) en attendant le niveau DAMIR.
- **Pourquoi :** seuils gelés appliqués tels quels ; résultat recalculé par un chemin pandas indépendant.
- **Ce qui le renverserait :** P2 pour les dentistes ; une révision des poids APL ; une dérive du recours par âge
  (L31, hors périmètre).

## 2026-11-15 — Module de besoin : amendement A1 aux protocoles P-B2, P-B3, P-B5, P-B6 (gelé, horodaté)
- **Décision** (axe 3, [A1](../../validation/preregistered/2026-11-15-besoin-amendement-a1.md)) : les constats de
  l'axe 4 changent des définitions et des sources, pas les règles de décision.
  - **Recours de la patientèle** = file active moyenne × effectif data.ameli.fr. Le jeu donne une moyenne par
    professionnel, pas un total. L'accessibilité reste calculée sur les effectifs du jumeau, pour ne pas partager
    l'erreur de mesure.
  - **P-B5** : la sensibilité au profil DAMIR 2016 est remplacée par les poids APL du millésime 2022 (DAMIR 2016 non
    lu).
  - **P-B6** :
    - le test décisif sur `m` est inchangé (Open Medic 2014–2018, région de résidence lue au descriptif) ;
    - `s(t)` régional par DAMIR est **abandonné**, car DAMIR est arrêté à 9 mois sur décision de
      l'utilisateur·rice ;
    - `s(t)` devient descriptif : Cour des comptes (national), Liard 2022 (cohortes), IQVIA rapporté à Open Medic.
  - **P-B1 et P-B4 ne sont pas amendés** : ils étaient déjà lancés.
  - **Jetons RFC 3161** à 03:18:22 UTC (FreeTSA) et 03:18:23 UTC (DigiCert), envoyés avec l'accord de
    l'utilisateur·rice. OpenTimestamps est en attente.
  - **Le premier gel** est ancré dans le bloc Bitcoin 975880 (lu par `ots info`, non vérifié contre un nœud).
- **Pourquoi :** les copies gelées supposaient un total de patients et des saisons DAMIR qui n'existent pas sur
  disque. L'amendement est daté et horodaté avant tout passage des quatre protocoles concernés.
- **Ce qui le renverserait :**
  - la page « Méthode » de la patientèle, si elle montre que la moyenne n'est pas pondérée par l'effectif publié ;
  - une reprise de la lecture de DAMIR 2015–2020, qui rouvrirait `s(t)` régional par un amendement A2.

## 2026-11-15 — Module de besoin, axe 4 : ingestion des sources, règles de lecture et de licence
- **Décision** (session besoin-axe4-donnees, dans le cadre du plan accepté) :
  - **Un module par source** dans `v2/besoin/donnees/` (`apl`, `ameli`, `medic`, `iqvia`, `damir`, `distancier`),
    chacun avec sa commande de reconstruction. Une fiche `*.meta.json` par table, rassemblée par `manifest.py` dans
    `v2/besoin/donnees/MANIFEST.md` et `controles.csv`.
  - **Licence → dossier.** Licence Ouverte 2.0 (APL, Open Medic, IQVIA, Open DAMIR, geo.api) :
    `v2/data/processed/besoin/`, commité. ODbL (les cinq jeux data.ameli.fr) : `v2/data/odbl/besoin/`, **ignoré par
    git** tant que la décision de licence est ouverte (§ Open). Seuls le script et le manifeste sont commités.
  - **Open DAMIR :** filtre `PRS_REM_TYP = 0` (le descriptif l'impose : sinon doublons) ; actes comptés par la
    quantité `PRS_ACT_QTE`, pas le dénombrement ; dentistes = nature 19, 53, 54 ou spécialité 36 ; MG = spécialité 1
    (O2) ; clés gardées : mois de flux et de soins, région du bénéficiaire et de l'exécutant, âge, sexe, statut
    juridique, secteur public/privé, top PS5, `PRS_NAT`. Le filtre « libéral » (`stj = 1`, `ppu = 2`) reste à
    l'usage, il n'est pas appliqué à l'agrégation. Les agrégats mensuels (~15 Mo par mois, ~0,7 Go) restent sur
    disque, ignorés par git ; deux tables dérivées sont commitées : `damir_profils` (flux 2024–2025, sans région de
    l'exécutant ni mois de soins) et `damir_vaccination` (codes de vaccination, mois de soins, deux régions).
  - **Fenêtre DAMIR lancée après le pilote :** 213 s pour un mois (0,97 Go, 36,6 M lignes, 4,6 Mo/s, mesuré),
    extrapolé à ~2 h 50 de machine pour les 48 autres mois, sous le seuil de 6 h fixé par la session parente.
  - **Distancier de repli :** distance du grand cercle entre centres geo.api (communes et arrondissements PLM),
    paires à ≤ 35 km ; temps = 1,3 × d / 60 km/h, **les deux valeurs supposées**, à traiter en hyperparamètres par
    M4. Table non commitée (~100 Mo, régénérable en ~10 s). Aucun téléchargement OSM/OSRM.
  - **Écarté :** `depenses-par-poste` de data.ameli.fr (jeu « risques professionnels », AT/MP du régime général).
- **Pourquoi :** critères de l'axe 4 du [plan](derivations/2026-11-15-besoin-plan.md) ; règle de l'utilisateur·rice
  sur la lecture en flux ; licence ODbL ouverte. Détail et contrôles dans le
  [rapport](reports/2026-11-15-besoin-axe4-donnees.md).
- **Résidu :** le contrôle « DAMIR contre le total inter-régimes publié, à 0,5 % » n'est **pas réalisable** tel quel :
  la Statistique mensuelle de la Cnam est en champ régime général + SLM, et DAMIR n'a pas de variable de régime.
  Seul un rapport DAMIR / RG est publié (§ open.md).
- **Ce qui le renverserait :** un total inter-régimes publié par profession (DREES, comptes de la santé, ou rapport
  charges et produits) au même périmètre ; la décision de licence (tables ODbL commitées sous ODbL) ; l'accord pour
  OSRM (le distancier de repli devient une référence naïve).

## 2026-11-15 — Module de besoin, axe 4 : Open DAMIR à 1 flux, 4 flux refusés par le serveur ; filtre en Arrow
- **Décision :** la demande de l'utilisateur·rice (« Oui, 4 en parallèle », relayée par la session parente) a été
  essayée puis **abandonnée**. On revient à 1 flux. Le filtre passe de pandas à Arrow, multi-cœur, pour attaquer le
  vrai goulot (Python mono-cœur, ~93 % d'un cœur, curl à ~4 %). Un refus déclenche une nouvelle tentative toutes
  les 60 s, jusqu'à 12 par mois.
- **Pourquoi :** avec 4 flux, le serveur `open-data-assurance-maladie.ameli.fr` sert une page HTML (« Limite de
  téléchargements atteinte ou délai de connexion dépassé ») au lieu du fichier. Ensuite, même 1 flux est refusé
  pendant plus de 6 min (observé à 03:53–04:01). Le filtre Arrow est identique au filtre pandas sur un test de
  synthèse (200 000 lignes, écart max 7·10⁻¹⁵).
- **Ce qui le renverserait :** une limite documentée qui permette 2 flux, ou un jeton par session (cookie).

## 2026-11-15 — Module de besoin, axe 4 : Open DAMIR arrêté à 9 mois sur 49, faute de temps ; P-B6 proposé sur Open Medic
- **Décision** (accord de l'utilisateur·rice : « oui go », en ajoutant qu'il faudra écrire qu'on était limités par
  le temps) :
  - la lecture d'Open DAMIR s'arrête aux 9 mois lus (flux 2025-01 à 2025-09). La boucle de relance est arrêtée.
    Pas de partage de connexion : ~37 Go pour un seul paramètre ;
  - `damir_profils` et `damir_vaccination` sont construits sur ces 9 mois ;
  - **proposé à l'axe 3** pour P-B6 : m mesuré sur Open Medic (boîtes J07BB par région de résidence, 2014–2025,
    différence de différences annuelle), et s(t) pris dans la part nationale de la Cour des comptes. C'est à l'axe 3
    de trancher avant le gel.
- **Pourquoi :**
  - l'indice M1 est rapporté à 2026, donc le niveau du recours s'annule ; la forme par âge vient des poids APL
    (4 professions) et des 9 mois de DAMIR (PH) ;
  - le prix par acte de M3 se calcule sur 9 mois ;
  - seul s(t) régional exigeait les 25 mois de 2015–2020 ;
  - le serveur bloquait la machine (adresse IP probable) depuis 03:53, et le temps du hackathon manque.
- **Supersede en partie** « Open DAMIR lu en flux » et « fenêtre réduite à ~37–49 fichiers » (2026-11-15) : la
  fenêtre décidée n'est pas lue en entier. La règle de lecture en flux reste.
- **Ce qui le renverserait :** du temps et une connexion non bloquée. `damir.py --fenetre` reprend là où il s'est
  arrêté.

## ~~2026-11-15 — Module de besoin : Open DAMIR définitivement limité à 9 mois pour cette phase, faute de temps~~
*Remplacé le 2026-11-15 : DAMIR 2025 a été lu en entier (octobre à décembre via un autre réseau, addendum de 05:06 du rapport de l'axe 4) ; `damir_profils` et `damir_vaccination` couvrent 12 mois.*
- **Décision** (utilisateur·rice : « mets donc bien dans le rapport qu'on a rien pu faire faute de temps ») :
  - Open DAMIR reste à 9 mois (2025-01 à 2025-09) pour toute la phase en cours ;
  - les 40 mois restants ne sont pas lus ;
  - le rapport de l'axe 4 porte un addendum qui le dit.
- **Pourquoi :**
  - l'IP de la machine a été bloquée par le serveur après le passage à 4 flux (proposé par la session parente) ;
  - la relance depuis un autre ordinateur, sur le même wifi, a échoué ;
  - le temps manque.
- **Conséquences :**
  - profils de M1 et prix moyens de M3 calculés sur 9 mois (biais saisonnier ≤ 1,3 %, mesuré) ;
  - P-B6 passe sur Open Medic (amendement A1).
- **Ce qui le renverserait :** une connexion non bloquée et du temps. Commande à 1 flux, dans l'addendum du rapport
  de l'axe 4.

## 2026-11-15 — Module de besoin, P-B6 : m reste supposé à 0 (absence d'effet détectable, placebo en échec) ; s(t) de L23 mesuré sur la série nationale
- **Décision** (règles gelées de P-B6 et de l'amendement A1, [rapport](reports/2026-11-15-besoin-p-b6-grippe-officine.md)) :
  - **`m` du transfert L23 = 0, étiqueté « supposé ».**
    - ATT +0,73 % [−0,12 ; +1,58] (IC 95 % bootstrap sauvage), permutation p = 0,15 sur 2 970 affectations.
    - Le placebo 0–19 ans donne +4,7 % [+1,2 ; +8,2] : verdict « non attribuable ».
  - **`s(t)` de L23** : s∞ = 0,74 ± 0,07, τ = 2,4 ± 0,5 ans, t₀ = 2019, ajusté sur la part officinale nationale
    (IQVIA ÷ Open Medic, 2021-22 à 2024-25). Il remplace la forme supposée par l'axe 1.
- **Pourquoi :** c'est le protocole gelé. Le résultat est cohérent avec les a priori publiés (HAS 46,1 % contre
  46,0 % ; Buchan 2017, rapport de prévalence 1,05).
- **Correction :** l'écart 8, écrit avant le calcul, tenait la campagne 2025-26 pour partielle. Elle est complète.
  L'ajustement de sensibilité qui l'inclut donne le même résultat (s∞ 0,75, τ 2,4).
- **Ce qui le renverserait :**
  - un placebo refait avec le vrai dénominateur 0–19 ans, qui passerait ;
  - un `s(t)` régional tiré de DAMIR 2015–2020.


## 2026-11-15 — Module de besoin : formulations de nouveauté retenues (aucun « premier »)
- **Décision** ([recherche journalisée](explorations/2026-11-15-besoin-nouveaute.md), 14 requêtes, profondeur « scan+ ») :
  - n° 1 (APL/E2SFCA projetée à 2050, démographie et effectifs en mouvement) : « nous n'avons pas trouvé, dans une
    recherche de profondeur limitée, de travail combinant… » ; plus proche voisin Bruns et coll. 2026 (IZA DP 18801).
  - n° 2 (reproduction de l'APL en données ouvertes) : décrite comme une évaluation, sans revendication d'antériorité.
  - n° 3 (opérateur de transfert) : « extension formelle de MacKenzie et coll. 2019 » ; `m` supposé nul (P-B6).
  - M2b (plateau de saturation) : revendication abandonnée, M2b étant tué par P-B2.
- **Pourquoi :** Scholar et Scopus non interrogés directement ; une recherche « scan » ne peut pas établir une nouveauté.
- **Ce qui le renverserait :** un 2SFCA dans le PDF de Bruns 2026 ou dans Doi 2017 ; une passe « standard » sur
  Scholar et Scopus qui ne trouve toujours rien (permettrait « à notre connaissance »).

## 2026-11-15 — Module de besoin, nouveauté : formulations confirmées après lecture de Bruns 2026 et Doi 2017
- **Décision :** les formulations de l'entrée précédente sont maintenues sans changement
  ([addendum](explorations/2026-11-15-besoin-nouveaute.md#addendum-même-jour--textes-lus-et-deuxième-passe-apis-ouvertes)).
- **Pourquoi :** Bruns 2026 (PDF lu) n'utilise ni 2SFCA ni distance ; Doi 2017 projette la demande contre des lits fixes.
  25 requêtes au total (Europe PMC, HAL en plus) sans antécédent trouvé.
- **Ce qui le renverserait :** une passe Scholar et Scopus (CAPTCHA ici, accès institutionnel requis).

## 2026-11-15 — Les spécialistes (ancienne « phase 2 ») deviennent une amélioration possible, hors plan
- **Décision** (utilisateur·rice, relayée par une bifurcation de la session besoin-derivation, puis confirmée ici :
  « Oui, les deux ») :
  - la phase 2 (cardiologie, dermatologie, ophtalmologie) **n'est plus à l'ordre du jour** : elle entre dans les
    améliorations possibles ;
  - les spécialistes restent admis comme **profession source** d'un transfert de tâches, sans projection ni indice de
    couverture (règle O2).
- **Remplace :**
  - « Spécialistes en phase 2 » (recadrage du 2026-11-14, `CLAUDE.md`, `v2/ROADMAP.md` §1 et §5, profil du
    laboratoire) ;
  - la condition de démarrage de la phase 2 dans le rapport technique (`ch-ouvertes.tex`).

  Ces mentions sont barrées ou annotées, pas effacées.
- **Pourquoi :** choix de l'utilisateur·rice. Le travail se concentre sur les cinq professions et sur le module de
  besoin.
- **Aussi aligné :** `docs/lab/profile.md`, README, Home. Le PDF du rapport technique n'est pas recompilé.

## 2026-11-15 — Module de besoin, P-B1 sous P2 : l'âge (M1) est retenu pour les cinq professions
- **Décision** (session besoin-v2-m1-m3, [rapport](reports/2026-11-15-besoin-pb1-age.md), section « Passage P2 ») :
  complète l'entrée précédente du même jour (qui laissait dentistes et pharmaciens en attente).
  - **Dentistes : M1 retenu.** P2 (Open DAMIR) conclut au maintien (S₁ = 87,1 % < 90 %, ρ = 0,999) ; l'abandon
    exige P1 **et** P2. Décision de justesse : l'écart est un décalage national du niveau, pas du classement.
  - **Pharmaciens : M1 retenu** sur P2 seul (S₁ = 0 %, ρ = 0,987). Profil DAMIR servi par M1 pour PH et MG.
  - **Écarts écrits avant calcul** (commit `4efa8b4`) : 9 mois de flux 2025 ; champ `PRS_PPU_SEC = 2` ; quantité
    sommée sur toutes les natures de prestation ; inconnus d'âge et de sexe exclus ; profil décennal, 80+ plat.
  - **MG (source O2)** : r̄ = 0,9 × 10⁻³ ETP par habitant standardisé, placeholder de M0 (supposé).
- **Pourquoi :** seuils gelés appliqués ; P1 reproduit à l'identique au second passage.
- **Ce qui le renverserait :** un profil PH en temps de pharmacien (unité « boîtes + honoraires » mêlée, ledger) ;
  les 3 mois de DAMIR manquants, si le biais saisonnier dépasse celui mesuré par l'axe 4 (≤ 1,3 %).

## 2026-11-15 — Module de besoin, P-B2 : M2b (saturation) tué ; M2a (AREA) construit comme repli
- **Décision** (session besoin-v2-m1-m3, [rapport](reports/2026-11-15-besoin-pb2-saturation.md)) :
  - **M2b tué pour les quatre professions testées** (IDE, MK, CD, SF) par la règle gelée : borne haute de l'IC à
    98,75 % de δ ≥ 0 partout ; pente du premier quintile non distinguable de 0 pour IDE, MK, SF ; placebo non
    attribuable pour MK et CD. Pharmaciens : non applicable (dérivation §6).
  - **Retrait du service** : `m2b.py` garde le code et le verdict, la classe n'est plus enregistrée.
  - **Le niveau du besoin non satisfait n'est pas identifié** par les données ouvertes au département.
  - **M2a construit** : `log R_std = α + β log A + γ log M`, M = indice de morbidité standardisé par âge et sexe
    (part des consommants avec au moins un repérage de la cartographie des pathologies 2024), offre fixée à la
    moyenne nationale ⇒ `B₂ₐ = r̄ · B₁ · M^γ`, M figé à 2024 (supposé). γ mesuré : IDE 3,66, MK 0,92, CD 1,44,
    SF 0,06 (MCO, 2023–2025).
  - **Écarts P-B2 écrits avant calcul** (commit `3ac2abd`) : Omphale au lieu des estimations Insee ; offre IDE 2023
    seule ; stabilité sur 2018 seule ; descriptif de la patientèle sans définition du département ; placebo sur le
    B₁ de la profession testée ; NLS `maxfev = 200`.
- **Pourquoi :** seuils gelés appliqués tels quels ; a priori de la littérature confirmé (pas de saturation).
- **Ce qui le renverserait :** un recours en actes au département ; un département de patientèle qui serait celui
  de résidence ; une offre IDE libérale seule (sensibilité au ledger).

## 2026-11-15 — Module de besoin, P-B3 : M3 sert l'indice des seuls infirmiers ; H-B3 rejetée
- **Décision** (session besoin-v2-m1-m3, [rapport](reports/2026-11-15-besoin-pb3-pathologies.md)) :
  - **(A) M3 retenu pour l'indice des infirmiers** (S₃ = 83 % < 90 %, ρ = 0,992, aux trois imputations) ;
    **réduit au recoupement** pour MK, CD, SF, PH (S₃ de 95 à 100 %, ρ ≥ 0,998 aux trois imputations).
    Constante `m3.INDICE = {infirmiers}`.
  - **(B) H-B3 rejetée** pour IDE, MK, CD, SF : ΔR² hors échantillon −0,03 à +0,01 (seuil 0,10).
  - **M3 (voie i)** : 16 groupes de niveau 1 de la cartographie 2024 (partition de la dépense) × dépense remboursée
    nationale par patient du groupe / prix moyen DAMIR (9 mois) + résidu national `r₀` par âge et sexe, non borné.
    Prévalences figées à 2024 (supposé). Unité : actes.
  - **Écarts écrits avant calcul** (commit `3bf9b5d`) : 18 plis régionaux (DROM compris) au lieu de « 13 » ;
    triangulation sans objet (M2b tué) ; voie (ii) SF non branchée.
- **Correction** : le rapport P-B2 disait « P-B3 compare M3 à M2a » ; le protocole ne le prévoit pas (corrigé).
- **Pourquoi :** seuils gelés appliqués tels quels.
- **Ce qui le renverserait :** une dépense par cas ventilée par âge ; une morbidité non repérée par la
  consommation de soins.

## 2026-11-15 — Module de besoin, P-B5 : H-B1 retenue ; le GBM qualifie pour IDE, CD, SF, mise en service ouverte
- **Décision** (session besoin-v2-m1-m3, [rapport](reports/2026-11-15-besoin-pb5-backtest.md)) :
  - **H-B1 retenue** : M1 bat la persistance du recours par habitant à 9 ans (2016 → 2025, MAPE départementale)
    pour IDE (7,7 contre 15,8), MK (10,8 contre 14,1), CD (9,4 contre 10,4), IC à 98,75 % sous 0 ; **SF perd**
    (66,6 contre 65,0). Même verdict sous P2 (poids APL 2022) : pas dépendante du profil.
  - **GBM** : qualifie par la règle gelée pour IDE, CD, SF ; **pas mis en service** dans cette session, car la
    mise en service comme besoin contredirait la norme (gain lié à la croissance de l'offre). Question ouverte
    (§ Open), avec avis : prédicteur du recours seulement.
  - **Données téléchargées** avec l'accord de l'utilisateur·rice : estimations de population Insee 1975–2023
    (département × sexe × âge quinquennal, `v2/data/raw/insee/`, ignoré par git) ; 2025 = Insee 2023 × croissance
    Omphale (écart 1, écrit avant calcul, commit `dd66519`). Autres écarts : kinés densité 2017 ; 18 plis régionaux.
- **Pourquoi :** seuils et hyperparamètres gelés appliqués tels quels.
- **Ce qui le renverserait :** un profil d'âge antérieur à 2016 (regard en avant) ; un recours en actes au
  département ; les estimations Insee 2025 définitives.

## 2026-11-15 — Module de besoin, P-B5 : le GBM servi comme prédicteur du recours seulement
- **Décision** (choix de l'utilisateur·rice : « Usage only », option (a) de la question ouverte du même jour) :
  - Le GBM de P-B5 est servi par `v2/besoin/estimateurs/gbm_recours.py` comme **prédicteur du recours** (patients,
    file active × effectif) pour IDE, CD et SF, les trois professions où il bat M1 au-delà de l'IC.
  - **Jamais comme besoin** : ce n'est pas une `NeedEstimator`, la classe n'est pas enregistrée, `besoin_api` ne
    peut pas le choisir (test L4). Kinés refusés (non qualifiés).
  - **Horizon servi : 9 ans seulement** (`predit(p, origine)` → origine + 9), appris sur toutes les paires
    2016 → 2025, hyperparamètres gelés de P-B5.
  - Branchement dans l'API ou la carte : non fait (hors des fichiers de cette session).
- **Pourquoi :** son gain suit la croissance de l'offre (diagnostic de P-B5) ; servi comme besoin, il rendrait B
  dépendant de l'offre, contraire à la norme et au cas limite « offre nulle ».
- **Ce qui le renverserait :** un GBM dont le gain résiste à un terme d'offre explicite ; une validation à un autre
  horizon.

## 2026-11-15 — Module de besoin, axe 4 : Open DAMIR porté à 12 mois (année 2025)
- **Decision :** les profils DAMIR (`damir_profils`, `damir_vaccination`) portent sur les 12 mois de 2025, et non plus
  sur 9. Supersède partiellement l'entrée « Open DAMIR arrêté à 9 mois sur 49, faute de temps ; P-B6 proposé sur Open Medic » (titre cité corrigé le 2026-11-15) : la limite
  tient encore pour 2024 et les campagnes 2015–2020.
- **Why :** l'utilisateur·rice a changé de réseau ; 2025-10 à 2025-12 ont été lus à 3 flux sans refus, en ~6 min de
  machine (mesuré). Contrôles bloquants passés.

## 2026-11-15 — Module de besoin : cible externe de M4 pharmaciens = APL DREES V0 2013 ; P-B4-PH gelé
- **Decision :** la cible de validation de M4 pharmaciens est l'APL DREES « Méthode initiale V0 » aux pharmacies,
  2013 (2010 en secondaire). Tranche l'entrée ouverte du même jour (« Cible externe de M4 pharmaciens »). Offre BPE
  2013, population RP 2011 brute, paliers 5 / 10 / 15 min de la Notice.
- **Why :** seule APL des pharmacies publiée (s) ; IRDES QES 308 n'en a pas ; le temps Insee au plus proche mesure
  autre chose.
- **Gel :** accord de l'utilisateur·rice (« Yes, timestamp it », 2026-11-15). SHA-256 `f96520f9…549d83` ; RFC 3161
  FreeTSA 04:09:44 UTC et DigiCert 04:09:45 UTC ; OpenTimestamps soumis. Jetons dans
  `v2/validation/preregistered/horodatage/2026-11-15-besoin-p-b4-ph-SHA256SUMS*`.

## 2026-11-15 — Tables dérivées ODbL commitées sous ODbL
- **Décision** (utilisateur·rice : « licence c'est ok pour ODbL sur nos données ici ») :
  - les tables dérivées des jeux data.ameli.fr (démographie, patientèle, honoraires, pathologies effectifs et
    dépenses ; 54 Mo) sont **commitées dans `v2/data/odbl/besoin/` sous ODbL 1.0**, avec la mention de la CNAM ;
  - les dérivés d'OpenStreetMap (matrice de temps OSRM) suivent la même licence, mais restent hors dépôt pour leur
    taille (`v2/data/odbl/osm/`, ignoré) ; on les reconstruit par script ;
  - les données sous Licence Ouverte 2.0 et le code ne changent pas.
- **Remplace :** la règle d'attente du même jour (aucune table ODbL commitée).
- **Reste ouvert :**
  - la licence du code (EUPL 1.2 proposée), d'où `LICENSE.draft` ;
  - l'activation de `NOTICE`, dont `NOTICE.draft` porte encore des mentions « à confirmer » (rapport
    `2026-11-15-licences-brouillon`).

  Tant que `NOTICE` n'est pas activé, la mention ODbL est portée par `v2/data/odbl/README.md`.
- **Pourquoi :** les chercheurs qui clonent le dépôt doivent avoir toutes les entrées de P-B2, P-B3 et P-B5 sans
  reconstruction.

## 2026-11-15 — Module de besoin : M4 construit ; P-B4 échoue en repli, M4 reste un indice maison
- **Décision** (session besoin-v2-m4, [rapport](reports/2026-11-15-besoin-p-b4-apl.md)) :
  - **M4** (`v2/besoin/estimateurs/m4.py`) : 2SFCA aux paliers DREES, relus dans l'onglet « Paramètres ». Le besoin
    vient d'un estimateur d'entrée (M4∘M1…) ; par défaut, poids d'âge ω de l'APL figés à l'année de base (2024 ;
    2023 pour les MK). `predict()` rend le besoin d'entrée inchangé ; `accessibilite()` rend A en ETP pour 100 000.
    Temps : vol d'oiseau × 1,3 à 50 km/h (supposé), en attendant OSRM.
  - **P-B4 passé en repli**, avec 11 écarts écrits et commités avant le passage (`76c04d5`) : `pop_std` de la DREES
    comme P^std, part des moins de 65 ans départementale, SF lues dans `sf_popage`, ETP = honoraires sans
    dépassement moyens / médiane.
  - **Verdict : indice maison pour les 4 professions.** ρ = 0,72 (IDE), 0,77 (MK), 0,66 (SF), 0,74 (CD), sous 0,90 ;
    EM de 21 à 29 %, au-dessus de 15 %. Le gain sur la meilleure densité naïve passe partout (+0,15 à +0,31, IC à
    98,75 % > 0). Aucun seuil changé.
  - **Libellé imposé :** M4 n'est jamais appelé « APL » dans la sortie, la carte ou un rapport.
  - Critères M4a–M4d dans `besoin.tests` (découverte des modules `criteres_*.py`), 11/11.
- **Pourquoi :** protocole gelé ; le repli ne peut pas valoir reproduction, et il échoue de toute façon.
- **Résidu :** la cause probable la plus forte est le distancier (Corse et montagne en tête des écarts ; ρ MK 0,78
  hors montagne, 0,66 dedans) ; l'ETP moyen départemental est la seconde. Passage OSRM soumis à l'accord de
  l'utilisateur·rice (extrait OSM de 4,8 Go).
- **Ce qui le renverserait :** un passage OSRM, daté comme amendement avant calcul, qui atteint les trois seuils.
- *Résidu complété le 2026-11-15 : le passage OSRM a eu lieu et échoue aussi ; le distancier n'est pas la cause
  principale. Voir l'entrée « P-B4 sur OSRM ».*

## 2026-11-15 — Module de besoin : P-B4 sur OSRM échoue aussi ; l'écart vient de l'offre communale, pas du distancier
- **Décision** (session besoin-v2-m4, accord de l'utilisateur·rice « Yes, OSRM », [rapport](reports/2026-11-15-besoin-p-b4-apl.md)) :
  - **OSRM installé** (Homebrew 26.11.0) ; extrait OSM France du miroir openstreetmap.fr (5,9 Go, plus rapide que
    Geofabrik) dans `v2/data/raw/osm/` du dépôt principal, non versionné. Graphe : métropole et Corse, voies
    carrossables seulement (le graphe complet saturait 24 Go de mémoire), algorithme CH.
  - **Distancier routier** `v2/besoin/donnees/distancier_osrm.py` → `v2/data/odbl/besoin/distancier_osrm.parquet`
    (ODbL, non commité, règle d'attente) : 2 997 245 paires à 30 min au plus, rayon de recherche 50 km.
  - **P-B4, passage 2 (voie principale, amendement A1 daté avant calcul) : indice maison pour les 4 professions.**
    ρ = 0,72 (IDE), 0,76 (MK), 0,71 (SF), 0,73 (CD) ; EM de 23 à 33 % ; gain sur les naïfs +0,15 à +0,35, IC > 0.
    Aucun seuil changé. Ce verdict remplace celui du repli comme verdict de P-B4 ; le repli reste rapporté.
  - **Diagnostic :** temps routiers contre vol d'oiseau, ρ change de −0,01 à +0,05 ; au département, ρ = 0,98 (MK).
    L'écart est dans la répartition de l'offre entre communes d'un même département (ETP individuel borné de la DREES,
    commune d'exercice SNIIR-AM), non ouverte au grain individuel.
- **Pourquoi :** voie principale du protocole, accordée ; elle tranche la cause que le repli laissait ouverte.
- **Résidu :** centres geo.api et non mairies ; voies `service` exclues ; profil OSRM par défaut.
- **Ce qui le renverserait :** une offre communale plus fidèle (activité individuelle ouverte, ou une offre inversée
  depuis l'APL publiée) qui, avec nos temps, atteindrait les seuils : l'écart viendrait alors bien de l'offre.

## 2026-11-15 — Module de besoin, P-B4-PH : M4 ne reproduit pas l'APL V0 des pharmacies ; indice maison
- **Décision** (règles gelées de P-B4-PH, [rapport](reports/2026-11-15-besoin-p-b4-ph-apl-v0.md)) :
  - **M4 pharmaciens reste un indice maison**, jamais appelé « APL ».
  - Mesures 2013 : Spearman M4–APL V0 0,72 [0,71 ; 0,74], sous 0,90 ; erreur médiane 33 %, au-dessus de 15 % ; gain
    sur la meilleure densité naïve +0,14 [+0,12 ; +0,16], qui passe.
  - Le niveau moyen est reproduit : 22,1 contre 22,5 officines pour 100 000 habitants.
- **Pourquoi :** c'est le protocole gelé. Le profil est le même que P-B4 pour les quatre autres professions. Ici
  l'offre est un simple compte d'officines : l'activité non ouverte n'explique donc pas l'écart. Les suspects
  principaux sont le distancier (paliers de 5 min) et la source de l'offre (FINESS contre SNIIR-AM).
- **Ce qui le renverserait :** un contrôle du distancier, ou une offre tirée de la BPE, qui ferait monter le Spearman
  au-dessus de 0,90.

## 2026-11-15 — Module de besoin : périmètre « libéral » de DAMIR, trois réserves mesurées et tranchées
Demande de la session v2 (accord de l'utilisateur·rice relayé, « oui »). Mesures sur `damir_profils.parquet`, flux
2025, secteur privé (`ppu = 2`).

1. **Statut inconnu (`stj = 9`) : déjà réintégré, rien à corriger.**
   - Part de `stj = 9` en actes (en montant remboursé) :

     | Profession | Actes | Montant |
     |---|---|---|
     | IDE | 12,6 % | 7,8 % |
     | MK | 7,8 % | 5,0 % |
     | PH | 5,5 % | 5,3 % |
     | CD | 3,9 % | 3,9 % |
     | SF | 3,3 % | 2,1 % |

     (mesuré)
   - **M1 ne filtre pas sur `stj`** : il prend `ppu = 2` et tous les statuts (1 libéral, 2 salarié de centre,
     9 inconnu). Le sous-comptage supposé n'existe donc pas dans le modèle ; seuls les contrôles de `damir.py`
     distinguent `stj`. C'est vérifié dans `estimateurs/m1.py`, où le filtre `ppu == 2` est le seul.
   - Sensibilité mesurée : la répartition par âge, tous statuts contre libéral strict (`stj = 1`), diffère de 2,7 %
     (IDE), 2,1 % (MK), 1,7 % (CD), 0,9 % (PH) et 0,2 % (SF) en variation totale (mesuré).
   - **Décision : garder tous les statuts.** On n'applique ni prorata ni filtre `stj = 1`.
2. **Offre privée contre recours de ville : écart de définition documenté, sans effet sur l'indice si les parts
   restent constantes.**
   - L'offre privée du jumeau compte les salariés du privé. Ordre de grandeur, part des salariés dans l'offre privée
     (`secteur_stock`, au centre de la fourchette) (mesuré) :

     | Profession | Millésime | Salariés du privé | dont clinique | Libéraux et mixtes |
     |---|---|---|---|---|
     | IDE | 2023 | 64,5 % | 34,0 % | 35,6 % |
     | PH | 2026 | 54,5 % (adjoints, industrie) | — | — |
     | SF | 2026 | 20,3 % | — | — |
     | MK | 2026 | 6,1 % | — | — |
     | CD | 2026 | 1,7 % | — | — |

   - Le recours DAMIR de ville ne compte pas les soins facturés par les établissements (IDE de clinique). Il compte en
     revanche les salariés de centres de santé (`stj = 2` : SF 13 %, CD 16 % des actes).
   - **Effet sur C** : nul tant que la part libérale de l'offre est constante dans le temps, puisque C est indexé
     à 2026 et qu'un facteur constant s'annule (dérivé). L'effet n'est pas nul **sur les niveaux** (ETP, comparaisons
     entre territoires).
   - **Décision :** l'indice reste « offre privée / demande de ville privée », avec l'écart écrit dans la sortie.
     Un niveau en ETP n'est jamais comparé à l'effectif privé total des IDE ni des PH. L'alignement exact
     (projeter la part libérale) reste ouvert.
3. **Deux grandeurs nommées distinctement.**
   - Ce que M1, M2a, M2b, M3 et M4 produisent est la **demande adressée au secteur privé de ville**, tirée du
     recours remboursé hors hôpital public. Ce n'est **pas le besoin de soins de la population**, dont une part est
     servie par l'hôpital public.
   - Dans le modèle : attribut `grandeur` de `NeedEstimator` (`v2/besoin/interface.py`), exposé dans la sortie
     d'API (`sortie.py`, clé `grandeur`). Le mot « besoin » reste celui du code (`B`, `besoin`), mais l'interface
     affiche la grandeur.
   - Dans l'interface : un libellé « demande de soins de ville (privé) », jamais « besoin de la population » ;
     l'indice C s'intitule « couverture de la demande de ville par l'offre privée ». C'est à appliquer au branchement
     dans la carte (plan de la session licences-et-carte).
- **Pourquoi :** demande de la session v2. La circularité recours/offre de la dérivation (§2) en est le cas général.

## 2026-11-15 — Module de besoin, axe 5 : C des kinés et des infirmiers affiché en fourchette entre estimateurs

## ~~2026-11-15 — Module de besoin, axe 5 : C des kinés et des infirmiers affiché en fourchette entre estimateurs~~
*Remplacée le 2026-11-15 pour l'affichage : voir « axe 5 : M0 retiré de la fourchette affichée ». Le verdict gelé ci-dessous reste valable et publié.*
- **Décision** (règle gelée du protocole `2026-11-15-besoin-axe5-sensibilite`, [rapport](reports/2026-11-15-besoin-axe5-sensibilite.md)) :
  - **Protocole gelé avant tout calcul de B ou de C** : SHA-256 `10a5b285…cd87834`, RFC 3161 FreeTSA 05:28:15 UTC
    et DigiCert 05:28:16 UTC, OpenTimestamps soumis ; accord de l'utilisateur·rice (« Oui, horodater »). Jetons dans
    `v2/validation/preregistered/horodatage/2026-11-15-besoin-axe5-SHA256SUMS*`.
  - **Ratio R = |Δ log C| de quotas × 1,2 / étendue de log C entre estimateurs survivants**, France, 2050 (mesuré) :
    SF 1,91, CD 40, PH 1,14 (distinguables) ; MK 0,77, IDE 0,34 (non distinguables).
  - **Règle d'affichage déclenchée pour les kinés et les infirmiers** : leur indice de couverture est affiché en
    **fourchette entre estimateurs** (min–max de M0, M1, M2a ; plus M3 pour les IDE), jamais un seul chiffre.
    SF, CD, PH : estimateur servi seul (M1).
  - **Statistique et seuil appliqués tels quels.** Aucun seuil changé.
- **Pourquoi :** seuil gelé du plan (R < 1 ⇒ « non distinguable ») et règle du critère d'acceptation de l'axe 5.
- **Résidu :** l'étendue vient presque toute de M0 ; sans M0, elle vaut ≤ 0,004 en log et R ≥ 25 partout. Garder
  M0 comme borne de la fourchette reste une question ouverte (§ Open / not yet decided). Les tirages de l'offre C1 portent 52 à
  92 % de la variance de log C : c'est la première source de largeur, pas le besoin.
- **Ce qui le renverserait :** une décision retirant M0 des estimateurs survivants (P-B1 a retenu l'âge) ; un test
  de séparabilité de l'offre qui change R de plus de 0,1.

## 2026-11-15 — Module de besoin, axe 5 : M0 retiré de la fourchette affichée ; le vieillissement est montré comme un effet
- **Décision** (utilisateur·rice : « okay donc go enlève le », après discussion sous l'angle de l'aide à la décision
  du DG d'ARS) :
  - **M0 n'est plus une borne de la fourchette affichée de C**, pour aucune profession. P-B1 l'a réfuté (l'âge est
    retenu pour les cinq professions) : ce n'est pas une alternative plausible.
  - **C est servi par l'estimateur retenu** : M1 ; M3 pour les infirmiers. Les estimateurs survivants qui tiennent
    compte de l'âge (M1, M2a, M3) diffèrent de 0,4 % au plus en 2050 (≤ 0,004 en log, mesuré) : un seul chiffre suffit
    au regard du choix du modèle de besoin.
  - **L'écart M0 → M1 est présenté comme l'effet du vieillissement sur le besoin**, à côté de l'effet du levier, pas
    comme une incertitude. Exemple, IDE, France, 2050 : C = 0,83 avec l'âge, 1,14 sans ; quotas × 1,2 : +11 % (mesuré).
  - **L'incertitude affichée autour de C est la bande de l'offre** (tirages de C1), qui porte 52 à 92 % de la variance
    de log C.
- **Remplace** l'affichage en fourchette de l'entrée « axe 5 : C des kinés et des infirmiers affiché en fourchette
  entre estimateurs ». **Le verdict gelé ne change pas** : R = 0,77 (MK) et 0,34 (IDE) avec M0 dans l'ensemble, publié
  tel quel. Ce changement est postérieur au résultat et déclaré comme tel ; aucun seuil n'est modifié.
- **Pourquoi :** une fourchette bornée par un modèle réfuté se lit « on ne sait pas » ; le message utile au décideur
  est « le vieillissement pèse plus que ce levier ». La largeur réelle de C vient de l'offre.
- **Ce qui le renverserait :** un choix normatif d'un « besoin égal par habitant » (M0 servi alors comme option
  choisie, pas comme borne d'incertitude) ; un estimateur plausible qui s'écarterait de M1 de plus que l'effet des
  leviers.

## 2026-11-15 — Module de besoin : rôle de M4 précisé ; pas de décomposition de l'écart à l'APL
- **Décision** (utilisateur·rice : « the actual M4 calculus was to have something rigorous in the metric of spatial
  accessibility, that's all ») :
  - **M4 sert de mesure rigoureuse d'accessibilité spatiale**, pas de reproduction de l'APL. Ce qui le rend
    rigoureux est déjà en place : paliers et poids publiés par la DREES, conservation exacte `Σ P·A = Σ S`
    (≈ 10⁻¹⁶), limites rayon 0 et ∞ testées, temps routiers OSRM.
  - **P-B4 reste au registre tel quel** : il dit seulement que M4 n'est pas le chiffre de l'APL (libellé « indice
    maison » maintenu) ; au département, M4 suit l'APL (ρ = 0,98, MK).
  - **Abandonné :** la décomposition de l'écart communal (offre contre distancier) ; elle confirmerait un diagnostic
    sans rien changer à l'usage.
- **Pourquoi :** le but de M4 est la métrique, pas la cible externe ; l'écart restant tient à des données non
  ouvertes (activité individuelle, adresse d'exercice).
- **Ce qui le renverserait :** un besoin de présenter M4 comme l'APL, ou l'ouverture de l'activité individuelle.


## 2026-11-15 — Assistant et compilateur : L23 compilé en transfert, couverture servie par l'API de la carte
- **Décision** (tâche de la session v2, [rapport](reports/2026-11-15-besoin-assistant.md)) :
  - **Compilateur** : la vaccination en officine produit un champ `transferts` (L23, avec t0 : année qui suit le terme
    dans sa proposition, défaut 2026) **et reste dans `non_modelise`**, car l'effectif ne change pas. L25, L27 et
    tension/diabète restent hors modèle, avec la raison « non mesurable » de leur fiche, sans transfert.
  - **Assistant** : l'indice de couverture vient seulement de l'outil `couverture` (passerelle → `GET /api/couverture` de
    la carte, contrat de l'étape 1 du plan besoin-carte ; branche de l'API absente au 2026-11-15). Écart au tendanciel en
    relatif, qualifié par seuils (< 1 % proche, < 5 % légèrement, au-delà sans adverbe) ; fourchette entre estimateurs
    quand l'API la donne. Jamais « % du besoin couvert ». MG et spécialistes : refus (O2), dans le schéma, la passerelle,
    le périmètre et le prompt.
  - **La passerelle charge le compilateur du dépôt** (`v2/langage/`) quand il existe, sinon celui de `vendor/` ;
    `LANGAGE_DIR` le force.
- **Pourquoi :** garder les jeux à l'aveugle comparables (vaccination toujours « non modélisée » pour l'effectif) ; ne
  pas recalculer la couverture hors de l'API de la carte ; le glossaire évolue plus vite que la copie du modèle.
- **Ce qui le renverserait :** une API de couverture publiée sous une autre forme ; une décision de servir le
  compilateur figé de `vendor/` seulement.

## 2026-11-15 — Besoin → carte : vue « Couverture », L23 de bout en bout, M4 en attente (P-B4)
- **Décision** (session besoin-carte, [rapport](reports/2026-11-15-besoin-carte.md), suit le
  [plan](derivations/2026-11-15-besoin-carte-plan.md)) :
  - `GET /api/couverture` sert C indexé 2026 (tendanciel `cb`, scénario `cs`, `ecart` = cs/cb − 1, fourchette
    `min`/`max` entre estimateurs survivants) par département, région (rapport des sommes) et France.
  - Estimateurs servis : IDE M1, M2a, M3 ; MK, CD, SF M1, M2a ; PH M1 seul. Central M1. M4 : emplacement désactivé,
    « en attente de validation (P-B4) ».
  - **Couleur de la vue = C scénario − 1** ; l'écart au tendanciel (relatif) va dans l'infobulle, la fiche, l'export.
    Écart au plan : la carte colorée par l'écart seul serait uniforme sans levier.
  - **L23** (`l23=1`, t₀ = 2026) : `s_∞` 0,74 et `τ` 2,4 **mesurés** (P-B6) reportés dans `L23_PARAMS` ; `a` 0,01,
    `k` 1, `μ` 0 **supposés** ; mode expert a ∈ [0 ; 0,05], k ∈ [0,25 ; 1]. N'agit qu'avec M1 (M2a et M3 sans MG).
  - « Actes de MG libérés » = s(t) × 2,6 M injections en consultation (Cour des comptes 2018) : dérivé.
  - Seuil de la fourchette de modèle : 5 % en 2050 (supposé, repris du plan).
  - Besoin mis en cache au démarrage (ne dépend pas des leviers d'offre) ; scénario de population central seulement.
- **Pourquoi :** K1–K6 verts (p95 28,8 ms, n = 60 ; L23 = 0 ⇒ écart 0 ; MG et spécialistes → 400).
- **Ce qui le renverserait :** une mesure de `a` en temps de MG (axe 4) ; M4 validé par P-B4 ; une préférence de
  l'utilisateur·rice pour une carte colorée par l'écart au tendanciel.
- **Non fait :** étape 5 du plan côté `v2/langage/` et `chatbot/` (autre session).

## 2026-11-15 — Carte : le transfert L23 dit en langue courante
- **Décision** (demande de l'utilisateur·rice) : plus de « actes de MG libérés », de « L23 » ni d'« ETP-équivalents » à
  l'écran ni dans l'export. Libellé du levier : « Les pharmaciens vaccinent davantage contre la grippe ». Fiche :
  « vaccinations en moins pour les médecins généralistes, soit le temps de travail d'environ N médecins à temps plein ».
  Les clés de l'API ne changent pas.
- **Pourquoi :** un·e utilisateur·rice sans formation doit tout comprendre.
- **Ce qui le renverserait :** un test de lecture qui montre une phrase encore mal comprise.

## 2026-11-15 — Assistant : outil couverture aligné sur l'API réelle de la carte ; intention « couverture »
- **Décision** (demande de la session besoin-derivation, [rapport](reports/2026-11-15-besoin-assistant.md)) :
  - L'outil `couverture` lit la forme réelle de `/api/couverture` (`fr`, `regs`, `deps`, `fourchette_visible`,
    `l23.transferts`), **remplace** la lecture « contrat du plan » de l'entrée précédente du même jour.
  - Fourchette entre estimateurs montrée **seulement si `fourchette_visible`** ; sinon, pour un estimateur unique
    (pharmaciens), la réponse dit qu'il n'y a pas de fourchette de modèle.
  - Le mot « couverture » dans une question appelle l'outil, avec ou sans L23 ; avec MG ou spécialistes, réponse O2.
  - Date de L23 : l'API applique 2026 ; une autre date est signalée, pas appliquée.
- **Pourquoi :** une seule source pour C (la carte) ; règle d'affichage de l'axe 5 respectée.
- **Ce qui le renverserait :** une API qui accepte `l23_t0` (alors la date compilée serait transmise).

## 2026-11-15 — Carte : la proposition `l23` de l'assistant ou de la phrase règle le levier de vaccination
- **Décision** : une proposition de l'assistant (`carte.l23`, `carte.vue = "couverture"`) ou un transfert L23 compris
  par `/api/interpret` coche « Les pharmaciens vaccinent davantage contre la grippe » et ouvre la vue Couverture,
  seulement au clic « Afficher sur la carte » (même confirmation que les autres leviers).
  `l23_t0` proposé par le compilateur est ignoré : la carte sert t₀ = 2026.
- **Pourquoi :** demande de l'utilisateur·rice ; vérifié dans le navigateur (« couverture des pharmaciens à
  Clermont-Ferrand en 2035 si les pharmaciens vaccinent » → Puy-de-Dôme, 2035, indice 0,98, −0,7 %, même valeur que
  la réponse de l'assistant). Capture : `figures/2026-11-15-besoin-carte-assistant-l23.jpg`.
- **Ce qui le renverserait :** une date de transfert choisie par l'utilisateur·rice (brancher `l23_t0`).

## 2026-11-15 — Assistant : L23 dit en langue courante, comme la carte
- **Décision** (demande de l'utilisateur·rice relayée par la session besoin-derivation ; carte `3c52883`) : libellé du
  levier dans le compilateur et l'assistant : « Les pharmaciens vaccinent davantage contre la grippe ». Effet sur la MG :
  « les médecins généralistes ont moins de vaccins à faire : environ N vaccinations en moins, soit le temps de travail
  d'environ M médecins à temps plein (France entière) ». **Remplace** « actes de médecine générale libérés … ETP-équivalents »
  de l'entrée « outil couverture aligné sur l'API réelle » du même jour. L'interdit de couverture MG (O2) est inchangé.
- **Pourquoi :** même vocabulaire à l'écran, dans l'export et dans l'assistant.

## 2026-11-15 — Assistant de la carte : trois exemples, un par cas d'usage
- **Décision** (demande de l'utilisateur·rice relayée par besoin-derivation) : `ASKEX` passe de 6 à 3 phrases ; l'accueil
  « Définir un scénario » ne montre plus que ces 3 (les cartes contextuelles « former 20 % » et « atteindre +10 % »
  doublaient les exemples 1 et 2) :
  1. leviers → effet : « Former 20 % de kinés en plus et repousser de 2 ans la cessation d'activité en Auvergne-Rhône-Alpes : quel effet en 2040 ? » ;
  2. objectif → possibilités : « Comment atteindre +10 % de densité de pharmaciens en Normandie d'ici 2040 ? » ;
  3. transfert (L23) → couverture : « Si les pharmaciens vaccinent, quelle couverture dans le Puy-de-Dôme en 2035 ? ».
  Les trois sont compris de bout en bout en mode sans IA (mesuré, `v2/langage/mesures/2026-11-15-assistant-trois-exemples.txt`) ;
  mode IA non vérifié (pas de clé). L'assistant dit « demande de soins de ville », plus « besoin ».

## 2026-11-15 — Carte : libellés du module de besoin alignés sur « demande de soins de ville »
- **Décision** (fusion de `besoin-assistant`, qui contient `besoin-carte-api`, avec l'accord de l'utilisateur·rice) :
  la carte applique la règle de libellé de l'entrée « périmètre libéral de DAMIR ».
  - **Indicateur, infobulle, fiche, export CSV :** « Couverture de la demande de ville » ; définition « offre privée
    rapportée à la demande de soins de ville estimée (recours remboursé hors hôpital public, pas le besoin de toute
    la population) ». Il n'y a plus de « besoin » dans les libellés affichés.
  - **Norme de l'estimateur :** elle reste affichée telle que l'estimateur la déclare, précédée de « (norme
    déclarée) ».
  - **Assistant :** il était déjà aligné, « demande de soins de ville » dans `chatbot/`.
  - **Exemples de l'assistant :** 3, un par cas d'usage (commit `5f264e3`).
- **Vérifié :**
  - `tests/couverture.py` : K1 à K6 passent, p95 18,5 ms ;
  - `besoin.tests` : 15/15 ;
  - rendu dans le navigateur (pharmaciens, France, 2050 : 1,01) ;
  - `jumeau.check` : seul C15 (temps) échoue, sous charge.
- **Corrigé à la fusion :** `Home.md` de la branche `besoin-assistant` contenait des marqueurs de conflit commités ;
  ils sont retirés, et les trois lignes du journal sont gardées.

## 2026-11-15 — Grain territorial : on s'arrête au département (pas de grain communal)
- **Décision** (utilisateur·rice, après la recette de l'application, constat P1-5 : « pas de grain communal, on
  s'arrête bien au départemental ») :
  - les sorties du jumeau et du module de besoin s'affichent **au département, à la région et au national**
    seulement ;
  - pas de commune ni de groupe de communes dans la carte, l'API ou l'assistant ;
  - les calculs internes qui passent par la commune restent permis (zonage conventionnel, M4 en 2SFCA, tables
    communales), mais leurs résultats ne sont publiés qu'agrégés au département ;
  - « Clermont-Ferrand » se lit « Puy-de-Dôme », comme l'assistant le fait déjà.
- **Remplace :** « Les modèles tournent à toutes les granularités, jusqu'à la commune » (2026-11-14), dans
  `CLAUDE.md`, `docs/lab/profile.md`, `v2/ROADMAP.md` et Home. Ces mentions sont barrées ou annotées, pas effacées.
  Prolonge « affichage au département » (K5 non confirmé, N12).
- **Pourquoi :**
  - projection communale non confirmée (K3 à K5, N10 à N12) ;
  - plus de la moitié des cellules commune × âge valent une personne (audit RGPD) ;
  - P-B4 : M4 ne reproduit pas l'APL à la commune, alors que l'accord est de 0,98 au département.
- **Conséquence :** le constat P1-5 de la recette (`2026-11-15-uat-application`) est clos par décision, pas par
  correction. Le parcours ARS commence au département.

## 2026-11-15 — Pas de « mode simple » pour l'élu·e : l'assistant IA en tient lieu
- **Décision** (utilisateur·rice, après la recette, constat P1-6 : « le mode simple pour l'élue c'est stale, on a
  l'assistant IA ») :
  - aucun mode simple séparé n'est construit ;
  - l'élu·e passe par l'**assistant de simulation**, qui traduit une phrase en leviers et répond en langue courante.
    C'est la suite de la décision du 2026-11-14, « L'agent conversationnel devient l'interface principale ».
- **Remplace :** le « mode simple » des personas (`CLAUDE.md`, règles maison, annoté) et la partie « mode simple »
  du constat P1-6.
- **Reste ouvert** (partie de P1-6 non couverte par cette décision) : le jargon de méthode (M1, DCIR, P-B4, L23,
  s∞…) visible dans la fiche et dans l'assistant. On le garde en P2, à reformuler en langue courante ou à replier
  dans un détail.

## 2026-11-15 — Carte : la fiche montre la couverture de l'année du curseur seulement
- **Décision** (demande de l'utilisateur·rice) : la fiche du territoire n'affiche plus la ligne fixe « Couverture de la
  demande de ville 2035 ». Elle montre seulement l'année du curseur ; l'export suit la même règle. L'étiquette de
  l'indicateur « Couverture 2040 » retrouve son espace (`&nbsp;`, comme « Densité ») : le bouton en flex supprimait
  l'espace avant l'année.
- **Pourquoi :** la ligne 2035 doublait celle du curseur ; une seule année se lit d'un coup d'œil.
- **Vérifié :** dans le navigateur (Puy-de-Dôme, pharmaciens, curseur sur 2040 : une ligne, 1,01).

## 2026-11-15 — Transferts hypothétiques admis dans l'assistant, étiquetés « hypothèse de l'utilisateur » ; O2 précisé : cible seulement
- **Décision** (tâche de la session v2, relayée à besoin-axe5-sensibilite ; [plan](derivations/2026-11-15-transfert-hypothetique-plan.md),
  [rapport](reports/2026-11-15-transfert-hypothetique.md)) :
  - **Forme :** celle de L23, généralisée à une source et à une cible quelconques. `GET /api/couverture` accepte
    `tr_src`, `tr_cible`, `tr_a` [0 ; 0,5], `tr_sinf` [0 ; 1], `tr_k` [0,1 ; 3], `tr_tau` [0,1 ; 20] et
    `tr_t0` [2026 ; 2050]. L'opérateur s'applique après L23, sur le besoin en cache.
  - **Profession affichée :** `prof` doit être la cible ou la source, sinon 400.
  - **Demande de la source :**
    - une des 5 : son propre besoin ;
    - MG : M1, niveau placeholder ;
    - spécialistes : M0, placeholder.
  - **Défauts, tous « supposé (hypothèse de l'utilisateur) » :** a 0,10, s∞ 1, k 1, τ 2,4 (forme de L23,
    empruntée), t₀ 2026.
  - **Lecture de la phrase :**
    - « p % des <acte> de Y » : s∞ = p, et a est balayé sur {5, 10, 20 %} ;
    - « p % de la demande de Y » : a = p, balayé sur {p/2, p, 2p}.
  - **Réponse de l'assistant :**
    - jamais un chiffre unique ;
    - source, cible et paramètres réaffichés avec leur statut ;
    - elle dit pourquoi ce n'est pas un levier de la carte : ni volume d'acte ni part du temps publiés en données
      ouvertes.
  - **L23 reste le seul transfert sourcé**, inchangé.
  - **O2 précisé :** la MG et les spécialistes sont refusés comme **cible** de l'indice (`tr_cible` ⇒ 400 ;
    « couverture des généralistes » ⇒ refus). Ils sont admis comme **source**.
    - Cela corrige le faux refus constaté en recette sur la phrase d'exemple : le mot « généralistes » déclenchait O2.
    - Les transferts L23 qui citent les médecins en profitent aussi.
  - **Carte :** aucun nouvel interrupteur, aucun bandeau. La carte ne propose pas d'afficher un transfert
    hypothétique, puisqu'elle n'a pas ce levier.
- **Pourquoi :**
  - demande de l'utilisateur·rice : que l'assistant « essaie » un transfert arbitraire ;
  - une seule source pour C, la carte : l'alternative calculée dans la passerelle est rejetée, car elle perd le
    département et ne se vérifie pas contre L23.
- **Vérifié :**
  - générique MG → PH aux paramètres de L23 = `l23=1` (écart 0,0) ;
  - L23 identique octet pour octet ;
  - K1–K7 verts, p95 24,7 ms ;
  - compilateur 10/10 sur des cas écrits avant le code, jeux existants inchangés ;
  - chatbot 50/51 (le 51ᵉ exige un arbre propre ; vert après nettoyage) ;
  - navigateur, mode sans IA.
- **Ce qui le renverserait :**
  - un volume d'acte ou une part du temps publiés : le transfert deviendrait un levier sourcé, comme L23 ;
  - un niveau mesuré de la demande MG, qui changerait l'ampleur.
- **Non fait :**
  - mode IA non vérifié (pas de clé) ;
  - pas de bandeau dans la carte.

## 2026-11-15 — Carte : familles de leviers repliées au chargement ; retour à la France sans écran intermédiaire
- **Décision** (demande de l'utilisateur·rice) :
  - Les six familles du panneau Scénario (Former, Attirer, Réguler, Retenir, Transférer des tâches, Hypothèses de
    contexte) sont **repliées à l'arrivée**. Le titre de chaque famille porte toujours l'effet du réglage dès qu'un
    levier est modifié. **Remplace** « quatre familles ouvertes au chargement » (entrée du 2026-11-14), choisie alors
    parce que, repliés, « les curseurs semblaient avoir disparu ». Choix confirmé par l'utilisateur·rice, qui avait
    été averti·e de cette raison.
  - Bouton « Vue France entière » : la fiche du territoire reste affichée, estompée, jusqu'à l'arrivée des chiffres
    nationaux, puis passe à « France ». Avant, elle passait par une fiche d'attente « France entière — Chargement… »
    pendant environ 200 ms. Si les chiffres nationaux n'arrivent pas, la fiche d'attente revient au bout de 4 s.
- **Vérifié** (navigateur, panneau masqué, dessin de la carte neutralisé) :
  - 6 familles avec `aria-expanded=false` ;
  - Puy-de-Dôme → estompée → France en 230 ms, sans titre intermédiaire.
- **Ce qui le renverserait :** un test de lecture où les curseurs repliés ne sont pas trouvés.

## 2026-11-15 — Transfert hypothétique : niveau MG et spécialistes mesuré, balayage dans la passerelle, bandeau dans la carte
- **Décision** (demande de l'utilisateur·rice : « les 3 go », sur les suites du rapport transfert hypothétique) :
  - **Niveau de la demande de la source.** Pour le transfert hypothétique seulement, la demande des MG et des
    spécialistes est ramenée, à l'année de référence, à l'**effectif libéral mesuré** (ameli, France, 1ᵉʳ janvier
    2025) : 56 005 médecins généralistes, 57 346 spécialistes. La répartition par territoire et par âge reste celle
    de M1 (MG) ou de M0 (spécialistes).
    - **Corrige ma proposition** « Open DAMIR » : DAMIR compte des actes, alors que le transfert raisonne en temps de
      professionnels, comme les cibles (1 professionnel = 1 temps plein).
    - Facteur MG 0,911 contre l'ancienne valeur provisoire.
    - **L23 garde le niveau de M1** : levier sourcé déjà validé, laissé inchangé ; l'alignement est au ledger.
    - K7 compare désormais le transfert générique avec `a` divisé par ce facteur à `l23=1` (écart 0,0).
  - **Balayage dans la passerelle**, quel que soit le mode.
    - Avec `transfert`, l'outil `couverture` renvoie `balayage_a` : 5, 10 et 20 % si `a` n'est pas donné, sinon
      a/2, a et 2a. Le point médian sert de réponse principale.
    - Le mode sans IA fait un seul appel au lieu de trois.
    - Consigne au modèle (schéma et prompt) : « p % des <acte> » donne s_inf = p/100, sans `a`.
  - **`l23` n'est plus actif par défaut** dans l'outil `couverture` : il est demandé seulement pour la vaccination.
  - **Bandeau dans la carte.**
    - La proposition de l'assistant porte les `tr_*` du point médian, et la carte les envoie à `/api/couverture`.
    - Un bandeau « Transfert hypothétique (paramètres de l'utilisateur) » s'affiche, avec « Retirer », tant que la
      profession affichée est la cible ou la source.
    - **Remplace** « aucun bandeau » de l'entrée « transferts hypothétiques admis » du même jour.
- **Pourquoi :** en mode IA, mesuré avant correction, la phrase d'exemple donnait un chiffre unique et lisait
  « 10 % des renouvellements » comme 10 % de toute la demande MG : −1,7 %, 10 fois trop.
- **Vérifié :**
  - mode IA (claude-haiku-5-5), 6 questions ([mesures](../../langage/mesures/2026-11-15-transfert-hypothetique-mode-ia.txt)) :
    - exemple : s_inf 0,1 et a balayé, −0,08 / −0,17 / −0,34 %, mêmes valeurs qu'en mode sans IA ;
    - « couverture des généralistes » : O2 dit, indice des infirmiers seulement ;
    - spécialistes → kinés : balayé ;
    - L23 : inchangé, −0,7 % ;
  - carte : le bandeau applique la proposition (−0,17 %, D63, 2035) et « Retirer » remet l'écart à 0 ;
  - K1–K7 verts, p95 23,5 ms ;
  - chatbot 50/51 avant nettoyage (le 51ᵉ exige un arbre propre).
- **Ce qui le renverserait :** une durée publiée des actes de la MG (a deviendrait mesurable) ; un choix
  d'aligner L23 sur le niveau mesuré.

## 2026-11-15 — UAT de l'application : assistant testé sans IA seulement ; constats notés, rien corrigé
- **Décision** (session uat-application, [rapport](reports/2026-11-15-uat-application.md)) : l'assistant est recetté
  en mode sans IA (glossaire), sur une passerelle et un chatbot propres à la branche (ports 8782, 8783). Le mode IA
  n'est pas appelé : une clé existe, mais un appel payant demande l'accord de l'utilisateur·rice. Conformément à la
  consigne, aucun constat n'est corrigé pendant la recette ; les 6 P1 vont au ledger.
- **Pourquoi :** consigne de la recette (« ne corrige rien ») ; règle de confirmation avant toute dépense.
- **Ce qui le renverserait :** un accord pour quelques appels Haiku (ligne du ledger « UAT en mode IA »).

## 2026-11-15 — L23 : la montée en charge part de la part déjà atteinte (P1-4) ; niveau de la demande MG mesuré dans M1 ; écart au protocole P-B6
- **Décision** (accord de l'utilisateur·rice : « 1 mais après la fusion », règle fixée avant la mesure : au-delà de
  20 % d'effet gonflé, corriger le double compte et le niveau ensemble ; enregistrée avant tout changement de code) :
  - **Constat mesuré (P1-4 de la recette).**
    - La part officinale nationale vaut déjà **0,687 en 2025-26** (IQVIA ÷ Open Medic, P-B6, mesuré) et 0,670 en
      2024-25.
    - La courbe ajustée (t₀ = 2019) donne s(2026) = 0,698 (dérivé).
    - L23 rejouait toute la montée (0 → 0,74) à partir de 2026 : effet **19 fois** trop grand en 2035
      (0,723 contre une marge de 0,038 ; dérivé).
    - L'année de base contient déjà l'officine : la demande des pharmaciens est calée sur leur offre de 2026 et le
      profil de la MG sur Open DAMIR 2025.
  - **Correction.**
    - L23 garde la courbe mesurée : s∞ 0,74, τ 2,4, **t₀ = 2019**.
    - Il n'applique que **ce qui reste au-delà de la part atteinte à l'année de base** :
      `s_eff(t) = max(0, s(t) − s(2026))`.
    - Nouveau champ `s_deja` de `Transfert`, à 0 par défaut : les autres transferts, dont l'hypothétique, ne changent
      pas.
  - **Niveau de la demande MG dans M1.**
    - r̄_MG est calé pour que la demande nationale de la MG à l'année de base égale l'**effectif libéral mesuré**
      (ameli, 1ᵉʳ janvier 2025 : 56 005, mesuré).
    - Il remplace le placeholder de 0,9 ‰ (supposé), plus haut d'environ 10 %.
    - La répartition par âge reste celle d'Open DAMIR.
  - **Écart au protocole P-B6** (gelé, horodaté).
    - Le protocole mesure s(t) avec t₀ = 2019 et ne fixe pas son application au besoin ; il est inchangé.
    - Ce qui change, c'est l'application dans le module de besoin : t₀ = 2019 et soustraction de s(2026), au lieu de
      t₀ = 2026.
    - s∞ et τ ne sont pas réajustés.
- **Pourquoi :**
  - effet gonflé de +1 830 %, bien au-delà du seuil de 20 % fixé avant la mesure ;
  - les deux corrections changent les chiffres de L23 : une seule fois, un seul passage de K4.
- **Effet attendu (dérivé, à vérifier) :** l'écart de couverture des pharmaciens avec L23 passe d'environ −0,7 % à
  environ −0,04 %. Les « vaccinations en moins pour les généralistes » baissent dans la même proportion.
- **⚑ Ce qui le fragilise :**
  - la marge restante (≈ 0,04) est plus petite que l'erreur type de s∞ (± 0,07) : son signe même n'est pas sûr ;
  - la grille de sensibilité (`v2/sensibilite/besoin/grille.py`) applique L23 avec t₀ = 2019 sans soustraire
    s(2026) : non corrigée ici, inscrite au ledger.
- **Ce qui le renverserait :** une année de base de la demande antérieure à 2019 (la soustraction serait alors de
  trop) ; un nouvel ajustement de P-B6 avec un s∞ nettement plus haut.

## 2026-11-15 — Erratum P1-4 propagé : grille de l'axe 5 relancée, rapports annotés
- **Fait** (rappel de l'utilisateur·rice, relayé par la session transfert-hypothetique : « corrige l'erreur L23
  partout où elle reste ») :
  - `v2/sensibilite/besoin/grille.py` appelle `l23(2026, …)` (constante `L23_REF`) au lieu de `l23(2019, …)` ;
  - la grille des pharmaciens est relancée ; les sorties des quatre autres professions sont gardées, puisqu'elles ne
    dépendent pas de L23 et que leurs grilles brutes ne sont pas versionnées ;
  - résultat : L23 en 2050, E 0,0002 et R 0,002, au lieu de 0,004 et 0,05 ; verdict inchangé, non distinguable.
- **Encadrés « Erratum 2026-11-15 (P1-4) »** en tête des rapports, anciens chiffres conservés et annotés :
  - `besoin-carte`, `besoin-assistant`, `uat-application`, `besoin-axe5-sensibilite` ;
  - trois fichiers de mesure de `v2/langage/mesures/` ;
  - trois lignes du journal de Home.
- **Article du besoin (`v2/papers/besoin/`)** : la phrase sur L23 est remplacée par les nouveaux chiffres.
- **Hors champ :** `besoin-axe1-fiches` ne cite pas l'effet de L23, seulement s∞ et τ, qui restent valables.

## 2026-11-15 — Corrections de la recette : méthode repliée, temps de médecin dit à part, O2 dans le texte de périmètre
- **Décision** (session uat-corrections, tâche de la session besoin-derivation ; [rapport](reports/2026-11-15-uat-corrections.md)) :
  - **Jargon (reste de P1-6) :** dans la fiche, la légende, le panneau « Transférer des tâches » et l'assistant, le texte
    visible par défaut ne cite plus de code (M1, M2a, M4, DCIR, P-B4, C1, L23, s_inf, tau…). Les codes, la norme déclarée
    de l'estimateur, les sources des paramètres et le nom technique du modèle passent dans un détail replié
    (« Méthode (détail) », « Sources et références », détail du « Calcul »). Les clés de l'API ne changent pas.
  - **Paramètres de la vaccination en officine** nommés en clair (« Part du temps des médecins généralistes consacrée à ce
    vaccin », « Temps du pharmacien pour un vaccin, rapporté à celui du médecin »…), nombres au format français ; le code
    reste entre parenthèses dans l'export.
  - **Temps de médecin libéré (P2-5) :** **remplace** « environ N vaccinations en moins, soit le temps de travail d'environ
    M médecins à temps plein » (entrées « Carte : le transfert L23 dit en langue courante » et « Assistant : L23 dit en
    langue courante » du même jour). Les deux nombres sont indépendants (N = s × actes, M = s × a × demande MG) : la fiche,
    l'export et l'assistant disent « N vaccinations en moins (France entière), au-delà de la part déjà faite en pharmacie en
    2026 », puis, à part, « temps de travail libéré : environ M médecins à temps plein, un ordre de grandeur qui dépend
    d'une part de temps supposée, pas du nombre de vaccinations ».
  - **Vaccination en officine dans les textes « pas dans le modèle » (P1-2) :** elle n'y figure plus ; la page dit qu'elle
    change la couverture de la demande des pharmaciens, pas le nombre de professionnels. Le compilateur la garde dans
    `non_modelise` (décision « L23 compilé en transfert », jeux à l'aveugle) ; c'est l'affichage qui la retire quand le
    transfert est compris, comme l'assistant le faisait déjà.
  - **Fourchette entre estimateurs (P2-1) :** affichée seulement si `fourchette_visible` (seuil de 5 %), dans l'infobulle,
    la fiche et la légende, comme l'assistant.
  - **Légende de la vue Couverture (P2-7) :** graduée en indice (unité « indice »), plus en %.
  - **Comparaison en vue Couverture (P1-1) :** colonne « Couverture · écart tend. », lue dans `/api/couverture` pour chaque
    territoire comparé (département, région, France), « — » si absente.
  - **Texte de périmètre (P2-8) :** MG et spécialistes « non projetés ; admis seulement comme source d'un transfert de
    tâches, jamais comme profession projetée ni pour un indice de couverture (règle O2) ». **Remplace** « spécialités
    prévues en phase 2 » dans la passerelle, `correspondances.yaml` et le glossaire.
  - **Badge de levier (P2-11) :** troisième état « effet non mesurable », comme l'export.
  - La vaccination en officine compte comme levier modifié dans le résumé du panneau ; « Revenir à la tendance » la
    désactive (P2-6).
  - `/api/couverture` avec une profession inconnue : 400 « profession inconnue », distinct du refus O2 (P2-12).
  - L'export reprend le libellé du modèle servi (`/api/agent/etat`, servi aussi quand le chatbot est absent), le même que
    l'assistant (P2-9).
- **Pourquoi :** recette du 2026-11-15 (P1-1 à P1-3, P1-6 en P2) ; le texte visible doit se lire sans connaître le
  projet ; l'Administration garde le détail en un clic.
- **Ce qui le renverserait :** un test de lecture qui montre qu'un libellé en clair est mal compris, ou une demande de
  l'Administration d'avoir les codes visibles par défaut.

## 2026-11-15 — Pas de bouton « A+ » : le test R25 est retiré de la recette de la carte
- **Décision** (utilisateur·rice, constat P2-14 de la recette : « Retirer R25 ») :
  - le bouton « A+ » (texte agrandi), disparu de la carte, n'est pas rétabli ;
  - le test R25 de `v2/prototype-carte/recette.mjs` est retiré, avec un commentaire qui renvoie à cette décision ;
  - l'agrandissement passe par le zoom du navigateur.
- **Pourquoi :** choix d'interface de l'utilisateur·rice. Le test échouait sur une fonction qui n'existe plus.
- **Ce qui le renverserait :** un retour d'accessibilité (RGAA) qui demande un réglage de taille de texte dans la page.

