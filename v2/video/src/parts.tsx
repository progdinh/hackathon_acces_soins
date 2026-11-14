// Briques visuelles habillées aux tokens de la carte.
import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, Img, staticFile } from 'remotion';
import { C, SANS, MONO, EASE, SCALE } from './tokens';
import { mulberry32 } from './lib/helpers/rand';
import FRANCE from './france.json';

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;
export const ramp = (f: number, a: number, b: number, ease = EASE) =>
  interpolate(f, [a, b], [0, 1], { ...clamp, easing: ease });

/** Mot qui entre en glissant depuis un léger flou (type blur-slide). */
export const BlurWord: React.FC<{ at: number; children: React.ReactNode; dur?: number; dy?: number; style?: React.CSSProperties }> = ({ at, children, dur = 18, dy = 28, style }) => {
  const f = useCurrentFrame();
  const t = ramp(f, at, at + dur);
  return (
    <span style={{ display: 'inline-block', opacity: t, transform: `translateY(${(1 - t) * dy}px)`, filter: `blur(${(1 - t) * 10}px)`, ...style }}>
      {children}
    </span>
  );
};

/** Ligne de mots, chaque mot décalé de `stagger` images. */
export const BlurLine: React.FC<{ at: number; text: string; stagger?: number; style?: React.CSSProperties; wordStyle?: (w: string, i: number) => React.CSSProperties | undefined }> = ({ at, text, stagger = 4, style, wordStyle }) => (
  <div style={style}>
    {text.split(' ').map((w, i) => (
      <React.Fragment key={i}>
        <BlurWord at={at + i * stagger} style={wordStyle?.(w, i)}>{w}</BlurWord>{' '}
      </React.Fragment>
    ))}
  </div>
);

/** Fente verticale qui fait défiler des mots (pill-slot-cycle) ; chaque mot a sa couleur. */
export const SlotWord: React.FC<{ items: { w: string; at: number; color: string }[]; fontSize: number }> = ({ items, fontSize }) => {
  const f = useCurrentFrame();
  const h = fontSize * 1.18;
  let idx = 0;
  items.forEach((it, i) => { if (f >= it.at) idx = i; });
  const prev = items[Math.max(0, idx - 1)];
  const cur = items[idx];
  const t = idx === 0 ? ramp(f, cur.at, cur.at + 14) : ramp(f, cur.at, cur.at + 12);
  const width = Math.max(...items.map((i) => i.w.length)) * fontSize * 0.56;
  const cell = (it: typeof cur, y: number, o: number) => (
    <span style={{ position: 'absolute', left: 0, top: 0, transform: `translateY(${y}px)`, opacity: o, color: it.color, whiteSpace: 'nowrap', fontWeight: 600 }}>{it.w}</span>
  );
  return (
    <span style={{ position: 'relative', display: 'inline-block', height: h, width, overflow: 'hidden', verticalAlign: 'bottom' }}>
      {idx > 0 && cell(prev, -t * h, 1 - t)}
      {cell(cur, (1 - t) * h, idx === 0 ? t : 1)}
    </span>
  );
};

/** Carte de France des départements : tracé du contour puis remplissage en échelle ocre → bleu. */
export const FranceMap: React.FC<{ size: number; drawAt: number; fillAt: number; stroke?: string }> = ({ size, drawAt, fillAt, stroke = C.ink }) => {
  const f = useCurrentFrame();
  const rnd = mulberry32(7);
  return (
    <svg viewBox="0 0 1000 1000" width={size} height={size} style={{ overflow: 'visible' }}>
      {(FRANCE as { code: string; d: string }[]).map((d, i) => {
        const r = rnd();
        const order = (i / FRANCE.length) * 30;
        const draw = ramp(f, drawAt + order, drawAt + order + 40);
        const fill = ramp(f, fillAt + r * 40, fillAt + r * 40 + 24);
        const col = SCALE[Math.min(SCALE.length - 1, Math.floor(rnd() * SCALE.length))];
        return (
          <path key={d.code} d={d.d} pathLength={1} fill={col} fillOpacity={fill * 0.95}
            stroke={stroke} strokeOpacity={0.55 - fill * 0.25} strokeWidth={1.1}
            strokeDasharray={1} strokeDashoffset={1 - draw} strokeLinejoin="round" />
        );
      })}
    </svg>
  );
};

/** Marque de l'outil, comme dans l'en-tête de la carte. */
export const Wordmark: React.FC<{ size: number; at: number }> = ({ size, at }) => {
  const f = useCurrentFrame();
  const sq = ramp(f, at, at + 16);
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: size * 0.42, fontFamily: SANS, fontWeight: 600, fontSize: size, color: C.ink, letterSpacing: '-0.02em' }}>
      <span style={{ width: size * 0.62, height: size * 0.62, background: C.sel, borderRadius: size * 0.08, transform: `scale(${sq}) rotate(${(1 - sq) * -45}deg)` }} />
      <BlurLine at={at + 6} text="Offre libérale 2050" stagger={4} />
    </div>
  );
};

/** Pastille de chiffre clé. */
export const Chip: React.FC<{ at: number; k: string; v: string; color?: string }> = ({ at, k, v, color = C.sel }) => {
  const f = useCurrentFrame();
  const t = ramp(f, at, at + 20);
  return (
    <div style={{ opacity: t, transform: `translateY(${(1 - t) * 24}px)`, background: C.panel, border: `1px solid ${C.line}`, borderRadius: 14, padding: '22px 30px', boxShadow: '0 10px 30px rgba(22,24,26,.07)', minWidth: 300 }}>
      <div style={{ fontFamily: MONO, fontSize: 46, color, fontWeight: 500, fontVariantNumeric: 'tabular-nums' }}>{v}</div>
      <div style={{ fontFamily: SANS, fontSize: 24, color: C.mute, marginTop: 6 }}>{k}</div>
    </div>
  );
};

/** Capture plein cadre (1920x1080, texture 2x) avec caméra 2D : zoom autour de (cx, cy). */
export type Cam = { f: number; cx: number; cy: number; z: number };
export const camAt = (keys: Cam[], f: number) => {
  let a = keys[0], b = keys[keys.length - 1];
  if (f <= a.f) return a;
  if (f >= b.f) return b;
  for (let i = 0; i < keys.length - 1; i++) if (f >= keys[i].f && f <= keys[i + 1].f) { a = keys[i]; b = keys[i + 1]; break; }
  const t = interpolate(f, [a.f, b.f], [0, 1], { ...clamp, easing: EASE_CAM });
  return { f, cx: a.cx + (b.cx - a.cx) * t, cy: a.cy + (b.cy - a.cy) * t, z: a.z + (b.z - a.z) * t };
};
import { Easing } from 'remotion';
const EASE_CAM = Easing.bezier(0.33, 0, 0.15, 1);

export const Shot: React.FC<{ src: string; keys: Cam[]; opacity?: number; blur?: number; children?: React.ReactNode }> = ({ src, keys, opacity = 1, blur = 0, children }) => {
  const f = useCurrentFrame();
  const c = camAt(keys, f);
  // garde le cadre rempli (zoom >= 1, centre borné)
  const z = Math.max(1, c.z);
  const cx = Math.min(1920 - 960 / z, Math.max(960 / z, c.cx));
  const cy = Math.min(1080 - 540 / z, Math.max(540 / z, c.cy));
  return (
    <AbsoluteFill style={{ opacity, overflow: 'hidden', filter: blur ? `blur(${blur}px)` : undefined }}>
      <div style={{ position: 'absolute', width: 1920, height: 1080, transformOrigin: '0 0', transform: `translate(${960 - cx * z}px, ${540 - cy * z}px) scale(${z})` }}>
        <Img src={staticFile(`textures/${src}.png`)} style={{ width: 1920, height: 1080 }} />
        {children}
      </div>
    </AbsoluteFill>
  );
};

/** Cadre de mise en évidence (coordonnées page). */
export const Focus: React.FC<{ at: number; out?: number; x: number; y: number; w: number; h: number; color?: string }> = ({ at, out = 1e9, x, y, w, h, color = C.sel }) => {
  const f = useCurrentFrame();
  const t = ramp(f, at, at + 14) * (1 - ramp(f, out, out + 10));
  return (
    <div style={{ position: 'absolute', left: x - 6, top: y - 6, width: w + 12, height: h + 12, borderRadius: 10, border: `2.5px solid ${color}`, opacity: t, transform: `scale(${1.06 - 0.06 * t})`, boxShadow: `0 0 0 ${(1 - t) * 30}px rgba(27,58,140,0)` }} />
  );
};

/** Curseur qui glisse jusqu'à un point puis clique (onde). Coordonnées page. */
export const Cursor: React.FC<{ from: [number, number]; to: [number, number]; at: number; click: number; out?: number }> = ({ from, to, at, click, out = 1e9 }) => {
  const f = useCurrentFrame();
  const t = ramp(f, at, click - 4);
  const x = from[0] + (to[0] - from[0]) * t, y = from[1] + (to[1] - from[1]) * t;
  const press = f >= click && f < click + 6 ? 0.85 : 1;
  const r = ramp(f, click, click + 20);
  const vis = ramp(f, at - 6, at) * (1 - ramp(f, out, out + 8));
  return (
    <div style={{ position: 'absolute', left: 0, top: 0, opacity: vis }}>
      {f >= click && <div style={{ position: 'absolute', left: to[0] - 30 * r, top: to[1] - 30 * r, width: 60 * r, height: 60 * r, borderRadius: '50%', border: `2px solid ${C.sel}`, opacity: 1 - r }} />}
      <svg width={26} height={32} viewBox="0 0 26 32" style={{ position: 'absolute', left: x, top: y, transform: `scale(${press})`, transformOrigin: '0 0', filter: 'drop-shadow(0 2px 3px rgba(0,0,0,.3))' }}>
        <path d="M2 2 L2 26 L8 20 L12 30 L17 28 L13 18 L22 18 Z" fill={C.ink} stroke="#fff" strokeWidth={2} strokeLinejoin="round" />
      </svg>
    </div>
  );
};

/** Grand encart de chiffre (DigitRoll monospace). */
export { DigitRoll } from './lib/DigitRoll';
