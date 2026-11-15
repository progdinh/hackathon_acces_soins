# jumeau-chat — interroger le jumeau de l'offre de soins en langage naturel

Chatbot pour poser des questions au jumeau numérique de l'offre de soins libérale (dépôt
[`progdinh/hackathon_acces_soins`](https://github.com/progdinh/hackathon_acces_soins), défi 8 du hackathon Adopt AI for Health) :
projections, effet d'un levier, comparaison de scénarios, sensibilité, classement de départements.

**Le modèle de langage interroge le modèle, il ne peut pas le modifier, et il ne répond que dans son périmètre.**

## Démarrer

```bash
git clone --recurse-submodules <ce dépôt> && cd jumeau-chat
uv sync
scripts/lancer.sh                       # passerelle (8770) puis chatbot : http://localhost:8768
```
Dans le dépôt du jumeau, inutile de lancer ces deux processus à la main : `uv run python v2/prototype-carte/server.py`
les démarre en interne et tout passe par http://localhost:8767 (bouton « Assistant de simulation »).

Avec `ANTHROPIC_API_KEY` dans l'environnement, Claude interprète les questions et rédige (mode IA) ; sans clé, le
compilateur à glossaire de l'équipe prend le relais (mode déterministe, sans IA). À la main :
`uv run python -m passerelle.server` puis `uv run python -m chat.server`.

## Architecture : deux processus, une seule porte

```
navigateur ──► chat/ (port 8768)  ──GET──►  passerelle/ (127.0.0.1:8770)  ──►  vendor/hackathon_acces_soins
               modèle de langage            liste blanche de 8 requêtes        (sous-module épinglé, lecture seule)
               + vérification des nombres   arguments validés
               n'importe pas le modèle      seul processus qui charge le modèle
```

| Dossier | Rôle |
|---|---|
| `vendor/hackathon_acces_soins` | le modèle, **sous-module git épinglé** (commit `426422c`) ; jamais modifié ici |
| `passerelle/` | `requetes.py` (seul code qui importe le modèle), `schemas.py` (liste blanche + validation), `server.py` (GET seulement) |
| `chat/` | `agent.py` (boucle d'outils, prompt), `verif.py` (vérification des nombres), `client.py` (seul accès à la passerelle), `server.py`, `index.html` |
| `tests/` | sécurité, vérification, agent (faux modèle de langage + vraie passerelle) : `uv run pytest` |
| `integrations/streamlit/` | composant `afficher_chatbot()` pour intégrer le chatbot dans une application Streamlit (via l'API HTTP) |
| `eval/` | périmètre (`evaluer_perimetre.py`) et compréhension sur les jeux à l'aveugle de l'équipe (`evaluer_analyse.py`) |

## Garantie 1 : interroger, jamais modifier

1. **Le modèle de langage n'a que 8 outils, tous en lecture** : `perimetre`, `projeter`, `comparer`, `balayer`, `classer`,
   `decrire_leviers`, `incertitude`, `interpreter_phrase`. Aucun outil de fichier, de code, de commande ou d'écriture n'existe.
2. **Séparation des processus.** Le chatbot n'importe pas le modèle (vérifié par un test statique et un test d'exécution) ;
   il ne peut qu'envoyer des GET à la passerelle.
3. **La passerelle n'accepte que la liste blanche** : `GET /v1/requete/<nom>?args=<json>`. Les arguments sont validés par
   un schéma strict (champs inconnus refusés, bornes du modèle, tailles maximales, NaN refusé) avant tout calcul. POST, PUT
   et DELETE renvoient 405. Aucun fichier n'est servi, aucun chemin n'est accepté, pas de trace d'exécution renvoyée.
4. **Version tracée.** La passerelle lit le commit du modèle et signale un code modifié localement ; le chatbot l'affiche.
5. **Défense en profondeur** (`scripts/lancer.sh`) : le sous-module passe en lecture seule (`chmod -R a-w`) et Python
   n'écrit pas de `.pyc`. Lancer en utilisateur normal (sous root, chmod n'empêche rien). En production : conteneur
   non-root, sous-module monté en lecture seule. *Ce verrou système n'a pas pu être vérifié dans l'environnement de
   développement ; les points 1 à 4 sont testés.*

Testé (`tests/test_securite.py`) : méthodes d'écriture, requêtes hors liste (`ecrire_fichier`, `__init__`, `S`), chemins
(`../pyproject.toml`, `vendor/…`), champ `code`, quotas ×3, NaN, `../../etc/passwd` comme territoire, listes et textes trop
longs ; après une série de requêtes, `git status` du modèle est vide.

## Couverture et vaccination en officine (2026-11-15)
L'outil `couverture` lit l'indice de couverture (base 2026 = 1) sur l'API de la carte (`CARTE_URL`, défaut
`http://127.0.0.1:8767`, `GET /api/couverture` de `v2/prototype-carte/server.py`). « Les pharmaciens peuvent vacciner » (L23) :
effectif inchangé dans le modèle, couverture des pharmaciens avec écart au tendanciel. Jamais de couverture pour la
médecine générale ni les spécialistes (règle O2). Le compilateur chargé est celui du dépôt (`v2/langage/`), `LANGAGE_DIR`
pour en forcer un autre. Rapport : `v2/docs/lab/reports/2026-11-15-besoin-assistant.md`.

## Garantie 2 : répondre dans le périmètre, sans inventer

1. **Le périmètre est une donnée du modèle**, pas une opinion du modèle de langage : la requête `perimetre` renvoie ce qui est
   couvert (5 professions, secteur libéral, département, 2026 à 2050) et ce qui ne l'est pas, avec la raison (médecins,
   commune, après 2050, besoin de soins, coûts, causes, autres pays, chiffre exact, jugement de valeur), plus les politiques
   non modélisées du glossaire de l'équipe. Il est intégré au prompt système à chaque conversation.
2. **Marqueurs obligatoires.** Hors périmètre, la réponse commence par « Hors du périmètre du modèle : » et la raison ;
   partiellement couvert, elle répond à la partie couverte et ajoute « Limite du modèle : ». Pas de substitution silencieuse.
3. **Vérification automatique des nombres** (`chat/verif.py`). Chaque nombre de la réponse doit venir d'un résultat de la
   passerelle, de la question ou des arguments envoyés (tolérance de 6 % pour l'arrondi ; années 2012 à 2050 et entiers
   ≤ 10 admis). Sinon : une demande de correction au modèle de langage, puis **blocage** de la réponse. L'interface affiche
   « ✓ Chaque nombre vient d'un résultat du modèle », « corrigée » ou « bloquée ».
4. Le modèle de langage ne voit pas les séries brutes ; les **graphiques** sont construits à partir des résultats de la
   passerelle, jamais du texte du modèle de langage.

Limite de la vérification : elle contrôle les **nombres**, pas les affirmations qualitatives. Celles-ci reposent sur le
prompt et sur `eval/evaluer_perimetre.py`.

## Mesures

| Mesure | Résultat |
|---|---|
| Tests (`uv run pytest`) | 51/51 (2026-11-15, transferts hypothétiques) |
| Grille d'évaluation, contrôle avec le glossaire (`eval/evaluer_analyse.py --deterministe`) | jeu 6 : 21/30, identique au score publié par l'équipe |
| Compréhension en mode IA, jeux 5 et 6 (`eval/evaluer_analyse.py`) | **pas encore mesurée** (clé d'API requise) ; à battre : 70 % (jeu 6) |
| Périmètre en mode IA, 27 cas (`eval/evaluer_perimetre.py`) | **pas encore mesuré** ; jeu écrit par l'auteur du prompt (en échantillon) |

## Mettre à jour le modèle

```bash
chmod -R u+w vendor/hackathon_acces_soins
git -C vendor/hackathon_acces_soins fetch && git -C vendor/hackathon_acces_soins checkout <commit>
uv run pytest && git add vendor/hackathon_acces_soins && git commit -m "modèle : passage à <commit>"
```
Un changement de l'interface du modèle (`v2/prototype/server.py` : `Model.answer`, `parse_levers`, `LEVIERS_UI`) se voit
aux tests.

## Limites
- Grain départemental (celui du modèle servi) ; une ville est ramenée à son département.
- Mode déterministe : une profession et un territoire par question ; garde le contexte (profession, territoire) d'un tour à l'autre, pas les leviers.
- Conversations en mémoire ; pas de flux en continu (réponse en 5 à 20 s en mode IA).
- Chart.js, marked et DOMPurify sont chargés depuis cdnjs (accès internet requis pour les graphiques).
