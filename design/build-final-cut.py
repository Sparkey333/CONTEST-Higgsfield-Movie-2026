#!/usr/bin/env python3
"""Render the Final Cut chapter into director-bible.html from two files:
  design/final-cut.data.json   — assembled by assemble-final-cut.py (plans, post-deadline work, favourites, uploads, analyses)
  design/final-cut.notes.json  — authored: the scenes as analysed, the diff, feel, grade, the three-changes check, lessons
Idempotent: the section lives between FINALCUT markers; the nav item, the lessons and the masthead
runtime are patched in place.   python3 design/build-final-cut.py
"""
import json, re, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
def esc(t): return html.escape(str(t), quote=False)
D = json.load(open(ROOT / "design" / "final-cut.data.json")); N = json.load(open(ROOT / "design" / "final-cut.notes.json"))
B = ROOT / "director-bible.html"; t = B.read_text()

def fmt(s):
    s = int(round(s)); return str(s // 60) + ":" + str(s % 60).zfill(2)
def seg(it):
    tip = esc(it.get("id", "")) + " · " + esc(it.get("dur", "")) + "s" + ((" · " + esc(it["title"])) if it.get("title") else "")
    return '<div class="seg' + (" ghost" if it.get("ghost") else "") + '" data-mv="' + str(it.get("mv", 0)) + '" style="flex:' + str(max(it.get("dur") or 1, 1)) + ' 0 0"><span class="seg-tip">' + tip + '</span></div>'
def ribbon(items, thin=False):
    return '<div class="ribbon' + (" thin" if thin else "") + '">' + "".join(seg(i) for i in items) + '</div>'
MV = {"S1":1,"S2":1,"S3":1,"S4":1,"S5":1,"NEW-3":1,"S23":1,"END":1,"S15a":3,"S15":3,"S16":3,"S17":3,"S18":3,"S19":3,"S20":3,"NEW-2":3,"S21":3,"S22":3}
def mvof(sid): return MV.get(sid, 2)

# ---------- 1. ribbons ----------
plans = D["plans"]
bib = [dict(id=s["id"], dur=s["dur"], mv=s["mv"]) for s in plans["bible"]["shots"]]
brd = [dict(id=c["id"], dur=c["dur"], mv=c["mv"], title=c["title"], ghost=c["status"] == "unshot") for c in plans["shot_board"]["cards"]]
scenes = N.get("scenes", [])
cut = [dict(id=sc.get("shot") or "?", dur=sc["t1"] - sc["t0"], mv=mvof(sc.get("shot") or ""), title=(sc.get("desc") or "")[:60], ghost=not sc.get("shot")) for sc in scenes]
cut_total = N.get("final_runtime_s") or (scenes[-1]["t1"] if scenes else 0)
cut_label = (fmt(cut_total) + " · " + str(len(cut)) + " scenes") if cut else "pending"
cut_rib = ribbon(cut) if cut else '<div class="ribbon thin"><div class="seg ghost" style="flex:1 0 0"></div></div>'
rib = ('<div class="ribbon-block">'
       '<div class="ribbon-row"><div class="ribbon-label"><span class="lt">The bible · 23 shots · planned Aug 29</span><span class="lr">' + fmt(plans["bible"]["total"]) + '</span></div>' + ribbon(bib, True) + '</div>'
       '<div class="ribbon-row"><div class="ribbon-label"><span class="lt">The shot board · 27 cards · Sep 14, 22:53 UTC — the scene-clip artefact the cut was made from</span><span class="lr">' + fmt(plans["shot_board"]["total"]) + ' · grey = not yet shot</span></div>' + ribbon(brd, True) + '</div>'
       '<div class="ribbon-row"><div class="ribbon-label"><span class="lt">The final cut · as analysed scene by scene</span><span class="lr">' + cut_label + '</span></div>' + cut_rib + '</div>'
       '<div class="legend"><span><i class="dot" style="background:var(--gold)"></i> I · the Sun</span><span><i class="dot" style="background:var(--void)"></i> II · the Ocean</span><span><i class="dot" style="background:var(--coral)"></i> III · the Island</span><span><i class="dot" style="background:var(--ink-3);opacity:.42"></i> planned but unshot, or unattributed</span></div></div>')

# ---------- 2. scenes ----------
def take_em(s): return (' <em>' + esc(s["take"]) + '</em>') if s.get("take") else ""
def sc_row(s):
    return ('<tr><td class="num">' + fmt(s["t0"]) + '–' + fmt(s["t1"]) + '</td><td class="num">' + str(int(round(s["t1"] - s["t0"]))) + 's</td><td class="name">' + esc(s.get("shot") or "—") + take_em(s) + '</td><td>' + esc(s.get("desc", "")) + '</td><td>' + esc(s.get("note", "")) + '</td></tr>')
scenes_html = ('<div class="tbl-scroll"><table style="min-width:900px"><thead><tr><th>Time</th><th>Len</th><th>Shot · take</th><th>What is on screen (the analyser&rsquo;s read, checked against the takes)</th><th>Against the board</th></tr></thead><tbody>' + "".join(sc_row(s) for s in scenes) + '</tbody></table></div>') if scenes else ('<div class="verdict" style="border-style:dashed"><b>The scene-by-scene read is pending.</b> ' + esc(N.get("pending_note", "")) + '</div>')

# ---------- 3. the diff ----------
def d_row(d):
    return ('<tr><td class="name">' + esc(d["shot"]) + '<em>' + esc(d.get("kind", "")) + '</em></td><td>' + esc(d.get("board", "")) + '</td><td>' + esc(d.get("cut", "")) + '</td><td>' + esc(d.get("priced", "")) + '</td><td>' + esc(d.get("why", "")) + '</td></tr>')
diff_html = ('<div class="tbl-scroll"><table style="min-width:900px"><thead><tr><th>Shot</th><th>On the board</th><th>In the cut</th><th>Priced as</th><th>What it says</th></tr></thead><tbody>' + "".join(d_row(d) for d in N.get("diff", [])) + '</tbody></table></div>') if N.get("diff") else ""

# ---------- 4. post-deadline work ----------
def w_row(w):
    fav = ' <span class="badge key">♥</span>' if w["favourite"] else ""
    return ('<tr><td class="num">' + esc(w["at"][5:16]) + '</td><td class="name">' + esc(w["id8"]) + fav + '</td><td>' + esc(w["label"]) + '</td><td class="num">' + esc(w.get("dur") or "—") + 's · ' + esc(w.get("res") or "—") + '</td><td>' + esc(", ".join(w["sources"]) or "text only") + '</td></tr>')
work_html = '<div class="tbl-scroll"><table style="min-width:820px"><thead><tr><th>When (UTC)</th><th>Job</th><th>What it was</th><th>Length</th><th>Made from</th></tr></thead><tbody>' + "".join(w_row(w) for w in D["post_deadline_work"]) + '</tbody></table></div>'

# ---------- 5. favourites vs picks ----------
def f_row(f):
    cell = '<span class="yes">favourited</span>' if f["pick_favourited"] else ('<span class="no">not favourited</span>' if f["pick"] else '<span class="no">no pick</span>')
    favs = ", ".join(x["id8"] + " (" + str(x["dur"]) + "s)" for x in f["favourites"]) or "—"
    return ('<tr><td class="name">' + esc(f["shot"]) + '<em>' + esc(f["title"][:34]) + '</em></td><td class="num">' + esc(f["pick"] or "—") + '</td><td>' + cell + '</td><td>' + esc(favs) + '</td></tr>')
fav_html = '<div class="tbl-scroll"><table style="min-width:760px"><thead><tr><th>Shot</th><th>Board pick</th><th>The cut&rsquo;s ♥</th><th>Favourited takes</th></tr></thead><tbody>' + "".join(f_row(f) for f in D["favourites"]) + '</tbody></table></div>'

# ---------- 6. authored blocks ----------
def cards(items):
    return '<div class="grid g3">' + "".join('<div class="card' + (" pick" if it.get("pick") else "") + '"><span class="tag">' + esc(it.get("tag", "")) + '</span><h3>' + esc(it["t"]) + '</h3><p>' + esc(it["p"]) + '</p></div>' for it in items) + '</div>'
feel_html = cards(N["feel"]) if N.get("feel") else ""
grade_html = cards(N["grade"]) if N.get("grade") else ""
chk_html = ('<div class="rules">' + "".join('<div class="rule-item"><div class="rk">' + esc(c["t"]) + '<em>' + esc(c.get("status", "")) + '</em></div><div class="rv">' + esc(c["p"]) + '</div></div>' for c in N["three_changes"]) + '</div>') if N.get("three_changes") else ""
verdict = ('<div class="verdict" style="margin-top:22px">' + N["verdict"] + '</div>') if N.get("verdict") else ""
ups = "".join('<tr><td class="name">' + esc(u["id"][:8]) + '</td><td>' + esc(u["role"]) + '</td><td class="num">' + esc(u["uploaded"]) + '</td><td class="num">' + esc(u["in_project"]) + '</td></tr>' for u in D["uploads"])
an = "".join('<tr><td class="name">' + esc(a["id"][:8]) + '</td><td>on ' + esc(a["on"]) + '</td><td>' + esc(a.get("status", "")) + '</td></tr>' for a in D["analyses"])
def h3(x): return '<h3 style="font-size:22px;margin:38px 0 10px">' + x + '</h3>'
def note(x): return '<p style="font-size:14.5px;color:var(--ink-2);max-width:78ch;margin-bottom:12px">' + x + '</p>'

section = ('<!-- FINALCUT-START -->\n<section id="finalcut" data-ch="film"><div class="wrap">\n'
           '<style>.le-c.cut{color:var(--mv3)} #finalcut .ribbon .seg.ghost{background:var(--ink-3);opacity:.42} #finalcut table td em{display:block;font-family:var(--mono);font-style:normal;font-size:10.5px;color:var(--ink-3);font-weight:400;margin-top:3px}</style>\n'
           '  <div class="sec-head"><span class="eyebrow">After delivery · read ' + esc(D["generated"]) + '</span><h2>The final cut &mdash; what the edit changed, and what it taught</h2><p>' + N.get("intro", "") + '</p></div>\n'
           + rib + '\n' + h3("Scene by scene") + scenes_html
           + ((h3("The diff against the board") + diff_html) if diff_html else "")
           + ((h3("The feel") + feel_html) if feel_html else "")
           + ((h3("The grade &mdash; how to read it, and how to grade the next one") + grade_html) if grade_html else "")
           + ((h3("The three changes, checked") + chk_html) if chk_html else "")
           + h3("What was made after the board closed") + note(N.get("work_note", "")) + work_html
           + h3("The cut&rsquo;s own record &mdash; favourites against the board&rsquo;s picks") + note(N.get("fav_note", "")) + fav_html
           + h3("The files") + '<div class="tbl-scroll"><table style="min-width:700px"><thead><tr><th>Upload</th><th>Role</th><th>Uploaded</th><th>In the project</th></tr></thead><tbody>' + ups + '</tbody></table></div>'
           + '<div class="tbl-scroll" style="margin-top:10px"><table style="min-width:500px"><thead><tr><th>Analysis</th><th>Input</th><th>Status</th></tr></thead><tbody>' + an + '</tbody></table></div>'
           + verdict + '\n</div></section>\n<!-- FINALCUT-END -->\n')
if "<!-- FINALCUT-START -->" in t:
    t = re.sub(r"<!-- FINALCUT-START -->.*?<!-- FINALCUT-END -->\n", lambda m: section, t, flags=re.S)
else:
    anchor = "<!-- ================= PIPELINE ================= -->"
    assert anchor in t; t = t.replace(anchor, section + anchor, 1)

navline = '      ["voice","Voice","Ten takes, the cast, and the settings that hold them"],'
navadd = navline + '\n      ["finalcut","Final Cut","The delivered film against the board — the diff, the feel, the grade"],'
if '["finalcut","Final Cut"' not in t:
    assert navline in t; t = t.replace(navline, navadd, 1)

t = re.sub(r"/\* FINALCUT-LESSONS \*/.*?/\* /FINALCUT-LESSONS \*/\n", "", t, flags=re.S)
m = re.search(r"const LESSONS=\[.*?\n\];\n", t, flags=re.S); assert m
if N.get("lessons"):
    push = "/* FINALCUT-LESSONS */\nLESSONS.push(" + ",\n".join(json.dumps(dict(c=l["c"], t=l["t"], w=l["w"], r=l["r"]), ensure_ascii=False) for l in N["lessons"]) + ");\n/* /FINALCUT-LESSONS */\n"
    t = t[:m.end()] + push + t[m.end():]

if N.get("final_runtime_s"):
    t = re.sub(r'<div class="stat"><span class="k">Runtime</span><span class="v">[^<]*</span><span class="n">[^<]*</span></div>',
               '<div class="stat"><span class="k">Runtime</span><span class="v">' + fmt(N["final_runtime_s"]) + '</span><span class="n">Planned 5:00 &middot; board 5:43 &middot; delivered</span></div>', t, count=1)
B.write_text(t)
print("final cut section written ·", len(scenes), "scenes ·", len(N.get("diff", [])), "diff rows ·", len(N.get("lessons", [])), "lessons")
