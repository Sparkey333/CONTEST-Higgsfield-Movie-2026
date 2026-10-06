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

LANE = {"A": "ships", "B": "coverage", "C": "chroma"}
def lanes_html(s, d):
    meta = f'{d}s · audio {"on" if s.get("audio") else "off"} on lane A · {esc(P["higgsfield"].get("video_model",""))} · {esc(P["format"]["aspect"])} · {esc(P["format"]["resolution"])}'
    out = []
    for l in s["lanes"]:
        c = l["c"]
        out.append(f'<div class="lane" data-lane="{esc(c)}"><div class="lh"><b class="lc">{esc(c)}</b><span class="ln">{esc(LANE.get(c, ""))}</span><h4>{esc(l.get("name",""))}</h4></div>'
                   f'<p class="lw">{esc(l.get("why",""))}</p><pre class="prompt">{mark(l["prompt"])}</pre><div class="acts pad"><button type="button" class="copy" data-copy="{esc(l["prompt"])}">Copy lane {esc(c)}</button></div></div>')
    return '<div class="lanes">' + "".join(out) + f'</div><p class="meta pad lanemeta">{meta}</p>'
SHOT = {s["id"]: s for s in P["shots"]}
def clock(x): x = int(round(x)); return f"{x//60}:{x%60:02d}"
def form_html(f):
    cut = f.get("cut") or []
    if f.get("auto") == "shots": cut = [{"shot": s["id"], "lane": "A", "s": s.get("duration_s", 0)} for s in P["shots"] if not str(s.get("status","")).startswith("merged-into:")]
    tot = sum(e.get("s", 0) for e in cut) or 1
    segs, rows, t0, part = [], [], 0, None
    for e in cut:
        sec = e.get("s", 0); sid = e.get("shot"); lane = e.get("lane", "A")
        if sid and sid in SHOT:
            tone = TONE.get(SHOT[sid]["act"], "sun"); lab = sid + ("" if lane == "A" else lane); title = SHOT[sid].get("title", sid)
        else:
            tone = "card"; lab = "card"; title = e.get("card", "card")
        tip = f'{lab} · {sec}s · {title}' + (f' — {e["note"]}' if e.get("note") else "")
        segs.append(f'<b data-tone="{tone}" style="flex:{sec}" title="{esc(tip)}">{esc(lab) if sec / tot >= 0.045 else ""}</b>')
        if e.get("part") and e["part"] != part:
            part = e["part"]; rows.append(f'<li class="part">{esc(part)}</li>')
        rows.append(f'<li><span class="tc">{clock(t0)}</span><span class="sh" data-tone="{tone}">{esc(lab)}</span><span class="se">{sec}s</span><span class="tt">{esc(title)}{(" — " + esc(e["note"])) if e.get("note") else ""}</span></li>')
        t0 += sec
    tgt = f.get("target_s")
    return (f'<article class="form" id="form-{esc(f["id"])}"><header><span class="fk">{esc(f.get("kind",""))}</span><h3>{esc(f["name"])}</h3><span class="rt">{clock(t0)}' + (f' of {clock(tgt)} target' if tgt else "") + '</span></header>'
            f'<p class="fw">{esc(f.get("why",""))}</p><div class="ribbon" aria-hidden="true">{"".join(segs)}</div>'
            f'<details><summary>The cut, in order · {len(cut)} pieces</summary><ol class="cutlist">{"".join(rows)}</ol></details></article>')
def sections():
    out, nav = [], []
    if P.get("forms"):
        nav.append(("Forms", "#forms"))
        out.append('<section class="xs" id="forms"><h2>One story, every length</h2><p class="note">' + esc(P.get("forms_note", "Every form is cut from the same shots. Lane A ships, B is coverage, C is the graded key-art take.")) + "</p>" + "".join(form_html(f) for f in P["forms"]) + "</section>")
    ep = P.get("episode")
    if ep:
        nav.append(("Episode", "#episode"))
        rows = "".join(f'<tr><td class="n">{esc(r["n"])}</td><td><b>{esc(r["scene"])}</b></td><td class="n">{esc(r["pages"])}</td><td class="n">{esc(r["min"])}</td><td>{esc(", ".join(r.get("shots", [])) or "—")}</td><td>{esc(r.get("adds",""))}</td></tr>' for r in ep["scenes"])
        out.append(f'<section class="xs" id="episode"><h2>{esc(ep.get("title","The episode"))}</h2><p class="note">{esc(ep.get("note",""))}</p><div class="tw"><table class="ep"><thead><tr><th>#</th><th>Scene</th><th>Pages</th><th>Min</th><th>In the short</th><th>The episode puts back</th></tr></thead><tbody>{rows}</tbody></table></div>'
                   + (f'<p class="note">{esc(ep["grow"])}</p>' if ep.get("grow") else "") + "</section>")
    br = P.get("bridges")
    if br:
        nav.append(("Bridges", "#bridges"))
        def bcard(k, label):
            b = br.get(k)
            if not b: return ""
            items = "".join(f'<li><b>{esc(i["from"])}</b> → {esc(i["to"])}</li>' for i in b.get("links", []))
            return f'<div class="bridge"><span class="fk">{label}</span><h3>{esc(b.get("title",""))}</h3><ul>{items}</ul>' + (f'<p class="meta">{esc(b["status"])}</p>' if b.get("status") else "") + "</div>"
        out.append(f'<section class="xs" id="bridges"><h2>Bridges</h2><p class="note">{esc(br.get("note",""))}</p><div class="bridges">{bcard("in", "In · from the episode before")}{bcard("out", "Out · to the episode after")}</div>{stills_html("bridge-out")}</section>')
    pw = P.get("power")
    if pw:
        nav.append(("Power", "#power"))
        def tcard(t):
            here = "".join(f"<li>{esc(h)}</li>" for h in t.get("here", []))
            rungs = "".join(f'<span class="chip-t" title="{esc(v)}">{esc(k)}</span>' for k, v in (t.get("rungs") or {}).items())
            return (f'<article class="tier" id="tier-{esc(t["id"])}"><header><span class="fk">{esc(t.get("rung",""))}</span><h3>{esc(t["name"])}</h3></header>'
                    f'<p class="fw">{esc(t.get("look",""))}</p>' + (f'<div class="sig">{rungs}</div>' if rungs else "") +
                    f'<dl class="fit"><dt>Book</dt><dd>{esc(t.get("book",""))}</dd><dt>Film 1</dt><dd>{esc("[" + t["mol"] + "]" if t.get("mol","").startswith("Matter") else t.get("mol",""))}</dd>'
                    f'<dt>Prompt</dt><dd><code>{esc(t.get("prompt",""))}</code></dd></dl>' + (f'<p class="fk">In this episode</p><ul class="here">{here}</ul>' if here else "") +
                    (f'<p class="meta">Next: {esc(t["next"])}</p>' if t.get("next") else "") + '</article>')
        srows = "".join(f'<tr><td><b>{esc(x["stone"])}</b></td><td>{esc(x.get("order",""))}</td><td>{esc(x.get("island",""))}</td><td>{esc(x.get("bearer",""))}</td><td>{esc(x.get("colour",""))}</td><td>{esc(("[" + x["mol"] + "]") if x.get("mol") else "")}</td></tr>' for x in pw.get("stones", []))
        en = pw.get("endings", {})
        rules = "".join(f"<li>{esc(r)}</li>" for r in pw.get("rules", []))
        out.append(f'<section class="xs" id="power"><h2>Power tiers</h2><p class="note">{esc(pw.get("_",""))}</p><ul class="rules">{rules}</ul><div class="tiers">{"".join(tcard(t) for t in pw.get("tiers", []))}</div>'
                   f'<h3 class="xs-sub">The Seven Stones</h3><div class="tw"><table class="ep"><thead><tr><th>Stone</th><th>Order</th><th>Island</th><th>Bearer</th><th>Colour</th><th>Film 1</th></tr></thead><tbody>{srows}</tbody></table></div>'
                   + (f'<h3 class="xs-sub">When a bearer dies</h3><dl class="fit"><dt>Book</dt><dd>{esc(en.get("book",""))}</dd><dt>Film 1</dt><dd>{esc(en.get("film1",""))}</dd><dt>Episode 2</dt><dd>{esc(en.get("episode2",""))}</dd></dl>' if en else "") + '</section>')
    cw = P.get("series", {}).get("crosswalk")
    if cw:
        nav.append(("Names", "#names"))
        rows = "".join(f'<tr><td><b>{esc(r["book"])}</b></td><td>[Matter of Light: {esc(r["film1"])}]</td><td>{esc(r["kind"])}</td><td>{esc(r["proof"])}</td></tr>' for r in cw["rows"])
        out.append(f'<section class="xs" id="names"><h2>Names: the book, and film 1</h2><p class="note">{esc(P["series"].get("names",""))} {esc(cw.get("_",""))}</p>'
                   f'<div class="tw"><table class="ep"><thead><tr><th>Book</th><th>Film 1</th><th>Kind</th><th>Proof</th></tr></thead><tbody>{rows}</tbody></table></div></section>')
    ca = P.get("carried")
    if ca:
        nav.append(("Cast", "#cast"))
        sheet = {x["id"]: x for x in P.get("stills", [])}
        def ccard(i):
            st = sheet.get(i.get("sheet", ""))
            art = f'<a href="{esc(st["url"])}" target="_blank" rel="noopener"><img src="{esc(st["thumb"])}" alt="{esc(i["name"])} for Episode 2" loading="lazy"></a>' if st else '<div class="noimg">not re-rendered</div>'
            soul = P.get("souls", {}).get(i["name"])
            return (f'<article class="carry">{art}<div class="cb"><h3>@{esc(i["name"])}</h3><p class="meta">{esc(i.get("label") or "from " + i.get("from",""))}' + (f' · Soul {esc(soul["soul_id"][:8])}' if isinstance(soul, dict) else "") + '</p>'
                    f'<p class="fw">{esc(i.get("tweak",""))}</p><button type="button" class="jid" data-copy="{esc(i["id"])}">{esc(i["id"])}</button></div></article>')
        mk = P.get("made") or {}
        made = (f'<h3 class="xs-sub">Made for this episode</h3><p class="note">{esc(mk.get("_",""))}</p><div class="carries">{"".join(ccard(dict(i, tweak=i.get("note",""), label="new in this episode · " + i.get("kind",""))) for i in mk.get("items", []))}</div>') if mk.get("items") else ""
        out.append(f'<section class="xs" id="cast"><h2>Cast</h2><h3 class="xs-sub">Carried over</h3><p class="note">{esc(ca.get("_",""))}</p><div class="carries">{"".join(ccard(i) for i in ca["items"])}</div>{made}</section>')
    th = P.get("themes")
    if th:
        nav.append(("Soundtrack", "#soundtrack"))
        cards = "".join(
            f'<article class="theme" id="theme-{esc(x["id"])}"><header><span class="fk">{esc(x.get("use",""))}</span><h3>{esc(x["title"])}</h3></header><p class="fw"><b>{esc(x["theme"])}</b> {esc(x.get("from",""))}</p>'
            f'<dl class="fit"><dt>Track</dt><dd>{esc(x.get("fit",""))}</dd><dt>Style</dt><dd><code>{esc(x["style"])}</code> <button type="button" class="copy sm" data-copy="{esc(x["style"])}">Copy style</button></dd></dl>'
            f'<details><summary>Lyrics · {len(x["lyrics"].split())} words</summary><pre class="lyr">{esc(x["lyrics"])}</pre><div class="acts pad"><button type="button" class="copy" data-copy="{esc(x["lyrics"])}">Copy lyrics</button></div></details></article>' for x in th["songs"])
        out.append(f'<section class="xs" id="soundtrack"><h2>{esc(th.get("title","Soundtrack"))}</h2><p class="note">{esc(th.get("note",""))}</p><div class="themes">{cards}</div></section>')
    if not out: return ""
    nav.append(("Shots", "#shots"))
    jump = '<nav class="jump">' + "".join(f'<a href="{h}">{esc(n)}</a>' for n, h in nav) + "</nav>"
    return jump + "".join(out) + '<h2 class="xs-h" id="shots">The shots</h2>'
XCSS = """
.jump{display:flex;flex-wrap:wrap;gap:6px;margin:22px 0 4px}.jump a{font:500 11px var(--mono);letter-spacing:.08em;text-transform:uppercase;text-decoration:none;color:var(--ink-2);border:1px solid var(--line);border-radius:999px;padding:6px 11px;background:var(--surface)}.jump a:hover{color:var(--ink)}
.xs{margin-top:34px}.xs>h2,.xs-h{font-size:clamp(22px,3vw,30px);margin:40px 0 8px}.xs .note{color:var(--ink-2);max-width:90ch;margin:0 0 14px}
.form,.theme,.bridge{border:1px solid var(--line);border-radius:12px;background:var(--surface);padding:16px 20px;margin-top:14px;min-width:0}
.form header,.theme header{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:baseline}.form h3,.theme h3,.bridge h3{font-size:19px;margin:0}
.fk{font:500 10.5px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}.rt{margin-left:auto;font:500 13px var(--mono);font-variant-numeric:tabular-nums}
.fw{color:var(--ink-2);margin:6px 0 10px;max-width:95ch}.form .ribbon{height:26px}
[data-tone="card"]{--t:var(--ink-3)}
.cutlist{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:3px;font-size:13.5px}.cutlist li{display:grid;grid-template-columns:44px 56px 36px minmax(0,1fr);gap:8px;align-items:baseline}
.cutlist li.part{display:block;font:500 11px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);margin-top:8px}
.cutlist .tc,.cutlist .se{font:12px var(--mono);color:var(--ink-3);font-variant-numeric:tabular-nums}.cutlist .sh{font:500 12px var(--mono);color:var(--t)}
.tw{overflow-x:auto}table.ep{border-collapse:collapse;width:100%;font-size:14px;min-width:760px}table.ep th,table.ep td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}table.ep th{font:500 10.5px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}table.ep td.n{font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}
.carries{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}.carry{border:1px solid var(--line);border-radius:12px;background:var(--surface);overflow:hidden;min-width:0;display:flex;flex-direction:column}
.carry img,.carry .noimg{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:var(--tile)}.carry .noimg{display:grid;place-items:center;font:12px var(--mono);color:var(--ink-3)}
.carry .cb{padding:12px 16px 14px;display:grid;gap:6px}.carry h3{margin:0;font:600 16px var(--mono)}.carry .meta,.carry .fw{margin:0}.carry .jid{justify-self:start;max-width:100%;overflow-wrap:anywhere}
#bridges .stills{padding:14px 0 0}
.refs{padding:0 22px 12px;display:grid;gap:6px}.sig{display:flex;flex-wrap:wrap;gap:6px;align-items:center}.sig .fk{margin-right:4px}
.chip-s,.chip-t{font:500 11.5px var(--mono);border:1px solid var(--line);border-radius:999px;padding:3px 9px;color:var(--ink-2);background:var(--surface)}.chip-t{border-style:dashed}
.tiers{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:14px;margin-top:14px}.tier{border:1px solid var(--line);border-radius:12px;background:var(--surface);padding:16px 20px;min-width:0}.tier h3{font-size:19px;margin:2px 0 0}.tier .here{margin:4px 0 0;padding-left:18px;font-size:13.5px;color:var(--ink-2)}.rules{max-width:95ch;color:var(--ink-2);padding-left:20px}.rules li{margin:4px 0}
a.chip-t{text-decoration:none}.bk{margin:2px 0;font-size:13.5px;color:var(--ink-2);max-width:100ch}.bk .fk{margin-right:6px}
.mol ul{margin:4px 0 0;padding-left:18px;font-size:13px;color:var(--ink-2)}.mol li{margin:2px 0}.mol b{font:500 12px var(--mono);color:var(--ink)}.mol code{font-size:11px}
.xs-sub{font:600 12px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);margin:22px 0 6px}
.bridges{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}.bridge ul{margin:8px 0 0;padding-left:18px;color:var(--ink-2)}.bridge li{margin:6px 0}
.themes{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:14px;align-items:start}.theme{margin-top:0}
.fit{display:grid;grid-template-columns:auto minmax(0,1fr);gap:6px 12px;margin:0 0 10px;font-size:14px}.fit dt{font:500 10.5px/1.9 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}.fit dd{margin:0;color:var(--ink-2)}.fit code{font:12px var(--mono);overflow-wrap:anywhere}
.lyr{white-space:pre-wrap;font:13px/1.6 var(--mono);max-height:none}
.copy.sm{padding:5px 9px;font-size:10px;margin-left:6px}
.lanes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;padding:0 22px}@media (max-width:1000px){.lanes{grid-template-columns:1fr}}
.lane{border:1px solid var(--line);border-radius:10px;background:var(--surface-2,var(--surface));min-width:0;display:flex;flex-direction:column}
.lane .lh{display:flex;align-items:baseline;gap:8px;padding:10px 12px 0}.lane .lc{font:600 13px var(--mono);width:22px;height:22px;display:inline-grid;place-items:center;border-radius:5px;background:var(--ink);color:var(--ground)}
.lane[data-lane="B"] .lc{background:var(--void)}.lane[data-lane="C"] .lc{background:var(--coral)}
.lane .ln{font:500 10.5px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}.lane h4{margin:0;font-size:15px}
.lane .lw{margin:6px 12px 0;font-size:13px;color:var(--ink-2)}.lane .prompt{margin:8px 12px;flex:1}.lane .acts{padding:0 12px 12px}.lanemeta{padding:8px 22px 18px;margin:0}
"""
STYLE = {x["id"]: x for x in (json.load(open(pdir.parent.parent / "style.json")).get("signatures", []) if (pdir.parent.parent / "style.json").exists() else [])}
TIERS = {t["id"]: t for t in P.get("power", {}).get("tiers", [])}
def refs_html(s):
    out = []
    if s.get("style"):
        out.append('<div class="sig"><span class="fk">House style</span>' + "".join(f'<span class="chip-s" title="{esc(STYLE[k]["rule"])}">{esc(STYLE[k]["name"])}</span>' for k in s["style"] if k in STYLE) + '</div>')
    if s.get("tiers"):
        out.append('<div class="sig"><span class="fk">Power</span>' + "".join(f'<a class="chip-t" href="#tier-{esc(t.rsplit(":",1)[-1])}" title="{esc(TIERS.get(t.rsplit(":",1)[-1], {}).get("look",""))}">{esc(t.rsplit(":",1)[0])} · {esc(TIERS.get(t.rsplit(":",1)[-1], {}).get("name", t.rsplit(":",1)[-1]))}</a>' for t in s["tiers"]) + '</div>')
    if s.get("mol_refs"):
        out.append('<div class="mol"><span class="fk">From Matter of Light (film 1)</span><ul>' + "".join(
            f'<li><b>{esc(r.get("tc") or r.get("what",""))}</b> {esc(r.get("what","") if r.get("tc") else "")}' + (f' <code>{esc(r["element"])}</code>' if r.get("element") else "") + '</li>' for r in s["mol_refs"]) + '</ul></div>')
    if s.get("book"): out.append(f'<p class="bk"><span class="fk">The book</span> {esc(s["book"])}</p>')
    if s.get("echo"): out.append(f'<p class="bk"><span class="fk">Echo of film 1</span> {esc(s["echo"])}</p>')
    return ('<div class="refs">' + "".join(out) + '</div>') if out else ""
STILLS = {}
for x in P.get("stills", []): STILLS.setdefault(x["shot"], []).append(x)
def stills_html(sid):
    xs = STILLS.get(sid)
    if not xs: return ""
    figs = "".join(f'<figure class="still"><a href="{esc(x["url"])}" target="_blank" rel="noopener"><img src="{esc(x.get("thumb") or x["url"])}" alt="{esc(sid)} lane {esc(x.get("lane",""))} still" loading="lazy"></a>'
                   f'<figcaption><b>{esc(x.get("lane",""))}</b> {esc(x.get("note",""))} <code>{esc(x["id"][:8])}</code>{" · animated" if x.get("animated") else ""}</figcaption></figure>' for x in xs)
    return f'<div class="stills"><span class="fk">Anchor stills · {esc(xs[0].get("model",""))}</span><div class="srow">{figs}</div></div>'
SCSS = """.stills{padding:0 22px 14px}.stills .srow{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px;margin-top:6px}
.still{margin:0;min-width:0}.still img{width:100%;aspect-ratio:21/9;object-fit:cover;border-radius:7px;border:1px solid var(--line);display:block;background:var(--tile)}
.still figcaption{font-size:12px;color:var(--ink-3);margin-top:4px}.still figcaption b{color:var(--ink);font-family:var(--mono)}"""
# The folder line: this board's own folder, unless the desk it ships in is another episode's. Then it is
# labelled as a reference, and the desk's lock is named as the one place this edition generates.
DESK = json.load(open(pdir.parent.parent / "desk.json")) if (pdir.parent.parent / "desk.json").exists() else {}
CURP = pdir.parent / DESK.get("current", "") / "project.json"
CURL = json.load(open(CURP)).get("higgsfield", {}).get("lock") if DESK.get("current") and DESK["current"] != pdir.name and CURP.exists() else None
FOLDER_NOTE = (f'Project folder (reference, read only): <a href="{esc(P["higgsfield"].get("project_url","#"))}">{esc(P["higgsfield"].get("project_name",""))}</a>. This desk generates only in {esc(CURL["project"])}'
               if CURL else f'Project folder: <a href="{esc(P["higgsfield"].get("project_url","#"))}">{esc(P["higgsfield"].get("project_name",""))}</a>')
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
        if s.get("lanes"): body = lanes_html(s, d)
        cards.append(f'<article class="shot new" data-tone="{tone}" id="{sid}"><header><span class="sid">{sid}</span><h3>{esc(title)}</h3><span class="dur">{d}s · unshot</span></header><p class="why">{esc(s.get("notes",""))}</p>{refs_html(s)}{stills_html(sid)}{body}</article>'); continue
    placed += 1; d = vids[pick].get("duration") or s.get("duration_s", 0); total += d
    ribbon.append(f'<b data-tone="{tone}" style="flex:{d}" title="{sid} · {d}s">{sid if d >= 10 else ""}</b>')
    ps = sc8.get(pick, {}).get("overall")
    if s.get("regenerate"): regen += 1
    rg = f'<div class="regen"><b>Make again.</b> {esc(s.get("notes",""))}</div>' if s.get("regenerate") else ""
    altdiv = "".join(tile(a, "alternate", ps) for a in alts) or '<p class="meta">No alternates in the ledger.</p>'
    cards.append(f'<article class="shot" data-tone="{tone}" id="{sid}"><header><span class="sid">{sid}</span><h3>{esc(title)}</h3><span class="dur">{d}s</span></header><p class="why">{esc(s.get("why",""))}</p>{rg}{refs_html(s)}{stills_html(sid)}<div class="row"><div class="pickcol">{tile(pick, "pick")}</div><div class="altcol">{altdiv}</div></div></article>')

mm = f"{int(total)//60}:{int(total)%60:02d}"; n = len([k for k in sc8 if k in vids]); hf = P["higgsfield"]
legend = " ".join(f'<span><i data-tone="{a.get("tone","sun")}"></i>{esc(a["id"])} · {esc(a["name"])}</span>' for a in P["acts"])
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(P["title"])} · Shot Board</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Archivo:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{--ground:#F2EFE8;--surface:#FBF9F5;--surface-2:#E9E4D9;--line:#CFC7B6;--line-soft:#E2DCCE;--ink:#171410;--ink-2:#4A443B;--ink-3:#7A7264;--sun:#9A6208;--stardust:#6E55C9;--forest:#2C7A4B;--lake:#1E7C97;--dark:#4B3F70;--void:#3E39C9;--coral:#B33A18;--good:#0A6B45;--good-soft:#CFEEE0;--warn:#8A4B00;--warn-soft:#FBE6CC;--bad:#9C2A2A;--tile:#1A1713;--ref:#B4482C;
--display:"Fraunces","Iowan Old Style",Palatino,Georgia,serif;--body:"Archivo",ui-sans-serif,system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--ground:#0D0B09;--surface:#161311;--surface-2:#211D19;--line:#3B342C;--line-soft:#241F1A;--ink:#F4EFE4;--ink-2:#B0A797;--ink-3:#7D7466;--sun:#EDB44C;--stardust:#C3B4FF;--forest:#6FD39A;--lake:#6BD0EC;--dark:#A596D6;--void:#9B97FF;--coral:#FF8D63;--good:#4FD9A2;--good-soft:#082C1F;--warn:#F0B36A;--warn-soft:#33220C;--bad:#F08A8A;--tile:#0A0908;--ref:#E2795C}}}}
:root[data-theme="dark"]{{--ground:#0D0B09;--surface:#161311;--surface-2:#211D19;--line:#3B342C;--line-soft:#241F1A;--ink:#F4EFE4;--ink-2:#B0A797;--ink-3:#7D7466;--sun:#EDB44C;--stardust:#C3B4FF;--forest:#6FD39A;--lake:#6BD0EC;--dark:#A596D6;--void:#9B97FF;--coral:#FF8D63;--good:#4FD9A2;--good-soft:#082C1F;--warn:#F0B36A;--warn-soft:#33220C;--bad:#F08A8A;--tile:#0A0908;--ref:#E2795C}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--ground);color:var(--ink);font:15px/1.6 var(--body);padding-inline:clamp(16px,3vw,26px);padding-block:0 80px}}
.wrap{{max-width:1240px;margin:0 auto}} h1,h2,h3{{margin:0;font-family:var(--display);font-weight:600;letter-spacing:-.012em;text-wrap:balance}} p{{margin:0}}
.eyebrow{{font-family:var(--mono);font-size:10.5px;letter-spacing:.19em;text-transform:uppercase;color:var(--ink-3)}} .eyebrow a{{color:inherit}}
.mast{{padding:40px 0 26px;border-bottom:1px solid var(--line);display:flex;flex-direction:column;gap:16px}} .mast h1{{font-size:clamp(32px,5vw,54px);line-height:1.02}}
.lede{{font-size:16.5px;color:var(--ink-2);max-width:70ch}} .kpis{{display:flex;flex-wrap:wrap;gap:10px}} .kpi{{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:10px 14px;min-width:118px}}
.kpi b{{display:block;font:600 24px/1 var(--display);font-variant-numeric:tabular-nums}} .kpi span{{font-size:12px;color:var(--ink-3)}}
.ribbon{{display:flex;height:32px;gap:1px;border-radius:5px;overflow:hidden}} .ribbon b{{display:flex;align-items:center;justify-content:center;min-width:0;font:400 9.5px var(--mono);color:#fff;overflow:hidden}}
[data-tone="sun"]{{--t:var(--sun)}} [data-tone="void"]{{--t:var(--void)}} [data-tone="coral"]{{--t:var(--coral)}} [data-tone="stardust"]{{--t:var(--stardust)}} [data-tone="forest"]{{--t:var(--forest)}} [data-tone="lake"]{{--t:var(--lake)}} [data-tone="dark"]{{--t:var(--dark)}} .ribbon b{{background:var(--t)}} .ribbon b.new{{outline:2px dashed #fff;outline-offset:-4px;opacity:.75}}
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
{XCSS}{SCSS}</style></head><body><div class="wrap">
<header class="mast"><p class="eyebrow"><a href="../../index.html">anchorframe</a> · {esc(P["title"])} · built {datetime.datetime.utcnow().strftime("%d %b %Y %H:%M")} UTC</p>
<h1>{esc(P["title"])} — the cut, take by take</h1>
<p class="lede">{esc(P.get("logline",""))}</p>
<div class="kpis"><div class="kpi"><b>{len(P["shots"])}</b><span>shots in the cut</span></div><div class="kpi"><b>{len(G)}</b><span>takes admitted to this project</span></div><div class="kpi"><b>{placed}</b><span>shots with a pick</span></div><div class="kpi"><b>{n}</b><span>takes scored</span></div><div class="kpi"><b>{regen}</b><span>to make again</span></div><div class="kpi"><b>{unshot}</b><span>not yet shot</span></div><div class="kpi"><b>{mm}</b><span>runtime of picks + unshot</span></div></div>
<div class="ribbon" aria-hidden="true">{"".join(ribbon)}</div><div class="legend">{legend}<span>dashed — not yet shot</span></div>
<p class="note">{FOLDER_NOTE} · video on <code>{esc(hf.get("video_model",""))}</code> · {esc(P["format"]["aspect"])} · {esc(P["format"]["resolution"])} · {P["format"].get("fps",24)} fps. Clips play inline when this file is opened locally; in a sandboxed viewer each tile shows its identity card and an <em>open the clip</em> link.</p></header>
{sections()}{"".join(cards)}
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
