# H3: overhead flyby (first + last guides)

**Graph:** ComfyUI native H3 Ref2VA + `MiniMaxH3AddGuide` · **Guides:** first_and_last · 960×544, 24 fps, 20 steps, `res_multistep`/`beta`

## Prompt

```text
subject_definitions:
<Subject 1> is the scene in <Picture 1>, seen from high above. A hand-painted late-1990s cel-animated space opera frame: the burgundy-and-gold Pilgrim cruiser seen from above, with its long pointed forward hull, circular dorsal assembly, dark bow recess and two long aft arms on thin pylons; and two hostile Ogre heavy drones, compact dark gunmetal and olive armoured bodies each with exactly two parallel rotary cannons and small red lights.
summary:
[reference generation] Seen from above, the two Ogres streak along the Pilgrim's starboard edge from its stern toward its bow, raking the armour with their rotary cannons. Rounds stitch a line of sparks and hits down the flank. As they pass the bow they stop firing and race on toward the right; the hits they left glow and cool.
retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - Preserve the Pilgrim exactly: rigid top-down silhouette, long forward hull, circular dorsal assembly, bow recess, both aft arms and pylons, burgundy-and-gold paint. Preserve both Ogres: rigid compact bodies, exactly two parallel cannons each. Hand-drawn cel look with ink outlines and flat paint. No extra craft or hardware. Space stays near-black.
detailed_description:
[Shot 1] A high overhead view with only a very slight camera drift; the Pilgrim stays rigid and nearly still in frame. The two Ogres fly fast in tight formation along the Pilgrim's lower (starboard) edge, from the lower left toward the right, travelling most of the width of the frame. While they fly they fire rapid alternating bursts: short orange rounds travel forward from the cannon mouths into the Pilgrim's armour just ahead of them, where small hard-edged sparks erupt and leave a trail of glowing hits along the flank. When they pass the bow the firing stops completely; they keep flying right. The line of hits on the armour dims to small orange embers in darkened scorch marks. Crisp ink outlines, flat cel paint, hard shadows. Light stays local: no full-frame glow, no shield, no explosion.
overall_soundscape:
A rapid rotary cannon run and armour impacts passing by, then engine whine fading and quiet ticking of cooling metal. No speech.
non_diegetic_music:
N/A
```

## Outcome

Seed 2609301612, 90 frames. Both first+last takes held the ship rigid and completed fire, stop and cool. The guns stop at source frame 79, placed on a strong accent. **Approved.**
