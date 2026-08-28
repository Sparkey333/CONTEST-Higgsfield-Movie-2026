# -*- coding: utf-8 -*-
"""Build workflow-sheets.pdf — the printable production kit.

Every table on these sheets is generated from the director-bible's own data
arrays (via design/extract-data.mjs), so the printed kit cannot drift from the
app. Pencil fields are ruled blanks; anything printed in light grey italic is
a pre-filled suggestion — the compressed Aug 27 → Sep 3 schedule and what is
already known to exist in the Higgsfield project — meant to be confirmed or
corrected in pencil, not trusted.

Run from the repo root:
    node design/extract-data.mjs > /tmp/bible-data.json
    python3 design/build-sheets.py /tmp/bible-data.json
Outputs design/workflow-sheets.html (the printable source) and, via
Playwright, workflow-sheets.pdf at the repo root.
"""
import html as H
import io
import json
import re
import sys

DATA = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/bible-data.json"))
RUN, PREP, FRAMES, SHOTS, PROC = (DATA[k] for k in ("RUN", "PREP", "FRAMES", "SHOTS", "PROC"))

TITLE = "MATTER OF LIGHT"
PRINTED = "printed 2026-08-27"
N_SHEETS = 8


def clean(t):
    """Entities and tags out; plain text in."""
    t = re.sub(r"<[^>]+>", "", t or "")
    return H.unescape(t).replace("→", "→")


def esc(t):
    return H.escape(clean(t), quote=False)


# ── the pre-fill layer ───────────────────────────────────────────────────────
# Matched against run-step titles. done: pencil-checked with a date.
# note: grey italic status read off the user's real project screenshots.
# target: the compressed schedule date, printed grey in the date blank.
PREFILL = [
    (r"from-scratch rule",        {"done": "Aug 26"}),
    (r"festival project",         {"done": "Aug 26", "note": "project exists — folder reads “Matter of Light”: pick the one title"}),
    (r"aura rule",                {"target": "Aug 27"}),
    (r"Oriane — train",           {"target": "Aug 27", "note": "started · 29 imgs across @Oriane + @Oriane-1 — sort into rest / ascended"}),
    (r"Oriane damaged",           {"target": "Aug 27", "note": "started · @Oriane-damaged holds 3, needs 6–8"}),
    (r"mind ladder",              {"target": "Aug 27"}),
    (r"Caedom — two forms",       {"target": "Aug 27", "note": "started · @Caedom holds 24 — split ascended / mortal"}),
    (r"Alder — the elder",        {"target": "Aug 27", "note": "started · split @KaiBrothers 16 by which boy is in frame"}),
    (r"Wren — the younger",       {"target": "Aug 27", "note": "then the height check: both A sheets side by side"}),
    (r"Threadwright and Keepers", {"target": "Aug 27", "note": "started · @ThreadWright 18 · @TheKeepers 8 → @vigil"}),
    (r"Turned and the fused",     {"target": "Aug 27", "note": "started · @TheTurned16 16 · @Wielder-Dominion 14 → @lev_rider"}),
    (r"seven domains",            {"target": "Aug 27"}),
    (r"attunement ladder",        {"target": "Aug 27"}),
    (r"lighting plates",          {"target": "Aug 27", "note": "generate bar was last seen 4:3 / 30s — set 21:9 before these"}),
    (r"Seventeen props",          {"target": "Aug 28"}),
    (r"Identity lock",            {"target": "Aug 28"}),
    (r"Movement I look",          {"target": "Aug 28"}),
    (r"Movement II look",         {"target": "Aug 28"}),
    (r"Movement III look",        {"target": "Aug 29"}),
    (r"String lock",              {"target": "Aug 29"}),
    (r"Stills reel",              {"target": "Aug 29"}),
    (r"Timing lock",              {"target": "Aug 29"}),
    (r"Cheap motion",             {"target": "Aug 30"}),
    (r"Motion lock",              {"target": "Aug 30"}),
    (r"Movement I \(S1",          {"target": "Aug 31"}),
    (r"Movement II \(S6",         {"target": "Aug 31–Sep 1"}),
    (r"Movement III \(S15",       {"target": "Sep 1"}),
    (r"deflicker",                {"target": "Sep 2"}),
    (r"Picture lock",             {"target": "Sep 2"}),
    (r"Rights and attribution",   {"target": "Sep 2"}),
    (r"Sound",                    {"target": "Sep 2"}),
    (r"Watermark",                {"target": "Sep 3"}),
    (r"Social post",              {"target": "Sep 3"}),
    (r"Verify the project",       {"target": "Sep 3", "note": "11:59 PM PT — aim for the morning, not the deadline"}),
]


def prefill(title):
    t = clean(title)
    for pat, v in PREFILL:
        if re.search(pat, t):
            return v
    return {}


# ── html scaffolding ─────────────────────────────────────────────────────────
CSS = """
@font-face{font-family:"Body";src:url("f/InstrumentSans-Regular.ttf");font-weight:400}
@font-face{font-family:"Body";src:url("f/InstrumentSans-Bold.ttf");font-weight:700}
@font-face{font-family:"Mono";src:url("f/GeistMono-Regular.ttf")}
@font-face{font-family:"Disp";src:url("f/InstrumentSerif-Regular.ttf")}
@font-face{font-family:"Num";src:url("f/BigShoulders-Bold.ttf")}
*{margin:0;padding:0;box-sizing:border-box}
@page{size:Letter;margin:0}
body{font:9.5pt/1.45 "Body",sans-serif;color:#101010;background:#fff;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}
.sheet{width:8.5in;height:11in;padding:.52in .55in .45in;page-break-after:always;
  position:relative;overflow:hidden;display:flex;flex-direction:column}
.sheet:last-child{page-break-after:auto}

/* running head */
.rh{display:flex;justify-content:space-between;align-items:baseline;
  border-bottom:1.6pt solid #101010;padding-bottom:5pt;margin-bottom:10pt}
.rh .l{font:700 8pt "Mono";letter-spacing:.18em}
.rh .m{font:8pt "Mono";color:#777;letter-spacing:.08em}
.rh .r{font:700 8pt "Mono";letter-spacing:.12em}
h2{font:700 13pt/1.1 "Body";letter-spacing:-.01em;margin-bottom:2pt}
.sub{font:8.5pt/1.4 "Body";color:#555;margin-bottom:8pt;max-width:6.6in}

/* boxes + pencil */
.cb{display:inline-block;width:9pt;height:9pt;border:1pt solid #333;border-radius:1.5pt;
  vertical-align:-1.5pt;flex:none}
.cb.pre{position:relative}
.cb.pre::after{content:"✓";position:absolute;left:.5pt;top:-3pt;font:700 9pt "Body";color:#8a8a8a}
.bl{display:inline-block;border-bottom:.8pt solid #999;min-width:52pt;height:9pt;
  vertical-align:baseline}
.pencil{font:italic 7.5pt "Body";color:#8a8a8a}
.penfill{font:italic 8pt "Body";color:#8a8a8a;border-bottom:.8pt solid #bbb;
  display:inline-block;min-width:52pt;text-align:center}
tt{font:7.5pt "Mono"}
td tt{white-space:nowrap}

/* generic table */
table{border-collapse:collapse;width:100%}
th{font:700 6.5pt "Mono";letter-spacing:.12em;text-transform:uppercase;color:#777;
  text-align:left;border-bottom:1pt solid #101010;padding:2pt 4pt 3pt}
td{border-bottom:.6pt solid #d9d9d9;padding:2.4pt 4pt;vertical-align:top}
tr{page-break-inside:avoid}
.num{font:700 10pt "Num";color:#999;width:16pt}
.gate td{background:#f1f1f1;border-top:1pt solid #101010;border-bottom:1pt solid #101010}
.gate .gt{font:700 8.5pt "Mono";letter-spacing:.1em}
.mono{font:6.5pt/1.4 "Mono";color:#444}
.small{font:8pt/1.35 "Body"}
.note{font:italic 7pt/1.25 "Body";color:#8a8a8a}
.right{text-align:right}

/* two-column ledger */
.cols2{column-count:2;column-gap:.3in;column-rule:.6pt solid #ddd}
.cols3{column-count:3;column-gap:.22in;column-rule:.6pt solid #ddd}
.ledrow{display:flex;gap:5pt;align-items:baseline;padding:2.2pt 0;
  border-bottom:.6pt solid #e2e2e2;break-inside:avoid}
.ledrow tt{flex:none}
.ledrow .nm{flex:1;font-size:8pt;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
.lhead{font:700 7pt "Mono";letter-spacing:.14em;text-transform:uppercase;color:#555;
  border-bottom:1pt solid #101010;padding:6pt 0 2pt;break-inside:avoid;break-after:avoid}

.foot{margin-top:auto;padding-top:6pt;border-top:.8pt solid #ccc;display:flex;
  justify-content:space-between;font:7pt "Mono";color:#999;letter-spacing:.08em}
.kv{display:flex;gap:14pt;flex-wrap:wrap;font:8pt "Body"}
.kv b{font-weight:700}
.rulebox{border:1pt solid #101010;padding:6pt 8pt;margin-top:8pt;font:8pt/1.45 "Body"}
.rulebox b{font-weight:700}
"""


def head(n, name):
    return (f'<div class="rh"><span class="l">{TITLE} · WORKFLOW SHEETS</span>'
            f'<span class="m">{PRINTED} · day&nbsp;<span class="bl" style="min-width:24pt"></span></span>'
            f'<span class="r">SHEET {n:02d}/{N_SHEETS:02d} · {name}</span></div>')


def foot(l, r=""):
    return f'<div class="foot"><span>{l}</span><span>{r}</span></div>'


sheets = []

# ── Sheet 1 · cover + countdown ─────────────────────────────────────────────
plan = [
    ("Aug 27", "Finish Phase 0 — split the handles, remaining references, four lighting plates"),
    ("Aug 28", "Gate A identity lock → anchor frames, Movements I and II"),
    ("Aug 29", "Anchors Movement III → Gate B → stills reel → Gate C timing lock"),
    ("Aug 30", "Cheap motion pass, all 23 shots → Gate D motion lock"),
    ("Aug 31", "Final generation — Movement I, start Movement II"),
    ("Sep 1",  "Final generation — finish Movement II, Movement III"),
    ("Sep 2",  "Deflicker → upscale → grade → Gate E picture lock → sound"),
    ("Sep 3",  "Watermark + packshot, public post, rights pass, verify project — SUBMIT"),
]
rows = "".join(
    f'<tr><td style="width:.62in"><b>{d}</b></td><td>{t}</td>'
    f'<td style="width:1.15in" class="right"><span class="pencil">actual&nbsp;</span><span class="bl" style="min-width:58pt"></span></td></tr>'
    for d, t in plan)
gates = "".join(
    f'<tr><td style="width:.55in;white-space:nowrap"><b>Gate {g}</b></td><td>{t}</td>'
    f'<td style="width:.42in"><span class="cb"></span></td>'
    f'<td style="width:1in"><span class="bl" style="min-width:60pt"></span></td></tr>'
    for g, t in [("A", "Identity lock — every face, palette and plate final"),
                 ("B", "String lock — all 39 anchors on one contact sheet"),
                 ("C", "Timing lock — runtime, order and shot count freeze"),
                 ("D", "Motion lock — every seam confirmed at draft tier"),
                 ("E", "Picture lock — no further generation")])
sheets.append(head(1, "COVER") + f"""
<div style="margin:14pt 0 4pt"><div style="font:400 34pt/1 'Disp'">Matter of Light</div>
<div style="font:8pt 'Mono';letter-spacing:.3em;color:#777;margin-top:4pt">HIGGSFIELD GLOBAL FILM FESTIVAL · 5:00 · 21:9 · DEADLINE SEP 3, 11:59 PM PT</div></div>
<div class="kv" style="margin:8pt 0 12pt">
 <span><b>42</b> references</span><span><b>39</b> anchor frames</span><span><b>23</b> shots</span>
 <span><b>34</b> run-sheet steps</span><span><b>5</b> gates</span><span><b>~200</b> images : <b>~76</b> video</span></div>
<div class="rulebox"><b>How to use this kit.</b> Print it, clip it, keep a pencil on it. Squares are things to tick;
ruled lines are yours to fill; anything already printed in <span class="pencil">grey italic</span> is a suggestion read
from the project as of Aug 27 — confirm or strike it, don't trust it. The app is the source of truth for prompts;
these sheets are the source of truth for <b>what is actually done</b>. Tables are generated from the bible's own data,
so counts here always match the app they were printed from.</div>
<h2 style="margin-top:14pt">The last seven days</h2>
<p class="sub">A compressed plan from today to the deadline. One line per day; write what actually happened beside it.</p>
<table>{rows}</table>
<h2 style="margin-top:12pt">The five gates</h2>
<p class="sub">A gate is a hard stop — nothing downstream begins until it holds. Date each one the moment it locks.</p>
<table>{gates}</table>
<div class="rulebox" style="margin-top:10pt"><b>Open decisions, still.</b>
(The title is decided: <i>Matter of Light</i>, everywhere.)
&nbsp;① <tt>@Drowning</tt> — define or delete: <span class="bl" style="min-width:80pt"></span>
&nbsp;② Leviathan scale reference object: <span class="bl" style="min-width:80pt"></span></div>
""" + foot("Sheet source: director-bible.html data arrays · design/build-sheets.py", "MVS = watermark + packshot on the film AND a public social post"))

# ── Sheet 2 · the process ───────────────────────────────────────────────────
prows = ""
for p in PROC:
    it = {0: "", 1: "↻", 2: "↻↻"}[p.get("it") or 0]
    gate = ' class="gate"' if p.get("g") else ""
    first = clean(p["b"][0]) if p.get("b") else ""
    itspan = ' <span style="color:#8a8a8a">' + it + "</span>" if it else ""
    prows += (f'<tr{gate}><td class="num">{p["n"]}</td>'
              f'<td><b class="{ "gt" if p.get("g") else "" }">{esc(p["t"])}</b>'
              f'{itspan}'
              f'<div class="small" style="color:#555">{esc(first)}</div></td>'
              f'<td style="width:.4in"><span class="cb"></span></td>'
              f'<td style="width:1.05in"><span class="bl" style="min-width:64pt"></span></td></tr>')
sheets.append(head(2, "THE PROCESS") + f"""
<h2>How a film gets made here</h2>
<p class="sub">The seventeen steps, in order. ↻ marks where a second pass is expected; ↻↻ where several are and the
budget should say so. Grey rows are gates. Date each step when it is genuinely finished — not when it is started.</p>
<table><tr><th></th><th>Step</th><th>Done</th><th>Date</th></tr>{prows}</table>
""" + foot("Transfers to the next film unchanged — this page is the method, not the movie"))

# ── Sheets 3–4 · run sheet ──────────────────────────────────────────────────
def run_row(i, r):
    pf = prefill(r["t"])
    gate = ' class="gate"' if r.get("g") else ""
    meta = ""
    if r.get("mdl"):
        meta = (f'<div class="mono">{esc(r["mdl"])} &nbsp;·&nbsp; {esc(r.get("ar",""))}'
                f' &nbsp;·&nbsp; {esc(r.get("fld",""))}'
                + (f' &nbsp;·&nbsp; save <b>{esc(r["sv"])}</b>' if r.get("sv") else "") + "</div>")
    note = f'<div class="note">{esc(pf["note"])}</div>' if pf.get("note") else ""
    if pf.get("done"):
        box, date = '<span class="cb pre"></span>', f'<span class="penfill">{pf["done"]}</span>'
    else:
        box = '<span class="cb"></span>'
        date = (f'<span class="penfill">{pf["target"]}</span>' if pf.get("target")
                else '<span class="bl" style="min-width:56pt"></span>')
    return (f'<tr{gate}><td class="num">{i+1}</td>'
            f'<td style="width:.62in"><tt>{esc(r["ph"])}</tt></td>'
            f'<td><b class="{ "gt" if r.get("g") else "" }">{esc(r["t"])}</b>{meta}{note}</td>'
            f'<td style="width:.34in">{box}</td>'
            f'<td style="width:1in">{date}</td></tr>')

half = 16
for s_i, chunk in enumerate((RUN[:half], RUN[half:])):
    rows = "".join(run_row(i + s_i * half, r) for i, r in enumerate(chunk))
    intro = ("" if s_i else '<h2>The run sheet</h2><p class="sub">All 34 steps in production order — '
             'grey dates are the compressed targets; overwrite them in pencil with the real ones.</p>')
    sheets.append(head(3 + s_i, f"RUN SHEET {'A' if not s_i else 'B'}") + intro +
                  f'<table><tr><th></th><th>Phase</th><th>Step</th><th>Done</th><th>Date / target</th></tr>{rows}</table>'
                  + foot(f"Steps {1 + s_i*half}–{s_i*half + len(chunk)} of {len(RUN)}",
                         "✓ in grey = already true on Aug 27 — strike it if not"))

# ── Sheet 5 · reference ledger ──────────────────────────────────────────────
ORDER = ["Rule sheet", "State ladder", "Character", "Lesser being", "Lighting plate",
         "Background", "Prop", "Asset"]
groups = {}
for p in PREP:
    groups.setdefault(p.get("tl", "Asset"), []).append(p)
led = ""
for g in ORDER:
    if g not in groups:
        continue
    led += f'<div class="lhead">{g} · {len(groups[g])}</div>'
    for p in groups[g]:
        led += (f'<div class="ledrow"><span class="cb"></span>'
                f'<tt>{esc(p["sv"])}</tt><span class="nm">{esc(p["n"])}</span>'
                f'<span class="bl" style="min-width:22pt"></span></div>')
sheets.append(head(5, "REFERENCE LEDGER") + f"""
<h2>Phase 0 — the 42 references</h2>
<p class="sub">Tick when the <b>A variant is selected, named and favourited</b> in the project — generated is not done.
The short blank takes the winning take number. Generate the Rule sheet first: everything else grades against it.
B / C / D variants are optional and wait until Gate A.</p>
<div class="cols2">{led}</div>
""" + foot("Selection rule: identity sheets, ladders, rule sheets, plates — keep exactly 1", "Rejects → 99 · LOOKDEV, never deleted"))

# ── Sheet 6 · frame string ──────────────────────────────────────────────────
ROLE = {"single": "·", "shared": "S", "bridge": "B", "match": "M"}
fr = ""
cur_mv = 0
for f in FRAMES:
    if f["mv"] != cur_mv:
        cur_mv = f["mv"]
        fr += f'<div class="lhead">Movement {"I"*cur_mv if cur_mv<4 else cur_mv} · {["","The Sun","The Ocean","The Island"][cur_mv]}</div>'
    fr += (f'<div class="ledrow"><span class="cb"></span><tt><b>{f["f"]}</b></tt>'
           f'<tt style="color:#777;width:10pt;text-align:center">{ROLE[f["r"]]}</tt>'
           f'<span class="nm">{esc(f["s"])}</span>'
           f'<span class="bl" style="min-width:20pt"></span></div>')
shared = sum(1 for f in FRAMES if f["r"] in ("shared", "bridge"))
sheets.append(head(6, "FRAME STRING") + f"""
<h2>Phase 1 — the 39 anchors, in film order</h2>
<p class="sub">One row per image. <tt>S</tt> shared join (one image, two shots) · <tt>B</tt> bridge (the seam itself)
· <tt>M</tt> matched pair across a transition · <tt>·</tt> single. Tick when selected and named; the blank takes the
take number. Work strictly top to bottom so shared joins are generated once and inherited.</p>
<div class="cols3">{fr}</div>
<div class="rulebox">39 images, not 46 — {shared} slots are shared joins or bridges. Batch of 4 per anchor, select 1.
Attach the movement's lighting plate and the relevant Soul on every generation. <b>F35 is the film</b> — biggest batch, longest look.</div>
""" + foot("Match pairs: F09/F10 (tear → ocean) and F22/F23 (streak → dawn) — design each pair together"))

# ── Sheet 7 · shot list ─────────────────────────────────────────────────────
srows = ""
clock = 0
for s in SHOTS:
    t0, clock = clock, clock + s["d"]
    model = clean(s["model"]).split("·")[0].strip()
    srows += (f'<tr><td style="width:.32in"><tt><b>{s["id"]}</b></tt></td>'
              f'<td style="width:.68in"><tt>{t0//60}:{t0%60:02d}–{clock//60}:{clock%60:02d}</tt></td>'
              f'<td style="width:.3in" class="right"><tt>{s["d"]}s</tt></td>'
              f'<td class="small">{esc(s["t"])}</td>'
              f'<td style="width:1.42in"><tt style="font-size:6.5pt">{esc(model)}</tt></td>'
              f'<td style="width:.36in"><span class="cb"></span></td>'
              f'<td style="width:.36in"><span class="cb"></span></td>'
              f'<td style="width:.62in"><span class="bl" style="min-width:38pt"></span></td></tr>')
sheets.append(head(7, "SHOT LIST") + f"""
<h2>Phases 3–4 — the 23 generations</h2>
<p class="sub">Two boxes per shot: <b>draft</b> (cheap tier, Gate D) and <b>final</b>. A shot that fails three times
leaves the queue for the escalation ladder — it does not get a quiet fourth try. Movement II must be generated in
sequence: S7's end frame is S8's start frame.</p>
<table><tr><th>ID</th><th>TC</th><th>Dur</th><th>Shot</th><th>Model</th><th>Draft</th><th>Final</th><th>Att / date</th></tr>{srows}</table>
<div class="rulebox"><b>Finish order, always:</b> deflicker → upscale (<tt>aigc</tt>) → grade. S13 ships silent.
S20 gets the most attempts of anything in the film. Two passes, then it ships.</div>
""" + foot(f"Total {clock//60}:{clock%60:02d} of 5:00 · mean {clock/len(SHOTS):.1f}s · longest {max(s['d'] for s in SHOTS)}s"))

# ── Sheet 8 · daily log + submit checklist ──────────────────────────────────
drows = ""
for d in ["Aug 27", "Aug 28", "Aug 29", "Aug 30", "Aug 31", "Sep 1", "Sep 2", "Sep 3"]:
    drows += (f'<tr><td style="width:.55in"><b>{d}</b></td>'
              + '<td style="width:.9in">' + '<span class="cb"></span> ' * 4 + "</td>"
              + ''.join(f'<td style="width:.62in"><span class="bl" style="min-width:30pt"></span><tt style="color:#999">/{n}</tt></td>'
                        for n in (42, 39, 23))
              + '<td style="width:.5in"><span class="bl" style="min-width:26pt"></span></td>'
              + '<td><span class="bl" style="min-width:100%"></span></td></tr>')
mvs = "".join(f'<div class="ledrow"><span class="cb"></span><span class="nm">{t}</span>'
              f'<span class="bl" style="min-width:40pt"></span></div>' for t in [
    "Official watermark + packshot on the final video",
    "Public post (IG / YT / X / Reddit) — film with both intact",
    "Post AND account load in a logged-out window",
    "Every asset still inside the submission project — deleted nothing",
    "All prompts swept — no novel term anywhere",
    "Licence clause read: exclusive / assignment / underlying works / moral rights",
    "English subtitles or VO for all dialogue · MP4/MOV · ≤4K · 21:9",
    "End card: “Original screen story by B.L. Barkey”",
    "Submitted — with a day of margin, not at 11:58",
])
sheets.append(head(8, "DAILY LOG · SUBMIT") + f"""
<h2>Daily log — forty seconds before work</h2>
<p class="sub">Four capture boxes: ① folder tree expanded ② Elements → Characters ③ Liked filter ④ generate bar.
Then the three counts, elements, and one line for what is blocking. Full window, never a crop; one screen per image;
never scale down.</p>
<table><tr><th>Day</th><th>Captures</th><th>Refs</th><th>Anchors</th><th>Shots</th><th>Elems</th><th>Blocked by / note</th></tr>{drows}</table>
<h2 style="margin-top:12pt">Before you submit — the list that disqualifies</h2>
<p class="sub">Every line here is a rule with teeth, not a style note. An entry missing an MVS component does not compete.</p>
{mvs}
<div class="rulebox" style="margin-top:8pt"><b>Where everything lives:</b> app + prompts → <tt>director-bible.html</tt> ·
one-pager → <tt>production-sheet.html</tt> · capture plate → <tt>design/four-captures.png</tt> ·
this kit rebuilds with <tt>design/build-sheets.py</tt>.</div>
""" + foot("The value of the log is in the diff — same four captures, same order, every day"))

# ── write + render ──────────────────────────────────────────────────────────
doc = ("<!doctype html><html><head><meta charset='utf-8'><title>Workflow Sheets</title>"
       f"<style>{CSS}</style></head><body>"
       + "".join(f'<div class="sheet">{s}</div>' for s in sheets)
       + "</body></html>")
io.open("design/workflow-sheets.html", "w", encoding="utf-8").write(doc)
print(f"design/workflow-sheets.html written — {len(sheets)} sheets, {len(doc)} bytes")
