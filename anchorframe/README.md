# Anchorframe

**One folder per film. Cast as ids, shots as prompts, takes as a board.**

Anchorframe is the production method that carried *Matter of Light* (5:43, 21:9, made entirely in Higgsfield) from a logline to a festival submission, generalised into a desk any short, anime, feature or series can run from one `project.json` — and shaped to grow into the same desk for games.

Nothing goes to video until it already exists as stills that are right. Every face is attached by id, never re-described. Every take is on a ledger. The cut is chosen from evidence.

## The workflow
Eight stages, five gates, one inner loop. `workflow.json` is the source; `workflow.html` is the page. Every stage carries its **iterate here** card — what triggers a loop, what you do, what lets you out, what it costs — and what actually happened on the film.

```
0 Story → 1 Cast ⟲ ─A─ 2 Anchors ⟲ ─B─ 3 Timing ⟲ ─C─ 4 Motion ⟲ ─D─ 5 Sound ⟲ → 6 Cut ⟲ ─E─ 7 Deliver
```

## Run it
```
cp anchorframe/project.example.json anchorframe/projects/<slug>/project.json    # cast ids, acts, shots
python3 anchorframe/ingest.py anchorframe/projects/<slug> <history dump> [...]   # admit this project's takes
python3 anchorframe/build.py  anchorframe/projects/<slug>                         # -> board.html
python3 anchorframe/desk.py                                                       # -> index.html, workflow.html, links.html
open anchorframe/serve.command
```
Keys, when the desk should generate: `keys.html` → export `keys.env` into `anchorframe/` →
```
python3 anchorframe/generate.py anchorframe/projects/<slug> --shot S5 --model <cloud model id> --prompt-from-shot
```

## The one-folder rule, and what the API can enforce
Exclusive to one Higgsfield project, enforced the only way the API allows: **admission by cast** (a take is yours if it was made with an element in your cast), **ledger on submission** (the request id is on `project.json` before anyone waits), and a **hand map** for anything placed by eye. Folder placement itself stays in the web app — no image model and almost no video model accepts a folder id over the API. `links.json` records every Higgsfield surface the production used, marked verified or not.

## Files
| | |
| --- | --- |
| `workflow.json` → `workflow.html` | the eight stages, gates and iteration loops |
| `links.json` → `links.html` | every link used, by stage, verified or not |
| `desk.py` → `index.html` | the front door |
| `ingest.py` · `build.py` · `generate.py` | the loop |
| `keys.html` | bring your own keys, local only |
| `tips.md` · `schema.md` · `project.example.json` | the tips, the format, the blank |
| `projects/matter-of-light/` | the worked example on real data: 27 shots, 59 of 130 takes admitted, none unplaced, 18 scored |

## From short to feature to game
Same primitives — cast ids, anchors, takes, board, ledger — three products. The short is built. Feature and Series need multi-project cast sharing and an act-level board. Play (games) needs a sheet type per asset class, an export to an engine folder layout, and a review board keyed by asset rather than shot. `workflow.json → expand` states each honestly as built or roadmap.

## Name
*Anchorframe* — the method's spine: the anchor frame, generated first, that every shot is a move between. It scales to games (key art, turnarounds) without changing meaning. A trademark search is yours to run before anything is sold under it.
