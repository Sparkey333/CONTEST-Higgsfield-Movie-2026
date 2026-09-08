#!/usr/bin/env python3
"""What has to be inside the submission project, and what does not.

    python3 design/filing-list.py images.json videos.json [--since YYYY-MM-DD] \
        -o design/project-1-filing.md

Why this is a list and not an action. The festival wants every asset in the film
to sit inside the submission project so the generation history verifies it, and
the API cannot put it there. Checked four ways on Sep 8: `list_workspaces`
returns one private workspace with no project target; the model catalogue has a
`folder_id` parameter on `minimax_h3` and `minimax_h3_max` only, only at the
moment of generation, and on no image model; there is no call to list folders,
create one, or move a finished generation; and no marketplace app exposes one.
So filing is permanently a hand action, and the useful thing a script can do is
say exactly what to move.

The list is driven by the film, not by the calendar. Three sources decide what
the film uses:

  design/element-map.json   every reference handle and the generation behind it
  design/anchor-plan.json   the 39 anchors and the job that produced each
  design/shot-ledger.json   each shot's clips by layer

A generation in none of those is exploration. It should stay out of the project,
because everything inside the project reads as part of the submission.
"""
import argparse
import datetime
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEATURED = re.compile(r"leviathan|wet flank of (?:an|the) enormous|near-black flank", re.I)


def read(path, default=None):
    try:
        with open(path) as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


def history(paths):
    """job id -> what the account knows about it, merged across dumps."""
    seen = {}
    for p in paths:
        d = read(p)
        if not d:
            sys.stderr.write("skipped %s (unreadable)\n" % p)
            continue
        for it in d.get("items", []):
            if not it.get("id"):
                continue
            prompt = (it.get("params") or {}).get("prompt") or ""
            seen[it["id"]] = {
                "ts": it.get("createdAt"),
                "kind": it.get("type") or "media",
                "model": it.get("model", ""),
                "status": it.get("status", ""),
                "prompt": " ".join(prompt.split()),
                "url": (it.get("results") or {}).get("rawUrl") or "",
            }
    return seen


def wanted():
    """job id -> (handle, why it is in the film). Ordered elements, anchors, shots."""
    out = {}
    em = read(os.path.join(ROOT, "design/element-map.json"), {})
    for name, e in (em.get("elements") or {}).items():
        if e.get("status") != "live" or not e.get("job"):
            continue
        out[e["job"]] = ("@" + name, "reference handle")
    plan = read(os.path.join(ROOT, "design/anchor-plan.json"), {})
    for f in plan.get("frames", []):
        if f.get("job"):
            out.setdefault(f["job"], (f.get("f", "?"), "anchor frame"))
    ledger = read(os.path.join(ROOT, "design/shot-ledger.json"), {})
    for sid, s in (ledger.get("shots") or {}).items():
        for key, why in (("finished", "finished clip"), ("final", "final clip"),
                         ("concept", "concept clip")):
            v = s.get(key)
            if isinstance(v, dict) and v.get("job"):
                out.setdefault(v["job"], (sid, why))
    return out


def hhmm(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime("%H:%M") if ts else "  ·  "


def day(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d") if ts else "unknown"


HEAD = "| | what | job | made | model | prompt |\n|---|---|---|---|---|---|\n"


def line(job, label, why, h, em_on=None):
    mark = "◆" if FEATURED.search(h.get("prompt", "")) else ""
    when = day(h["ts"]) if h.get("ts") else (em_on or "—")
    return ("| %s | **%s** <br><small>%s</small> | `%s` | %s | `%s` | %s |\n"
            % (mark, label, why, job, when, h.get("model", "—"),
               (h.get("prompt") or "")[:80] or "—"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dumps", nargs="+", help="show_generations JSON dumps, any number")
    ap.add_argument("--since", default=None, help="YYYY-MM-DD, for the recent-activity section")
    ap.add_argument("-o", "--out", default="design/project-1-filing.md")
    a = ap.parse_args()

    hist = history(a.dumps)
    need = wanted()
    if not need:
        sys.exit("nothing to file — element-map.json, anchor-plan.json and "
                 "shot-ledger.json all came back empty")

    em = read(os.path.join(ROOT, "design/element-map.json"), {})
    el_on = {e["job"]: e.get("on") for e in (em.get("elements") or {}).values() if e.get("job")}

    # A wanted job the history dumps do not carry is still wanted. Say so rather
    # than dropping it, or the count quietly under-reports what has to move.
    rows = []
    for job, (label, why) in need.items():
        h = hist.get(job)
        rows.append((job, label, why, h or {"ts": None}, h is not None))
    order = {"reference handle": 0, "anchor frame": 1,
             "concept clip": 2, "final clip": 3, "finished clip": 4}
    rows.sort(key=lambda r: (order.get(r[2], 9), r[1]))

    since_ts = 0
    if a.since:
        since_ts = datetime.datetime.strptime(a.since, "%Y-%m-%d").replace(
            tzinfo=datetime.timezone.utc).timestamp()
    recent = sorted(((j, h) for j, h in hist.items() if h.get("ts") and h["ts"] >= since_ts),
                    key=lambda x: x[1]["ts"])
    stray = [(j, h) for j, h in recent if j not in need]
    featured = [r for r in rows if FEATURED.search(r[3].get("prompt", ""))]

    L = ["# Filing list — what belongs inside the submission project\n\n",
         "Generated by `design/filing-list.py`. Do not hand-edit; re-run it.\n\n",
         "## The rule, and why nothing here is automatic\n\n",
         "Every asset used in the film has to sit inside the submission project, because that "
         "is how the generation history verifies the film. **The API cannot put it there.** "
         "Checked four ways: one private workspace with no project target; a `folder_id` "
         "parameter that exists only on `minimax_h3` and `minimax_h3_max`, only at the moment "
         "of generation, and on no image model; no call anywhere to list folders, create one, "
         "or move a finished generation; and no marketplace app that exposes one. So this is a "
         "list to work down by hand in the web app, and it is regenerated rather than "
         "remembered.\n\n",
         "## How to work it\n\n",
         "1. Open the generation history in the web app.\n"
         "2. Work down **The film's own assets** below. Each row names the handle, frame or "
         "shot it is, so a row you cannot find is a real problem, not a typo.\n"
         "3. Leave everything in **Recent, but not in the film** where it is. The project is "
         "read as the submission; exploration inside it only muddies that.\n"
         "4. Record the date you finished as `filing.filed_through` in `design/gates.json`, "
         "then re-run `python3 design/verify-steps.py` — step 34 checks the two against each "
         "other.\n\n",
         "A row marked ◆ is a creature shot.\n\n"]

    if featured:
        L += ["## The creature shots — %d\n\n" % len(featured),
              "Listed first because they get asked for by name. They also appear in their "
              "own section below; file each once.\n\n", HEAD]
        L += [line(j, lb, wy, h, el_on.get(j)) for j, lb, wy, h, _ in featured]
        L.append("\n")

    L += ["\n## The film's own assets — %d generations\n\n" % len(rows), HEAD]
    L += [line(j, lb, wy, h, el_on.get(j)) for j, lb, wy, h, _ in rows]

    missing = [r for r in rows if not r[4]]
    if missing:
        L += ["\n**%d of these are not in the history dumps this run read.** That is a dump "
              "that did not reach far enough back, not a missing generation — pull more "
              "pages of `show_generations` and re-run before trusting the count:\n\n" % len(missing)]
        L += ["- %s (`%s`)\n" % (lb, j) for j, lb, _, _, _ in missing]

    if a.since:
        L += ["\n## Recent, and referenced by nothing — %d generations\n\n" % len(stray),
              "Made on or after %s and named by no handle, anchor or shot. A row here is "
              "one of two things, and only a person can tell them apart: exploration, which "
              "belongs outside the project; or a re-render that was generated and never "
              "promoted, which belongs in the project the moment it is chosen — promote it "
              "by pointing its handle at this job in `design/element-map.json`, or its shot "
              "at it in `design/shot-ledger.json`, then re-run this script and it moves up "
              "into the section above.\n\n" % a.since, HEAD]
        for j, h in stray:
            L.append(line(j, "—", "not referenced", h))

    L += ["\n## Totals\n\n",
          "- **%d generations belong in the project** (%d reference handles, %d anchors, "
          "%d clips)\n" % (
              len(rows),
              sum(1 for r in rows if r[2] == "reference handle"),
              sum(1 for r in rows if r[2] == "anchor frame"),
              sum(1 for r in rows if r[2].endswith("clip"))),
          "- %d creature shots\n" % len(featured),
          "- %d recent generations that are **not** part of the film\n" % len(stray),
          "\nSouls and reference handles are workspace objects, not generations, so they are "
          "not filed themselves — the image behind each one is, and that is the row above "
          "carrying its `@handle`. `design/element-map.json` holds the whole join.\n"]

    out = a.out if os.path.isabs(a.out) else os.path.join(ROOT, a.out)
    with open(out, "w") as fh:
        fh.writelines(L)
    print("%d in the film (%d not found in these dumps) · %d recent strays -> %s"
          % (len(rows), len(missing), len(stray), a.out))


if __name__ == "__main__":
    main()
