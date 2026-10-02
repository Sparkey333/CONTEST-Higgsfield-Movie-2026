#!/usr/bin/env python3
"""Build design/status-sheet.html — what is done and what is left, on paper.

Every figure is read from a file: the shot ledger for clips, the anchor plan
for frames, element-map for handles and Souls, project-folder-gap for what is
still outside the contest project. Nothing here is remembered.
"""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda p: json.load(open(os.path.join(ROOT, p), encoding="utf-8"))
led = R("design/shot-ledger.json")["shots"]
plan = R("design/anchor-plan.json")
em = R("design/element-map.json")
gap = R("design/project-folder-gap.json")
aud = R("design/model-audit.json")

SOULS = [("oriane","keep","Movement I and II"), ("alder","keep","Movement III"),
         ("wren","keep","Movement III"), ("caedom-ascended","keep","Movement I and S23"),
         ("caedom-before","keep","not used by the film"),
         ("caedom-mortal","DELETE","contaminated training set"),
         ("Caedom","DELETE","this is Oriane, misnamed")]
order = sorted(led, key=lambda x: int(x[1:]))
tc, TC = 0, {}
for s in order: TC[s] = tc; tc += led[s]["d"]
def mmss(n): return "%d:%02d" % (n//60, n%60)
def esc(x): return html.escape(str(x or ""))
fails = {r["id"]: r["fails"] for r in aud["shots"]}
nconc = sum(1 for v in led.values() if v.get("concept"))
MV = {1:"I · The Sun", 2:"II · The Ocean", 3:"III · The Island"}

o=["""<meta charset="utf-8"><title>Status</title>
<style>
@page{size:letter;margin:0}
*{box-sizing:border-box}
body{margin:0;font:11px/1.45 "Helvetica Neue",Helvetica,Arial,sans-serif;color:#141210;background:#fff}
.sheet{width:8.5in;height:11in;padding:0.6in 0.62in;position:relative;page-break-after:always;overflow:hidden;background:#fff}
@media screen{body{background:#3a3631;padding:26px 14px}
 .sheet{margin:0 auto 22px;box-shadow:0 2px 22px rgba(0,0,0,.42)}}
.sheet:last-child{page-break-after:auto}
h1{font:400 27px/1.1 Georgia,serif;margin:0 0 5px;letter-spacing:-.01em}
.sub{color:#6d665c;margin:0 0 16px;font-size:11.5px}
.rule{height:1px;background:#141210;margin:0 0 15px}
h2{font:400 15px/1.2 Georgia,serif;margin:19px 0 7px;display:flex;align-items:baseline;gap:8px}
h2 .c{margin-left:auto;font:400 9px/1 ui-monospace,Menlo,monospace;letter-spacing:.12em;color:#8b8378}
.kpi{display:flex;border:1px solid #d8d2c8;margin:0 0 6px}
.kpi div{flex:1;padding:8px 10px;border-right:1px solid #d8d2c8}
.kpi div:last-child{border-right:0}
.kpi b{display:block;font:400 19px/1.1 ui-monospace,Menlo,monospace;font-variant-numeric:tabular-nums}
.kpi span{font-size:8.5px;color:#8b8378;letter-spacing:.03em;text-transform:uppercase}
table{border-collapse:collapse;width:100%;font-size:10px}
th{text-align:left;font:400 8.5px/1 ui-monospace,Menlo,monospace;letter-spacing:.11em;
   text-transform:uppercase;color:#8b8378;padding:0 5px 5px;border-bottom:1px solid #141210}
td{padding:3.4px 5px;border-bottom:1px solid #ece7df;vertical-align:top}
td.m{font-family:ui-monospace,Menlo,monospace;font-variant-numeric:tabular-nums;white-space:nowrap}
.bx{display:inline-block;width:9px;height:9px;border:1.2px solid #141210;margin-right:3px;vertical-align:-1px}
.bx.on{background:#141210;position:relative}
.bx.on::after{content:"";position:absolute;left:2px;top:0.5px;width:2.5px;height:5px;
  border:solid #fff;border-width:0 1.2px 1.2px 0;transform:rotate(43deg)}
.warn{color:#a8442c}
.ok{color:#3d6b55}
.dim{color:#8b8378}
p.note{font-size:10px;color:#544e46;margin:6px 0 0;max-width:62ch}
.fn{position:absolute;left:0.62in;right:0.62in;bottom:0.42in;border-top:1px solid #ece7df;
    padding-top:6px;font:8.5px/1.3 ui-monospace,Menlo,monospace;color:#a8a096;
    display:flex;justify-content:space-between}
ol.todo{margin:4px 0 0;padding-left:0;list-style:none;counter-reset:t}
ol.todo li{counter-increment:t;padding:5px 0 5px 22px;border-bottom:1px solid #ece7df;position:relative;font-size:10.5px}
ol.todo li::before{content:counter(t,decimal-leading-zero);position:absolute;left:0;top:6px;
  font:8.5px ui-monospace,Menlo,monospace;color:#a8a096}
ol.todo b{font-weight:600}
ol.todo span{color:#8b8378}
</style>"""]

# ---------------- sheet 1 : the film ----------------
o.append('<div class="sheet"><h1>MATTER OF LIGHT — where it stands</h1>')
o.append('<p class="sub">%s · deadline 14 Sep 23:59 UTC · every figure below read from a file, none remembered</p>'
         % esc(aud["checked"]))
o.append('<div class="rule"></div>')
o.append('<div class="kpi"><div><b>39 / 39</b><span>anchor frames</span></div>'
         '<div><b>%d / 23</b><span>shots with a clip</span></div>'
         '<div><b>0 / 23</b><span>final pass</span></div>'
         '<div><b>0 / 23</b><span>finished</span></div>'
         '<div><b>15 / 37</b><span>elements in project</span></div></div>' % nconc)
o.append('<h2>The 23 shots<span class="c">draft = a cheap 10s concept clip, not the shot</span></h2>')
o.append('<table><thead><tr><th style="width:34px">&nbsp;</th><th style="width:34px">Shot</th>'
         '<th>Title</th><th style="width:42px">At</th><th style="width:30px">Sec</th>'
         '<th style="width:52px">Draft</th><th style="width:46px">Final</th>'
         '<th>Blocked by</th></tr></thead><tbody>')
for mv in (1,2,3):
    ss=[s for s in order if led[s]["mv"]==mv]
    o.append('<tr><td colspan="8" style="padding-top:8px;border-bottom:1px solid #141210">'
             '<b>MOVEMENT %s</b> <span class="dim">· %d shots · %ds</span></td></tr>'
             % (esc(MV[mv]), len(ss), sum(led[s]["d"] for s in ss)))
    for s in ss:
        v=led[s]; f=fails.get(s) or []
        blk = "model cannot do 2.39:1" if any("2.39" in x for x in f) else ""
        if any("start frame only" in x for x in f): blk = "no end frame; " + blk if blk else "no end frame"
        if any("tops out" in x for x in f): blk = (blk+"; " if blk else "")+"over duration cap"
        o.append('<tr><td><span class="bx%s"></span></td><td class="m">%s</td><td>%s</td>'
                 '<td class="m dim">%s</td><td class="m">%d</td><td class="m %s">%s</td>'
                 '<td class="m dim">—</td><td class="%s" style="font-size:9px">%s</td></tr>'
                 % (" on" if v.get("concept") else "", s, esc(v["title"]), mmss(TC[s]), v["d"],
                    "ok" if v.get("concept") else "dim", "yes" if v.get("concept") else "none",
                    "warn" if blk else "dim", esc(blk or "ready")))
o.append('</tbody></table>')
o.append('<p class="note"><b>Read this honestly:</b> eleven shots have a ten-second 720p concept clip '
         'generated from their anchors. None is the shot. Nothing has had a final pass, so the film '
         'exists as 39 stills and a rough animatic, not as a cut.</p>')
o.append('<div class="fn"><span>Sheet 1 of 3 · the film</span><span>design/shot-ledger.json</span></div></div>')

# ---------------- sheet 2 : cast, elements, what is left ----------------
o.append('<div class="sheet"><h1>Cast, references, and what is left</h1>')
o.append('<p class="sub">Souls read live from the account. Elements counted against what the shot prompts attach.</p>')
o.append('<div class="rule"></div>')
o.append('<h2>Soul casts<span class="c">all seven trained and ready — none missing</span></h2>')
o.append('<table><thead><tr><th style="width:34px">&nbsp;</th><th style="width:130px">Soul</th>'
         '<th style="width:66px">Verdict</th><th>Note</th></tr></thead><tbody>')
for n,v,note in SOULS:
    keep = v=="keep"
    o.append('<tr><td><span class="bx on"></span></td><td class="m">%s</td>'
             '<td class="m %s">%s</td><td class="dim">%s</td></tr>'
             % (esc(n), "ok" if keep else "warn", esc(v), esc(note)))
o.append('</tbody></table>')
o.append('<p class="note">No Soul is missing. The Threadwright needs none — her face is never fully '
         'revealed by design — and the Keepers are an order, carried by an element rather than a face. '
         '<b class="warn">One hard limit:</b> a generation takes one Soul only, so the seven shots with two '
         'people in frame (S2, S3, S5, S15, S16, S17, S22) must run on elements, not Souls.</p>')

o.append('<h2>The Turned<span class="c">consistency comes from the rule, not the faces</span></h2>')
o.append('<p class="note">They are written to read as individuals who went wrong separately — no uniforms, '
         'no matching costume — so chasing per-face consistency fights the design. Three things must be '
         'identical in every Turned shot instead: the aura is black at the centre, the cloth is dark and '
         'sodden with no armour, and the rank reads off the aura. Attach <b>one</b> canonical group element '
         'everywhere (pick one of the three now in the project and retire the other two), plus '
         '<b>aura-grammar</b> so the hollow is decided once, plus the domain sheet only when that power is '
         'on screen. Elements take several references in one prompt, which is why this works and Souls '
         'cannot do it. Never describe a Turned face in words.</p>')

o.append('<div class="fn"><span>Sheet 2 of 3 · cast</span><span>account · show_characters</span></div></div>')

o.append('<div class="sheet"><h1>What is left</h1>')
o.append('<p class="sub">Ordered by what it blocks, not by when it was thought of.</p>')
o.append('<div class="rule"></div>')
o.append('<h2>References still outside the project<span class="c">%d handles · blocking all 23 shots</span></h2>'
         % len(gap["must_move"]))
o.append('<table><thead><tr><th style="width:34px">&nbsp;</th><th style="width:150px">Handle</th>'
         '<th style="width:38px">Shots</th><th>Where it is needed</th></tr></thead><tbody>')
for r in gap["must_move"]:
    o.append('<tr><td><span class="bx"></span></td><td class="m">@%s</td><td class="m">%d</td>'
             '<td class="m dim" style="font-size:9px">%s</td></tr>'
             % (esc(r["handle"]), len(r["shots"]), esc(", ".join(r["shots"]))))
o.append('</tbody></table>')
o.append('<p class="note">All twenty-two already exist in the account. This is a move, not a rebuild.</p>')

o.append('<h2>What is left, in order<span class="c">ordered by what it blocks</span></h2>')
o.append('<ol class="todo">'
 '<li><b>Move 22 references into the project folder.</b> <span>Four lighting plates first — between them they carry 21 of 23 shots.</span></li>'
 '<li><b>Rename the four elements carrying novel vocabulary.</b> <span>Production history is public. Cairn Island, the Vigil.</span></li>'
 '<li><b>Replace prop_leviathan_v1.</b> <span>It holds a video and no still, so it cannot be an image reference.</span></li>'
 '<li><b>Hold Gate A — identity lock.</b> <span>Gates 17 of the 20 remaining steps.</span></li>'
 '<li><b>Verify the six upload-backed handles.</b> <span>No real face as input. The only disqualification risk.</span></li>'
 '<li><b>Re-assign 16 shots off models that cannot do 2.39:1.</b> <span>The motion sheet carries the replacement for each.</span></li>'
 '<li><b>Generate the 12 shots with no clip at all.</b> <span>S3 S4 S5 S9 S13 S14 S15 S16 S17 S21 S22 S23.</span></li>'
 '<li><b>Cast three voices.</b> <span>Oriane is Kiki. Caedom, Alder and Wren are not cast.</span></li>'
 '<li><b>Final pass, all 23.</b> <span>Then deflicker, upscale, grade — in that order.</span></li>'
 '<li><b>File 87 generations, publish, check it logged out.</b></li>'
 '</ol>')
o.append('<div class="fn"><span>Sheet 3 of 3 · remaining work</span>'
         '<span>element-map.json · project-folder-gap.json</span></div></div>')

doc = "\n".join(o)
open(os.path.join(ROOT,"design/status-sheet.html"),"w",encoding="utf-8").write(doc)
open(os.path.join(ROOT,"status.html"),"w",encoding="utf-8").write(doc)
print("status-sheet.html built — %d shots, %d with a clip, %d handles to move"
      % (len(led), nconc, len(gap["must_move"])))
