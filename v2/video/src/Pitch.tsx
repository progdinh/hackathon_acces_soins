// Vidéo de présentation « Offre libérale 2050 » — 1920x1080, 30 i/s.
// Le temps de chaque scène est calé sur la voix off (src/voix-words.json, transcription ElevenLabs Scribe).
import React from 'react';
import { AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame } from 'remotion';
import { C, SANS, MONO, FPS } from './tokens';
import { BlurLine, BlurWord, SlotWord, FranceMap, Wordmark, Chip, Shot, Focus, Cursor, DigitRoll, ramp } from './parts';
import WORDS from './voix-words.json';

export const VO_START = 15; // la voix démarre à 0,5 s
const v = (sec: number) => Math.round(VO_START + sec * FPS); // seconde de voix -> image du film

// Table des scènes : seule source de vérité du minutage.
export const SHOTS = {
  hook: { from: 0, to: v(6.0) },
  promise: { from: v(6.0), to: v(14.0) },
  map: { from: v(14.0), to: v(26.6) },
  lever: { from: v(26.6), to: v(40.0) },
  phrase: { from: v(40.0), to: v(46.3) },
  outro: { from: v(46.3), to: v(54.44) + 60 },
};
export const TOTAL = SHOTS.outro.to;
const loc = (shot: keyof typeof SHOTS, sec: number) => v(sec) - SHOTS[shot].from; // image locale à la scène

const XF = 12; // fondu enchaîné entre scènes

const Fade: React.FC<{ dur: number; children: React.ReactNode; inF?: number; outF?: number }> = ({ dur, children, inF = XF, outF = XF }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, Math.max(inF, 0.5), dur - outF, dur], [inF ? 0 : 1, 1, 1, outF ? 0 : 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};

// ---------- 1. Accroche ----------
const Hook: React.FC = () => {
  const L = (s: number) => loc('hook', s);
  return (
    <AbsoluteFill style={{ background: C.ground }}>
      <div style={{ position: 'absolute', right: 70, top: 40 }}>
        <FranceMap size={1000} drawAt={0} fillAt={L(4.0)} />
      </div>
      <div style={{ position: 'absolute', left: 130, top: 330, fontFamily: SANS, color: C.ink, fontSize: 92, lineHeight: 1.12, letterSpacing: '-0.025em', fontWeight: 500 }}>
        <BlurLine at={L(0.1)} text="En 2050," stagger={6} wordStyle={(w) => (w === '2050,' ? { fontFamily: MONO, fontWeight: 500, color: C.sel } : undefined)} />
        <div><BlurWord at={L(1.1)}>combien de</BlurWord>{' '}</div>
        <div style={{ height: 112 }}>
          <SlotWord fontSize={92} items={[
            { w: 'kinés', at: L(1.7), color: C.kine },
            { w: 'infirmiers', at: L(2.3), color: C.inf },
            { w: 'sages-femmes', at: L(3.3), color: C.sf },
          ]} />
        </div>
        <BlurLine at={L(4.0)} text="en libéral, près de chez vous ?" stagger={3} style={{ fontSize: 56, color: C.mute, marginTop: 18 }} />
      </div>
    </AbsoluteFill>
  );
};

// ---------- 2. Promesse ----------
const Promise: React.FC = () => {
  const f = useCurrentFrame();
  const L = (s: number) => loc('promise', s);
  const up = ramp(f, L(7.6), L(8.4));
  return (
    <AbsoluteFill style={{ background: C.ground, alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ position: 'absolute', right: 70, top: 40, opacity: 0.16 }}>
        <FranceMap size={1000} drawAt={-200} fillAt={-200} />
      </div>
      <div style={{ transform: `translateY(${-up * 150}px) scale(${1 - up * 0.15})` }}>
        <Wordmark size={104} at={L(6.15)} />
      </div>
      <div style={{ position: 'absolute', top: 600, display: 'flex', gap: 36 }}>
        <Chip at={L(8.5)} v="5" k="professions de santé" />
        <Chip at={L(10.1)} v="2026 → 2050" k="projection annuelle" />
        <Chip at={L(12.9)} v="100 %" k="données ouvertes" />
      </div>
    </AbsoluteFill>
  );
};

// ---------- 3. Carte : France -> région -> département -> fiche ----------
// Coordonnées en px CSS de la capture 1920x1080 (src/layout.json).
const Map: React.FC = () => {
  const f = useCurrentFrame();
  const L = (s: number) => loc('map', s);
  const enter = ramp(f, 0, 26);
  const toReg = ramp(f, L(16.2), L(16.75));
  const toDep = ramp(f, L(17.6), L(18.15));
  return (
    <AbsoluteFill style={{ background: C.ground }}>
      <AbsoluteFill style={{ transform: `scale(${0.86 + 0.14 * enter}) translateY(${(1 - enter) * 60}px)`, borderRadius: 18 * (1 - enter), overflow: 'hidden', boxShadow: `0 30px 80px rgba(22,24,26,${0.2 * (1 - enter)})` }}>
        <Shot src="a1-france" opacity={1 - toReg} keys={[{ f: 0, cx: 1000, cy: 560, z: 1 }, { f: L(15.9), cx: 1180, cy: 560, z: 1.08 }, { f: L(16.75), cx: 1430, cy: 640, z: 2.2 }]}>
          <Focus at={L(15.9)} out={L(16.3)} x={1290} y={420} w={300} h={210} />
        </Shot>
        <Shot src="a2-region" opacity={toReg * (1 - toDep)} keys={[{ f: L(16.2), cx: 960, cy: 540, z: 1.25 }, { f: L(16.9), cx: 960, cy: 540, z: 1 }, { f: L(17.6), cx: 760, cy: 470, z: 1.12 }, { f: L(18.15), cx: 720, cy: 460, z: 2.0 }]} />
        <Shot src="a3-dep" opacity={toDep} keys={[
          { f: L(17.6), cx: 960, cy: 540, z: 1.2 }, { f: L(18.4), cx: 960, cy: 540, z: 1 },
          { f: L(19.3), cx: 1300, cy: 400, z: 1.15 }, { f: L(20.2), cx: 1560, cy: 300, z: 1.75 },
          { f: L(24.0), cx: 1580, cy: 360, z: 1.6 }, { f: L(24.9), cx: 1600, cy: 430, z: 1.55 },
        ]}>
          <Focus at={L(19.6)} out={L(21.6)} x={1296} y={196} w={170} h={80} />
          <Focus at={L(21.7)} out={L(24.1)} x={1494} y={196} w={200} h={110} />
          <Focus at={L(24.4)} x={1374} y={360} w={460} h={230} />
        </Shot>
      </AbsoluteFill>
      <Kicker at={8} out={L(26.2)} n="01" text="Explorer le territoire" />
    </AbsoluteFill>
  );
};

const Kicker: React.FC<{ at: number; out: number; n: string; text: string }> = ({ at, out, n, text }) => {
  const f = useCurrentFrame();
  const t = ramp(f, at, at + 18) * (1 - ramp(f, out - 10, out));
  return (
    <div style={{ position: 'absolute', left: 48, top: 44, opacity: t, transform: `translateX(${(1 - t) * -30}px)`, display: 'flex', alignItems: 'center', gap: 16, background: C.ink, color: '#fff', padding: '14px 24px', borderRadius: 12, fontFamily: SANS, fontSize: 30, fontWeight: 500, boxShadow: '0 12px 34px rgba(22,24,26,.25)' }}>
      <span style={{ fontFamily: MONO, fontSize: 24, opacity: 0.6 }}>{n}</span>{text}
    </div>
  );
};

// ---------- 4. Levier : avant / après ----------
const Lever: React.FC = () => {
  const f = useCurrentFrame();
  const L = (s: number) => loc('lever', s);
  const click = L(29.3);
  const sweep = ramp(f, click + 6, click + 30); // le volet révèle la carte recalculée
  const keys = [
    { f: 0, cx: 960, cy: 540, z: 1.05 }, { f: L(28.3), cx: 700, cy: 480, z: 1.15 },
    { f: L(31.4), cx: 900, cy: 520, z: 1 },
    { f: L(33.0), cx: 900, cy: 520, z: 1 }, { f: L(33.8), cx: 300, cy: 360, z: 2.3 },
    { f: L(37.2), cx: 300, cy: 380, z: 2.2 }, { f: L(38.0), cx: 260, cy: 600, z: 2.3 },
  ];
  const big = ramp(f, L(33.4), L(34.0)) * (1 - ramp(f, L(37.0), L(37.5)));
  return (
    <AbsoluteFill style={{ background: C.ground }}>
      <Shot src="b1-ecart-avant" keys={keys}>
        <Cursor from={[700, 760]} to={[254, 427]} at={L(28.4)} click={click} out={click + 26} />
      </Shot>
      <AbsoluteFill style={{ clipPath: `inset(0 ${(1 - sweep) * 100}% 0 0)` }}>
        <Shot src="b2-ecart-apres" keys={keys}>
          <Focus at={L(33.6)} out={L(37.1)} x={37} y={267} w={399} h={104} />
          <Focus at={L(37.9)} x={37} y={640} w={300} h={26} />
        </Shot>
      </AbsoluteFill>
      {sweep > 0 && sweep < 1 && <div style={{ position: 'absolute', top: 0, bottom: 0, left: `${sweep * 100}%`, width: 4, background: C.sel, boxShadow: '0 0 24px rgba(27,58,140,.6)' }} />}
      <div style={{ position: 'absolute', right: 90, top: 300, opacity: big, transform: `translateY(${(1 - big) * 30}px)`, background: C.panel, borderRadius: 18, padding: '34px 44px', boxShadow: '0 24px 70px rgba(22,24,26,.18)', border: `1px solid ${C.line}` }}>
        <div style={{ fontFamily: SANS, fontSize: 26, color: C.mute }}>Former 20 % de kinés en plus</div>
        <div style={{ fontFamily: MONO, fontSize: 104, color: C.kine, fontWeight: 500, display: 'flex', alignItems: 'baseline' }}>
          <span>+</span><DigitRoll value={'19 110'} delay={L(33.4)} fontSize={104} color={C.kine} />
        </div>
        <div style={{ fontFamily: SANS, fontSize: 28, color: C.ink }}>kinés libéraux en France en 2050</div>
        <div style={{ fontFamily: SANS, fontSize: 24, color: C.mute, marginTop: 6 }}>par rapport à la tendance · fourchette affichée</div>
      </div>
      <Kicker at={8} out={SHOTS.lever.to - SHOTS.lever.from} n="02" text="Simuler une politique" />
    </AbsoluteFill>
  );
};

// ---------- 5. Phrase -> scénario ----------
const PHRASE = 'former 20 % de kinés en plus en Auvergne';
const Phrase: React.FC = () => {
  const f = useCurrentFrame();
  const L = (s: number) => loc('phrase', s);
  const typeEnd = L(41.9);
  const n = Math.round(interpolate(f, [6, typeEnd], [0, PHRASE.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const clickT = L(42.15);
  const toModal = ramp(f, clickT + 4, clickT + 16);
  const caret = Math.floor(f / 8) % 2 === 0 && f < clickT;
  return (
    <AbsoluteFill style={{ background: C.ground }}>
      <Shot src="c0-vide" opacity={1 - toModal} keys={[{ f: 0, cx: 300, cy: 260, z: 2.5 }, { f: clickT, cx: 330, cy: 250, z: 2.3 }, { f: clickT + 16, cx: 700, cy: 500, z: 1.3 }]}>
        <div style={{ position: 'absolute', left: 39, top: 197, width: 306, height: 33, background: '#fff', borderRadius: 6, display: 'flex', alignItems: 'center', paddingLeft: 9, fontFamily: SANS, fontSize: 15, color: C.ink, whiteSpace: 'nowrap', overflow: 'hidden' }}>
          {PHRASE.slice(0, n)}{caret && <span style={{ width: 1.5, height: 18, background: C.ink, marginLeft: 1 }} />}
        </div>
        <Cursor from={[600, 420]} to={[392, 214]} at={typeEnd - 18} click={clickT} out={clickT + 14} />
      </Shot>
      <Shot src="c2-compris" opacity={toModal} keys={[{ f: clickT, cx: 700, cy: 500, z: 1.3 }, { f: L(43.2), cx: 960, cy: 530, z: 1.6 }, { f: L(44.4), cx: 1000, cy: 560, z: 1.75 }]}>
        <Focus at={L(43.0)} out={L(44.3)} x={700} y={500} w={520} h={66} />
        <Focus at={L(44.6)} x={984} y={588} w={228} h={33} />
      </Shot>
      <Kicker at={8} out={SHOTS.phrase.to - SHOTS.phrase.from} n="03" text="Décrire une politique en une phrase" />
    </AbsoluteFill>
  );
};

// ---------- 6. Clôture ----------
const Outro: React.FC = () => {
  const f = useCurrentFrame();
  const L = (s: number) => loc('outro', s);
  const gone = ramp(f, L(49.45), L(49.9));
  const lines = [
    { t: 'Données ouvertes', at: L(46.45) },
    { t: 'Hypothèses sourcées', at: L(47.35) },
    { t: 'Pas de boîte noire', at: L(48.6) },
  ];
  return (
    <AbsoluteFill style={{ background: C.ground, alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ position: 'absolute', left: 200, top: 330, opacity: 1 - gone, transform: `translateY(${-gone * 40}px)` }}>
        {lines.map((l) => (
          <div key={l.t} style={{ display: 'flex', alignItems: 'center', gap: 26, marginBottom: 26 }}>
            <BlurWord at={l.at} dy={0} dur={10}><span style={{ display: 'inline-block', width: 22, height: 22, background: C.sel, borderRadius: 4 }} /></BlurWord>
            <BlurLine at={l.at + 2} text={l.t} stagger={3} style={{ fontFamily: SANS, fontSize: 84, fontWeight: 500, color: C.ink, letterSpacing: '-0.02em' }} />
          </div>
        ))}
      </div>
      <div style={{ opacity: gone, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 34 }}>
        {gone > 0 && <Wordmark size={112} at={L(49.6)} />}
        <BlurLine at={L(51.5)} text="Anticiper l'offre de soins, territoire par territoire." stagger={3} style={{ fontFamily: SANS, fontSize: 44, color: C.mute }} />
        <div style={{ fontFamily: MONO, fontSize: 21, color: C.faint, marginTop: 40, opacity: ramp(f, L(52.6), L(53.4)) }}>
          DREES · Insee Omphale · CartoSanté · FINESS · Annuaire Santé — données ouvertes
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- Sous-titres (depuis la transcription) ----------
type W = { text: string; start: number; end: number; type: string };
const FIX: Record<string, string> = { '1071': '1 071', '1700': '1 700', 'Libérale': 'libérale' };
const LINES = (() => {
  const ws = (WORDS as { words: W[] }).words.filter((w) => w.type === 'word');
  const out: { text: string; from: number; to: number }[] = [];
  let cur: W[] = [];
  const fix = (t: string) => Object.entries(FIX).reduce((s, [a, b]) => s.replace(a, b), t);
  const flush = () => { if (!cur.length) return; out.push({ text: cur.map((w) => fix(w.text)).join(' ').replace(' ?', ' ?').replace(' %', ' %'), from: v(cur[0].start), to: v(cur[cur.length - 1].end) }); cur = []; };
  ws.forEach((w) => { cur.push(w); const n = cur.length; if (/[.?]$/.test(w.text) || (/,$/.test(w.text) && n >= 5) || n >= 11) flush(); });
  flush();
  // chaque ligne reste jusqu'à la suivante (max +0,6 s)
  return out.map((l, i) => ({ ...l, to: Math.min(out[i + 1]?.from ?? l.to + 18, l.to + 18) }));
})();
const Subtitles: React.FC = () => {
  const f = useCurrentFrame();
  const l = LINES.find((x) => f >= x.from && f < x.to);
  if (!l) return null;
  const t = ramp(f, l.from, l.from + 5);
  return (
    <div style={{ position: 'absolute', left: 0, right: 0, bottom: 54, display: 'flex', justifyContent: 'center', opacity: t }}>
      <div style={{ background: 'rgba(22,24,26,.82)', color: '#fff', fontFamily: SANS, fontSize: 34, fontWeight: 500, padding: '10px 22px', borderRadius: 10, maxWidth: 1300, textAlign: 'center' }}>{l.text}</div>
    </div>
  );
};

export const Pitch: React.FC<{ bgm: boolean; subtitles: boolean }> = ({ bgm, subtitles }) => {
  const f = useCurrentFrame();
  const scenes: [keyof typeof SHOTS, React.FC][] = [['hook', Hook], ['promise', Promise], ['map', Map], ['lever', Lever], ['phrase', Phrase], ['outro', Outro]];
  return (
    <AbsoluteFill style={{ background: C.ground }}>
      {scenes.map(([k, Comp], i) => {
        const s = SHOTS[k];
        const last = i === scenes.length - 1;
        return (
          <Sequence key={k} from={s.from} durationInFrames={s.to - s.from + (last ? 0 : XF)}>
            <Fade dur={s.to - s.from + (last ? 0 : XF)} inF={i === 0 ? 0 : XF} outF={last ? 20 : XF}><Comp /></Fade>
          </Sequence>
        );
      })}
      {subtitles && f >= SHOTS.promise.from && f < SHOTS.outro.from + 6 && <Subtitles />}
      <Sequence from={VO_START}><Audio src={staticFile('audio/voix-A.mp3')} /></Sequence>
      {bgm && <Audio src={staticFile('audio/bgm.mp3')} volume={(fr) => 0.085 * interpolate(fr, [0, 30, TOTAL - 60, TOTAL], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })} />}
      {/* repère image pour l'assurance qualité */}
      <div style={{ display: 'none' }}>{f}</div>
    </AbsoluteFill>
  );
};
