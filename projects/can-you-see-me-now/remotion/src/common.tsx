import React from 'react';
import '@fontsource/share-tech-mono/400.css';
import '@fontsource/saira-condensed/700.css';
import '@fontsource/saira-condensed/800.css';
import '@fontsource/exo-2/200.css';
import '@fontsource/exo-2/300.css';
import '@fontsource/exo-2/500.css';
import '@fontsource/rajdhani/500.css';
import '@fontsource/rajdhani/600.css';
import '@fontsource/rajdhani/700.css';
import {AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame, random} from 'remotion';
export const MONO = '"Share Tech Mono", monospace';
export const SANS = '"Exo 2", sans-serif';
export const SAIRA = '"Saira Condensed", sans-serif';
export const RAJ = '"Rajdhani", sans-serif';
export const Plate: React.FC<{src: string; filter: string}> = ({src, filter}) => (
  <AbsoluteFill>
    <OffthreadVideo src={staticFile(src)} muted style={{width: '100%', height: '100%', filter}} />
  </AbsoluteFill>
);
export const Scanlines: React.FC<{color: string; opacity: number; gap?: number}> = ({color, opacity, gap = 4}) => (
  <AbsoluteFill style={{backgroundImage: `repeating-linear-gradient(0deg, ${color} 0px, ${color} 1px, transparent 1px, transparent ${gap}px)`, opacity, mixBlendMode: 'screen'}} />
);
export const Vignette: React.FC = () => (
  <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.75) 100%)'}} />
);
/** deterministic per-frame jitter */
export const useJitter = (seed: string, amp: number) => {
  const f = useCurrentFrame();
  return [(random(seed + 'x' + f) - 0.5) * amp, (random(seed + 'y' + f) - 0.5) * amp] as const;
};
