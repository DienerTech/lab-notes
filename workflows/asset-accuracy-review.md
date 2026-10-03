# Asset-accuracy review: why AI reviewers miss malformed subjects, and what we do about it

The most humbling lesson of *Can You See Me Now*: across many drafts, **Claude, Codex and their peer reviews approved shots with a malformed hero ship**. I spotted them immediately. I flew the Pilgrim in EVE for years, and I know its silhouette at a glance.

## Why the errors got through

1. **Recognition by livery.** Vision models identify "the Pilgrim" from its colours and context, not by checking its parts. Any plausible ship in burgundy and gold passes.
2. **Wrong scale.** Claude and Codex reviewed downscaled contact sheets, where a background ship is about 100 px wide. Shape errors, and a texture that turns into mosaic noise, only show at 1:1 on the delivery master.
3. **The author's criterion.** Claude checked that the redraw "traced the real hull", and it passed. My test was whether it "looks like the same ship, in the same film, at full size", and no agent asked that. An agent reviewing its own work, knowing what it meant to make, drifts into confirming it.
4. **Shared blind spots.** Claude and Codex failed the same way. Their peer review caught process bugs, but not this class of visual error.

## The protocol (we now run it on every project)

1. **Asset inventory per shot.** List every recurring subject that's visible, including partial and background ones. Give each a **landmark checklist**:
   - hero ship: forward prongs framing a blue bow recess, the hatch plate, the round dorsal dome, two raised aft blocks on struts, large panel paint (not a mosaic);
   - drone: compact body, two big rotary cannons side by side, red lights, no legs.
2. **The right authority.** The identity authority is the **production's own approved house design, plus the shots that cut into and out of this one**. Game or official geometry is a structural aid only. We learned this the hard way: I rejected a game-accurate redraw as "a distinctly skinnier ship".
3. **Side by side at a matched angle.** Put the crop next to the authority at the nearest angle, at equal size. Code-render the real geometry at a matched camera when the angle is new.
4. **1:1 crops at delivery resolution.** Check shape *and* texture and paint style against the neighbouring shots.
5. **Blind description first.** Describe the crop's parts without being told what it's meant to be, then compare against the checklist. A plausible whole with a missing landmark is a fail.
6. **Attitude and continuity.** Check heading, lean and screen direction against the neighbours, along with any effect that implies motion. In one draft the Pilgrim was, as I put it, "warping sideways", because the tunnel's vanishing point was perpendicular to its heading.
7. **Metrics are screens, not verdicts.** Silhouette IoU, symmetry spreads and flow direction trigger a look; they don't replace one. A shape pass says nothing about style.
8. **Honest labels.** Say which checks you did. Mark anything unchecked "unverified". Never write "fixed" when only your own metric passed.
9. **A cheap human check.** When a recurring asset changes, Claude or Codex shows me a crop sheet before animating or rendering masters. **One crop check with me settled in one round what four rounds of agent review hadn't.**
10. **Removal is a valid fix.** If a background asset can't be made accurate, take it out.

![Keyframe options Claude showed me before animating; I picked the head-on view](../projects/can-you-see-me-now/media/warp-keyframe-options.webp)

## Put it where every agent reads it

The protocol lives in the project's agent instructions (`AGENTS.md`) and in our shared working guide, so Claude and Codex both follow it at the start of every session without me reminding them.
