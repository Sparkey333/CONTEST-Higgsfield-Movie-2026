# Festival rules, checked against what we have built

Pulled 2026-09-08 from the festival's own announcement and two independent write-ups,
because until now the rules in this repo were carried from memory of an earlier read and
the deadline has already moved twice. Sources at the bottom. **The contest page itself is
unreachable from this container — verify anything below against
`higgsfield.ai/contests/higgsfield-global-film-festival` before you rely on it.**

## The rules, and where we stand

| Rule | What it says | Us |
| --- | --- | --- |
| **Length** | Minimum **3 minutes**. No maximum stated. | 5:00 across 23 shots. Comfortable. |
| **Where assets are made** | Every new video and image asset generated **inside Higgsfield**. | Everything, by construction. |
| **Production history** | Kept in a **dedicated Cinema Studio project**. | The whole reason `project-1-filing.md` exists. 93 generations to move. |
| **Publication** | The finished work published **publicly**. | RUN 33, and the logged-out check is already in it. |
| **Audio** | Music, voice and sound design **AI-generated**, files **uploaded into the submission project**, creator holds the rights. | RUN 31 says exactly this. |
| **Real people** | Inputs **cannot include a real person's face or voice — not even your own**. | ⚠️ **Open. See below.** |
| **Language** | Any language, real or fictional, **with English subtitles or voice-over**. | ⚠️ **Open. See below.** |
| **Format** | MP4 or MOV, up to 4K. | Finish target is 4K; confirm the container at export. |
| **Team** | Solo or up to four, 18+. | Solo. |
| **Entries** | Unlimited, each a standalone film. | One. |
| **Deadline** | **September 14, 11:59 PM UTC.** | Matches what the run sheet already carries. |

## Gap 1 — six reference handles are backed by uploads, not generations

`design/element-map.json` records six elements whose source is a `media_input` — a file
uploaded into the account — rather than an `image_job`:

    caedom-before · caedom-ascended-1 · caedom-mortal-1 · alder-1 · wren-1 · oriane-1

Every other handle points at a generation whose prompt is in this repo, so its provenance
is self-evident. These six do not, and the rule about real faces is absolute: a real
person's face cannot be an input, **including your own**. The five Souls were trained from
images, and a Soul inherits whatever went into it.

This is not an accusation that anything is wrong — as far as the pipeline record goes these
were re-uploads of generated frames. It is a statement that **the repo cannot prove it**,
and six days out that is worth thirty seconds of checking rather than a disqualification.

**What to do:** open each of the six in the account and confirm the file it was built from
is a Higgsfield generation. If any one of them traces back to a photograph of a real person,
delete the handle, delete any Soul trained from it, and regenerate the identity from a text
prompt. Then record the outcome in this file.

## Gap 2 — nothing in the 34 steps produces subtitles

The rule is *English subtitles **or** voice-over*, so the film may already satisfy it: there
is dialogue in Movement I and a V.O. in S22. But no step in the run sheet produces a
subtitle file, and no step confirms that the spoken English covers enough of the film to
count as the alternative. A five-minute film with two minutes of wordless Movement II is
exactly the case where "we have a voice-over" turns out not to be an answer.

**What to do at RUN 31, with the sound:** decide which limb of the rule you are satisfying.
If it is subtitles, burn them in or ship a sidecar with the export — and remember they are
picture, so they are made in Cinema Studio, not in an outside editor. If it is voice-over,
confirm the English is continuous enough to carry the film to a judge who speaks no other
language.

## Canvas, from the platform's own guidance

Canvas is described as the tool for when **one reference set drives several shot prompts** —
a multi-shot scene or an episode — rather than for a single generation. That is exactly the
shape of a movement in this film: one lighting plate and one cast driving nine shots. It is
independent corroboration for the one-board-per-plate layout in `canvas-guide.pdf`, which
was arrived at from the light-drift argument alone.

Practical notes from the same guidance: existing generations are pulled onto a board from
the Assets panel as reference nodes; a node is removed by selecting it and pressing Delete
or Backspace; a whole board can be saved as a reusable template. Boards are collaborative in
real time.

**One project, three boards.** The project is what Rule 7 cares about and there must be
exactly one of those. The boards inside it are a working convenience, and three is right:
one per lighting plate, because every frame on a board inherits that board's key.

## Sources

- [Higgsfield Global Film Festival — how to enter, rules, prize pool](https://higgsfield.ai/blog/higgsfield-global-film-festival)
- [Higgsfield Global Film Festival — contest page](https://higgsfield.ai/contests/higgsfield-global-film-festival)
- [Entry rules and prizes write-up](https://uselamina.ai/blog/higgsfield-global-film-festival-rules-and-entry-guide)
- [How to actually enter, 2026](https://aivideosensei.com/guides/higgsfield-global-film-festival-guide)
- [How do I use Canvas — Higgsfield help centre](https://higgsfield.ai/creator-hub/help-center/tools/how-do-i-use-canvas)
- [AI Canvas — node-based image and video workflow](https://higgsfield.ai/canvas-intro)
- [Which Higgsfield tool should I use](https://higgsfield.ai/creator-hub/help-center/tools/which-higgsfield-tool-should-i-use)
