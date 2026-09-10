#!/usr/bin/env python3
"""Build frame-index.html — every anchor frame in film order, with its image.

The tiles point straight at the account's CDN, so the page shows real frames in
a browser that is signed in and identity cards in one that is not. It is built
from anchor-plan.json rather than from the account, which means a frame missing
here is a frame the film does not plan for, not a frame that failed to upload.
"""
import json, os, html, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
plan = json.load(open(os.path.join(ROOT, "design/anchor-plan.json"), encoding="utf-8"))
led = json.load(open(os.path.join(ROOT, "design/shot-ledger.json"), encoding="utf-8"))["shots"]

MV = {1: ("I", "The Sun", "#E0A33A"),
      2: ("II", "The Ocean", "#5C8CA8"),
      3: ("III", "The Island", "#D9694E")}

frames = plan["frames"]
by_mv = collections.OrderedDict()
for f in frames:
    by_mv.setdefault(f["mv"], []).append(f)

def esc(s): return html.escape(str(s or ""))

out = []
out.append("""<title>Anchor Frames</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--ground:#0B0A09;--surface:#141210;--edge:#252019;--ink:#EDE6DA;--muted:#8C8477;--dim:#5F594F;
 --serif:ui-serif,Georgia,"Iowan Old Style","Times New Roman",serif;
 --sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
 --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.55}
.wrap{max-width:1180px;margin:0 auto;padding:52px 24px 90px}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim);margin:0 0 14px}
h1{font-family:var(--serif);font-weight:400;font-size:clamp(28px,4.4vw,42px);margin:0 0 14px;letter-spacing:-.01em}
.standfirst{color:var(--muted);max-width:62ch;margin:0 0 8px}
header{border-bottom:1px solid var(--edge);padding-bottom:26px;margin-bottom:40px}
h2{font-family:var(--serif);font-weight:400;font-size:23px;margin:44px 0 4px;display:flex;align-items:baseline;gap:12px}
h2 .rn{font-family:var(--mono);font-size:11px;letter-spacing:.16em}
h2 .ct{font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.1em;margin-left:auto}
.mvnote{color:var(--dim);font-size:13px;margin:0 0 20px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}
.tile{border:1px solid var(--edge);border-radius:3px;background:var(--surface);overflow:hidden;display:flex;flex-direction:column}
.shot{position:relative;aspect-ratio:21/9;background:#0d0c0b;display:block}
.shot img{width:100%;height:100%;object-fit:cover;display:block}
.card{position:absolute;inset:0;display:none;flex-direction:column;justify-content:center;padding:14px 16px;gap:5px}
.card.on{display:flex}
.card .fid{font-family:var(--mono);font-size:22px;color:var(--ink);letter-spacing:-.02em}
.card .hs{font-family:var(--mono);font-size:10px;color:var(--dim);line-height:1.5;word-break:break-all}
.meta{padding:11px 14px 13px;border-top:1px solid var(--edge)}
.row1{display:flex;align-items:baseline;gap:9px;margin-bottom:5px}
.fno{font-family:var(--mono);font-size:14px;letter-spacing:-.02em}
.srv{font-family:var(--mono);font-size:10px;color:var(--dim);letter-spacing:.1em;text-transform:uppercase}
.ttl{font-size:13px;color:var(--muted);margin:0 0 7px;line-height:1.4}
.hnd{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px}
.hnd span{font-family:var(--mono);font-size:9.5px;color:var(--dim);border:1px solid var(--edge);border-radius:2px;padding:2px 5px}
a.jl{font-family:var(--mono);font-size:9.5px;color:var(--muted);text-decoration:none;border-bottom:1px solid var(--edge);word-break:break-all}
a.jl:hover{color:var(--ink)}
.note{border:1px solid var(--edge);border-left:2px solid #E0A33A;border-radius:3px;padding:16px 20px;margin:0 0 34px;background:var(--surface)}
.note p{margin:0;color:var(--muted);font-size:14px;max-width:66ch}
footer{border-top:1px solid var(--edge);margin-top:56px;padding-top:18px;color:var(--dim);font-size:12px;font-family:var(--mono)}
</style>
<div class="wrap">
<header>
<p class="eyebrow">Matter of Light &middot; anchor frames &middot; __N__ in film order</p>
<h1>Every frame the film is built between</h1>
<p class="standfirst">Each shot is a move from one of these to the next. They are listed in film
order, not in the order they were generated, because the order is the point.</p>
</header>
<div class="note"><p><b>If the tiles are grey:</b> the images live behind your Higgsfield account.
Open this page in the browser you are signed in to and they appear. Otherwise each tile still shows
its frame number, the handles attached to it, and a direct link to the file.</p></div>
""".replace("__N__", str(len(frames))))

for mv in sorted(by_mv):
    rn, name, col = MV[mv]
    fs = by_mv[mv]
    out.append('<h2><span class="rn" style="color:%s">MOVEMENT %s</span> %s'
               '<span class="ct">%d frames</span></h2>' % (col, rn, esc(name), len(fs)))
    shots = sorted({f["s"].split()[0] for f in fs}, key=lambda s: int(s[1:]))
    out.append('<p class="mvnote">%s</p>' % esc(" · ".join(shots)))
    out.append('<div class="grid">')
    for f in fs:
        sid = f["s"].split()[0]
        title = led.get(sid, {}).get("title", "")
        hs = "".join('<span>@%s</span>' % esc(x) for x in (f.get("handles") or []))
        hs_plain = esc(", ".join("@" + x for x in (f.get("handles") or [])) or "no handles")
        url = f.get("url", "")
        img = ('<img src="%s" alt="%s" loading="lazy" '
               'onerror="this.style.display=\'none\';'
               'this.parentNode.querySelector(\'.card\').classList.add(\'on\')">'
               % (esc(url), esc(f["f"]))) if url else ""
        card = ('<div class="card%s"><div class="fid">%s</div>'
                '<div class="hs">%s</div></div>'
                % ("" if url else " on", esc(f["f"]), hs_plain))
        out.append(
          '<div class="tile"><div class="shot">%s%s</div><div class="meta">'
          '<div class="row1"><span class="fno">%s</span><span class="srv">%s</span></div>'
          '<p class="ttl">%s</p><div class="hnd">%s</div>'
          '<a class="jl" href="%s" target="_blank" rel="noopener">%s</a>'
          '</div></div>'
          % (img, card, esc(f["f"]), esc(f["s"]), esc(title), hs,
             esc(url or "#"), esc(f.get("job", ""))))
    out.append('</div>')

out.append('<footer>Built from design/anchor-plan.json &middot; rebuild with '
           'design/build-frame-index.py &middot; URLs pulled %s</footer></div>'
           % esc(plan["meta"].get("urls_pulled", "")))

open(os.path.join(ROOT, "frame-index.html"), "w", encoding="utf-8").write("\n".join(out))
print("frame-index.html — %d frames across %d movements" % (len(frames), len(by_mv)))
