#!/usr/bin/env python3
"""Build Anchorframe's pages from data: index.html (front door), workflow.html (nine stages,
five gates, the iteration loops), links.html (every link, by stage). Sources: workflow.json,
links.json, tips.md, projects/index.json.   python3 anchorframe/desk.py
"""
import json, re, html, pathlib, datetime
D = pathlib.Path(__file__).resolve().parent
esc = lambda t: html.escape(str(t), quote=True)
W = json.load(open(D / "workflow.json")); L = json.load(open(D / "links.json"))
tips = (D / "tips.md").read_text(); ix = json.load(open(D / "projects" / "index.json")) if (D / "projects" / "index.json").exists() else []
LINK = {l["id"]: l for g in L["groups"] for l in g["links"]}
EX = [json.load(open(f)) for f in sorted((D / "projects").glob("*/examples.json"))]
NOW = datetime.datetime.utcnow().strftime("%d %b %Y %H:%M UTC")

def inline(t):
    t = esc(t); t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t); t = re.sub(r"`(.+?)`", r"<code>\1</code>", t); return re.sub(r"(?<!\*)\*(?!\*)(.+?)\*", r"<em>\1</em>", t)

CSS = """
:root{--ground:#EDEFF5;--surface:#FFFFFF;--surface-2:#E3E6EF;--surface-3:#D6DAE7;--line:#BFC6D8;--line-soft:#DCE1EC;--ink:#0E1017;--ink-2:#3D4459;--ink-3:#646B80;--gold:#8A5A00;--gold-soft:#FBEBC4;--gold-line:#D9AC46;--void:#3A32DC;--void-soft:#DEDCFF;--void-line:#9A96F5;--coral:#BC3317;--coral-soft:#FFDCD1;--coral-line:#EE9273;--jade:#046B45;--jade-soft:#CDF0E0;--jade-line:#5EBE95;--shadow:0 1px 2px rgba(16,18,28,.06),0 8px 24px -12px rgba(16,18,28,.18);
--display:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;--body:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;--mono:ui-monospace,"SF Mono","Cascadia Code","JetBrains Mono",Menlo,Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ground:#07080D;--surface:#111319;--surface-2:#1A1D28;--surface-3:#242938;--line:#333A4D;--line-soft:#20242F;--ink:#F4F0E6;--ink-2:#A8AEC2;--ink-3:#767D92;--gold:#FFBE4A;--gold-soft:#33260F;--gold-line:#6B4E18;--void:#9B9DFF;--void-soft:#1C1D3D;--void-line:#403FA0;--coral:#FF8F6B;--coral-soft:#3A1C13;--coral-line:#7A3826;--jade:#4FDCA0;--jade-soft:#0A2E20;--jade-line:#1D6B4C;--shadow:0 1px 2px rgba(0,0,0,.4),0 12px 32px -14px rgba(0,0,0,.7)}}
:root[data-theme="dark"]{--ground:#07080D;--surface:#111319;--surface-2:#1A1D28;--surface-3:#242938;--line:#333A4D;--line-soft:#20242F;--ink:#F4F0E6;--ink-2:#A8AEC2;--ink-3:#767D92;--gold:#FFBE4A;--gold-soft:#33260F;--gold-line:#6B4E18;--void:#9B9DFF;--void-soft:#1C1D3D;--void-line:#403FA0;--coral:#FF8F6B;--coral-soft:#3A1C13;--coral-line:#7A3826;--jade:#4FDCA0;--jade-soft:#0A2E20;--jade-line:#1D6B4C;--shadow:0 1px 2px rgba(0,0,0,.4),0 12px 32px -14px rgba(0,0,0,.7)}
*{box-sizing:border-box} html{scroll-behavior:smooth;scroll-padding-top:70px} body{margin:0;background:var(--ground);color:var(--ink);font:16px/1.6 var(--body);padding:0 0 90px;overflow-x:hidden} a{color:inherit}
.wrap{max-width:1100px;margin:0 auto;padding:0 clamp(16px,3vw,26px)}
header.top{border-bottom:1px solid var(--line);background:linear-gradient(180deg,var(--surface),var(--ground));padding:44px 0 32px}
.eyebrow{font:600 10.5px/1 var(--mono);letter-spacing:.19em;text-transform:uppercase;color:var(--ink-3);display:block;margin-bottom:14px} .eyebrow a{text-decoration:none}
h1{font:400 clamp(36px,6.4vw,58px)/1.02 var(--display);margin:0 0 12px;letter-spacing:-.012em} .tag{font:400 clamp(20px,2.6vw,26px)/1.3 var(--display);color:var(--ink-2);margin:0 0 14px;max-width:30ch} .lede{margin:0;max-width:66ch;color:var(--ink-2);font-size:16.5px}
.badges{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px} .badge{font:600 10px/1 var(--mono);letter-spacing:.11em;text-transform:uppercase;padding:6px 9px;border-radius:5px;border:1px solid var(--line);background:var(--surface-2);color:var(--ink-2)} .badge.on{background:var(--jade-soft);color:var(--jade);border-color:var(--jade-line)}
nav.jump{position:sticky;top:0;z-index:8;background:color-mix(in srgb,var(--ground) 92%,transparent);backdrop-filter:blur(9px);border-bottom:1px solid var(--line);margin-bottom:38px} nav.jump .wrap{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none} nav.jump a{font:600 10.5px/1 var(--mono);letter-spacing:.13em;text-transform:uppercase;color:var(--ink-3);text-decoration:none;padding:15px 13px;border-bottom:2px solid transparent;white-space:nowrap} nav.jump a:hover,nav.jump a.on{color:var(--ink);border-bottom-color:var(--gold-line)}
section{margin-bottom:54px;scroll-margin-top:74px} h2{font:400 27px/1.2 var(--display);margin:0 0 8px} h2 .n{font:600 11px/1 var(--mono);letter-spacing:.16em;color:var(--ink-3);vertical-align:middle;margin-right:12px} .sec-head{margin-bottom:20px} .sec-head p{margin:0;color:var(--ink-2);max-width:72ch;font-size:15px}
code{font:12.5px/1.45 var(--mono);background:var(--surface-2);border:1px solid var(--line-soft);border-radius:4px;padding:1.5px 5px;word-break:break-word}
.muted{color:var(--ink-3)} footer{color:var(--ink-3);font-size:13px;margin-top:40px}
/* map strip */
.map{display:flex;align-items:stretch;gap:0;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--surface)} .map a{flex:1 1 0;min-width:0;text-decoration:none;padding:12px 12px 10px 18px;display:flex;flex-direction:column;gap:4px;border-right:1px solid var(--line-soft);position:relative} .map a:last-child{border-right:0} .map a:hover{background:var(--surface-2)}
.map .sn{font:600 10px/1 var(--mono);letter-spacing:.14em;color:var(--ink-3)} .map .nm{font:600 13.5px/1.2 var(--body);padding-right:22px;overflow-wrap:anywhere} .map .q{font-size:11.5px;color:var(--ink-3);line-height:1.35;padding-right:6px} .map .it{position:absolute;top:9px;right:9px;font:700 13px/1 var(--mono);color:var(--coral)} .map .gt{position:absolute;right:-9px;top:50%;transform:translateY(-50%);z-index:2;font:700 9.5px/1 var(--mono);background:var(--gold);color:#fff;border-radius:3px;padding:4px 5px;letter-spacing:.08em}
@media (max-width:900px){.map{flex-wrap:wrap}.map a{flex:1 1 33%;border-bottom:1px solid var(--line-soft)}.map .gt{display:none}}
.legend{display:flex;gap:18px;flex-wrap:wrap;margin-top:10px;font:11px var(--mono);color:var(--ink-3)} .legend b{color:var(--coral);font-weight:700} .legend i{font-style:normal;background:var(--gold);color:#fff;border-radius:3px;padding:2px 5px;font-size:9.5px;letter-spacing:.08em}
/* stage cards */
.stage{background:var(--surface);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);margin-top:22px;overflow:hidden;scroll-margin-top:74px}
.stage>header{padding:22px 24px 8px;display:flex;flex-wrap:wrap;gap:10px 14px;align-items:baseline} .stage .sn{font:600 11px/1 var(--mono);letter-spacing:.16em;color:var(--gold)} .stage h2{margin:0;font-size:26px} .stage .q{width:100%;margin:2px 0 0;font:400 18px/1.35 var(--display);color:var(--ink-2)}
.stage .goal{padding:0 24px 16px;margin:0;color:var(--ink-2);font-size:15px;max-width:80ch}
.grid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(280px,1fr);gap:18px;padding:0 24px 20px} @media (max-width:820px){.grid{grid-template-columns:1fr}}
.col h4{margin:14px 0 6px;font:600 10.5px/1 var(--mono);letter-spacing:.15em;text-transform:uppercase;color:var(--ink-3)} .col h4:first-child{margin-top:0} .col ol,.col ul{margin:0;padding-left:20px;font-size:14.5px;color:var(--ink-2)} .col li{margin:5px 0}
.iter{border:1px solid var(--coral-line);background:linear-gradient(180deg,var(--coral-soft),var(--surface) 70%);border-radius:10px;padding:16px 18px} .iter .ih{display:flex;align-items:baseline;gap:10px;margin-bottom:8px} .iter .ih b{font:700 15px/1 var(--mono);color:var(--coral)} .iter .ih h4{margin:0;font:600 15px/1.3 var(--body)} .iter .ih span{margin-left:auto;font:600 9.5px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--coral)}
.iter dl{margin:0;display:grid;grid-template-columns:64px 1fr;gap:6px 10px;font-size:13.5px} .iter dt{font:600 10px/1.6 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)} .iter dd{margin:0;color:var(--ink-2)} .iter .mol{margin-top:12px;padding-top:10px;border-top:1px dashed var(--coral-line);font-size:13px;color:var(--ink-2)} .iter .mol b{font:600 9.5px/1.8 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);display:block}
.iter.none{border-color:var(--line);background:var(--surface-2)} .iter.none .ih b,.iter.none .ih span{color:var(--ink-3)}
.chips{display:flex;flex-wrap:wrap;gap:6px;padding:0 24px 8px} .chips .k{font:600 9.5px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);align-self:center;margin-right:4px;min-width:64px} .chip{font:11.5px var(--mono);padding:5px 9px;border-radius:6px;border:1px solid var(--line);background:var(--surface-2);color:var(--ink-2);text-decoration:none} a.chip:hover{border-color:var(--gold-line);color:var(--ink)} .chip.hf{border-color:var(--void-line);background:var(--void-soft);color:var(--void)}
.stage .foot{padding:12px 24px 16px;border-top:1px solid var(--line-soft);font:12px var(--mono);color:var(--ink-3);display:flex;gap:18px;flex-wrap:wrap}
.gate{margin-top:14px;border:1px solid var(--gold-line);background:var(--gold-soft);border-radius:10px;padding:14px 20px;display:grid;grid-template-columns:auto 1fr;gap:6px 16px;align-items:baseline} .gate .gk{font:700 12px/1 var(--mono);letter-spacing:.16em;color:var(--gold);background:var(--surface);border:1px solid var(--gold-line);border-radius:5px;padding:7px 9px} .gate h3{margin:0;font:600 16px/1.3 var(--body)} .gate p{margin:0;grid-column:2;font-size:14px;color:var(--ink-2)}
/* the living course: examples + reminders */
.course{border-top:1px solid var(--line-soft);padding:16px 24px 6px;display:grid;grid-template-columns:minmax(0,2.2fr) minmax(240px,1fr);gap:18px} @media (max-width:820px){.course{grid-template-columns:1fr}}
.course h4{margin:0 0 10px;font:600 10.5px/1 var(--mono);letter-spacing:.15em;text-transform:uppercase;color:var(--ink-3)} .course h4 b{color:var(--gold);font-weight:600}
.exrow{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px} .xt{margin:0;display:flex;flex-direction:column;gap:6px;min-width:0} .xt.wide{grid-column:span 2} @media (max-width:520px){.xt.wide{grid-column:span 1}}
.xa{position:relative;border-radius:7px;overflow:hidden;background:#1A1713;border:1px solid var(--line);aspect-ratio:21/9} .xa[data-ar="16/9"]{aspect-ratio:16/9} .xa[data-ar="1/1"]{aspect-ratio:1/1}
.xa img,.xa video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;opacity:0} .xa.live img,.xa.live video{opacity:1} .xa.live .xph{display:none}
.xph{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;text-align:center;padding:8px;z-index:1;pointer-events:none} .xph b{font:600 18px var(--display);color:#EDE5D6;opacity:.9;font-weight:400} .xph span{font:9px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:#9A8F7C}
.xpair{display:grid;grid-template-columns:1fr 1fr;gap:6px} .xpair .xa{aspect-ratio:21/9} .xpair .xa[data-ar="16/9"]{aspect-ratio:16/9} .xpair .xa[data-ar="1/1"]{aspect-ratio:1/1} .xpair small{display:block;font:10px var(--mono);color:var(--ink-3);margin-top:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.xt figcaption{font-size:12.5px;color:var(--ink-2);line-height:1.45} .xt figcaption b{display:block;color:var(--ink);font-weight:600;font-size:13px} .xt figcaption .fr{display:block;font:10px var(--mono);color:var(--ink-3);margin-top:3px} .xt figcaption a{color:var(--void);text-decoration:none;font-size:11.5px} .xt figcaption a:hover{text-decoration:underline}
.xt audio{width:100%;height:36px} .xa.au{aspect-ratio:auto;height:52px;background:var(--surface-2);border-color:var(--line-soft);display:flex;align-items:center;justify-content:center} .xa.au .xph{position:static;flex-direction:row;gap:8px} .xa.au .xph b{color:var(--ink-2);font-size:14px} .xa.au .xph span{color:var(--ink-3)}
.rem ul{list-style:none;margin:0;padding:0} .rem li{margin:0 0 8px} .rem label{display:grid;grid-template-columns:18px 1fr;gap:9px;align-items:start;font-size:13.5px;color:var(--ink-2);cursor:pointer;line-height:1.45} .rem input{margin:3px 0 0;width:15px;height:15px;accent-color:var(--jade)} .rem input:checked+span{color:var(--ink-3);text-decoration:line-through} .rem .st{font:10px var(--mono);color:var(--ink-3);margin-top:6px}
/* generic cards */
.docs{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px} a.doc,.doc{display:flex;flex-direction:column;gap:10px;text-decoration:none;background:var(--surface);border:1px solid var(--line);border-radius:11px;padding:20px 22px 18px;box-shadow:var(--shadow)} a.doc:hover{border-color:var(--gold-line)} .doc .k{font:600 9.5px/1 var(--mono);letter-spacing:.15em;text-transform:uppercase;color:var(--gold)} .doc h3{font:600 18px/1.25 var(--body);margin:0} .doc p{margin:0;font-size:14px;color:var(--ink-2);flex:1} .doc .f{font:11px/1 var(--mono);color:var(--ink-3);border-top:1px solid var(--line-soft);padding-top:11px;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap} a.doc.primary{border-color:var(--gold-line);background:linear-gradient(180deg,var(--gold-soft),var(--surface) 62%)}
.stats{display:flex;flex-wrap:wrap;gap:6px 14px;font:12px var(--mono);color:var(--ink-3)} .stats b{color:var(--ink);font-weight:600}
.pill{font:600 9.5px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;padding:5px 8px;border-radius:4px;border:1px solid var(--line);color:var(--ink-3);align-self:flex-start} .pill.built{background:var(--jade-soft);color:var(--jade);border-color:var(--jade-line)} .pill.road{background:var(--gold-soft);color:var(--gold);border-color:var(--gold-line)}
.steps{display:flex;flex-direction:column;border-top:1px solid var(--line)} .step{display:grid;grid-template-columns:52px 1fr;gap:16px;padding:17px 0;border-bottom:1px solid var(--line-soft)} .step .sn{font:600 12px/1.5 var(--mono);color:var(--ink-3);letter-spacing:.08em} .step h4{margin:0 0 5px;font:600 15.5px/1.35 var(--body)} .step p{margin:0;font-size:14px;color:var(--ink-2)} .step p+p{margin-top:5px}
.loop{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px} .lp{background:var(--surface);border:1px solid var(--line);border-radius:9px;padding:14px 15px} .lp b{display:block;font:600 10px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:8px} .lp p{margin:0;font-size:13px;color:var(--ink-2)} .lp code{display:block;margin-top:8px;white-space:pre-wrap}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:11px;padding:24px;box-shadow:var(--shadow);margin-bottom:18px} .panel p{margin:0 0 10px;font-size:14.5px;color:var(--ink-2)} .panel p:last-child{margin:0}
.tips{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px} .tg{background:var(--surface);border:1px solid var(--line);border-radius:11px;padding:18px 20px 14px} .tg h3{margin:0 0 8px;font:600 15px/1.3 var(--body)} .tg ol{margin:0;padding-left:22px;font-size:14px;color:var(--ink-2)} .tg li{margin:6px 0} .tg li b{color:var(--ink)}
table{border-collapse:collapse;width:100%;font-size:14px} th,td{text-align:left;padding:10px 10px;border-bottom:1px solid var(--line-soft);vertical-align:top} th{font:600 10px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)} td a{color:var(--void);text-decoration:none;word-break:break-all} td a:hover{text-decoration:underline} .tw{overflow-x:auto} .g{font:400 22px/1.2 var(--display);margin:30px 0 6px}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""
def head(title, desc): return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><style>{CSS}</style></head><body>'
def nav(items, on): return '<nav class="jump"><div class="wrap">' + "".join(f'<a href="{esc(h)}"{" class=on" if h == on else ""}>{esc(t)}</a>' for t, h in items) + "</div></nav>"

# ---------- the map strip (shared) ----------
def mapstrip(prefix=""):
    out = []
    for s in W["stages"]:
        loop = s["iterate"]["name"] != "none"; gate = s["gate"]
        lp = '<span class="it" title="iteration">⟲</span>' if loop else ""
        gt = '<span class="gt" title="gate">' + esc(gate["id"]) + '</span>' if gate else ""
        out.append('<a href="' + prefix + '#s-' + s["key"] + '"><span class="sn">' + str(s["id"]) + '</span><span class="nm">' + esc(s["name"]) + '</span><span class="q">' + esc(s["question"]) + '</span>' + lp + gt + '</a>')
    return '<div class="map">' + "".join(out) + '</div><div class="legend"><span><b>⟲</b> an iteration loop lives in this stage</span><span><i>A</i> a gate closes it — a person looking at a screen, recorded</span></div>'

# ---------- workflow.html ----------
def chips(k, items, cls=""): return f'<div class="chips"><span class="k">{esc(k)}</span>' + "".join(f'<span class="chip {cls}">{esc(i)}</span>' for i in items) + "</div>" if items else ""
def linkchips(ids):
    out = []
    for i in ids:
        l = LINK.get(i)
        if l: out.append(f'<a class="chip hf" href="{esc(l["url"])}" target="_blank" rel="noopener" title="{esc(l["for"])}">{esc(l["name"])} ↗</a>')
    return f'<div class="chips"><span class="k">links</span>{"".join(out)}</div>' if out else ""
def xmedia(x):
    ar = x.get("ar", "21/9"); ph = '<div class="xph"><b>' + esc(x.get("label") or "") + '</b><span>' + esc(x.get("kind", "")) + '</span></div>'
    if x["kind"] == "image": return '<div class="xa" data-ar="' + ar + '">' + ph + '<img loading="lazy" alt="' + esc(x.get("label", "")) + '" src="' + esc(x["url"]) + '"></div>'
    if x["kind"] == "video": return '<div class="xa" data-ar="' + ar + '">' + ph + '<video muted playsinline preload="metadata" controls poster="' + esc(x.get("poster", "")) + '" src="' + esc(x["url"]) + '"></video></div>'
    if x["kind"] == "audio": return '<div class="xa au"><div class="xph"><b>◉ voice</b><span>' + esc(x.get("from", "")) + '</span></div></div><audio controls preload="none" src="' + esc(x["url"]) + '"></audio>'
    return ""
def xtile(x):
    if x["kind"] == "pair":
        body = '<div class="xpair"><div>' + xmedia(x["a"]) + '<small>' + esc(x["a"].get("label", "")) + '</small></div><div>' + xmedia(x["b"]) + '<small>' + esc(x["b"].get("label", "")) + '</small></div></div>'
        opens = '<a href="' + esc(x["a"]["url"]) + '" target="_blank" rel="noopener">open left ↗</a> · <a href="' + esc(x["b"]["url"]) + '" target="_blank" rel="noopener">open right ↗</a>'
        cls = "xt wide"
    else:
        body = xmedia(x); opens = '<a href="' + esc(x["url"]) + '" target="_blank" rel="noopener">open ↗</a>'; cls = "xt" + (" wide" if x["kind"] == "audio" and False else "")
    return '<figure class="' + cls + '">' + body + '<figcaption><b>' + esc(x.get("label", "")) + '</b>' + esc(x.get("why", "")) + '<span class="fr">' + esc(x.get("from", "")) + ' · ' + opens + '</span></figcaption></figure>'
def course(stage):
    key = stage["key"]; blocks = []
    for X in EX:
        items = X.get("stages", {}).get(key) or []
        if items: blocks.append('<div class="ex"><h4>From <b>' + esc(X.get("title", X.get("project", ""))) + '</b> — what to look for</h4><div class="exrow">' + "".join(xtile(x) for x in items) + '</div></div>')
    rem = stage.get("reminders") or []
    remh = ('<div class="rem"><h4>Reminders</h4><ul>' + "".join('<li><label><input type="checkbox" data-rem="' + key + ':' + str(i) + '"><span>' + esc(r) + '</span></label></li>' for i, r in enumerate(rem)) + '</ul><div class="st" data-remst="' + key + '"></div></div>') if rem else ""
    if not blocks and not remh: return ""
    if not blocks: blocks = ['<div class="ex"><h4>Examples</h4><p class="muted" style="font-size:13px;margin:0">No examples for this stage yet — add them to a project\'s <code>examples.json</code>.</p></div>']
    return '<div class="course">' + "".join(blocks) + remh + '</div>'
stages_html = []
for s in W["stages"]:
    it = s["iterate"]; none = it["name"] == "none"
    iter_html = (f'<div class="iter{" none" if none else ""}"><div class="ih"><b>⟲</b><h4>{"No loop — a checklist" if none else "Iterate here: " + esc(it["name"])}</h4><span>{"stage 7" if none else "iteration"}</span></div>'
                 f'<dl><dt>trigger</dt><dd>{esc(it["trigger"])}</dd><dt>do</dt><dd>{esc(it["do"])}</dd><dt>exit</dt><dd>{esc(it["exit"])}</dd><dt>cost</dt><dd>{esc(it["cost"])}</dd></dl>'
                 f'<div class="mol"><b>On Matter of Light</b>{esc(it["mol"])}</div></div>')
    gate_html = f'<div class="gate"><span class="gk">GATE {esc(s["gate"]["id"])}</span><h3>{esc(s["gate"]["name"])}</h3><p>{esc(s["gate"]["test"])}</p></div>' if s["gate"] else ""
    stages_html.append(f'''<article class="stage" id="s-{s["key"]}"><header><span class="sn">STAGE {s["id"]}</span><h2>{esc(s["name"])}</h2><p class="q">{esc(s["question"])}</p></header>
<p class="goal">{esc(s["goal"])}</p>
<div class="grid"><div class="col"><h4>Do</h4><ol>{"".join(f"<li>{esc(x)}</li>" for x in s["steps"])}</ol><h4>In</h4><ul>{"".join(f"<li>{esc(x)}</li>" for x in s["inputs"])}</ul><h4>Out</h4><ul>{"".join(f"<li>{esc(x)}</li>" for x in s["outputs"])}</ul></div><div class="col">{iter_html}</div></div>
{chips("surfaces", s["surfaces"], "hf")}{chips("files", s["files"])}{linkchips(s["links"])}
{course(s)}
<div class="foot"><span>{esc(s["mol"]["numbers"])}</span><span>{esc(s["mol"]["dates"])}</span></div></article>{gate_html}''')
loop_html = "".join(f'<div class="lp"><b>{i+1} · {esc(x["k"])}</b><p>{esc(x["do"])}</p><code>{esc(x["cmd"])}</code></div>' for i, x in enumerate(W["loop"]["steps"]))
expand_html = "".join(f'<div class="doc"><span class="k">{esc(k)} · unit: {esc(v["unit"])}</span><h3>{esc(v["name"])}</h3><p>{esc(v["scale"])}</p><span class="pill {"built" if v["status"].startswith("built") else "road"}">{esc(v["status"].split(" — ")[0])}</span><span class="f">{esc(v["status"].split(" — ",1)[1] if " — " in v["status"] else "")}</span></div>' for k, v in W["expand"].items() if not k.startswith("_"))
unique_html = "".join(f'<div class="doc"><h3>{esc(u["k"])}</h3><p>{esc(u["d"])}</p></div>' for u in W["unique"])
NAV_W = [("Overview", "index.html"), ("The map", "#map"), ("Stages", "#s-story"), ("The loop", "#loop"), ("Scale", "#scale"), ("Links", "links.html"), ("Keys", "keys.html")]
wf = head(f'{W["name"]} · Workflow', "Nine stages, five gates, one loop — the end-to-end workflow with its iteration points, derived from a finished film.") + f'''
<header class="top"><div class="wrap"><span class="eyebrow"><a href="index.html">{esc(W["name"])}</a> · the workflow · built {NOW}</span><h1>Nine stages. Five gates. One loop.</h1><p class="tag">{esc(W["promise"])}</p><p class="lede">{esc(W["derived_from"])}</p></div></header>
{nav(NAV_W, "#map")}<main class="wrap">
<section id="map"><div class="sec-head"><h2><span class="n">MAP</span>Where the loops are, and what closes them</h2><p>Every stage with a ⟲ has an <em>iterate here</em> card: what triggers the loop, what you do, what lets you out, what it costs — and what it cost on the film. Gates are the exits; nothing downstream begins until the gate above holds.</p></div>{mapstrip()}</section>
{"".join(stages_html)}
<section id="loop" style="margin-top:54px"><div class="sec-head"><h2><span class="n">INNER LOOP</span>Inside stages 4–6</h2><p>{esc(W["loop"]["_"])}</p></div><div class="loop">{loop_html}</div></section>
<section id="scale"><div class="sec-head"><h2><span class="n">SCALE</span>From short to feature to game</h2><p>{esc(W["expand"]["_"])}</p></div><div class="docs">{expand_html}</div></section>
<section id="why"><div class="sec-head"><h2><span class="n">WHY</span>What is different about this</h2></div><div class="docs">{unique_html}</div></section>
<footer>Built by <code>anchorframe/desk.py</code> from <code>workflow.json</code>, <code>links.json</code> and every project's <code>examples.json</code>. Regenerate, don't hand-edit.</footer></main>
<script>
document.querySelectorAll('.xa img').forEach(function(i){{i.addEventListener('load',function(){{i.parentNode.classList.add('live')}});i.addEventListener('error',function(){{i.remove()}});if(i.complete&&i.naturalWidth)i.parentNode.classList.add('live')}});
document.querySelectorAll('.xa video').forEach(function(v){{v.addEventListener('loadeddata',function(){{v.parentNode.classList.add('live')}});v.addEventListener('error',function(){{v.remove()}})}});
(function(){{var K='anchorframe.course';var st={{}};try{{st=JSON.parse(localStorage.getItem(K)||'{{}}')}}catch(e){{}}
var boxes=document.querySelectorAll('input[data-rem]');boxes.forEach(function(b){{b.checked=!!st[b.dataset.rem];b.addEventListener('change',function(){{st[b.dataset.rem]=b.checked;try{{localStorage.setItem(K,JSON.stringify(st))}}catch(e){{}}tally()}})}});
function tally(){{document.querySelectorAll('[data-remst]').forEach(function(el){{var k=el.dataset.remst,all=document.querySelectorAll('input[data-rem^="'+k+':"]'),on=0;all.forEach(function(b){{if(b.checked)on++}});el.textContent=on+' of '+all.length+' ticked — kept in this browser'}})}}tally();}})();
</script></body></html>'''
(D / "workflow.html").write_text(wf)

# ---------- links.html ----------
rows = []
for g in L["groups"]:
    rows.append(f'<h3 class="g">{esc(g["g"])}</h3><div class="tw"><table><thead><tr><th>Link</th><th>What it is for</th><th>Stages</th><th>Status</th></tr></thead><tbody>')
    for l in g["links"]:
        rows.append(f'<tr><td><a href="{esc(l["url"])}" target="_blank" rel="noopener"><b>{esc(l["name"])}</b></a><br><a href="{esc(l["url"])}" target="_blank" rel="noopener" class="muted" style="font:11px var(--mono);color:var(--ink-3)">{esc(l["url"])}</a></td><td>{esc(l["for"])}</td><td>{" ".join(f"<span class=chip>{esc(s)}</span>" for s in l["stages"])}</td><td><span class="pill {"built" if l["verified"] else "road"}">{"verified" if l["verified"] else "unverified"}</span></td></tr>')
    rows.append("</tbody></table></div>")
NAV_L = [("Overview", "index.html"), ("Workflow", "workflow.html"), ("Links", "links.html"), ("Keys", "keys.html")]
lk = head(f'{W["name"]} · Links', "Every Higgsfield surface and outside link the production used, by stage, verified or not.") + f'''
<header class="top"><div class="wrap"><span class="eyebrow"><a href="index.html">{esc(W["name"])}</a> · links · built {NOW}</span><h1>Every link, by stage</h1><p class="lede">{esc(L["_"])}</p></div></header>{nav(NAV_L, "links.html")}<main class="wrap">{"".join(rows)}
<footer>Built by <code>anchorframe/desk.py</code> from <code>links.json</code>. Add a link there, rebuild.</footer></main></body></html>'''
(D / "links.html").write_text(lk)

# ---------- index.html ----------
groups, cur = [], None
for line in tips.splitlines():
    if line.startswith("## "): cur = {"h": line[3:].strip(), "items": []}; groups.append(cur)
    elif re.match(r"^\d+\. ", line) and cur: n, body = line.split(". ", 1); cur["items"].append((n, body))
tips_html = "".join(f'<div class="tg"><h3>{esc(g["h"])}</h3><ol start="{g["items"][0][0] if g["items"] else 1}">' + "".join(f"<li>{inline(b)}</li>" for _, b in g["items"]) + "</ol></div>" for g in groups)
cards = "".join(f'''<a class="doc primary" href="projects/{esc(r["slug"])}/board.html"><span class="k">{esc(r["kind"])} · {esc(r["aspect"])}</span><h3>{esc(r["title"])}</h3><p>{esc(r["logline"])}</p>
<div class="stats"><span><b>{r["shots"]}</b> shots</span><span><b>{r["takes"]}</b> takes</span><span><b>{r["picks"]}</b> picks</span><span><b>{r["scored"]}</b> scored</span><span><b>{r["unshot"]}</b> unshot</span><span><b>{esc(r["runtime"])}</b> runtime</span></div>
<span class="f"><span>{esc(r["byline"])}</span><span>built {esc(r["built"])}</span></span></a>''' for r in ix) or '<p class="muted">No projects yet — the first build.py run adds one here.</p>'
toplinks = "".join(f'<a class="chip hf" href="{esc(LINK[i]["url"])}" target="_blank" rel="noopener">{esc(LINK[i]["name"])} ↗</a>' for i in ["hf_project","hf_elements","hf_cinema_studio","contest_page","festival_blog","hf_cloud_keys","hf_mcp_credits","hf_contact"] if i in LINK)
NEX = sum(len(v) for X in EX for v in X.get("stages", {}).values())
NAV_I = [("Workflow", "#workflow"), ("Projects", "#projects"), ("Start", "#start"), ("The loop", "#loop"), ("One folder", "#rule"), ("Scale", "#scale"), ("Why", "#why"), ("Links", "#links"), ("Keys", "keys.html"), ("Tips", "#tips")]
idx = head(W["name"], W["tagline"]) + f'''
<header class="top"><div class="wrap"><span class="eyebrow">{esc(W["name"])} · a folder per film</span><h1>{esc(W["name"])}</h1><p class="tag">{esc(W["tagline"])}</p><p class="lede">{esc(W["promise"])}</p>
<div class="badges"><span class="badge on">{len(W["stages"])} stages · {sum(1 for s in W["stages"] if s["gate"])} gates · 1 loop</span><span class="badge on">{NEX} examples · a living course</span><span class="badge on">{len(ix)} project{"s" if len(ix)!=1 else ""}</span><span class="badge">bring your own keys</span><span class="badge">regenerate, don't hand-edit</span><span class="badge">short → feature → play</span></div></div></header>
{nav(NAV_I, "#workflow")}<main class="wrap">
<section id="workflow"><div class="sec-head"><h2><span class="n">01</span>The workflow, at a glance</h2><p>Derived from a finished film, simplified to nine stages — the ninth is the read of the finished cut. ⟲ marks where you iterate; the gold ticks are the gates that close a stage. Each stage on the workflow page shows frames, takes and voice from a finished film with what to look for, and a reminders checklist that remembers your ticks. <a href="workflow.html">Open the full workflow →</a></p></div>{mapstrip("workflow.html")}</section>
<section id="projects"><div class="sec-head"><h2><span class="n">02</span>Projects</h2><p>One card per <code>projects/&lt;slug&gt;/</code>. <code>build.py</code> keeps this list current.</p></div><div class="docs">{cards}</div></section>
<section id="start"><div class="sec-head"><h2><span class="n">03</span>Start a project</h2></div><div class="steps">
<div class="step"><span class="sn">01</span><div><h4>Copy the example</h4><p><code>cp anchorframe/project.example.json anchorframe/projects/&lt;slug&gt;/project.json</code></p><p>Title, kind, format, the Higgsfield project URL and folder id, the date window.</p></div></div>
<div class="step"><span class="sn">02</span><div><h4>Write the cast as ids</h4><p>Characters, environments, props, effects — <code>name → element uuid</code>. This list is what makes a generation yours. Souls one per name.</p></div></div>
<div class="step"><span class="sn">03</span><div><h4>Write the shots</h4><p>Id, act, title, duration, audio on or off, and the prompt with <code>@[name](uuid)</code> references. Leave <code>pick</code> empty; the board chooses by score until you decide.</p></div></div>
<div class="step"><span class="sn">04</span><div><h4>Ingest the history</h4><p><code>python3 anchorframe/ingest.py anchorframe/projects/&lt;slug&gt; &lt;dump&gt; [...]</code></p><p>Dumps are the files the Higgsfield connector writes when history is paged in Claude. Anything not made with your cast is dropped and counted.</p></div></div>
<div class="step"><span class="sn">05</span><div><h4>Build and open</h4><p><code>python3 anchorframe/build.py anchorframe/projects/&lt;slug&gt;</code> · <code>python3 anchorframe/desk.py</code> · <code>anchorframe/serve.command</code>. Clips play inline when served or opened locally.</p></div></div>
<div class="step"><span class="sn">06</span><div><h4>Keys, then generate</h4><p>Export <code>keys.env</code> from the <a href="keys.html">keys page</a>. <code>python3 anchorframe/generate.py anchorframe/projects/&lt;slug&gt; --shot S5 --model &lt;cloud model id&gt; --prompt-from-shot</code>. The request id lands on the ledger on acceptance.</p></div></div></div></section>
<section id="loop"><div class="sec-head"><h2><span class="n">04</span>The loop</h2><p>{esc(W["loop"]["_"])}</p></div><div class="loop">{loop_html}</div></section>
<section id="rule"><div class="sec-head"><h2><span class="n">05</span>One folder, and what that can mean</h2></div><div class="panel">
<p><b>The desk is exclusive to one Higgsfield project.</b> It enforces that the only way the API allows: <b>admission by cast</b> (a take is yours if it was made with an element in your cast), <b>ledger on submission</b> (the desk records what it makes before it waits), and <b>a hand map</b> for anything you place yourself.</p>
<p><b>Folder placement itself stays in the web app.</b> No image model and almost no video model accepts a folder id over the API. When a rule needs the generation history to live inside the project, generate there in Cinema Studio; the desk will find those renders by their cast and lay them out.</p>
<p class="muted">History pulls come through the Higgsfield connector in Claude, which pages the account and writes files. Point <code>ingest.py</code> at them.</p></div></section>
<section id="scale"><div class="sec-head"><h2><span class="n">06</span>From short to feature to game</h2><p>{esc(W["expand"]["_"])}</p></div><div class="docs">{expand_html}</div></section>
<section id="why"><div class="sec-head"><h2><span class="n">07</span>What is different about this</h2></div><div class="docs">{unique_html}</div></section>
<section id="links"><div class="sec-head"><h2><span class="n">08</span>Links</h2><p>The eight you will open most. <a href="links.html">All {sum(len(g["links"]) for g in L["groups"])}, by stage, verified or not →</a></p></div><div class="chips" style="padding:0">{toplinks}</div></section>
<section id="tips"><div class="sec-head"><h2><span class="n">09</span>Working tips</h2><p>What one production learned, in the order you meet it. Source: <code>tips.md</code>.</p></div><div class="tips">{tips_html}</div></section>
<footer>Built by <code>anchorframe/desk.py</code> from <code>workflow.json</code>, <code>links.json</code>, <code>tips.md</code> and <code>projects/index.json</code>. Regenerate, don't hand-edit.</footer></main></body></html>'''
(D / "index.html").write_text(idx)
print(f"wrote index.html {len(idx)} · workflow.html {len(wf)} · links.html {len(lk)} — {len(W['stages'])} stages, {sum(1 for s in W['stages'] if s['gate'])} gates, {sum(len(g['links']) for g in L['groups'])} links, {len(groups)} tip groups")
