# MiniMax H3: working notes

*As of September 2026. H3 image/reference-to-video, run locally through ComfyUI's native nodes. Evidence is mostly from [Can You See Me Now](../../projects/can-you-see-me-now/): hundreds of takes across 20 drafts and several research sweeps.*

H3 is great at hand-drawn motion, light and texture. It is also very literal about its inputs, drifts over long takes, and depends heavily on the seed. Most of what follows is about working with those traits.

## Our setup

| | |
|---|---|
| **Graph** | ComfyUI native `MiniMaxH3ReferenceToVideo` (Ref2VA) with `MiniMaxH3AddGuide` guide frames at frame 0, at interior frames, or at the last frame (`-1`). |
| **Weights** | Pruned INT8 (convrot) diffusion model, NVFP4 (AWQ) Qwen3-VL text encoder, FP16 video VAE, FP32 audio VAE. |
| **Sampling** | 960×544, 24 fps, 20 steps, `res_multistep` sampler, `beta` scheduler. |
| **Hosts** | An RTX 5090 on Windows: about 90 s per 90-frame take and about 180–215 s per 158-frame take once warm. Two GB10 Linux boxes: about 280–300 s per 90-frame take. |

- **Canvas size.** 1280×720 failed a latent patch reshape on our runtime, while 1280×736 and 1536×864 worked. **Tested** (one runtime): keep both dimensions divisible by 32.
- **Bigger canvases don't transfer takes.** A larger canvas changes the latent and noise shapes, so the same seed is a different take. Upscaling the edit is not the same as rendering natively at that size.

## Prompt format

We use a six-section structure, written in positive physical terms:

```text
subject_definitions:
<Subject 1> is the exact burgundy-and-gold Pilgrim cruiser in <Picture 1>, seen squarely head-on ...
summary:
[reference generation] The Pilgrim rushes toward the camera through a warp tunnel.
retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - preserve the rigid hull, the forward prongs ...
detailed_description:
Retro cel-animated space opera, bold ink outlines, hard-edged cel shading.
[Shot 1] Begin in the reference composition. The camera flies backward in front of the Pilgrim ...
overall_soundscape:
Low smooth mechanical rushing sound, no speech.
non_diegetic_music:
N/A
```

- **Name the parts to preserve.** List them in `retention_analysis`: "both long raised aft armour blocks with the gap and truss between them". **Lead:** once we rewrote a wrong part description, a take stopped reproducing the old error.
- **Timestamps in prose are approximate.** "Guns stop at 2.5 s" might land anywhere from 1.8 s to 3.5 s. Measure the actual event frame, then choose the in-point so the event lands on the beat you want.
- **Negative wording didn't stop floods or invented hardware.** Phrases like "no shield", "background stays the same" and "unchanged hardware" failed repeatedly. **Failed** as a fix. Change the reference or the seed instead.

## The reference image is the script

H3 animates what the still shows, mistakes included.

- **Fix anatomy in the still first.** A bent hull, a fourth gun pod, or barrels pointing below a shield all got animated faithfully. **Tested**, across many shots.
- **Don't let generated references become the only authority on identity.** A chain of image edits kept a misshapen hull while each edit "fixed" something else. See [asset-accuracy review](../../workflows/asset-accuracy-review.md).
- **Partial subjects invite invention.** In a flank-run shot where the camera slides along a partly visible hull, 2 of 4 seeds grew new structures as unseen parts came into view: a tower and a canopy. **Tested.**
- **Full silhouette plus a near-fixed camera holds identity.** An overhead strafing run with the whole ship in frame stayed rigid in 4 of 4 takes. **Tested.**

## Guide frames

| Configuration | What we saw | Status |
|---|---|---|
| First frame only | Locks composition and identity at the start. Motion tends to be restrained. Later drift is common: invented planets, background floods. | Tested |
| First + last | Completes bounded changes such as a weld closing, a shield collapsing, or drones crossing frame and ceasing fire. Make the last keyframe by *editing* the first, so the drawing matches. | Tested |
| Last only | Real camera travel onto a known frame ("rush in"), but the early frames invent content. Use the converged tail. | Lead |
| First + interior + last (same keyframe) | Long 158-frame warp takes: 4 of 4 anchored takes held clean, against 2 of 7 unanchored ones. The unanchored failures were floods and one invented cut. Seeds and keyframes vary between takes. The subject ends up nearly static. | Lead |
| First frame = an approved shot's last frame | Seamless continuation of approved footage, e.g. a secondary explosion. | Tested |
| 22-frame video guide at an interior frame | Doubled, scratchy detail inside the guide window. | Failed |

## Seeds and floods

- **The most common failure is a flood mid-take.** The background washes to haze, white-orange sun flares appear, or the frame turns yellow or grey. These depend on the seed: the same prompt and reference gave one dark take and one flooded take many times over. **Tested.**
- **Render seed pairs or triples and review the whole take.** Endpoint-only review misses mid-take floods. A take can end perfectly after flooding in the middle.
- **Checking the seed first is cheap.** One replicate seed fixed a haze problem that a pile of lighting prose didn't.

## Motion and camera

- **First-guide takes rarely deliver big travel.** We measured drone-centroid travel of 8–15% of frame width, against a 25% goal.
- **Last guides travel farther but invent more.**
- **Prompt for a run, not a pose.** A drone *strafing along* a hull, with the camera tracking or leading, gave our strongest action shots. Tableaux like "drone hovers and fires" read as static.
- **Deterministic camera moves and effects can go on top in code.** Push-ins and beat-locked streaks are examples; see [code motion layers](../../techniques/code-motion-layers.md).

## Things we tried that didn't clearly help, in our tests

These are **Failed** at the configurations we tested. That's not a verdict on the ideas in general.

- **Community motion adapters** (weapon and combat LoRAs, Wushu): no consistent gain in contact, grip or rigid-hull fidelity.
- **Hybrid checkpoints between reference and first/last modes:** fixed one seed's flash, but no general ranking emerged.
- **Choosing a "quiet" boundary frame for continuation:** worked on one seed, failed replication.
- **Depth or edge ControlNet from Blender proxies:** framing got more consistent, but the proxy silhouette leaked into the art.

## Reviewing H3 output

Review consecutive frames, not samples. Check each of these separately:

- identity;
- the count of guns, drones and parts;
- direction of fire and travel (from consecutive frames);
- background and lighting;
- the camera.

Measure what you can: silhouette agreement, centroid travel, event frames, flow direction. Then look anyway.
