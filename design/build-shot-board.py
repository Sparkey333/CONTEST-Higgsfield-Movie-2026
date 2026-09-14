#!/usr/bin/env python3
"""Build shot-board.html — the cut take by take: one pick per shot, up to three alternates,
every one of them a real render from the account, by URL.

Inputs (scratchpad dir as argv[1]): allvideos.json, shotmap.json, picks.json, virality.json
Repo inputs: design/new-shots.md (the prompts for the shots that do not exist yet)
"""
import json, re, sys, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SCR = pathlib.Path(sys.argv[1])
vids = {v["id"][:8]: v for v in json.load(open(SCR/"allvideos.json"))}
smap = json.load(open(SCR/"shotmap.json")); picks = json.load(open(SCR/"picks.json"))
vir = {k[:8]: v for k, v in json.load(open(SCR/"virality.json")).items()}
newshots = (ROOT/"design"/"new-shots.md").read_text()
esc = lambda t: html.escape(str(t), quote=True)

REF = re.compile(r"@\[[a-z0-9_-]{1,40}\]\([0-9a-f-]{36}\)|<<<[0-9a-f-]{36}>>>|@[a-z][a-z0-9_-]{2,40}", re.I)
def mark(t):
    out, i = [], 0
    for m in REF.finditer(t):
        out.append(esc(t[i:m.start()])); out.append('<b class="ref">'+esc(m.group(0))+'</b>'); i = m.end()
    out.append(esc(t[i:])); return "".join(out)

SHOTS = [("S1",1,"Rise out of the fire"),("S2",1,"The courtyard of worlds"),("S3",1,"“There must be risk”"),("S4",1,"“He's your brother”"),
 ("S5",1,"“Tomorrow” — the tear freezes"),("NEW-3",1,"Transition A — the facet becomes ocean"),("S6",2,"108 years later — the run"),("S7",2,"Sixteen behind her, and a wall of ice"),
 ("S8",2,"Up the wall"),("S9",2,"The threadwright's eyes"),("S10",2,"The leviathan"),("S11",2,"Running the flank"),("S12",2,"The lightning river"),
 ("S13",2,"The vortex, from the Sun"),("NEW-1",2,"The mind divides"),("S14",2,"The Stone leaves her"),("NEW-4",2,"Transition B — the streak crosses the world"),
 ("S15",3,"Nacre Beach — the same sun"),("S16",3,"Over the abyss"),("S17",3,"Twelve ships"),("S18",3,"The Temple does not answer"),("S19",3,"The Keepers kneel"),
 ("S20",3,"The mountain"),("NEW-2",3,"The mound"),("S21",3,"The garden replants itself"),("S22",3,"What Alder saw"),("S23",1,"Tomorrow, again")]
NEWDUR = {"NEW-1":16,"NEW-2":16,"NEW-3":8,"NEW-4":12}

blocks = {}
for m in re.finditer(r"^## (NEW-\d) · \"([^\"]+)\" · \*\*(\d+s)\*\* · audio \*\*(ON|OFF)\*\* · goes between (.+?)\n+```\n(.*?)```", newshots, re.S|re.M):
    blocks[m.group(1)] = dict(title=m.group(2), dur=m.group(3), audio=m.group(4), where=m.group(5).strip(), text=m.group(6).strip())

def chip(label, v, lo=False):
    cls = "good" if (v>=55 if not lo else v<=0.5) else ("warn" if (v>=45 if not lo else v<=0.6) else "bad")
    return f'<span class="sc {cls}" title="{esc(label)}">{esc(label)} <b>{v if not lo else f"{v:.2f}"}</b></span>'

def tile(id8, role, pickscore=None):
    v = vids[id8]; s = vir.get(id8); t = smap.get(id8, {}).get("title", "")
    mp4 = v.get("mp4") or ""; thumb = v.get("thumb") or ""
    refs = "".join(f"<i>@{esc(r)}</i>" for r in v["refs"])
    scores = ""
    if s:
        beats = pickscore is not None and s["overall"] > pickscore
        scores = ('<div class="scs">'+chip("overall",s["overall"])+chip("hook",s["hook"])+chip("engage",s["engagement"])+chip("wander",s["dmn_mean"],lo=True)
                  +('<span class="sc up">scores above the pick — check on your screen</span>' if beats else '')+'</div>')
    elif v["duration"] > 16:
        scores = '<div class="scs"><span class="sc muted">not scored — over the Predictor\'s 16s limit</span></div>'
    else:
        scores = '<div class="scs"><span class="sc muted">not scored</span></div>'
    frames = "chained on start/end frames" if v["frames"] else "no start/end frames"
    return f'''<div class="tile {role}" id="r-{id8}">
  <div class="art"><div class="ph"><span class="fid">{esc(id8)}</span><span class="fr">{esc(role)}</span></div>
    {f'<video muted playsinline preload="metadata" poster="{esc(thumb)}" src="{esc(mp4)}" controls></video>' if mp4 else ''}</div>
  <div class="cap"><b>{esc(t)}</b><span class="role {role}">{esc(role)}</span></div>
  <div class="meta">{v["duration"]}s · {esc(str(v["resolution"]))} · {esc(v["model"])} · {frames} · audio {"on" if v["audio"] else "off"}</div>
  {scores}
  <div class="hs">{refs}</div>
  <div class="acts">{f'<a href="{esc(mp4)}" target="_blank" rel="noopener">open the clip ↗</a>' if mp4 else ''}<button type="button" class="jid" data-copy="{esc(v["id"])}" title="copy the job id">{esc(v["id"])}</button></div>
  <details><summary>Prompt as generated</summary><pre>{mark(v["prompt"].strip())}</pre></details>
</div>'''

cards, ribbon, total = [], [], 0
for sid, mv, title in SHOTS:
    if sid.startswith("NEW"):
        b = blocks.get(sid); d = NEWDUR[sid]; total += d
        ribbon.append(f'<b data-mv="{mv}" class="new" style="flex:{d}" title="{sid} · {d}s · not yet shot">{sid}</b>')
        body = (f'<pre class="prompt">{mark(b["text"])}</pre><div class="acts"><button type="button" class="copy" data-copy="{esc(b["text"])}">Copy prompt</button>'
                f'<span class="meta">{b["dur"]} · audio {b["audio"]} · {esc(b["where"])}</span></div>') if b else ""
        note = ("<p class='why'>Redundant: the S6 pick already opens on the tear-to-ocean match cut and carries the card. Skip this one unless you want the macro on its own.</p>" if sid=="NEW-3" else
                "<p class='why'>Not generated yet. Nothing has been made in the account since 06:57 UTC. This is on the list.</p>")
        cards.append(f'''<article class="shot new" data-mv="{mv}" id="{sid}"><header><span class="sid">{sid}</span><h3>{esc(title)}</h3><span class="dur">{d}s · unshot</span></header>{note}{body}</article>''')
        continue
    if sid == "S2":
        cards.append(f'''<article class="shot merged" data-mv="{mv}" id="S2"><header><span class="sid">S2</span><h3>{esc(title)}</h3><span class="dur">inside S1</span></header><p class="why">{esc(picks["S2"]["why"])}</p></article>''')
        continue
    p = picks[sid]; pid = p["pick"]; pv = vids[pid]; d = pv["duration"] if sid != "S1" else 30; total += d
    ribbon.append(f'<b data-mv="{mv}" style="flex:{d}" title="{sid} · {d}s">{sid if d>=10 else ""}</b>')
    ps = vir.get(pid, {}).get("overall")
    alts = "".join(tile(a, "alternate", ps) for a in p["alts"][:3] if a in vids)
    regen = f'<div class="regen"><b>Make again.</b> {esc(p.get("regen_note",""))}</div>' if p.get("regen") else ""
    cards.append(f'''<article class="shot" data-mv="{mv}" id="{sid}">
  <header><span class="sid">{sid}</span><h3>{esc(title)}</h3><span class="dur">{d}s</span></header>
  <p class="why">{esc(p["why"])}</p>{regen}
  <div class="row"><div class="pickcol">{tile(pid, "pick")}</div><div class="altcol">{alts or '<p class="meta">No alternates in the account.</p>'}</div></div>
</article>''')

scored = [vir[k] for k in vir]; n = len(scored)
regen_n = sum(1 for p in picks.values() if p.get("regen")); unshot = sum(1 for s,_,_ in SHOTS if s.startswith("NEW") and s!="NEW-3")
mm = f"{total//60}:{total%60:02d}"

page = f'''<title>Canvas Boards</title>
<meta name="description" content="The cut take by take: the best render for every shot, three alternates each, and the shots still to make.">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Archivo:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{--ground:#F2EFE8;--surface:#FBF9F5;--surface-2:#E9E4D9;--line:#CFC7B6;--line-soft:#E2DCCE;--ink:#171410;--ink-2:#4A443B;--ink-3:#7A7264;
--sun:#9A6208;--sun-soft:#FAEBCB;--void:#3E39C9;--void-soft:#E0DEFB;--coral:#B33A18;--coral-soft:#FBDDD1;--good:#0A6B45;--good-soft:#CFEEE0;--warn:#8A4B00;--warn-soft:#FBE6CC;--bad:#9C2A2A;--tile:#1A1713;--ref:#B4482C;
--display:"Fraunces","Iowan Old Style",Palatino,Georgia,serif;--body:"Archivo",ui-sans-serif,system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--ground:#0D0B09;--surface:#161311;--surface-2:#211D19;--line:#3B342C;--line-soft:#241F1A;--ink:#F4EFE4;--ink-2:#B0A797;--ink-3:#7D7466;
--sun:#EDB44C;--sun-soft:#33260E;--void:#9B97FF;--void-soft:#1B1A3E;--coral:#FF8D63;--coral-soft:#37190F;--good:#4FD9A2;--good-soft:#082C1F;--warn:#F0B36A;--warn-soft:#33220C;--bad:#F08A8A;--tile:#0A0908;--ref:#E2795C}}}}
:root[data-theme="dark"]{{--ground:#0D0B09;--surface:#161311;--surface-2:#211D19;--line:#3B342C;--line-soft:#241F1A;--ink:#F4EFE4;--ink-2:#B0A797;--ink-3:#7D7466;
--sun:#EDB44C;--sun-soft:#33260E;--void:#9B97FF;--void-soft:#1B1A3E;--coral:#FF8D63;--coral-soft:#37190F;--good:#4FD9A2;--good-soft:#082C1F;--warn:#F0B36A;--warn-soft:#33220C;--bad:#F08A8A;--tile:#0A0908;--ref:#E2795C}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--ground);color:var(--ink);font:15px/1.6 var(--body);-webkit-font-smoothing:antialiased;padding-inline:clamp(16px,3vw,26px);padding-block:0 80px}}
.wrap{{max-width:1240px;margin:0 auto}} h1,h2,h3{{margin:0;font-family:var(--display);font-weight:600;letter-spacing:-.012em;text-wrap:balance}} p{{margin:0}}
.eyebrow{{font-family:var(--mono);font-size:10.5px;letter-spacing:.19em;text-transform:uppercase;color:var(--ink-3)}}
.mast{{padding:46px 0 30px;border-bottom:1px solid var(--line);display:flex;flex-direction:column;gap:18px}} .mast h1{{font-size:clamp(34px,5.4vw,58px);line-height:1.02}}
.lede{{font-size:17px;color:var(--ink-2);max-width:66ch}} .lede b{{color:var(--ink)}}
.kpis{{display:flex;flex-wrap:wrap;gap:10px}} .kpi{{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:10px 14px;min-width:120px}}
.kpi b{{display:block;font:600 26px/1 var(--display);font-variant-numeric:tabular-nums}} .kpi span{{font-size:12px;color:var(--ink-3)}}
.ribbon{{display:flex;height:34px;gap:1px;border-radius:5px;overflow:hidden;margin-top:6px}} .ribbon b{{display:flex;align-items:center;justify-content:center;min-width:0;font:400 9.5px var(--mono);color:#fff;overflow:hidden}}
.ribbon b[data-mv="1"]{{background:#9A6208}} .ribbon b[data-mv="2"]{{background:#3E39C9}} .ribbon b[data-mv="3"]{{background:#B33A18}} .ribbon b.new{{outline:2px dashed #fff;outline-offset:-4px;opacity:.75}}
.note{{border-left:3px solid var(--line);padding:2px 0 2px 16px;color:var(--ink-2);font-size:14px;max-width:80ch}}
.shot{{margin-top:26px;border:1px solid var(--line);border-radius:14px;background:var(--surface);overflow:hidden}}
.shot[data-mv="1"]{{border-top:3px solid var(--sun)}} .shot[data-mv="2"]{{border-top:3px solid var(--void)}} .shot[data-mv="3"]{{border-top:3px solid var(--coral)}}
.shot header{{padding:18px 22px 6px;display:flex;flex-wrap:wrap;gap:12px;align-items:baseline}} .shot h3{{font-size:21px}}
.sid{{font:500 12px var(--mono);letter-spacing:.06em;color:var(--ink-3)}} .dur{{margin-left:auto;font:11px var(--mono);color:var(--ink-3)}}
.why{{padding:0 22px 12px;color:var(--ink-2);max-width:90ch}} .shot.new .why,.shot.merged .why{{padding-bottom:18px}}
.regen{{margin:0 22px 14px;padding:10px 14px;border:1px solid var(--warn);background:var(--warn-soft);border-radius:8px;font-size:14px}}
.row{{display:grid;grid-template-columns:minmax(280px,1.4fr) minmax(280px,2fr);gap:18px;padding:0 22px 22px}}
.altcol{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;align-content:start}}
.tile{{display:flex;flex-direction:column;gap:6px;min-width:0}} .tile.pick .art{{border:2px solid var(--good)}}
.art{{position:relative;aspect-ratio:21/9;border-radius:7px;overflow:hidden;background:var(--tile);border:1px solid var(--line);max-width:100%}}
.art video{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;background:#000;opacity:0}} .art.live video{{opacity:1}} .art.live .ph{{display:none}}
.art .ph{{position:absolute;inset:0;z-index:1;pointer-events:none;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;text-align:center}}
.art .ph .fid{{font:600 22px var(--display);color:#EDE5D6;opacity:.9}} .art .ph .fr{{font:9px var(--mono);letter-spacing:.16em;text-transform:uppercase;color:#9A8F7C}}
.cap{{display:flex;align-items:baseline;gap:7px;flex-wrap:wrap}} .cap b{{font-size:13px}} .role{{font:9px var(--mono);letter-spacing:.13em;text-transform:uppercase;padding:2px 5px;border-radius:3px;background:var(--surface-2);color:var(--ink-3);border:1px solid var(--line-soft)}}
.role.pick{{background:var(--good-soft);color:var(--good);border-color:var(--good)}}
.meta{{font-size:11.5px;color:var(--ink-3)}} .hs{{display:flex;flex-wrap:wrap;gap:3px}} .hs i{{font:9.5px var(--mono);font-style:normal;padding:2px 5px;border-radius:3px;background:var(--surface-2);color:var(--ink-3);border:1px solid var(--line-soft)}}
.scs{{display:flex;flex-wrap:wrap;gap:4px}} .sc{{font:10.5px var(--mono);padding:3px 7px;border-radius:4px;border:1px solid var(--line);color:var(--ink-2)}} .sc b{{font-weight:500}}
.sc.good{{border-color:var(--good);color:var(--good)}} .sc.warn{{border-color:var(--warn);color:var(--warn)}} .sc.bad{{border-color:var(--bad);color:var(--bad)}} .sc.muted{{color:var(--ink-3);border-style:dashed}} .sc.up{{background:var(--good-soft);border-color:var(--good);color:var(--good)}}
.acts{{display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-size:12px}} .acts a{{color:var(--sun)}}
.jid{{font:9.5px var(--mono);color:var(--ink-3);background:none;border:0;padding:0;cursor:pointer;text-align:left;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:100%}} .jid:hover{{color:var(--ink-2);text-decoration:underline}}
details summary{{cursor:pointer;color:var(--ink-3);font-size:12px}} pre{{white-space:pre-wrap;font:12px/1.55 var(--mono);background:var(--surface-2);border:1px solid var(--line-soft);border-radius:6px;padding:10px;margin:6px 0 0;overflow-x:auto}}
.ref{{color:var(--ref);font-weight:500}} .prompt{{margin:0 22px 12px}} .shot.new .acts{{padding:0 22px 20px}}
.copy{{font:600 11px var(--body);letter-spacing:.08em;text-transform:uppercase;background:var(--ink);color:var(--ground);border:0;border-radius:6px;padding:9px 14px;cursor:pointer}} .copy:focus-visible,.jid:focus-visible{{outline:2px solid var(--sun);outline-offset:2px}}
h2{{font-size:clamp(22px,3vw,30px);margin:48px 0 10px}} .callout{{border:1px solid var(--warn);background:var(--warn-soft);border-radius:10px;padding:14px 18px;font-size:14px;max-width:90ch}}
@media (max-width:760px){{.row{{grid-template-columns:1fr}}}} @media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
</style>
<div class="wrap">
<header class="mast">
  <p class="eyebrow">Matter of Light · canvas boards · rebuilt 14 Sep, 21:50 UTC</p>
  <h1>The cut, take by take</h1>
  <p class="lede">Every tile is a real render from the account, by URL — <b>one pick per shot</b>, then up to three alternates, in running order from the star to the star. Scores are the platform's Virality Predictor on the renders it could take (≤16s). The picks are mine, and the reason for each is written under it.</p>
  <div class="kpis">
    <div class="kpi"><b>23</b><span>shots · one merged into S1</span></div><div class="kpi"><b>{len(smap)}</b><span>project renders placed</span></div>
    <div class="kpi"><b>{n}</b><span>renders scored</span></div><div class="kpi"><b>{regen_n}</b><span>shots to make again</span></div><div class="kpi"><b>{unshot}</b><span>shots not yet shot</span></div><div class="kpi"><b>{mm}</b><span>runtime of the picks + unshot</span></div>
  </div>
  <div class="ribbon" aria-hidden="true">{"".join(ribbon)}</div>
  <p class="note">In the published view the clips cannot load — the account's CDN is outside the viewer's sandbox — so each tile shows its identity card and an <em>open the clip</em> link that works. Open the same file from your own copy of the repository and every clip plays inline.</p>
</header>
<div class="callout" style="margin-top:22px"><b>Read the hook column with care.</b> Mean hook across the scored renders is in the low thirties because the film opens almost every shot on stillness — a locked frame, a slow crane, a held wide. The Predictor is built for feeds and penalises that; a jury does not. Use the hook numbers for one thing only: choosing the clip for the public post. That is S22's chroma take (hook 41) or S23 (38).</div>
{"".join(cards)}
<h2>Method</h2>
<p class="note">Built by <code>design/build-shot-board.py</code> from the account's generation history, the shot map, the picks and the Predictor scores. Regenerate, do not hand-edit. Per-shot prompts for the reshoots are in <code>design/recreate-prompts.md</code>; the four unshot prompts are in <code>design/new-shots.md</code>.</p>
</div>
<script>
document.querySelectorAll('.art video').forEach(v=>{{v.addEventListener('loadeddata',()=>v.parentNode.classList.add('live'));v.addEventListener('error',()=>v.remove())}});
document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{{const t=b.dataset.copy,o=b.textContent;const done=()=>{{b.textContent='copied';setTimeout(()=>b.textContent=o,1400)}};
try{{await navigator.clipboard.writeText(t);done();return}}catch(e){{}}
const ta=document.createElement('textarea');ta.value=t;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{{document.execCommand('copy');done()}}catch(e){{b.textContent='select and ⌘C'}}ta.remove();}}));
</script>
'''
(ROOT/"shot-board.html").write_text(page)
print("wrote shot-board.html", len(page), "bytes;", len(cards), "cards;", n, "scored; runtime", mm)
