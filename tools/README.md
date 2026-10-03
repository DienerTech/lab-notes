# Tools

These are small reference scripts, cleaned up from production. They're meant to be read and adapted; they aren't a framework. Python 3.11+ with `numpy`, `pillow`, `scipy` and `av` (PyAV).

| Script | What it does | Where it came from |
|---|---|---|
| [`silhouette_qa.py`](silhouette_qa.py) | Scores redraws against a true silhouette mask, raw and after alignment, and writes overlays | [Code previs to AI redraw](../techniques/code-previs-to-ai-redraw.md) |
| [`warp_streaks.py`](warp_streaks.py) | Adds a beat-locked warp-streak layer and an eased push-in behind a subject | [Code motion layers](../techniques/code-motion-layers.md) |
| [`streak_flow.py`](streak_flow.py) | Measures whether streaks flow into or out of the vanishing point | [Code motion layers](../techniques/code-motion-layers.md) |
| [`scrub_check.py`](scrub_check.py) | A pre-publish scan for keys, paths, IPs, e-mails, private patterns and image metadata | [Experiment logs](../workflows/experiment-logs-and-agent-memory.md) |

The Remotion HUD example lives with its project: [projects/can-you-see-me-now/remotion](../projects/can-you-see-me-now/remotion/).

**Tuning.** These scripts are tuned for our footage: a burgundy and gold ship on blue space, at 960×544. Expect to adjust the segmentation thresholds for your own subjects.
