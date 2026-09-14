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
smap = json.load(open(SCR / "shotmap.json"))
dlg = json.load(open(ROOT / "design" / "dialogue.json"))

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

# ---------- the three changes, priced from the data ----------
MV = lambda shot: 1 if shot in ("S1","S2","S3","S4","S5","S23") else (2 if shot in ("S6","S7","S8","S9","S10","S11","S12","S13","S14") else 3)
rows_s = [(k, v, smap.get(k[:8], {}).get("shot", "?")) for k, v in vir.items()]
N = len(rows_s)
peak_last = sum(1 for k, v, sh in rows_s if v["peak_second"] >= v["dur"])
mean = lambda key, rs: (sum(v[key] for k, v, sh in rs) / len(rs)) if rs else 0
mv2 = [r for r in rows_s if MV(r[2]) == 2]; mv3 = [r for r in rows_s if MV(r[2]) == 3]
aud_low = sum(1 for k, v, sh in rows_s if v["auditory_mean"] < 0.40)
chromas = [vir[k] for k in vir if k[:8] in ("4896c8e3","4bb7a3e9")]; chroma = max(chromas, key=lambda c: c["overall"]) if chromas else None; c_over = sum(c["overall"] for c in chromas)/len(chromas) if chromas else 0
filthy = [vir[k] for k in vir if k[:8] in ("6b0d0fac","38eb40d5","d35da4ef")]
f_over = sum(f["overall"] for f in filthy)/len(filthy) if filthy else 0; f_dmn = sum(f["dmn_mean"] for f in filthy)/len(filthy) if filthy else 0; f_vis = sum(f["visual_mean"] for f in filthy)/len(filthy) if filthy else 0
s1 = dlg["takes"]["lines"].get("S1-CAEDOM", {}); s1t = (s1.get("takes") or [{}])[0]
kl = dlg.get("kept_lines") or []
s1line = next((l.get("text") or l.get("line") for l in kl if isinstance(l, dict) and str(l.get("shot","")).upper()=="S1"), None) if isinstance(kl, list) else None
changes_html = f"""
<h2>Three changes that make it a bigger film — priced from the data, one per judge</h2>
<p class="lede">Sixteen-plus renders through the Predictor, five brain regions each, second by second. Three things fall out of it that are also exactly what Catmull, Papamichael and Anderson each sit on the jury to look for. All three are doable in the hour. Two of them need no generation at all.</p>

<article class="chg"><div class="chg-h"><span class="n">1</span><h3>Meet the brothers before she dies</h3><span class="judge">Catmull · the arc</span></div>
<p><b>The data.</b> Movement III's warm, bright clips average <b>{mean("overall", mv3):.0f}</b> overall against <b>{mean("overall", mv2):.0f}</b> for Movement II's dark ocean, and they hold attention better (mind-wandering {mean("dmn_mean", mv3):.2f} vs {mean("dmn_mean", mv2):.2f}). The cut as built runs two and a half minutes of dark before any warmth, then kills its lead and introduces two strangers. Catmull's whole question is <em>who changes, and do I care when they do</em> — and right now the audience meets Alder ninety seconds before the film asks him to carry the ending.</p>
<p><b>The change.</b> Put the first five seconds of S15 — the brothers at the tide line, take <code>aa65cc3d</code> — immediately before S13. The audience has faces to hold when Oriane goes, and the vortex lands harder for cutting away from warmth. This is the Canvas Boards page's Option B; the Predictor now puts a number on it.</p>
<ol class="apply"><li><b>Zero generations.</b> Same take, used twice: 0–5s early, 5–10s in place after S14.</li><li><b>ffmpeg route:</b> <code>pull-picks.sh</code> already does this — the assembly list carries the split with in/out points.</li><li><b>Resolve route:</b> drop S15 on the timeline, blade at 00:05:00, drag the first half to sit before S13. Keep its own beach ambience under it — it is the only warm sound in the film's middle.</li><li>Cut S13 in hard on the vortex. No dissolve. The contrast is the point.</li></ol></article>

<article class="chg"><div class="chg-h"><span class="n">2</span><h3>Cut on the tail, never the head — and let take selection be the grade</h3><span class="judge">Papamichael · the light and the hold</span></div>
<p><b>The data.</b> <b>{peak_last} of {N}</b> scored clips reach their attention peak on their <em>final</em> second. Not one peaks early. And the clearest A/B in the whole set is one shot, one prompt, one grade decision: the two S22 chroma takes score <b>{" and ".join(str(c["overall"]) for c in sorted(chromas, key=lambda c:-c["overall"]))}</b> — the two highest numbers in the account — and the three "filthy" takes of the same shot average <b>{f_over:.0f}</b>; visual-cortex activation {chroma["visual_mean"] if chroma else 0:.2f} vs {f_vis:.2f}; mind-wandering {chroma["dmn_mean"] if chroma else 0:.2f} vs {f_dmn:.2f}. (The one flat take that scores 55 gets there on its audio, with the visual channel at 0.39 — the picture is still the weak half.) The two murky Oriane blends are the weakest hooks in the account (28, 28). High chroma, extreme contrast, bright shapes on black — the look the bible specifies — is worth roughly {c_over - f_over:.0f} points per shot in this model, and a cinematographer on the jury reads the same thing without a model.</p>
<p><b>The change.</b> Two editing rules and one refusal. Whenever a take is longer than its slot, trim from the <em>head</em>; the end is where the shot pays. Where a chroma take and a flat take exist, use chroma. And do not grade in Resolve tonight.</p>
<ol class="apply"><li><b>Never shorten an ending.</b> The 30s S1, the 20s S3/S4, the 15s S5/S6/S8 — if any has to lose time, it comes off the front.</li><li><b>Picks that are already the grade:</b> S22 <code>4896c8e3</code> (chroma; <code>4bb7a3e9</code> is the equal alternate), S10 on the water-line pair (not the dragon-dead sheet), S12 on the pull-off-the-hide take (not the blends). The board carries these.</li><li><b>No colour pass.</b> A one-hour grade across 23 shots from two lighting worlds produces drift, which is the one thing Papamichael punishes. Selection is the grade. Ship the renders as rendered.</li><li><b>Hold S10, S13, S20 whole.</b> The bible's no-cut rule; the curves say the same thing — attention is still climbing at the last frame of every one of them.</li></ol></article>

<article class="chg"><div class="chg-h"><span class="n">3</span><h3>Give the first three seconds a voice — and if you make one thing, make the mound</h3><span class="judge">Anderson · the hook and the set piece</span></div>
<p><b>The data.</b> The auditory region is the weakest of the five in <b>{aud_low} of {N}</b> clips (mean {mean("auditory_mean", rows_s):.2f} against {mean("visual_mean", rows_s):.2f} for vision) — the generated ambience is not doing much. In the two clips where speech arrives late, the auditory and language regions jump and attention peaks with them (S23 alt: 0.25→0.68 across the clip; S22 chroma: 0.46→0.74). Mean hook is <b>{mean("hook", rows_s):.0f}</b> because the 0–3s window of S1 is silent black. That is right for the film. It is wrong for a screener watching entry four hundred.</p>
<p><b>The change.</b> Fill the hook window with the film's own first line. The opening narration exists — Caedom, take 1, already generated, measured and vast: <code>{esc(s1t.get("job","")[:8])}</code>. Lay it under the black; the crane rises under the voice. {"<em>“"+esc(s1line)+"”</em>" if s1line else ""} Then, if you generate exactly one shot tonight, generate NEW-2 — the mound crushing the ships is the set piece the cut currently skips, and Anderson's seat is the set piece.</p>
<ol class="apply"><li><b>Voice on A2 at 00:00:01:00</b>, under S1's black. File: <a href="{esc(s1t.get("file",""))}">S1-CAEDOM take 1</a> (three more takes in <code>dialogue.json</code> if it reads too slow — take 1 is the spec at speech_rate −12). Upload the WAV into the submission project when you submit; the rule requires every audio file in there.</li><li><b>NEW-2 first, 16s, 1080p, audio on</b> — paste from the board, generate at minute 0 so it renders while you assemble (4–5 min). It goes between S20 and S21. If it doesn't land clean, ship without it; nothing else depends on it.</li><li><b>The public post is not the film.</b> Cut a 15s teaser <em>peak-first</em>: the last 5s of S22 chroma, the last 5s of S20, the last 5s of S13 orbital — the three highest-rated seconds in the account, front-loaded. Watermark and packshot on that too. The film's hook can be quiet by design; the post's does not have to be.</li></ol></article>

<h2>The hour</h2>
<div class="tw"><table><thead><tr><th>Min</th><th>Do</th></tr></thead><tbody>
<tr><td>0–2</td><td>Paste NEW-2 into Cinema Studio and start it. Start <code>bash pull-picks.sh</code>.</td></tr>
<tr><td>2–10</td><td>Clips land in <code>picks/</code>. If ffmpeg is present the assembly with the S15 split writes itself; otherwise open Resolve, drag the folder in order, blade S15 at 5s and move the first half before S13.</td></tr>
<tr><td>10–20</td><td>Voice on A2 at 00:00:01:00. Drop NEW-2 in before S21 if it rendered. Nothing else — no grade, no titles beyond the end card.</td></tr>
<tr><td>20–30</td><td>Export MP4, 2560×1098 or 1920×823, 24fps, H.264 CRF 17. Watch it once at 2× — you are checking for a wrong take, not for taste.</td></tr>
<tr><td>30–42</td><td>Upload into the submission project. Cinema Studio applies watermark and packshot. Upload the S1 WAV into the project too.</td></tr>
<tr><td>42–52</td><td>Public post (YouTube is the safest of the four — no aspect fight). Post <em>and account</em> public. Open the link in a private window to prove it.</td></tr>
<tr><td>52–60</td><td>Submit. Then stop.</td></tr>
</tbody></table></div>
"""
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
.tw{{overflow-x:auto}} .chg{{background:var(--sur);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:6px;padding:18px 20px;margin:14px 0;max-width:86ch}} .chg-h{{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin-bottom:8px}} .chg-h .n{{font:500 26px/1 Fraunces,serif;color:var(--gold)}} .chg-h .judge{{margin-left:auto;font:600 11px "IBM Plex Sans",sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}} .chg p{{margin:6px 0}} .apply{{margin:8px 0 0;padding-left:20px}} .apply li{{margin:4px 0}} @media (max-width:760px){{.gen{{grid-template-columns:1fr}}}}
@media (prefers-reduced-motion:no-preference){{.gen{{transition:border-color .2s}}}}
</style>
<p class="eyebrow">Matter of Light · 14 Sep · read at 21:40 UTC</p>
<h1>What the last twenty renders do to a viewer</h1>
<p class="lede">Every score here is the platform's own Virality Predictor run on your latest renders, not my opinion of them. The verdicts are mine. The bars are 0–100 normalized proxies; the sparkline is predicted attention second by second, with the three-second hook window shaded.</p>
<div class="kpis">
<div class="kpi"><b>{n}</b><span>of 20 scored — every one the tool could take (two 16s takes exceed its limit)</span></div>
<div class="kpi"><b>{avg("overall")}</b><span>mean overall</span></div>
<div class="kpi"><b>{avg("hook")}</b><span>mean hook — the weak column</span></div>
<div class="kpi"><b>{avg("engagement")}</b><span>mean engagement</span></div>
<div class="kpi"><b>{kept}</b><span>are the pick for their shot</span></div>
<div class="kpi"><b>5</b><span>things to make, listed below</span></div>
</div>
{changes_html}
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
