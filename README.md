# Jumeau numérique de l'offre de soins libérale

> Hackathon santé publique : **« Anticiper l'évolution de l'offre de soins »**

Un projet de recherche quantitative. On simule des **politiques publiques nationales** et on mesure
leur effet sur le nombre de professionnels de santé **libéraux** (hors médecine générale) jusqu'en
**2050**, à toutes les échelles, de la commune au national. Chaque politique est un réglage
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

Déjà cloné ? `git pull` puis `uv sync` suffisent. Si une erreur parle de `data/raw/` ou d'un fichier
`.parquet` absent :

```bash
git pull                                        # les données traitées sont commitées depuis le 2026-11-14
uv run python v2/data/manifest.py --check       # doit afficher « OK »
```

Ne lancez **pas** `sante.load` ni les `v2/data/build_*.py` pour démarrer : ils servent seulement à
[reconstruire les données](#reconstruire-les-données) à partir des fichiers bruts (≈ 3,6 Go, non
commités).

**Vidéo de présentation** (57 s, voix off IA) : [`v2/video/out/pitch.mp4`](v2/video/out/pitch.mp4), commitée.
Pour la refaire (Remotion, voir `v2/video/README.md`) :

```bash
cd v2/video && npm install && npm run render    # -> v2/video/out/pitch.mp4
```

## Le problème

Former un professionnel de santé prend de 3 à 10 ans. Une décision prise aujourd'hui (quotas,
régulation de l'installation, âge de départ) ne produit son plein effet que bien plus tard, et souvent
ailleurs que là où on l'attendait. Les projections publiées (DREES, Insee) sont nationales et
tendancielles. Il manque un outil qui dise, **pour un territoire donné**, ce qu'une politique change
et avec quelle incertitude.

Professions couvertes : **sages-femmes, chirurgiens-dentistes, pharmaciens,
masseurs-kinésithérapeutes, infirmiers**. Les spécialités médicales (cardiologie, dermatologie,
ophtalmologie) forment une phase 2.

**« Libéral » au sens large.** Ici, « libéral » désigne **tout le secteur privé**, lucratif ou non :
libéraux et mixtes, pharmaciens adjoints d'officine, salariés de cliniques privées, industrie. Tout
employeur public est exclu. C'est plus large que le sens habituel du RPPS ou d'ameli (exercice
indépendant), et chaque sortie le rappelle.

## Ce que fait l'outil

**La carte de décision** (`v2/prototype-carte/`, http://localhost:8767) :

- **Carte des départements et des régions**, au choix : évolution 2026 → 2050, écart au tendanciel,
  ou **densité 2050 pour 100 000 habitants** (Insee Omphale 2022). Recalcul après chaque réglage en
  environ 50 ms (mesuré).
- **9 leviers en 4 familles** (former, attirer, installer, retenir), chacun avec son délai d'effet et
  son niveau de preuve (sourcé ou supposé). Le curseur principal de chaque famille est visible ; les
  réglages fins sont sous « Plus de réglages ».
- **Une phrase en langage naturel** (« augmenter de 20 % les places de kinés dans le Puy-de-Dôme »)
  devient un réglage des leviers. Le compilateur est déterministe et à glossaire (`v2/langage/`) : il
  traduit, il ne calcule jamais. Environ **77 % des phrases** sont entièrement bien traduites, mesuré
  sur des jeux écrits à l'aveugle. Un écran montre toujours ce qui a été compris et ce qui n'est pas dans
  le modèle, et rien n'est appliqué sans confirmation.
- **Hypothèses de contexte** : scénario de population Insee (central, bas, haut) et activité moyenne
  par professionnel (équivalents temps plein, supposée).
- **Fiche par territoire** : effectif 2026, 2050, écart au tendanciel, repères 2030 / 2035 / 2040 / 2050
  avec fourchette et densité, écart décomposé par flux, export CSV avec sources, millésimes, hypothèses et
  version du code.
- **Mode expert** : écart par flux et par année, chaque levier avec sa valeur, son paramètre, son délai,
  son statut et sa source, trois scénarios épinglés côte à côte, export JSON.

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
| 1. Hyperparamètres | Fiches sourcées : régulation conventionnelle, filières en pharmacie, spécialisation en odontologie, abandon en IFSI… | ✅ fiches, sources à relire en texte intégral |
| 2. Méthodes | Battre le stock-flux sans boîte noire | ✅ cohortes bayésiennes : MAPE dép. 7,73 % contre 8,68 % ; projection communale (K3 à K5) non confirmée, affichage au département |
| 3. Validation | Protocoles pré-enregistrés, gelés par SHA-256 (N1 à N12) | ✅ exécutés en grande partie ; dépôts à noter sur les données 2027 |
| 4. Données | Public / privé, registre de 30 événements datés, zonage par commune, grain communal | ✅ |
| 5. Sensibilité | Morris puis Sobol : quels paramètres déplacent l'effectif en 2050 ? | ✅ en 2050, la décision pèse plus que l'incertitude pour IDE, MK, SF |
| Carte | Leviers, phrase, densité, mode expert, export | ✅ démontrable |
| Phase 2 | Cardiologie, dermatologie, ophtalmologie | à venir |

Article de synthèse (feuille de route, six axes, interface, suite) : `v2/papers/synthese/`
(`python3 build.py && tectonic main.tex`).

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
  tendance (mesuré, secteur privé).
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
  prototype/           serveur des leviers et du jumeau (bibliothèque de la carte, port 8766)
  prototype-carte/     carte de décision (port 8767)
  papers/              un article par axe et l'article de synthèse (LaTeX)
  docs/lab/            décisions, questions ouvertes, rapports, fiches, lexique ; archive-v1/
data/
  processed/           données de base traitées (commitées, voir MANIFEST.md)
  raw/                 fichiers bruts (non commités)
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
uv run python v2/data/manifest.py                  # réécrit les manifestes ; --check pour vérifier
```

Outils de recherche (certains lisent des fichiers bruts, par exemple le vivier de formation DREES) :

```bash
PYTHONPATH=v2 uv run python -m jumeau.check                 # critères d'acceptation du jumeau
PYTHONPATH=v2 uv run python -m methodes.banc                # axe 2 : banc des méthodes
PYTHONPATH=v2 uv run --with scipy python -m validation.did  # axe 3 : effet de la régulation
uv run python v2/langage/evaluer_hors_echantillon.py cas_test_hors_echantillon_6.yaml   # compilateur
```

## Confidentialité des données

Le dépôt est **privé**, réservé à l'équipe.

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
- **Pas de module de besoin.** Les transferts de tâches (vaccination en officine, IPA, accès direct au
  kiné) n'ont aucun effet dans le jumeau ; ils sont signalés « pas encore dans le modèle ». Un plan
  existe : `v2/docs/lab/derivations/2026-11-14-module-besoin.md`.
- Les effectifs sont comptés en têtes. L'activité par professionnel (équivalents temps plein) n'est
  qu'une hypothèse supposée, sans série ouverte vérifiée.
- Les tranches d'âge de 5 ans supposent des âges uniformes dans chaque tranche (biais connu sur les
  seniors).
- Le compilateur de phrases bien traduit environ 77 % des phrases : l'écran de confirmation reste
  indispensable.

## Feuille de route

- Rejouer la recette par personas sur la carte finale.
- Module de besoin (population × recours par âge, transferts de tâches), après son test d'abandon.
- Phase 2 : cardiologie, dermatologie, ophtalmologie.
- Noter les dépôts pré-enregistrés sur les effectifs 2027.

Détail : [`v2/ROADMAP.md`](v2/ROADMAP.md).
