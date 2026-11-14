// Tokens visuels repris de la carte de décision (v2/prototype-carte/index.html).
import { Easing } from 'remotion';
import { loadFont as loadSans } from '@remotion/google-fonts/IBMPlexSans';
import { loadFont as loadMono } from '@remotion/google-fonts/IBMPlexMono';

export const SANS = loadSans('normal', { weights: ['400', '500', '600'], subsets: ['latin', 'latin-ext'] }).fontFamily;
export const MONO = loadMono('normal', { weights: ['400', '500'], subsets: ['latin', 'latin-ext'] }).fontFamily;

export const C = {
  ground: '#F4F5F2',
  sea: '#D5DADF',
  panel: '#FFFFFF',
  ink: '#16181A',
  mute: '#5C6166',
  faint: '#8A8F94',
  line: '#DCDED8',
  sel: '#1B3A8C',
  // professions
  sf: '#7A4E8C',
  dent: '#2F6A8A',
  pharma: '#8A6A1E',
  kine: '#3D4F9E',
  inf: '#2E7D6B',
};
// échelle de la carte, ocre -> encre bleue (jamais rouge/vert)
export const SCALE = ['#8C5A1B', '#B88A4E', '#DCC39C', '#C4C2B8', '#A9B6D6', '#6A80B8', '#1B3A8C'];

// Mouvement : courbe de la carte cubic-bezier(.16,1,.3,1) ; préset "professionnel" ~21f sans rebond.
export const EASE = Easing.bezier(0.16, 1, 0.3, 1);
export const EASE_IO = Easing.bezier(0.65, 0, 0.35, 1);
export const FPS = 30;
