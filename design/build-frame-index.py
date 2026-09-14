#!/usr/bin/env python3
"""Build frame-index.html — the film shot by shot, with the frames it runs between.

Each of the 23 shots gets its start and end anchor, the camera move, a primary
generation method, one backup that is a genuinely different route rather than a
second model, and the seam into the next shot.

Model capabilities below were read from the platform on 2026-09-10 rather than
remembered, which is how the aspect-ratio audit at the top of the page is built:
several shots are currently assigned to models that cannot deliver 2.39:1.
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda p: json.load(open(os.path.join(ROOT, p), encoding="utf-8"))
plan, led = R("design/anchor-plan.json"), R("design/shot-ledger.json")["shots"]
bible = open(os.path.join(ROOT, "director-bible.html"), encoding="utf-8").read()

# ---- shot data straight out of the bible ------------------------------------
seg = bible[bible.find('{id:"S1",mv:1'): bible.find("\n]", bible.find('{id:"S23"'))]
SHOTS = {}
for m in re.finditer(r'\{id:"(S\d+)",mv:(\d+),d:(\d+),t:"(.*?)",cam:"(.*?)",model:"(.*?)"', seg):
    sid = m.group(1)
    nxt = seg.find('{id:"S', m.end())
    body = seg[m.end(): nxt if nxt > 0 else len(seg)]
    sm = re.search(r'seam:"(.*?)",\n', body)
    SHOTS[sid] = dict(mv=int(m.group(2)), d=int(m.group(3)), t=m.group(4),
                      cam=m.group(5), assigned=m.group(6), seam=sm.group(1) if sm else "")

# ---- capabilities, read from the platform 2026-09-10 ------------------------
CAP = {
 "cinematic_studio_3_0":      dict(two=True,  ar=True,  lo=4, hi=15, res="4K"),
 "seedance_2_5":              dict(two=True,  ar=True,  lo=4, hi=30, res="1080p"),
 "seedance_2_0":              dict(two=True,  ar=True,  lo=4, hi=15, res="4K"),
 "flux_3_video":              dict(two=True,  ar=True,  lo=5, hi=20, res="1080p"),
 "minimax_h3":                dict(two=True,  ar=True,  lo=4, hi=15, res="2K"),
 "cinematic_studio_video_v2": dict(two=True,  ar=False, lo=3, hi=12, res="—"),
 "kling3_0":                  dict(two=True,  ar=False, lo=3, hi=15, res="4K"),
 "kling2_6":                  dict(two=False, ar=False, lo=5, hi=10, res="—"),
 "minimax_hailuo":            dict(two=True,  ar=False, lo=6, hi=10, res="1080p"),
 "wan3_0":                    dict(two=True,  ar=False, lo=2, hi=30, res="1080p"),
 "veo3_1":                    dict(two=False, ar=False, lo=4, hi=8,  res="—"),
 "veo3_1_lite":               dict(two=False, ar=False, lo=4, hi=8,  res="—"),
}
MOVING = re.compile(r"crane|dolly|track|travel|drift|swing|orbit|push|pull|arc|aerial|rise", re.I)
LOCKED = re.compile(r"lock|static|held|unbroken|does not move", re.I)

GENRE = {1: {"S1": "epic", "S2": "epic", "S3": "drama", "S4": "drama", "S5": "drama"},
         2: {"S13": "epic"},
         3: {"S17": "epic", "S18": "epic", "S19": "epic", "S20": "epic"}}

def genre(sid, mv):
    return GENRE.get(mv, {}).get(sid, "action" if mv == 2 else "drama")

def methods(sid, s):
    """Primary, then one backup on a different route."""
    d, mv, cam = s["d"], s["mv"], s["cam"]
    g = genre(sid, mv)
    moving, locked = bool(MOVING.search(cam)), bool(LOCKED.search(cam))
    if d <= 15:
        p = dict(model="cinematic_studio_3_0", how="two-frame move",
                 set="21:9 · 1080p draft, 4K at finish · genre %s · %ds" % (g, d),
                 body="Start frame and end frame both attached, prompt describes only the move "
                      "between them. It is the one model that gives you 2.39:1, both frames, this "
                      "duration and a 4K finish in the same call.")
    else:
        p = dict(model="seedance_2_5", how="two-frame move",
                 set="21:9 · 1080p · %ds · generate_audio off" % d,
                 body="Over fifteen seconds, so Cinema Studio 3.0 cannot hold it in one generation. "
                      "Seedance 2.5 runs to thirty and still takes both frames at 2.39:1.")
    if moving and (mv == 2 or sid in ("S17", "S18", "S19", "S20")):
        b = dict(model="hf_mult_motion_control", how="motion transfer · Genjutsu",
                 set="1080p · driving clip + this shot's anchors as image references",
                 body="Generate the swing once on anything — a throwaway clip whose only job is the "
                      "move — then transfer that motion onto these frames. It is how you get a "
                      "repeatable camera arc instead of rolling the dice on the word 'swings'.")
    elif locked:
        b = dict(model="seedance_2_0", how="two-frame move",
                 set="21:9 · 1080p · genre %s · %ds" % (g, min(max(d, 4), 15)),
                 body="A locked frame is the cheapest thing to re-roll, and this model is eligible "
                      "for unlimited generations when an allowance is live. Same two-frame "
                      "discipline, different family, so it fails differently.")
    else:
        b = dict(model="flux_3_video", how="two-frame move",
                 set="2:1 or 21:9 · 1080p · %ds" % min(max(d, 5), 20),
                 body="The only other model offering 2:1 as well as 21:9, so it is the one to reach "
                      "for if the framing wants a hair more height than 2.39:1 gives you.")
    return p, b

def seam_kind(s, nxt):
    t = (s["seam"] or "").lower()
    if "match cut" in t or "match" in t: return ("Match cut", "shared frame — this shot's end anchor IS the next shot's start anchor. Generate once, use twice.")
    if "hard cut" in t: return ("Hard cut", "no generation. Two finished clips butted together, nothing between them.")
    if not nxt: return ("End", "cut to black, then the title card.")
    return ("Shared frame", "chain from the rendered last frame of this clip, never from the still. The still is where the shot was planned; the render is where it actually ended up.")

def audit(sid, s):
    c = CAP.get(s["assigned"].split(" ")[0].split("·")[0].strip())
    if not c: return None
    bad = []
    if not c["ar"]: bad.append("cannot output 2.39:1")
    if not c["two"]: bad.append("takes a start frame only, no end frame")
    if s["d"] > c["hi"]: bad.append("tops out at %ds, this shot is %ds" % (c["hi"], s["d"]))
    return bad or None

order = sorted(SHOTS, key=lambda x: int(x[1:]))
tc, TC = 0, {}
for sid in order:
    TC[sid] = tc; tc += SHOTS[sid]["d"]

FR = {}
for f in plan["frames"]:
    FR.setdefault(f["s"].split()[0], []).append(f)

flags = {sid: audit(sid, SHOTS[sid]) for sid in order}
nflag = sum(1 for v in flags.values() if v)

MV = {1: ("I", "The Sun", "#E0A33A"), 2: ("II", "The Ocean", "#5C8CA8"), 3: ("III", "The Island", "#D9694E")}
def esc(x): return html.escape(str(x or ""))
def mmss(n): return "%d:%02d" % (n // 60, n % 60)

o = ["""<title>The Motion Sheet</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--ground:#0B0A09;--surface:#141210;--sunk:#0F0D0C;--edge:#252019;--ink:#EDE6DA;--muted:#8C8477;
--dim:#5F594F;--gold:#E0A33A;--warn:#D9694E;--ok:#6FA8A0;
--serif:ui-serif,Georgia,"Iowan Old Style","Times New Roman",serif;
--sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.55}
.wrap{max-width:1120px;margin:0 auto;padding:52px 24px 100px}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim);margin:0 0 14px}
h1{font-family:var(--serif);font-weight:400;font-size:clamp(30px,5vw,46px);margin:0 0 14px;letter-spacing:-.01em;text-wrap:balance}
.standfirst{color:var(--muted);max-width:64ch;margin:0}
header{border-bottom:1px solid var(--edge);padding-bottom:26px;margin-bottom:30px}
.note{border:1px solid var(--edge);border-left:2px solid var(--warn);border-radius:3px;padding:17px 21px;margin:0 0 16px;background:var(--surface)}
.note.ok{border-left-color:var(--ok)}
.note h3{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--warn);margin:0 0 8px;font-weight:400}
.note.ok h3{color:var(--ok)}
.note p{margin:0 0 8px;color:var(--muted);font-size:14px;max-width:70ch}
.note p:last-child{margin:0}
.note b{color:var(--ink)}
.note code{font-family:var(--mono);font-size:12.5px;color:var(--ink)}
h2.mv{font-family:var(--serif);font-weight:400;font-size:25px;margin:50px 0 6px;display:flex;align-items:baseline;gap:13px}
h2.mv .rn{font-family:var(--mono);font-size:11px;letter-spacing:.16em}
h2.mv .ct{font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.1em;margin-left:auto}
.mvnote{color:var(--dim);font-size:13.5px;margin:0 0 22px;max-width:70ch}
.shot{border:1px solid var(--edge);border-radius:3px;background:var(--surface);margin-bottom:20px;overflow:hidden}
.sh{display:flex;flex-wrap:wrap;align-items:baseline;gap:11px;padding:16px 22px 12px}
.sid{font-family:var(--mono);font-size:13px;color:var(--gold);letter-spacing:.06em}
.stt{font-family:var(--serif);font-size:21px;letter-spacing:-.01em}
.stc{font-family:var(--mono);font-size:11px;color:var(--dim);margin-left:auto;font-variant-numeric:tabular-nums}
.cam{padding:0 22px 15px;color:var(--muted);font-size:14px;max-width:78ch;margin:0}
.frames{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:12px;padding:0 22px 18px}
.fr{border:1px solid var(--edge);border-radius:2px;overflow:hidden;background:var(--sunk)}
.fr .im{aspect-ratio:21/9;position:relative;display:block}
.fr img{width:100%;height:100%;object-fit:cover;display:block}
.fr .cd{position:absolute;inset:0;display:none;flex-direction:column;justify-content:center;align-items:center;gap:4px}
.fr .cd.on{display:flex}
.fr .cd b{font-family:var(--mono);font-size:19px;color:var(--muted)}
.fr .cd i{font-family:var(--mono);font-size:9.5px;color:var(--dim);font-style:normal}
.fr .lb{display:flex;justify-content:space-between;gap:8px;padding:7px 10px;border-top:1px solid var(--edge)}
.fr .lb span{font-family:var(--mono);font-size:10px;color:var(--dim);letter-spacing:.08em}
.fr .lb a{font-family:var(--mono);font-size:10px;color:var(--muted);text-decoration:none}
.fr .lb a:hover{color:var(--ink)}
.arrow{font-family:var(--mono);color:var(--dim);font-size:15px}
.m2{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));border-top:1px solid var(--edge)}
.m{padding:16px 22px;border-right:1px solid var(--edge)}
.m:last-child{border-right:0}
.mk{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;margin:0 0 8px}
.m.p .mk{color:var(--gold)} .m.b .mk{color:var(--dim)}
.mn{font-family:var(--mono);font-size:14px;color:var(--ink);margin:0 0 3px;word-break:break-all}
.mh{font-size:12.5px;color:var(--muted);margin:0 0 6px}
.ms{font-family:var(--mono);font-size:11px;color:var(--dim);margin:0 0 9px;letter-spacing:.02em}
.m p.mb{margin:0;font-size:13.5px;color:var(--muted);max-width:52ch}
.seam{display:flex;flex-wrap:wrap;gap:11px;align-items:baseline;padding:13px 22px;border-top:1px solid var(--edge);background:var(--sunk)}
.seam .k{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ok)}
.seam p{margin:0;font-size:13.5px;color:var(--muted);max-width:74ch}
.flag{margin:0 22px 16px;border:1px solid var(--warn);border-radius:2px;padding:10px 14px}
.flag b{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--warn);display:block;margin-bottom:5px}
.flag p{margin:0;font-size:13px;color:var(--muted)}
footer{border-top:1px solid var(--edge);margin-top:58px;padding-top:19px;color:var(--dim);font-size:12px;font-family:var(--mono)}
</style>
<div class="wrap">
<header>
<p class="eyebrow">Matter of Light &middot; motion sheet &middot; 23 shots &middot; 5:00 &middot; 2.39:1</p>
<h1>Every shot, the two frames it runs between, and how to make the move</h1>
<p class="standfirst">One primary method per shot and one backup on a different route, so a refusal
never costs you the day. Model limits below were read off the platform, not remembered.</p>
</header>"""]

o.append('<div class="note"><h3>Before you generate anything &mdash; %d shots are on a model that cannot do the job</h3>'
 '<p>The film is 2.39:1. Six of the models the shot list currently names cannot output it at all: '
 '<code>wan3_0</code>, <code>veo3_1</code>, <code>kling3_0</code>, <code>kling2_6</code>, '
 '<code>cinematic_studio_video_v2</code> and <code>minimax_hailuo</code>. They silently fall back to 16:9.</p>'
 '<p><b>The worst of them is on the ending.</b> <code>veo3_1</code> is assigned to S22 and S9. It takes a '
 'start frame only with no end frame, it caps at eight seconds against S22&rsquo;s fourteen, and it does not '
 'offer 2.39:1. Three separate failures on the film&rsquo;s last held close-up.</p>'
 '<p>Every primary below is picked to clear all three bars at once. Follow them and the audit closes.</p></div>'
 % nflag)

o.append('<div class="note ok"><h3>Camera swings, specifically</h3>'
 '<p>Do not reach for the preset library. All sixty-odd presets are consumer templates built around an '
 'uploaded selfie &mdash; K-pop fansign, paparazzi walk, action figure &mdash; and several take a real face as '
 'input, which the festival rules forbid outright.</p>'
 '<p>Swings come from two places instead. <b>Write the move as the whole prompt</b> on a two-frame '
 'generation, so the model is interpolating a camera path rather than inventing a scene. And where the '
 'swing has to be repeatable or exact, <b>transfer it</b>: <code>hf_mult_motion_control</code> takes a '
 'driving clip and puts its motion onto your frames. Generate the arc once on a throwaway, then reuse it '
 'across every shot in the movement that needs the same energy.</p></div>')

for mv in (1, 2, 3):
    rn, nm, col = MV[mv]
    ss = [s for s in order if SHOTS[s]["mv"] == mv]
    secs = sum(SHOTS[s]["d"] for s in ss)
    o.append('<h2 class="mv"><span class="rn" style="color:%s">MOVEMENT %s</span> %s'
             '<span class="ct">%d shots &middot; %ds</span></h2>' % (col, rn, esc(nm), len(ss), secs))
    o.append('<p class="mvnote">%s</p>' % esc(
        {1: "A sustained oner. The first thirty-four seconds contain no cut at all, so every seam here is a shared frame and none of them is a cut.",
         2: "Continuous travelling motion. This is where the camera swings live and where the two perspective reassignments happen.",
         3: "Locked-off witness. The camera stops moving. Movement is inside the frame, not of it."}[mv]))
    for i, sid in enumerate(ss):
        s = SHOTS[sid]
        fs = sorted(FR.get(sid, []), key=lambda f: f["i"])
        p, b = methods(sid, s)
        nxt = order[order.index(sid) + 1] if order.index(sid) + 1 < len(order) else None
        kind, ktext = seam_kind(s, nxt)
        o.append('<div class="shot">')
        o.append('<div class="sh"><span class="sid">%s</span><span class="stt">%s</span>'
                 '<span class="stc">%s &middot; %ds</span></div>' %
                 (sid, esc(s["t"]), mmss(TC[sid]), s["d"]))
        o.append('<p class="cam">%s</p>' % esc(s["cam"]).replace("&amp;mdash;", "&mdash;"))
        if len(fs) >= 2:
            a, z = fs[0], fs[-1]
            cells = []
            for f, role in ((a, "START"), (z, "END")):
                hs = ", ".join("@" + x for x in (f.get("handles") or [])) or "no handles"
                u = f.get("url", "")
                cells.append(
                  '<div class="fr"><div class="im">'
                  '<img src="%s" alt="%s" loading="lazy" onerror="this.style.display=\'none\';'
                  'this.parentNode.querySelector(\'.cd\').classList.add(\'on\')">'
                  '<div class="cd"><b>%s</b><i>%s</i></div></div>'
                  '<div class="lb"><span>%s &middot; %s</span><a href="%s" target="_blank" rel="noopener">open</a></div></div>'
                  % (esc(u), esc(f["f"]), esc(f["f"]), esc(hs), role, esc(f["f"]), esc(u or "#")))
            o.append('<div class="frames">%s<span class="arrow">&rarr;</span>%s</div>' % (cells[0], cells[1]))
        if flags[sid]:
            o.append('<div class="flag"><b>currently assigned %s</b><p>%s. Use the primary below instead.</p></div>'
                     % (esc(s["assigned"].split("·")[0].strip()), esc("; ".join(flags[sid]))))
        o.append('<div class="m2">')
        for cls, label, mm in (("p", "Primary", p), ("b", "Backup", b)):
            o.append('<div class="m %s"><p class="mk">%s</p><p class="mn">%s</p>'
                     '<p class="mh">%s</p><p class="ms">%s</p><p class="mb">%s</p></div>'
                     % (cls, label, esc(mm["model"]), esc(mm["how"]), esc(mm["set"]), esc(mm["body"])))
        o.append('</div>')
        o.append('<div class="seam"><span class="k">%s%s</span><p>%s %s</p></div>'
                 % (esc(kind), (" &rarr; " + nxt) if nxt else "", esc(ktext),
                    esc(s["seam"]).replace("&amp;mdash;", "&mdash;")))
        o.append('</div>')

o.append('<footer>Built from anchor-plan.json and the bible&rsquo;s shot list &middot; model limits read from the '
         'platform 2026-09-10 &middot; rebuild with design/build-frame-index.py</footer></div>')

open(os.path.join(ROOT, "frame-index.html"), "w", encoding="utf-8").write("\n".join(o))
print("frame-index.html — 23 shots, %d with a model flag" % nflag)
