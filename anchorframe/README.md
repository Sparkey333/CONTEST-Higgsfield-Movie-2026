# Anchorframe

**One folder per film. Cast as ids, shots as prompts, takes as a board.**

Anchorframe is the production method that carried *Matter of Light* (5:43, 21:9, made entirely in Higgsfield) from a logline to a festival submission, generalised into a desk any short, anime, feature or series can run from one `project.json` — and shaped to grow into the same desk for games.

Nothing goes to video until it already exists as stills that are right. Every face is attached by id, never re-described. Every take is on a ledger. The cut is chosen from evidence.

## The workflow
Nine stages, five gates, one inner loop — the ninth reads the finished cut back against the board. `workflow.json` is the source; `workflow.html` is the page. Every stage carries its **iterate here** card — what triggers a loop, what you do, what lets you out, what it costs — and what actually happened on the film.

```
0 Story → 1 Cast ⟲ ─A─ 2 Anchors ⟲ ─B─ 3 Timing ⟲ ─C─ 4 Motion ⟲ ─D─ 5 Sound ⟲ → 6 Cut ⟲ ─E─ 7 Deliver → 8 Learn ⟲
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
Exclusive to one Higgsfield project. Since Sep 29 the connector exposes `list_projects`, `list_folders` and `list_project_assets`, so **membership is now the first admission rule**: page the project's assets, save them as `placements.tsv`, and `ingest.py --placements` admits every item placed in the project, with its folder and favourite flag on the take. The older rules still apply behind it — **admission by cast**, **ledger on submission**, a **hand map** — because a project can hold takes made with a retired cast, and the desk can make takes the web app has not filed yet. Generation still lands in the folder only when made in the web app or on a model that takes `folder_id`; `create_folder` / `create_project` now exist for the desk to file into. `links.json` records every Higgsfield surface the production used, marked verified or not.

## Files
| | |
| --- | --- |
| `workflow.json` → `workflow.html` | the nine stages, gates and iteration loops |
| `links.json` → `links.html` | every link used, by stage, verified or not |
| `desk.py` → `index.html` | the front door |
| `ingest.py` · `build.py` · `generate.py` | the loop |
| `keys.html` | bring your own keys, local only |
| `tips.md` · `schema.md` · `project.example.json` | the tips, the format, the blank |
| `projects/matter-of-light/` | the worked example on real data: 27 shots, 59 of 130 takes admitted, none unplaced, 18 scored |
| `projects/stone-of-matter-ep2-darkness/` | the second film, written before a frame exists: 26 shots in four movements, every pending sheet briefed, the previous film's lessons applied as rules |

## The second film
`projects/stone-of-matter-ep2-darkness/` is the desk's first sequel: a board written from the Episode 2 screenplay the day after the Episode 1 read, with nothing generated yet. It inherits the first film's plates and Souls **by id** (`project.json → inherits`), carries the Learn stage's findings as rules (`inherits.lessons_applied`), briefs every new face and place in one line (`sheets`) and locks its three cues before the stills reel (`music`). Its board renders every shot as an unshot prompt, ready to paste; `schema.md` documents the four optional blocks.

## From short to feature to game
Same primitives — cast ids, anchors, takes, board, ledger — three products. The short is built. Feature and Series need multi-project cast sharing and an act-level board. Play (games) needs a sheet type per asset class, an export to an engine folder layout, and a review board keyed by asset rather than shot. `workflow.json → expand` states each honestly as built or roadmap.

## Name
*Anchorframe* — the method's spine: the anchor frame, generated first, that every shot is a move between. It scales to games (key art, turnarounds) without changing meaning. A trademark search is yours to run before anything is sold under it.
