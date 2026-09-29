#!/usr/bin/env python3
"""Assemble the DATA half of design/final-cut.json — the three planned cuts, the post-deadline
work, the favourites, the uploads and the analyses — from files that already exist. The authored
half (the scene read, the diff, feel, grade, lessons) lives in design/final-cut.notes.json and is
merged by build-final-cut.py.   python3 design/assemble-final-cut.py <scratchpad> <anchorframe-project-dir>
"""
import json, sys, csv, pathlib, datetime
S = pathlib.Path(sys.argv[1]); AF = pathlib.Path(sys.argv[2]); ROOT = pathlib.Path(__file__).resolve().parent.parent
plans = json.load(open(S / "plans.json"))
jobs = json.load(open(S / "new-jobs.json"))["items"]
gens = json.load(open(AF / "generations.json")); gens = gens if isinstance(gens, list) else gens.get("takes") or gens.get("generations")
by8 = {g["id"][:8]: g for g in gens}
proj = json.load(open(AF / "project.json"))
rows = list(csv.DictReader(open(AF / "placements.tsv"), delimiter="\t"))
fav = {r["item_id"] for r in rows if str(r.get("fav")).lower() in ("1", "true", "yes")}
ts = lambda t: datetime.datetime.utcfromtimestamp(float(t)).strftime("%Y-%m-%d %H:%M UTC")

# --- post-deadline work, grouped by what it was for ---
KIND = [("S11 regenerated on the battle sheet", lambda p, s: p.startswith("Regenerate this clip") and "b1b71c32" in s),
        ("S7 regenerated on the battle sheet", lambda p, s: p.startswith("Regenerate this clip")),
        ("NEW-3 · Transition A (the facet becomes ocean)", lambda p, s: p.startswith("Macro, locked, no camera move. A single faceted bead")),
        ("NEW-1 · The mind divides", lambda p, s: p.startswith("Extreme slow motion, camera held wide and low")),
        ("NEW-4 · Transition B (the streak crosses the world)", lambda p, s: p.startswith("Extreme wide, camera high above the curve")),
        ("NEW-2 · The mound", lambda p, s: p.startswith("Locked-off wide from the shoreline")),
        ("S10 upgraded to the leviathan element", lambda p, s: p.startswith("upgrade this attached video gen")),
        ("Editor splice of an S12 take", lambda p, s: True)]
work = []
for it in sorted(jobs, key=lambda i: i["createdAt"]):
    p = (it.get("params") or {}).get("prompt") or ""
    meds0 = (it.get("params") or {}).get("medias") or []
    srcs = " ".join((m.get("data") or {}).get("id", "") for m in meds0)
    label = next(k for k, f in KIND if f(p, srcs))
    res = it.get("results"); url = (res.get("rawUrl") if isinstance(res, dict) else (res[0].get("url") if res else "")) if res else ""
    meds = (it.get("params") or {}).get("medias") or []
    src = [(m.get("data") or {}).get("id", "")[:8] + ":" + str(m.get("role")) for m in meds]
    work.append(dict(id=it["id"], id8=it["id"][:8], at=ts(it["createdAt"]), model=it.get("model"), status=it.get("status"), dur=(it.get("params") or {}).get("duration"), res=(it.get("params") or {}).get("resolution"), audio=(it.get("params") or {}).get("generate_audio"), label=label, sources=src, url=url, favourite=it["id"] in fav))

# --- favourites vs the board's picks ---
favs = []
for s in proj["shots"]:
    sid = s["id"]; pk = s.get("pick") or ""
    f = [g for g in gens if g.get("shot") == sid and g["id"] in fav]
    favs.append(dict(shot=sid, title=s["title"], pick=pk[:8] if pk else None, pick_favourited=bool(pk) and (by8.get(pk[:8], {}).get("id") in fav),
                     favourites=[dict(id8=g["id"][:8], dur=g.get("duration"), at=str(g.get("createdAt"))[:10] if isinstance(g.get("createdAt"), str) else ts(g["createdAt"])[:10], model=g.get("model")) for g in f]))

uploads = [dict(id="7b801917-51e4-4cfc-b62b-e8560f2b8f3e", role="master · the MOV cut after the Sep 15 generations", uploaded="2026-09-16 18:32 UTC", in_project="root · 2026-09-16 21:52 UTC"),
           dict(id="bd28d7c2-25e7-4f5e-9e7f-90c5f710b131", role="Sep 18 upload · 18:55 UTC (the low or the HQ)", uploaded="2026-09-18 18:55 UTC", in_project="—"),
           dict(id="c0bdbe0e-44cb-478c-86a9-f1fc2845e6f5", role="Sep 18 upload · 19:28 UTC (the low or the HQ)", uploaded="2026-09-18 19:28 UTC", in_project="—")]
analyses = [dict(id="b51a7a53-5bd0-4ba0-91fb-a2a7dd004c57", on="7b801917", status="queued"), dict(id="c4da8f1e-583f-48c1-9b74-b6f1d767464f", on="c0bdbe0e", status="queued")]
out = dict(_="Data half of the final-cut read. Regenerate with design/assemble-final-cut.py; the authored half is design/final-cut.notes.json.",
           generated=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"), plans=plans, post_deadline_work=work, favourites=favs, uploads=uploads, analyses=analyses)
json.dump(out, open(ROOT / "design" / "final-cut.data.json", "w"), indent=1, ensure_ascii=False)
print("work items", len(work), "| favourites rows", sum(1 for f in favs if f["favourites"]), "| plans", {k: v["total"] for k, v in plans.items()})
for w in work: print(w["at"], w["id8"], w["label"], "| fav" if w["favourite"] else "", "| src", w["sources"])
