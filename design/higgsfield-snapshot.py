# -*- coding: utf-8 -*-
"""Turn a raw Higgsfield generation pull into the bible's project snapshot.

The pull itself happens in the Claude session, which is the only place holding
the account credential:

    mcp__Higgsfield__show_generations   (paginate with next_cursor)
    mcp__Higgsfield__show_reference_elements
    mcp__Higgsfield__show_characters
    mcp__Higgsfield__list_workspaces

Large pages are written to files rather than into the conversation; point this
script at those files and it produces one compact snapshot the app can render.

    python3 design/higgsfield-snapshot.py /tmp/bible-data.json <dump>.txt [...] \
        --elements elements.json --characters chars.json --workspace ws.json \
        -o higgsfield.local.json

Matching is by prompt text: every generation carries the prompt it was made
from, and the bible's 42 assets × 4 variants own those prompts, so a generation
can be attributed to an asset and a lane without any naming convention in the
account. Anything unmatched is kept under "loose" rather than dropped — an
unattributed generation is usually the interesting one.

The output is deliberately NOT committed. It holds account handles and asset
URLs; like crosswalk.local.js it stays gitignored and local.
"""
import argparse
import html
import json
import re
import sys


def norm(t):
    """Prompts drift by entity encoding and whitespace between the app and the
    platform; compare on letters and digits only. The whole prompt is compared:
    the split-screen character sheets share a preamble longer than 400
    characters, and a truncated key let the last one indexed swallow the rest
    (Caedom's ascended A lane showed as missing for a day because of it)."""
    t = html.unescape(t or "")
    return re.sub(r"[^a-z0-9]+", "", t.lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bible")
    ap.add_argument("dumps", nargs="+")
    ap.add_argument("--elements")
    ap.add_argument("--characters")
    ap.add_argument("--workspace")
    ap.add_argument("-o", "--out", default="higgsfield.local.json")
    a = ap.parse_args()

    bible = json.load(open(a.bible))
    index = {}
    for p in bible["PREP"]:
        for v in p["v"]:
            index[norm(v["p"])] = (p["k"], p["n"], v["c"], v["n"], v.get("sv", ""), p.get("fld", ""))

    gens = {}
    for f in a.dumps:
        d = json.load(open(f))
        for it in d.get("items", []):
            gens[it["id"]] = it

    assets, loose = {}, []
    for it in gens.values():
        pr = (it.get("params") or {}).get("prompt", "")
        hit = index.get(norm(pr))
        res = it.get("results") or {}
        row = {
            "id": it["id"],
            "at": it.get("createdAt"),
            "model": it.get("model"),
            "ar": (it.get("params") or {}).get("aspect_ratio"),
            "res": (it.get("params") or {}).get("resolution"),
            "thumb": res.get("minUrl") or res.get("rawUrl"),
            "raw": res.get("rawUrl"),
        }
        if hit:
            k, name, lane, lane_n, save_as, folder = hit
            A = assets.setdefault(k, {"name": name, "folder": folder, "lanes": {}})
            L = A["lanes"].setdefault(lane, {"name": lane_n, "save_as": save_as, "items": []})
            L["items"].append(row)
        else:
            row["prompt"] = pr[:160]
            loose.append(row)

    for A in assets.values():
        for L in A["lanes"].values():
            L["items"].sort(key=lambda r: r["at"] or 0, reverse=True)
            L["n"] = len(L["items"])
            L["items"] = L["items"][:8]      # newest few carry the thumbnails
    loose.sort(key=lambda r: r["at"] or 0, reverse=True)

    def load(p):
        return json.load(open(p)) if p else None

    els = load(a.elements) or {}
    chars = load(a.characters) or {}
    ws = load(a.workspace) or {}

    def el_rows(src):
        out = []
        for e in (src.get("items") or []):
            m = (e.get("medias") or [{}])[0]
            out.append({"id": e.get("id"), "name": e.get("name"),
                        "cat": e.get("category"), "thumb": m.get("url")})
        return out

    snap = {
        "pulled": None,          # stamped by the caller; scripts have no clock here
        "project": "MATTER OF LIGHT",
        "workspace": [{"id": w.get("id"), "plan": w.get("plan_type"),
                       "credits": w.get("credits"), "role": w.get("user_role")}
                      for w in (ws.get("workspaces") or [])],
        "souls": [{"id": c.get("soul_id") or c.get("id"), "name": c.get("name"),
                   "status": c.get("status"), "thumb": c.get("thumbnail_url")}
                  for c in (chars.get("items") or [])],
        "elements": el_rows(els),
        "assets": assets,
        "loose": loose[:40],
        "counts": {
            "generations_seen": len(gens),
            "assets_matched": len(assets),
            "assets_total": len(bible["PREP"]),
            "lanes_matched": sum(len(A["lanes"]) for A in assets.values()),
            "loose": len(loose),
        },
    }
    json.dump(snap, open(a.out, "w"), indent=1)
    c = snap["counts"]
    print(f"{a.out} written — {c['generations_seen']} generations, "
          f"{c['assets_matched']}/{c['assets_total']} assets matched, "
          f"{c['lanes_matched']} lanes, {c['loose']} unattributed")


if __name__ == "__main__":
    sys.exit(main())
