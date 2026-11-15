---
type: analysis
date: 2026-11-15
author: session besoin-axe5-sensibilite
question: L'assistant peut-il simuler un transfert de tâches proposé par l'utilisateur·rice sans le présenter comme un levier sourcé ?
headline: "Oui : forme de L23 généralisée dans /api/couverture. Le transfert générique MG → PH aux paramètres de L23 reproduit l23=1 à 0,0 près. Infirmiers, Puy-de-Dôme, 2035, 10 % des renouvellements d'ordonnance des généralistes : −0,1 / −0,2 / −0,4 % pour a = 5 / 10 / 20 % (hypothèse de l'utilisateur). p95 24,7 ms."
status: done
professions: [infirmiers, pharmaciens, kines, dentistes, sages-femmes]
hypothesis: plan v2/docs/lab/derivations/2026-11-15-transfert-hypothetique-plan.md
sources: [v2/besoin/transferts.py, v2/prototype-carte/server.py, v2/langage/compilateur.py, chatbot/chat/agent.py]
tags: [besoin, transfert, assistant, O2]
---

# Transfert de tâches hypothétique dans l'assistant

> **Headline :** l'assistant simule maintenant « X prennent p % de <acte> de Y ».
> - La réponse est balayée sur `a`, jamais un chiffre unique, et étiquetée « hypothèse de l'utilisateur ».
> - L23 n'a pas changé : mêmes sorties, octet pour octet.
> - Le faux refus O2 de la recette est corrigé.

## Question
- On veut répondre à « si les infirmiers prennent 10 % des renouvellements d'ordonnance des généralistes, quelle
  couverture des infirmiers dans le Puy-de-Dôme en 2035 ? ».
- Deux contraintes : sans nouvelle source pour C, et sans faire passer le résultat pour sourcé.
- Le plan et le challenge sont dans [la dérivation](../derivations/2026-11-15-transfert-hypothetique-plan.md).

## Result
| Critère (plan) | Mesure | État |
|---|---|---|
| 1. L23 inchangé | `l23=1` (avec et sans `l23_a`/`l23_k`, avec leviers d'offre) et `prof=infirmiers` : JSON identiques avant/après (hors `ms` et nouvelle clé) | ✅ |
| 2. Transfert nul ⇒ écart 0 | `tr_a=0` : écart max 0,0 (dép., France) | ✅ |
| 3. Générique = L23 | MG → PH, a 0,01, k 1, s∞ 0,74, τ 2,4, t₀ 2026 : écart max sur `cs` 0,0 | ✅ |
| 4. O2 sur la cible | `tr_cible` MG, spécialistes, orthophonistes ⇒ 400 ; `tr_src` MG ou spécialistes ⇒ 200 | ✅ |
| 5. Compilateur | 10 phrases écrites avant le code : 10/10 ; 7 jeux existants inchangés (35/36, six jeux à l'aveugle, transferts 11/12) | ✅ |
| 6. Sans IA | phrase d'exemple : 3 points de a, paramètres et statuts réaffichés, raison « pas un levier de la carte », pas de refus O2 ; « couverture des généralistes » ⇒ refus O2 | ✅ (navigateur, port 8795) |
| 7. Latence | p95 24,7 ms (n = 30, à chaud) ; K1–K6 toujours verts | ✅ |

Exemple, infirmiers, Puy-de-Dôme, 2035. La valeur `s∞` = 10 % est celle donnée par l'utilisateur·rice. Les autres
paramètres sont supposés : k 1, τ 2,4 ans, t₀ 2026.

| a (poids de l'acte dans la demande des MG, balayé) | indice (tendanciel 0,949) | écart au tendanciel |
|---|---|---|
| 5 % | 0,948 | −0,1 % |
| 10 % | 0,948 | −0,2 % |
| 20 % | 0,946 | −0,4 % |

Pour a = 10 %, le temps transféré correspond à environ 630 médecins à temps plein (France, 2035). Ce chiffre est
**dérivé** d'un niveau de demande MG supposé.

![Capture](../figures/2026-11-15-transfert-hypothetique-assistant.jpg)

## How
- **Données :** inchangées.
  - Besoin M1, M2a et M3 en cache.
  - Demande de la MG : M1, profil Open DAMIR 2025, niveau placeholder de 0,9 ‰ (supposé).
  - Demande des spécialistes : M0, même placeholder.
- **Méthode :**
  - Formules : `B'_cible = B_cible + s·a·k·B_src` et `B'_src = B_src (1 − s·a)`.
  - Elles sont appliquées dans `couverture_carte` sur les tableaux de besoin en cache, après L23.
  - Le compilateur lit la phrase (`transfert_hypothetique`, glossaire `transferts_hypothetiques`).
  - L'assistant appelle `couverture` trois fois (balayage de a).
- **Tests :** `uv run python v2/prototype-carte/tests/couverture.py <url>` (K1–K7) ;
  `uv run python v2/langage/evaluer_transferts_hypothetiques.py` ; `cd chatbot && uv run pytest` (51 tests).

## ⚑ What could make it wrong
- **Ampleur.** L'écart vaut environ `−s·a·k·B_src/B_cible`, et le niveau `B_src` de la MG et des spécialistes est un
  placeholder. Un niveau réel 2 fois plus élevé double l'effet.
- **Sens de p.** L'analyse de « p % des <acte> » (s∞ = p, a balayé) ou de « p % de la demande » (a = p) est une
  convention du glossaire. Une tournure non prévue retombe sans transfert, sur la projection tendancielle.
- **Fourchette entre estimateurs.** Pour les infirmiers, M2a et M3 n'ont pas de MG : la même `B_src` (M1) leur est
  ajoutée. La fourchette entre estimateurs ne reflète donc pas l'incertitude de la source.
- **L23 combiné à un transfert MG.** Le transfert hypothétique lit la demande MG de base, pas celle déjà réduite
  par L23 : petit double compte possible.

## → What it changes
- `v2/prototype-carte/server.py` : `/api/couverture` accepte `tr_*`, ajoute le bloc `transfert_hypothetique` et le
  critère K7.
- `v2/langage/` : nouveaux champs `transferts_hypothetiques` et `o2_cible`.
- `chatbot/` : schéma `couverture.transfert`, balayage de a, O2 limité à la cible.
- La carte ne propose pas d'afficher un transfert hypothétique, car elle n'a pas ce levier. Pas de bandeau ajouté.

## ? Next
| Item | Cost |
|---|---|
| Mode IA : vérifier que le modèle balaie aussi a (consigne dans le schéma, pas dans le prompt) | ~10 min Claude + une clé |
| Niveau de la demande MG (r̄) depuis Open DAMIR 12 mois, au lieu du placeholder | ~30 min Claude |
| Bandeau « transfert hypothétique » dans la carte, avec `tr_*` transmis depuis la proposition de l'assistant | ~20 min Claude |

## Suites du 2026-11-15 (« les 3 go »)
| Suite | Résultat |
|---|---|
| Niveau MG / spécialistes | Mesuré, effectif libéral ameli 2025 : 56 005 / 57 346. Facteur 0,911 sur la MG. Exemple : −0,08 / −0,17 / −0,34 % (avant : −0,1 / −0,2 / −0,4 %). Environ 574 médecins à temps plein pour a = 10 % (avant : 630). L23 inchangé. |
| Mode IA | Avant correction : chiffre unique, a = 10 % de toute la demande MG, −1,7 % (10 fois trop). Après : balayage par la passerelle et consigne « p % des <acte> » → s_inf ; 6 questions conformes ([mesures](../../langage/mesures/2026-11-15-transfert-hypothetique-mode-ia.txt)). |
| Bandeau | « Transfert hypothétique (paramètres de l'utilisateur) » avec « Retirer ». La carte reprend le point médian (−0,17 %, D63, 2035), « Retirer » remet l'écart à 0. |

⚑ Mode IA : la réponse L23 garde deux écarts antérieurs (« ETP libérés », « la demande diminue »), inscrits au
ledger. Le dessin de la carte n'a pas été vu dans le navigateur, faute de rendu dans le panneau masqué ; les états
(bandeau, vue, écart) ont été vérifiés par script.

## Recontrôle après la correction L23 (P1-4, `b35a380`)
- **Sans IA, bout en bout par la carte.** Exemple : −0,08 / −0,17 / −0,34 %, environ 574 médecins à temps plein ;
  les valeurs sont inchangées, le niveau MG étant déjà le niveau mesuré. « Couverture des généralistes » : refus O2.
  Mode « demande » : 2,5 / 5 / 10 %. L23 : 101 666 vaccinations en moins en 2035, environ 23 à temps plein.
- **Mode IA, question d'exemple posée 4 fois.**
  - Appel juste 4/4 : `s_inf` = 0,1 et `a` balayé.
  - Réponse finale avec les trois points 3/4, dont 2 après la correction automatique. 1/4 a été bloquée par la
    vérification (« moyen terme », qualificatif sans source) : le garde-fou a joué, la réponse n'est pas fausse
    mais vide.
- **L23 en mode IA.** Nouveaux chiffres (écart ≈ 0,0 %), et la réponse explique que seule la part au-delà de 2026
  (≈ 0,70) agit.
- **Écart de vocabulaire restant en mode IA.** « équivalents temps plein » ou « ETP » apparaissent encore dans
  certaines réponses (ledger).
- **Erreur de vérification corrigée.** Un premier passage avait été servi par la passerelle et le chatbot d'une autre
  session (ports 8796 et 8797, worktree `c1-gbm`) : il a été écarté et refait sur des ports propres.

