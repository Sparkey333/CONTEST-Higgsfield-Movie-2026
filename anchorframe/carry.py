#!/usr/bin/env python3
"""Carry a cast from one episode to the next, and keep the ids straight.

    python3 anchorframe/carry.py plan  anchorframe/projects/<next> [--from anchorframe/projects/<prev>]
    python3 anchorframe/carry.py link  anchorframe/projects/<next>
    python3 anchorframe/carry.py check anchorframe/projects/<next>

plan   Sorts the previous episode's cast against this one into bins: inherited by id unchanged
       (inherits.elements), carried and dressed (carried.items), still to carry (a pending name the
       carried.map points at an old element), new (a pending name with no counterpart; it gets a sheet
       from its brief), and left behind. Souls are listed by id: they are reused, never duplicated.
       Prints a checklist and writes <next>/carry-plan.json.
link   Rewrites every bare @name in the shots, lanes, forms and episode to @[name](id) for each cast
       name whose id is filled. Idempotent; run it after every batch of new elements.
check  Fails (exit 1) on a prompt that attaches a previous episode's element that is not inherited,
       a ledger or stills row filed outside higgsfield.lock, or one id under two cast names. Pending
       names still in prompts are listed as warnings.

The Higgsfield side (duplicating an element, making the dress sheet, creating the final element) runs
through the connector — Claude or the studio — because elements are made there. This file keeps the
record honest: which id plays which part, where it came from, and that nothing points backwards.
"""
import argparse, json, pathlib, re, sys

PENDING = "<element uuid>"
KINDS = ("characters", "environments", "props", "fx")
SKIP = {"cast", "sheets", "souls", "inherits", "carried", "ledger", "stills", "passes", "retired", "higgsfield"}
UID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

def load(pdir): return json.load(open(pathlib.Path(pdir) / "project.json"))
def cast_of(P):
    out = {}
    for k in KINDS:
        for n, v in P.get("cast", {}).get(k, {}).items():
            if not n.startswith("_"): out[n] = (k, None if v == PENDING else v)
    return out
def prompts(x, path=""):
    if isinstance(x, str): yield path, x
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from prompts(v, f"{path}[{i}]")
    elif isinstance(x, dict):
        for k, v in x.items():
            if path == "" and k in SKIP: continue
            yield from prompts(v, f"{path}.{k}" if path else k)

def plan(a):
    P = load(a.project); nxt = pathlib.Path(a.project)
    prev_dir = pathlib.Path(a.prev) if a.prev else nxt.parent / P.get("inherits", {}).get("from", "")
    Q = load(prev_dir) if (prev_dir / "project.json").exists() else {"cast": {}}
    old, new = cast_of(Q), cast_of(P)
    inh = P.get("inherits", {}).get("elements", {}); car = P.get("carried", {}); items = car.get("items", [])
    cmap = car.get("map", {})
    used_old = set(inh.values()) | {i.get("from_id") for i in items if i.get("from_id")}
    bins = {"inherit": [], "carried": [], "to_carry": [], "new": [], "left": []}
    for n, i in inh.items(): bins["inherit"].append({"name": n, "id": i})
    for i in items: bins["carried"].append({"name": i["name"], "id": i["id"], "from": i.get("from", ""), "tweak": i.get("tweak", "")})
    carried_names = {i["name"] for i in items}
    for n, (k, i) in new.items():
        if i or n in carried_names or n in inh: continue
        src = next((o for o, t in cmap.items() if t == n), None)
        brief = P.get("sheets", {}).get(k, {}).get(n, "")
        if src: bins["to_carry"].append({"name": n, "kind": k, "from": src, "from_id": old.get(src, (None, None))[1], "brief": brief}); used_old.add(old.get(src, (None, None))[1])
        else: bins["new"].append({"name": n, "kind": k, "brief": brief})
    for o, (k, i) in old.items():
        if i and i not in used_old: bins["left"].append({"name": o, "kind": k, "id": i})
    souls = {"previous": Q.get("souls", {}), "inherited": P.get("inherits", {}).get("souls", {}), "this": P.get("souls", {})}
    out = {"from": str(prev_dir), "to": str(nxt), "lock": P.get("higgsfield", {}).get("lock", {}).get("folder_id"), "bins": bins, "souls": souls}
    (nxt / "carry-plan.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"# Carry plan: {Q.get('title', prev_dir.name)} → {P['title']}\n")
    print(f"Lock: {out['lock'] or 'NONE — set higgsfield.lock before generating anything'}\n")
    for key, title in (("inherit", "Inherited by id, unchanged"), ("carried", "Carried and dressed"), ("to_carry", "Still to carry: duplicate, dress, make the final element"), ("new", "New: a sheet from the brief"), ("left", "Left in the previous episode")):
        rows = bins[key]; print(f"## {title} ({len(rows)})")
        for r in rows:
            print("- [{}] @{}{}{}".format("x" if key in ("inherit", "carried") else " ", r["name"], f"  {r['id']}" if r.get("id") else "", f"  ← {r['from']}" if r.get("from") else ""))
        print()
    print("## Souls — reused by id, never duplicated")
    for n, s in (P.get("souls") or {}).items():
        if not n.startswith("_"): print(f"- @{n}: {s.get('soul_id') if isinstance(s, dict) else s}" + (f" (was {s['was']})" if isinstance(s, dict) and s.get("was") else ""))
    print(f"\nwrote {nxt / 'carry-plan.json'}")
    return 0

def link(a):
    pf = pathlib.Path(a.project) / "project.json"; P = json.load(open(pf)); C = cast_of(P)
    subs = [(re.compile(r"@" + re.escape(n) + r"(?![a-z0-9_-])"), f"@[{n}]({i})") for n, (k, i) in sorted(C.items(), key=lambda kv: -len(kv[0])) if i]
    count = {"n": 0}
    def walk(x, top=False):
        if isinstance(x, str):
            for r, s in subs: x, k = r.subn(s, x); count["n"] += k
            return x
        if isinstance(x, list): return [walk(v) for v in x]
        if isinstance(x, dict): return {k: (v if top and k in SKIP else walk(v)) for k, v in x.items()}
        return x
    P = walk(P, top=True); pf.write_text(json.dumps(P, indent=1, ensure_ascii=False))
    print(f"linked {count['n']} references across {sum(1 for _ in subs)} filled cast names")
    return 0

def check(a):
    P = load(a.project); C = cast_of(P); errs, warns = [], []
    lock = P.get("higgsfield", {}).get("lock", {}).get("folder_id")
    if not lock: errs.append("no higgsfield.lock: the project is not pinned to a folder")
    for sec, rows in (("stills", P.get("stills", [])), ("ledger.jobs", P.get("ledger", {}).get("jobs", []))):
        for r in rows:
            if lock and r.get("folder_id") and r["folder_id"] != lock: errs.append(f"{sec}: {r.get('id') or r.get('request_id')} is filed in {r['folder_id']}, not the lock")
    ids = {}
    for n, (k, i) in C.items():
        if i: ids.setdefault(i, []).append(n)
    for i, ns in ids.items():
        if len(ns) > 1: errs.append(f"one id under two names: {i} → {', '.join(ns)}")
    prev = pathlib.Path(a.project).parent / P.get("inherits", {}).get("from", "")
    old = {i for _, (k, i) in cast_of(load(prev)).items() if i} if (prev / "project.json").exists() else set()
    allowed = set(P.get("inherits", {}).get("elements", {}).values()) | {i for i in ids}
    pend = {}
    for path, t in prompts(P):
        for u in UID.findall(t):
            if u in old and u not in allowed: errs.append(f"{path} attaches a previous-episode element that is not inherited: {u}")
        for m in re.finditer(r"@([a-z][a-z0-9_-]{2,40})(?![a-z0-9_-])", t):
            n = m.group(1)
            if n in C and not C[n][1]: pend[n] = pend.get(n, 0) + 1
    for n, c in sorted(pend.items(), key=lambda kv: -kv[1]): warns.append(f"pending @{n} in {c} prompt{'s' if c > 1 else ''}")
    for w in warns: print("warn ", w)
    for e in errs: print("ERROR", e)
    print(f"{len(errs)} errors, {len(warns)} warnings · lock {lock or 'none'} · {sum(1 for v in C.values() if v[1])} of {len(C)} cast ids filled")
    return 1 if errs else 0

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("plan"); p.add_argument("project"); p.add_argument("--from", dest="prev")
    sp.add_parser("link").add_argument("project"); sp.add_parser("check").add_argument("project")
    a = ap.parse_args()
    return {"plan": plan, "link": link, "check": check}[a.cmd](a)

if __name__ == "__main__": sys.exit(main())
