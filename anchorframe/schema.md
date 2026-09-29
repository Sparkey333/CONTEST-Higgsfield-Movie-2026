# project.json — field by field

`schema` · `"anchorframe/1"`.
`title`, `byline`, `logline`, `kind` (`short` | `anime` | `feature` | `series`), `runtime_target_s`.
`format` · `aspect` (`21:9`, `16:9`, `2.39:1`…), `resolution`, `fps`, `container`.
`higgsfield` · `project_name`, `project_url`, `folder_id`, `video_model`, `image_model`, `audio_model`. The folder id is recorded so the desk can say where a project lives; see the README for what the API can and cannot do with it.
`window` · `from` / `to` (ISO dates). Ingest drops anything outside it.
`acts[]` · `id`, `name`, `tone` (`sun` | `void` | `coral` — the board's colour for that act).
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
