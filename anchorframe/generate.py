#!/usr/bin/env python3
"""Submit a generation for one shot of one project, and put it on the project's ledger.

    python3 anchorframe/generate.py anchorframe/projects/<slug> --shot S5 --model <sdk model id> \
        [--prompt "..." | --prompt-from-shot] [--arg key=value ...] [--args-json '{...}'] [--no-wait]

Keys: HF_KEY, or HF_API_KEY + HF_API_SECRET, in the environment or in anchorframe/keys.env
(KEY=VALUE lines; *.env is gitignored). Get them at https://cloud.higgsfield.ai/api-keys.
Needs `pip install higgsfield-client`.

What "one folder" means here: the request id is written to project.json -> ledger.jobs the
moment the submission is accepted, tagged with the project and the shot. ingest.py admits
anything on the ledger regardless of what the API can filter on, so a generation made through
this script can always be pulled back into the same project. Filing it into the Higgsfield
web-app folder is still done in the web app for models that take no folder_id over the API.

Folder lock: a project whose project.json carries higgsfield.lock is pinned to one Higgsfield
project folder. The Cloud API cannot file into a project folder, so this script refuses to submit
for a locked project unless --outside-lock is passed; generate through the studio or through
Claude's Higgsfield connection instead, which file every take into the locked folder.

Model ids are the Cloud API's (e.g. "bytedance/seedream/v4/text-to-image"), not the web app's.
Reference-element attachment is model-specific — pass whatever the model's docs name via --arg.
"""
import argparse, json, os, sys, time, hashlib, pathlib, datetime

def load_env(path):
    p = pathlib.Path(path)
    if not p.exists(): return
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project"); ap.add_argument("--shot", required=True); ap.add_argument("--model", required=True)
    ap.add_argument("--prompt"); ap.add_argument("--prompt-from-shot", action="store_true")
    ap.add_argument("--arg", action="append", default=[], help="key=value, repeatable (numbers and true/false are parsed)")
    ap.add_argument("--args-json", help="a JSON object merged into the arguments")
    ap.add_argument("--outside-lock", action="store_true", help="submit even though the project is locked to a Higgsfield folder this API cannot file into")
    ap.add_argument("--no-wait", action="store_true"); ap.add_argument("--keys", default=str(pathlib.Path(__file__).parent / "keys.env"))
    a = ap.parse_args()
    P0 = json.load(open(pathlib.Path(a.project) / "project.json")); lock = P0.get("higgsfield", {}).get("lock")
    if lock and not a.outside_lock:
        sys.exit(f"refused: {P0['title']} is locked to the Higgsfield folder '{lock['project']}' ({lock['folder_id']}). "
                 "The Cloud API cannot file a generation into it. Generate from the studio or through Claude instead, or pass --outside-lock to submit anyway.")
    load_env(a.keys)
    if not (os.environ.get("HF_KEY") or (os.environ.get("HF_API_KEY") and os.environ.get("HF_API_SECRET"))):
        sys.exit("no Higgsfield key: set HF_KEY or HF_API_KEY + HF_API_SECRET (env or anchorframe/keys.env). Get one at https://cloud.higgsfield.ai/api-keys")
    try: import higgsfield_client
    except ImportError: sys.exit("pip install higgsfield-client")
    pdir = pathlib.Path(a.project); pfile = pdir / "project.json"; P = json.load(open(pfile))
    shot = next((s for s in P["shots"] if s["id"] == a.shot), None)
    if not shot: sys.exit(f"shot {a.shot} is not in {pfile}")
    args = {}
    if a.prompt_from_shot: args["prompt"] = shot.get("prompt") or sys.exit(f"shot {a.shot} has no prompt")
    if a.prompt: args["prompt"] = a.prompt
    for kv in a.arg:
        k, v = kv.split("=", 1)
        try: v = json.loads(v)
        except Exception: pass
        args[k] = v
    if a.args_json: args.update(json.loads(a.args_json))
    if "prompt" not in args: sys.exit("no prompt: pass --prompt or --prompt-from-shot")
    digest = hashlib.sha256(json.dumps(args, sort_keys=True).encode()).hexdigest()[:12]
    ctl = higgsfield_client.submit(a.model, arguments=args)
    rid = getattr(ctl, "request_id", None) or getattr(ctl, "id", None) or str(ctl)
    entry = {"request_id": rid, "project": P["title"], "outside_lock": bool(lock), "shot": a.shot, "model": a.model, "args_digest": digest,
             "submitted_at": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z", "status": "submitted"}
    P.setdefault("ledger", {}).setdefault("jobs", []).append(entry); pfile.write_text(json.dumps(P, indent=1, ensure_ascii=False))
    print(f"submitted {rid} for {a.shot} on {a.model} — on the ledger")
    if a.no_wait: return 0
    for st in ctl.poll_request_status(): print(" ", type(st).__name__, end="\r")
    res = ctl.get(); print()
    entry["status"] = "completed"; entry["result"] = res; pfile.write_text(json.dumps(P, indent=1, ensure_ascii=False))
    gpath = pdir / "generations.json"; G = json.load(open(gpath)) if gpath.exists() else []
    url = ""
    for key in ("video", "videos", "images", "image"):
        v = res.get(key) if isinstance(res, dict) else None
        if isinstance(v, list) and v: url = v[0].get("url", "") if isinstance(v[0], dict) else str(v[0]); break
        if isinstance(v, dict): url = v.get("url", ""); break
    G.insert(0, {"id": rid, "createdAt": time.time(), "type": "video" if "video" in json.dumps(res)[:200] else "image", "model": a.model,
                 "duration": args.get("duration"), "resolution": args.get("resolution"), "w": None, "h": None, "audio": args.get("generate_audio"),
                 "frames": [], "refs": [], "prompt": args["prompt"], "thumb": "", "mp4": url, "shot": a.shot, "how": "ledger"})
    gpath.write_text(json.dumps(G, indent=1, ensure_ascii=False)); print(f"result {url or res} — appended to generations.json; rebuild the board")
    return 0

if __name__ == "__main__": sys.exit(main())
