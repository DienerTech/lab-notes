# Experiment logs and agent memory

Agents forget between sessions, and models get updated. Across 20 drafts, what kept the work compounding was a **written, searchable record**.

## What we keep for every generation

- The **exact prompt** (the full text, not a summary), the **reference images** with hashes, the **seed**, and the **exact submitted graph**.
- The model and runtime profile, the host, the timings, and the GPU telemetry.
- The output hash, the **selected range**, and the **review**.
- **Rejected attempts, preserved.** The failures explain the fixes.

A per-project `experiment.json` holds this. A cross-project `experiments.jsonl` index lets any session search for "what happened last time we tried first + last guides on a drone shot?"

## Agent review is not my approval

Record them separately and never merge them. In our records, `assistant_review` is Claude or Codex, and `user_review` is me:

```json
{
  "assistant_review": {"verdict": "accepted_range", "range": [20, 85],
                        "notes": "overhead Pilgrim rigid; Ogres travel ~60% of frame; guns stop at src 79"},
  "user_review": {"verdict": "approved",
                  "quote": "Love the ogre shots tho, those flyby attacks are really nice"}
}
```

When I override an earlier acceptance by Claude or Codex, the record says so. The old verdict stays, as history.

## A working guide that learns

- **Findings with scope and status.** Each finding records its scope and status (see [CONVENTIONS.md](../CONVENTIONS.md)) and is linked to its evidence. We write "2 of 2 anchored takes clean (seed-confounded)", not "anchors fix floods".
- **Corrections in place.** When I correct a principle, for example that the identity authority is the house design and not the game model, the agent fixes the guide and dates the change.

## Agent instructions and memory

- **`AGENTS.md` at the workspace root** is read by both Claude and Codex at session start. It holds the non-negotiables:
  - read the working guide before planning;
  - keep every generation traceable;
  - record my reviews separately from theirs;
  - run the asset-accuracy protocol.
- **Personal agent memory** holds durable preferences. For example: "dynamic drone action is the strongest material" and "creator credit is DienerTech". It is not a place for facts the repo already records.

## Publishing notes like these

We write this public repo from those private records rather than copying the records out. Each source project keeps a small publish manifest listing:
- what was exported;
- the source hashes;
- how each item was processed: resized to webp, prompts trimmed, paths and IDs scrubbed.

[tools/scrub_check.py](../tools/scrub_check.py) runs before each commit. It checks against a private, git-ignored pattern list, so the patterns themselves never get published.
