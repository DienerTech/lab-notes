# GPT Images: working notes (keyframes and redraws)

*As of September 2026. We used the OpenAI Images edit endpoint with 1–4 input images, mostly `gpt-image-2.5-sunburst`, at 1536×1024. Evidence comes from [Can You See Me Now](../../projects/can-you-see-me-now/).*

For H3, GPT Images makes the **keyframes**: new angles, the start and end states of an action, and repaired stills. In a keyframe, identity matters more than beauty, because H3 will animate whatever it's given.

## Give every input image one job

Say in the prompt which image controls what.

| Role | Typical input |
|---|---|
| Composition and geometry | A code-rendered layout from real 3D geometry at the exact camera. It controls **shape and position only**. |
| Identity and paint | The production's approved art for that ship (its "house design"). |
| Subject design | An approved frame of a *different* subject, such as the film's established drone. |
| Style or background | A crop of an effect or background, with no ship in it. |
| Edit target | An approved frame you want to change in one respect. |

- **Split shape from paint.** When the layout render was also allowed to set the paint, the redraw copied the game's literal small-block camouflage and clashed with neighbouring shots. With shape from the layout and paint from the approved art, the join matched. **Tested:** the keyframes were the only thing that changed.
- **Treat layout drones as placeholders.** "The drone models in Image 1 are rough placeholders for position, size and heading only; draw them exactly like Images 3 and 4" made the film's twin-cannon drone appear in every candidate. When we told it to "keep Image 1's drone shape", we got the boxy real-game model, which I rejected. **Tested.**
- **Use ship-free style crops.** To reuse an old background's look without its wrong ship, crop a region with no ship in it. The model copies anything visible. **Tested.**

## Angle fidelity

- **Angles near the approved art trace closely.** A three-quarter view like the approved art matched the true silhouette well (IoU ~0.78).
- **Novel angles get reframed or reinterpreted.** An over-the-shoulder view was enlarged every time (scale 0.82–0.94), though the shape held after alignment.
- **Some views don't exist in the house design, and invented ones failed.** We had no approved stern view of the hero ship. I rejected every rear-view redraw, both the game-accurate one and the house-style one. The front three-quarter and a new head-on view succeeded. **Tested** (one ship).
- **Mirrored or new views of an established face work.** The head-on view was new to the film but kept the recognisable bow, and I picked it.

## Editing approved frames

- **For a one-respect change, edit the approved frame itself.** Examples: turn the ship squarely head-on, move the drones and stop the guns, or swap the background for a warp tunnel. The identity carries over.
  - **Measure the change you asked for.** Squaring the head-on ship took its landmark centreline spread from 94 px to 6.5 px.
- **Don't reuse an approved shot's exact framing as a *new* shot.** It stays on-model, but to me it looked "weird and lazy". Use frame edits for continuations; new shots need a new camera.
- **End keyframes that are edits of the start keyframe** give H3 matched first and last guides: same drawing, new state.

## Practical notes

- **Rate limit.** Our organisation hit an input-image rate limit of about 5 input images per minute, so a 4-image request right after a 3-image one failed. Space out multi-reference requests.
- **Input fidelity.** `input_fidelity=high` on an older model traced worse for us (IoU 0.35–0.50) than the newer default.
- **Candidates.** Request at least two per call. They differ in small but important ways, like the pod count or the paint scale.
- **Screen before anyone looks.** We score each candidate against the true silhouette mask, raw and after the best scale and shift alignment. It's only a screen: dark paint on near-black space lowers the score, and a pass on shape says nothing about style. See [tools/silhouette_qa.py](../../tools/silhouette_qa.py).
