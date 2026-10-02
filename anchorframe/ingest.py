#!/usr/bin/env python3
"""Ingest Higgsfield generation history into one project, and nothing else.

    python3 anchorframe/ingest.py anchorframe/projects/<slug> DUMP [DUMP ...] [--images] [--all] [--scores FILE]

A DUMP is a JSON file in the shape the Higgsfield MCP `show_generations` tool returns
({"items":[...]}), a bare list of such items, or a file holding several of either
concatenated. Big pulls land on disk as files, which is exactly what this reads.

The one-folder rule, enforced the only way the API allows: a generation is admitted if
    (0) it is placed in the project (list_project_assets → --placements) — the API can now say so, or
    (a) any reference element it was made with is in this project's cast, or
    (b) its job id is on this project's ledger (the desk made it), or
    (c) its id or prompt is in projects/<slug>/shotmap.json (you placed it by hand),
and it falls inside the project's date window. Everything else is counted and dropped.

Output: projects/<slug>/generations.json — newest first, each take attributed to a shot
where possible, with its clip and poster URLs. Re-run any time; it is a pure function of
its inputs.
"""
import argparse, json, re, sys, html, datetime, pathlib

def load_items(path):
    raw = pathlib.Path(path).read_text()
    dec = json.JSONDecoder(); i = 0; out = []
    while i < len(raw):
        while i < len(raw) and raw[i].isspace(): i += 1
        if i >= len(raw): break
        obj, j = dec.raw_decode(raw, i); i = j
        if isinstance(obj, dict) and "items" in obj: out += obj["items"]
        elif isinstance(obj, list): out += obj
        elif isinstance(obj, dict) and "id" in obj: out.append(obj)
    return out

def norm(t): return re.sub(r"[^a-z0-9 ]+", " ", html.unescape(t or "").lower())
def toks(t): return set(w for w in norm(t).split() if len(w) > 3)
def epoch(v):
    if v is None: return 0.0
    if isinstance(v, (int, float)): return float(v)
    try: return datetime.datetime.fromisoformat(str(v).replace("Z", "+00:00")).timestamp()
    except Exception: return 0.0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project"); ap.add_argument("dumps", nargs="+")
    ap.add_argument("--images", action="store_true", help="admit image generations too (default: video only)")
    ap.add_argument("--all", action="store_true", help="admit everything in the window regardless of cast (audit mode)")
    ap.add_argument("--scores", help="a scores.json to copy alongside (id -> Virality Predictor record)")
    ap.add_argument("--placements", help="project membership from list_project_assets: a TSV (item_id, folder, ...) or a JSON file/list of {items:[...]} pages. When given, membership is the first admission rule and the folder rides on each take.")
    a = ap.parse_args()
    pdir = pathlib.Path(a.project); P = json.load(open(pdir / "project.json"))
    cast_ids = {v for grp in P["cast"].values() for v in grp.values() if not str(v).startswith("<")}
    cast_names = {k for grp in P["cast"].values() for k in grp}
    ledger = {j.get("request_id") or j.get("id") for j in P.get("ledger", {}).get("jobs", [])}
    smap = json.load(open(pdir / "shotmap.json")) if (pdir / "shotmap.json").exists() else {}
    w = P.get("window", {}); t0 = epoch(w.get("from")) if w.get("from") else 0; t1 = epoch(w.get("to")) + 86400 if w.get("to") else 1e12
    shots = {s["id"]: s for s in P["shots"]}
    member = {}
    if a.placements:
        raw = pathlib.Path(a.placements).read_text()
        if a.placements.endswith(".tsv"):
            for line in raw.splitlines()[1:]:
                c = line.split("\t")
                if len(c) >= 2 and c[0]: member[c[0]] = {"folder": c[1], "status": c[3] if len(c) > 3 else "", "favourite": (c[4] == "1") if len(c) > 4 else False}
        else:
            for pg in load_items(a.placements) if raw.lstrip().startswith("[") or raw.lstrip().startswith("{") else []:
                if isinstance(pg, dict) and pg.get("item_id"): member[pg["item_id"]] = {"folder": pg.get("folder_id", ""), "status": pg.get("status", ""), "favourite": bool(pg.get("is_favourite"))}
    by_pick = {}
    for s in P["shots"]:
        if s.get("pick"): by_pick[s["pick"][:8]] = (s["id"], "pick")
        for alt in s.get("alternates", []): by_pick.setdefault(alt[:8], (s["id"], "alternate"))
    prompt_toks = {s["id"]: toks(s.get("prompt", "")) for s in P["shots"] if s.get("prompt")}

    seen, admitted, rejected = {}, [], {"type": 0, "window": 0, "cast": 0}
    for path in a.dumps:
        for it in load_items(path):
            gid = it.get("id"); 
            if not gid or gid in seen: continue
            seen[gid] = True
            typ = it.get("type"); 
            if typ != "video" and not (a.images and typ == "image"): rejected["type"] += 1; continue
            ts = epoch(it.get("createdAt") or it.get("created_at"))
            if not (t0 <= ts <= t1): rejected["window"] += 1; continue
            prm = it.get("params") or {}
            refs = [{"id": r.get("id"), "name": r.get("name")} for r in (prm.get("reference_elements") or [])]
            ok = a.all or gid in member or gid in ledger or gid[:8] in smap or any(r["id"] in cast_ids or r["name"] in cast_names for r in refs)
            if not ok: rejected["cast"] += 1; continue
            res = it.get("results") or {}
            if isinstance(res, list): res = res[0] if res else {}
            g = {"id": gid, "createdAt": ts, "type": typ, "model": it.get("model"),
                 "duration": prm.get("duration"), "resolution": prm.get("resolution"), "w": prm.get("width"), "h": prm.get("height"),
                 "audio": prm.get("generate_audio", prm.get("sound")),
                 "frames": [{"role": m.get("role"), "id": (m.get("data") or {}).get("id")} for m in (prm.get("medias") or []) if isinstance(m, dict)],
                 "refs": refs, "prompt": prm.get("prompt") or "",
                 "thumb": res.get("thumbnailUrl") or res.get("thumbnail_url") or "", "mp4": res.get("rawUrl") or res.get("url") or res.get("video_url") or ""}
            # attribution: ledger > hand map > pick/alternate lists > prompt similarity
            shot, how = None, "unplaced"
            for j in P.get("ledger", {}).get("jobs", []):
                if (j.get("request_id") or j.get("id")) == gid and j.get("shot"): shot, how = j["shot"], "ledger"
            if not shot and gid[:8] in smap: shot, how = (smap[gid[:8]]["shot"] if isinstance(smap[gid[:8]], dict) else smap[gid[:8]]), "map"
            if not shot and gid[:8] in by_pick: shot, how = by_pick[gid[:8]]
            if not shot and prompt_toks:
                gt = toks(g["prompt"]); best, bs = None, 0.0
                for sid, st in prompt_toks.items():
                    if not st or not gt: continue
                    j = len(gt & st) / len(gt | st)
                    if j > bs: best, bs = sid, j
                if best and bs >= 0.35: shot, how = best, f"prompt:{bs:.2f}"
            g["shot"], g["how"] = shot, how
            if gid in member: g["folder"] = member[gid]["folder"]; g["favourite"] = member[gid]["favourite"]; g["placement_status"] = member[gid]["status"]; g["member"] = True
            else: g["member"] = False
            admitted.append(g)
    admitted.sort(key=lambda g: -g["createdAt"])
    (pdir / "generations.json").write_text(json.dumps(admitted, indent=1, ensure_ascii=False))
    if a.scores:
        sc = json.load(open(a.scores)); keep = {k: v for k, v in sc.items() if k in seen}
        (pdir / "scores.json").write_text(json.dumps(keep, indent=1)); print(f"scores: {len(keep)} kept of {len(sc)}")
    from collections import Counter
    per = Counter(g["shot"] for g in admitted if g["shot"]); zero = [s for s in shots if s not in per and shots[s].get("status") not in ("unshot",) and not str(shots[s].get("status","")).startswith("merged")]
    print(f"admitted {len(admitted)}  rejected {rejected}  unplaced {sum(1 for g in admitted if not g['shot'])}  members {sum(1 for g in admitted if g.get('member'))}" + (f"  (placements listed {len(member)}, {sum(1 for m in member if m not in seen)} not in any dump)" if member else ""))
    print("takes per shot:", dict(sorted(per.items(), key=lambda kv: (len(kv[0]), kv[0]))))
    if zero: print("shots with zero takes:", zero)
    return 0

if __name__ == "__main__": sys.exit(main())
