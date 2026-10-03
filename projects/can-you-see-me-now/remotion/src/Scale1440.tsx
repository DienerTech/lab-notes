import React from 'react';
import {AbsoluteFill} from 'remotion';
// Render a 1920x1080-authored composition at 2560x1440 as vector (exact 4/3 CSS scale), avoiding fractional --scale.
export const scale1440 = <P extends object>(C: React.FC<P>): React.FC<P> => (props: P) => (
  <AbsoluteFill style={{background: '#000'}}>
    <div style={{width: 1920, height: 1080, transform: 'scale(1.3333333333)', transformOrigin: '0 0', position: 'absolute', left: 0, top: 0}}>
      <C {...props} />
    </div>
  </AbsoluteFill>
);
