import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, random} from 'remotion';
import {Plate, Scanlines, Vignette, MONO, SAIRA} from './common';
// Minmatar Republic fire-control: rust, bone, hazard red. Rough, riveted, loud.
const RUST = '#e0782c', BONE = '#eadbc0', RED = '#ff3a26', DARK = 'rgba(18,8,4,0.86)';
const tc = (f: number) => ({
  x: interpolate(f, [0, 48, 96], [780, 960, 990], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
  y: interpolate(f, [0, 48, 96], [470, 500, 510], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
});
const TURRETS = [
  {id: 'T1', gun: '425mm AC', lag: 7, a: 330, w: 0.23, p: 0.4},
  {id: 'T2', gun: '425mm AC', lag: 11, a: 420, w: 0.19, p: 2.2},
  {id: 'T3', gun: '425mm AC', lag: 5, a: 280, w: 0.29, p: 4.1},
  {id: 'T4', gun: '425mm AC', lag: 14, a: 470, w: 0.16, p: 5.3},
];
const ERRORS = [
  {f: 3, x: 1180, y: 150, t: 'TRACKING FAILURE', s: 'T2  // ANGULAR VEL > TURRET TRACKING'},
  {f: 8, x: 110, y: 610, t: 'SOLUTION LOST', s: 'T4  // REACQUIRE . . . REACQUIRE . . .'},
  {f: 12, x: 1260, y: 560, t: 'ERROR', s: 'FIRE CONTROL DESYNC  0x3F'},
  {f: 16, x: 520, y: 130, t: 'AIM CORRECTION SATURATED', s: 'SERVO LIMIT  // T1 T3'},
  {f: 20, x: 1040, y: 760, t: 'ERROR', s: 'TRACKING DISRUPTOR DETECTED'},
  {f: 24, x: 160, y: 250, t: 'NO FIRING SOLUTION', s: 'ALL TURRETS'},
  {f: 28, x: 700, y: 640, t: 'ERROR', s: 'ERROR ERROR ERROR'},
  {f: 32, x: 1320, y: 320, t: 'TRACKING 7%', s: 'OPTIMAL RANGE UNREACHABLE'},
];
const Hazard: React.FC<{w: number; h: number}> = ({w, h}) => (
  <div style={{width: w, height: h, backgroundImage: `repeating-linear-gradient(45deg, ${RED} 0 10px, #1a0703 10px 20px)`}} />
);
const Popup: React.FC<{e: typeof ERRORS[0]; f: number; i: number}> = ({e, f, i}) => {
  const t = f - e.f;
  if (t < 0) return null;
  const scale = interpolate(t, [0, 2, 4], [1.9, 0.92, 1], {extrapolateRight: 'clamp'});
  const shake = t < 5 ? (random('p' + i + f) - 0.5) * 22 : 0;
  const flicker = t < 3 ? (t % 2 ? 0.35 : 1) : random('fl' + i + f) > 0.93 ? 0.5 : 1;
  const big = e.t === 'ERROR';
  return (
    <div style={{position: 'absolute', left: e.x + shake, top: e.y, transform: `scale(${scale}) rotate(${(random('r' + i) - 0.5) * 5}deg)`, transformOrigin: 'left top', opacity: flicker,
      display: 'flex', border: `3px solid ${RED}`, background: DARK, boxShadow: `0 0 18px ${RED}`, fontFamily: MONO}}>
      <Hazard w={22} h={big ? 104 : 86} />
      <div style={{padding: '8px 16px'}}>
        <div style={{display: 'flex', gap: 12, alignItems: 'center'}}>
          <span style={{background: RED, color: '#140400', fontWeight: 900, fontSize: 20, padding: '1px 8px', letterSpacing: 2}}>!! ERROR</span>
          <span style={{color: BONE, fontSize: 14, opacity: 0.75}}>{`E-${(4096 + i * 377).toString(16).toUpperCase()}`}</span>
        </div>
        <div style={{fontFamily: SAIRA, color: big ? RED : BONE, fontSize: big ? 52 : 36, fontWeight: 800, letterSpacing: 3, lineHeight: 1.15, textShadow: `0 0 10px ${RED}`}}>{e.t}</div>
        <div style={{color: RUST, fontSize: 15, letterSpacing: 2}}>{e.s}</div>
      </div>
    </div>
  );
};
const Pip: React.FC<{tr: typeof TURRETS[0]; f: number}> = ({tr, f}) => {
  const c = tc(f - tr.lag);
  const drift = interpolate(f, [0, 40], [0.7, 1.2], {extrapolateRight: 'clamp'});
  const x = c.x + tr.a * drift * Math.sin(tr.w * f + tr.p) + 90 * Math.sin(tr.w * 3.1 * f);
  const y = c.y + tr.a * 0.55 * drift * Math.cos(tr.w * 1.3 * f + tr.p * 1.7);
  const t = tc(f);
  const err = Math.hypot(x - t.x, y - t.y);
  const blink = Math.floor(f / 3) % 2 === 0;
  return (
    <>
      <svg style={{position: 'absolute', left: 0, top: 0}} width={1920} height={1080}>
        <line x1={x} y1={y} x2={t.x} y2={t.y} stroke={RUST} strokeWidth={2} strokeDasharray="8 10" opacity={0.7} />
        <g transform={`translate(${x},${y}) rotate(${f * 9 * (tr.w > 0.2 ? 1 : -1)})`} stroke={blink ? RED : RUST} strokeWidth={4} fill="none">
          <path d="M-48,-20 L-48,-48 L-20,-48 M20,-48 L48,-48 L48,-20 M48,20 L48,48 L20,48 M-20,48 L-48,48 L-48,20" />
          <line x1={-12} y1={0} x2={12} y2={0} /><line x1={0} y1={-12} x2={0} y2={12} />
        </g>
      </svg>
      <div style={{position: 'absolute', left: x + 56, top: y - 44, fontFamily: MONO, color: BONE, fontSize: 17, lineHeight: 1.2, textShadow: '0 0 6px #000'}}>
        <div style={{color: blink ? RED : RUST, fontWeight: 900}}>{tr.id} {tr.gun}</div>
        <div>ΔΘ {(err / 900).toFixed(2)} rad</div>
        <div style={{color: RED}}>{blink ? 'NO TRACK' : ''}</div>
      </div>
    </>
  );
};
export const LokiHud: React.FC = () => {
  const f = useCurrentFrame();
  const hits = ERRORS.filter((e) => f - e.f >= 0 && f - e.f < 3).length;
  const sx = hits ? (random('sx' + f) - 0.5) * 18 : 0, sy = hits ? (random('sy' + f) - 0.5) * 12 : 0;
  const t = tc(f);
  const trk = Math.max(3, Math.round(interpolate(f, [0, 34], [41, 7], {extrapolateRight: 'clamp'}) + (random('tk' + f) - 0.5) * 6));
  const banner = f >= 40;
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `translate(${sx}px,${sy}px)`}}>
        <Plate src="plate-loki.mp4" filter="grayscale(1) sepia(1) hue-rotate(-18deg) saturate(2.0) brightness(0.9) contrast(1.3)" />
        <Scanlines color="rgba(255,140,60,0.18)" opacity={1} gap={5} />
        <Vignette />
        {/* true target lock: steady, the only thing that is right */}
        <svg style={{position: 'absolute', left: 0, top: 0}} width={1920} height={1080}>
          <g transform={`translate(${t.x},${t.y}) rotate(45)`}><rect x={-26} y={-26} width={52} height={52} stroke={BONE} strokeWidth={2} fill="none" /></g>
        </svg>
        <div style={{position: 'absolute', left: t.x + 44, top: t.y + 30, fontFamily: MONO, color: BONE, fontSize: 16, letterSpacing: 2}}>LOCK HELD // PILGRIM</div>
        {TURRETS.map((tr) => <Pip key={tr.id} tr={tr} f={f} />)}
        {/* frame + header */}
        <div style={{position: 'absolute', inset: 34, border: `2px solid ${RUST}`, opacity: 0.8}} />
        <div style={{position: 'absolute', left: 34, top: 34, right: 34, height: 70, background: DARK, borderBottom: `3px solid ${RUST}`, display: 'flex', alignItems: 'center', gap: 28, padding: '0 26px', fontFamily: MONO}}>
          <Hazard w={60} h={40} />
          <span style={{fontFamily: SAIRA, color: BONE, fontSize: 38, fontWeight: 800, letterSpacing: 5}}>LOKI // FIRE CONTROL</span>
          <span style={{color: RUST, fontSize: 18, letterSpacing: 3}}>REPUBLIC FLEET  ·  4× 425mm AUTOCANNON</span>
          <span style={{marginLeft: 'auto', color: RED, fontSize: 22, fontWeight: 900, opacity: Math.floor(f / 4) % 2 ? 1 : 0.4}}>● TRACKING {trk}%</span>
        </div>
        {/* tracking bar */}
        <div style={{position: 'absolute', left: 60, bottom: 70, width: 520, fontFamily: MONO, color: BONE, fontSize: 16, letterSpacing: 2}}>
          <div>REQUIRED TRACKING  0.44 rad/s</div>
          <div style={{height: 14, background: '#2a1208', margin: '6px 0 12px'}}><div style={{width: '100%', height: '100%', background: RUST}} /></div>
          <div>AVAILABLE  {(0.44 * trk / 100).toFixed(3)} rad/s  <span style={{color: RED}}>▼ DISRUPTED</span></div>
          <div style={{height: 14, background: '#2a1208', marginTop: 6}}><div style={{width: `${trk}%`, height: '100%', background: RED}} /></div>
        </div>
        {ERRORS.map((e, i) => <Popup key={i} e={e} f={f} i={i} />)}
        {banner && (
          <div style={{position: 'absolute', left: 0, right: 0, top: 440, height: 200, background: 'rgba(40,4,0,0.9)', borderTop: `4px solid ${RED}`, borderBottom: `4px solid ${RED}`,
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 40, transform: `scaleY(${interpolate(f, [40, 43], [0.05, 1], {extrapolateRight: 'clamp'})})`,
            opacity: random('bn' + f) > 0.9 ? 0.55 : 1}}>
            <Hazard w={150} h={200} />
            <div style={{fontFamily: MONO, textAlign: 'center'}}>
              <div style={{fontFamily: SAIRA, color: RED, fontSize: 120, fontWeight: 800, letterSpacing: 10, textShadow: `0 0 26px ${RED}`}}>TRACKING DISRUPTED</div>
              <div style={{color: BONE, fontSize: 24, letterSpacing: 8}}>TARGET MOVING FASTER THAN TURRETS CAN FOLLOW</div>
            </div>
            <Hazard w={150} h={200} />
          </div>
        )}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
