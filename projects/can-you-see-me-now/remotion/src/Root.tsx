import React from 'react';
import {Composition} from 'remotion';
import {LokiHud} from './LokiHud';
import {scale1440} from './Scale1440';

// Trimmed from the production Root: only the example HUD, at both delivery sizes.
// Supply your own footage plate at public/plate-loki.mp4 (not included in this repository).
const LokiHud1440 = scale1440(LokiHud);

export const Root: React.FC = () => (
  <>
    <Composition id="LokiHud" component={LokiHud} durationInFrames={96} fps={24} width={1920} height={1080} />
    <Composition id="LokiHud-1440" component={LokiHud1440} durationInFrames={96} fps={24} width={2560} height={1440} />
  </>
);
