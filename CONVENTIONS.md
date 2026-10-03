# Conventions

These notes grow over time and cover several models and projects, so we write every finding the same way.

## Voice

- **"I"** is me, DienerTech: director, reviewer, and author of these notes.
- **Claude** and **Codex** are named whenever it matters which agent did something, proposed it, or got it wrong.
- **"We"** is the three of us working together.
- My review notes are quoted as I wrote them.

## Status labels

| Label | Meaning |
|---|---|
| **Tested** | It worked for us, in the stated setup, with evidence we kept: prompts, seeds, graphs, frames. |
| **Lead** | It has worked a few times, but with other factors mixed in or a small sample. Worth trying, not relying on. |
| **Hypothesis** | A plausible idea we haven't tested enough. |
| **Failed** | We tried it and it didn't work in our setup. We keep these deliberately. |
| **Approved** | I signed off on the actual output in the cut, as director. That's separate from Claude or Codex passing it in review. |

## Writing a finding

- **Scope it.** Name the model and runtime, the shot type, and how many seeds or takes. "2 clean takes of 2" is more useful than "this works."
- **Name every factor that changed.** A new reference plus a new prompt plus a new seed is not an isolated prompt test.
- **Keep the failure next to the fix.** The failed attempts explain why the working method looks the way it does.
- **Date anything about a model or tool.** For example: "H3 via ComfyUI native nodes, September 2026." Models and runtimes change fast.
- **Link the evidence.** Point from the evergreen notes (`models/`, `techniques/`, `workflows/`) to the project page that holds the proof.

## Folder growth

- `projects/<name>/` is one production: the case study, sampled prompts, and small media.
- `models/<model>/` is how we use one model. It's updated over time and is not tied to one project.
- `techniques/` holds methods that work across models.
- `workflows/` covers how the people and agents work together.
- `tools/` holds small scripts with arguments instead of hardcoded paths. Note what each one is for, and what it isn't for.

## Media

- **Size.** Keep images small: webp, about 1,280 px wide at most. Keep animated loops short, a few seconds at 480 to 640 px.
- **Full renders.** Masters and long clips live on the video host or in releases, not in git.
- **Third-party IP.** Show it only as fan content under its owner's terms. See [NOTICE.md](NOTICE.md).
