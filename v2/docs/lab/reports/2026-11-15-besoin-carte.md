---
date: 2026-11-15
type: analysis
headline: "/api/couverture 28,8 ms au 95ᵉ centile (n = 60) ; L23 : C pharmaciens France 2050 1,013 → 1,006 (−0,7 %), 495 ETP-équivalents de MG libérés ; L23 = 0 ⇒ écart 0"
status: fait, branche claude/besoin-carte-api-6d9504 (non fusionnée)
author: session besoin-carte
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

# Besoin → carte : vue « Couverture » et levier L23 de bout en bout

D'après le [plan](../derivations/2026-11-15-besoin-carte-plan.md). Branches fusionnées avant : `besoin-v2-m1-m3`
(estimateurs) et `licences-et-carte` (plan) — déjà contenues dans la branche de départ.

## Ce qui est branché

| Couche | Ajout |
|---|---|
| `v2/besoin/transferts.py` | étape 0 du plan : `s_∞` 0,74 et `τ` 2,4 ans **mesurés** (P-B6, série nationale) ; `a`, `k`, `μ` **supposés**, sources réécrites |
| `server.py` | `GET /api/couverture?prof&leviers&l23=0|1[&l23_a&l23_k]` : `cb` (tendanciel), `cs` (scénario), `ecart` (= cs/cb − 1), `min`/`max` entre estimateurs survivants, par département, région (rapport des sommes) et France ; bloc `l23` (paramètres avec statut et source, `etp_liberes_source`, `etp_recus_cible`, `actes_mg_liberes`) ; `en_attente` : M4 « en attente de validation (P-B4) » ; 400 pour MG et spécialistes |
| `index.html` | bouton « Couverture » ; échelle divergente centrée sur 1 ; infobulle « indice … (référence : 2026) · écart au tendanciel · fourchette » ; famille « Transférer des tâches ? » (case L23, réglages experts a et k aux bornes des fiches, paramètres étiquetés) ; fiche : indice 2035 et année affichée, fourchette, estimateur central, M4 en attente, ligne « actes de MG libérés » ; export CSV : mêmes lignes et sources ; contexte de l'assistant : transferts et paramètres L23, jamais d'indice MG |
| `tests/couverture.py` | critères K1–K6 ci-dessous, résultats dans `v2/artifacts/besoin_carte/results.json` |

Calcul : C(T,t) = [S(T,t)/B(T,t)] / [S_tend(T,2026)/B_tend(T,2026)]. S = séries `b`/`s` déjà calculées par
`carte()` (aucun second passage du jumeau) ; B = `besoin_api` sur les états de base, mis en cache au démarrage
(8,5 s, 11 estimations) car le besoin ne dépend pas des leviers d'offre.

Estimateurs servis : IDE M1, M2a, M3 ; MK, CD, SF M1, M2a ; PH M1 seul (M2a n'a pas de pharmaciens ; M3 réservé
aux IDE). Central : M1.

## Critères (mesurés, `uv run python v2/prototype-carte/tests/couverture.py`)

| # | Critère | Mesure | |
|---|---|---|---|
| K1 | O2 : MG, spécialistes | 400 et 400 ; aucune clé `medecine-generale`/`specialistes` hors du bloc `transferts` | ✅ |
| K2 | sans levier : C scénario = C tendanciel ; C₂₀₂₆ = 1 | écart max 0,0 (5 professions, 101 dép. + France) | ✅ |
| K3 | L23 = 0 ⇒ couverture identique au tendanciel du même scénario | écart 0,0 (quotas × 1,3, retraite + 2 ans) ; les leviers d'offre, eux, bougent C (0,29) | ✅ |
| K4 | L23 = 1 change C des pharmaciens ; statuts | C France 2050 1,0126 → 1,0056 ; 495 ETP-équivalents et 1,92 M injections de MG libérés en 2050 ; 6 paramètres étiquetés | ✅ |
| K5 | latence `/api/couverture` < 150 ms au p95, n ≥ 30 | **p95 28,8 ms**, p50 22,0, max 32,8 (n = 60, leviers et professions variés, HTTP local) ; premier passage d'un jeu de leviers exclu et déclaré : jusqu'à 263 ms (trajectoire du jumeau) | ✅ |
| K6 | lexique | aucun terme interdit dans `index.html` | ✅ |
| — | `besoin.tests` | 15/15 | ✅ |
| — | `jumeau.check` | aucun échec (lancé depuis le dépôt principal : `data/raw/` absent du worktree) | ✅ |

Capture (navigateur intégré, Puy-de-Dôme, pharmaciens, L23 actif) :
![[2026-11-15-besoin-carte-couverture-l23.jpg]]

## Écarts au plan (registre)

- **Couleur de la vue** = C scénario − 1 (évolution de la couverture par rapport à 2026) ; l'écart au tendanciel
  (relatif) est dans l'infobulle, la fiche et l'export. Une carte colorée par l'écart seul est uniforme sans levier.
- **L23 n'agit qu'avec M1** : M2a et M3 ne portent pas la MG (source). Pour les pharmaciens, M1 est le seul
  estimateur : pas de fourchette de modèle, ce que la légende dit.
- **Actes de MG libérés** = s(t) × 2,6 M injections en consultation (Cour des comptes, 2018) : dérivé, pas mesuré.
- **Assistant** : le contexte envoyé au chatbot porte `transferts` et les paramètres L23 ; l'étape 5 du plan
  (lexique d'intentions dans `v2/langage/`, gabarit `chatbot/`) n'est **pas faite** — hors périmètre de cette session.
- **Critère 2 du plan** (cinq valeurs identiques à 1e-9 : API, carte, fiche, export, assistant) : la page affiche les
  valeurs de l'API sans recalcul ; pas de test automatique d'égalité sur les cinq canaux.

## ⚑ Ce qui pourrait rendre ce résultat faux

- `a` = 0,01 du temps de MG et `k` = 1 sont supposés : l'effet de L23 (−0,7 %) est un ordre de grandeur.
- Double compte possible : le recours de base (DAMIR 2025) contient déjà le transfert commencé en 2019 ; L23 à
  t₀ = 2026 se lit comme un transfert supplémentaire de même forme.
- Le cache du besoin suppose le scénario de population central ; changer `pop_scen` change S (densité) mais pas B.

## → Ce que ça change

Le module de besoin est visible dans la carte ; M4 a son emplacement. Fusion de la branche à décider.

## ? À étudier ensuite

- Lexique d'intentions L23 dans `v2/langage/` et gabarit du chatbot (≈ 15 min, autre session).
- B dépendant de `pop_scen` (≈ 10 min : clé de cache par scénario de population).
- Test d'égalité API = fiche = export (≈ 15 min, recette navigateur).
