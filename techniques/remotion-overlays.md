# Remotion overlays: HUDs, titles and exact text

Image and video models are bad at text, and at effects that must be exact: target reticles, "ERROR" cascades, capacitor readouts, credits. We draw those in [Remotion](https://www.remotion.dev/) and composite them over AI footage.

## What we built

- **Sensor and fire-control HUDs.** A drifting reticle, off-target turret pips, and an error cascade over a decloaking ship. I approved the fire-control HUD. **Approved.**
- **A shield HUD**, as a fallback for when a generated shield collapse wouldn't read. It gets drawn hits, ticked on the beats.
- **Title and end cards.** The title decloaks along with the ship. The end card carries the creator credit.

The split that worked: **H3 provides the physical machinery and action; the overlays provide exact text, colour and timing.**

## Tips

- **Drive everything from frame numbers.** Write overlay events as functions of `useCurrentFrame()` and a shared beat map. Then a re-cut moves them with the music automatically.

  ```tsx
  const frame = useCurrentFrame();
  const beat = beats.findLast((b) => b.frame <= frame);
  const sinceBeat = beat ? frame - beat.frame : 99;
  const pulse = Math.exp(-sinceBeat / 4);          // brightness surge on each beat
  ```

- **Render at delivery resolution.** Render 1080p and 1440p variants rather than upscaling the overlay; thin HUD lines don't survive upscaling.
- **Watch the colour range.** Remotion wrote full-range `yuvj420p`. A format-only conversion copied the full-range luma into limited-range `yuv420p` unchanged, so players crushed the blacks: the title's mean luma fell from 14.6 to 8.4. Convert through RGB, or tag the range explicitly. Then **verify levels in the final master**, not in the derived card. Our visual check compared the wrong file and missed this.
- **Keep the derived plates.** When an overlay is burned onto a plate, keep that plate. We once had to re-derive a title plate by frame matching because it hadn't been saved.
