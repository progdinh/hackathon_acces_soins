# Vidéo de présentation — Offre libérale 2050

Vidéo motion de 57 s (1920×1080, 30 i/s) pour le jury, en Remotion, avec une voix off IA en français.

## Plan
| # | Temps | Scène | Ce qu'on voit |
|---|---|---|---|
| 1 | 0–6,5 s | Accroche | « En 2050, combien de kinés / infirmiers / sages-femmes… », carte des départements tracée puis colorée |
| 2 | 6,5–14,5 s | Promesse | Marque « Offre libérale 2050 », 5 professions · 2026 → 2050 · données ouvertes |
| 3 | 14,5–27 s | 01 Explorer le territoire | Captures France → Auvergne-Rhône-Alpes → Puy-de-Dôme ; fiche kinés 1 071 → 1 731, fourchette |
| 4 | 27–40,5 s | 02 Simuler une politique | Clic sur « Former 20 % de plus », volet avant/après, +19 110 en 2050, délai et statut du levier |
| 5 | 40,5–46,8 s | 03 Une phrase | Saisie de la phrase, « Ce que j'ai compris », confirmation |
| 6 | 46,8–56,8 s | Clôture | Données ouvertes · hypothèses sourcées · pas de boîte noire ; marque et accroche |

## Refaire la vidéo
```bash
cd v2/video
npm install
# 1. captures (la carte doit tourner : uv run python v2/prototype-carte/server.py 8767)
npm run capture
# 2. aperçu interactif
npm run dev
# 3. rendu
npm run render                                        # out/pitch.mp4 (avec musique)
npx remotion render src/index.ts Pitch out/pitch-sans-musique.mp4 --props=out/props-nobgm.json
```
Le fichier `out/props-nobgm.json` contient `{"bgm":false,"subtitles":true}`. Sous Windows, passez les props par fichier : la ligne de commande retire les guillemets du JSON.

## Fichiers
- `src/Pitch.tsx`
  - `SHOTS` : seule table de minutage, en secondes de voix (`v(sec)`).
  - Scènes et sous-titres, générés depuis `src/voix-words.json`.
- `src/parts.tsx` : briques visuelles.
  - Mots qui entrent depuis un flou, fente de mots qui défilent.
  - Carte tracée, caméra sur capture, cadres de mise en évidence, curseur.
- `src/tokens.ts` : tokens repris de la carte (IBM Plex, couleurs, courbes de mouvement).
- `capture/capture.mjs` : captures 2x et `src/layout.json`.
- `capture/france_paths.py` : contours simplifiés des départements depuis `app/assets/` (IGN/Etalab).
- `src/lib/` : composants copiés de video-shotcraft (licence Apache-2.0).

## Sources des médias
- Voix : ElevenLabs, voix « Perle | Premium French Corporate Voice », modèle eleven_v4. Le texte est dans la décision du 2026-11-14 (`v2/docs/lab/decisions.md`).
- Musique : « House Vibez » (Lily J), Mixkit Stock Music Free License, sans attribution.
- Chiffres : ceux affichés par la carte de décision au 2026-11-14.
  - Kinés, Puy-de-Dôme : 1 071 en 2026, 1 731 en 2050 (fourchette 1 244 – 2 219).
  - Préréglage « Former 20 % de plus » : +19 110 en France en 2050.
- Licence Remotion : gratuite pour les particuliers et les petites équipes.
