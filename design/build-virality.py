#!/usr/bin/env python3
"""Build virality-read.html from the account's own numbers.

Inputs (scratchpad or design/):
  latest20.json   the 20 newest video generations — prompt, references, result URLs
  virality.json   the Virality Predictor scores per video id
  verdicts.json   which film shot each render is, and what to do about it
  new-shots.md    the paste-ready prompts for the shots that still have to be made
"""
import json, re, sys, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCR = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "design"
gens = json.load(open(SCR / "latest20.json"))
vir = json.load(open(SCR / "virality.json"))
ver = json.load(open(SCR / "verdicts.json"))
newshots = (ROOT / "design" / "new-shots.md").read_text()

def esc(t): return html.escape(t, quote=True)

REF = re.compile(r"@\[[a-z0-9_-]{1,40}\]\([0-9a-f-]{36}\)|<<<[0-9a-f-]{36}>>>|@[a-z][a-z0-9_-]{2,40}", re.I)
def mark(t):
    out, i = [], 0
    for m in REF.finditer(t):
        out.append(esc(t[i:m.start()])); out.append('<b class="ref">'+esc(m.group(0))+'</b>'); i = m.end()
    out.append(esc(t[i:])); return "".join(out)

def spark(vals, w=220, h=44):
    if not vals: return ""
    lo, hi = min(vals), max(vals); rng = (hi-lo) or 1
    pts = []
    for k, v in enumerate(vals):
        x = k/(len(vals)-1 or 1)*(w-4)+2; y = h-2-((v-lo)/rng)*(h-8)
        pts.append(f"{x:.1f},{y:.1f}")
    area = f"M2,{h} L" + " L".join(pts) + f" L{w-2},{h} Z"
    pk = vals.index(hi); px, py = pts[pk].split(",")
    hook = f'<rect x="2" y="0" width="{(3/(len(vals)-1 or 1))*(w-4):.1f}" height="{h}" class="hookwin"/>'
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" class="spark" aria-hidden="true">{hook}'
            f'<path d="{area}" class="area"/><polyline points="{" ".join(pts)}" class="line"/>'
            f'<circle cx="{px}" cy="{py}" r="3" class="pk"/></svg>')

def bar(label, v, lo_better=False):
    v = round(v); cls = "good" if (v>=55 if not lo_better else v<=45) else ("warn" if (v>=42 if not lo_better else v<=58) else "bad")
    return f'<div class="bar"><span class="bl">{label}</span><span class="bt"><i class="{cls}" style="width:{v}%"></i></span><span class="bv">{v}</span></div>'

# pull the fenced prompt blocks out of new-shots.md, keyed by heading
blocks = {}
for m in re.finditer(r"^## (NEW-\d) · \"([^\"]+)\" · \*\*(\d+s)\*\* · audio \*\*(ON|OFF)\*\* · goes between (.+?)\n+```\n(.*?)```", newshots, re.S|re.M):
    blocks[m.group(1)] = dict(title=m.group(2), dur=m.group(3), audio=m.group(4), where=m.group(5).strip(), text=m.group(6).strip())

rows, made = [], sorted(gens, key=lambda g: -g["createdAt"])
for g in made:
    v = vir.get(g["id"]); vd = ver.get(g["id"], {})
    thumb = (g.get("results") or {}).get("thumbnailUrl", ""); mp4 = (g.get("results") or {}).get("rawUrl", "")
    refs = " ".join(f'<b class="ref">@{esc(r["name"])}</b>' for r in g["refs"])
    verdict = vd.get("verdict", "—"); cls = {"KEEP":"keep","REGENERATE":"regen","REPLACE":"replace","UNSCORED":"muted"}.get(verdict, "muted")
    scores = ""
    if v:
        scores = (f'<div class="scores">{bar("Overall", v["overall"])}{bar("Hook (0–3s)", v["hook"])}{bar("Engagement", v["engagement"])}'
                  f'{bar("Viral", v["viral"])}</div><div class="sp">{spark(v["global"])}<span class="spc">attention by second · peak at {v["peak_second"]}s · hook window shaded</span></div>')
    else:
        scores = f'<p class="muted small">{esc(vd.get("why_unscored","Not scored."))}</p>'
    rows.append(f'''
<article class="gen {cls}" id="g-{g["id"][:8]}">
  <div class="media">{f'<video muted playsinline preload="metadata" poster="{esc(thumb)}" src="{esc(mp4)}" controls></video>' if mp4 else ''}</div>
  <div class="body">
    <header><span class="shot">{esc(vd.get("shot","?"))}</span><h3>{esc(vd.get("title", g["id"][:8]))}</h3>
      <span class="chip {cls}">{esc(verdict)}</span></header>
    <p class="meta">{g["duration"]}s · {esc(str(g["resolution"]))} {g["w"]}×{g["h"]} · {"frames chained" if g["frames"] else "no start/end frames"} · audio {"on" if g["audio"] else "off"} · <code>{g["id"][:8]}</code></p>
    {scores}
    <p class="note">{esc(vd.get("note",""))}</p>
    <p class="refs">{refs}</p>
    <details><summary>Prompt as generated</summary><pre>{mark(g["prompt"].strip())}</pre></details>
  </div>
</article>''')

plan = []
for key in ["NEW-1","NEW-2","NEW-3","NEW-4"]:
    b = blocks.get(key)
    if not b: continue
    plan.append(f'''
<article class="shotcard">
  <header><span class="shot">{key}</span><h3>{esc(b["title"])}</h3><span class="meta">{b["dur"]} · audio {b["audio"]} · {esc(b["where"])}</span></header>
  <pre class="prompt">{mark(b["text"])}</pre>
  <button class="copy" data-copy="{esc(b["text"])}">Copy prompt</button>
</article>''')

scored = [vir[g["id"]] for g in made if g["id"] in vir]
n = len(scored); avg = lambda k: round(sum(s[k] for s in scored)/n) if n else 0
kept = sum(1 for g in made if ver.get(g["id"],{}).get("verdict")=="KEEP")
regen = sum(1 for g in made if ver.get(g["id"],{}).get("verdict") in ("REGENERATE","REPLACE"))

page = f'''<title>Matter of Light · Virality Read</title>
<meta name="description" content="What the last twenty renders are doing to a viewer's attention, and which ones to make again.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,500;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{--bg:#F6F2EC;--sur:#FFFDFA;--ink:#1D1A17;--mute:#6B625A;--line:#E3DBD1;--ref:#B4482C;--gold:#9A7B2E;--jade:#2F7A5E;--coral:#B4482C;--void:#3B3A56;--hook:rgba(154,123,46,.12);
--keep:#2F7A5E;--regen:#B4482C;--replace:#7A2F5E}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#161412;--sur:#1F1C19;--ink:#EDE6DD;--mute:#A79C90;--line:#332E29;--ref:#E2795C;--gold:#D2B05A;--jade:#6FC39E;--coral:#E2795C;--void:#A7A5CC;--hook:rgba(210,176,90,.14);--keep:#6FC39E;--regen:#E2795C;--replace:#D48AB8}}}}
:root[data-theme="dark"]{{--bg:#161412;--sur:#1F1C19;--ink:#EDE6DD;--mute:#A79C90;--line:#332E29;--ref:#E2795C;--gold:#D2B05A;--jade:#6FC39E;--coral:#E2795C;--void:#A7A5CC;--hook:rgba(210,176,90,.14);--keep:#6FC39E;--regen:#E2795C;--replace:#D48AB8}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 "IBM Plex Sans",system-ui,sans-serif;padding-inline:clamp(16px,4vw,48px);padding-block:32px 96px}}
h1,h2,h3{{font-family:Fraunces,Georgia,serif;font-weight:500;letter-spacing:-.01em;text-wrap:balance;margin:0}}
h1{{font-size:clamp(34px,5vw,56px);line-height:1.02;font-variation-settings:"opsz" 144}} h2{{font-size:26px;margin:56px 0 12px}} h3{{font-size:19px}}
.lede{{max-width:64ch;color:var(--mute);font-size:17px}} .eyebrow{{text-transform:uppercase;letter-spacing:.14em;font-size:11px;color:var(--gold);font-weight:600}}
.kpis{{display:flex;flex-wrap:wrap;gap:12px;margin:24px 0 8px}} .kpi{{background:var(--sur);border:1px solid var(--line);border-radius:6px;padding:12px 16px;min-width:140px}}
.kpi b{{display:block;font:500 30px/1 Fraunces,serif;font-variant-numeric:tabular-nums}} .kpi span{{color:var(--mute);font-size:12px}}
.gen{{display:grid;grid-template-columns:minmax(220px,340px) 1fr;gap:20px;background:var(--sur);border:1px solid var(--line);border-left:4px solid var(--line);border-radius:6px;padding:16px;margin:14px 0}}
.gen.keep{{border-left-color:var(--keep)}} .gen.regen{{border-left-color:var(--regen)}} .gen.replace{{border-left-color:var(--replace)}}
.media video{{width:100%;aspect-ratio:21/9;background:#000;border-radius:4px;display:block}}
.gen header{{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}} .shot{{font:500 12px "IBM Plex Mono",monospace;color:var(--gold);letter-spacing:.06em}}
.chip{{margin-left:auto;font:600 11px/1 "IBM Plex Sans",sans-serif;letter-spacing:.1em;padding:6px 9px;border-radius:3px;color:#fff;background:var(--mute)}}
.chip.keep{{background:var(--keep)}} .chip.regen{{background:var(--regen)}} .chip.replace{{background:var(--replace)}}
.meta{{color:var(--mute);font-size:12.5px;margin:4px 0 10px}} code{{font-family:"IBM Plex Mono",monospace;font-size:.92em}}
.scores{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:6px 22px;max-width:640px}}
.bar{{display:grid;grid-template-columns:86px 1fr 30px;align-items:center;gap:8px;font-size:12px}} .bl{{color:var(--mute)}} .bv{{text-align:right;font-variant-numeric:tabular-nums;font-weight:600}}
.bt{{height:8px;background:var(--line);border-radius:4px;overflow:hidden}} .bt i{{display:block;height:100%;border-radius:4px}} .bt .good{{background:var(--jade)}} .bt .warn{{background:var(--gold)}} .bt .bad{{background:var(--coral)}}
.sp{{display:flex;align-items:center;gap:12px;margin:10px 0 4px;flex-wrap:wrap}} .spc{{font-size:11.5px;color:var(--mute)}}
.spark .area{{fill:var(--gold);opacity:.18}} .spark .line{{fill:none;stroke:var(--gold);stroke-width:1.6}} .spark .pk{{fill:var(--coral)}} .spark .hookwin{{fill:var(--hook)}}
.note{{margin:10px 0 6px;max-width:70ch}} .refs{{margin:0 0 6px;line-height:1.9}} .ref{{color:var(--ref);font-weight:500;font-family:"IBM Plex Mono",monospace;font-size:.86em}}
details summary{{cursor:pointer;color:var(--mute);font-size:13px}} pre{{white-space:pre-wrap;font:13px/1.55 "IBM Plex Mono",monospace;background:var(--bg);border:1px solid var(--line);border-radius:4px;padding:12px;margin:8px 0 0;overflow-x:auto}}
.shotcard{{background:var(--sur);border:1px solid var(--line);border-radius:6px;padding:18px;margin:14px 0}} .shotcard header{{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin-bottom:8px}}
.copy{{margin-top:10px;font:600 12px "IBM Plex Sans",sans-serif;letter-spacing:.06em;background:var(--ink);color:var(--bg);border:0;border-radius:4px;padding:9px 14px;cursor:pointer}} .copy:focus-visible{{outline:2px solid var(--gold);outline-offset:2px}}
.muted{{color:var(--mute)}} .small{{font-size:13px}} .rule{{border:0;border-top:1px solid var(--line);margin:40px 0}}
table{{border-collapse:collapse;width:100%;font-size:14px}} th,td{{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}} th{{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:var(--mute)}}
.tw{{overflow-x:auto}} @media (max-width:760px){{.gen{{grid-template-columns:1fr}}}}
@media (prefers-reduced-motion:no-preference){{.gen{{transition:border-color .2s}}}}
</style>
<p class="eyebrow">Matter of Light · 14 Sep · read at 21:40 UTC</p>
<h1>What the last twenty renders do to a viewer</h1>
<p class="lede">Every score here is the platform's own Virality Predictor run on your latest renders, not my opinion of them. The verdicts are mine. The bars are 0–100 normalized proxies; the sparkline is predicted attention second by second, with the three-second hook window shaded.</p>
<div class="kpis">
<div class="kpi"><b>{n}</b><span>of 20 scored (two 16s takes exceed the tool's limit)</span></div>
<div class="kpi"><b>{avg("overall")}</b><span>mean overall</span></div>
<div class="kpi"><b>{avg("hook")}</b><span>mean hook — the weak column</span></div>
<div class="kpi"><b>{avg("engagement")}</b><span>mean engagement</span></div>
<div class="kpi"><b>{kept}</b><span>are the pick for their shot</span></div>
<div class="kpi"><b>5</b><span>things to make, listed below</span></div>
</div>
{ver.get("_summary_html","")}
<h2>The ledger, newest first</h2>
{"".join(rows)}
<hr class="rule">
<h2>Shots that do not exist yet — paste these next</h2>
<p class="lede">Nothing has been generated since the 06:57 UTC pair. All four of these are still to make. Model <code>cinematic_studio_video_4_0</code>, 21:9, 1080p, inside the project.</p>
{"".join(plan)}
<script>
document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',async()=>{{const t=b.dataset.copy;try{{await navigator.clipboard.writeText(t);b.textContent='Copied';}}catch(e){{const ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();try{{document.execCommand('copy');b.textContent='Copied';}}catch(_){{b.textContent='Select and ⌘C';}}ta.remove();}}setTimeout(()=>b.textContent='Copy prompt',1600);}}));
</script>
'''
(ROOT / "virality-read.html").write_text(page)
print("wrote virality-read.html", len(page), "bytes;", n, "scored;", len(plan), "plan cards")
