# lab-notes

**Field notes from DienerTech on making films and videos with AI models, code and agents.**

*A note on voice: I'm DienerTech. I direct these projects, review every cut, and write these notes. Claude (Anthropic) and Codex (OpenAI) do much of the hands-on production as coding and production agents, and I name them where their specific work or mistakes matter. "We" means the three of us together.*

This isn't a reproduction kit, a course or a finished method. It's what we learned by making things: what worked, what failed, and how we checked. The models change fast and nobody has solved them, H3 especially. The community is still working out how to use it well, and these notes are our share of that exploration.

[![Support on Ko-fi](https://img.shields.io/badge/Ko--fi-support%20DienerTech-FF5E5B?logo=ko-fi&logoColor=white)](https://ko-fi.com/dienertech)

---

## Featured: *Can You See Me Now* (EVE Online AMV, 2026)

A three-minute anime-style EVE Online music video: a Pilgrim cruiser hunts a Loki, a Myrmidon and a Raven. It went through twenty full drafts. The footage came from MiniMax H3 image-to-video, the keyframes from GPT Images, and the staging from code previs built on real ship geometry. The HUDs and cards are Remotion overlays. Claude and Codex worked as production agents, and I directed and reviewed every cut.

- 🎬 **Watch:** [Can You See Me Now? on YouTube](https://youtu.be/iFqGIgsO468)
- 📓 **How it was made:** [projects/can-you-see-me-now](projects/can-you-see-me-now/)

## What's here

| Folder | What it holds |
|---|---|
| [`projects/`](projects/) | One case study per production. The story of the cut, sample prompts and keyframes, and what we'd do differently. |
| [`models/`](models/) | Notes per model that get updated over time. How we prompt and guide each model, and where it fails. |
| [`techniques/`](techniques/) | Methods that work across models and projects: code previs to AI redraw, compositing repairs, beat-locked editing, code motion layers, Remotion overlays. |
| [`workflows/`](workflows/) | How the humans and agents work together: experiment logs and agent memory, and the asset-accuracy review we now run on everything. |
| [`tools/`](tools/) | A few small, cleaned-up scripts. They're references to adapt, not a framework. |

New productions go in `projects/`. Lessons that carry across projects get pulled up into `models/`, `techniques/` or `workflows/`, with a link back to their evidence.

## How to read these notes

Every finding is labelled with its status. See [CONVENTIONS.md](CONVENTIONS.md) for the full scheme.

- **Tested:** it worked for us, in the stated setup, with evidence.
- **Lead:** promising, but seen only a few times or with other factors mixed in.
- **Hypothesis:** an idea we haven't tested enough.
- **Failed:** something we tried that didn't work. We keep these.
- **Approved:** I signed off on the actual output, as director.

A result from one ship, one seed or one runtime is no universal rule. We say so where it applies.

## Start here

- [How we got the Pilgrim right, after Claude and Codex kept approving wrong ships](workflows/asset-accuracy-review.md)
- [MiniMax H3: guides, anchors, seeds and floods](models/minimax-h3/)
- [Code directs, AI draws: previs with real geometry, then redraw](techniques/code-previs-to-ai-redraw.md)
- [Experiment logs and agent memory: how the work kept compounding](workflows/experiment-logs-and-agent-memory.md)

## Support

Everything here is free. If it helped you, you can [buy DienerTech a coffee on Ko-fi](https://ko-fi.com/dienertech). Support is optional and never gates any content.

## Credits, licenses and notices

- Created and directed by **DienerTech**, with Claude (Anthropic) and Codex (OpenAI) as production and coding agents.
- **EVE Online.** EVE Online® and Fenris Creations™, and all related logos and elements, are trademarks of Fenris Creations hf. (formerly CCP Games). ©2026 Fenris Creations. All rights reserved. This material is used with limited permission of Fenris Creations. No official affiliation or endorsement is stated or implied. No game assets are distributed here.
- **Music.** *Can You See Me Now* is set to "Clowns (Can You See Me Now?)" by t.A.T.u. Thank you to the artists and rights holders. The song appears only in the video and isn't included here.
- **Licenses.** The code is [MIT](LICENSE) and the notes are [CC BY 4.0](LICENSE-CONTENT.md). Third-party IP is excluded; see [NOTICE.md](NOTICE.md).
