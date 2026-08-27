# Production Desk

A local, offline app for building a 5-minute AI short for the Higgsfield Global
Film Festival — and, after that, for building the next one.

Original screen story by **B.L. Barkey**.

## Run it

Clone or download the repository, then:

| | |
| --- | --- |
| **Fastest** | Double-click `index.html`. Everything works straight off the disk. |
| **As a Mac app** | Double-click `Open Director Bible.command` (first run: right-click → **Open**), then Chrome/Edge → **File → Install page as app**. You get a Dock icon and its own window. |
| **By hand** | `python3 -m http.server 8733` in this folder, then open `http://localhost:8733`. |

No build step, no dependencies, no account, no network calls.

> **One thing to know before you start:** run-sheet progress and vault keys live
> in browser local storage, which is per-origin. Opening from a `file://` path
> and from `localhost` gives you two separate sets of saved progress. Pick one
> route and stay on it.

## What's in it

| File | What it's for |
| --- | --- |
| **`index.html`** | The front door. Documents, install routes, open decisions, the **status read**, and the **key vault**. |
| **`director-bible.html`** | The working app. This is where the film actually gets made. |
| **`production-sheet.html`** | One page to keep open beside Higgsfield while you generate. |
| **`lookbook-audit.html`** | The honest list of what the adaptation drops and what has no reference plate. |
| **`ASSET-REGISTER.md`** | Line-referenced audit of every asset against the source chapters. |
| **`PROJECT-BRIEF.md`** | Paste-ready copy for the festival's project brief field. |

### Inside the director's bible

| Section | What's in it |
| --- | --- |
| **Process** | The whole film in bold headlines and short bullets, with iteration and review points marked. Start here. |
| **Control Room** | A 34-step run sheet that remembers where you stopped. One step lit at a time, with the exact screen, model, aspect ratio, prompt and filename per step. |
| **Reuse** | Every part of this document classified generic / template / project, plus what changes for a vertical short, an ad, a music video, a trailer, an episode. |
| **Asset Prompts** | 42 reference assets × 4 variant lanes — A continuity, B in-world plate, C alternate medium, D chroma pass. |
| **Forms & States** | 34 character states across 7 groups. A character is not one asset. |
| **Power Ladders** | Two orthogonal axes — attunement A1–A6 and mind-splits M1→M200+ — carried as prompt modifiers rather than as separate assets. |
| **Filing & Selection** | Three axes: references by identity, anchors by position, shots by pipeline stage. Plus what to do with bad generations. |
| **Revision Loop** | Download, refine, re-upload, mark v2, take it back in. Five moves and a drift-report template. |
| **Binding** | The board that turns favourites into a cohesive whole instead of a favourites reel. |
| **Lessons** | Mistakes already paid for. The page that compounds — carry it into the next project first. |
| **Shot List** | 23 shots — timecode, duration, model, camera direction, seam, and three prompt lanes each. |
| **Pipeline & Gates** | Five hard locks: identity, string, timing, motion, picture. Nothing downstream starts until the gate above holds. |
| **Frame String** | All 39 anchor frames, shared joins and bridge frames, as an interactive ledger. |
| **Model Matrix** | Every video model compared on max length, resolution, frame roles and references. |
| **Key Vault** | BYOK storage with a `.env` export for local tooling. Browser storage only. |

### The status read

Four screenshots, in this order, are enough to reconstruct where the project
stands without describing it. **The first alone answers most of it.**

1. **Project folder tree, fully expanded** — every folder open, asset counts legible
2. **Elements → Characters** — every `@handle` with its image count
3. **All assets, filtered to Liked** — separates *generated* from *chosen*
4. **The generate bar as it sits** — model, aspect ratio, duration

`index.html` → **Status read** holds these as a checklist, takes the images,
and builds a hand-off block with the counts already filled in. It logs each
reading so the day-over-day delta is visible rather than remembered, and
exports the log as CSV.

Capture rules: full window never a region, one screen per image, and do not
scale down on export — filenames and counts are the payload.

## Keys

Bring your own. The vault in `index.html` stores them in browser local storage
and shares them with the director's bible, because both pages are one origin.
Enter a key in either and both have it.

**Exporting:** browsers refuse to save a leading-dot filename — Chromium strips
the dot and appends `.txt` — so the export lands as `production-desk.env`.
Rename it where your tooling wants a dotfile: `mv production-desk.env .env`.
All three names (`.env`, `*.env`, `env.txt`) are gitignored, because the one
that silently isn't covered is the one that gets committed with live keys in it.

## How the film is being made

**Image-first.** Nothing is generated as video until the film exists as stills.
Each shot's first and last frame is made as an anchor image, in film order, and
the motion pass is a move between two frames that are already right. Roughly 200
images to 76 video generations — after which reordering is an editing problem,
not a regeneration problem.

**One identity per character, trained once.** Every other state — damage,
costume, power level — is generated from that same trained identity rather than
re-described. Re-describing a face is how faces drift.

**Three camera grammars, one per movement.** A sustained oner on the Sun,
continuous travelling motion over the ocean, locked-off static frames on the
island. Cuts are motivated by point of view, time or revelation — never by a clip
running out.

**Two passes, then it ships.** A third pass on the same prompt is almost always a
different prompt, not a better one.

## Rights

`LICENSE` (Apache-2.0) covers the software and tooling **only**. It does not
cover `source/`, which holds manuscript chapters of an unpublished novel, nor the
narrative content derived from them. See **`NOTICE`** — read it before reusing
anything here.

Names in this repository are production names, deliberately distinct from the
novel's. The table mapping the two sets is **not committed**: it lives in
`crosswalk.local.js`, which is gitignored. If that file is beside
`director-bible.html` on your machine, the crosswalk appears in the bible's
rights section; in any published copy there is nothing there to leak.

