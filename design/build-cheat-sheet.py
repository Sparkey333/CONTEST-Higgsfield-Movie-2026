#!/usr/bin/env python3
"""Build the Matter of Light cheat sheet from design/cheat-sheet.json.

    python3 design/build-cheat-sheet.py [--fonts CACHE_DIR] [--fragment OUT] [--pdf]

Writes cheat-sheet.html (a full page), optionally a fragment for publishing, and with --pdf
prints cheat-sheet.pdf through headless Chromium (US Letter, landscape). Fonts are inlined
from Google Fonts when they can be fetched, so the page and the PDF use the same faces;
otherwise the page links them. Regenerate, don't hand-edit.
"""
import json, re, sys, html, base64, pathlib, subprocess, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[1]
D = json.load(open(ROOT / "design" / "cheat-sheet.json", encoding="utf-8"))
args = sys.argv[1:]
def opt(name):
    return args[args.index(name) + 1] if name in args else None
esc = lambda t: html.escape(str(t), quote=True)
def md(t):
    t = esc(t); t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t); return re.sub(r"`(.+?)`", r"<code>\1</code>", t)

FAMILIES = "family=Barlow+Condensed:wght@500;600;700&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;600&display=swap"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
def fonts_css():
    cache = pathlib.Path(opt("--fonts") or (ROOT / ".font-cache")); cache.mkdir(parents=True, exist_ok=True)
    try:
        css = urllib.request.urlopen(urllib.request.Request("https://fonts.googleapis.com/css2?" + FAMILIES, headers={"User-Agent": UA}), timeout=20).read().decode()
        faces = {}
        for blk in re.findall(r"/\* latin \*/\s*@font-face\s*\{(.*?)\}", css, re.S):
            fam = re.search(r"font-family:\s*'([^']+)'", blk).group(1); sty = re.search(r"font-style:\s*(\w+)", blk).group(1)
            w = int(re.search(r"font-weight:\s*(\d+)", blk).group(1)); url = re.search(r"url\((https://[^)]+\.woff2)\)", blk).group(1)
            f = faces.setdefault(url, {"fam": fam, "sty": sty, "w": []}); f["w"].append(w)
        out = []
        for url, f in faces.items():
            p = cache / url.rsplit("/", 1)[1]
            if not p.exists(): p.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read())
            b64 = base64.b64encode(p.read_bytes()).decode(); lo, hi = min(f["w"]), max(f["w"])
            out.append(f"@font-face{{font-family:'{f['fam']}';font-style:{f['sty']};font-weight:{lo if lo == hi else f'{lo} {hi}'};font-display:swap;src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
        return "<style>" + "".join(out) + "</style>", len(faces)
    except Exception as e:
        print("fonts not inlined:", e)
        return f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FAMILIES}">', 0

CSS = r"""
/* A call-sheet grid: nine stage cards in three phase rows; each card is banded by colour into steps, settings and lessons, and a gate closes it in green. */
:root{
 --paper:#EEF1F5;--sheet:#FFFFFF;--ink:#151821;--ink-2:#434A5B;--ink-3:#5F6679;--rule:#D3D8E2;--slate:#1B1F29;--slate-ink:#F4F6FA;
 --step:#1D5BB8;--step-tint:#E6EEFB;--step-line:#B9CDF1;
 --set:#875800;--set-tint:#FBF1DA;--set-line:#E3C47E;
 --lesson:#AE3820;--lesson-tint:#FCE6E0;--lesson-line:#EBAE9E;
 --gate:#17734A;--gate-tint:#DDF2E7;--gate-line:#93D1B0;
 --display:"Barlow Condensed","Arial Narrow","Roboto Condensed",sans-serif;
 --body:"Source Sans 3","Segoe UI",system-ui,-apple-system,sans-serif;
 --mono:"JetBrains Mono",ui-monospace,"SF Mono",Menlo,Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
 --paper:#0D1015;--sheet:#151922;--ink:#EDF0F5;--ink-2:#B3BACA;--ink-3:#8C94A7;--rule:#283040;--slate:#E9ECF2;--slate-ink:#12151C;
 --step:#8EB5FF;--step-tint:#152238;--step-line:#2D4673;--set:#F2C462;--set-tint:#2B2210;--set-line:#5E4A1C;
 --lesson:#FF9F89;--lesson-tint:#331A15;--lesson-line:#6B3226;--gate:#62D6A0;--gate-tint:#0F2A1E;--gate-line:#22603F;color-scheme:dark}}
:root[data-theme="dark"]{
 --paper:#0D1015;--sheet:#151922;--ink:#EDF0F5;--ink-2:#B3BACA;--ink-3:#8C94A7;--rule:#283040;--slate:#E9ECF2;--slate-ink:#12151C;
 --step:#8EB5FF;--step-tint:#152238;--step-line:#2D4673;--set:#F2C462;--set-tint:#2B2210;--set-line:#5E4A1C;
 --lesson:#FF9F89;--lesson-tint:#331A15;--lesson-line:#6B3226;--gate:#62D6A0;--gate-tint:#0F2A1E;--gate-line:#22603F;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 var(--body);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.wrap{max-width:1240px;margin:0 auto;padding-block:30px 60px;padding-inline:max(16px,3vw)}
code{font:.86em/1.3 var(--mono);background:color-mix(in srgb,var(--ink) 7%,transparent);border-radius:3px;padding:.5px 4px;overflow-wrap:anywhere}
h1,h2,h3,h4{text-wrap:balance;margin:0}
/* header */
.top{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px 28px;align-items:end;border-bottom:2px solid var(--ink);padding-bottom:16px}
.eyebrow{font:600 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--ink-3);margin:0 0 10px}
h1{font:700 clamp(34px,5.4vw,56px)/.95 var(--display);text-transform:uppercase;letter-spacing:.01em}
.lede{margin:10px 0 0;max-width:68ch;color:var(--ink-2);font-size:16px}
.by{font:12px/1.4 var(--mono);color:var(--ink-3);text-align:right}
@media (max-width:720px){.top{grid-template-columns:1fr}.by{text-align:left}}
/* key + tools */
.key{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;margin:16px 0 0;font-size:13.5px;color:var(--ink-2)}
.k{display:inline-flex;align-items:center;gap:7px} .k b{color:var(--ink)}
.mk{display:inline-block;width:13px;height:13px;flex:none;border:2px solid currentColor;border-radius:2px}
.mk.step{color:var(--step)} .mk.set{color:var(--set);transform:rotate(45deg) scale(.86);border-radius:1px} .mk.lesson{color:var(--lesson);background:var(--lesson);border-radius:50%;border-color:var(--lesson)}
.gk{font:700 10px/1 var(--mono);letter-spacing:.12em;color:var(--gate);background:var(--gate-tint);border:1px solid var(--gate-line);border-radius:3px;padding:4px 6px}
.lp{font:700 14px/1 var(--mono);color:var(--ink-3)}
.tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-left:auto}
.tools .lbl{font:600 10.5px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
.tg{font:600 12.5px/1 var(--body);padding:7px 11px;border-radius:999px;border:1.5px solid var(--rule);background:var(--sheet);color:var(--ink-2);cursor:pointer}
.tg[aria-pressed="true"].step{border-color:var(--step);color:var(--step);background:var(--step-tint)}
.tg[aria-pressed="true"].set{border-color:var(--set);color:var(--set);background:var(--set-tint)}
.tg[aria-pressed="true"].lesson{border-color:var(--lesson);color:var(--lesson);background:var(--lesson-tint)}
.tg.plain{border-style:dashed}
.tg:focus-visible,.tick:focus-visible{outline:2px solid var(--step);outline-offset:2px}
.count{font:12px var(--mono);color:var(--ink-3);font-variant-numeric:tabular-nums}
/* map */
.map{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:0;margin:20px 0 0;border:1.5px solid var(--ink);border-radius:6px;overflow:hidden;background:var(--sheet)}
.map a{position:relative;display:flex;flex-direction:column;gap:5px;padding:10px 12px 10px;text-decoration:none;color:var(--ink);border-right:1px solid var(--rule);min-width:0}
.map a:last-child{border-right:0} .map a:hover{background:var(--paper)}
.map .n{font:700 22px/1 var(--display);color:var(--ink-3)} .map .nm{font:600 15px/1.05 var(--display);text-transform:uppercase;letter-spacing:.02em;overflow-wrap:anywhere}
.map .ct{display:flex;gap:7px;font:600 11px/1 var(--mono);font-variant-numeric:tabular-nums} .map .ct .s{color:var(--step)} .map .ct .t{color:var(--set)} .map .ct .l{color:var(--lesson)}
.map .g{position:absolute;top:8px;right:8px}
@media (max-width:900px){.map{grid-template-columns:repeat(3,minmax(0,1fr))}.map a{border-bottom:1px solid var(--rule)}.map a:nth-child(3n){border-right:0}}
/* numbers */
.nums{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:10px;margin:18px 0 0}
.nums div{border-top:2px solid var(--ink);padding-top:6px;min-width:0} .nums b{display:block;font:600 26px/1 var(--display);font-variant-numeric:tabular-nums} .nums span{font-size:12px;color:var(--ink-3);line-height:1.2;display:block;margin-top:3px}
@media (max-width:900px){.nums{grid-template-columns:repeat(3,minmax(0,1fr))}}
/* sections */
.sec{margin-top:34px} .sec>h2{font:700 24px/1 var(--display);text-transform:uppercase;letter-spacing:.02em;display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.sec>h2 .ph{font:600 11px/1 var(--mono);letter-spacing:.16em;color:var(--ink-3)} .sec>p.note{margin:6px 0 14px;color:var(--ink-2);max-width:80ch;font-size:14.5px}
/* global settings */
.glob{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
@media (max-width:1100px){.glob{grid-template-columns:repeat(2,minmax(0,1fr))}} @media (max-width:560px){.glob{grid-template-columns:1fr}}
.gc{background:var(--set-tint);border:1px solid var(--set-line);border-radius:6px;padding:11px 13px;min-width:0}
.gc h3{font:700 14px/1 var(--display);text-transform:uppercase;letter-spacing:.06em;color:var(--set);margin-bottom:8px;display:flex;align-items:center;gap:8px}
.gc dl{margin:0;display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 10px;font-size:13px} .gc dt{color:var(--ink-3);font-weight:600} .gc dd{margin:0;color:var(--ink);overflow-wrap:anywhere}
.gc dd code,.gc dd{font-family:var(--body)}
.bl{background:var(--lesson-tint);border:1px solid var(--lesson-line);border-radius:6px;padding:12px 14px}
.bl ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 22px} @media (max-width:760px){.bl ul{grid-template-columns:1fr}}
/* stage cards */
.stages{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;align-items:start}
@media (max-width:1000px){.stages{grid-template-columns:1fr}}
.stage{background:var(--sheet);border:1px solid var(--rule);border-radius:6px;overflow:hidden;min-width:0}
.stage>header{display:grid;grid-template-columns:auto minmax(0,1fr);gap:0 12px;align-items:stretch;border-bottom:1px solid var(--rule)}
.stage .num{background:var(--slate);color:var(--slate-ink);font:700 30px/1 var(--display);display:flex;align-items:center;justify-content:center;min-width:52px;padding:0 10px;font-variant-numeric:tabular-nums}
.stage .hd{padding:10px 12px 9px 0;min-width:0} .stage h3{font:700 21px/1 var(--display);text-transform:uppercase;letter-spacing:.02em}
.stage .q{margin:4px 0 0;font-style:italic;color:var(--ink-2);font-size:14px;line-height:1.35}
.stage .mol{margin:0;padding:7px 12px;font:11px/1.45 var(--mono);color:var(--ink-3);border-bottom:1px solid var(--rule)} .stage .mol span{font-weight:600;letter-spacing:.1em;text-transform:uppercase;margin-right:6px;color:var(--ink-2)}
.grp{padding:8px 12px 9px;border-bottom:1px solid var(--rule)}
.grp.step{background:var(--step-tint)} .grp.set{background:var(--set-tint)} .grp.lesson{background:var(--lesson-tint)}
.grp h4{font:700 12px/1 var(--display);text-transform:uppercase;letter-spacing:.12em;display:flex;align-items:center;gap:7px;margin:0 0 6px}
.grp.step h4{color:var(--step)} .grp.set h4{color:var(--set)} .grp.lesson h4{color:var(--lesson)} .grp h4 .c{font:600 10.5px/1 var(--mono);opacity:.85}
.grp ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:5px}
.grp li{display:grid;grid-template-columns:16px minmax(0,1fr);gap:8px;align-items:start;font-size:14px;line-height:1.4;color:var(--ink-2)} .grp li b{color:var(--ink);font-weight:700}
.grp li label{cursor:pointer}
.tick{appearance:none;-webkit-appearance:none;margin:3px 0 0;width:14px;height:14px;border:2px solid var(--step);border-radius:2px;background:var(--sheet);cursor:pointer;display:grid;place-content:center}
.set .tick{border-color:var(--set);transform:rotate(45deg) scale(.82);border-radius:1px;margin-top:4px}
.tick:checked{background:var(--step)} .set .tick:checked{background:var(--set)}
.tick:checked::after{content:"";width:6px;height:6px;background:var(--sheet);clip-path:polygon(14% 44%,0 65%,50% 100%,100% 16%,80% 0,43% 62%)}
.set .tick:checked::after{transform:rotate(-45deg)}
.tick:checked+label{color:var(--ink-3);text-decoration:line-through;text-decoration-thickness:1px} .tick:checked+label b{color:var(--ink-3)}
.dot{width:10px;height:10px;border-radius:50%;background:var(--lesson);margin:5px 0 0 2px}
.loop{margin:0;padding:8px 12px;font-size:13px;line-height:1.4;color:var(--ink-2);border-bottom:1px solid var(--rule)} .loop b{color:var(--ink)} .loop .lp{margin-right:5px}
.gate{display:grid;grid-template-columns:auto minmax(0,1fr);gap:2px 10px;align-items:baseline;padding:9px 12px 10px;background:var(--gate-tint)}
.gate .gk{grid-row:span 2;align-self:start} .gate b{font:700 14px/1.1 var(--display);text-transform:uppercase;letter-spacing:.05em;color:var(--gate)} .gate p{margin:0;font-size:13px;line-height:1.4;color:var(--ink-2)}
.stage>:last-child{border-bottom:0}
body.hide-step .grp.step,body.hide-set .grp.set,body.hide-lesson .grp.lesson{display:none}
footer{margin-top:34px;padding-top:12px;border-top:1px solid var(--rule);font:12px/1.5 var(--mono);color:var(--ink-3);display:flex;flex-wrap:wrap;gap:6px 22px;justify-content:space-between}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
/* print: US Letter landscape; light palette always */
@page{size:11in 8.5in;margin:.32in .34in}
@media print{
 :root,:root[data-theme="dark"],:root:not([data-theme="light"]){--paper:#FFFFFF;--sheet:#FFFFFF;--ink:#151821;--ink-2:#3A4152;--ink-3:#5F6679;--rule:#D3D8E2;--slate:#1B1F29;--slate-ink:#F4F6FA;
  --step:#1D5BB8;--step-tint:#E9F0FC;--step-line:#B9CDF1;--set:#875800;--set-tint:#FCF3DF;--set-line:#E3C47E;--lesson:#AE3820;--lesson-tint:#FDEAE4;--lesson-line:#EBAE9E;--gate:#17734A;--gate-tint:#E1F4EA;--gate-line:#93D1B0;color-scheme:light}
 body{font-size:8.2pt;background:#fff} .wrap{max-width:none;padding:0}
 .tools{display:none} .top{padding-bottom:8pt} h1{font-size:30pt} .lede{font-size:9.5pt;margin-top:5pt} .eyebrow{font-size:7pt;margin-bottom:5pt} .by{font-size:7.5pt}
 .key{margin-top:8pt;font-size:8.5pt} .map{margin-top:10pt;grid-template-columns:repeat(9,minmax(0,1fr))} .map a{padding:6pt 7pt;border-bottom:0;border-right:1px solid var(--rule)} .map a:last-child{border-right:0} .map .n{font-size:15pt} .map .nm{font-size:10pt} .map .ct{font-size:7.5pt}
 .nums{grid-template-columns:repeat(9,minmax(0,1fr));margin-top:10pt} .nums b{font-size:17pt} .nums span{font-size:7.5pt}
 .sec{margin-top:13pt} .sec>h2{font-size:15pt} .sec>p.note{font-size:8.5pt;margin:3pt 0 7pt}
 .glob{grid-template-columns:1fr 1.25fr .9fr 1.3fr 1fr;gap:6pt} .gc{padding:7pt 8pt} .gc h3{font-size:9.5pt;margin-bottom:5pt} .gc dl{font-size:7.8pt;gap:2.5pt 6pt}
 .bl{padding:6pt 9pt} .bl ul{grid-template-columns:repeat(3,minmax(0,1fr));gap:3pt 14pt} .bl li{font-size:8pt}
 .phase{break-before:page;margin-top:0} .stages{grid-template-columns:repeat(3,minmax(0,1fr));gap:8pt}
 .stage{break-inside:avoid} .stage .num{font-size:20pt;min-width:34pt} .stage h3{font-size:13.5pt} .stage .q{font-size:8.5pt} .stage .hd{padding:6pt 8pt 6pt 0}
 .stage .mol{font-size:6.8pt;padding:4pt 8pt} .grp{padding:5pt 8pt 6pt} .grp h4{font-size:8pt;margin-bottom:3.5pt} .grp ul{gap:2.5pt} .grp li{font-size:8.1pt;line-height:1.32;grid-template-columns:10pt minmax(0,1fr);gap:5pt}
 .tick{width:9pt;height:9pt;border-width:1.3pt;margin-top:1.5pt} .set .tick{margin-top:2pt} .dot{width:6.5pt;height:6.5pt;margin:3pt 0 0 1.5pt}
 .loop{font-size:7.8pt;padding:4.5pt 8pt} .gate{padding:5pt 8pt 6pt} .gate b{font-size:9pt} .gate p{font-size:7.8pt} .gk{font-size:6.8pt;padding:2.5pt 4pt}
 footer{display:none}
}
"""

def counts(s): return len(s["steps"]), len(s["settings"]), len(s["lessons"])
def grp(s, kind, items, label):
    lis = []
    for i, t in enumerate(items):
        iid = f"{s['key']}-{kind}-{i}"
        if kind == "lesson": lis.append(f'<li><span class="dot" aria-hidden="true"></span><span>{md(t)}</span></li>')
        else: lis.append(f'<li><input type="checkbox" class="tick" id="{iid}" data-k="{iid}"><label for="{iid}">{md(t)}</label></li>')
    return f'<section class="grp {kind}"><h4><span class="mk {kind}" aria-hidden="true"></span>{label} <span class="c">{len(items)}</span></h4><ul>{"".join(lis)}</ul></section>'
def card(s):
    loop = s.get("loop"); gate = s.get("gate")
    lp = f'<p class="loop"><span class="lp" aria-hidden="true">⟲</span><b>Iterate · {esc(loop["name"])}.</b> When {esc(loop["when"])}: {esc(loop["do"])}.</p>' if loop else '<p class="loop"><span class="lp" aria-hidden="true">✓</span><b>No loop.</b> This stage is a checklist.</p>'
    gt = f'<div class="gate"><span class="gk">GATE {esc(gate["id"])}</span><b>{esc(gate["name"])}</b><p>{esc(gate["test"])}</p></div>' if gate else ""
    return (f'<article class="stage" id="s-{s["key"]}"><header><span class="num">{s["n"]}</span><div class="hd"><h3>{esc(s["name"])}</h3><p class="q">{esc(s["q"])}</p></div></header>'
            f'<p class="mol"><span>On the film</span>{esc(s["mol"])}</p>'
            + grp(s, "step", s["steps"], "Steps") + grp(s, "set", s["settings"], "Settings") + grp(s, "lesson", s["lessons"], "Lessons") + lp + gt + "</article>")

st = D["stages"]; ns, nt, nl = (sum(counts(s)[i] for s in st) for i in range(3))
def gate_badge(s): return ('<span class="gk g">' + esc(s["gate"]["id"]) + "</span>") if s.get("gate") else ""
def map_cell(s):
    a, b, c = counts(s)
    return ('<a href="#s-' + s["key"] + '"><span class="n">' + str(s["n"]) + '</span><span class="nm">' + esc(s["name"]) + '</span><span class="ct">'
            + '<span class="s" title="steps">' + str(a) + '</span><span class="t" title="settings">' + str(b) + '</span><span class="l" title="lessons">' + str(c) + "</span></span>" + gate_badge(s) + "</a>")
mapc = "".join(map_cell(s) for s in st)
nums = "".join(f"<div><b>{esc(v)}</b><span>{esc(l)}</span></div>" for v, l in D["numbers"])
glob = "".join(f'<div class="gc"><h3><span class="mk set" aria-hidden="true"></span>{esc(g["h"])}</h3><dl>{"".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in g["rows"])}</dl></div>' for g in D["global"])
bl = D["bible"]
def dot_li(x): return '<li><span class="dot" aria-hidden="true"></span><span>' + md(x) + "</span></li>"
bible = '<div class="bl"><ul class="grp lesson" style="background:none;padding:0;border:0">' + "".join(dot_li(x) for x in bl["lessons"]) + "</ul></div>"
phases = ""
for ph in D["phases"]:
    cards = "".join(card(s) for s in st if s["phase"] == ph["id"])
    phases += f'<section class="sec phase" id="phase-{ph["id"]}"><h2><span class="ph">PHASE {ph["id"]}</span>{esc(ph["name"])}</h2><p class="note">{esc(ph["note"])}</p><div class="stages">{cards}</div></section>'

JS = r"""<script>
(function(){
 var P='mol-cheat:',ticks=[].slice.call(document.querySelectorAll('.tick')),cnt=document.getElementById('cnt');
 function get(k){try{return localStorage.getItem(P+k)}catch(e){return null}}
 function put(k,v){try{v?localStorage.setItem(P+k,'1'):localStorage.removeItem(P+k)}catch(e){}}
 function upd(){if(cnt)cnt.textContent=ticks.filter(function(t){return t.checked}).length+' of '+ticks.length+' ticked'}
 ticks.forEach(function(t){t.checked=get(t.dataset.k)==='1';t.addEventListener('change',function(){put(t.dataset.k,t.checked);upd()})});upd();
 [].slice.call(document.querySelectorAll('.tg[data-kind]')).forEach(function(b){var k=b.dataset.kind;if(get('hide-'+k)==='1'){b.setAttribute('aria-pressed','false');document.body.classList.add('hide-'+k)}
  b.addEventListener('click',function(){var on=b.getAttribute('aria-pressed')!=='true';b.setAttribute('aria-pressed',on?'true':'false');document.body.classList.toggle('hide-'+k,!on);put('hide-'+k,!on)})});
 var c=document.getElementById('clear');if(c)c.addEventListener('click',function(){ticks.forEach(function(t){t.checked=false;put(t.dataset.k,false)});upd()});
})();
</script>"""

fonts, nfaces = fonts_css()
body = f'''<div class="wrap">
<header class="top"><div><p class="eyebrow">{esc(D["eyebrow"])}</p><h1>{esc(D["h1"])}</h1><p class="lede">{esc(D["lede"])}</p></div><p class="by">{esc(D["byline"])}<br>{ns} steps · {nt} settings · {nl} lessons</p></header>
<div class="key"><span class="k"><span class="mk step"></span><b>Step</b> do it, tick it</span><span class="k"><span class="mk set"></span><b>Setting</b> use this value</span><span class="k"><span class="mk lesson"></span><b>Lesson</b> what the film taught</span><span class="k"><span class="gk">GATE</span> a person checks a screen</span><span class="k"><span class="lp">⟲</span> the loop inside a stage</span>
<div class="tools" role="group" aria-label="Show subtasks"><span class="lbl">Show</span><button type="button" class="tg step" data-kind="step" aria-pressed="true">Steps</button><button type="button" class="tg set" data-kind="set" aria-pressed="true">Settings</button><button type="button" class="tg lesson" data-kind="lesson" aria-pressed="true">Lessons</button><span class="count" id="cnt"></span><button type="button" class="tg plain" id="clear">Clear ticks</button></div></div>
<nav class="map" aria-label="The nine stages">{mapc}</nav>
<div class="nums">{nums}</div>
<section class="sec" id="settings"><h2><span class="ph">EVERY STAGE</span>Settings at a glance</h2><p class="note">The values that applied across the whole production.</p><div class="glob">{glob}</div></section>
<section class="sec" id="bible"><h2><span class="ph">THE DOCUMENTS</span>{esc(bl["h"])}</h2><p class="note">{esc(bl["note"])}</p>{bible}</section>
{phases}
<footer><span>Built by design/build-cheat-sheet.py from design/cheat-sheet.json · regenerate, don’t hand-edit</span><span>Sources: anchorframe/workflow.json · anchorframe/tips.md · director-bible.html · design/final-cut.notes.json</span></footer>
</div>'''
head = f'<title>{esc(D["title"])}</title>{fonts}<style>{CSS}</style>'
full = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">{head}</head><body>{body}{JS}</body></html>'
(ROOT / "cheat-sheet.html").write_text(full, encoding="utf-8")
if opt("--fragment"): pathlib.Path(opt("--fragment")).write_text(head + body + JS, encoding="utf-8")
print(f"wrote cheat-sheet.html · {len(full)//1024} KB · {nfaces} font files inlined · {ns} steps · {nt} settings · {nl} lessons")
if "--pdf" in args:
    chrome = next((p for p in ["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "chromium", "google-chrome"] if pathlib.Path(p).exists() or p in ("chromium", "google-chrome")), None)
    out = ROOT / "cheat-sheet.pdf"
    subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={out}", (ROOT / "cheat-sheet.html").as_uri()], check=True, capture_output=True, timeout=120)
    print(f"wrote {out} · {out.stat().st_size//1024} KB")
