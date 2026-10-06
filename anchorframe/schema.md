# project.json — field by field

`schema` · `"anchorframe/1"`.
`title`, `byline`, `logline`, `kind` (`short` | `anime` | `feature` | `series`), `runtime_target_s`.
`format` · `aspect` (`21:9`, `16:9`, `2.39:1`…), `resolution`, `fps`, `container`.
`higgsfield` · `project_name`, `project_url`, `folder_id`, `video_model`, `image_model`, `audio_model`. The folder id is recorded so the desk can say where a project lives; see the README for what the API can and cannot do with it.
`window` · `from` / `to` (ISO dates). Ingest drops anything outside it.
`acts[]` · `id`, `name`, `tone` (`sun` | `void` | `coral` | `stardust` | `forest` | `lake` | `dark` — the board's colour for that act).
`cast` · `characters`, `environments`, `props`, `fx` — each `name → element uuid`. This is the admission list: a generation is this project's if any element it was made with is here.
`souls` · `name → soul uuid`. One Soul per generation is the platform limit; multi-person shots run on elements.
`retired` · `old name → old uuid`. Swept out of prompts; kept so old renders still attribute.
`shots[]` · `id`, `act`, `title`, `duration_s`, `audio` (bool), `status` (`shot` | `unshot` | `merged-into:<id>`), `prompt` (the paste-ready text, with `@[name](uuid)` references), `pick` (job id), `alternates[]` (job ids), `why`, `regenerate` (bool), `notes`.
`board` · `max_alternates`, `score_over_pick` (when no explicit pick, take the highest Predictor score).
`ledger.jobs[]` · every submission `generate.py` made: `request_id`, `project`, `shot`, `model`, `args_digest`, `submitted_at`, `status`, `result`.

## Sidecars in the project folder
`generations.json` — written by `ingest.py`; the admitted takes, newest first, with `shot` and `how` (`pick` | `alternate` | `map` | `ledger` | `prompt:0.xx` | `unplaced`).
`scores.json` — `job id → Virality Predictor record` (`overall`, `hook`, `engagement`, `viral`, `dmn_mean`, `peak_second`, `dur`, `global[]`).
`shotmap.json` — optional hand placement, `8-char id → {shot, title}`.
`board.html` — the output. Never edit it.

## `final` — the delivered film

Written at stage 8. `master` is the file the jury saw (upload id, container, when uploaded, where it sits in the project); `exports` are the later encodes (the low proxy, the HQ); `analyses` are the platform's scene-analysis job ids on each; `read` points at where the diff against the board lives. Every id here is an upload, not a generation, so `ingest.py` never admits them — they are the film, not a take.

## Sequels — `series`, `inherits`, `sheets`, `music` (optional)

Added for the second film. None of them is read by `build.py`; they are the record the next reader needs.
`series` · where the film sits: `world`, `book`, `episode`, `follows` (the previous project's slug), `source`, `codex` (the note in the story codex), `form`, `names` (which name set the prompts use, and why).
`inherits` · what this film takes from the previous one **by id**: `elements` (`name → uuid`, attached in prompts exactly as before), `souls`, `read` (one paragraph of what the previous film's Learn stage found) and `lessons_applied[]` (what this board does differently because of it).
`sheets` · for a board written before anything is generated: one-line briefs for every pending element under `characters`, `environments`, `props`, `fx`, so Stage 1 can run from the project file alone. A pending id is the literal `<element uuid>`; prompts reference it as `@name` so the board marks it, and switch to `@[name](uuid)` when the sheet exists.
`music` · the cues, which shots each covers, and the words the cuts land on — written at Stage 0, because tip 32 says so.

## Carrying a cast over — `higgsfield.lock`, `higgsfield.links`, `souls`, `carried`, `made`, `stills`, `passes`

The record of moving from one episode to the next (the process is on the workflow page under *Carry over*, and `carry.py` runs it).
`higgsfield.lock` · `{project, project_id, folder_id, workspace_id, set, rule}` — the one folder every generation and remix is filed into. The studio refuses to submit unless its folder matches; `generate.py` refuses for a locked project; `carry.py check` fails on any `stills` or `ledger` row outside it.
`higgsfield.links` · `{id: {name, url, for, verified}}` — overrides for the desk's own project links (`hf_project`, `hf_elements`, `hf_public_project`, `hf_assets`), so each edition's desk opens its own episode's folder and nothing else.
`souls` · `{name: {soul_id, was, element, status}}` — a Soul is reused by id across episodes (`was` names the part it played before); it is never duplicated.
`carried` · `{_, set, map{old: new}, items[{name, id, base, from, sheet, tweak}]}` — what came over from the previous episode: `base` is the untouched duplicate (`ep<N>-<name>-base`), `id` the dressed element the prompts attach, `sheet` the generation it was dressed from.
`made` · `{_, items[{name, id, kind, sheet, note}]}` — elements first made in this episode.
`stills[]` · `{shot, lane, id, model, res, credits, url, thumb, note, animated, folder_id, at, pass}` — anchor frames by shot; `shot` may be `cast` (sheets and plates) or `bridge-out` (tags), and `build.py` draws them on the cards, the Cast section and Bridges.
`passes[]` · one entry per generation pass: `{date, name, stills, videos, blocked, credits, how, learned[]}`.
`inherits.pace_and_look` · the previous film's rhythm and grade turned into this film's generation rules.

## Lanes, forms, the episode, bridges, themes (optional, rendered by `build.py`)

`shots[].lanes[]` · the Matter of Light shot grammar: `{c, name, why, prompt}` with `c` = `A` (ships — the one the forms and the frame string assume), `B` (coverage — a second angle so the editor has more than one), `C` (chroma — graded to its ceiling for spots, key art and the music video). `prompt` on the shot stays lane A, so `generate.py --prompt-from-shot` is unchanged.
`forms[]` · one story at every length, cut from the same shots: `{id, kind, name, target_s, why, cut[]}` where each cut entry is `{shot, lane, s, note?, part?}` or an editorial `{card, s}`; `auto: "shots"` builds the cut from the board in order. The board draws a ribbon and a timed cut list per form.
`episode` · the long form (20–60 minutes): `{title, note, scenes[{n, scene, pages, min, shots[], adds}], grow}` — the screenplay's scenes at a page a minute, which shots of the short cover each, and what the episode puts back.
`bridges` · transitions between episodes: `{note, in{title, status, links[{from, to}]}, out{…}}`. A transition belongs to the episode it opens and is listed by the one it closes.
`themes` · the soundtrack: `{title, note, songs[{id, title, use, theme, from, fit, style, lyrics}]}` — `style` and `lyrics` are paste-ready for a music generator (section tags in brackets).

## `desk.json` (optional, one per branch)
`{title, edition, series, episode, current, eyebrow, description, editions_note, editions[{edition, episode, title, state, branch, url, note}]}` — which desk this branch is. `desk.py` uses it for the page title, the edition badge and the Editions panel, and lists the `current` project first.

## The studio's data (`intake.json`, `projects/<slug>/intake.json`, `parity.json`, and the shared store)
`intake.json` · `{sections[{id, name}], questions[{id, section, kind: text|long|choice|multi, options?, upload?, feeds, q, why}]}` — the template's questions; `feeds` names the project field each answer fills.
`projects/<slug>/intake.json` · `{proposed: {qid: text | [options]}}` — what the repository already knows, shown as a proposal, never as an answer.
`parity.json` · `{columns[{id, name, note}], groups[{name, rows[{f, <column id>: built|partial|planned|none, n}]}], plan[{phase, items[]}]}`.
The studio's shared store (read by Claude on sync): `answers/<qid>` `{value, by, at}` · `uploads/<asset id>` `{asset, name, kind, tag, note, contentType, size, by, at}` · `ideas/<id>` `{text, tag, by, at}` · `shots/<shot id>` `{status, note, by, at}` · `jobs/<id>` `{target, label, tool, model, seconds, aspect, credits, ids[], status, payload, by, at}` · `links/<Higgsfield item id>` `{target: "sheet:<name>" | "shot:<id>:<lane>", kind, model, auto?, by, at}`.
