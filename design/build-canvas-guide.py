# -*- coding: utf-8 -*-
"""Build the canvas guide — printable sheets for building the boards offline.

The paper kit (build-paper-kit.py) is for THINKING; the workflow sheets
(build-sheets.py) are for TRACKING. These sheets TEACH: how a canvas is laid
out, in what order, and what to look at when the four variants come back.

Scene 1 gets the full start-to-finish walkthrough because it is the smallest
board and the only one whose dependencies are all already chosen. Canvases II
and III then get the same shape at a glance, so the method is learned once and
applied twice.

Run from the repo root:
    node design/extract-data.mjs --prompts > /tmp/bible-data.json
    python3 design/build-canvas-guide.py /tmp/bible-data.json
    node design/render-canvas-guide.mjs
Writes design/canvas-guide.html, then the render script writes canvas-guide.pdf
(combined, repo root) and canvas-guide/NN-*.pdf (one per sheet).
"""
import html as H
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/bible-data.json"))
PLAN = json.load(open(os.path.join(ROOT, "design/anchor-plan.json")))
EMAP = json.load(open(os.path.join(ROOT, "design/element-map.json")))

ENT = {"&ldquo;": "“", "&rdquo;": "”", "&mdash;": "—", "&ndash;": "–",
       "&amp;": "&", "&rsquo;": "’", "&lsquo;": "‘", "&nbsp;": " ",
       "&middot;": "·", "&hellip;": "…", "&#37;": "%"}
TITLE = "MATTER OF LIGHT"
SUBT = "CANVAS GUIDE"


def clean(t):
    t = re.sub(r"<[^>]*>", "", str(t or ""))
    for k, v in ENT.items():
        t = t.replace(k, v)
    return t


def esc(t):
    return H.escape(clean(t), quote=False)


def snip(t, n):
    """Trim to n characters on a word boundary. A line cut mid-word reads as
    a rendering fault rather than an abbreviation."""
    t = clean(t)
    if len(t) <= n:
        return t
    cut = t[:n].rstrip()
    sp = cut.rfind(" ")
    if sp > n * 0.6:
        cut = cut[:sp]
    return cut.rstrip(" ,;:.\u2014-") + "\u2026"


# ---------------------------------------------------------------- data joins
JOB = {f["f"]: f.get("job") for f in PLAN["frames"]}
HAND = {f["f"]: f.get("handles", []) for f in PLAN["frames"]}
DEP = {f["f"]: f.get("dep") for f in PLAN["frames"]}
FR = {f["f"]: f for f in DATA["FRAMES"]}

SHOTS = []
_t = 0
for s in DATA["SHOTS"]:
    SHOTS.append(dict(id=s["id"], mv=int(s["mv"]), d=int(s["d"]), t=clean(s["t"]),
                      at=_t, model=clean(s.get("model", "")), cam=clean(s.get("cam", "")),
                      seam=clean(s.get("seam", ""))))
    _t += int(s["d"])
TOTAL = _t

# a frame's label carries its shot roles, e.g. "S10 B / S11 A"
START, END = {}, {}
for f in DATA["FRAMES"]:
    for part in str(f.get("s", "")).split("/"):
        m = re.match(r"^(S\d+)\s*([AB])$", part.strip())
        if m:
            (START if m.group(2) == "A" else END)[m.group(1)] = f["f"]
for s in SHOTS:
    s["a"], s["b"] = START.get(s["id"]), END.get(s["id"])


def board(mv):
    """The shots that live on a board, in order, plus its unique frame columns."""
    fr = [f["f"] for f in DATA["FRAMES"] if int(f["mv"]) == mv]
    sh = [s for s in SHOTS if s["a"] in fr]
    cols = []
    for s in sh:
        if not cols or cols[-1] != s["a"]:
            cols.append(s["a"])
        cols.append(s["b"])
    return sh, cols


BOARDS = {
    1: dict(name="Canvas I · The Sun", plate="plate-sun",
            souls=["oriane", "caedom-ascended"],
            look="Gold on black. Key from below, thrown by a burning star. Warm highlights, "
                 "cold shadows, beams of solid light behaving as architecture.",
            note="Movement I and the coda. The only board that is a bright field — and so "
                 "never the source for a social cut."),
    2: dict(name="Canvas II · The Ocean", plate="plate-ocean-dark",
            souls=["oriane"],
            look="Storm sea and sky near-black. Lightning, wave crests and hanging spray are "
                 "the only bright shapes. Fully desaturated, no warm colour anywhere.",
            note="The whole of Movement II. Dark ground, high local contrast — every social "
                 "cut comes from this board."),
    3: dict(name="Canvas III · The Island", plate="plate-island",
            souls=["alder", "wren"],
            look="Golden hour with the treeline's shadow claiming most of the ground. The "
                 "bombardment shots swap to plate-bombardment: low red sun, backlit, no cool tone.",
            note="Movement III. Two plates on one board is the single exception to the "
                 "one-plate rule, and it is why the bombardment shots are grouped."),
}

CSS = """
@font-face{font-family:"Body";src:url("f/InstrumentSans-Regular.ttf");font-weight:400}
@font-face{font-family:"Body";src:url("f/InstrumentSans-Bold.ttf");font-weight:700}
@font-face{font-family:"Mono";src:url("f/GeistMono-Regular.ttf")}
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
h3{font:700 10pt/1.2 "Body";margin:9pt 0 3pt}
.sub{font:8.5pt/1.4 "Body";color:#555;margin-bottom:8pt;max-width:6.9in}
.cb{display:inline-block;width:9pt;height:9pt;border:1pt solid #333;border-radius:1.5pt;
  vertical-align:-1.5pt;flex:none}
.bl{display:inline-block;border-bottom:.8pt solid #999;min-width:52pt;height:9pt}
tt{font:7.5pt "Mono"}
table{border-collapse:collapse;width:100%}
th{font:700 6.5pt "Mono";letter-spacing:.12em;text-transform:uppercase;color:#777;
  text-align:left;border-bottom:1pt solid #101010;padding:2pt 4pt 3pt}
td{border-bottom:.6pt solid #d9d9d9;padding:2.6pt 4pt;vertical-align:top}
tr{page-break-inside:avoid}
.small{font:8pt/1.35 "Body"}
.note{font:italic 7pt/1.25 "Body";color:#8a8a8a}
.foot{margin-top:auto;padding-top:6pt;border-top:.8pt solid #ccc;display:flex;
  justify-content:space-between;font:7pt "Mono";color:#999;letter-spacing:.08em}

/* numbered steps */
.step{display:grid;grid-template-columns:20pt 1fr;gap:8pt;padding:5pt 0;
  border-bottom:.6pt solid #e4e4e4;break-inside:avoid}
.step:last-child{border-bottom:0}
.step .n{font:700 12pt/1 "Num";color:#101010;padding-top:1pt}
.step b{font:700 8.6pt "Body";display:block;margin-bottom:1pt}
.step b b,.step b tt{display:inline;font-weight:700}
.step span{font:8pt/1.4 "Body";color:#444;display:block}
.step tt{color:#222}

/* the shelf strip */
.shelf{border:1pt solid #101010;padding:6pt 8pt;margin:6pt 0 10pt}
.shelf .lb{font:700 6.5pt "Mono";letter-spacing:.14em;text-transform:uppercase;color:#777;
  margin-bottom:4pt}
.hchips{display:flex;flex-wrap:wrap;gap:3pt}
.hchips i{font:7.5pt "Mono";font-style:normal;border:.7pt solid #999;border-radius:2pt;
  padding:2pt 4pt;background:#f4f4f4}
.hchips i.p{border-color:#101010;border-width:1pt;font-weight:700;background:#e8e8e8}
.hchips i.s{border-style:dashed}

/* board strip: anchor boxes with shot brackets under them */
.strip{display:flex;gap:4pt;align-items:flex-start;margin-top:4pt}
.acell{flex:1 1 0;min-width:0;display:flex;flex-direction:column;gap:2pt}
.acell .fr{border:1pt solid #333;border-radius:1.5pt;height:.62in;background:#fff;
  display:flex;align-items:center;justify-content:center;font:700 8pt "Mono"}
.acell .fr.sh{border-width:2pt;background:#f0ece0}
.acell .fr.br{border-style:dashed;background:#ececf6}
.acell .fr.mt{border-width:1.4pt;background:#f7ece8}
.acell .cap{font:6pt/1.25 "Mono";color:#777;text-align:center;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.brk{display:flex;gap:4pt;margin-top:3pt}
.brk .sp{border:.8pt solid #101010;border-top-width:2.4pt;border-radius:2pt;
  padding:3pt 4pt;min-width:0;display:flex;flex-direction:column;gap:1pt}
.brk .sp b{font:700 7.5pt "Mono"}
.brk .sp span{font:6.8pt/1.25 "Body";color:#555;
  display:block;overflow:hidden}
.brk .sp.nc{background:#f6efdf}

/* frame ledger with pencil blanks */
.led th:nth-child(1),.led td:nth-child(1){width:34pt}
.led th:nth-child(2),.led td:nth-child(2){width:44pt}
.led th:nth-child(5),.led td:nth-child(5){width:96pt}
.led td.k{font:7.5pt "Mono"}
.tight td{padding:1.5pt 4pt}
.tight td.h{font:6.2pt/1.22 "Mono"}
.tight td.small{font:7.2pt/1.25 "Body"}
.tight .acell .fr{height:.5in}
.led td.h{font:6.6pt/1.3 "Mono";color:#555}
.led td.pick{border-bottom:.6pt solid #d9d9d9}
.led td.pick i{display:block;border-bottom:.8pt solid #aaa;height:9pt;font-style:normal}

/* ordering ribbons */
.ord{margin-top:5pt}
.ord .rw{display:flex;height:15pt;gap:.6pt;margin:2pt 0 3pt;border:.7pt solid #101010}
.ord .rw b{display:block;min-width:0}
.ord .rw b.m1{background:#101010}
.ord .rw b.m2{background:#767676}
.ord .rw b.m3{background:#c9c9c9}
.ord .rw b.nw{background:repeating-linear-gradient(45deg,#101010 0 2pt,#fff 2pt 4pt)}
.ord .oh{display:flex;align-items:baseline;gap:6pt;margin-top:7pt}
.ord .oh b{font:700 9pt "Body"}
.ord .oh tt{color:#777}
.ord p{font:7.8pt/1.35 "Body";color:#444;margin-top:1pt}
.ord p em{font-style:normal;font-weight:700;color:#101010}
.legend{display:flex;gap:10pt;font:6.5pt "Mono";color:#777;margin-top:3pt}
.legend s{text-decoration:none;display:flex;align-items:center;gap:3pt}
.legend s i{width:8pt;height:8pt;display:block;border:.6pt solid #999}

.rulebox{border:1pt solid #101010;padding:6pt 8pt;margin-top:8pt;font:8pt/1.45 "Body"}
.rulebox b{font-weight:700}
.warn{border-left:3pt solid #101010;background:#f4f4f4;padding:5pt 8pt;margin-top:7pt;
  font:8pt/1.4 "Body"}
"""


def head(n, tot, right):
    return ('<div class="rh"><span class="l">%s</span>'
            '<span class="m">%s &middot; SHEET %02d OF %02d</span>'
            '<span class="r">%s</span></div>' % (TITLE, SUBT, n, tot, right))


def foot(left):
    return ('<div class="foot"><span>%s</span>'
            '<span>%d shots &middot; %d anchors &middot; %ds</span></div>'
            % (left, len(SHOTS), len(DATA["FRAMES"]), TOTAL))


ROLE_CLS = {"shared": "sh", "bridge": "br", "match": "mt"}


def strip_html(mv, with_caps=True):
    sh, cols = board(mv)
    idx = {c: i for i, c in enumerate(cols)}
    cells = []
    for c in cols:
        r = FR[c].get("r", "single")
        extra = [h for h in HAND.get(c, []) if h != BOARDS[mv]["plate"]]
        cap = ", ".join("@" + h for h in extra[:2]) or ("+" + str(len(extra)) if extra else "plate only")
        if len(extra) > 2:
            cap += " +%d" % (len(extra) - 2)
        cells.append('<div class="acell"><div class="fr %s">%s</div>%s</div>'
                     % (ROLE_CLS.get(r, ""), c,
                        '<div class="cap">%s</div>' % esc(cap) if with_caps else ""))
    brk = []
    for s in sh:
        span = idx[s["b"]] - idx[s["a"]] + 1
        nc = " nc" if re.match(r"^(None|No seam)", s["seam"]) else ""
        brk.append('<div class="sp%s" style="flex:%d 1 0"><b>%s &middot; %ds</b>'
                   '<span>%s</span></div>' % (nc, span, s["id"], s["d"], esc(s["t"])))
    return ('<div class="strip">%s</div><div class="brk">%s</div>'
            % ("".join(cells), "".join(brk)))


def shelf_html(mv):
    cfg = BOARDS[mv]
    _, cols = board(mv)
    hs = []
    for c in cols:
        for h in HAND.get(c, []):
            if h not in hs:
                hs.append(h)
    chips = "".join('<i class="%s">@%s</i>' % ("p" if h == cfg["plate"] else "", esc(h))
                    for h in hs)
    chips += "".join('<i class="s">soul: %s</i>' % esc(s) for s in cfg["souls"])
    return ('<div class="shelf"><div class="lb">Shelf &mdash; drag these in first, '
            'left to right</div><div class="hchips">%s</div></div>' % chips)


def ledger_html(mv):
    _, cols = board(mv)
    cut = 96 if len(cols) <= 12 else 72
    rows = []
    for c in cols:
        f = FR[c]
        rows.append(
            '<tr><td class="k">%s</td><td class="k">%s</td><td class="h">%s</td>'
            '<td class="small">%s</td><td class="pick"><i></i></td></tr>'
            % (c, esc(f.get("r", "single")),
               esc(" ".join("@" + h for h in HAND.get(c, []))),
               esc(snip(f.get("d", ""), cut)),
               ))
    return ('<table class="led"><thead><tr><th>Frame</th><th>Role</th><th>Attach</th>'
            '<th>What it has to be</th><th>Chosen job id</th></tr></thead>'
            '<tbody>%s</tbody></table>' % "".join(rows))


# ------------------------------------------------------------------- sheets
def sheet_method(n, tot):
    steps = [
        ("One canvas per plate, not per scene",
         "Every frame on a board inherits that board's key and palette. A board that mixes "
         "plates is a board where the light drifts between neighbouring shots. Movement I's "
         "coda returns to the Sun, so <tt>S23</tt> is built on Canvas I even though it plays last."),
        ("Shelf first: plate, then location, then people and props",
         "Drag each handle in from the Elements panel before generating anything. A face or a "
         "place that is dragged in cannot drift; one that is described in words will."),
        ("Anchors left to right in shot order",
         "A <b>shared</b> frame ends one shot and starts the next — one image, generated once, "
         "serving two shots. A <b>bridge</b> is a near-black hidden cut. A <b>match</b> pair is "
         "two different images designed to cut together."),
        ("Batch of four, select one, and only then move on",
         "The account holds one image per anchor. That is a skeleton, not a choice. Nothing "
         "downstream of a frame is generated until that frame is chosen."),
        ("Chain from the rendered last frame, never from the anchor still",
         "Once a shot exists, pull its actual final frame and start the next shot from that. "
         "The anchor is the target; the render is the truth."),
        ("Any face at medium or closer is re-run on the Soul",
         "Handles hold a look; Souls hold an identity. Generate with <tt>soul_2</tt> and that "
         "character's Soul whenever the face carries the shot."),
    ]
    body = "".join(
        '<div class="step"><span class="n">%d</span><div><b>%s</b><span>%s</span></div></div>'
        % (i + 1, t, d) for i, (t, d) in enumerate(steps))
    return ('<section class="sheet" data-slug="method">' + head(n, tot, "THE METHOD") +
            '<h2>How a board is built</h2>'
            '<p class="sub">Six rules. Everything else in this guide is these six applied to '
            '%d anchors and %d shots across three boards.</p>' % (len(DATA["FRAMES"]), len(SHOTS)) +
            body +
            '<div class="rulebox"><b>Two things the API cannot do, so the canvas has to.</b> '
            'It cannot place a generation inside the submission project — there is no folder '
            'call anywhere in the platform API — and it cannot pay for the final pass out of '
            'the credit balance. So the API is the concept side: it writes and holds the '
            'prompts, runs the wide batches that find a composition, and keeps the ledger. '
            '<b>Every frame and clip that reaches the cut is generated here, in the '
            'project.</b></div>'
            '<div class="warn"><b>Do not route picture through anything else.</b> Anything that '
            'touches the image outside the platform produces footage with no generation history '
            'behind it, which is what the rules exist to catch. Deflicker, upscale and grade '
            'inside Cinema Studio or not at all. Sound may be made anywhere — and then every '
            'audio file has to be uploaded into the project.</div>' +
            foot("Read this sheet once. The rest of the kit assumes it.") + '</section>')


def sheet_scene1_walk(n, tot):
    sh, cols = board(1)
    s1, s2 = sh[0], sh[1]
    steps = [
        ("Open the project and show the Elements panel",
         "Everything is generated inside the submission project, from the first test frame "
         "onward. A frame made outside it has to be made again."),
        ("Drag the shelf in, in order",
         "<tt>@plate-sun</tt> first — it decides the key for every other tile on this board — "
         "then <tt>@courtyard-of-worlds</tt>, then <tt>@oriane</tt> and "
         "<tt>@caedom-ascended-1</tt>, then <tt>@frozen-tear</tt>."),
        ("Generate <b>F01</b> — four variants, pick one",
         "Attach <tt>@plate-sun</tt> only. Judge it at thumbnail size: ninety percent of the "
         "frame must be empty black with one ember at the bottom edge. If you can see a "
         "horizon or a structure, it is wrong."),
        ("Generate <b>F02</b> — four variants, pick one",
         "Attach <tt>@plate-sun</tt> and <tt>@courtyard-of-worlds</tt>. The centre has to be "
         "genuinely blinding: the seam that carries %s into %s hides inside that glare, and a "
         "readable centre means a visible cut." % (s1["id"], s2["id"])),
        ("Generate <b>F03</b> — four variants, pick one",
         "Attach the plate, the location, both identities, <b>and the F02 you just chose</b> "
         "as the previous frame. Same room, same lens height, same costume state. Figures from "
         "behind — this is the last frame before the film shows a face."),
        ("Generate %s from F01 → F02" % s1["id"],
         "<tt>%s</tt>. Start frame F01, end frame F02. %s" % (esc(s1["model"]), esc(s1["cam"]))),
        ("Extract %s's real last frame, then generate %s" % (s1["id"], s2["id"]),
         "<tt>%s</tt>. Do not start from the F02 still — start from the frame %s actually "
         "rendered, or the join will show. End on F03." % (esc(s2["model"]), s1["id"])),
        ("Watch the two shots back as one 34-second run",
         "You are testing one thing only: whether the seam inside the glare is invisible. If "
         "it is not, the fix is a brighter F02, not a different %s." % s2["id"]),
    ]
    body = "".join(
        '<div class="step"><span class="n">%d</span><div><b>%s</b><span>%s</span></div></div>'
        % (i + 1, t, d) for i, (t, d) in enumerate(steps))
    return ('<section class="sheet" data-slug="scene-1-walkthrough">' +
            head(n, tot, "SCENE 1 · WALKTHROUGH") +
            '<h2>Scene 1, start to finish</h2>'
            '<p class="sub">Three anchors and two shots — the smallest complete unit in the '
            'film, and the only one whose every dependency is already chosen. Build this board '
            'first. If the method holds here it holds everywhere; if it does not, the fault is '
            'in the method and not in the film.</p>' +
            shelf_html(1) + body +
            '<div class="warn"><b>Where Scene 1 stands right now.</b> A four-variant selection '
            'pass for F01, F02 and F03 has been generated into the account and is waiting to be '
            'looked at. F03 was chained from the <i>skeleton</i> F02, so once you choose a real '
            'F02 it is worth re-running F03 against it — one batch, and the continuity is '
            'honest.</div>' +
            foot("Scene 1 · S1 + S2 · 34 seconds") + '</section>')


def sheet_board(mv, n, tot, slug):
    cfg = BOARDS[mv]
    sh, cols = board(mv)
    secs = sum(s["d"] for s in sh)
    tight = " tight" if len(cols) > 12 else ""
    return ('<section class="sheet%s" data-slug="%s">' % (tight, slug) +
            head(n, tot, cfg["name"].split("·")[0].strip().upper()) +
            '<h2>%s</h2>' % esc(cfg["name"]) +
            '<p class="sub">%s <b>Look line:</b> %s</p>' % (esc(cfg["note"]), esc(cfg["look"])) +
            shelf_html(mv) +
            '<h3>The board — anchors across, shots bracketed underneath</h3>' +
            strip_html(mv) +
            '<div class="legend">'
            '<s><i style="background:#f0ece0;border-width:1.4pt"></i>shared &mdash; one image, two shots</s>'
            '<s><i style="background:#ececf6;border-style:dashed"></i>bridge &mdash; hidden cut</s>'
            '<s><i style="background:#f7ece8"></i>match &mdash; designed together</s>'
            '<s><i style="background:#f6efdf"></i>no cut permitted inside</s></div>'
            '<h3>Frame ledger &mdash; write the job id you choose</h3>' +
            ledger_html(mv) +
            foot("%d anchors · %d shots · %ds" % (len(cols), len(sh), secs)) + '</section>')


def sheet_selection(n, tot):
    rows = [
        ("Plate and location frames", "F01, F02, F10, F23, F32",
         "Judge at thumbnail size, squinting. You are checking key direction and where the "
         "bright shapes sit, not detail. Reject anything whose light disagrees with its plate."),
        ("Identity frames — a face at medium or closer", "F06, F07, F35",
         "Full size, and side by side with the character sheet. One moved feature is a "
         "rejection. Re-run on soul_2 with the Soul rather than arguing with a handle."),
        ("Shared frames", "F02, F11, F12, F17, F30",
         "Judged twice — once as the end of the shot before, once as the start of the shot "
         "after. A shared frame that only works one way is not chosen yet."),
        ("Match pairs", "F09/F10, F22/F23",
         "Only ever judged as a pair, laid side by side. Scale, colour and shape have to "
         "carry across the cut; either image alone tells you nothing."),
        ("Bridge frames", "B01, B02",
         "The test is whether they are dark or flat enough to hide a cut. If you can read "
         "detail in one, it is not a bridge."),
        ("Held shots — no cut permitted", "S10, S13, S20",
         "The composition has to survive being held for its whole duration. Look at it for "
         "the full sixteen seconds before choosing; boredom at second nine is a rejection."),
    ]
    body = "".join('<tr><td class="small"><b>%s</b></td><td class="k">%s</td>'
                   '<td class="small">%s</td></tr>' % (t, f, d) for t, f, d in rows)
    return ('<section class="sheet" data-slug="selection-pass">' +
            head(n, tot, "SELECTION") +
            '<h2>Batch of four, select one</h2>'
            '<p class="sub">Every anchor in the account today is one generation — a skeleton, '
            'made so the boards could be laid out. None of them has been looked at. What '
            'follows is what to actually look at, by what kind of frame it is.</p>'
            '<table><thead><tr><th>Kind of frame</th><th>Which</th>'
            '<th>What decides it</th></tr></thead><tbody>%s</tbody></table>' % body +
            '<div class="rulebox"><b>Spend the allowance where the film is decided.</b> '
            'F35 first — it is the last image in the film and it carries the whole ending. Then '
            'F06 and F07, the two-shot that has to hold fourteen seconds on one face. Then F17, '
            'the scale shot. Then the F09/F10 match, which is the only join between two '
            'movements. Everything else can be chosen in one pass.</div>'
            '<h3>Order of work</h3>'
            '<p class="small">Gate A before any anchor is trusted: every reference on one '
            'screen, read left to right twice, looking for one thing — a face that moved. Then '
            'the anchors board by board. Then Gate B: all %d on one contact sheet in film order. '
            'Drift caught at Gate B costs one image; the same drift caught after the motion pass '
            'costs a clip.</p>' % len(DATA["FRAMES"]) +
            foot("Nothing downstream of a frame is generated until that frame is chosen") +
            '</section>')


def sheet_order(n, tot):
    ids = [s["id"] for s in SHOTS]
    D = {s["id"]: s for s in SHOTS}

    def ribbon(order):
        cells = []
        for x in order:
            if isinstance(x, tuple):
                sid, dur, mv, new = x
            else:
                sid, dur, mv, new = x, D[x]["d"], D[x]["mv"], False
            cells.append('<b class="m%d%s" style="flex:%d"></b>'
                         % (mv, " nw" if new else "", dur))
        return '<div class="rw">%s</div>' % "".join(cells)

    opts = [
        ("A", "Linear — three movements in order", "0 new anchors", ids,
         "Nothing to build; chains run forward in strict order and the source's own sequence "
         "is preserved exactly. <em>But</em> it peaks at the vortex at 2:50 and then runs two "
         "minutes of falling action, and Oriane dies at 3:18 with two strangers arriving cold."),
        ("B", "Prologue splice — the beach lands before she does", "1 new anchor",
         ids[:12] + [("S15a", 6, 3, True)] + ["S13", "S14"] + [("S15b", 6, 3, True)] + ids[15:],
         "<em>Recommended.</em> Splits S15 and moves the first half early, so the brothers are "
         "established before Oriane dies — the biggest structural complaint against the current "
         "cut, gone for one generation. F23 already carries the streak's reflection, so the only "
         "new frame is a clean Nacre Beach dawn with no streak in it. Risk: a quiet beach beat "
         "now sits immediately before the film's biggest moment."),
        ("C", "Alternating — II's back half into III's front half", "about 3 anchors",
         ids[:12] + ["S15", "S13", "S16", "S14", "S17"] + ids[17:],
         "Two clocks through the middle, and the scale jump into S13 gets bigger, not smaller. "
         "<em>But</em> alternation reads as simultaneity and the source explicitly denies it — "
         "and it strands three seams: F22/F23 no longer adjoin, S16 has to start off the closing "
         "vortex eye, and the green streak needs a new place to land."),
        ("D", "Full causal interlace", "about 60 anchors",
         ["S1", "S2", "S3", "S15", "S4", "S5", "S16", "S6", "S7", "S17", "S8", "S9",
          "S18", "S10", "S11", "S19", "S12", "S13", "S20", "S14", "S21", "S22", "S23"],
         "Argued properly and lost five criteria to three. It needs about 40 generations at a "
         "7-second mean, asks the audience to infer a causal link the text denies, and ends on a "
         "resolution rather than a revelation — closing off the novel it exists to introduce."),
    ]
    body = ""
    for k, name, cost, order, why in opts:
        body += ('<div class="oh"><b>%s &middot; %s</b><tt>%s</tt></div>%s<p>%s</p>'
                 % (k, esc(name), esc(cost), ribbon(order), why))
    return ('<section class="sheet" data-slug="ordering">' + head(n, tot, "ORDERING") +
            '<h2>Four ways to order the same shots</h2>'
            '<p class="sub">Bar width is duration. Black is the Sun, grey the Ocean, pale the '
            'Island; hatched is a shot that does not exist yet. The question these four answer '
            'is whether Movement II\'s back half should fold into Movement III\'s front half.</p>'
            '<div class="ord">%s</div>' % body +
            '<div class="rulebox"><b>Why B is cheap and C is not.</b> The full interlace lost on '
            'source fidelity and on one-viewing legibility, and both losses come from the same '
            'thing: alternation reads as simultaneity, and the source opens the second story '
            '&ldquo;the next day&rdquo;. A single establishing beat placed early is not '
            'alternation. It buys the emotional continuity without asking anyone to infer a '
            'causal link the source denies.</div>' +
            foot("Decide at Gate C · after this a structural change costs video, not images") +
            '</section>')


def sheet_lessons(n, tot):
    rows = [
        ("Generating outside the project",
         "Every asset in the film has to sit inside the submission project so the generation "
         "history verifies it. There is no folder call in the API — nothing can be moved in "
         "afterwards from code. Generate inside the project from the first frame."),
        ("Describing a face instead of dragging it",
         "A described face drifts between frames and there is no fixing it later. Drag the "
         "handle; for anything at medium or closer, use the Soul."),
        ("Building on an unchosen frame",
         "The account holds one image per anchor and none has been looked at. Anything chained "
         "off a skeleton frame has to be made again once the real frame is picked."),
        ("Starting a shot from the anchor still",
         "The still is the target, not the output. Chain from the frame the previous shot "
         "actually rendered or the join will show."),
        ("Cutting inside a held shot",
         "S10, S13 and S20 do their whole job by not cutting. Awe needs duration; a cut there "
         "destroys the only thing the shot is for."),
        ("Mixing plates on one board",
         "Neighbouring frames inherit from whatever is nearest. One plate per board, with the "
         "bombardment shots as the one deliberate exception."),
        ("Naming a handle carelessly",
         "The API cannot rename or delete an element. A wrong name is permanent from that side "
         "and has to be cleaned up by hand in the web app."),
        ("Leaving exploration in the project",
         "Everything inside the project is read as part of the submission. Work the film does "
         "not use belongs outside it."),
    ]
    body = "".join('<tr><td class="small"><b>%s</b></td><td class="small">%s</td></tr>'
                   % (t, d) for t, d in rows)
    return ('<section class="sheet" data-slug="costly-mistakes">' + head(n, tot, "WHAT IT COSTS") +
            '<h2>Eight ways to lose a day</h2>'
            '<p class="sub">Each of these has already happened once on this production or is '
            'one obvious step away from it. They are cheap to avoid and expensive to '
            'discover late.</p>'
            '<table><thead><tr><th>The mistake</th><th>Why it costs</th></tr></thead>'
            '<tbody>%s</tbody></table>' % body +
            '<h3>The order of everything</h3>'
            '<p class="small">Gate A, identity &mdash; every reference on one screen, no face '
            'moved. Then the anchors, board by board, batch of four and select one. Gate B, the '
            'string &mdash; all %d anchors on one contact sheet in film order. Gate C, timing '
            '&mdash; runtime, shot count and order frozen. Then the cheap motion pass, then Gate '
            'D. Then the final pass, then Gate E, picture lock, after which nothing is generated '
            'again. Sound, watermark, packshot, public post, and submit with a full day in '
            'hand.</p>' % len(DATA["FRAMES"]) +
            foot("A gate that is not written down is not held") + '</section>')


# ------------------------------------------------------------------- output
BUILDERS = [
    sheet_method,
    sheet_scene1_walk,
    lambda n, t: sheet_board(1, n, t, "canvas-1-sun"),
    sheet_selection,
    lambda n, t: sheet_board(2, n, t, "canvas-2-ocean"),
    lambda n, t: sheet_board(3, n, t, "canvas-3-island"),
    sheet_order,
    sheet_lessons,
]

TOT = len(BUILDERS)
sheets = "\n".join(b(i + 1, TOT) for i, b in enumerate(BUILDERS))
out = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
       '<title>%s — canvas guide</title><style>%s</style></head><body>%s</body></html>'
       % (TITLE, CSS, sheets))
path = os.path.join(ROOT, "design/canvas-guide.html")
open(path, "w", encoding="utf-8").write(out)
print("design/canvas-guide.html — %d sheets, %d bytes" % (TOT, len(out)))
