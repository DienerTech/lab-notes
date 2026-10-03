# H3: head-on warp (first + interior + last anchors)

**Graph:** ComfyUI native H3 Ref2VA + `MiniMaxH3AddGuide` · **Guides:** first + interior(80) + last (same keyframe) · 960×544, 24 fps, 20 steps, `res_multistep`/`beta`

## Prompt

```text
subject_definitions:
<Subject 1> is the exact burgundy-and-gold Pilgrim cruiser in <Picture 1>, seen squarely head-on and left-right symmetric: two long forward prongs framing a glowing blue bow recess, a gold hatch plate, a round tiered dorsal dome, and two raised aft armour blocks on struts joined by a truss.
summary:
[reference generation] The Pilgrim rushes toward the camera through a warp tunnel.
retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - preserve the rigid hull, the forward prongs and blue bow recess, the hatch plate, the dorsal dome, both raised aft armour blocks with their struts and truss, and the burgundy-and-gold panel paint.
detailed_description:
Retro cel-animated space opera, intricate hand-drawn spacecraft, bold ink outlines, hard-edged cel shading.
[Shot 1] Begin in the reference composition. The camera flies backward in front of the Pilgrim, matching its speed, so the ship stays large and centred with only a gentle drift. Fine blue star streaks radiate from the vanishing point directly behind the ship and stream outward past it toward the camera and the frame edges. The ship holds its heading straight at the camera, centred and symmetric, without pitching, rolling, yawing or turning; the hull stays rigid and sharply inked. The bow recess glows a steady blue. Constant dark indigo background and steady illumination. One uninterrupted shot with no other spacecraft or weapons. No text, panels or UI.
overall_soundscape:
Low smooth mechanical rushing sound, no speech.
non_diegetic_music:
N/A
```

## Outcome

Seed 2609302101, 158 frames. The same keyframe sits at frame 0, frame 80 and the last frame. The ship stays centred and symmetric (median offset 2.2 px). The push-in and streaks were added in code. **Approved.**
