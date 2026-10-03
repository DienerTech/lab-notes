# Remotion example: Loki fire-control HUD

This is the overlay from the ambush scene. A Minmatar Loki's fire control fails as a tracking disruptor lands: turret pips drift off target, error pop-ups cascade, and a "TRACKING DISRUPTED" banner slams in. I approved this overlay in review.

![Loki HUD in the final cut](../media/loki-hud.webp)

- `src/LokiHud.tsx` is the composition. Every element is a pure function of `useCurrentFrame()`, so re-renders are exact.
- `src/common.tsx` holds shared pieces: the footage plate, scanlines, vignette and fonts.
- `src/Scale1440.tsx` renders a composition authored at 1920×1080 at 2560×1440 with an exact CSS scale. That keeps vector lines crisp without fractional `--scale`.

## Running it

```bash
npm install
npm run studio
```

`LokiHud` expects a footage plate at `public/plate-loki.mp4`. The film's plate isn't included, so use any clip of your own. The HUD grades it with a CSS filter and composites on top.

## Notes

- **Colour range.** Remotion's default output was full-range `yuvj420p`. If you convert it into a limited-range master, go through RGB or tag the range, otherwise the blacks get crushed. See [Remotion overlays](../../../techniques/remotion-overlays.md).
- **Licensing.** The code is MIT. The on-screen terms (Loki, Minmatar, 425mm) refer to EVE Online, which belongs to Fenris Creations; see [NOTICE.md](../../../NOTICE.md).
