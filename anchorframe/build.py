#!/usr/bin/env python3
"""Build the shot board for one project: the cut in order, one pick per shot, the alternates,
every tile a real render by URL, and the unshot shots with their prompts ready to paste.

    python3 anchorframe/build.py anchorframe/projects/<slug>        ->  projects/<slug>/board.html

Reads project.json, generations.json (from ingest.py) and scores.json if present.
Pick order: the shot's explicit `pick` -> highest Predictor score (if board.score_over_pick)
-> newest take. Nothing here is hand-edited; change the JSON and rebuild.
"""
import json, re, sys, html, pathlib, datetime
pdir = pathlib.Path(sys.argv[1]); P = json.load(open(pdir / "project.json"))
G = json.load(open(pdir / "generations.json")) if (pdir / "generations.json").exists() else []
SC = json.load(open(pdir / "scores.json")) if (pdir / "scores.json").exists() else {}
vids = {g["id"][:8]: g for g in G}; sc8 = {k[:8]: v for k, v in SC.items()}
esc = lambda t: html.escape(str(t), quote=True)
REF = re.compile(r"@\[[a-z0-9_-]{1,40}\]\([0-9a-f-]{36}\)|<<<[0-9a-f-]{36}>>>|@[a-z][a-z0-9_-]{2,40}", re.I)
def mark(t):
    out, i = [], 0
    for m in REF.finditer(t): out.append(esc(t[i:m.start()])); out.append('<b class="ref">' + esc(m.group(0)) + '</b>'); i = m.end()
    out.append(esc(t[i:])); return "".join(out)
TONE = {a["id"]: a.get("tone", "sun") for a in P["acts"]}; ANAME = {a["id"]: a["name"] for a in P["acts"]}
maxalt = P.get("board", {}).get("max_alternates", 3); sop = P.get("board", {}).get("score_over_pick", True)

def chip(label, v, lo=False):
    cls = "good" if (v >= 55 if not lo else v <= 0.5) else ("warn" if (v >= 45 if not lo else v <= 0.6) else "bad")
    return f'<span class="sc {cls}">{esc(label)} <b>{v if not lo else f"{v:.2f}"}</b></span>'
def tile(id8, role, pickscore=None):
    v = vids[id8]; s = sc8.get(id8); refs = "".join(f"<i>@{esc(r['name'])}</i>" for r in v["refs"] if r.get("name"))
    if s:
        up = pickscore is not None and s["overall"] > pickscore
        scores = '<div class="scs">' + chip("overall", s["overall"]) + chip("hook", s["hook"]) + chip("engage", s["engagement"]) + chip("wander", s["dmn_mean"], lo=True) + ('<span class="sc up">scores above the pick</span>' if up else "") + "</div>"
    else: scores = '<div class="scs"><span class="sc muted">' + ("over the Predictor's 16s limit" if (v.get("duration") or 0) > 16 else "not scored") + "</span></div>"
    frames = "chained on start/end frames" if v.get("frames") else "no start/end frames"
    when = datetime.datetime.utcfromtimestamp(v["createdAt"]).strftime("%d %b %H:%M") if v.get("createdAt") else ""
    return f'''<div class="tile {role}" id="r-{id8}"><div class="art"><div class="ph"><span class="fid">{id8}</span><span class="fr">{role}</span></div>
{f'<video muted playsinline preload="metadata" poster="{esc(v["thumb"])}" src="{esc(v["mp4"])}" controls></video>' if v.get("mp4") else ''}</div>
<div class="cap"><b>{esc({"map":"placed by hand map","pick":"on the pick list","alternate":"on the alternate list","ledger":"made by the desk","unplaced":"unplaced"}.get(v.get("how",""), v.get("how","").replace("prompt:","prompt match ")))}</b><span class="role {role}">{role}</span></div>
<div class="meta">{v.get("duration")}s · {esc(v.get("resolution"))} · {esc(v.get("model"))} · {frames} · audio {"on" if v.get("audio") else "off"} · {when} UTC</div>{scores}
<div class="hs">{refs}</div><div class="acts">{f'<a href="{esc(v["mp4"])}" target="_blank" rel="noopener">open the clip ↗</a>' if v.get("mp4") else ''}<button type="button" class="jid" data-copy="{esc(v["id"])}">{esc(v["id"])}</button></div>
<details><summary>Prompt as generated</summary><pre>{mark(v.get("prompt","").strip())}</pre></details></div>'''

takes_by_shot = {}
for g in G:
    if g.get("shot"): takes_by_shot.setdefault(g["shot"], []).append(g["id"][:8])
def resolve(s):
    takes = takes_by_shot.get(s["id"], [])
    pick = s.get("pick")[:8] if s.get("pick") and s["pick"][:8] in vids else None
    if not pick and takes:
        scored = [t for t in takes if t in sc8]
        pick = max(scored, key=lambda t: sc8[t]["overall"]) if (sop and scored) else takes[0]
    alts = [a[:8] for a in s.get("alternates", []) if a[:8] in vids and a[:8] != pick]
    rest = sorted([t for t in takes if t != pick and t not in alts], key=lambda t: (-(sc8.get(t, {}).get("overall", -1)), -vids[t]["createdAt"]))
    return pick, (alts + rest)[:maxalt]

cards, ribbon, total, unshot, regen, placed = [], [], 0, 0, 0, 0
for s in P["shots"]:
    sid, mv, title, tone = s["id"], s["act"], s.get("title", s["id"]), TONE.get(s["act"], "sun")
    st = str(s.get("status", "shot"))
    if st.startswith("merged-into:"):
        cards.append(f'<article class="shot merged" data-tone="{tone}" id="{sid}"><header><span class="sid">{sid}</span><h3>{esc(title)}</h3><span class="dur">inside {esc(st.split(":",1)[1])}</span></header><p class="why">{esc(s.get("why") or s.get("notes",""))}</p></article>'); continue
    pick, alts = resolve(s)
    if not pick:
        d = s.get("duration_s", 0); total += d; unshot += 1
        ribbon.append(f'<b data-tone="{tone}" class="new" style="flex:{d}" title="{sid} · {d}s · not yet shot">{sid}</b>')
        body = (f'<pre class="prompt">{mark(s["prompt"])}</pre><div class="acts pad"><button type="button" class="copy" data-copy="{esc(s["prompt"])}">Copy prompt</button><span class="meta">{d}s · audio {"on" if s.get("audio") else "off"} · {esc(P["higgsfield"].get("video_model",""))} · {esc(P["format"]["aspect"])} · {esc(P["format"]["resolution"])}</span></div>') if s.get("prompt") else '<p class="why muted">No prompt written yet.</p>'
        cards.append(f'<article class="shot new" data-tone="{tone}" id="{sid}"><header><span class="sid">{sid}</span><h3>{esc(title)}</h3><span class="dur">{d}s · unshot</span></header><p class="why">{esc(s.get("notes",""))}</p>{body}</article>'); continue
    placed += 1; d = vids[pick].get("duration") or s.get("duration_s", 0); total += d
    ribbon.append(f'<b data-tone="{tone}" style="flex:{d}" title="{sid} · {d}s">{sid if d >= 10 else ""}</b>')
    ps = sc8.get(pick, {}).get("overall")
    if s.get("regenerate"): regen += 1
    rg = f'<div class="regen"><b>Make again.</b> {esc(s.get("notes",""))}</div>' if s.get("regenerate") else ""
    altdiv = "".join(tile(a, "alternate", ps) for a in alts) or '<p class="meta">No alternates in the ledger.</p>'
    cards.append(f'<article class="shot" data-tone="{tone}" id="{sid}"><header><span class="sid">{sid}</span><h3>{esc(title)}</h3><span class="dur">{d}s</span></header><p class="why">{esc(s.get("why",""))}</p>{rg}<div class="row"><div class="pickcol">{tile(pick, "pick")}</div><div class="altcol">{altdiv}</div></div></article>')

mm = f"{int(total)//60}:{int(total)%60:02d}"; n = len([k for k in sc8 if k in vids]); hf = P["higgsfield"]
legend = " ".join(f'<span><i data-tone="{a.get("tone","sun")}"></i>{esc(a["id"])} · {esc(a["name"])}</span>' for a in P["acts"])
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(P["title"])} · Shot Board</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Archivo:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{--ground:#F2EFE8;--surface:#FBF9F5;--surface-2:#E9E4D9;--line:#CFC7B6;--line-soft:#E2DCCE;--ink:#171410;--ink-2:#4A443B;--ink-3:#7A7264;--sun:#9A6208;--void:#3E39C9;--coral:#B33A18;--good:#0A6B45;--good-soft:#CFEEE0;--warn:#8A4B00;--warn-soft:#FBE6CC;--bad:#9C2A2A;--tile:#1A1713;--ref:#B4482C;
--display:"Fraunces","Iowan Old Style",Palatino,Georgia,serif;--body:"Archivo",ui-sans-serif,system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--ground:#0D0B09;--surface:#161311;--surface-2:#211D19;--line:#3B342C;--line-soft:#241F1A;--ink:#F4EFE4;--ink-2:#B0A797;--ink-3:#7D7466;--sun:#EDB44C;--void:#9B97FF;--coral:#FF8D63;--good:#4FD9A2;--good-soft:#082C1F;--warn:#F0B36A;--warn-soft:#33220C;--bad:#F08A8A;--tile:#0A0908;--ref:#E2795C}}}}
:root[data-theme="dark"]{{--ground:#0D0B09;--surface:#161311;--surface-2:#211D19;--line:#3B342C;--line-soft:#241F1A;--ink:#F4EFE4;--ink-2:#B0A797;--ink-3:#7D7466;--sun:#EDB44C;--void:#9B97FF;--coral:#FF8D63;--good:#4FD9A2;--good-soft:#082C1F;--warn:#F0B36A;--warn-soft:#33220C;--bad:#F08A8A;--tile:#0A0908;--ref:#E2795C}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--ground);color:var(--ink);font:15px/1.6 var(--body);padding-inline:clamp(16px,3vw,26px);padding-block:0 80px}}
.wrap{{max-width:1240px;margin:0 auto}} h1,h2,h3{{margin:0;font-family:var(--display);font-weight:600;letter-spacing:-.012em;text-wrap:balance}} p{{margin:0}}
.eyebrow{{font-family:var(--mono);font-size:10.5px;letter-spacing:.19em;text-transform:uppercase;color:var(--ink-3)}} .eyebrow a{{color:inherit}}
.mast{{padding:40px 0 26px;border-bottom:1px solid var(--line);display:flex;flex-direction:column;gap:16px}} .mast h1{{font-size:clamp(32px,5vw,54px);line-height:1.02}}
.lede{{font-size:16.5px;color:var(--ink-2);max-width:70ch}} .kpis{{display:flex;flex-wrap:wrap;gap:10px}} .kpi{{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:10px 14px;min-width:118px}}
.kpi b{{display:block;font:600 24px/1 var(--display);font-variant-numeric:tabular-nums}} .kpi span{{font-size:12px;color:var(--ink-3)}}
.ribbon{{display:flex;height:32px;gap:1px;border-radius:5px;overflow:hidden}} .ribbon b{{display:flex;align-items:center;justify-content:center;min-width:0;font:400 9.5px var(--mono);color:#fff;overflow:hidden}}
[data-tone="sun"]{{--t:var(--sun)}} [data-tone="void"]{{--t:var(--void)}} [data-tone="coral"]{{--t:var(--coral)}} .ribbon b{{background:var(--t)}} .ribbon b.new{{outline:2px dashed #fff;outline-offset:-4px;opacity:.75}}
.legend{{display:flex;gap:16px;flex-wrap:wrap;font:10.5px var(--mono);color:var(--ink-3)}} .legend span{{display:flex;align-items:center;gap:6px}} .legend i{{width:11px;height:11px;border-radius:3px;background:var(--t)}}
.note{{border-left:3px solid var(--line);padding:2px 0 2px 16px;color:var(--ink-2);font-size:14px;max-width:80ch}}
.shot{{margin-top:24px;border:1px solid var(--line);border-top:3px solid var(--t);border-radius:14px;background:var(--surface);overflow:hidden}}
.shot header{{padding:16px 22px 6px;display:flex;flex-wrap:wrap;gap:12px;align-items:baseline}} .shot h3{{font-size:20px}}
.sid{{font:500 12px var(--mono);letter-spacing:.06em;color:var(--ink-3)}} .dur{{margin-left:auto;font:11px var(--mono);color:var(--ink-3)}}
.why{{padding:0 22px 12px;color:var(--ink-2);max-width:90ch}} .shot.new .why,.shot.merged .why{{padding-bottom:16px}}
.regen{{margin:0 22px 14px;padding:10px 14px;border:1px solid var(--warn);background:var(--warn-soft);border-radius:8px;font-size:14px}}
.row{{display:grid;grid-template-columns:minmax(280px,1.4fr) minmax(280px,2fr);gap:18px;padding:0 22px 22px}} .altcol{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;align-content:start}}
.tile{{display:flex;flex-direction:column;gap:6px;min-width:0}} .tile.pick .art{{border:2px solid var(--good)}}
.art{{position:relative;aspect-ratio:{P["format"]["aspect"].replace(":","/")};border-radius:7px;overflow:hidden;background:var(--tile);border:1px solid var(--line);max-width:100%}}
.art video{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;background:#000;opacity:0}} .art.live video{{opacity:1}} .art.live .ph{{display:none}}
.art .ph{{position:absolute;inset:0;z-index:1;pointer-events:none;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px}} .art .ph .fid{{font:600 22px var(--display);color:#EDE5D6;opacity:.9}} .art .ph .fr{{font:9px var(--mono);letter-spacing:.16em;text-transform:uppercase;color:#9A8F7C}}
.cap{{display:flex;align-items:baseline;gap:7px;flex-wrap:wrap}} .cap b{{font-size:12.5px;color:var(--ink-3);font-weight:500}} .role{{font:9px var(--mono);letter-spacing:.13em;text-transform:uppercase;padding:2px 5px;border-radius:3px;background:var(--surface-2);color:var(--ink-3);border:1px solid var(--line-soft)}} .role.pick{{background:var(--good-soft);color:var(--good);border-color:var(--good)}}
.meta{{font-size:11.5px;color:var(--ink-3)}} .hs{{display:flex;flex-wrap:wrap;gap:3px}} .hs i{{font:9.5px var(--mono);font-style:normal;padding:2px 5px;border-radius:3px;background:var(--surface-2);color:var(--ink-3);border:1px solid var(--line-soft)}}
.scs{{display:flex;flex-wrap:wrap;gap:4px}} .sc{{font:10.5px var(--mono);padding:3px 7px;border-radius:4px;border:1px solid var(--line);color:var(--ink-2)}} .sc b{{font-weight:500}} .sc.good{{border-color:var(--good);color:var(--good)}} .sc.warn{{border-color:var(--warn);color:var(--warn)}} .sc.bad{{border-color:var(--bad);color:var(--bad)}} .sc.muted{{color:var(--ink-3);border-style:dashed}} .sc.up{{background:var(--good-soft);border-color:var(--good);color:var(--good)}}
.acts{{display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-size:12px}} .acts.pad{{padding:0 22px 20px}} .acts a{{color:var(--sun)}}
.jid{{font:9.5px var(--mono);color:var(--ink-3);background:none;border:0;padding:0;cursor:pointer;text-align:left;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:100%}} .jid:hover{{color:var(--ink-2);text-decoration:underline}}
details summary{{cursor:pointer;color:var(--ink-3);font-size:12px}} pre{{white-space:pre-wrap;font:12px/1.55 var(--mono);background:var(--surface-2);border:1px solid var(--line-soft);border-radius:6px;padding:10px;margin:6px 0 0;overflow-x:auto}} .prompt{{margin:0 22px 12px}} .ref{{color:var(--ref);font-weight:500}}
.copy{{font:600 11px var(--body);letter-spacing:.08em;text-transform:uppercase;background:var(--ink);color:var(--ground);border:0;border-radius:6px;padding:9px 14px;cursor:pointer}} .copy:focus-visible,.jid:focus-visible{{outline:2px solid var(--sun);outline-offset:2px}}
h2{{font-size:clamp(22px,3vw,30px);margin:44px 0 10px}} .muted{{color:var(--ink-3)}} footer{{margin-top:40px;color:var(--ink-3);font-size:13px}}
@media (max-width:760px){{.row{{grid-template-columns:1fr}}}} @media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
</style></head><body><div class="wrap">
<header class="mast"><p class="eyebrow"><a href="../../index.html">anchorframe</a> · {esc(P["title"])} · built {datetime.datetime.utcnow().strftime("%d %b %Y %H:%M")} UTC</p>
<h1>{esc(P["title"])} — the cut, take by take</h1>
<p class="lede">{esc(P.get("logline",""))}</p>
<div class="kpis"><div class="kpi"><b>{len(P["shots"])}</b><span>shots in the cut</span></div><div class="kpi"><b>{len(G)}</b><span>takes admitted to this project</span></div><div class="kpi"><b>{placed}</b><span>shots with a pick</span></div><div class="kpi"><b>{n}</b><span>takes scored</span></div><div class="kpi"><b>{regen}</b><span>to make again</span></div><div class="kpi"><b>{unshot}</b><span>not yet shot</span></div><div class="kpi"><b>{mm}</b><span>runtime of picks + unshot</span></div></div>
<div class="ribbon" aria-hidden="true">{"".join(ribbon)}</div><div class="legend">{legend}<span>dashed — not yet shot</span></div>
<p class="note">Project folder: <a href="{esc(hf.get("project_url","#"))}">{esc(hf.get("project_name",""))}</a> · video on <code>{esc(hf.get("video_model",""))}</code> · {esc(P["format"]["aspect"])} · {esc(P["format"]["resolution"])} · {P["format"].get("fps",24)} fps. Clips play inline when this file is opened locally; in a sandboxed viewer each tile shows its identity card and an <em>open the clip</em> link.</p></header>
{"".join(cards)}
<footer>Built by <code>anchorframe/build.py</code> from <code>project.json</code>, <code>generations.json</code> and <code>scores.json</code>. Change the JSON and rebuild; do not hand-edit this file.</footer></div>
<script>
document.querySelectorAll('.art video').forEach(v=>{{v.addEventListener('loadeddata',()=>v.parentNode.classList.add('live'));v.addEventListener('error',()=>v.remove())}});
document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{{const t=b.dataset.copy,o=b.textContent;const done=()=>{{b.textContent='copied';setTimeout(()=>b.textContent=o,1400)}};try{{await navigator.clipboard.writeText(t);done();return}}catch(e){{}}const ta=document.createElement('textarea');ta.value=t;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{{document.execCommand('copy');done()}}catch(e){{b.textContent='select and ⌘C'}}ta.remove();}}));
</script></body></html>'''
(pdir / "board.html").write_text(page)
# keep the desk's project index current
ix = pdir.parent / "index.json"; idx = json.load(open(ix)) if ix.exists() else []
rec = {"slug": pdir.name, "title": P["title"], "byline": P.get("byline",""), "kind": P.get("kind",""), "logline": P.get("logline",""), "aspect": P["format"]["aspect"],
       "shots": len(P["shots"]), "takes": len(G), "picks": placed, "scored": n, "unshot": unshot, "regen": regen, "runtime": mm, "project_url": hf.get("project_url",""),
       "built": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}
idx = [r for r in idx if r.get("slug") != pdir.name] + [rec]; ix.write_text(json.dumps(idx, indent=1, ensure_ascii=False))
print(f"wrote {pdir/'board.html'}: {len(page)} bytes · {len(cards)} cards · {placed} picks · {unshot} unshot · {n} scored · {mm}")
