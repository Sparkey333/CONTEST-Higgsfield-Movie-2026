# -*- coding: utf-8 -*-
"""Build the paper kit — twelve separate printable sheets for thinking on paper.

The workflow sheets (build-sheets.py) TRACK the production; these sheets THINK
it. Every one is a pencil surface: thumbnail boxes, pacing grids, review
checklists — in the same order as the director-bible's run sheet, so sheet N
is always the paper twin of the step you are standing on in the app.

The storyboard sheets come in four formats because pacing has two honest
questions and each needs its own geometry:
  · equal frames (6-up, 12-up)  — composition, one drawing per idea
  · equal TIME   (pulse, 12s)   — what is on screen at every fixed tick
  · weighted TIME (ribbon)      — box width = shot length; draw inside the
                                  time you actually have

Run from the repo root:
    node design/extract-data.mjs > /tmp/bible-data.json
    python3 design/build-paper-kit.py /tmp/bible-data.json
    node design/render-paper-kit.mjs
Outputs design/paper-kit.html, then the render script writes paper-kit.pdf
(combined, repo root) and paper-kit/NN-*.pdf (one file per sheet).
"""
import html as H
import io
import json
import os
import re
import sys

DATA = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/bible-data.json"))
RUN, PREP, FRAMES, SHOTS, PROC = (DATA[k] for k in ("RUN", "PREP", "FRAMES", "SHOTS", "PROC"))
for s in SHOTS:
    s["d"] = int(s["d"]); s["mv"] = int(s["mv"])

TITLE = "MATTER OF LIGHT"
PRINTED = "printed 2026-08-29"
TOTAL = sum(s["d"] for s in SHOTS)


def clean(t):
    t = re.sub(r"<[^>]+>", "", t or "")
    return H.unescape(t)


def esc(t):
    return H.escape(clean(t), quote=False)


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
.rh{display:flex;justify-content:space-between;align-items:baseline;
  border-bottom:1.6pt solid #101010;padding-bottom:5pt;margin-bottom:10pt}
.rh .l{font:700 8pt "Mono";letter-spacing:.18em}
.rh .m{font:8pt "Mono";color:#777;letter-spacing:.08em}
.rh .r{font:700 8pt "Mono";letter-spacing:.12em}
h2{font:700 13pt/1.1 "Body";letter-spacing:-.01em;margin-bottom:2pt}
h3{font:700 10pt/1.2 "Body";margin:8pt 0 3pt}
.sub{font:8.5pt/1.4 "Body";color:#555;margin-bottom:8pt;max-width:6.9in}
.cb{display:inline-block;width:9pt;height:9pt;border:1pt solid #333;border-radius:1.5pt;
  vertical-align:-1.5pt;flex:none}
.bl{display:inline-block;border-bottom:.8pt solid #999;min-width:52pt;height:9pt;
  vertical-align:baseline}
.pencil{font:italic 7.5pt "Body";color:#8a8a8a}
tt{font:7.5pt "Mono"}
table{border-collapse:collapse;width:100%}
th{font:700 6.5pt "Mono";letter-spacing:.12em;text-transform:uppercase;color:#777;
  text-align:left;border-bottom:1pt solid #101010;padding:2pt 4pt 3pt}
td{border-bottom:.6pt solid #d9d9d9;padding:2.4pt 4pt;vertical-align:top}
tr{page-break-inside:avoid}
.mono{font:6.5pt/1.4 "Mono";color:#444}
.small{font:8pt/1.35 "Body"}
.note{font:italic 7pt/1.25 "Body";color:#8a8a8a}
.right{text-align:right}
.cols2{column-count:2;column-gap:.3in;column-rule:.6pt solid #ddd}
.ledrow{display:flex;gap:5pt;align-items:baseline;padding:2.2pt 0;
  border-bottom:.6pt solid #e2e2e2;break-inside:avoid}
.ledrow .nm{flex:1;font-size:8pt;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
.lhead{font:700 7pt "Mono";letter-spacing:.14em;text-transform:uppercase;color:#555;
  border-bottom:1pt solid #101010;padding:6pt 0 2pt;break-inside:avoid;break-after:avoid}
.foot{margin-top:auto;padding-top:6pt;border-top:.8pt solid #ccc;display:flex;
  justify-content:space-between;font:7pt "Mono";color:#999;letter-spacing:.08em}
.rulebox{border:1pt solid #101010;padding:6pt 8pt;margin-top:8pt;font:8pt/1.45 "Body"}
.rulebox b{font-weight:700}

/* sketch surfaces */
.fr{border:1pt solid #333;border-radius:1.5pt;background:#fff;position:relative}
.fr.lite{border:.7pt solid #888}
.frl{font:6.5pt "Mono";color:#999;letter-spacing:.06em}
.grid6{display:grid;grid-template-columns:1fr 1fr;gap:10pt 14pt}
.grid6 .fr{height:1.52in}
.grid12{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8pt 10pt}
.grid12 .fr{height:.99in}
.pulse{display:grid;grid-template-columns:repeat(5,1fr);gap:11pt 10pt}
.pulse .fr{height:.92in}
.ribbon{display:flex;flex-wrap:wrap;gap:6pt 3pt;align-items:flex-start}
.ribbon .cell{display:flex;flex-direction:column;gap:1pt}
.ribbon .fr{height:.80in}
.ribbon .m1{border-top:3pt solid #101010}
.ribbon .m2{border-top:5pt double #101010}
.ribbon .m3{border-top:2.5pt dotted #101010}
.anch{display:grid;grid-template-columns:repeat(4,1fr);gap:5pt 8pt}
.anch .fr{height:.58in}
.anch .frl{font-size:6pt}
.anch .shared .fr{border-style:dashed}
.anch .bridge .fr{background:#e9e9e9}
.lines{border-bottom:.7pt solid #bbb;height:11pt}
.mth{border:1pt solid #101010;padding:7pt 9pt;margin-top:7pt;page-break-inside:avoid}
.mth h3{margin:0 0 2pt}
.mth .tag{font:700 6.5pt "Mono";letter-spacing:.16em;color:#fff;background:#101010;
  padding:1.5pt 5pt;border-radius:2pt;vertical-align:2pt;margin-right:5pt}
.mth ol{margin:3pt 0 0 14pt;font:8pt/1.5 "Body"}
.mth .q{font:italic 7.5pt/1.35 "Body";color:#555;margin-top:3pt}
"""

SHEET_DEFS = []  # (slug, name) in order — the render script reads this list


def head(n, name):
    return (f'<div class="rh"><span class="l">{TITLE} · PAPER KIT</span>'
            f'<span class="m">{PRINTED} · day&nbsp;<span class="bl" style="min-width:24pt"></span></span>'
            f'<span class="r">SHEET {n:02d}/12 · {name}</span></div>')


def foot(l, r=""):
    return f'<div class="foot"><span>{l}</span><span>{r}</span></div>'


sheets = []


def add(slug, rhname, body, footline, footr=""):
    n = len(sheets) + 1
    SHEET_DEFS.append((slug, rhname))
    sheets.append((slug, head(n, rhname) + body + foot(footline, footr)))


# ── P01 · cover — how the paper loop works ──────────────────────────────────
contents = [
    ("02", "Phase 0 ledger", "RUN steps 1–14 — the 42 references, in generation order"),
    ("03", "Gate A review", "RUN step 15 — identity lock, on paper before you call it"),
    ("04", "Anchor string", "Phase 1 — thumbnail all 39 anchors before generating one"),
    ("05", "Storyboard 6-up", "equal frames, large — one drawing per idea"),
    ("06", "Storyboard 12-up", "equal frames, small — alternates and coverage"),
    ("07", "Pulse · 12s ticks", "equal TIME — 25 frames, one every 12 seconds"),
    ("08", "Ribbon · weighted", "box width = shot length — draw inside the time you have"),
    ("09", "Gates B + C", "contact-sheet drift hunt, then the timing lock"),
    ("10", "Shot cards", "Phases 3–4 — draft and final passes, 23 shots"),
    ("11", "Methods", "what wins now, and the two methods this production adds"),
    ("12", "Finish + submit", "Phases 6–7 — the order that cannot be reversed, and the MVS"),
]
crow = "".join(
    f'<tr><td style="width:.4in"><b class="mono" style="font-size:8pt">{n}</b></td>'
    f'<td style="width:1.55in"><b>{t}</b></td><td class="small">{d}</td></tr>'
    for n, t, d in contents)
add("cover", "COVER", f"""
<div style="margin:12pt 0 4pt"><div style="font:400 32pt/1 'Disp'">Matter of Light</div>
<div style="font:8pt 'Mono';letter-spacing:.3em;color:#777;margin-top:4pt">THE PAPER KIT · TWELVE SHEETS FOR THINKING, NOT TRACKING</div></div>
<p class="sub" style="margin-top:8pt">The workflow sheets record what happened; these decide what should. Structure is
cheapest on paper — a re-ordered movement costs an eraser here and forty generations after Gate&nbsp;C. Each sheet is the
paper twin of a bible step, in the same order the run sheet walks.</p>
<h3>The loop</h3>
<table style="margin-bottom:4pt">
<tr><td style="width:.35in"><b class="mono" style="font-size:9pt">1</b></td><td><b>Print</b> the sheet for the step you are on. Letter, portrait, black and white is fine.</td></tr>
<tr><td><b class="mono" style="font-size:9pt">2</b></td><td><b>Pencil.</b> Thumbnail, strike out, re-order, argue in the margin. Nothing here costs a credit.</td></tr>
<tr><td><b class="mono" style="font-size:9pt">3</b></td><td><b>Photograph</b> the marked sheet — the bible's <b>Paper</b> panel has a notes camera that keeps the
photo with the step, or drop the picture straight into the Claude session.</td></tr>
<tr><td><b class="mono" style="font-size:9pt">4</b></td><td><b>Iterate.</b> The session reads the marks, revises the prompts and the sheets, and you reprint.
Each round of photo → revision is logged with the step, so the loop gets sharper as the pile grows.</td></tr>
</table>
<h3>What is in the kit</h3>
<table>{crow}</table>
<div class="rulebox"><b>One rule:</b> nothing on paper is canon until it is carried back into the bible. The sheet
proposes; the app decides; the printed kit is regenerated from the app's own data so the two can never drift.</div>
""", "print single-sided · pencil, not pen · the eraser is the point")

# ── P02 · Phase 0 ledger ────────────────────────────────────────────────────
order = ["Rule sheet", "Character", "State ladder", "Lesser being", "Lighting plate", "Background", "Prop", "Effect"]
by = {}
for p in PREP:
    by.setdefault(p["tl"], []).append(p)
led = ""
for tl in order:
    if tl not in by:
        continue
    led += f'<div class="lhead">{esc(tl)} · {len(by[tl])}</div>'
    for p in by[tl]:
        led += (f'<div class="ledrow"><span class="cb"></span>'
                f'<tt>{esc(p["sv"])}</tt><span class="nm">{esc(p["n"])}</span>'
                f'<span class="pencil">batch</span><span class="bl" style="min-width:20pt"></span></div>')
add("phase0-ledger", "PHASE 0 LEDGER", f"""
<h2>Phase 0 — the 42 references, in generation order</h2>
<p class="sub">Tick when the A variant is locked; B/C/D wait for Gate A. Batch of 4, select 1. The aura rule sheet is
first on purpose — it needs no identity and everything else grades against it.</p>
<div class="cols2">{led}</div>
""", f"{len(PREP)} assets · A variants required · B/C/D after Gate A", "one identity per Soul, never two")

# ── P03 · Gate A review ─────────────────────────────────────────────────────
idents = [
    ("ORIANE", "brows squared at the inner edge · pale blue-grey eyes · crystal is aura over cloth, never skin"),
    ("CAEDOM", "same bone structure in both forms · white light irises, no beam · never brightens"),
    ("ALDER — nineteen", "blonde, longer face, watchful · mouth closed · same height as his brother"),
    ("WREN — eighteen", "brunette, rounder face, mid-speech · same height — age reads in features, never stature"),
]
irow = ""
for n, must in idents:
    irow += (f'<tr><td style="width:1.35in"><b>{n}</b></td><td class="small">{must}</td>'
             f'<td style="width:1.7in"><div class="lines"></div><div class="lines"></div></td></tr>')
checks = [
    "Every reference on one screen, side by side — hunt for a face that moved",
    "Brothers height check: both A sheets together, identical stature, non-negotiable",
    "Aura rule holds everywhere: adept hollow at the centre, bearer lit from within",
    "Every character against its movement's lighting plate — plastic shows here first",
    "Damage fixed at exactly three marks on Oriane — reject any frame with a fourth",
    "No colour in Movement II references except the crystal and the seam-light",
]
cl = "".join(f'<div class="ledrow"><span class="cb"></span><span class="nm" style="white-space:normal">{c}</span></div>' for c in checks)
add("gate-a", "GATE A", f"""
<h2>Gate A — identity lock, argued on paper first</h2>
<p class="sub">An anchor built on an unlocked face gets rebuilt thirty-nine times. Before you call this gate, write —
in pencil, from memory, without the screen — the three features per identity that must never move. Then open the
references and see if the sheets agree with you.</p>
<table><tr><th>Identity</th><th>Must not move</th><th>What moved (pencil)</th></tr>{irow}</table>
<h3>The lock list</h3>
{cl}
<div class="rulebox"><b>Passing this gate closed:</b> date <span class="bl" style="min-width:50pt"></span> ·
what you re-rolled to pass it <span class="bl" style="min-width:180pt"></span></div>
""", "nothing downstream begins until this holds", "gate closes once, in writing")

# ── P04 · anchor string ─────────────────────────────────────────────────────
cells = ""
for f in FRAMES:
    role = f["r"]
    cls = "shared" if role in ("shared", "match") else ("bridge" if role == "bridge" else "")
    tag = {"single": "", "shared": " · shared", "bridge": " · BRIDGE", "match": " · match"}[role]
    cells += (f'<div class="cell {cls}"><div class="fr"></div>'
              f'<div class="frl"><b>{esc(f["f"])}</b> {esc(f["s"])}{tag}</div></div>')
add("anchor-string", "ANCHOR STRING", f"""
<h2>Phase 1 — thumbnail the string before you generate it</h2>
<p class="sub">All 39 anchors in film order. Dashed boxes are shared joins or matched pairs — one drawing serves two
shots, so draw it once and mean it. Grey boxes are the two authored bridges and must go genuinely near-black.
Read the finished page as a comic strip: if the story fails here it fails in motion at forty times the price.</p>
<div class="anch">{cells}</div>
""", "39 anchors · 7 shared joins · 2 bridges · 2 matched pairs", "sketch loose, read strict")

# ── P05 · storyboard 6-up ───────────────────────────────────────────────────
c6 = "".join(
    '<div><div class="fr"></div>'
    '<div class="frl" style="margin-top:2pt">shot <span class="bl" style="min-width:30pt"></span> · '
    'sec <span class="bl" style="min-width:18pt"></span> · '
    'seam out <span class="bl" style="min-width:70pt"></span></div>'
    '<div class="lines" style="margin-top:2pt"></div><div class="lines"></div></div>'
    for _ in range(6))
add("storyboard-6up", "6-UP · EQUAL", f"""
<h2>Storyboard — six equal frames</h2>
<p class="sub">One drawing per idea, at a size where a composition can actually be judged. All frames 2.39:1.
Use it for the shots that carry the film — F35, the mountain, the vortex — and for arguing a variant against
the specced version before either is generated.</p>
<div class="grid6">{c6}</div>
""", "2.39:1 · equal frames · composition, not timing")

# ── P06 · storyboard 12-up ──────────────────────────────────────────────────
c12 = "".join(
    '<div><div class="fr lite"></div>'
    '<div class="frl" style="margin-top:1.5pt">shot <span class="bl" style="min-width:24pt"></span> · '
    '<span class="bl" style="min-width:52pt"></span></div></div>'
    for _ in range(12))
add("storyboard-12up", "12-UP · EQUAL", f"""
<h2>Storyboard — twelve equal frames</h2>
<p class="sub">Coverage and alternates: four takes on one shot, or a whole movement at a glance. Small on purpose —
if an idea does not read at this size it will not read at speed on screen either.</p>
<div class="grid12">{c12}</div>
<div class="rulebox"><b>Thumbnail discipline:</b> silhouette first, camera height second, light direction third.
No faces at this scale — a face drawn here is detail hiding a composition that has not been decided.</div>
""", "2.39:1 · equal frames · alternates and coverage")

# ── P07 · pulse — equal time ────────────────────────────────────────────────
ticks = ""
clock = 0
spans = []
for s in SHOTS:
    spans.append((clock, clock + s["d"], s))
    clock += s["d"]
STEP = 12
for i in range(0, TOTAL, STEP):
    on = next(s for a, b, s in spans if a <= i < b)
    m, sec = divmod(i, 60)
    ticks += (f'<div><div class="fr lite"></div>'
              f'<div class="frl" style="margin-top:1.5pt"><b>{m}:{sec:02d}</b> · {on["id"]} · MV{on["mv"]}</div></div>')
add("pulse-12s", "PULSE · 12s", f"""
<h2>The pulse — one frame every twelve seconds</h2>
<p class="sub">Equal time between frames, whatever the shots are doing: 25 ticks across the full 5:00. Sketch what is
actually on screen at each tick. This is the pacing read the shot list cannot give you — when three adjacent ticks
draw the same held composition, the hold is spending 24+ seconds, and it had better be S1, S13 or S20. When every
tick is a new sketch, you have built a trailer.</p>
<div class="pulse">{ticks}</div>
<div class="rulebox"><b>Read it in one pass:</b> the eye should snag exactly where the film means it to — the first
cut (0:48), the silence (S13), the empty frame after S14, the push on the older brother. Circle any snag the film
did not intend.</div>
""", f"25 ticks · every {STEP}s · total {TOTAL // 60}:{TOTAL % 60:02d}", "equal spacing — the honest pacing read")

# ── P08 · ribbon — duration-weighted ────────────────────────────────────────
SCALE = 0.150  # inches per second
rb = ""
for s in SHOTS:
    w = s["d"] * SCALE
    rb += (f'<div class="cell" style="width:{w:.2f}in">'
           f'<div class="fr m{s["mv"]}" style="width:{w:.2f}in"></div>'
           f'<div class="frl"><b>{s["id"]}</b> · {s["d"]}s</div></div>')
add("ribbon-weighted", "RIBBON · WEIGHTED", f"""
<h2>The ribbon — box width is shot length</h2>
<p class="sub">Every box is drawn at the width of its screen time ({SCALE:.3f}&Prime;/s), wrapping like text. A 16-second
hold gives you a wide panel and demands a composition that survives it; an 8-second aftermath gives you a sliver and
forbids one. Draw inside the time you actually have — the sheet makes over-designing a short shot physically
uncomfortable, which is the point. Top border: solid = Movement&nbsp;I, double = II, dotted = III.</p>
<div class="ribbon">{rb}</div>
<div class="rulebox"><b>Two uses:</b> thumbnail the whole film in order at true proportion, or cut the boxes out and
re-order them on the desk — the interleave of the swim and the battle was decided exactly this way. Re-ordering here
costs scissors; after Gate&nbsp;C it costs generations.</div>
""", f"23 shots · {TOTAL}s at {SCALE:.3f} in/s · mean {TOTAL / len(SHOTS):.1f}s", "different lengths, accordingly")

# ── P09 · gates B + C ───────────────────────────────────────────────────────
drift = [
    "Face — any identity whose features moved between neighbouring anchors",
    "Costume — damage marks, seam-light, robe construction identical across joins",
    "Light — key direction agrees with the movement's plate in every frame",
    "Grade — no warm tone anywhere in Movement II; island only warms at golden hour",
    "Shared joins — F11, F12, F17 read correctly as the END of one shot and the START of the next",
    "Match pairs — F09/F10 and F22/F23 agree on shape, scale and colour",
    "Bridges — B01 and B02 go genuinely near-black; 70% obscured reads as a failed hide",
]
dr = "".join(f'<div class="ledrow"><span class="cb"></span><span class="nm" style="white-space:normal">{d}</span></div>' for d in drift)
mvd = "".join(
    f'<tr><td style="width:1in"><b>Movement {m}</b></td>'
    f'<td style="width:.8in" class="right"><tt>{d}s</tt></td>'
    f'<td style="width:1.1in"><span class="pencil">actual&nbsp;</span><span class="bl" style="min-width:40pt"></span></td>'
    f'<td class="small">{n}</td></tr>'
    for m, d, n in [("I", 80, "five shots, first cut at 0:48"),
                    ("II", 118, "generated in strict sequence — the chain is the shot"),
                    ("III", 102, "locked-off witness; the only push is the last")])
add("gates-b-c", "GATES B + C", f"""
<h2>Gate B — the drift hunt</h2>
<p class="sub">All 39 anchors on one contact sheet, read left to right, twice. Fixing a jump here costs an image;
fixing it after Gate C costs a shot. Work the list with a pencil — an unticked line is an open gate.</p>
{dr}
<h2 style="margin-top:10pt">Gate C — the timing lock</h2>
<p class="sub">Cut the stills reel, watch all five minutes without stopping, then freeze. Note the timecode of every
reach-for-the-phone moment before deciding anything.</p>
<table><tr><th>Block</th><th>Target</th><th>Actual</th><th>Note</th></tr>{mvd}</table>
<div class="rulebox"><b>Cost table, after this gate:</b> re-order two shots ≈ 2 images before · ≈ 80 generations
after. Insert ≈ 3 before · ≈ 120 after. The lock is the last cheap moment — date closed
<span class="bl" style="min-width:50pt"></span></div>
""", "contact sheet then stills reel then freeze", "the last cheap moment")

# ── P10 · shot cards ────────────────────────────────────────────────────────
rows = ""
clock = 0
for s in SHOTS:
    tc = f"{clock // 60}:{clock % 60:02d}"
    clock += s["d"]
    model = esc(s["model"]).split("·")[0].strip()
    seam = esc(s["seam"])
    seam = seam[:56] + "…" if len(seam) > 58 else seam
    rows += (f'<tr><td style="width:.32in"><b>{s["id"]}</b></td>'
             f'<td style="width:.4in"><tt>{tc}</tt></td>'
             f'<td style="width:.3in" class="right"><tt>{s["d"]}s</tt></td>'
             f'<td style="width:1.28in" class="small">{esc(s["t"])}</td>'
             f'<td class="mono" style="width:1.05in">{model}</td>'
             f'<td class="note">{seam}</td>'
             f'<td style="width:.3in"><span class="cb"></span></td>'
             f'<td style="width:.3in"><span class="cb"></span></td>'
             f'<td style="width:.55in"><span class="bl" style="min-width:30pt"></span></td></tr>')
add("shot-cards", "SHOT CARDS", f"""
<h2>Phases 3–4 — the 23 generations, draft then final</h2>
<p class="sub">Draft box ticks at Gate D (does the seam read? can the model reach the B-frame?); final box ticks when
the shot ships. Attempts in pencil — three failures and the shot leaves the queue for the escalation ladder, and the
promoted-frame column records any draft frame that beat its anchor.</p>
<table><tr><th>ID</th><th>TC</th><th>Dur</th><th>Shot</th><th>Model</th><th>Seam into next</th>
<th>Drft</th><th>Fin</th><th>Att·prom</th></tr>{rows}</table>
""", f"total {TOTAL // 60}:{TOTAL % 60:02d} · Movement II in strict sequence · S20 gets the most attempts")

# ── P11 · methods ───────────────────────────────────────────────────────────
NOW = [
    ("Image-first anchor string", "decide the film as ~39 stills before any video; motion animates decisions already made"),
    ("End→start frame chaining", "shot N's last frame is N+1's literal first — continuity by construction, drift watched per link"),
    ("Forward extension", "feed the finished clip back in and continue the take (+30s) — the oner engine, 720p tax paid at finish"),
    ("Multi-shot in one generation", "several angles inside one generation hold world, wardrobe and light constant across their own cuts"),
    ("Ramps and body wipes", "speed ramps and near-black wipes deliver a cut's accent without leaving the frame"),
    ("Motion control", "drive a still character with a reference clip — choreography becomes repeatable instead of rerolled"),
    ("Cheap-pass previz + promotion", "every shot at budget tier first; any draft frame that beats its anchor is promoted into the ledger"),
    ("Deflicker → upscale → grade", "in that order, always — the reverse bakes shimmer into the master permanently"),
]
nrows = "".join(f'<tr><td style="width:1.85in"><b>{n}</b></td><td class="small">{d}</td></tr>' for n, d in NOW)
add("methods", "METHODS", f"""
<h2>Methods — what wins now, and what this production adds</h2>
<p class="sub">The first table is current best practice on the platform, as used by strong entrants and documented in
the bible. The two boxed methods are this production's additions — one better than practice, one best available.
Both were adversarially reviewed before they were written down; their qualifications are part of the method.</p>
<table>{nrows}</table>
__METHOD_BETTER__
__METHOD_BEST__
""", "current practice + two additions · qualifications are part of the method")

# ── P12 · finish + submit ───────────────────────────────────────────────────
fin = [
    ("1", "Deflicker every extended and chained shot — the seams shimmer and this is the only pass that removes it"),
    ("2", "Upscale to 2K/4K with the aigc preset — after deflicker, never before"),
    ("3", "Grade — three looks, one per movement: gold-on-black · cold blue-grey · golden hour"),
    ("4", "Gate E — picture lock. Anything still wrong is a sound problem, or it ships"),
]
frow = "".join(f'<tr><td style="width:.32in"><b class="mono" style="font-size:9pt">{n}</b></td><td>{t}</td>'
               f'<td style="width:.42in"><span class="cb"></span></td></tr>' for n, t in fin)
mvs = "".join(f'<div class="ledrow"><span class="cb"></span><span class="nm" style="white-space:normal">{t}</span></div>' for t in [
    "Official watermark + packshot on the final video",
    "Public post (IG / YT / X / Reddit) — film with both intact, account public and staying public",
    "Post AND account load in a logged-out browser window",
    "Every asset still inside the submission project — deleted nothing",
    "All prompts read as a stranger would — no novel term anywhere, they get published",
    "English subtitles or VO for all dialogue · MP4/MOV · ≤4K · 21:9",
    "S13 still ships silent — protect it from every instinct to fill it",
    "End card: “Original screen story by B.L. Barkey” · adapted-from credit in the description",
    "Submitted with a full day of margin — deadline night is not when you find a scope problem",
])
add("finish-submit", "FINISH · SUBMIT", f"""
<h2>Phase 6 — the order that cannot be reversed</h2>
<p class="sub">Four steps, strictly in order. Upscaling a flickering shot upscales the flicker, and there is no
route back from it.</p>
<table>{frow}</table>
<h2 style="margin-top:12pt">Phase 7 — the list that disqualifies</h2>
<p class="sub">Every line is a rule with teeth. An entry missing an MVS component does not compete and is not
published.</p>
{mvs}
<div class="rulebox"><b>Sign-off:</b> submitted <span class="bl" style="min-width:60pt"></span> ·
public post URL <span class="bl" style="min-width:170pt"></span></div>
""", "deflicker → upscale → grade · then the MVS, line by line", "11:59 PM PT · aim for morning")


# ── write ───────────────────────────────────────────────────────────────────
def build(better_html, best_html):
    out = []
    for slug, body in sheets:
        body = body.replace("__METHOD_BETTER__", better_html).replace("__METHOD_BEST__", best_html)
        out.append(f'<div class="sheet" data-slug="{slug}">{body}</div>')
    doc = ("<!doctype html><html><head><meta charset='utf-8'><title>Paper Kit</title>"
           f"<style>{CSS}</style></head><body>" + "".join(out) + "</body></html>")
    io.open("design/paper-kit.html", "w", encoding="utf-8").write(doc)
    print(f"design/paper-kit.html written — {len(sheets)} sheets, {len(doc)} bytes")


METHODS_FILE = "design/paper-kit-methods.json"
if os.path.exists(METHODS_FILE):
    m = json.load(open(METHODS_FILE))
    build(m["better"], m["best"])
else:
    build('<div class="mth"><h3><span class="tag">BETTER</span>(methods pending review)</h3></div>', "")
