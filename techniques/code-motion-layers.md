# Code motion layers: exact camera moves and effects on top of AI footage

Anchored H3 takes can be identity-stable but nearly static. We added motion afterwards, in code, where it's exact and repeatable.

![The warp, v19 to v20](../projects/can-you-see-me-now/media/warp-evolution.webp)

## Push-in

An eased zoom (for example 1.00 to 1.10 over the shot) about the subject's centre, applied after compositing. It's cheap and deterministic, and it adds life to a held composition.

## Warp streaks (beat-locked)

- **Geometry.** Fit the vanishing point to the *painted* streaks, so the code layer shares the tunnel.
  - Use structure-tensor orientation on the background, then a least-squares line intersection.
  - Take the median over several frames. Single-frame fits drifted as the ship mask changed.
- **Particles.** Particles move along rays from the vanishing point with perspective speed, `dr/dt = ±k·r`, and respawn at the far end. Draw each at 2× with a thin bright core and a soft blue glow, then downsample.
- **Beat lock.** Speed and brightness surge at the beats and strong accents from the audio map, with a short exponential decay.
- **Matte.** Composite only where the subject matte is zero. Warm-colour segmentation missed dark mechanical strips and separate hull parts. The convex hull of all the warm regions kept the hull clean, at the cost of hiding a few streaks in small background notches.

## Get the direction right (we didn't, at first)

**The streaks must move toward the point the subject is moving away from.** For a ship flying *toward* the camera, the visible vanishing point behind the ship is the **focus of contraction**: the stars rush *into* it.

Claude's first version flowed *out* of that point. When I watched it, the streaks looked like they were "flowing backwards". Here's which way they should go:

| Subject | Visible vanishing point | Streak flow |
|---|---|---|
| Flying away from the camera (we see its engines) | Ahead of the bow | Outward from the vanishing point, past the ship |
| Flying toward the camera (we see its bow) | Behind the ship | **Inward**, into the vanishing point |

**Measure it; don't eyeball it.**
- **Isolate the layer.** Subtract a render made without streaks.
- **Measure along rays.** Sample intensity along rays from the vanishing point in consecutive frames and cross-correlate. The sign of the shift gives the direction. Ours measured +8.5 px per frame for the wrong version and −12 to −18 px per frame after the fix.
- **Phase correlation reports zero here.** Thin streaks moving along their own length are an aperture problem.

The script is [tools/warp_streaks.py](../tools/warp_streaks.py) and the flow check is [tools/streak_flow.py](../tools/streak_flow.py).

## Deliver losslessly

Render each layer to a lossless clip (FFV1) so the assembler treats it like any other source. Keep a JSON sidecar with the vanishing point, the beat events and the parameters.
