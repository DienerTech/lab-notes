# Compositing repairs: fix one thing, keep the rest bit-exact

**Problem.** I loved a chase shot's drone motion, but the distant Pilgrim in the background was malformed. Regenerating the shot would have lost the motion.

**Approach.** Repair only the broken region in post. Every other pixel stays identical to the source.

## What we tried

| Attempt | Result |
|---|---|
| Replace the ship with a redrawn sprite: track it, remove the old ship, composite the correct design on the same track | **Failed.** To me it looked worse than the original. Claude's sprite was geometrically correct, but its fine panel pattern turned into mosaic noise at that size, and its flat paint read as a pasted cutout. It passed Claude's geometry check and failed my test as a viewer. |
| Redraw the ship inside the actual frame with an image edit, to match the scene's painting style | **Failed** the landmark check at that side-on angle, so Claude rejected it before showing me. |
| **Remove the ship** and fill with a starfield plate that moves on the ship's own track | **Approved** by me. Clean, with nothing left to look wrong. The foreground I loved is untouched. |

![Before, the failed sprite, and the approved removal](../projects/can-you-see-me-now/media/background-repair.webp)

## Technique notes

- **Track the object's own unclipped edges, not the frame.** Phase correlation over the region was dominated by a large moving foreground ship. The right and top edges of the old ship's mask, fitted smoothly over time, tracked well.
- **Build the removal mask generously.** Warm-hull segmentation missed the dim ink outline and the cyan bow lights. Add a sweep for dim, non-background pixels in a box around the object.
- **Take plate donors from a region that's known to be empty.** Our first plate reused pixels 70 px above each hole, which overlapped the old ship. The fill then pasted hull fragments back in as orange specks. Build the plate from a strip of sky above the object, tiled, and move it on the object's track.
- **Protect the foreground.** Only pixels inside the removal mask, or under a replacement, may change.
- **Verify exactly.** Keep the repaired clip lossless (FFV1, RGB), then check that:
  - no pixel changed outside the repair region;
  - frames outside the repaired window are identical to the decoded source;
  - frame-to-frame change in the repaired region is no higher than the original's, so no flicker was added.

## Lesson

**Removing an asset you can't make accurate is a valid fix.** A correct-but-foreign replacement can be worse than a slightly wrong original. Judge the result at delivery resolution, in the cut.
