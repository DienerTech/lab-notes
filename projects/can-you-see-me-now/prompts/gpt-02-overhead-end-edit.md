# GPT Images: end keyframe as an edit of the start keyframe

**Model:** `gpt-image-2.5-sunburst` · **Size:** 1536x1024 · **Candidates:** 2

| Input | Role |
|---|---|
| Image 1 | edit target: selected k41F-v002 (first frame of this shot) |
| Image 2 | layout of the last moment (code render, t=3.1): Ogre positions/sizes ONLY |

## Prompt

```text
Image 1 is a finished cel-animation frame seen from high above. Keep EVERYTHING in Image 1 identical: the Pilgrim cruiser's exact shape, position, size and paint, the painted starfield, the camera and framing, and the design, paint and size of the two Ogre drones. Change only the moment in time, about two and a half seconds later.

New moment: the two Ogres have raced along the Pilgrim's lower (starboard) edge and are now at the RIGHT side of the frame, just past the Pilgrim's pointed bow, still flying toward the right, in the positions and sizes that Image 2 (a rough 3D layout) shows for them. Only use Image 2 for where the two drones are; draw them exactly like Image 1's drones, each with its two parallel rotary cannons. The left part of the frame, where they were, is now empty space.

Their guns have STOPPED: no muzzle flashes, no rounds in flight, no sparks. Along the Pilgrim's starboard armour, where the rounds struck, leave a line of five or six small dim orange glowing impact scars inside darkened scorch marks, drawn in the same hand-painted cel style with hard edges and no bloom.

No other change. No text, no UI.
```

## Outcome

Used as the last guide of the approved 1:45 overhead flyby. The drawing matches the first guide because it *is* the first guide, edited.

![result](../media/overhead-flyby.webp)
