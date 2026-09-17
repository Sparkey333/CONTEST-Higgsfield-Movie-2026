# filmdesk

One folder per film. Every generation the film uses, pulled from a single Higgsfield project, laid out as a shot board — one pick per shot, the alternates beside it, every tile a real render by URL — with the prompts for what is not shot yet, the Predictor scores for what is, and a ledger of everything the desk itself made.

It is the toolchain that carried *Matter of Light* to submission, generalised: any short, anime, feature or series is a `project.json`.

## Start a project
```
cp filmdesk/project.example.json filmdesk/projects/<slug>/project.json     # fill in cast ids, acts, shots
python3 filmdesk/ingest.py filmdesk/projects/<slug> <history dump> [...]    # admit this project's takes
python3 filmdesk/build.py  filmdesk/projects/<slug>                          # -> board.html
open filmdesk/serve.command                                                  # or just open board.html
```
Keys, when you want the desk to generate: open `filmdesk/keys.html`, export `keys.env` into `filmdesk/`, then
```
python3 filmdesk/generate.py filmdesk/projects/<slug> --shot S5 --model <cloud model id> --prompt-from-shot
```

## The one-folder rule, and what the API can actually enforce
The desk is exclusive to one Higgsfield project. That exclusivity is enforced the only way the API allows:

- **Admission by cast.** `ingest.py` admits a generation only if it was made with a reference element in this project's cast, or its id is on this project's ledger, or you placed it by hand in `shotmap.json`. Everything else in the account is counted and dropped.
- **Ledger on submission.** `generate.py` writes the request id to `project.json` the moment a submission is accepted, tagged with project and shot, so it can always be pulled back.
- **Folder placement stays in the web app.** No image model and almost no video model accepts a folder id over the API (on this account, only `minimax_h3`, `minimax_h3_max`, `marketing_studio_video`, `sync_so`, `video_upscale`, `video_deflicker`). Generate inside the project in Cinema Studio when the rules require the history to live there; the desk will find those renders by their cast.

## Where history comes from
The account's generation history is paged by the Higgsfield MCP connector in Claude (`show_generations`, written to files when large). Point `ingest.py` at those files. The Cloud API's history endpoints could not be verified from the environment this was built in — `docs.higgsfield.ai` is reachable from yours; if it lists one, `ingest.py`'s loader already accepts a bare list of jobs.

## Files
`ingest.py` · `build.py` · `generate.py` · `keys.html` · `index.html` · `tips.md` · `schema.md` · `serve.command` · `project.example.json` · `projects/<slug>/`

## The worked example
`projects/matter-of-light/` is the real film: 27 shots, 59 admitted takes out of 130 in the account, 18 scored, 4 unshot with prompts in place. Open its `board.html`.
