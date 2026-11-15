---
type: analysis
date: 2026-11-15
author: session uat-application
question: "Les trois personas (ARS/DG, Administration, élu·e) accomplissent-elles leur mission sur toute l'application (carte, assistant de simulation, module de besoin), et que reste-t-il à corriger avant la démo ?"
headline: "0 P0, 6 P1, 17 P2 ; scores : ARS/DG 4/6, Administration 4,5/5, élu·e 3/5, module de besoin 5,5/7 ; chiffres identiques entre carte, fiche, export et assistant (Puy-de-Dôme, pharmaciens, 2035 : 781, couverture 0,98, −0,7 %)"
status: done
professions: [sages-femmes, dentistes, pharmaciens, kines, infirmiers]
hypothesis: "UAT, pas d'hypothèse"
sources: ["carte v2/prototype-carte (commit 6a49486)", "assistant chatbot/ en mode sans IA", "/api/carte, /api/couverture, /api/scenario, /api/agent"]
tags: [uat, carte, assistant, besoin, personas]
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

# UAT de l'application : carte, assistant, module de besoin

> **Headline :** aucun P0, 6 P1 et 17 P2. Scores (réussite = 1, partielle = 0,5) : ARS/DG 4/6, Administration 4,5/5,
> élu·e 3/5, module de besoin 5,5/7. Sur la question du sujet (pharmaciens, Puy-de-Dôme, 2035, vaccination en
> officine), la carte, la fiche, l'export CSV et l'assistant donnent les mêmes chiffres : effectif 781 (755–807),
> couverture 0,98 contre 0,99 au tendanciel, soit −0,7 %. Les P1 portent sur des textes contradictoires, un
> « −NaN % » dans la comparaison, un territoire mal affiché par l'assistant et un doute de modèle sur la date de
> départ de L23.

## Question
Les trois personas de `CLAUDE.md` peuvent-elles mener leur parcours de bout en bout sur toute l'application ? Le
module de besoin respecte-t-il les décisions du registre : O2, libellés « demande de soins de ville », M4 en
attente, L23 en langue courante ? Méthode et grille P0/P1/P2 reprises de
[`2026-11-14-uat-carte-v2`](2026-11-14-uat-carte-v2.md) et [`2026-11-14-uat-interface`](2026-11-14-uat-interface.md).

## Méthode
- **Branche testée :** `claude/uat-application-d7ed57`, au commit `6a49486` (même contenu que
  `claude/besoin-derivation-4a2fe6`). Données brutes branchées par lien symbolique, retiré à la fin.
- **Serveurs, ports libres :**
  - carte sur 8781 ;
  - passerelle du chatbot sur 8782 (`JUMEAU_REPO` = cette branche, `CARTE_URL` = 8781) ;
  - chatbot **sans IA** sur 8783, clés d'API retirées de l'environnement.
- **Mode IA non testé.** Une clé existe dans le `.env` du dépôt principal, mais un appel payant demande l'accord
  de l'utilisateur·rice, qui n'a pas été donné.
- **Un onglet isolé par persona** dans le navigateur intégré : ARS/DG dans l'onglet 3, Administration dans les
  onglets 4 et 5.
  - Le panneau du navigateur a été masqué en cours de recette. La suite a donc été menée par le DOM, et les
    captures ont été faites dans un Chrome headless piloté par le protocole DevTools : script maison du même type
    que `recette.mjs`, rendu WebGL logiciel.
  - Les effectifs à « 0 » vus dans l'onglet masqué viennent de l'animation des chiffres, qui attend
    `requestAnimationFrame`. On ne les retrouve pas en headless : **ce n'est pas un constat**.
- **Assistant :** 8 questions, dont les 3 exemples et la question du sujet. Chacune est posée deux fois, pour lire la
  réponse et pour cliquer « Afficher ce scénario sur la carte ».
- **Recette automatique :** `recette.mjs --option1` sur 8781 (46 contrôles).
- **Latences :** `urllib`, n = 20 par point d'accès, au p50 et au p95, **mesurées** pendant que d'autres scripts
  headless tournaient (charge partielle). Les durées de l'assistant sont celles qu'il affiche (champ `secondes`).
- **Limites :**
  - le testeur est un agent, pas un utilisateur réel ;
  - les durées perçues des tâches ne sont pas chronométrées ;
  - le parcours clavier complet n'a pas été fait (voir « Non testé »).

## Résultat

### Scores par persona

| Persona | Tâche | Réussite |
|---|---|---|
| ARS/DG | Zoom commune (Clermont-Ferrand) | **non** : « Aucun territoire trouvé · Grain communal : à venir » (P1-5) |
| ARS/DG | Zoom département (Puy-de-Dôme) | oui |
| ARS/DG | Zoom région (fil d'Ariane → ARA) | oui |
| ARS/DG | Lecture de la fiche | partielle : jargon (P1-6), fourchette dégénérée (P2-1) |
| ARS/DG | Comparaison de territoires | partielle : « −NaN % » en vue Couverture (P1-1) |
| ARS/DG | Export de la fiche (CSV) | oui : sources, millésimes, leviers et couverture présents |
| Administration | Tous les leviers, statut et source | oui (P2-13 : badge et export divergent pour un levier) |
| Administration | Mode expert de L23 (a, k) | oui : a 0,01 → 0,05 fait passer l'écart de −0,7 % à −3,3 % |
| Administration | Lien du scénario | oui : restauré à l'identique dans un onglet neuf (L23, a, k, année, vue) |
| Administration | Export CSV | oui (P2-2, P2-3 : libellés et format) |
| Administration | Cohérence carte / fiche / export / assistant | partielle : chiffres identiques, textes contradictoires (P1-2) |
| Élu·e | Mode simple | **non** : il n'existe pas, une seule interface pour tous (P1-6) |
| Élu·e | Exemple 1 (leviers → effet) | oui : 19 300 (17 200–21 500) dans l'assistant, 19 349 (17 222–21 477) sur la carte |
| Élu·e | Exemple 2 (objectif → possibilités) | partielle : « Territoire : France » pour un calcul fait en Normandie (P1-3) ; pas de bouton carte |
| Élu·e | Exemple 3 (L23 → couverture) | oui : 0,98, −0,7 %, identique sur la carte après clic |
| Élu·e | Lisibilité | partielle : L23, M1, M2a, DCIR, P-B4, s_inf (P1-6, P2-2) |
| Besoin | Vue Couverture | oui |
| Besoin | Fourchette entre estimateurs | partielle : affichée « 1,22 – 1,22 » alors que `fourchette_visible` = false (P2-1) |
| Besoin | L23 actif / inactif, simple et expert | oui (P2-6 : résumé « tendance » avec L23 actif) |
| Besoin | Règle O2 (MG, spécialistes) | oui : API → 400, carte → retour aux kinés avec message, assistant → refus motivé |
| Besoin | Libellés « demande de soins de ville » | partielle : « besoin » subsiste à trois endroits (P2-2) |
| Besoin | M4 « en attente » | oui : « M4 : en attente de validation (P-B4) » dans la fiche et l'export |
| Besoin | Question du sujet | partielle : les pharmaciens et Clermont → Puy-de-Dôme passent ; les spécialistes sont refusés avec un texte périmé (P2-8) ; doute de modèle (P1-4) |

**Scores :** ARS/DG 4/6 · Administration 4,5/5 · élu·e 3/5 · module de besoin 5,5/7.

### Constats

Repro : chaque URL part de `http://localhost:8781/`. `L` désigne la chaîne de leviers par défaut copiée par
« Lien du scénario ».

| # | Gr. | Constat | Reproduction pas à pas | Capture | Piste de correction |
|---|---|---|---|---|---|
| P1-1 | **P1** | Vue Couverture : la comparaison affiche « Écart tend. −NaN % » pour chaque territoire, à toutes les années, avec ou sans L23 | 1. Pharmaciens, Puy-de-Dôme. 2. Indicateur « Couverture ». 3. « Ajouter à la comparaison », puis l'onglet « Comparer ». Mesuré en 2035 et 2050 ; vues Variation, Écart et Densité correctes | [09](../figures/2026-11-15-uat-app-09-comparaison-nan.jpg) | `renderCmp` calcule la colonne avec `raw()`, qui renvoie NaN quand `d.cy` manque : lire `COUV` pour chaque territoire comparé, ou afficher « — » |
| P1-2 | **P1** | La page dit à la fois que la vaccination en officine est modélisée et qu'elle ne l'est pas | 1. Pharmaciens, Puy-de-Dôme, cocher « Les pharmaciens vaccinent davantage contre la grippe ». 2. Ouvrir « Plus : phrase, résumé, actions » : « Pas encore dans le modèle : … transferts de tâches (vaccination en officine, …) ». 3. Export CSV : « Limites : … transferts de tâches non modélisés », trois lignes au-dessus du bloc L23 actif | [06](../figures/2026-11-15-uat-app-06-vaccination-non-modelisee.jpg) | Retirer « vaccination en officine » de `#nonmod` (index.html, l. 803) et des limites de l'export ; écrire « autres transferts de tâches (IPA…) » |
| P1-3 | **P1** | Exemple 2 de l'assistant : l'encadré « Ce que l'assistant a compris » affiche « Territoire : France · Pharmaciens », alors que le calcul porte sur la Normandie (94,3 → 110,6 pour 100 000 = valeurs R28 de `/api/scenario`, contre 93,4 → 97,8 pour la France) | Assistant → exemple « Comment atteindre +10 % de densité de pharmaciens en Normandie d'ici 2040 ? » ; `/api/agent` renvoie `objectif.terr = "FR"` | [11](../figures/2026-11-15-uat-app-11-assistant-ex2-territoire.jpg) | Passerelle ou compilateur : renseigner `objectif.terr` avec le territoire résolu (R28) ; ajouter un bouton « Afficher sur la carte » pour le levier suffisant |
| P1-4 | **P1** (modèle, à confirmer) | L23 rejoue à partir de 2026 la montée en charge mesurée depuis 2019 : s∞ 0,74 et τ 2,4 ans, ajustés avec t₀ = 2019 ([P-B6](2026-11-15-besoin-p-b6-grippe-officine.md), l. 66), appliqués avec t₀ = 2026. Si la demande de base des pharmaciens contient déjà la vaccination en officine, l'effet est compté deux fois. Avec t₀ = 2019, s(2026) ≈ 0,70 (**dérivé**) : la marge restante (≈ 0,04 sur 0,72 en 2035) ne ferait qu'environ 6 % de l'effet affiché (−0,7 % ; 1,88 M vaccinations ; 468 ETP) | Lire `L23_PARAMS` et `l23(t0=2026)` dans `v2/besoin/transferts.py`, puis comparer à P-B6 | [04](../figures/2026-11-15-uat-app-04-couverture-d63-l23.jpg) | Session besoin : dire si l'année de base DCIR contient l'officine ; si oui, appliquer s(t) − s(2026), ou bien t₀ = 2019, et le libeller « au-delà de la part actuelle » |
| P1-5 | **P1** | Pas de grain communal ni de groupe de communes, alors que le recadrage du 2026-11-14 demande « toutes les échelles, jusqu'à la commune » ; le parcours ARS commence à la commune | Taper « Clermont-Ferrand » dans la recherche : « Aucun territoire trouvé · Grain communal : à venir ». L'assistant ramène bien la ville à son département et le dit | [03](../figures/2026-11-15-uat-app-03-recherche-commune.jpg), [15](../figures/2026-11-15-uat-app-15-assistant-clermont.jpg) | Arbitrer entre le recadrage (commune) et le protocole N10 (aucun grain infra-départemental fiable) ; au minimum, proposer le département de la commune dans les résultats de recherche |
| P1-6 | **P1** | Aucun mode simple pour l'élu·e ; le jargon de méthode est visible de tous dans la fiche et l'assistant : « Estimateur central M1 (norme déclarée) … DCIR, poids APL … P-B4 », « fourchette M1, M2a », « C1, axe 2 », « (L23) », « s_inf mesuré, tau mesuré » | Ouvrir n'importe quelle fiche en vue Couverture ; exemple 3 de l'assistant | [04](../figures/2026-11-15-uat-app-04-couverture-d63-l23.jpg), [12](../figures/2026-11-15-uat-app-12-assistant-ex3.jpg) | Mettre les lignes de méthode dans un `<details>` « Méthode » replié ; bascule « mode simple » qui masque estimateurs, codes de protocole et paramètres |
| P2-1 | P2 | Fourchette entre estimateurs affichée même dégénérée (« fourchette M1, M2a : 1,22 – 1,22 ») alors que l'API dit `fourchette_visible: false` (seuil de 5 %) ; même chose dans l'export | Kinés, Puy-de-Dôme, vue Couverture | [08](../figures/2026-11-15-uat-app-08-fourchette-degeneree.jpg) | N'afficher la fourchette que si `fourchette_visible` (règle déjà appliquée par l'assistant) |
| P2-2 | P2 | « besoin » encore à l'écran, contre la décision « libellés alignés sur demande de soins de ville » : note du levier L23 (« une part du besoin de vaccination passe… »), export (« Norme du besoin : besoin = … », hors la mention « (norme déclarée) ») | Cocher L23 ; export CSV | [05](../figures/2026-11-15-uat-app-05-l23-reglages-experts.jpg) | « une part des vaccinations passe… » ; « Norme déclarée de l'estimateur : … » |
| P2-3 | P2 | « L23 », « MG », « t_PH / t_MG », « s_inf », « tau », « mu », « P-B6 », « fiche L23 » visibles dans le panneau (réglages experts), l'export (« L23 vaccination antigrippale en officine (actif) ») et l'assistant (« (L23) », « paramètres de L23 »), contre les décisions « transfert L23 dit en langue courante » (carte, assistant) | Cocher L23, ouvrir « Réglages experts » ; exporter ; exemple 3 | [05](../figures/2026-11-15-uat-app-05-l23-reglages-experts.jpg), [12](../figures/2026-11-15-uat-app-12-assistant-ex3.jpg) | Libellés en clair pour les paramètres (« part du temps des généralistes consacrée au vaccin »…) ; garder les codes dans une colonne « référence » |
| P2-4 | P2 | Nombres au format anglais : « a = 0.01 », « s_inf = 0.74 », « actes_mg_base = 2600000 » (panneau, export), « pente d'erreur 0.37 %/an » (export) | Idem | [05](../figures/2026-11-15-uat-app-05-l23-reglages-experts.jpg) | `toLocaleString("fr-FR")` sur `p.value` et la pente |
| P2-5 | P2 | « N vaccinations en moins, soit le temps de travail de M médecins » : les deux nombres sont indépendants (s × 2,6 M contre s × a × B_MG). En mode expert, a = 0,05 donne les mêmes 1 878 752 vaccinations pour 2 340 ETP, soit ≈ 2 h par vaccination (**dérivé**, 1 600 h par ETP **supposé**) ; à a = 0,01, ≈ 24 min. Chiffre national dans une fiche départementale | Réglages experts, a = 0,05 | [05](../figures/2026-11-15-uat-app-05-l23-reglages-experts.jpg) | Relier les ETP aux vaccinations par une durée par acte sourcée, ou remplacer « soit » par « et » ; resserrer la borne haute de a |
| P2-6 | P2 | Avec L23 actif, le résumé du panneau reste « Scénario · tendance » ; l'encadré de l'exemple 3 dit « Leviers : aucun : tendance sans nouvelle politique » et le graphique « aucun levier » | Cocher L23, replier le panneau ; exemple 3 | [12](../figures/2026-11-15-uat-app-12-assistant-ex3.jpg), [17](../figures/2026-11-15-uat-app-17-mobile-fiche.jpg) | Compter L23 dans `changedN()` ; ajouter une ligne « Transfert » à `askPlan` |
| P2-7 | P2 | Légende de la vue Couverture graduée en « % » de −50 à +50 alors que la valeur affichée est un indice (« Puy-de-Dôme 0,98 ») ; pastille « Couverture2050 » sans espace | Vue Couverture | [04](../figures/2026-11-15-uat-app-04-couverture-d63-l23.jpg), [01](../figures/2026-11-15-uat-app-01-accueil.jpg) | Graduer en indice (0,5 à 1,5) ou afficher « −2 % » ; espace insécable avant `<span class="yl">` |
| P2-8 | P2 | La question du sujet avec « spécialistes » reçoit « spécialités … prévues en phase 2, non construites » : texte périmé depuis la décision du 2026-11-15 (amélioration possible, hors plan). Toute la question est refusée, la partie pharmaciens comprise | Assistant : « Si les pharmaciens peuvent vacciner, combien de spécialistes à Clermont-Ferrand en 2035 ? » | [14](../figures/2026-11-15-uat-app-14-assistant-specialistes.jpg) | Mettre à jour le texte de périmètre du chatbot ; proposer la reformulation « pharmaciens à Clermont-Ferrand » |
| P2-9 | P2 | Description du modèle incohérente : l'export dit « jumeau v2, stock-flux à taux locaux », l'assistant « Modèle bayésien hiérarchique (cohortes… C1, axe 2) », pour les mêmes chiffres | Export CSV ; encadré « Calcul » de l'assistant | [12](../figures/2026-11-15-uat-app-12-assistant-ex3.jpg) | Un seul libellé de modèle, lu dans `/api/meta` |
| P2-10 | P2 | Comparaison sans couverture ni fourchette (déjà vu le 2026-11-14) | Comparer deux départements | [09](../figures/2026-11-15-uat-app-09-comparaison-nan.jpg) | Colonne « Couverture » et fourchette 2050 |
| P2-11 | P2 | Le statut du levier « Les professionnels bloqués… » est « effet supposé » à l'écran et « effet non mesurable » dans l'export (déjà vu le 2026-11-14) | Panneau « Réguler l'installation » ; export | [01](../figures/2026-11-15-uat-app-01-accueil.jpg) | Troisième badge « non mesurable » |
| P2-12 | P2 | `/api/couverture?prof=xyz` répond « pas d'indice de couverture pour 'xyz' (sources de transferts seulement) » : profession inconnue confondue avec une profession O2 | curl | — | 400 « profession inconnue » hors `SANS_COUVERTURE` |
| P2-13 | P2 | Accessibilité : champ « phrase » `#nlq` sans libellé (placeholder seul) ; carte libellée « Map » en anglais ; curseurs sans `aria-valuetext` (un lecteur d'écran lit « 1 », pas « autant qu'aujourd'hui ») ; aucun `h1` | Inspection du DOM | — | `aria-label` ; `aria-valuetext` = phrase du levier ; `h1` = titre du bandeau |
| P2-14 | P2 | Le bouton « A+ » (texte agrandi) a disparu : `recette.mjs` R25 échoue (45/46) | `node v2/prototype-carte/recette.mjs http://localhost:8781/ --option1` | — | Rétablir A+ ou retirer R25 de la recette, avec une décision |
| P2-15 | P2 | Après la navigation par le fil d'Ariane vers la région, la recherche affiche encore « Puy-de-Dôme » | Rechercher Puy-de-Dôme, puis cliquer « Auvergne-Rhône-Alpes » | [10](../figures/2026-11-15-uat-app-10-assistant-ex1-carte.jpg) | Vider ou synchroniser `#q` dans `select()` |
| P2-16 | P2 | « Diplômés installés en libéral : 107 % » : une part supérieure à 100 % sans explication courte | Fiche kinés | [01](../figures/2026-11-15-uat-app-01-accueil.jpg) | Expliquer en une ligne (installés venus d'autres cohortes) ou parler de « rapport » |
| P2-17 | P2 | Assistant : « Ce que l'assistant a compris » puis « Ce que j'ai compris » répètent la même chose ; « +2 an(s) » ; dans l'exemple 2, la ligne « +35 % (région seulement) » donne le même résultat que la ligne nationale, en doublon | Exemples 1 et 2 | [10](../figures/2026-11-15-uat-app-10-assistant-ex1-carte.jpg), [11](../figures/2026-11-15-uat-app-11-assistant-ex2-territoire.jpg) | Supprimer la phrase redondante ; accorder « ans » ; fusionner les lignes identiques |

**Constats de l'UAT du 2026-11-14 qui ne se reproduisent plus :**
- P0 : le sélecteur de profession est accessible sur mobile (`scrollWidth` = 375 à 375 px).
- P1 : le retour à la France retire « quotas régionaux » et l'annonce par un message.
- P1 : l'export contient sources, millésimes et statut de chaque levier.
- P1 : les infirmiers sont projetés et le périmètre le dit.

### Cohérence des chiffres (Administration)

| Grandeur (pharmaciens, Puy-de-Dôme, 2035, L23 actif) | Carte (fiche) | Export CSV | Assistant | API |
|---|---|---|---|---|
| Effectif | 781 (755–807) | 780,8 (755,0–806,6) | 781 (755–807) | — |
| Couverture | 0,98 ; tendanciel 0,99 | 0,98 ; 0,99 | 0,98 ; 0,99 | — |
| Écart au tendanciel | −0,7 % | −0,7 % | −0,7 % | — |
| Vaccinations reprises, ETP | 1 878 752 ; 468 | 1 878 752 ; 468 | 1 878 752 ; 468 | — |
| Kinés, couverture, France 2050 | 1,34 | — | — | `fr.cs` = 1,3396 |
| Kinés, couverture, Puy-de-Dôme 2050 | 1,43 | — | — | `deps.63.cs` = 1,4269 |
| Kinés, ARA 2040, exemple 1 | 19 349 (17 222–21 477), écart +1 550 | — | 19 300 (17 200–21 500), tendanciel 17 800 | — |

Tous les chiffres concordent (**mesuré**). Avec L23 actif, l'écart de couverture des kinés vaut 0, comme le dit la
note du levier.

### Latences (mesurées)

| Point d'accès | p50 | p95 |
|---|---|---|
| `/api/couverture` (pharmaciens, L23) | 16,8 ms | 18,4 ms |
| `/api/couverture` (kinés, quotas × 1,2, L23) | 17,3 ms | 22,9 ms |
| `/api/carte` (pharmaciens, D63) | 74,3 ms | 120,5 ms |
| `/api/scenario` (pharmaciens, D63) | 51,9 ms | 214,5 ms |
| `/api/meta` | 9,6 ms | 15,2 ms |

- **Assistant sans IA :** 0,06 à 2,1 s par réponse (champ `secondes`). La question d'objectif (exemple 2) est la
  plus lente, 2,1 s.
- **Chargement de la page en headless** (jusqu'à `META`, carte et style prêts) : 2,0 à 2,7 s ; 5,5 à 6,8 s au
  premier chargement à froid.
- **Toutes les latences de calcul restent sous 2 s.**

### Transverse
- **Console et réseau :** aucune erreur et aucune réponse ≥ 400 non voulue sur les 30 chargements headless. Les
  journaux de la carte et de la passerelle n'ont aucune erreur. Les seules réponses 400 sont les refus O2,
  attendus.
- **Mobile (375 × 812) :**
  - pas de défilement horizontal (`scrollWidth` 375) ;
  - l'assistant s'ouvre en plein écran (375 × 812) et reste lisible ;
  - la légende masque le bas de la carte, mais la page défile ([16](../figures/2026-11-15-uat-app-16-mobile-accueil.jpg),
    [17](../figures/2026-11-15-uat-app-17-mobile-fiche.jpg), [18](../figures/2026-11-15-uat-app-18-mobile-assistant.jpg)).
- **Lexique neutre :** aucun terme de la liste « à éviter » dans les réponses de l'assistant (contrôle du lexique
  au vert). Dans la page, seul « zone sous-dotée » apparaît : c'est un terme réglementaire du zonage, cité dans
  `#nonmod`.
- **Accessibilité de base :** voir P2-13. Le reste est correct : `lang="fr"`, curseurs et listes nommés,
  `role="combobox"` sur la recherche, aucun `tabindex` positif, dialogue de l'assistant en `<dialog>` modal
  refermable par Échap (lecture du code).

## How
- **Données :** API de la carte au commit `6a49486`, données brutes de la machine par lien symbolique.
- **Méthode :** parcours dans le navigateur intégré, puis Chrome headless (CDP), `recette.mjs`, `urllib`. Les
  scripts de capture sont restés dans le scratchpad de la session ; ils ne sont pas commités.

## ⚑ What could make it wrong
- **Agent, pas utilisateur.** La lisibilité pour un·e élu·e est jugée par lecture, pas observée.
- **P1-4 est une inférence.** Elle vient du code et du rapport P-B6. La présence de l'officine dans l'année de
  base n'a pas été vérifiée dans les données.
- **Mode IA non testé.** Les réponses peuvent différer : encadré, libellés, refus O2.
- **Panneau masqué.** Une partie des contrôles a été faite par le DOM ; les captures viennent du headless, avec un
  rendu logiciel.

## → What it changes
- **Carte, `v2/prototype-carte/index.html` :** P1-1 (`renderCmp`), P1-2 (`#nonmod` et limites de l'export), P1-6
  (mode simple), P2-1 à P2-7.
- **Chatbot, `chatbot/` (passerelle et texte de périmètre) :** P1-3, P2-8, P2-3.
- **Module de besoin, `v2/besoin/transferts.py` :** P1-4, à trancher par la session besoin avant toute démo de la
  question du sujet.
- **Démo :** l'exemple 3 et la question du sujet passent de bout en bout. À éviter tant que P1-1 et P1-3 ne sont
  pas corrigés : la comparaison en vue Couverture et l'exemple 2.

## ? Next
| Item | Cost |
|---|---|
| Corriger P1-1, P1-2, P2-1, P2-6, P2-7 (carte) | ~30 min Claude |
| P1-3 (`objectif.terr`) et P2-8 (texte de périmètre) dans `chatbot/` | ~20 min Claude |
| P1-4 : vérifier l'officine dans l'année de base DCIR, puis choisir le t₀ de L23 | ~30 min Claude, puis une décision |
| P1-6 : mode simple (méthode repliée, codes masqués) | ~45 min Claude |
| UAT du mode IA (3 exemples et question du sujet, Haiku) | ~10 min Claude, quelques centimes d'API, sur accord |

## Non testé
- **Mode IA de l'assistant :** clé présente, mais coût non autorisé.
- **Parcours clavier complet** (Tab sur toute la page, ordre et focus visible) et lecteur d'écran réel.
- **Navigateurs :** Firefox et Safari ; vrai téléphone ; zoom du navigateur à 200 %.
- **Persona Administration :** combinaisons de leviers aux bornes, rafales de curseurs (faites le 2026-11-14,
  non refaites).
- **Professions :** sages-femmes, dentistes et infirmiers en vue Couverture, vus seulement par l'API. M3 pour les
  infirmiers n'est pas vérifié dans la fiche.
- **Durées perçues par tâche :** non chronométrées.
