---
type: analysis
date: 2026-11-15
author: session besoin-assistant
question: "Le compilateur et l'assistant savent-ils traiter la vaccination en officine (L23) et l'indice de couverture, sans couverture MG ?"
headline: "Jeu transferts (12 phrases, écrit avant le code) : 3/12 → 11/12 ; six jeux à l'aveugle inchangés (29, 27, 30, 30, 30, 21 / 30) ; 33 → 45 tests du chatbot verts, API de couverture simulée selon le plan"
status: draft
professions: [pharmaciens, infirmiers, kines]
hypothesis: "L23 compilé avec sa date ; L25, L27, tension/diabète restent hors modèle (non mesurables)"
sources: [v2/docs/lab/fiches/param-besoin-l23-vaccination.md, v2/docs/lab/fiches/param-besoin-l25-ipa.md, v2/docs/lab/fiches/param-besoin-l27-kine.md, v2/docs/lab/fiches/param-besoin-tension-diabete.md, v2/docs/lab/derivations/2026-11-15-besoin-carte-plan.md]
tags: [besoin, langage, chatbot, L23, O2]
---

> **Erratum 2026-11-15 (P1-4, double compte de L23).** Les effets de L23 cités plus bas sont **dépassés**. Ils
> rejouaient à partir de 2026 la montée en charge mesurée depuis 2019, alors que la part officinale atteignait déjà
> 0,687. Seule la part au-delà de celle atteinte en 2026 agit désormais (commit b35a380, décision au registre).
> Nouveaux chiffres, mesurés sur b35a380 :
> - pharmaciens, France 2050 : −0,03 % (C 1,0126 → 1,0123), au lieu de −0,7 % (1,0056) ;
> - Puy-de-Dôme 2035 : 0,9892 → 0,9889 (−0,03 %) ;
> - vaccinations en moins pour les généralistes : 104 110 en 2050 (101 666 en 2035), au lieu d'environ 1,9 M ;
> - soit environ 24 généralistes à temps plein (23 en 2035), au lieu d'environ 495.
>
> Rapport de référence : [L23, marge au-delà de la part atteinte](2026-11-15-l23-p1-4-marge.md). Les anciens chiffres
> restent ci-dessous, tels que mesurés à l'époque.

# Besoin dans l'assistant et le compilateur : L23 et couverture

> **Headline :** sur un jeu de 12 phrases écrit **avant** le changement, le compilateur passe de **3/12 à 11/12** en
> correspondance exacte (champ `transferts` : 5/12 → 12/12). Les six jeux à l'aveugle existants, non modifiés, gardent
> exactement leur score. L'assistant répond « effectif inchangé dans le modèle, couverture … » et refuse toute couverture MG.

## Question
Faire comprendre l'indice de couverture C (base 2026) et le levier L23 au compilateur `v2/langage/` et à l'assistant
`chatbot/`, sans toucher à `v2/prototype-carte/`.

## Méthode
- **Jeu nouveau** `v2/langage/cas_test_transferts.yaml` (12 phrases : 7 L23 dont 4 datées, 4 non mesurables, 1 témoin),
  écrit et mesuré avant toute modification du compilateur. ⚑ Pas à l'aveugle : même session que le code.
- `evaluer_hors_echantillon.py` compte le champ `transferts` (id, t0) seulement pour les jeux qui le déclarent ; les jeux
  existants sont scorés comme avant.
- Sorties brutes : `v2/langage/mesures/2026-11-15-transferts-avant.txt` et `…-apres.txt` (mesuré).

## Résultats (mesurés)
| Jeu | Avant | Après |
|---|---|---|
| hors échantillon 1 | 29/30 | 29/30 |
| hors échantillon 2 | 27/30 | 27/30 |
| hors échantillon 3, 4, 5 | 30/30 chacun | 30/30 chacun |
| hors échantillon 6 | 21/30 | 21/30 |
| en échantillon (`evaluer.py`) | 35/36 | 35/36 |
| **transferts (nouveau)** | **3/12** | **11/12** (L23 6/7, non mesurables 4/4, témoin 1/1) |

Échec restant : t12 « Pharmaciens qui vaccinent et infirmiers en pratique avancée » : deux professions, le compilateur
retient la première (pharmaciens, avec avertissement) alors que le jeu attend `null`. Laissé tel quel (règle existante).

Tests du chatbot : 33/33 avant ; **45/45** après (12 nouveaux dans `tests/test_couverture.py`, liste blanche mise à jour).
`test_aucun_fichier_du_modele_modifie` exige un arbre git propre : il passe après commit, pas avant.

## Ce qui a changé
- **Compilateur** : nouvelle section `transferts_besoin` (L23 : vacciner, vaccination…, cible pharmaciens, t0 par défaut
  2026). Sortie `transferts` = `[{id: L23, t0, source, cible, parametres_api: {l23: 1, l23_t0}, statut, fiche}]`. Date =
  année qui suit le terme dans sa proposition (« à partir de », « dès », « en ») ; une année placée avant (« en 2050 si
  les officines vaccinent ») reste l'horizon. Négation (« ne pas autoriser … à vacciner ») : L23 écarté. La vaccination
  reste aussi dans `non_modelise` : l'effectif ne change pas.
- **Non mesurables** : raisons de `ipa` (L25) et `acces_direct` (L27) réécrites d'après les fiches ; nouvelle entrée
  `tension_diabete`. Aucune n'a de `transferts`.
- **Passerelle** : outil `couverture` (indice base 2026, tendanciel et scénario, `ecart_tendanciel_pct`, fourchette entre
  estimateurs si l'API la donne, statuts des paramètres L23, ETP libérés chez la source) ; refus O2 ; périmètre mis à jour
  (`besoin` devient « besoin absolu, part du besoin couvert », nouvelle entrée `couverture_medecins`).
- **Assistant** : règle 12 du prompt (vocabulaire couverture, interdit MG, pas de « % du besoin couvert ») ; mode
  déterministe : « **Vaccination en officine (L23), à partir de 2026 : effectif inchangé dans le modèle.** Couverture des
  pharmaciens en 2035 (…) : x avec la vaccination, y au tendanciel, soit couverture légèrement moindre qu'au tendanciel ».

## Interface : contrat, pas API réelle
`origin/claude/besoin-carte-api-*` n'existait pas au `git fetch` du 2026-11-15. Le code suit l'étape 1 du plan
`2026-11-15-besoin-carte-plan.md` : `GET {CARTE_URL}/api/couverture?prof&terr&<leviers>&l23&l23_t0`, réponse de la forme
`besoin_api` (`years`, `territories`, `couverture`, `couverture_base`, optionnels `couverture_min/max`, `transferts`,
`hypotheses`). Tests contre une fausse API (`chatbot/tests/faux_carte.py`, **valeurs fictives**). Si l'API manque, la
réponse le dit (« indice de couverture non disponible »).

## ⚑ Ce qui pourrait rendre ceci faux
- La forme réelle de `/api/couverture` diffère du plan (noms de champs, `l23_t0` non accepté) : `_serie` lit plusieurs
  formes, mais un écart de nom casse l'outil. Coût de reprise : ~10 min une fois la branche publiée.
- Jeu de 12 phrases écrit par la session qui code : score en échantillon, optimiste.
- L'assistant charge désormais le compilateur du dépôt (plus celui de la copie `vendor/`) : ses réponses suivent le
  glossaire courant, la copie du modèle n'est plus la seule version qui compte.

## → Ce que ça change
`v2/prototype-carte/` (autre session) peut appeler `compile()` et lire `transferts[].parametres_api` pour poser `l23=1`.

## ? À étudier
- Rebrancher sur l'API réelle et rejouer `tests/test_couverture.py` contre elle (~10 min).
- Jeu L23 à l'aveugle écrit par un agent qui n'a pas vu le glossaire (~10 min).
- Mode LLM : non testé avec un vrai modèle de langage (pas de clé ici) ; vérifier que la règle 12 est suivie (~15 min, quota).

## Mise à jour : API réelle (2026-11-15, après fusion de `claude/besoin-carte-api-6d9504`)
- **Outil `couverture` aligné sur `couverture_carte`** : zones `fr` / `regs["R84"]` / `deps["63"]` = {cb, cs, ecart, min,
  max} ; fourchette montrée seulement si `fourchette_visible` (règle des 5 % de la carte) ; `l23.transferts` donne
  `actes_mg_liberes` et `etp_liberes_source` (France). L'API date L23 à 2026 : une autre date est signalée, pas appliquée.
  Défaut `CARTE_URL` : port 8767.
- **Étape 5 du plan** : intention « couverture » dans l'assistant (outil appelé même sans L23) ; MG + couverture → texte
  O2 ; `_scenario_carte` de la carte propose `{vue: couverture, l23: 1}` après un appel `couverture`.
- **Bout en bout (mesuré, serveur de la carte lancé, `v2/langage/mesures/2026-11-15-assistant-bout-en-bout.txt`)** :
  « couverture des pharmaciens à Clermont-Ferrand en 2035 si les pharmaciens vaccinent » → effectif 771 (tendanciel 771,
  inchangé) ; indice 0,98 avec L23 contre 0,99 au tendanciel, −0,7 %, « couverture proche du tendanciel » ; actes de MG
  libérés 1 878 752 injections, 468 ETP-équivalents (France) ; aucune couverture MG. **Pas de fourchette entre
  estimateurs** : un seul estimateur (M1) servi pour les pharmaciens (décision axe 5), la réponse le dit. Kinés ARA 2050 :
  fourchette M1–M2a affichée. Tests de la carte `tests/couverture.py` : K3–K6 OK.
- Tests du chatbot : **47/47**.
- ⚑ Manque : `index.html` n'applique pas encore la proposition `vue: couverture, l23: 1` (frontend de la carte, non touché).
- **Formulation (2026-11-15, après `3c52883`)** : l'assistant dit « Les pharmaciens vaccinent davantage contre la grippe » et
  « les médecins généralistes ont moins de vaccins à faire : environ N vaccinations en moins, soit le temps de travail
  d'environ M médecins à temps plein », comme la carte ; plus de « actes de MG libérés ». Tests 47/47.
- **Trois exemples de la carte (2026-11-15)** : `ASKEX` réduit à 3 phrases (leviers → effet ; objectif → possibilités ;
  L23 → couverture), doublons de l'accueil retirés ; chacune comprise de bout en bout sans IA (appels `projeter` ;
  `atteindre` ; `projeter` + `couverture` avec proposition `vue: couverture, l23: 1`) ; lexique OK ; mode IA non testé
  (pas de clé). Capture : `v2/docs/lab/figures/2026-11-15-assistant-trois-exemples.jpg`.
