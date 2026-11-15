---
type: analysis
date: 2026-11-15
author: session uat-corrections
question: "Les constats de la recette de l'application (P1-1, P1-2, P1-3, jargon de P1-6, P2 faciles) sont-ils corrigés, et la reproduction de chacun passe-t-elle ?"
headline: "3 P1 corrigés sur 3 (P1-1, P1-2, P1-3) et le jargon de P1-6 replié ; 14 P2 corrigés, 3 laissés (P2-10 en partie, P2-14, P2-5 sur le fond) ; K1–K7 verts (p95 17,9 ms), besoin.tests 15/15, chatbot 51/51"
status: done
professions: [sages-femmes, dentistes, pharmaciens, kines, infirmiers]
hypothesis: "corrections de recette, pas d'hypothèse"
sources: ["recette v2/docs/lab/reports/2026-11-15-uat-application.md", "carte v2/prototype-carte", "assistant chatbot/ en mode sans IA", "/api/couverture, /api/agent"]
tags: [uat, carte, assistant, besoin, corrections]
---

# Corrections de la recette de l'application

> **Headline :** les trois P1 encore ouverts (P1-1, P1-2, P1-3) sont corrigés et leur reproduction passe. Le jargon
> de méthode (reste de P1-6) est replié dans des détails « Méthode ». 14 P2 sont corrigés, 3 sont laissés. Contrôles :
> K1–K7 verts (p95 17,9 ms, n = 60), `besoin.tests` 15/15, chatbot 51/51.

## Question
Corriger ce que la [recette du 2026-11-15](2026-11-15-uat-application.md) a relevé, sans toucher au modèle
(`v2/besoin/estimateurs/`, `v2/jumeau/`) ni aux protocoles gelés. P1-4 (b35a380), P1-5 et la partie « mode simple » de
P1-6 étaient déjà tranchés au [registre](../decisions.md).

## Résultat

### Constat → correction → preuve

| # | Constat | Correction | Preuve (re-recette) |
|---|---|---|---|
| P1-1 | « Écart tend. −NaN % » en comparaison, vue Couverture | `renderCmp` lit `/api/couverture` pour chaque territoire comparé (département, région, France) ; colonne « Couverture · écart tend. », « — » si absente | Pharmaciens, D63 + D15 + ARA + France, 2035, vaccination active : avant `−NaN %` ×4 ; après `0,99 · −0,03 %`, `0,94 · −0,03 %`, `0,96 · −0,03 %`, `0,96 · −0,03 %` ([avant](../figures/2026-11-15-uat-corr-p1-1-avant.jpg), [après](../figures/2026-11-15-uat-corr-p1-1-apres.jpg)) |
| P1-2 | La page dit à la fois que la vaccination en officine est modélisée et qu'elle ne l'est pas | `#nonmod` : « autres transferts de tâches (IPA…) » + « Vaccination en officine : dans le modèle… change la couverture… pas le nombre de professionnels » ; limites de l'export idem ; phrase traduite (`/api/interpret`) : la vaccination comprise comme transfert sort de « Pas encore dans le modèle » et le bouton « Appliquer » apparaît ; glossaire sans « (L23) » | Texte de `#nonmod` et de l'export lus dans le DOM et le CSV (D63, pharmaciens) ; panneau ([avant](../figures/2026-11-15-uat-corr-p1-2-avant.jpg), [après](../figures/2026-11-15-uat-corr-p1-2-apres.jpg)) |
| P1-3 | Exemple 2 : « Territoire : France » pour un calcul en Normandie | La passerelle renvoie `code_territoire` dans la réponse d'`atteindre` ; la carte lit aussi `entree.territoire` en repli | Encadré : « Territoire : Normandie · Pharmaciens » ([avant](../figures/2026-11-15-uat-corr-ex2-avant.jpg), [après](../figures/2026-11-15-uat-corr-ex2-apres.jpg)) |
| P1-6 (jargon) | M1, M2a, DCIR, P-B4, C1, L23, s_inf… visibles par défaut | Fiche : phrase courante (« demande estimée à partir du recours actuel… ») et détail replié « Méthode (détail) » (estimateur, norme déclarée, seuil de fourchette, M4) ; légende sans code ; panneau : paramètres en clair, codes et sources sous « Sources et références » ; assistant : « jumeau numérique (projection par âge et par département) », nom technique dans le détail du calcul ; réponses sans « (L23) », « M1 », « paramètres de L23 » | Fiche kinés D63 ([avant](../figures/2026-11-15-uat-corr-fiche-avant.jpg), [après](../figures/2026-11-15-uat-corr-fiche-apres.jpg)) ; exemple 3 ([avant](../figures/2026-11-15-uat-corr-ex3-avant.jpg), [après](../figures/2026-11-15-uat-corr-ex3-apres.jpg)) |
| P2-1 | Fourchette dégénérée « 1,22 – 1,22 » | Fourchette seulement si `fourchette_visible` (infobulle, fiche, légende) | Fiche kinés D63 : plus de fourchette ; le seuil est dans « Méthode » |
| P2-2 | « besoin » à l'écran | Note du levier : « une part des vaccinations… » ; export : « Norme déclarée de l'estimateur central » | Panneau et CSV lus |
| P2-3 | L23, MG, t_PH / t_MG, s_inf, tau, mu visibles | Libellés en clair ; code entre parenthèses dans l'export | Panneau ([après](../figures/2026-11-15-uat-corr-p1-2-apres.jpg)), CSV |
| P2-4 | Nombres au format anglais | `toLocaleString("fr-FR")` : « 0,01 », « 2 600 000 », pente « 0,37 %/an » | CSV lu |
| P2-5 | « N vaccinations, soit le temps de M médecins » : nombres indépendants | « N vaccinations en moins… au-delà de la part déjà faite en pharmacie en 2026 » ; à part : « temps de travail libéré : environ M médecins, ordre de grandeur qui dépend d'une part supposée » (carte, export, assistant) | Fiche et exemple 3 ([après](../figures/2026-11-15-uat-corr-ex3-apres.jpg)) ; **le fond reste** (voir « laissés ») |
| P2-6 | Résumé « tendance » avec L23 actif | L23 compte dans `changedN()` (« Scénario · 1 levier modifié ») ; « Revenir à la tendance » le désactive ; encadré de l'assistant : ligne « Transfert » | DOM : `#levsum` = « Scénario · 1 levier modifié » ; exemple 3 |
| P2-7 | Légende en % pour un indice | Graduations 0,50 … 1,50, unité « indice » | DOM : `#ticks` = 0,50 / 0,75 / 1,00 / 1,25 / 1,50 ([après](../figures/2026-11-15-uat-corr-fiche-apres.jpg)) |
| P2-8 | Spécialistes « prévus en phase 2 » | Texte O2 actuel : « non projetés (amélioration possible, hors plan) ; admis seulement comme source d'un transfert, jamais comme profession projetée ni pour un indice de couverture » (passerelle, `correspondances.yaml`, glossaire) | Question du sujet : partie pharmaciens répondue, spécialistes refusés avec le nouveau texte ([avant : figure 14 de la recette](../figures/2026-11-15-uat-app-14-assistant-specialistes.jpg), [après](../figures/2026-11-15-uat-corr-p2-8-apres.jpg)) |
| P2-9 | Modèle « stock-flux » dans l'export, « bayésien C1 » dans l'assistant | L'export lit le même libellé (`/api/agent/etat`, servi aussi sans chatbot) | CSV : « jumeau v2, Modèle bayésien hiérarchique (…) » |
| P2-11 | Badge « effet supposé » / export « non mesurable » | Troisième badge « effet non mesurable » | Lecture du code (statut servi par `/api/meta`) |
| P2-12 | Profession inconnue confondue avec O2 | `/api/couverture?prof=xyz` → 400 « profession inconnue » | curl : `xyz` → « profession inconnue » ; `specialistes` → message O2 |
| P2-13 | Accessibilité | `h1` = titre du bandeau ; canevas de la carte libellé en français ; `aria-valuetext` = phrase du levier ; `#nlq` avait déjà son libellé | DOM |
| P2-15 | Recherche figée après le fil d'Ariane | `select()` aligne `#q` sur le territoire ouvert | Capture ([après](../figures/2026-11-15-uat-corr-p1-1-apres.jpg) : recherche « Puy-de-Dôme » ouverte depuis le lien) |
| P2-16 | « 107 % » sans explication | Une ligne : rapport des installés de l'année aux diplômés de l'année, au-dessus de 100 % quand des diplômés plus anciens s'installent | Fiche kinés ([après](../figures/2026-11-15-uat-corr-fiche-apres.jpg)) |
| P2-17 | « Ce que j'ai compris » répété ; « an(s) » ; ligne « région seulement » en doublon | La carte retire la phrase quand l'encadré la dit ; « +3 ans » ; la ligne « région seulement » n'est plus testée quand le territoire est une région | Exemple 2 : une seule ligne « Places en formation : +35 % », « +3 ans » |
| (en plus) | « −0,0 % » pour un écart de −0,03 % | Deux décimales sous 0,1 % (carte et passerelle) | « −0,03 % » partout |

**Décompte :** P1 corrigés 3/3 (P1-1, P1-2, P1-3), plus le jargon de P1-6. P2 corrigés : 14 (P2-1, 2, 3, 4, 6, 7, 8, 9,
11, 12, 13, 15, 16, 17), dont P2-5 pour la formulation. P2 laissés : 3.

### P2 laissés, et pourquoi

| # | Ce qui reste | Pourquoi |
|---|---|---|
| P2-5 (fond) | ETP et vaccinations calculés indépendamment (a × demande MG contre s × 2,6 M) ; borne haute de a | Toucher au calcul, c'est toucher au module de besoin (`v2/besoin/transferts.py`), hors consigne. La formulation ne lie plus les deux nombres |
| P2-10 | Fourchette 2050 dans la comparaison ; couverture hors vue Couverture | La couverture est dans la comparaison en vue Couverture (P1-1). Ajouter les colonnes à toutes les vues change la largeur du tableau sur mobile : plus de 15 min avec le contrôle mobile |
| P2-14 | Bouton « A+ » disparu, R25 de `recette.mjs` échoue | Rétablir ou retirer R25 est un choix d'interface à trancher par l'utilisateur·rice (le constat le demande avec une décision) |

Non corrigé non plus : le sous-titre du graphique de l'exemple 3 (« aucun levier : scénario tendanciel ») reste celui
de la projection d'effectif, qui n'a en effet aucun levier ; l'encadré, lui, nomme le transfert.

### Contrôles

| Contrôle | Résultat |
|---|---|
| `v2/prototype-carte/tests/couverture.py` (serveur sur 8793) | K1–K7 OK ; K5 p95 17,9 ms (n = 60, **mesuré**) |
| `PYTHONPATH=v2 uv run python -m besoin.tests` | 15/15 OK |
| `cd chatbot && uv run pytest` | 51/51 (lancé sur l'arbre propre, après le commit) |
| `recette.mjs --option1` | 44/46 : R25 (« A+ », P2-14, déjà en échec à la recette) ; R14 p95 504 ms pour 500 ms visés (**mesuré** pendant que d'autres scripts headless tournaient ; monnaie du projet < 2 s). Premier passage : R22 en échec (export rendu asynchrone), corrigé et repassé ; R37 en échec ponctuel, repassé seul et dans le passage complet |

## How
- **Branche :** `claude/uat-corrections-7f792f`, partie de b35a380. Données brutes branchées par lien symbolique,
  retirées à la fin.
- **Serveurs (ports libres, entrées locales de `.claude/launch.json`, non commitées) :** carte 8793 ; passerelle 8796
  (`CARTE_URL` = 8793) ; chatbot sans IA 8797, clés d'API retirées de l'environnement. Les captures « avant » viennent
  d'une copie temporaire de la page au commit b35a380 servie sur 8811, puis supprimée.
- **Captures :** Chrome for Testing headless piloté par le protocole DevTools (script du scratchpad, même méthode que
  `recette.mjs`), rendu WebGL logiciel.

## ⚑ What could make it wrong
- **Mode IA non testé** (pas d'accord de dépense) : le prompt est mis à jour, la réponse réelle d'un modèle ne l'est pas.
- **Lisibilité jugée par un agent**, pas par un·e élu·e.
- **Captures « avant » de l'assistant** : faites avant redémarrage du chatbot. Celle de P2-8 vient de la recette
  (figure 14), car la copie temporaire de la page passait par le chatbot déjà corrigé.

## → What it changes
- `v2/prototype-carte/index.html`, `v2/prototype-carte/server.py` (`_objectif`, message 400), `chatbot/chat/agent.py`,
  `chatbot/passerelle/requetes.py`, `chatbot/passerelle/correspondances.yaml`, `v2/langage/glossaire.yaml` (textes
  seulement).
- Démo : la comparaison en vue Couverture et l'exemple 2 sont de nouveau montrables.
- Registre : entrée « Corrections de la recette : méthode repliée, temps de médecin dit à part, O2 dans le texte de
  périmètre ».

## ? Next
| Item | Cost |
|---|---|
| P2-14 : rétablir « A+ » ou retirer R25, sur décision | ~10 min Claude après la décision |
| P2-10 : couverture et fourchette 2050 dans toutes les vues de la comparaison, contrôle mobile | ~25 min Claude |
| P2-5 (fond) : relier les ETP aux vaccinations par une durée par acte sourcée (session besoin) | ~30 min Claude + une source |
| Recette du mode IA sur les mêmes reproductions | ~10 min Claude + quelques centimes d'API, sur accord |
