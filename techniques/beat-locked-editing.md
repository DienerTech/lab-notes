# Beat-locked editing: measure the music, then place events

Generic technique notes. They aren't about any particular song.

## Check the meter before building an edit grid

- **An early grid was wrong from the start.** It was phase-correct but spanned 1.5 beats, so every "on-grid" cut still crossed bar lines, and the edit felt loose.
- **Full-band onsets can lock onto the hi-hats.** One fit put the beats on the "and"s.
- **Split the bands.** Kick-band and snare-band onsets moved the phase by half a beat. Kick on 1 and 3, snare on 2 and 4, plus changes in the harmony, picked the downbeat.
- **Confirm the tempo twice.** Two independent periodicity tests agreeing is better than one BPM fit.

## Cut placement is not the same as event placement

- **Most cuts can land on a grid while the action still misses.** Measure the events *inside* each shot:
  - the first muzzle flash;
  - the impact;
  - the moment the guns stop;
  - shield collapse.
- **Pin a measured event to a strong accent by choosing the in-point**, not by retiming. For example, if a take's guns stop at source frame 79, start the range so that frame lands on the accent.
- **Automatic event proxies are noisy.** Brightness or motion peaks near accents are a rough screen. Hand-checked anchors are the real evidence: the impact frame, or the frame the volley flashes.

## Keep deterministic events in code

- **Overlays and code effects can be exactly on the beat.** HUD pulses, warp-streak surges and title timing are functions of the beat index, not prompted. See [code motion layers](code-motion-layers.md) and [Remotion overlays](remotion-overlays.md).
- **Generated motion is approximate.** "Guns stop at 2.5 s" in a prompt might land anywhere nearby, so measure it and choose the range.

## Pacing still needs ears

A listen of the assembled cut with the music is the real test. Measurements tell you where to look.
