# Jumeau numérique de l'offre de soins libérale

> Hackathon santé publique : **« Anticiper l'évolution de l'offre de soins »**

Un projet de recherche quantitative. On simule des **politiques publiques nationales** et on mesure
leur effet sur le nombre de professionnels de santé **libéraux** (hors médecine générale) jusqu'en
**2050**, du département au national (pas de grain communal affiché, décision du 2026-11-15). Chaque politique est un réglage
d'hyperparamètres **sourcés** : places en formation, âge de départ, diplômés à l'étranger, régulation
de l'installation, etc. Chaque résultat est **reproductible, falsifiable et interprétable**, sans
boîte noire.

## Sommaire

- [Démarrer en 5 minutes](#démarrer-en-5-minutes)
- [Le problème](#le-problème)
- [Ce que fait l'outil](#ce-que-fait-loutil)
- [État des travaux](#état-des-travaux)
- [Données et méthode](#données-et-méthode)
- [Architecture](#architecture)
- [Reconstruire les données](#reconstruire-les-données)
- [Confidentialité des données](#confidentialité-des-données)
- [Limites connues](#limites-connues)
- [Feuille de route](#feuille-de-route)

## Démarrer en 5 minutes

Prérequis : Python 3.12+ et [uv](https://docs.astral.sh/uv/). **Aucune donnée à télécharger** : les
données traitées (données ouvertes, ≈ 37 Mo) sont dans le dépôt.

```bash
git clone https://github.com/progdinh/hackathon_acces_soins.git
cd hackathon_acces_soins
uv sync
uv run python v2/prototype-carte/server.py
```

Puis ouvrir **http://localhost:8767**. Le serveur met une dizaine de secondes à charger les
5 professions ; il affiche `prêt : http://localhost:8767` quand c'est fait.

**Un seul port.** La carte démarre elle-même, en processus séparés et internes (127.0.0.1), la passerelle en lecture
seule et le chatbot de `chatbot/` (code de Juliette Konop). Le bouton « Assistant de simulation » leur relaie les
questions par `/api/agent` : il n'y a rien d'autre à lancer, et tout passe par http://localhost:8767. Le chatbot
explique les résultats sans rien calculer ; chaque nombre vient du jumeau et est vérifié.

`.env` (à la racine, ignoré par git) contient `ANTHROPIC_API_KEY=sk-ant-...` ; la carte ne la transmet qu'au processus
du chatbot, jamais au navigateur. **Sans clé**, le chatbot répond quand même, avec le glossaire de l'équipe (sans IA).
`CARTE_SANS_ASSISTANT=1` lance la carte seule ; le panneau indique alors que l'assistant n'est pas disponible. Le
contrôle du lexique neutre (`v2/agent/garde_fous.py`) s'applique à chaque réponse.

Déjà cloné ? `git pull` puis `uv sync` suffisent. Si une erreur parle de `data/raw/` ou d'un fichier
`.parquet` absent :

```bash
git pull                                        # les données traitées sont commitées depuis le 2026-11-14
uv run python v2/data/manifest.py --check       # doit afficher « OK »
```

Ne lancez **pas** `sante.load` ni les `v2/data/build_*.py` pour démarrer : ils servent seulement à
[reconstruire les données](#reconstruire-les-données) à partir des fichiers bruts (≈ 3,6 Go, non
commités).

**Vidéos de présentation** (Remotion, voir `v2/video/README.md`), commitées :
- **V2** (60 s, sans voix ni musique) : [`v2/video/out/pitch-v2.mp4`](v2/video/out/pitch-v2.mp4). Elle suit un seul cas d'usage : un conseiller ministériel règle +20 % de places en formation de kinés en France, puis lit l'effet dans la Manche à 2036, 2046 et 2050. Chaque horizon donne l'effectif, l'écart au tendanciel, la densité et la fourchette.
- **V1** (57 s, voix off IA) : [`v2/video/out/pitch.mp4`](v2/video/out/pitch.mp4).

```bash
cd v2/video && npm install
npm run capture:v2 && npm run render:v2    # -> v2/video/out/pitch-v2.mp4 (la carte doit tourner, port 8767)
npm run render                             # V1 -> v2/video/out/pitch.mp4
```

## Le problème

Former un professionnel de santé prend de 3 à 10 ans. Une décision prise aujourd'hui (quotas,
régulation de l'installation, âge de départ) ne produit son plein effet que bien plus tard, et souvent
ailleurs que là où on l'attendait. Les projections publiées (DREES, Insee) sont nationales et
tendancielles. Il manque un outil qui dise, **pour un territoire donné**, ce qu'une politique change
et avec quelle incertitude.

Professions couvertes : **sages-femmes, chirurgiens-dentistes, pharmaciens,
masseurs-kinésithérapeutes, infirmiers**. Les spécialités médicales (cardiologie, dermatologie,
ophtalmologie) sont une amélioration possible (décision du 2026-11-15) ; elles ne sont plus un jalon du
plan. Elles peuvent servir de profession source d'un transfert de tâches, sans projection.

**« Libéral » au sens large.** Ici, « libéral » désigne **tout le secteur privé**, lucratif ou non :
libéraux et mixtes, pharmaciens adjoints d'officine, salariés de cliniques privées, industrie. Tout
employeur public est exclu. C'est plus large que le sens habituel du RPPS ou d'ameli (exercice
indépendant), et chaque sortie le rappelle.

## Ce que fait l'outil

**La carte de décision** (`v2/prototype-carte/`, http://localhost:8767) : trois colonnes fixes, habillage
[DSFR](https://www.systeme-de-design.gouv.fr/) 1.15.4 (Système de design de l'État, copie locale dans
`v2/prototype-carte/dsfr/`, licence Etalab 2.0, réservé aux sites de l'État). La carte garde sa gamme bistre ↔ pétrole,
jamais rouge ni vert. Aucun build ni framework : HTML, CSS et JavaScript, comme avant. Le scénario est à gauche : la profession (liste déroulante) et l'année affichée
en tête, puis les leviers par famille. La carte est au centre, avec le fil d'Ariane posé dessus. À droite, le panneau « Résultat » : la fiche du
territoire, puis cinq modes de visualisation (Graphique à courbes superposables, dont effectif + âge moyen et, pour
les infirmiers, le taux d'installation des diplômés ; Pyramide des âges ; Flux ; Comparer ; Données). La carte va de
l'orange (en dessous de la moyenne nationale) au vert (au-dessus), en couleurs du DSFR. L'assistant de simulation
s'ouvre dans une fenêtre par trois boutons : « Aide au scénario », « Aide à la lecture » et l'icône en bas à droite de
la carte. Les deux panneaux latéraux se replient en une barre bleue (un clic la déplie), et la carte s'ouvre centrée sur la France.
L'assistant et le compilateur comprennent la vaccination en officine (L23) : effectif inchangé dans le modèle,
indice de couverture des pharmaciens (base 2026) lu sur `/api/couverture` ; seule la part de vaccinations au-delà de
celle déjà faite en officine en 2026 agit (correctif P1-4 : effet 2050 de −0,03 % au lieu de −0,7 %). Pas de
couverture pour la médecine générale sur la carte ; dans l'assistant, l'option « effectivité » (décision O3) dit si le
transfert soulage les généralistes sans trop peser sur les pharmaciens, avec une offre de généralistes supposée constante
([rapport](v2/docs/lab/reports/2026-11-15-besoin-assistant.md)).

- **Carte des départements et des régions**, au choix : variation de l'effectif 2026 → 2050, écart au tendanciel,
  ou **densité 2050 pour 100 000 habitants** (Insee Omphale 2022). Sous la légende, « Comment lire cet indicateur ? » déplie sa
  définition (facultatif, fermé par défaut).
  La carte est colorée par département ; un clic ouvre le département, et sa région s'ouvre par le fil
  d'Ariane ou la recherche. Recalcul après chaque réglage en
  environ 50 ms (mesuré).
- **Curseur d'année** (2026 → 2050, pas annuel, 2050 par défaut, bouton ▶ pour faire défiler) : carte,
  légende, résumé, fiche et comparaison suivent l'année choisie. Toutes les années arrivent en un seul
  appel (environ 100 ms) : bouger le curseur ne relance pas le calcul. L'année est gardée dans le lien.
- **9 leviers en 4 familles** (former, attirer, installer, retenir), chacun avec son délai d'effet et
  son niveau de preuve (sourcé ou supposé). Une famille = un accordéon, ouvert au chargement : curseur
  principal, délai et source, puis réglages fins ; son titre affiche l'effet du réglage. Les hypothèses de
  contexte (population, activité) forment un cinquième accordéon, replié.
- **Une phrase en langage naturel** (« augmenter de 20 % les places de kinés dans le Puy-de-Dôme »)
  devient un réglage des leviers. Le compilateur est déterministe et à glossaire (`v2/langage/`) : il
  traduit, il ne calcule jamais. Environ **77 % des phrases** sont entièrement bien traduites sur les jeux 5 et 6 écrits à
  l'aveugle, et **70 %** sur le seul jeu resté à l'aveugle après les réglages. Un écran montre toujours ce qui a été compris et ce qui n'est pas dans
  le modèle, et rien n'est appliqué sans confirmation.
- **Questions en français** (bouton « Questions », facultatif) : prototype qui relaie vers le chatbot de
  `chatbot/` (Claude Haiku 5.5 avec une clé, glossaire sans clé), avec le contexte affiché (profession,
  territoire, leviers, année). Il explique l'écart par flux, le délai d'effet, la fourchette et le statut des
  leviers ; il **ne calcule rien**, et les nombres non rattachés à un résultat sont corrigés puis bloqués.
  **Assistant de simulation** (interface de chatbot, scénarios à essayer) : on y propose une politique ou un **mélange de
  politiques** ; la réponse dit ce que ça change concrètement, la part de chaque levier et leur interaction, et nomme le
  modèle servi (C1, cohortes bayésiennes, MAPE 7,73 % à 5 ans ; A0, stock-flux à taux départementaux, si `JUMEAU_MODELE=A0`). Proposer « former 20 % de kinés en plus en Auvergne d'ici 2035 » : le bouton
  « Afficher ce scénario sur la carte » règle profession, territoire, leviers et année. Les grandeurs sont dites dans un
  **vocabulaire fixe calculé par le code** (« légère hausse », « incertitude modérée », « moyen terme », « proche de la
  moyenne nationale » ; seuils dans `v2/docs/lab/lexicon.md`), vérifié comme les nombres. Mesuré sur 22 questions avec
  Haiku 5.5 : 54 qualificatifs, 0 non conforme ; 21/22 réponses entièrement ancrées ; hors périmètre 5/5 ; médiane 8 s
  (`v2/agent/score_chatbot.txt`). Interface principale ; mise en page en attente de l'équipe UX. `v2/agent/` (premier
  agent) est gelé ; seuls son contrôle du lexique et ses scripts de mesure servent.
- **Hypothèses de contexte** : scénario de population Insee (central, bas, haut) et activité moyenne
  par professionnel (équivalents temps plein, supposée).
- **Fiche par territoire** : effectif 2026, 2050, écart au tendanciel, repères 2030 / 2035 / 2040 / 2050
  avec fourchette et densité, écart décomposé par flux, export CSV avec sources, millésimes, hypothèses et
  version du code.
  - Sans territoire ouvert, la fiche montre la France.
  - Avec un territoire ouvert, une bascule « territoire / France entière » donne les chiffres nationaux.
- **Mode expert** : écart par flux et par année, chaque levier avec sa valeur, son paramètre, son délai,
  son statut et sa source, trois scénarios épinglés côte à côte, export JSON.

La recette iso-fonctionnelle vérifie chaque fonction dans Chrome headless, sans dépendance. Elle a besoin de Node 22 ou
plus et d'un serveur lancé sur une version à jour :

```bash
node v2/prototype-carte/recette.mjs --option1   # 45 contrôles sur 46 ; R25 (bouton A+) absent de cette mise en page
```

L'ancienne carte à panneaux flottants a été remplacée le 2026-11-14. Elle reste dans l'historique git :
`git show 17842ea:v2/prototype-carte/index.html`.

**Le jumeau** (`v2/jumeau/`), sur lequel la carte est branchée :

- **Un état, des flux, des scénarios.** Chaque année, des modules (vieillissement, sorties, entrées,
  formation, diplômés étrangers, régulation…) lisent l'état et écrivent des flux. Un registre garde
  chaque flux, si bien que tout écart s'explique par ses composantes.
- **Les leviers sont des événements datés** : « places × 1,2 à partir de l'année de décision + durée
  des études », « régulation activée dans telle liste de géocodes ». Un scénario se sérialise en JSON
  et se rejoue à l'identique.
- **Régulation par géocodes.** En zone « remplacement d'un départ seulement », les entrées ne peuvent
  pas dépasser les sorties. L'excédent est déplacé (vers le salariat, une zone voisine ou hors de la
  profession), jamais perdu ni créé.
- **18 critères d'acceptation**, chacun capable d'échouer sur le code d'avant correction, après trois
  revues adversariales : `PYTHONPATH=v2 uv run python -m jumeau.check`.
- **Rapide** : 15 ms par scénario au département, 1,1 s pour 5 professions à la commune (mesuré).

## État des travaux

| Axe | Contenu | État |
|---|---|---|
| 0. Jumeau | État unique (profession × secteur × territoire × sexe × âge), modules de flux en plug-ins, scénarios datés | ✅ 18 critères sur 18, 3 revues adversariales |
| 1. Hyperparamètres | Fiches sourcées : régulation conventionnelle, filières en pharmacie, spécialisation en odontologie, abandon en IFSI… | ✅ fiches relues en texte intégral le 2026-11-15 : 20 confirmées, 8 corrigées, 1 introuvable, aucune valeur du code changée ([rapport](v2/docs/lab/reports/2026-11-15-axe1-relecture-sources.md)) |
| 2. Méthodes | Battre le stock-flux sans boîte noire | ✅ cohortes bayésiennes : MAPE dép. 7,73 % contre 8,68 % ; projection communale (K3 à K5) non confirmée, affichage au département |
| 3. Validation | Protocoles pré-enregistrés, gelés par SHA-256 (N1 à N12) | ✅ exécutés en grande partie ; dépôts à noter sur les données 2027 |
| 4. Données | Public / privé, registre de 30 événements datés, zonage par commune, grain communal | ✅ |
| 5. Sensibilité | Morris puis Sobol : quels paramètres déplacent l'effectif en 2050 ? | ✅ en 2050, la décision pèse plus que l'incertitude pour IDE, MK, SF |
| Carte | Leviers, phrase, densité, mode expert, export | ✅ démontrable |
| Besoin → carte | Vue « Couverture » (indice C, référence 2026 = 1, fourchette M1/M2a/M3), levier L23 « vaccination en officine » de bout en bout ; M4 non servi (P-B4 échoue, OSRM compris) | ✅ 6 critères sur 6 ; `/api/couverture` 28,8 ms au 95ᵉ centile (n = 60) |
| Transferts hypothétiques | L'assistant simule « X prennent p % de <acte> de Y » (forme de L23, `tr_*` sur `/api/couverture`), balayé sur a (mode IA et sans IA), étiqueté « hypothèse de l'utilisateur », bandeau dans la carte ; niveau MG et spécialistes mesuré (ameli 2025) ; O2 refuse la MG et les spécialistes en cible seulement | ✅ 7 critères sur 7 ([rapport](v2/docs/lab/reports/2026-11-15-transfert-hypothetique.md)) |
| Phase 2 | Cardiologie, dermatologie, ophtalmologie | amélioration possible (plus au plan depuis le 2026-11-15) |

**Rapport technique pour la reprise** (document d'entrée unique : données, paramètres, jumeau, méthodes,
validation, sensibilité, interface, conformité, menaces à la validité, questions ouvertes, reproductibilité) :
`v2/papers/rapport-technique/` (`tectonic main.tex`). L'ancien article de synthèse reste dans
`v2/papers/synthese/`.

## Données et méthode

| Donnée | Producteur | Période | Usage |
|---|---|---|---|
| Démographie des professionnels de santé (RPPS), département × âge × sexe × mode × secteur | DREES | 2012-2026 (kinés : 2017-2026) | stock et taux |
| Infirmières libérales (SNDS), infirmières salariées (BTS) | DREES / Insee | 2012-2023 | stock IDE |
| Projections de population Omphale 2022 (département × âge × sexe), 3 scénarios | Insee | 2018-2070 | densités |
| Effectifs libéraux, 23 spécialités | ameli (Assurance Maladie) | 2010-2025 | contrôle croisé |
| Effectifs par commune et zonage conventionnel | CartoSanté / Atlasanté | 2004-2025 | échelle communale, régulation |
| Annuaire Santé (RPPS en libre accès) | ANS | nov. 2026 | grain communal, public / privé |
| Établissements (FINESS), historique | Ministère de la Santé | 2004-2025 | public / privé, officines |
| Diplômés et inscrits en formation (séries longues) | DREES | 1966-2025 | vivier de formation |
| Projections DREES (Dossier n°76, ER 1319) | DREES | 2021-2050 | comparaison à long terme |
| Inscriptions en santé par université | DREES (fichiers des organisateurs) | 2020-2025 | vivier, **jamais versionnés** |

Points de méthode :

- **Stock-flux par cohortes**, en tranches d'âge de 5 ans, taux ajustés par territoire. Les entrées sont
  un flux absolu, pour éviter le double comptage relevé lors du premier backtest.
- **Backtest contre des références naïves.** Par département, à 5 ans : 8,68 % de MAPE pour le
  stock-flux à taux locaux, 7,73 % pour les cohortes bayésiennes de l'axe 2, contre 9,30 % pour la
  tendance (mesuré, secteur privé). La carte et l'assistant servent C1 par défaut (taux précalculés dans
  `v2/methodes/out/c1_taux/`, `v2/methodes/c1_jumeau.py`).
- **Budget d'erreur.** Sur les 7,76 points de MAPE de C1, 3,1 points viennent d'un plancher de bruit
  poissonien (dérivé). L'essentiel du reste est local : la répartition des installations et des 35 à 59 ans
  entre départements. Cet écart local ne persiste pas d'une fenêtre de 5 ans à l'autre (r ≤ 0,24, mesuré).
  Ni modèle gravitaire ni modèle à agents pour l'instant : on teste d'abord des covariables
  ([rapport](v2/docs/lab/reports/2026-11-15-budget-erreur-c1-a2.md)).
- **2050 ne se backteste pas.** Les données vont de 2012 à 2026, donc on valide au plus sur environ
  10 ans. Au-delà, on s'appuie sur la reproduction des projections DREES, les cas limites du modèle et
  des fourchettes extrapolées, toujours affichées comme telles.
- **Plusieurs estimateurs, jamais un chiffre unique** présenté comme « la » projection.
- **Chaque nombre dit s'il est mesuré, sourcé, dérivé ou supposé**, et chaque entrée cite son jeu de
  données et son millésime. Le vocabulaire reste neutre : on décrit et on compare (« accès moindre »),
  on ne juge pas ([lexique](v2/docs/lab/lexicon.md)).

## Architecture

```
v2/
  ROADMAP.md           objectif, axes de recherche, ordre de travail
  jumeau/              axe 0 : état, moteur, scénarios, modules de flux (plug-ins), critères
  sante/               chargeurs des données de base, modèle stock-flux et estimateurs de référence
  methodes/            axe 2 : estimateurs candidats, banc de comparaison
  validation/          axe 3 : protocoles pré-enregistrés (preregistered/, gelés), prévision, DiD
  sensibilite/         axe 5 : Morris, Sobol, fourchettes à 2050
  data/                axe 4 : scripts de construction, processed/ (commité), manifest.py
  langage/             compilateur phrase -> leviers, glossaire, jeux de test à l'aveugle
  agent/               premier agent (gelé) : garde-fous (ancrage, lexique), jeu de 22 questions
  prototype/           serveur des leviers et du jumeau (bibliothèque de la carte)
  prototype-carte/     carte de décision (port 8767)
  papers/              un article par axe et l'article de synthèse (LaTeX)
  docs/lab/            décisions, questions ouvertes, rapports, fiches, lexique ; archive-v1/
data/
  processed/           données de base traitées (commitées, voir MANIFEST.md)
  raw/                 fichiers bruts (non commités)
chatbot/               chatbot (passerelle lecture seule + agent), relayé par la carte
docs/lab/profile.md    profil du laboratoire (lu par les skills de .claude/)
Home.md                page d'accueil du coffre Obsidian
```

Le dépôt est aussi un **coffre Obsidian** : ouvrez la racine dans Obsidian et commencez par
`Home.md`. Chaque décision est datée dans `v2/docs/lab/decisions.md`, et chaque question ouverte a
un prix dans `v2/docs/lab/open.md`. L'ancienne v1 (application Streamlit, premier registre du
13 novembre) a été absorbée le 2026-11-14 : son code utile est dans `v2/sante/`, son registre est
archivé dans `v2/docs/lab/archive-v1/`.

## Reconstruire les données

Seulement pour régénérer `data/processed/` ou `v2/data/processed/`, après avoir placé les fichiers
bruts dans `data/raw/` et `v2/data/raw/` (sources et millésimes : `MANIFEST.md` de chaque dossier, et
l'en-tête de chaque script) :

```bash
PYTHONPATH=v2 uv run python -m sante.load          # DREES RPPS + Insee Omphale -> data/processed/
uv run python v2/data/build_secteur.py             # séparation public / privé (≈ 30 s)
uv run python v2/data/build_zonage.py              # zonage par commune
uv run python v2/data/build_sise.py                # inscrits CD et PH par année d'études (SISE, ouvert)
uv run python v2/data/manifest.py                  # réécrit les manifestes ; --check pour vérifier
```

Outils de recherche (certains lisent des fichiers bruts, par exemple le vivier de formation DREES) :

```bash
PYTHONPATH=v2 uv run python -m jumeau.check                 # critères d'acceptation du jumeau
PYTHONPATH=v2 uv run --with scipy python -m besoin.tests    # module de besoin : critères d'identité et cas limites
uv run python v2/prototype-carte/tests/couverture.py http://127.0.0.1:8767   # besoin → carte (serveur lancé) : O2, L23, latence
PYTHONPATH=v2 uv run python -m besoin.validation.pb1        # besoin, P-B1 : âge (M1) contre population (M0)
PYTHONPATH=v2 uv run --with scipy python -m besoin.validation.pb2   # besoin, P-B2 : saturation (M2b)
PYTHONPATH=v2 uv run python -m besoin.validation.pb3        # besoin, P-B3 : morbidité (M3)
PYTHONPATH=v2 uv run --with scikit-learn --with xlrd --with openpyxl python -m besoin.validation.pb5   # P-B5 : backtest
PYTHONPATH=v2 uv run --with scipy python -W ignore -m sensibilite.besoin.grille && PYTHONPATH=v2 uv run python -m sensibilite.besoin.stats   # besoin, axe 5 : sensibilité de C
PYTHONPATH=v2 uv run python -m methodes.banc                # axe 2 : banc des méthodes
PYTHONPATH=v2 uv run --with scipy python -W ignore -m methodes.budget_erreur   # axe 2 : budget d'erreur
PYTHONPATH=v2 uv run --with scipy python -m validation.did  # axe 3 : effet de la régulation
uv run python v2/langage/evaluer_hors_echantillon.py cas_test_hors_echantillon_6.yaml   # compilateur
```

## Confidentialité des données

Le dépôt est **public** sur GitHub (vérifié le 2026-11-15). Les tables communales publiées contiennent des
cellules à une personne : voir l'[audit RGPD, AIPD, 2017/745](v2/docs/lab/reports/2026-11-15-audit-rgpd-aipd-dm.md)
et la question ouverte sur le seuil de diffusion.

- `data/processed/` et `v2/data/processed/` sont **commités** : ils ne contiennent que des données
  ouvertes (DREES, Insee, ameli, CartoSanté, Annuaire Santé, FINESS, zonage data.gouv).
  `v2/data/manifest.py --check` échoue si un script de construction lit un fichier des organisateurs.
- `data/raw/` et `v2/data/raw/` restent exclus par `.gitignore`.
- Les fichiers fournis par les organisateurs (inscriptions par université) sont couverts par un accord
  de confidentialité et ne sont **jamais** versionnés, ni bruts ni dérivés. Ils restent dans `data/raw/`
  sur les postes qui les ont reçus ; seuls des réglages optionnels du jumeau les lisent.
- Les documents tiers (mémoire EHESP) restent en local.

## Limites connues

- **Le public et le privé ne sont séparés que par estimation.** Les fichiers DREES regroupent les
  salariés hospitaliers. La sortie 2026 est donc une fourchette (sages-femmes : 12 059 à 14 660).
- **Pas de projection fiable sous le département.** Les modèles communaux testés (K3 à K5) n'ont pas
  passé la validation pré-enregistrée ; la carte affiche les projections au département.
- **Module de besoin : indice de couverture, pas un niveau de besoin.** `v2/besoin/` rapporte l'offre du
  jumeau à un besoin estimé, indexé à 2026. Les sept protocoles gelés sont passés (2026-11-15,
  `v2/docs/lab/reports/2026-11-15-besoin-etape.md`) : la pondération par l'âge (M1) est retenue pour les cinq
  professions (dentistes de justesse) ; la saturation du recours (M2b) tombe, donc le besoin non satisfait n'est
  pas identifié ; la morbidité (M3) ne sert l'indice que pour les infirmiers ; le backtest 2016 → 2025 retient
  l'âge contre la persistance pour 3 professions sur 4. L'indice spatial M4 échoue à reproduire l'APL DREES en
  repli vol d'oiseau (ρ 0,66 à 0,77 pour 0,90 exigé), avec les temps routiers OSRM (ρ 0,71 à 0,76) et pour les
  pharmacies contre l'APL V0 2013 (P-B4-PH, ρ 0,72) : c'est une mesure d'accessibilité maison, jamais appelée « APL ». Pour les transferts de tâches, `k` et l'expansion `m` restent supposés. Aucun indice de
  couverture n'est produit pour la médecine générale. Les passages lisent des tables data.ameli.fr (ODbL) hors
  dépôt, à reconstruire avec `uv run python v2/besoin/donnees/ameli.py`.
- **Grandeur mesurée : la demande de ville, pas le besoin de la population.** Le recours vient d'Open DAMIR,
  secteur privé, tous statuts d'exécutant (statut inconnu compris : 3 à 13 % des actes). C'est la demande adressée
  au secteur privé de ville ; la part servie par l'hôpital public n'y est pas. L'offre privée du jumeau compte les
  salariés du privé (64,5 % des infirmiers privés, dont 34 % en clinique), que ce recours ne voit pas : sans effet
  sur l'indice tant que leur part reste constante, mais un niveau en ETP ne se compare jamais à l'effectif privé
  total des infirmiers ou des pharmaciens (registre, « périmètre libéral de DAMIR »).
- **Sensibilité de l'indice de couverture (axe 5 du besoin, 2026-11-15).** En 2050, l'effet de quotas × 1,2 sur
  C dépasse l'écart entre modèles de besoin pour les sages-femmes, dentistes et pharmaciens, pas pour les kinés
  (ratio 0,77) ni les infirmiers (0,34). Cet écart tient à M0 (sans effet de l'âge), réfuté par P-B1 : il est
  retiré de l'affichage et montré comme l'effet du vieillissement. C est servi par M1 (M3 pour les infirmiers) ; sa
  largeur vient de l'incertitude de l'offre (52 à 92 % de la variance), affichée en bande.
  `v2/docs/lab/reports/2026-11-15-besoin-axe5-sensibilite.md`.
- Données du module de besoin (2026-11-15) : `v2/besoin/donnees/`, un module par source (APL DREES,
  data.ameli.fr, Open Medic, IQVIA, Open DAMIR lu en flux, distancier à vol d'oiseau), manifeste et contrôles dans
  `v2/besoin/donnees/MANIFEST.md`. Les tables issues de data.ameli.fr (ODbL) ne sont pas versionnées : les
  reconstruire avec `uv run python v2/besoin/donnees/ameli.py`.
- Les effectifs sont comptés en têtes. L'activité par professionnel (équivalents temps plein) n'est
  qu'une hypothèse supposée, sans série ouverte vérifiée.
- Les tranches d'âge de 5 ans supposent des âges uniformes dans chaque tranche (biais connu sur les
  seniors).
- Le compilateur de phrases bien traduit environ 70 à 77 % des phrases selon le jeu de test : l'écran de confirmation reste
  indispensable.

## Feuille de route

- Recette de l'application : les 6 P1 sont corrigés ; 3 P2 restent, dont le bouton « A+ » (texte agrandi) disparu, à
  rétablir ou à retirer de la recette ([corrections](v2/docs/lab/reports/2026-11-15-uat-corrections.md)).
- Module de besoin : mesurer `k` des transferts ; projeter la part libérale de l'offre privée ; trouver une source
  ouverte de la demande servie par l'hôpital public.
- Amélioration possible, hors plan : spécialités (cardiologie, dermatologie, ophtalmologie).
- Noter les dépôts pré-enregistrés sur les effectifs 2027.

Détail : [`v2/ROADMAP.md`](v2/ROADMAP.md).
