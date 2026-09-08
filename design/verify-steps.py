# -*- coding: utf-8 -*-
"""Answer one question for each of the 34 RUN steps: has it actually been done?

    node design/extract-data.mjs --prompts > /tmp/bible-data.json
    python3 design/verify-steps.py /tmp/bible-data.json -o design/progress.json

Three kinds of evidence, and the distinction matters more than the score:

  auto     something in a file proves it. A generation exists for this exact
           prompt; an element handle exists; a Soul is ready; a clip is in the
           ledger. These are checked here and cannot be talked up.
  manual   nobody can prove it from a file. A gate is a person looking at a
           screen and deciding. Every one of these carries the steps to run by
           hand, and stays "todo" until someone records the answer in
           design/gates.json.
  blocked  the evidence lives in a file that is not present. The account
           snapshot and the crosswalk are both gitignored, so a clone of this
           repo can verify structure but not the account.

Nothing here writes to the account or spends a credit. Re-run it as often as
you like; it is the cheapest thing in the project.
"""
import argparse
import datetime
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEADLINE = datetime.datetime(2026, 9, 14, 23, 59, tzinfo=datetime.timezone.utc)


def clean(t):
    return re.sub(r"<[^>]+>", "", html.unescape(t or ""))


def load(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


class Facts:
    """Everything the checks are allowed to look at, loaded once."""

    def __init__(self, bible):
        self.bible = bible
        self.snapshot = load(os.path.join(ROOT, "higgsfield.local.json"))
        self.anchors = load(os.path.join(ROOT, "design/anchor-plan.json"), {})
        self.shots = load(os.path.join(ROOT, "design/shot-ledger.json"), {})
        self.gates = load(os.path.join(ROOT, "design/gates.json"), {})
        self.elements = {}
        self.souls = {}
        if self.snapshot:
            for e in self.snapshot.get("elements", []):
                self.elements[e["name"]] = e["id"]
            for s in self.snapshot.get("souls", []):
                self.souls[s["name"]] = s.get("status")
        # The ledger records what changed after the snapshot was pulled, so it
        # wins: a Soul that finished training since then is ready, not training.
        for name, eid in (self.shots.get("elements_since_snapshot") or {}).items():
            self.elements[name] = eid
        for name, status in (self.shots.get("souls_since_snapshot") or {}).items():
            self.souls[name] = status

    def lane(self, key, lane="A"):
        if not self.snapshot:
            return None
        a = self.snapshot.get("assets", {}).get(key)
        if not a:
            return []
        return a.get("lanes", {}).get(lane, {}).get("items", [])

    def frames(self):
        return self.anchors.get("frames", [])


# --- the checks -------------------------------------------------------------
# Each returns (state, have, need, evidence[]). state is pass / partial / todo /
# blocked. A check that needs the snapshot returns blocked without it, never a
# false pass.

def need_assets(f, keys, elements=(), souls=()):
    if f.snapshot is None:
        return ("blocked", 0, len(keys) + len(elements) + len(souls),
                ["higgsfield.local.json not present — run design/higgsfield-snapshot.py"])
    ev, have = [], 0
    need = len(keys) + len(elements) + len(souls)
    for k in keys:
        items = f.lane(k)
        if items:
            have += 1
        else:
            ev.append("no A-lane generation for asset %s" % k)
    for name in elements:
        if name in f.elements:
            have += 1
        else:
            ev.append("no element handle @%s" % name)
    for name in souls:
        st = f.souls.get(name)
        if st == "ready":
            have += 1
        elif st:
            ev.append("Soul %s is %s, not ready" % (name, st))
        else:
            ev.append("no Soul named %s" % name)
    state = "pass" if have == need else ("partial" if have else "todo")
    if state == "pass":
        ev.append("%d of %d present" % (have, need))
    return (state, have, need, ev)


def check_anchors(f, movement, need):
    fr = [x for x in f.frames() if x.get("mv") == movement]
    done = [x for x in fr if x.get("job")]
    ev = []
    if not fr:
        return ("blocked", 0, need, ["design/anchor-plan.json has no frames"])
    layer = f.anchors.get("meta", {}).get("layer", "skeleton")
    ev.append("%d of %d generated (%s pass — one image each, not yet selected)"
              % (len(done), need, layer))
    sel = [x for x in fr if x.get("selected")]
    if sel:
        ev.append("%d selected from a batch" % len(sel))
    state = "pass" if len(done) >= need and len(sel) >= need else (
        "partial" if done else "todo")
    return (state, len(sel) if sel else len(done), need, ev)


def check_shots(f, ids, field):
    led = f.shots.get("shots", {})
    if not led:
        return ("todo", 0, len(ids), ["design/shot-ledger.json has no shots yet"])
    have = [s for s in ids if (led.get(s) or {}).get(field)]
    missing = [s for s in ids if s not in have]
    ev = ["%d of %d have a %s clip" % (len(have), len(ids), field)]
    if missing:
        ev.append("missing: " + ", ".join(missing))
    state = "pass" if len(have) == len(ids) else ("partial" if have else "todo")
    return (state, len(have), len(ids), ev)


def check_gate(f, gate):
    g = (f.gates.get(gate) or {})
    if g.get("held"):
        return ("pass", 1, 1, ["held %s by %s" % (g.get("on", "?"), g.get("by", "?"))])
    return ("todo", 0, 1, ["not recorded in design/gates.json"])


def check_rights(f):
    """Every prompt that ships is scanned for the novel's vocabulary.

    The word list lives in crosswalk.local.js, which is gitignored, so this
    check is blocked rather than passed on a machine that does not hold it.
    """
    path = os.path.join(ROOT, "crosswalk.local.js")
    if not os.path.exists(path):
        return ("blocked", 0, 1, ["crosswalk.local.js not present — cannot scan"])
    src = open(path, encoding="utf-8").read()
    terms = set()
    for m in re.finditer(r"<i>([^<]{3,40})</i>", src):
        t = clean(m.group(1)).strip().lower()
        if len(t) > 3:
            terms.add(t)
    for m in re.finditer(r"/\s*([A-Z][A-Z]{3,})\b", src):
        terms.add(m.group(1).lower())
    if not terms:
        return ("blocked", 0, 1, ["crosswalk.local.js parsed to no terms"])
    hits = []
    for p in f.bible["PREP"]:
        for v in p["v"]:
            body = clean(v.get("p", "")).lower()
            for t in terms:
                if re.search(r"\b%s\b" % re.escape(t), body):
                    hits.append("%s/%s contains %r" % (p["k"], v["c"], t))
    for s in f.bible["SHOTS"]:
        for v in s["v"]:
            body = clean(v.get("p", "")).lower()
            for t in terms:
                if re.search(r"\b%s\b" % re.escape(t), body):
                    hits.append("%s/%s contains %r" % (s["id"], v["c"], t))
    if hits:
        return ("todo", 0, 1, ["%d prompt(s) still carry novel vocabulary" % len(hits)] + hits[:8])
    return ("pass", 1, 1, ["%d terms scanned across every shipped prompt, no hit" % len(terms)])


def check_refs_in_shots(f):
    """Feature parity with the anchors: a shot prompt has to name its elements.

    The Sep 8 clips proved why. Every prompt matched the bible exactly and every
    one was still generated text-only — no start frame, no end frame, no
    element — so nothing in them can hold an identity.
    """
    total = len(f.bible["SHOTS"])
    have = 0
    missing = []
    for s in f.bible["SHOTS"]:
        a = [v for v in s["v"] if v["c"] == "A"]
        body = clean(a[0].get("p", "")) if a else ""
        if "@" in body or "attach" in body.lower():
            have += 1
        else:
            missing.append(s["id"])
    ev = ["%d of %d shot A-prompts name their references" % (have, total)]
    if missing:
        ev.append("text-only: " + ", ".join(missing))
    state = "pass" if have == total else ("partial" if have else "todo")
    return (state, have, total, ev)


WORLD = ["courtyard", "beach", "bgbloom", "temple", "bgisle", "bgmachira",
         "stone", "shell", "coral", "levbody", "propore", "ships", "proptear",
         "fxhollow", "fxmind", "fxmountain", "fxkill"]
WORLD_EL = ["courtyard-of-worlds", "nacre-beach", "corals-abyss", "white-temple",
            "keepers-isle", "machira-orbit", "founding-stone", "aura-shell",
            "leviathan-plating", "leviathan", "iron-spears", "twelve-ships",
            "frozen-tear", "fx-hollow", "fx-segmented-mind",
            "fx-floating-mountain", "fx-kill-beat"]

STEPS = {
    1: dict(kind="manual", manual=[
        "Open the festival rules page and read the from-scratch rule.",
        "Confirm nothing in the project pre-dates the contest window."]),
    2: dict(kind="manual", manual=[
        "Open Cinema Studio and confirm the festival project exists.",
        "Confirm every generation so far is inside that project, not loose."]),
    3: dict(check=lambda f: need_assets(f, ["aurarule"], ["aura-grammar"])),
    4: dict(check=lambda f: need_assets(f, ["gwen"], ["oriane"], ["oriane"])),
    5: dict(check=lambda f: need_assets(f, ["gwendmg"], ["oriane-damaged"])),
    6: dict(check=lambda f: need_assets(f, ["ladder"], ["ladder-oriane"])),
    7: dict(check=lambda f: need_assets(f, ["caedomasc", "caedommortal"],
                                        ["caedom-ascended-1", "caedom-before"],
                                        ["caedom-ascended", "caedom-before"])),
    8: dict(check=lambda f: need_assets(f, ["alder"], ["alder"], ["alder"])),
    9: dict(check=lambda f: need_assets(f, ["wren"], ["wren"], ["wren"])),
    10: dict(check=lambda f: need_assets(f, ["pup", "guard"],
                                         ["threadwright", "keeper", "keeper-kneel"])),
    11: dict(check=lambda f: need_assets(f, ["turned", "levrider"],
                                         ["turned", "lev-rider"])),
    12: dict(check=lambda f: need_assets(
        f, ["bhollow", "bwater", "benergy", "bgravity", "bmetal", "bthrall", "banchor"],
        ["turned-hollows", "turned-water", "turned-energy", "turned-gravity",
         "turned-metals", "turned-thrall", "turned-anchor"])),
    13: dict(check=lambda f: need_assets(f, ["darkladder"], ["ladder-attunement"])),
    14: dict(check=lambda f: need_assets(f, ["l1", "l2", "l3", "platemv3b"],
                                         ["plate-sun", "plate-ocean-dark",
                                          "plate-island", "plate-bombardment"])),
    15: dict(check=lambda f: need_assets(f, WORLD, WORLD_EL)),
    16: dict(kind="gate", gate="A", manual=[
        "Put every reference on one screen, in the canvas or a contact sheet.",
        "Read left to right twice looking for one thing: a face that moved.",
        "Alder beside Wren — same height, age only in the face.",
        "Record the answer in design/gates.json as gate A."]),
    17: dict(check=lambda f: check_anchors(f, 1, 11)),
    18: dict(check=lambda f: check_anchors(f, 2, 14)),
    19: dict(check=lambda f: check_anchors(f, 3, 14)),
    20: dict(kind="gate", gate="B", manual=[
        "All 39 anchors on one contact sheet in film order.",
        "Read it twice. Drift caught here costs one image; caught later it costs a clip.",
        "Record the answer in design/gates.json as gate B."]),
    21: dict(kind="manual", manual=[
        "Cut the 39 anchors as stills at their real shot durations, 21:9, 24 fps.",
        "Watch all five minutes without stopping. Read the dialogue aloud over it.",
        "Note every place the eye gets bored — that is a shot that cannot be held."]),
    22: dict(kind="gate", gate="C", manual=[
        "Freeze runtime at 300 s, 23 shots, and the shot order.",
        "Resolve the three duration shortfalls first: S4, S5, S22.",
        "Decide whether S1+S2 are one 30 s generation or two.",
        "Record the answer in design/gates.json as gate C."]),
    23: dict(check=lambda f: check_shots(f, ["S%d" % i for i in range(1, 24)], "concept")),
    24: dict(kind="gate", gate="D", manual=[
        "Watch the cheap pass in order. You are testing seams, not quality.",
        "Any draft frame that beats its anchor gets extracted and promoted.",
        "Record the answer in design/gates.json as gate D."]),
    25: dict(check=lambda f: check_shots(f, ["S1", "S2", "S3", "S4", "S5"], "final")),
    26: dict(check=lambda f: check_shots(f, ["S%d" % i for i in range(6, 15)], "final")),
    27: dict(check=lambda f: check_shots(f, ["S%d" % i for i in range(15, 24)], "final")),
    28: dict(check=lambda f: check_shots(f, ["S%d" % i for i in range(1, 24)], "finished")),
    29: dict(kind="gate", gate="E", manual=[
        "Picture lock. After this nothing is generated again.",
        "Record the answer in design/gates.json as gate E."]),
    30: dict(check=check_rights, manual=[
        "Read the end card: it must credit the novel by its own title.",
        "Open the public post in a logged-out browser and read every visible prompt."]),
    31: dict(kind="manual", manual=[
        "Make the sound anywhere you like — that part is not restricted.",
        "Upload every audio file into the festival project. Files made elsewhere",
        "and never uploaded are the classic disqualification.",
        "S13 stays silent. Confirm its audio is off, not merely quiet."]),
    32: dict(kind="manual", manual=[
        "Apply the watermark in Cinema Studio.",
        "Generate the packshot. This is component 1 of the minimal viable submission."]),
    33: dict(kind="manual", manual=[
        "Post publicly and tag as the rules require — component 2.",
        "Open the post in a logged-out browser. If you cannot see it, neither can a judge.",
        "Social cuts come from S10, S20, S13, S12 or S16 only. Never Movement I."]),
    34: dict(kind="manual", manual=[
        "Verify every generation is still inside the festival project.",
        "Submit with a full day in hand, not on the deadline itself."]),
}

EXTRA = {
    23: check_refs_in_shots,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bible", nargs="?", default="/tmp/bible-data.json")
    ap.add_argument("-o", "--out", default=os.path.join(ROOT, "design/progress.json"))
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    bible = load(a.bible)
    if not bible:
        sys.exit("cannot read %s — run: node design/extract-data.mjs --prompts > %s"
                 % (a.bible, a.bible))
    f = Facts(bible)
    run = bible["RUN"]

    out = []
    for i, step in enumerate(run, 1):
        spec = STEPS.get(i, {})
        kind = spec.get("kind", "auto")
        if kind == "gate":
            state, have, need, ev = check_gate(f, spec["gate"])
        elif kind == "manual":
            state, have, need, ev = ("todo", 0, 1, ["manual step — no file can prove it"])
            g = (f.gates.get("step%d" % i) or {})
            if g.get("done"):
                state, have, ev = "pass", 1, ["recorded %s by %s" % (g.get("on", "?"), g.get("by", "?"))]
        else:
            state, have, need, ev = spec["check"](f)
        if i in EXTRA:
            s2, h2, n2, e2 = EXTRA[i](f)
            ev = e2 + ev
            if s2 != "pass" and state == "pass":
                state = "partial"
        out.append(dict(
            n=i, title=clean(step.get("t", "")), phase=step.get("ph"),
            where=clean(str(step.get("w", ""))), kind=kind, state=state,
            have=have, need=need, evidence=ev, manual=spec.get("manual", [])))

    counts = {}
    for s in out:
        counts[s["state"]] = counts.get(s["state"], 0) + 1
    weighted = sum(1.0 if s["state"] == "pass" else
                   (s["have"] / s["need"] if s["need"] and s["state"] == "partial" else 0.0)
                   for s in out)
    now = datetime.datetime.now(datetime.timezone.utc)
    doc = dict(
        generated=now.strftime("%Y-%m-%dT%H:%MZ"),
        deadline=DEADLINE.strftime("%Y-%m-%dT%H:%MZ"),
        days_left=round((DEADLINE - now).total_seconds() / 86400, 1),
        snapshot_present=bool(f.snapshot),
        crosswalk_present=os.path.exists(os.path.join(ROOT, "crosswalk.local.js")),
        rollup=dict(total=len(out), done=counts.get("pass", 0),
                    partial=counts.get("partial", 0), todo=counts.get("todo", 0),
                    blocked=counts.get("blocked", 0),
                    pct=round(100.0 * weighted / len(out), 1)),
        steps=out)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1)
        fh.write("\n")

    if not a.quiet:
        mark = {"pass": "done", "partial": "part", "todo": "TODO", "blocked": "????"}
        for s in out:
            frac = "%d/%d" % (s["have"], s["need"]) if s["need"] > 1 else ""
            print("%2d %-4s %-6s %-58s %s" % (
                s["n"], mark[s["state"]], frac, s["title"][:58],
                s["evidence"][0][:60] if s["evidence"] else ""))
        r = doc["rollup"]
        print("\n%s of 34 done, %s partial, %s todo, %s unverifiable here — %s%% weighted"
              % (r["done"], r["partial"], r["todo"], r["blocked"], r["pct"]))
        print("%s days to the deadline" % doc["days_left"])


if __name__ == "__main__":
    main()
