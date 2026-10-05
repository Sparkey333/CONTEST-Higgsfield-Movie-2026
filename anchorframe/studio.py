#!/usr/bin/env python3
"""Build the Anchorframe studio: the working app for one project. Tabs: Start, Questions (the intake),
Uploads (asset storage), Higgsfield (live project, credits), Generate (sheets, shots, ledger), Parity.

    python3 anchorframe/studio.py [--fragment OUT] [--desk-href desk.html]

Reads desk.json (which project is current), intake.json (the template), projects/<slug>/intake.json
(proposed answers), projects/<slug>/project.json and parity.json. Writes anchorframe/studio.html.
In a claude.ai viewer the page saves to its shared store, uploads assets, and calls the viewer's
Higgsfield connector; opened locally it shows the plan and the prompts read-only.
"""
import json, re, sys, html, pathlib, datetime
D = pathlib.Path(__file__).resolve().parent
args = sys.argv[1:]
def opt(n, default=None): return args[args.index(n) + 1] if n in args else default
DK = json.load(open(D / "desk.json")); slug = DK["current"]; PD = D / "projects" / slug
P = json.load(open(PD / "project.json", encoding="utf-8")); I = json.load(open(D / "intake.json", encoding="utf-8"))
PR = json.load(open(PD / "intake.json", encoding="utf-8")) if (PD / "intake.json").exists() else {"proposed": {}}
PAR = json.load(open(D / "parity.json", encoding="utf-8"))
esc = lambda t: html.escape(str(t), quote=True)
hf = P["higgsfield"]; PENDING = "<element uuid>"

# cast: every name with kind, id (None when pending) and brief
cast = {}
for kind in ("characters", "environments", "props", "fx"):
    for name, uid in P["cast"].get(kind, {}).items():
        if name == "_": continue
        cast[name] = {"kind": kind, "id": None if uid == PENDING else uid, "brief": P.get("sheets", {}).get(kind, {}).get(name, "")}
def sheet_prompt(name, c):
    b = c["brief"]; label = name.replace("-", " ")
    tail = " Photoreal, cinematic. No text, no letters, no labels, no numbers, no watermark anywhere."
    if name.startswith("plate-"):
        return ("Lighting plate for a film movement: " + b + " An empty frame with no subject and no people: only the light, colour and contrast that every frame of this movement inherits. 21:9." + tail), "21:9"
    if c["kind"] == "characters":
        return ("Character reference sheet for " + label + ": " + b + " Plain light-grey studio background, even soft light. Full-body front, three-quarter and profile views, plus one head-and-shoulders close-up, all the same figure. Every person shown is an adult, 18 or older." + tail), "16:9"
    if c["kind"] == "environments":
        return ("Environment reference sheet for " + label + ": " + b + " Three views on one sheet: a wide establishing view, a medium view and a detail. No people." + tail), "16:9"
    if c["kind"] == "props":
        return ("Prop reference sheet for " + label + ": " + b + " On a plain light-grey background: three angles and one close detail." + tail), "16:9"
    return ("Effect reference sheet for " + label + ": " + b + " Three stages of the effect side by side on a dark neutral background. No people." + tail), "16:9"
sheets = []
for name, c in cast.items():
    if c["id"] is None:
        pr, ar = sheet_prompt(name, c); sheets.append({"name": name, "kind": c["kind"], "brief": c["brief"], "prompt": pr, "aspect": ar})
shots = [{"id": s["id"], "act": s["act"], "title": s["title"], "d": s["duration_s"], "audio": s["audio"], "notes": s.get("notes", ""),
          "lanes": s.get("lanes") or [{"c": "A", "name": "As boarded", "why": "", "prompt": s["prompt"]}]} for s in P["shots"]]
acts = {a["id"]: a["name"] for a in P["acts"]}
ctx = [f"Film: {P['title']} ({DK.get('edition','')}), by {P.get('byline','')}. Logline: {P.get('logline','')}",
       "Movements: " + "; ".join(f"{a['id']} {a['name']}: " + ", ".join(f"{s['id']} {s['title']}" for s in P["shots"] if s["act"] == a["id"]) for a in P["acts"]),
       "Cast and places: " + "; ".join(f"{n} ({c['kind'][:-1]}{', exists' if c['id'] else ''}): {c['brief'][:160]}" for n, c in cast.items()),
       "Episode scenes: " + "; ".join(f"{r['n']} {r['scene']} ({r['min']} min)" for r in P.get("episode", {}).get("scenes", [])),
       "Songs: " + ", ".join(x["title"] for x in P.get("themes", {}).get("songs", [])),
       "Format: " + f"{P['format']['aspect']} {P['format']['resolution']} {P['format'].get('fps', 24)} fps; video model {hf.get('video_model')}; image model {hf.get('image_model')}."]
data = {
 "desk": {k: DK.get(k) for k in ("title", "edition", "episode", "editions")},
 "project": {"slug": slug, "title": P["title"], "logline": P.get("logline", ""), "acts": acts,
             "hf": {k: hf.get(k) for k in ("project_id", "workspace_id", "folder_id", "project_url", "video_model", "image_model", "lock")}},
 "intake": I, "proposed": PR.get("proposed", {}), "shots": shots, "cast": cast, "sheets": sheets, "parity": PAR,
 "links": {"desk": "index.html", "board": f"projects/{slug}/board.html", "workflow": "workflow.html", "links": "links.html", "keys": "keys.html"},
 "context": "\n".join(ctx), "built": datetime.datetime.utcnow().strftime("%d %b %Y %H:%M UTC")}
DATA = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

desk_src = (D / "desk.py").read_text(encoding="utf-8")
TOKENS = re.search(r'(:root\{--ground.*?:root\[data-theme="dark"\]\{[^\n]*\})', desk_src, re.S).group(1)
CSS = TOKENS + r"""
/* The studio: a header with live status, sticky tabs, one working surface per tab. Desk tokens throughout. */
*{box-sizing:border-box} html{scroll-padding-top:70px} body{margin:0;background:var(--ground);color:var(--ink);font:15.5px/1.55 var(--body);padding-block:0 80px}
a{color:inherit} button{font:inherit;color:inherit} code{font:12.5px/1.45 var(--mono);background:var(--surface-2);border:1px solid var(--line-soft);border-radius:4px;padding:1px 5px;overflow-wrap:anywhere}
.wrap{max-width:1180px;margin:0 auto;padding-inline:max(16px,3vw)}
h1,h2,h3,h4{margin:0;text-wrap:balance} .muted{color:var(--ink-3)} [hidden]{display:none!important}
header.top{background:linear-gradient(180deg,var(--surface),var(--ground));border-bottom:1px solid var(--line);padding-block:30px 18px}
.eyebrow{font:600 10.5px/1 var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--ink-3);margin:0 0 10px;display:flex;flex-wrap:wrap;gap:6px 14px}
.eyebrow a{text-decoration:none;color:var(--ink-3)} .eyebrow a:hover{color:var(--ink)}
h1{font:400 clamp(30px,5vw,48px)/1.04 var(--display);letter-spacing:-.01em} h1 small{font:400 .55em var(--display);color:var(--ink-3);margin-left:8px}
.lede{margin:8px 0 0;max-width:70ch;color:var(--ink-2)}
.status{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.st{display:inline-flex;align-items:center;gap:8px;font:600 11px/1 var(--mono);letter-spacing:.06em;padding:7px 10px;border-radius:6px;border:1px solid var(--line);background:var(--surface);color:var(--ink-2);text-decoration:none;cursor:pointer}
.st b{color:var(--ink);font-variant-numeric:tabular-nums} .st i{width:8px;height:8px;border-radius:50%;background:var(--ink-3);flex:none} .st.ok i{background:var(--jade)} .st.warn i{background:var(--gold)} .st.bad i{background:var(--coral)}
nav.tabs{position:sticky;top:env(safe-area-inset-top,0px);z-index:9;background:color-mix(in srgb,var(--ground) 93%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
nav.tabs .wrap{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none} nav.tabs a{font:600 11px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);text-decoration:none;padding:15px 12px;border-bottom:2px solid transparent;white-space:nowrap}
nav.tabs a[aria-current="page"]{color:var(--ink);border-bottom-color:var(--gold-line)} nav.tabs a:hover{color:var(--ink)} nav.tabs .sep{flex:1}
nav.tabs a.out{color:var(--ink-3);font-weight:500}
main{padding-block:26px}
.banner{border:1px solid var(--gold-line);background:var(--gold-soft);border-radius:9px;padding:11px 15px;margin-bottom:18px;font-size:14px;color:var(--ink-2)} .banner b{color:var(--ink)}
.sec-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 16px;margin:0 0 6px} .sec-h h2{font:400 26px/1.15 var(--display)} .sec-p{margin:0 0 18px;color:var(--ink-2);max-width:78ch}
.card{background:var(--surface);border:1px solid var(--line);border-radius:11px;padding:16px 18px;box-shadow:var(--shadow);min-width:0}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:14px;align-items:start}
.btn{font:600 12px/1 var(--body);letter-spacing:.04em;padding:9px 13px;border-radius:7px;border:1px solid var(--line);background:var(--surface-2);color:var(--ink);cursor:pointer;white-space:nowrap}
.btn:hover{border-color:var(--ink-3)} .btn.pri{background:var(--ink);color:var(--ground);border-color:var(--ink)} .btn.go{background:var(--jade);border-color:var(--jade);color:#fff} .btn.warn{background:var(--coral);border-color:var(--coral);color:#fff}
.btn:disabled{opacity:.5;cursor:not-allowed} .btn.sm{padding:6px 9px;font-size:11px}
.btn:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible,nav.tabs a:focus-visible,.chip:focus-visible{outline:2px solid var(--void);outline-offset:2px}
input[type=text],input[type=number],textarea,select{font:inherit;font-size:14.5px;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:7px;padding:8px 10px;width:100%;min-width:0}
textarea{min-height:84px;resize:vertical;line-height:1.5} label.lb{display:block;font:600 10.5px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);margin:0 0 6px}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
/* steps */
.steps{display:flex;flex-direction:column;border-top:1px solid var(--line)} .step{display:grid;grid-template-columns:44px minmax(0,1fr) auto;gap:14px;align-items:center;padding:14px 0;border-bottom:1px solid var(--line-soft)}
.step .sn{font:600 13px var(--mono);color:var(--ink-3)} .step h3{font:600 16px/1.3 var(--body)} .step p{margin:3px 0 0;font-size:14px;color:var(--ink-2)} .step.done .sn{color:var(--jade)}
@media (max-width:640px){.step{grid-template-columns:32px minmax(0,1fr)}.step .btn{grid-column:2;justify-self:start}}
.tw{overflow-x:auto} table{border-collapse:collapse;width:100%;font-size:14px} th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line-soft);vertical-align:top} th{font:600 10px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);white-space:nowrap}
td.num{font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}
.copybox{display:flex;gap:8px;align-items:center;flex-wrap:wrap;background:var(--surface-2);border:1px dashed var(--line);border-radius:8px;padding:10px 12px;margin-top:10px} .copybox code{font-size:14px;background:none;border:0}
/* questions */
.qsec{margin:26px 0 8px;font:600 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--ink-3)}
.q{background:var(--surface);border:1px solid var(--line);border-radius:11px;padding:16px 18px;margin-top:12px}
.q header{display:flex;gap:12px;align-items:baseline} .q .qn{font:600 12px var(--mono);color:var(--ink-3)} .q h3{font:600 16.5px/1.35 var(--body);flex:1}
.qs{font:600 10px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;padding:5px 7px;border-radius:4px;border:1px solid var(--line);color:var(--ink-3);white-space:nowrap}
.qs.ok{color:var(--jade);border-color:var(--jade-line);background:var(--jade-soft)} .qs.busy{color:var(--gold);border-color:var(--gold-line)}
.q .why{margin:6px 0 10px;color:var(--ink-2);font-size:14px;max-width:80ch}
.prop{border-left:3px solid var(--gold-line);background:var(--gold-soft);border-radius:0 7px 7px 0;padding:8px 12px;margin:0 0 10px;font-size:14px;color:var(--ink-2);display:flex;gap:12px;align-items:flex-start;flex-wrap:wrap}
.prop span{flex:1;min-width:200px} .prop b{display:block;font:600 10px/1.6 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--gold)}
.chips{display:flex;flex-wrap:wrap;gap:6px} .chip{font:600 12.5px/1 var(--body);padding:8px 12px;border-radius:999px;border:1.5px solid var(--line);background:var(--surface);cursor:pointer}
.chip[aria-pressed="true"]{border-color:var(--void);background:var(--void-soft);color:var(--void)}
.feeds{margin:8px 0 0;font:11px var(--mono);color:var(--ink-3)} .sug{margin-top:8px;font-size:14px;color:var(--ink-2);background:var(--void-soft);border-radius:7px;padding:9px 12px;white-space:pre-wrap}
/* uploads */
.files{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.file{border:1px solid var(--line);border-radius:9px;background:var(--surface);overflow:hidden;display:flex;flex-direction:column;min-width:0}
.file .pv{aspect-ratio:16/9;background:var(--surface-3);display:flex;align-items:center;justify-content:center;font:600 12px var(--mono);color:var(--ink-3);max-width:100%}
.file .pv img,.file .pv video{width:100%;height:100%;object-fit:cover;display:block}
.file .fi{padding:9px 11px;font-size:13px;display:flex;flex-direction:column;gap:3px} .file .fi b{overflow-wrap:anywhere} .file .fi span{color:var(--ink-3);font:11px var(--mono)}
.meter{height:8px;border-radius:5px;background:var(--surface-3);overflow:hidden;margin-top:6px} .meter i{display:block;height:100%;background:var(--void)}
.msg{font-size:13.5px;margin-top:8px} .msg.bad{color:var(--coral)} .msg.ok{color:var(--jade)}
.idea{border-left:3px solid var(--void-line);padding:6px 0 6px 12px;margin:10px 0;font-size:14px;white-space:pre-wrap} .idea span{display:block;font:11px var(--mono);color:var(--ink-3);margin-top:3px}
/* generate */
.seg{display:inline-flex;border:1px solid var(--line);border-radius:8px;overflow:hidden;margin-bottom:16px} .seg button{border:0;background:var(--surface);padding:9px 14px;font:600 12px var(--body);cursor:pointer;border-right:1px solid var(--line)} .seg button:last-child{border-right:0} .seg button[aria-pressed="true"]{background:var(--ink);color:var(--ground)}
.shot{background:var(--surface);border:1px solid var(--line);border-radius:11px;margin-top:12px;overflow:hidden}
.shot>header{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:baseline;padding:12px 16px;border-bottom:1px solid var(--line-soft)} .shot .sid{font:600 12px var(--mono);color:var(--ink-3)} .shot h3{font:600 16px/1.3 var(--body);flex:1;min-width:160px} .shot .meta{font:11.5px var(--mono);color:var(--ink-3)}
.shot .ctl{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:10px 16px;border-bottom:1px solid var(--line-soft)} .shot .ctl select{width:auto} .shot .ctl input{flex:1;min-width:180px}
.lanes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0} @media (max-width:980px){.lanes{grid-template-columns:1fr}}
.lane{padding:12px 16px;border-right:1px solid var(--line-soft);min-width:0;display:flex;flex-direction:column;gap:8px} .lane:last-child{border-right:0} @media (max-width:980px){.lane{border-right:0;border-bottom:1px solid var(--line-soft)}}
.lane .lh{display:flex;gap:8px;align-items:baseline} .lane .lc{font:700 12px var(--mono);width:20px;height:20px;display:inline-grid;place-items:center;border-radius:4px;background:var(--ink);color:var(--ground);flex:none}
.lane[data-c="B"] .lc{background:var(--void)} .lane[data-c="C"] .lc{background:var(--coral)} .lane h4{font:600 14px/1.3 var(--body)} .lane .lw{font-size:13px;color:var(--ink-2);margin:0}
details summary{cursor:pointer;font-size:12.5px;color:var(--ink-3)} pre.pr{white-space:pre-wrap;font:12px/1.55 var(--mono);background:var(--surface-2);border:1px solid var(--line-soft);border-radius:6px;padding:9px;margin:6px 0 0;max-height:260px;overflow:auto}
.pend{font-size:12.5px;color:var(--gold);background:var(--gold-soft);border-radius:6px;padding:6px 9px} .pend code{font-size:11.5px}
.gen{display:flex;flex-wrap:wrap;gap:6px;align-items:center} .gen select,.gen input{width:auto;font-size:13px;padding:6px 8px} .gen input[type=number]{width:70px}
.confirm{display:flex;flex-wrap:wrap;gap:8px;align-items:center;background:var(--coral-soft);border:1px solid var(--coral-line);border-radius:8px;padding:8px 10px;font-size:13.5px}
.res{font-size:12.5px;color:var(--ink-2)} .ow{font-size:12.5px;color:var(--ink-3);display:inline-flex;gap:5px;align-items:center} .res.bad{color:var(--coral)} .res.ok{color:var(--jade)}
.sheet{background:var(--surface);border:1px solid var(--line);border-radius:11px;padding:13px 16px;margin-top:10px;display:grid;grid-template-columns:minmax(0,1fr) minmax(240px,auto);gap:10px 18px;align-items:start} @media (max-width:760px){.sheet{grid-template-columns:1fr}}
.sheet h3{font:600 15.5px/1.3 var(--body)} .sheet .k{font:600 10px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)} .sheet p{margin:4px 0 0;font-size:13.5px;color:var(--ink-2)}
.pill{font:600 10px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;padding:5px 7px;border-radius:4px;border:1px solid var(--line);color:var(--ink-3);white-space:nowrap} .pill.built,.pill.ok{background:var(--jade-soft);color:var(--jade);border-color:var(--jade-line)} .pill.partial{background:var(--gold-soft);color:var(--gold);border-color:var(--gold-line)} .pill.planned{background:var(--void-soft);color:var(--void);border-color:var(--void-line)} .pill.none{color:var(--ink-3)}
.par td:nth-child(n+2):not(:last-child){white-space:nowrap} .par td:last-child{color:var(--ink-2);font-size:13px;min-width:220px}
.plan{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px} .plan .card h3{font:600 12px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin-bottom:8px} .plan ul{margin:0;padding-left:18px;font-size:14px;color:var(--ink-2)} .plan li{margin:5px 0}
.ask textarea{min-height:70px} .ans{white-space:pre-wrap;font-size:14.5px;color:var(--ink-2);margin-top:10px}
footer{margin-top:40px;padding-top:12px;border-top:1px solid var(--line);font:12px var(--mono);color:var(--ink-3)}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

JS = r"""
(function(){
'use strict';
const D = JSON.parse(document.getElementById('studio-data').textContent);
const HF = 'Higgsfield', PID = D.project.hf.project_id, WS = D.project.hf.workspace_id, FOLDER = D.project.hf.folder_id;
const VIDEO_MODEL = D.project.hf.video_model, IMAGE_MODEL = D.project.hf.image_model, LOCK = D.project.hf.lock || null;
const lockOk = () => !!LOCK && LOCK.folder_id === FOLDER && LOCK.project_id === PID;
// A locked studio lists exactly the locked folder (no other folders, no descendants), so what it shows is what the episode holds.
const listArgs = () => Object.assign({workspace_id: WS, project_id: PID, size: 50}, lockOk() ? {folder_id: FOLDER} : {});
const QS = D.intake.questions, SECTIONS = D.intake.sections;
const PENDING = new Set(Object.keys(D.cast).filter(n => !D.cast[n].id));
const KINDS = [
 {id:'source', name:'Source', what:'Manuscript, screenplays, transition pages', types:'PDF, Markdown, text'},
 {id:'ideas', name:'Ideas', what:'Notes, treatments, lists', types:'Markdown, text, PDF'},
 {id:'look', name:'Look', what:'Mood frames, palettes, lighting references', types:'Images, video'},
 {id:'cast', name:'Cast', what:'Character, place and prop references; tag with the element name', types:'Images'},
 {id:'music', name:'Music', what:'A track as video, or a lyric sheet', types:'MP4, WebM, text'},
 {id:'takes', name:'Outside clips', what:'Footage made outside Higgsfield', types:'MP4, WebM'},
 {id:'other', name:'Other', what:'Anything else worth keeping with the project', types:'Any accepted type'}];
const EXT = {pdf:'application/pdf', md:'text/markdown', markdown:'text/markdown', txt:'text/plain', csv:'text/csv', json:'application/json',
 png:'image/png', jpg:'image/jpeg', jpeg:'image/jpeg', webp:'image/webp', gif:'image/gif', svg:'image/svg+xml', mp4:'video/mp4', webm:'video/webm'};
const OK_TYPES = new Set(Object.values(EXT));
const S = {answers:{}, uploads:[], ideas:[], shots:{}, jobs:[], links:{}, usage:null, ro:false, uid:null, canWrite:null,
 hf:{state:'idle', perm:null, credits:null, plan:null, items:[], more:false, cursor:null, err:null, storedAt:null}, view:'sheets'};
let db = null, assets = null, mcp = null, sample = null, perms = null, unwatch = [];

const $ = (s, r) => (r || document).querySelector(s);
function h(tag, props){ const e = document.createElement(tag); const kids = [].slice.call(arguments, 2);
 if (props) for (const k in props){ const v = props[k]; if (v == null || v === false) continue;
  if (k === 'class') e.className = v; else if (k === 'text') e.textContent = v; else if (k.slice(0,2) === 'on') e.addEventListener(k.slice(2), v); else e.setAttribute(k, v === true ? '' : v); }
 kids.flat(9).forEach(k => { if (k == null || k === false) return; e.append(k.nodeType ? k : document.createTextNode(String(k))); }); return e; }
const now = () => new Date().toISOString();
const when = iso => { if (!iso) return ''; const d = new Date(iso); return isNaN(d) ? '' : d.toLocaleString(undefined, {month:'short', day:'numeric', hour:'2-digit', minute:'2-digit'}); };
const mb = b => (b / 1048576).toFixed(b < 1048576 ? 2 : 1) + ' MB';
async function copy(text, btn){ const o = btn.textContent; try { await navigator.clipboard.writeText(text); btn.textContent = 'Copied'; } catch(e){ btn.textContent = 'Select and copy'; } setTimeout(() => btn.textContent = o, 1400); }
const answered = q => { const a = S.answers[q.id]; const v = a && a.value; return Array.isArray(v) ? v.length > 0 : !!(v && String(v).trim()); };

/* ---------- shared store ---------- */
const chains = {};
function write(path, fn){ const p = (chains[path] || Promise.resolve()).then(fn); chains[path] = p.catch(() => {}); return p.catch(e => { dbErr(e); throw e; }); }
function dbErr(e){ const c = e && e.code;
 if (c === 'invalid_argument' && S.canWrite !== true){ S.ro = true; banner('You can read this studio, but your sharing level does not let you change it. Ask the owner for Contributor access.'); }
 else if (c === 'quota_exceeded') banner('The studio is full: ' + (e.message || 'a storage cap was reached') + '. Delete old ideas or ledger rows, then try again.');
 else if (c === 'revoked') banner('Access to this studio changed while it was open. Reload the page.');
 else if (c === 'resource_exhausted') banner('Too many changes at once. Wait a few seconds and try again.'); }
function banner(text){ const b = $('#banner'); b.textContent = text; b.hidden = false; }
function subscribe(){
 const on = (col, fn) => db.collection(col).onSnapshot(fn, dbErr);
 on('answers', s => { S.answers = {}; s.docs.forEach(d => S.answers[d.id] = d.data()); syncQuestions(); renderStatus(); renderStart(); });
 on('uploads', s => { S.uploads = s.docs.map(d => Object.assign({key:d.id}, d.data())).sort((a, b) => (b.at || '').localeCompare(a.at || '')); renderUploads(); renderStatus(); renderStart(); });
 on('ideas', s => { S.ideas = s.docs.map(d => Object.assign({key:d.id}, d.data())).sort((a, b) => (b.at || '').localeCompare(a.at || '')); renderIdeas(); });
 on('shots', s => { S.shots = {}; s.docs.forEach(d => S.shots[d.id] = d.data()); syncShots(); renderStatus(); });
 on('jobs', s => { S.jobs = s.docs.map(d => Object.assign({key:d.id}, d.data())).sort((a, b) => (b.at || '').localeCompare(a.at || '')); renderLedger(); renderStatus(); });
 on('links', s => { S.links = {}; s.docs.forEach(d => S.links[d.id] = d.data()); renderHFItems(); renderSheetsCounts(); renderStatus(); renderStart(); });
}

/* ---------- header status ---------- */
function renderStatus(){
 const nq = QS.filter(answered).length, sheetsDone = D.sheets.filter(s => linkedTo('sheet:' + s.name).length).length;
 const takes = Object.values(S.links).filter(l => l.target && l.target.indexOf('shot:') === 0).length;
 const hf = S.hf.state === 'live' ? (S.hf.credits != null ? Math.round(S.hf.credits).toLocaleString() + ' credits' : 'connected') : (S.hf.state === 'error' ? 'needs attention' : 'not connected');
 const chip = (cls, label, val, tab) => h('a', {class:'st ' + cls, href:'#' + tab}, h('i'), label, ' ', h('b', null, val));
 $('#status').replaceChildren(
  chip(nq === QS.length ? 'ok' : nq ? 'warn' : '', 'Questions', nq + ' / ' + QS.length, 'questions'),
  chip(S.uploads.length ? 'ok' : '', 'Uploads', S.uploads.length, 'uploads'),
  chip(S.hf.state === 'live' ? 'ok' : S.hf.state === 'error' ? 'bad' : '', 'Higgsfield', hf, 'higgsfield'),
  chip(sheetsDone === D.sheets.length ? 'ok' : sheetsDone ? 'warn' : '', 'Sheets', sheetsDone + ' / ' + D.sheets.length, 'generate'),
  chip(takes ? 'ok' : '', 'Takes logged', takes, 'generate'));
}
const linkedTo = target => Object.keys(S.links).filter(k => S.links[k].target === target);

/* ---------- tabs ---------- */
const TABS = ['start', 'questions', 'uploads', 'higgsfield', 'generate', 'parity'];
function show(tab){ if (TABS.indexOf(tab) < 0) tab = 'start'; TABS.forEach(t => { $('#tab-' + t).hidden = t !== tab; const a = $('#nav-' + t); if (t === tab) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
 try { localStorage.setItem('af-studio-tab', tab); } catch(e){} }
window.addEventListener('hashchange', () => { const t = location.hash.slice(1); if (TABS.indexOf(t) >= 0){ show(t); window.scrollTo(0, 0); } });

/* ---------- start ---------- */
function renderStart(){
 const nq = QS.filter(answered).length, sheetsDone = D.sheets.filter(s => linkedTo('sheet:' + s.name).length).length;
 const steps = [
  {done: nq === QS.length, t: 'Answer the questions', p: nq + ' of ' + QS.length + ' answered. Each one says what it decides and where it goes in the project; most have a proposal to accept.', tab: 'questions', b: 'Open questions'},
  {done: S.uploads.some(u => u.kind === 'source'), t: 'Upload the source and your references', p: 'Manuscript pages, the Episode 1 transition pages, look and cast references. ' + S.uploads.length + ' file' + (S.uploads.length === 1 ? '' : 's') + ' stored so far.', tab: 'uploads', b: 'Open uploads'},
  {done: S.hf.state === 'live', t: 'Connect Higgsfield', p: S.hf.state === 'live' ? 'Connected' + (S.hf.credits != null ? ': ' + Math.round(S.hf.credits).toLocaleString() + ' credits on ' + (S.hf.plan || 'your plan') : '') + '.' : 'Uses your own Higgsfield connector; nothing is spent until you confirm a cost.', tab: 'higgsfield', b: 'Open Higgsfield'},
  {done: sheetsDone === D.sheets.length, t: 'Make the cast sheets', p: sheetsDone + ' of ' + D.sheets.length + ' sheets have an image assigned. Generate each one, then assign the image you like to its element.', tab: 'generate', b: 'Open sheets'},
  {done: false, t: 'Sync with Claude', p: 'Claude reads everything saved here, writes it into the project, turns assigned sheets into elements and fills every pending id. Then the shots can be generated.', tab: null}];
 $('#start-steps').replaceChildren(...steps.map((s, i) => h('div', {class:'step' + (s.done ? ' done' : '')}, h('span', {class:'sn'}, s.done ? '✓' : String(i + 1).padStart(2, '0')),
  h('div', null, h('h3', null, s.t), h('p', null, s.p)), s.tab ? h('a', {class:'btn', href:'#' + s.tab}, s.b) : h('span'))));
}

/* ---------- questions ---------- */
const qEls = {};
function currentValue(id){ const el = qEls[id]; if (!el) return ''; return el.get(); }
function buildQuestions(){
 const root = $('#q-list'); root.replaceChildren();
 SECTIONS.forEach(sec => {
  root.append(h('h3', {class:'qsec'}, sec.name));
  QS.filter(q => q.section === sec.id).forEach(q => {
   const prop = D.proposed[q.id]; const hasProp = Array.isArray(prop) ? prop.length > 0 : !!(prop && String(prop).trim());
   const state = h('span', {class:'qs'}, 'Not answered'); let field, get, set;
   if (q.kind === 'choice' || q.kind === 'multi'){
    const sel = new Set(); field = h('div', {class:'chips', role:'group', 'aria-label':q.q});
    const btns = q.options.map(o => { const b = h('button', {type:'button', class:'chip', 'aria-pressed':'false', onclick: () => { if (q.kind === 'choice'){ sel.clear(); sel.add(o); } else { sel.has(o) ? sel.delete(o) : sel.add(o); } paint(); save(q, get()); }}, o); return b; });
    const paint = () => btns.forEach((b, i) => b.setAttribute('aria-pressed', sel.has(q.options[i]) ? 'true' : 'false'));
    field.append(...btns);
    get = () => q.kind === 'choice' ? ([...sel][0] || '') : q.options.filter(o => sel.has(o));
    set = v => { sel.clear(); (Array.isArray(v) ? v : (v ? [v] : [])).forEach(x => sel.add(x)); paint(); };
   } else {
    field = q.kind === 'text' ? h('input', {type:'text', id:'f-' + q.id, 'aria-label':q.q}) : h('textarea', {id:'f-' + q.id, 'aria-label':q.q});
    let t = null; field.addEventListener('input', () => { state.textContent = 'Typing…'; state.className = 'qs busy'; clearTimeout(t); t = setTimeout(() => save(q, field.value), 900); });
    field.addEventListener('blur', () => { clearTimeout(t); const a = S.answers[q.id]; if ((a ? a.value : '') !== field.value) save(q, field.value); });
    get = () => field.value; set = v => { if (document.activeElement !== field) field.value = v || ''; };
   }
   const sug = h('div', {class:'sug', hidden:true});
   const sugBtn = h('button', {type:'button', class:'btn sm', hidden:true, onclick: () => suggest(q, sug, set)}, 'Suggest with Claude');
   const upl = q.upload ? h('a', {class:'btn sm', href:'#uploads', onclick: () => { const s = $('#up-kind'); if (s) s.value = q.upload; }}, 'Upload ' + (KINDS.find(k => k.id === q.upload) || {}).name + ' files') : null;
   const card = h('article', {class:'q', id:'q-' + q.id},
    h('header', null, h('span', {class:'qn'}, q.id.slice(1)), h('h3', null, q.q), state),
    h('p', {class:'why'}, q.why),
    hasProp ? h('div', {class:'prop'}, h('span', null, h('b', null, 'Proposed from the project'), Array.isArray(prop) ? prop.join(' · ') : prop),
      h('button', {type:'button', class:'btn sm', onclick: () => { set(prop); save(q, prop); }}, 'Use this')) : null,
    field, h('div', {class:'row', style:'margin-top:8px'}, upl, sugBtn), sug,
    h('p', {class:'feeds'}, 'Fills project.json → ' + q.feeds));
   root.append(card); qEls[q.id] = {get, set, state, sugBtn};
  });
 });
}
function syncQuestions(){
 QS.forEach(q => { const el = qEls[q.id]; if (!el) return; const a = S.answers[q.id];
  if (a) el.set(a.value);
  if (el.state.className.indexOf('busy') < 0 || a){ const ok = answered(q); el.state.textContent = ok ? 'Saved' : 'Not answered'; el.state.className = 'qs' + (ok ? ' ok' : ''); } });
 $('#q-progress').textContent = QS.filter(answered).length + ' of ' + QS.length + ' answered';
}
function save(q, value){
 const el = qEls[q.id];
 if (!db){ el.state.textContent = 'Not saved here'; el.state.className = 'qs'; return; }
 if (S.ro) return;
 el.state.textContent = 'Saving…'; el.state.className = 'qs busy';
 write('answers/' + q.id, () => db.doc('answers/' + q.id).set({value: value, by: S.uid, at: now()}))
  .then(() => { el.state.textContent = 'Saved'; el.state.className = 'qs ok'; })
  .catch(() => { el.state.textContent = 'Not saved'; el.state.className = 'qs'; });
}
async function suggest(q, box, set){
 if (!sample) return; box.hidden = false; box.textContent = 'Thinking…';
 const prop = D.proposed[q.id]; const cur = currentValue(q.id);
 const input = 'You help a filmmaker fill in a production intake for an AI-generated short film made in Higgsfield.\n\nProject context:\n' + D.context +
  '\n\nQuestion: ' + q.q + '\nWhy it matters: ' + q.why + '\nProposed answer from the project files: ' + (Array.isArray(prop) ? prop.join(', ') : (prop || '(none)')) +
  '\nTheir current answer: ' + (Array.isArray(cur) ? cur.join(', ') : (cur || '(empty)')) + (q.options ? '\nAllowed options: ' + q.options.join(' | ') : '') +
  '\n\nWrite one improved answer in the filmmaker\'s own voice: one to four plain sentences, concrete, no preamble, no quotation marks.' + (q.options ? ' Answer with options from the allowed list only, separated by commas.' : '');
 try {
  const r = await sample(input, {modelTier:'quick', onText: u => { box.textContent = u.text; }});
  box.replaceChildren(h('span', null, r.text), ' ', h('button', {type:'button', class:'btn sm', onclick: () => { const v = q.options ? r.text.split(',').map(x => x.trim()).filter(x => q.options.indexOf(x) >= 0) : r.text.trim(); const val = q.kind === 'choice' ? (v[0] || '') : v; set(val); save(q, val); box.hidden = true; }}, 'Use this'));
 } catch(e){ box.textContent = e && e.code === 'rate_limited' ? 'Claude is busy. Try again in a minute.' : e && e.code === 'not_granted' ? 'Asking Claude is turned off for this page.' : 'No suggestion this time (' + ((e && e.code) || 'error') + ').'; }
}

/* ---------- uploads ---------- */
function typeFor(f){ const ext = (f.name.split('.').pop() || '').toLowerCase(); if (OK_TYPES.has(f.type)) return f.type; return EXT[ext] || null; }
async function doUpload(){
 const files = [...$('#up-file').files], kind = $('#up-kind').value, tag = $('#up-tag').value.trim(), note = $('#up-note').value.trim(), out = $('#up-msg');
 if (!files.length){ out.textContent = 'Choose one or more files first.'; out.className = 'msg bad'; return; }
 const lines = [];
 for (const f of files){
  const ext = (f.name.split('.').pop() || '').toLowerCase(), type = typeFor(f);
  if (['doc', 'docx', 'pages', 'rtf', 'odt'].indexOf(ext) >= 0){ lines.push(f.name + ': Word and Pages files are not accepted. Export to PDF, or save as Markdown or plain text. The paperback is already in the codex.'); continue; }
  if (['mp3', 'wav', 'm4a', 'aac', 'flac', 'ogg', 'aiff'].indexOf(ext) >= 0){ lines.push(f.name + ': audio files are not accepted. Paste the Suno link in question 10, or upload the track as an MP4 video.'); continue; }
  if (!type){ lines.push(f.name + ': this type is not accepted. Use PDF, Markdown, text, CSV, JSON, images, MP4 or WebM.'); continue; }
  if (f.size > 20 * 1048576){ lines.push(f.name + ': over the 20 MB limit (' + mb(f.size) + '). Split or compress it.'); continue; }
  out.textContent = 'Uploading ' + f.name + '…'; out.className = 'msg';
  try {
   const r = await assets.upload(f, {type});
   await write('uploads/' + r.id, () => db.doc('uploads/' + r.id).set({asset: r.id, name: f.name, kind, tag, note, contentType: r.contentType, size: r.sizeBytes, by: S.uid, at: now()}));
   lines.push(f.name + ': stored.');
  } catch(e){ const c = e && e.code; lines.push(f.name + ': ' + (c === 'too_large' ? 'too large.' : c === 'unsupported_type' ? 'type not accepted.' : c === 'quota_or_state' ? 'storage is full; delete files nothing uses.' : c === 'rate_limited' ? 'too many uploads at once; try again shortly.' : 'not stored (' + (c || 'error') + ').')); }
 }
 out.textContent = lines.join(' '); out.className = 'msg' + (lines.every(l => /stored\.$/.test(l)) ? ' ok' : ' bad');
 $('#up-file').value = ''; refreshUsage();
}
async function refreshUsage(){ if (!assets) return; try { const r = await assets.list(); S.usage = r.usage; } catch(e){ S.usage = null; } renderUsage(); }
function renderUsage(){ const u = S.usage, el = $('#up-usage'); if (!u){ el.textContent = ''; return; }
 const pct = u.maxBytes ? Math.min(100, Math.round(u.bytes / u.maxBytes * 100)) : 0;
 el.replaceChildren(h('span', {class:'muted'}, u.files + ' files · ' + mb(u.bytes) + (u.maxBytes ? ' of ' + mb(u.maxBytes) : '')), h('div', {class:'meter'}, h('i', {style:'width:' + pct + '%'}))); }
function renderUploads(){
 const root = $('#up-list'); root.replaceChildren();
 if (!S.uploads.length){ root.append(h('p', {class:'muted'}, db ? 'Nothing stored yet. Start with the source: the manuscript as a PDF, and the Episode 1 transition pages.' : 'Uploads appear here when the studio is opened in claude.ai.')); return; }
 KINDS.forEach(k => { const items = S.uploads.filter(u => u.kind === k.id); if (!items.length) return;
  root.append(h('h3', {class:'qsec'}, k.name + ' · ' + items.length), h('div', {class:'files'}, items.map(u => {
   const src = '/_blob/' + u.asset, img = /^image\//.test(u.contentType), vid = /^video\//.test(u.contentType);
   const del = h('button', {type:'button', class:'btn sm', hidden: !assets, onclick: () => askDelete(u, del)}, 'Delete');
   return h('div', {class:'file'}, h('div', {class:'pv'}, img ? h('img', {src, alt:u.name, loading:'lazy'}) : vid ? h('video', {src, controls:true, preload:'metadata', playsinline:true}) : (u.contentType || '').replace(/^.*\//, '').toUpperCase()),
    h('div', {class:'fi'}, h('b', null, u.name), u.tag ? h('span', null, 'tag: ' + u.tag) : null, u.note ? h('span', null, u.note) : null,
     h('span', null, mb(u.size || 0) + ' · ' + when(u.at)), h('div', {class:'row'}, h('a', {class:'btn sm', href:src, target:'_blank', rel:'noopener'}, 'Open'), del)));
  })));
 });
}
function askDelete(u, btn){
 const row = h('span', {class:'confirm'}, 'Delete ' + u.name + ' for everyone?', h('button', {type:'button', class:'btn sm warn', onclick: async () => {
   try { await assets.delete(u.asset); await write('uploads/' + u.key, () => db.doc('uploads/' + u.key).delete()); refreshUsage(); } catch(e){ row.textContent = 'Not deleted (' + ((e && e.code) || 'error') + ').'; } }}, 'Delete'),
  h('button', {type:'button', class:'btn sm', onclick: () => row.replaceWith(btn)}, 'Keep'));
 btn.replaceWith(row);
}
function renderIdeas(){
 const root = $('#idea-list'); root.replaceChildren(...(S.ideas.length ? S.ideas.map(i => h('div', {class:'idea'}, i.text, h('span', null, (i.tag ? i.tag + ' · ' : '') + when(i.at), ' ',
  h('button', {type:'button', class:'btn sm', hidden: !db || S.ro, onclick: () => write('ideas/' + i.key, () => db.doc('ideas/' + i.key).delete())}, 'Remove')))) : [h('p', {class:'muted'}, 'No ideas yet.')]));
}
async function addIdea(){ const t = $('#idea-text'), tag = $('#idea-tag'); if (!db || !t.value.trim()) return;
 try { await db.collection('ideas').add({text: t.value.trim(), tag: tag.value.trim(), by: S.uid, at: now()}); t.value = ''; tag.value = ''; } catch(e){ dbErr(e); } }

/* ---------- Higgsfield ---------- */
const HF_COPY = {
 needs_reauth: 'Your Higgsfield connection lapsed. Reconnect Higgsfield in claude.ai Settings → Connectors, then press Refresh.',
 server_not_connected: 'Higgsfield is not connected to your claude.ai account. Add it in claude.ai Settings → Connectors, then reload.',
 selection_required: 'You have more than one Higgsfield connector. Choose one when claude.ai asks, then reload.',
 not_in_manifest: 'Higgsfield is turned off for this page. Turn it on from the page’s Permissions menu.',
 blocked_by_policy: 'Your organization blocks this Higgsfield tool.',
 approval_required: 'Your organization requires approval for this tool, which pages cannot ask for yet.',
 server_unavailable: 'Higgsfield did not answer. It will try again shortly.',
 not_granted: 'Connectors are not available in this view.', capability_disabled: 'Connectors are not available in this view.'};
const hfMsg = e => HF_COPY[e && e.code] || ('Higgsfield reported: ' + ((e && e.message) || 'an error') + '.');
function connectHF(){
 if (!mcp) return; unwatch.forEach(u => { try { u(); } catch(e){} }); unwatch = []; S.hf.state = 'connecting'; S.hf.err = null; renderHF();
 unwatch.push(mcp.watchTool(HF, 'balance', null, ev => {
  if (ev.type === 'data'){ const p = ev.result.payload || {}; S.hf.credits = typeof p.credits === 'number' ? p.credits : null; S.hf.plan = p.subscription_plan_type || null; S.hf.state = 'live'; S.hf.err = null; }
  else { S.hf.err = ev.error; if (['needs_reauth', 'server_not_connected', 'blocked_by_policy', 'approval_required', 'not_in_manifest', 'selection_required', 'not_granted', 'capability_disabled'].indexOf(ev.error.code) >= 0){ S.hf.state = 'error'; S.hf.credits = null; } }
  renderHF(); renderStatus(); renderStart(); }, {refetchInterval: 120000}));
 unwatch.push(mcp.watchTool(HF, 'list_project_assets', listArgs(), ev => {
  if (ev.type === 'data'){ const p = ev.result.payload || {}; S.hf.items = p.items || []; S.hf.more = !!p.has_more; S.hf.cursor = p.cursor || null; S.hf.storedAt = ev.result.cache ? ev.result.cache.storedAt : Date.now(); }
  else if (['needs_reauth', 'server_not_connected', 'blocked_by_policy', 'not_in_manifest', 'not_granted'].indexOf(ev.error.code) >= 0){ S.hf.items = []; }
  renderHFItems(); }, {refetchInterval: 60000}));
}
async function loadMore(btn){ if (!S.hf.cursor) return; btn.disabled = true;
 try { const r = await mcp.callTool(HF, 'list_project_assets', Object.assign(listArgs(), {cursor: S.hf.cursor})); const p = r.payload || {};
  S.hf.items = S.hf.items.concat(p.items || []); S.hf.more = !!p.has_more; S.hf.cursor = p.cursor || null; renderHFItems(); }
 catch(e){ $('#hf-items-msg').textContent = hfMsg(e); } btn.disabled = false; }
function renderHF(){
 const st = $('#hf-state'), s = S.hf;
 const body = [];
 if (!mcp) body.push(h('p', null, window.claude ? 'Connectors are not available in this view. Open the studio from claude.ai while signed in.' : 'Open this page from claude.ai to connect Higgsfield. Locally it shows the plan only.'));
 else if (s.state === 'live') body.push(h('p', null, h('b', null, s.credits != null ? Math.round(s.credits * 10) / 10 + ' credits' : 'Connected'), s.plan ? ' on the ' + s.plan + ' plan.' : '.'));
 else if (s.state === 'connecting') body.push(h('p', null, 'Connecting… claude.ai may ask you to allow Higgsfield for this page.'));
 else body.push(h('p', null, 'Connect to see your credits and this project’s generations live. Nothing is spent by connecting.'));
 if (s.err) body.push(h('p', {class:'msg bad'}, hfMsg(s.err)));
 const btns = h('div', {class:'row'});
 if (mcp && s.state !== 'live') btns.append(h('button', {type:'button', class:'btn pri', onclick: connectHF}, s.state === 'error' ? 'Try again' : 'Connect Higgsfield'));
 if (mcp && s.state === 'live') btns.append(h('button', {type:'button', class:'btn', onclick: () => { mcp.invalidate(HF).catch(() => {}).then(connectHF); }}, 'Refresh'));
 if (perms && s.err && s.err.code === 'not_in_manifest') btns.append(h('button', {type:'button', class:'btn', onclick: () => perms.manage().catch(() => {})}, 'Open permissions'));
 btns.append(h('a', {class:'btn', href: D.project.hf.project_url, target:'_blank', rel:'noopener'}, lockOk() ? 'Open ' + LOCK.project + ' in Higgsfield ↗' : 'Open the project in Higgsfield ↗'));
 body.push(h('p', {class: lockOk() ? 'msg ok' : 'msg bad'}, lockOk() ? 'Locked: every generation and remix from this studio is filed into ' + LOCK.project + ' and nowhere else.' : 'Not locked to a folder: generation is off until the project names its Higgsfield folder.'));
 st.replaceChildren(...body, btns);
}
const TARGETS = () => [['', 'Not assigned']].concat(D.sheets.map(s => ['sheet:' + s.name, 'Sheet · @' + s.name]),
 [].concat(...D.shots.map(s => s.lanes.map(l => ['shot:' + s.id + ':' + l.c, s.id + ' lane ' + l.c + ' · ' + s.title])))); 
function laneOf(target){ const m = target.split(':'); const s = D.shots.find(x => x.id === m[1]); if (!s) return null; const l = s.lanes.find(x => x.c === m[2]) || s.lanes[0]; return {prompt: l.prompt, d: s.d}; }
function motionOf(prompt){ const i = prompt.indexOf(' REFERENCES — attach before generating:'); return (i >= 0 ? prompt.slice(0, i) : prompt).replace(/@\[([a-z0-9_-]+)\]\([0-9a-f-]{36}\)/gi, (m, n) => n.replace(/-/g, ' ')).replace(/@([a-z][a-z0-9_-]{2,40})/gi, (m, n) => n.replace(/-/g, ' ')).trim(); }
function renderHFItems(){
 const root = $('#hf-items'); if (!root) return; const items = S.hf.items;
 if (S.hf.state !== 'live' && !items.length){ root.replaceChildren(h('p', {class:'muted'}, 'Connect Higgsfield to list this project’s generations and uploads.')); return; }
 if (!items.length){ root.replaceChildren(h('p', {class:'muted'}, 'The project is empty. Generations made here or in the Higgsfield web app inside this project appear in this list.')); return; }
 const opts = TARGETS();
 const rows = items.map(it => { const link = S.links[it.item_id];
  const sel = h('select', {'aria-label':'Assign ' + it.item_id, disabled: !db || S.ro, onchange: () => { const v = sel.value; write('links/' + it.item_id, () => v ? db.doc('links/' + it.item_id).set({target: v, kind: it.output_kind, model: it.model_id, by: S.uid, at: now()}) : db.doc('links/' + it.item_id).delete()); }},
   opts.map(o => h('option', {value:o[0]}, o[1])));
  sel.value = link ? link.target : '';
  let remix = null;
  if (it.output_kind === 'image' && it.status === 'completed' && it.type === 'job'){
   remix = h('button', {type:'button', class:'btn sm', onclick: () => {
    const lane = link && link.target.indexOf('shot:') === 0 ? laneOf(link.target) : null;
    const ta = h('textarea', {'aria-label':'What moves', placeholder:'What moves in this still, and how the camera moves'}); ta.value = lane ? motionOf(lane.prompt) : '';
    const tr = h('tr', null, h('td', {colspan:'8'}, h('div', {class:'card', style:'box-shadow:none'}, h('label', {class:'lb'}, 'Animate this still · start frame ' + String(it.item_id).slice(0, 8)), ta,
     genControls({target: link ? link.target : 'remix:' + it.item_id, label: 'Animate ' + String(it.item_id).slice(0, 8), prompt: '', promptEl: ta, kind: 'video', fixedKind: 'video', duration: lane ? lane.d : 8, medias: [{role: 'start_image', value: it.item_id}]}))));
    remix.closest('tr').after(tr); remix.disabled = true; }}, 'Animate');
  }
  return h('tr', null, h('td', {class:'num'}, when(it.created_at)), h('td', null, it.output_kind || it.type), h('td', null, it.model_id || (it.type || '').replace('_', ' ')),
   h('td', null, it.status), h('td', null, it.is_favourite ? '♥' : ''), h('td', {class:'num'}, h('code', null, String(it.item_id).slice(0, 8))), h('td', null, sel), h('td', null, remix)); });
 const more = S.hf.more ? h('button', {type:'button', class:'btn sm', onclick: e => loadMore(e.currentTarget)}, 'Load more') : null;
 const fresh = S.hf.storedAt ? h('p', {class:'feeds'}, 'Listed ' + new Date(S.hf.storedAt).toLocaleTimeString() + '. Refreshes every minute.') : null;
 root.replaceChildren(h('div', {class:'tw'}, h('table', null, h('thead', null, h('tr', null, ['Made', 'Kind', 'Model', 'Status', '♥', 'Id', 'Assign to', ''].map(t => h('th', null, t)))), h('tbody', null, rows))), more, fresh);
}

/* ---------- generate ---------- */
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
function pendingIn(prompt){ const out = new Set(); (prompt.match(/@([a-z][a-z0-9_-]{2,40})/gi) || []).forEach(m => { const n = m.slice(1); if (PENDING.has(n)) out.add(n); }); return [...out]; }
function toApi(prompt, asWords){
 const i = prompt.indexOf(' REFERENCES — attach before generating:'); let body = i >= 0 ? prompt.slice(0, i) : prompt; const refs = i >= 0 ? prompt.slice(i) : '';
 const seen = new Set(); body = body.replace(/@\[([a-z0-9_-]+)\]\(([0-9a-f-]{36})\)/gi, (m, n, id) => { if (seen.has(id)) return n.replace(/-/g, ' '); seen.add(id); return '<<<' + id + '>>>'; });
 const extra = []; (refs.match(/\(([0-9a-f-]{36})\)/gi) || []).forEach(m => { const id = m.slice(1, -1); if (!seen.has(id)){ seen.add(id); extra.push('<<<' + id + '>>>'); } });
 if (asWords) body = body.replace(/@([a-z][a-z0-9_-]{2,40})/gi, (m, n) => PENDING.has(n) ? n.replace(/-/g, ' ') : m);
 return body.trim() + (extra.length ? ' References: ' + extra.join(' ') + '.' : '');
}
function extractIds(payload){ const ids = new Set(), skip = new Set([PID, WS, FOLDER].concat(Object.values(D.cast).map(c => c.id).filter(Boolean)));
 (function walk(v, k){ if (v == null) return; if (typeof v === 'string'){ if (UUID.test(v) && !skip.has(v) && /(^|_)(job|jobs|id|ids|request_id|generation_id)$/i.test(k || '')) ids.add(v); return; }
  if (Array.isArray(v)) return v.forEach(x => walk(x, k)); if (typeof v === 'object') Object.keys(v).forEach(kk => walk(v[kk], kk)); })(payload, '');
 return [...ids]; }
function genControls(spec){
 // spec: {target, label, prompt, kind: 'video'|'still', aspect, duration, fixedKind}
 const wrap = h('div', {class:'gen'}), res = h('div', {class:'res'});
 const promptOf = () => spec.promptEl ? spec.promptEl.value : spec.prompt;
 const pend = spec.promptEl ? [] : pendingIn(spec.prompt); let asWords = false;
 const kindSel = spec.fixedKind ? null : h('select', {'aria-label':'What to make'}, h('option', {value:'video'}, 'Video · ' + VIDEO_MODEL), h('option', {value:'still'}, 'Still · ' + IMAGE_MODEL));
 if (kindSel) kindSel.value = spec.kind || 'video';
 const dur = h('input', {type:'number', min:'4', max:'16', step:'1', value: String(Math.min(16, spec.duration || 8)), 'aria-label':'Seconds'});
 const res720 = h('select', {'aria-label':'Resolution'}, h('option', {value:'720p'}, '720p'), h('option', {value:'1080p'}, '1080p'));
 const aud = h('label', {class:'ow'}, h('input', {type:'checkbox'}), ' model audio');
 const kind = () => spec.fixedKind || kindSel.value;
 const sync = () => { const v = kind() !== 'video'; dur.hidden = v; res720.hidden = v; aud.hidden = v; };
 if (kindSel) kindSel.addEventListener('change', sync); sync();
 const pv = h('button', {type:'button', class:'btn sm', onclick: () => run(true)}, 'Preview cost');
 const ow = pend.length ? h('label', {class:'ow'}, h('input', {type:'checkbox', onchange: e => { asWords = e.target.checked; }}), ' send pending names as plain words') : null;
 function params(preview){ const p = {model: kind() === 'video' ? VIDEO_MODEL : IMAGE_MODEL, prompt: toApi(promptOf(), asWords), aspect_ratio: kind() === 'video' ? '21:9' : (spec.aspect || '21:9'), folder_id: FOLDER};
  if (kind() === 'video'){ p.duration = Math.max(4, Math.min(16, parseInt(dur.value, 10) || 8)); p.resolution = res720.value; p.generate_audio = !!aud.querySelector('input').checked; }
  else if (IMAGE_MODEL === 'cinematic_studio_2_5') p.resolution = '2k';
  if (spec.medias){ p.medias = spec.medias; if (kind() === 'video') p.mode = 'omni_reference'; }
  if (spec.declinedPreset) p.declined_preset_id = spec.declinedPreset;
  if (preview) p.get_cost = true; return p; }
 async function run(preview, unlim){
  if (!mcp){ res.textContent = 'Open the studio in claude.ai to generate.'; res.className = 'res bad'; return; }
  if (!lockOk()){ res.textContent = 'Refused: this studio is not linked to its locked Higgsfield folder. Nothing was sent.'; res.className = 'res bad'; return; }
  if (spec.promptEl && !spec.promptEl.value.trim()){ res.textContent = 'Write what should move first.'; res.className = 'res bad'; return; }
  if (pend.length && !asWords){ res.textContent = 'Needs sheets first: ' + pend.map(n => '@' + n).join(', ') + '. Sync with Claude after the sheets are assigned, or tick “send pending names as plain words”.'; res.className = 'res bad'; return; }
  const tool = kind() === 'video' ? 'generate_video' : 'generate_image', p = params(preview); if (unlim != null) p.use_unlim = unlim;
  res.textContent = preview ? 'Asking Higgsfield for the cost…' : 'Submitting…'; res.className = 'res';
  try {
   const r = await mcp.callTool(HF, tool, {params: p}, preview ? {cache: false} : undefined); const pay = r.payload;
   if (preview){ const c = pay && pay.cost ? pay.cost.credits : null; if (c == null){ res.textContent = 'Higgsfield answered without a cost: ' + JSON.stringify(pay).slice(0, 200); return; }
    res.replaceChildren(h('span', {class:'confirm'}, 'This ' + (kind() === 'video' ? p.duration + 's ' + p.resolution + ' video' + (spec.medias ? ' from the still' : '') : 'still') + ' costs ' + c + ' credits, filed to ' + (LOCK ? LOCK.project : 'the project') + '.',
     h('button', {type:'button', class:'btn sm go', onclick: () => run(false)}, 'Generate · ' + c), h('button', {type:'button', class:'btn sm', onclick: () => { res.textContent = ''; }}, 'Cancel'))); spec.lastCost = c; return; }
   if (pay && pay.unlim_choice){ res.replaceChildren(h('span', {class:'confirm'}, typeof pay.unlim_choice === 'string' ? pay.unlim_choice : 'Higgsfield asks which balance pays: your unlimited generations or your credits.',
     h('button', {type:'button', class:'btn sm go', onclick: () => run(false, true)}, 'Use unlimited'), h('button', {type:'button', class:'btn sm', onclick: () => run(false, false)}, 'Use credits'))); return; }
   const ids = extractIds(pay);
   const ptxt = JSON.stringify(pay || '');
   if (!ids.length && /preset/i.test(ptxt)){ const m = ptxt.match(/declined_preset_id[^0-9a-f]{0,6}([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/i) || ptxt.match(/preset[^0-9a-f]{0,40}([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/i);
    res.replaceChildren(h('span', {class:'confirm'}, 'Higgsfield suggested one of its presets instead of making this take. Nothing was charged.',
     m ? h('button', {type:'button', class:'btn sm go', onclick: () => { spec.declinedPreset = m[1]; run(false); }}, 'Make it without the preset') : null,
     h('button', {type:'button', class:'btn sm', onclick: () => { res.textContent = ''; }}, 'Cancel'))); return; }
   await logJob(spec, tool, p, ids, 'submitted', pay);
   res.textContent = 'Submitted' + (ids.length ? ': ' + ids.map(x => x.slice(0, 8)).join(', ') : '') + '. It appears in the Higgsfield tab when the project lists it.'; res.className = 'res ok';
   mcp.invalidate(HF, 'list_project_assets').catch(() => {}); mcp.invalidate(HF, 'balance').catch(() => {});
  } catch(e){ const c = e && e.code;
   if (!preview && (c === 'server_unavailable' || c === 'upstream_error' || c === 'cancelled')){ await logJob(spec, tool, p, [], 'unknown', {error: c, message: e.message}); res.textContent = 'The outcome is unknown: Higgsfield may have started it. Check the Higgsfield tab before trying again.'; res.className = 'res bad'; return; }
   res.textContent = c === 'tool_error' ? 'Higgsfield refused: ' + (e.message || 'no reason given') : hfMsg(e); res.className = 'res bad'; }
 }
 wrap.append(...[kindSel, dur, res720, aud, pv, ow].filter(Boolean));
 return h('div', null, wrap, res);
}
async function logJob(spec, tool, params, ids, status, payload){
 if (!db) return; const at = now();
 try {
  await db.collection('jobs').add({target: spec.target, label: spec.label, tool, model: params.model, seconds: params.duration || null, aspect: params.aspect_ratio, credits: spec.lastCost || null, ids, status, at, by: S.uid, payload: JSON.stringify(payload || null).slice(0, 6000)});
  for (const id of ids) await write('links/' + id, () => db.doc('links/' + id).set({target: spec.target, kind: tool === 'generate_video' ? 'video' : 'image', model: params.model, auto: true, by: S.uid, at}));
 } catch(e){ dbErr(e); }
}
function renderSheets(){
 const root = $('#gen-sheets'); root.replaceChildren(h('p', {class:'sec-p'}, 'Every face, place, prop and effect the board still needs, with its brief written into a sheet prompt. Generate a still, look at it in the Higgsfield tab, and assign the one you like to its sheet. On sync, Claude turns each assigned image into an element and fills its id everywhere it is used.'));
 const groups = {characters:'Characters', environments:'Places and plates', props:'Props', fx:'Effects'};
 Object.keys(groups).forEach(k => { const list = D.sheets.filter(s => s.kind === k); if (!list.length) return; root.append(h('h3', {class:'qsec'}, groups[k] + ' · ' + list.length));
  list.forEach(s => { const cnt = h('span', {class:'pill', 'data-sheet':s.name}, '');
   const cb = h('button', {type:'button', class:'btn sm', onclick: e => copy(s.prompt, e.currentTarget)}, 'Copy prompt');
   root.append(h('div', {class:'sheet'}, h('div', null, h('span', {class:'k'}, '@' + s.name + ' · ' + s.aspect), h('h3', null, s.name.replace(/-/g, ' ')), h('p', null, s.brief),
     h('details', null, h('summary', null, 'Sheet prompt'), h('pre', {class:'pr'}, s.prompt), cb)),
    h('div', null, h('div', {class:'row', style:'margin-bottom:8px'}, cnt), genControls({target: 'sheet:' + s.name, label: 'Sheet @' + s.name, prompt: s.prompt, kind: 'still', fixedKind: 'still', aspect: s.aspect})))); });
 });
 renderSheetsCounts();
}
function renderSheetsCounts(){ document.querySelectorAll('[data-sheet]').forEach(el => { const n = linkedTo('sheet:' + el.getAttribute('data-sheet')).length; el.textContent = n ? n + ' image' + (n > 1 ? 's' : '') + ' assigned' : 'no image yet'; el.className = 'pill' + (n ? ' ok' : ''); }); }
const STATUS = ['unshot', 'anchors', 'generating', 'takes in', 'picked', 'in the cut'];
const shotEls = {};
function renderShots(){
 const root = $('#gen-shots'); root.replaceChildren(h('p', {class:'sec-p'}, 'All 26 shots with their three lanes. A lane that still names a pending sheet waits until sync; S1 can be generated now, because everything it attaches already exists. A still is the anchor frame; a video is the take. Every Generate previews its cost first.'));
 let act = null;
 D.shots.forEach(s => {
  if (s.act !== act){ act = s.act; root.append(h('h3', {class:'qsec'}, 'Movement ' + act + ' · ' + (D.project.acts[act] || ''))); }
  const st = h('select', {'aria-label':'Status of ' + s.id, disabled: !db || S.ro, onchange: () => saveShot(s.id)}, STATUS.map(x => h('option', {value:x}, x)));
  const note = h('input', {type:'text', placeholder:'Note for this shot', 'aria-label':'Note for ' + s.id, disabled: !db || S.ro});
  let t = null; note.addEventListener('input', () => { clearTimeout(t); t = setTimeout(() => saveShot(s.id), 900); });
  shotEls[s.id] = {st, note};
  const lanes = s.lanes.map(l => { const pend = pendingIn(l.prompt); const cb = h('button', {type:'button', class:'btn sm', onclick: e => copy(l.prompt, e.currentTarget)}, 'Copy for the web app');
   return h('div', {class:'lane', 'data-c':l.c}, h('div', {class:'lh'}, h('span', {class:'lc'}, l.c), h('h4', null, l.name)), l.why ? h('p', {class:'lw'}, l.why) : null,
    h('details', null, h('summary', null, 'Prompt'), h('pre', {class:'pr'}, l.prompt), cb),
    pend.length ? h('div', {class:'pend'}, 'Waits for ', pend.map((n, i) => [i ? ', ' : '', h('code', null, '@' + n)])) : null,
    genControls({target: 'shot:' + s.id + ':' + l.c, label: s.id + ' lane ' + l.c, prompt: l.prompt, kind: 'video', duration: s.d})); });
  root.append(h('article', {class:'shot', id:'shot-' + s.id}, h('header', null, h('span', {class:'sid'}, s.id), h('h3', null, s.title), h('span', {class:'meta'}, s.d + 's · audio ' + (s.audio ? 'on' : 'off') + ' on lane A')),
   h('div', {class:'ctl'}, h('label', {class:'lb', style:'margin:0'}, 'Status'), st, note), h('div', {class:'lanes'}, lanes)));
 });
 syncShots();
}
function syncShots(){ Object.keys(shotEls).forEach(id => { const d = S.shots[id] || {}, el = shotEls[id]; if (document.activeElement !== el.st) el.st.value = d.status || 'unshot'; if (document.activeElement !== el.note) el.note.value = d.note || ''; }); }
function saveShot(id){ if (!db || S.ro) return; const el = shotEls[id]; write('shots/' + id, () => db.doc('shots/' + id).set({status: el.st.value, note: el.note.value, by: S.uid, at: now()})); }
function renderLedger(){
 const root = $('#gen-ledger'); if (!root) return;
 if (!S.jobs.length){ root.replaceChildren(h('p', {class:'muted'}, db ? 'Nothing generated from the studio yet. Every submission is written here with its cost and ids.' : 'The ledger appears when the studio is opened in claude.ai.')); return; }
 const head = h('thead', null, h('tr', null, ['When', 'What', 'Model', 'Credits', 'Ids', 'Status'].map(x => h('th', null, x))));
 const rows = S.jobs.map(j => h('tr', null,
  h('td', {class:'num'}, when(j.at)),
  h('td', null, j.label || j.target),
  h('td', null, (j.model || '') + (j.seconds ? ' · ' + j.seconds + 's' : '')),
  h('td', {class:'num'}, j.credits != null ? j.credits : '—'),
  h('td', {class:'num'}, (j.ids || []).map(x => x.slice(0, 8)).join(', ') || '—'),
  h('td', null, h('span', {class: 'pill' + (j.status === 'submitted' ? ' ok' : ' partial')}, j.status))));
 root.replaceChildren(h('div', {class:'tw'}, h('table', null, head, h('tbody', null, rows))));
}
function setView(v){ S.view = v; ['sheets', 'shots', 'ledger'].forEach(x => { $('#gen-' + x).hidden = x !== v; $('#seg-' + x).setAttribute('aria-pressed', x === v ? 'true' : 'false'); }); try { localStorage.setItem('af-studio-gen', v); } catch(e){} }

/* ---------- parity ---------- */
function renderParity(){
 const P = D.parity, cols = P.columns, LBL = {built:'built', partial:'partial', planned:'planned', none:'—'};
 const count = (c, k) => P.groups.reduce((n, g) => n + g.rows.filter(r => r[c.id] === k).length, 0);
 $('#par-cols').replaceChildren(...cols.map(c => h('div', {class:'card'},
  h('h3', {style:'font:600 15px var(--body)'}, c.name),
  h('p', {class:'muted', style:'margin:4px 0 0;font-size:13.5px'}, c.note),
  h('p', {class:'feeds'}, ['built', 'partial', 'planned'].map(k => count(c, k) + ' ' + k).join(' · ')))));
 const head = h('thead', null, h('tr', null, h('th', null, 'Feature'), cols.map(c => h('th', null, c.name)), h('th', null, 'Notes')));
 const body = [];
 P.groups.forEach(g => {
  body.push(h('tr', null, h('td', {colspan: String(cols.length + 2), class:'qsec', style:'padding-top:18px'}, g.name)));
  g.rows.forEach(r => body.push(h('tr', null, h('td', null, r.f), cols.map(c => h('td', null, h('span', {class: 'pill ' + r[c.id]}, LBL[r[c.id]] || r[c.id]))), h('td', null, r.n))));
 });
 $('#par-table').replaceChildren(h('div', {class:'tw'}, h('table', {class:'par'}, head, h('tbody', null, body))));
 $('#par-plan').replaceChildren(...P.plan.map(x => h('div', {class:'card'}, h('h3', null, x.phase), h('ul', null, x.items.map(i => h('li', null, i))))));
}

/* ---------- ask ---------- */
async function ask(){
 const q = $('#ask-q').value.trim(), out = $('#ask-a'); if (!q || !sample) return; out.textContent = 'Thinking…';
 const ans = QS.map(x => { const a = S.answers[x.id]; return a ? x.q + ' → ' + (Array.isArray(a.value) ? a.value.join(', ') : a.value) : null; }).filter(Boolean).join('\n');
 const input = 'You are the production assistant inside the Anchorframe studio for an AI-generated film made in Higgsfield. Answer plainly and briefly, with concrete next steps.\n\nProject:\n' + D.context + '\n\nAnswers saved so far:\n' + (ans || '(none)') +
  '\n\nFiles stored: ' + (S.uploads.map(u => u.name + ' [' + u.kind + ']').join(', ') || '(none)') + '\n\nQuestion: ' + q;
 try { const r = await sample(input, {onText: u => { out.textContent = u.text; }, cache: false}); out.textContent = r.text; }
 catch(e){ out.textContent = e && e.code === 'rate_limited' ? 'Claude is busy. Try again in a minute.' : 'No answer this time (' + ((e && e.code) || 'error') + ').'; }
}

/* ---------- boot ---------- */
function boot(){
 buildQuestions(); renderSheets(); renderShots(); renderLedger(); renderParity(); renderUploads(); renderIdeas(); renderHF(); renderHFItems(); renderStatus(); renderStart(); syncQuestions();
 $('#up-kind').replaceChildren(...KINDS.map(k => h('option', {value:k.id}, k.name + ' · ' + k.what)));
 $('#up-go').addEventListener('click', doUpload); $('#idea-go').addEventListener('click', addIdea); $('#ask-go').addEventListener('click', ask);
 $('#sync-copy').addEventListener('click', e => copy('Sync SoM V2', e.currentTarget));
 ['sheets', 'shots', 'ledger'].forEach(v => $('#seg-' + v).addEventListener('click', () => setView(v)));
 let tab = location.hash.slice(1); if (TABS.indexOf(tab) < 0){ try { tab = localStorage.getItem('af-studio-tab') || 'start'; } catch(e){ tab = 'start'; } } show(tab);
 let gv = 'sheets'; try { gv = localStorage.getItem('af-studio-gen') || 'sheets'; } catch(e){} setView(gv);
 const C = window.claude;
 if (!C || typeof C.use !== 'function'){ banner('Opened outside claude.ai: the plan, the questions and every prompt are here, but nothing saves, uploads or connects. Open the published studio to work.'); return; }
 C.use('user').then(async u => { if (!u) return; try { S.uid = await u.id(); S.canWrite = await u.can('data.write'); } catch(e){} if (S.canWrite === false){ S.ro = true; banner('You can read this studio, but your sharing level does not let you change it.'); } });
 C.use('db').then(d => { if (!d){ banner('Saving is not available in this view. Sign in to claude.ai and open the studio there.'); return; } db = d; subscribe(); renderShots(); renderUploads(); renderLedger(); });
 C.use('assets').then(a => { assets = a; $('#up-form').hidden = !a; $('#up-ro').hidden = !!a; if (a) refreshUsage(); renderUploads(); });
 C.use('permissions').then(p => { perms = p; });
 C.use('mcp').then(async m => { mcp = m; if (m){ let st = 'prompt'; try { const p = await C.use('permissions'); if (p) st = await p.state('mcp:' + HF); } catch(e){ st = 'prompt'; } S.hf.perm = st; if (st === 'granted') connectHF(); } renderHF(); renderHFItems(); });
 C.use('sample').then(s => { sample = s; Object.values(qEls).forEach(el => { el.sugBtn.hidden = !s; }); $('#ask').hidden = !s; });
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
"""

def body(desk_href):
    L = dict(data["links"], desk=desk_href); ed = DK.get("edition", ""); P0 = data["project"]
    where = [("The manuscript", "Uploads → Source, as a PDF or Markdown", "Word files are not accepted here. The paperback .docx is already in the codex (codex/_source)."),
             ("Screenplays and transition pages", "Uploads → Source, tag “transition” for bridge pages", "The Episode 1 last pages go here; Claude rewrites the bridge from them on sync."),
             ("Ideas and notes", "Uploads → the Ideas box, or a Markdown file under Ideas", "Short notes in the box; anything longer as a file."),
             ("Look references", "Uploads → Look", "One plate per movement; images or short clips."),
             ("Character and place art", "Uploads → Cast, tagged with the element name", "For example tag “ammon”. Claude uses them when building sheets."),
             ("Tracks", "Question 10, as Suno links with tempo", "Audio files are not accepted; a track can go up as MP4 video."),
             ("Generated stills and takes", "Higgsfield, inside this project (automatic)", "Assign each one to a sheet or a shot lane in the Higgsfield tab."),
             ("Decisions", "Questions", "Saved for everyone you share the studio with; Claude writes them into project.json.")]
    rows = "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td class=\"muted\">{esc(c)}</td></tr>" for a, b, c in where)
    edl = "".join(f'<a href="{esc(e["url"])}" target="_blank" rel="noopener">{esc(e["edition"])} ↗</a>' for e in DK.get("editions", []) if e.get("edition") != ed and e.get("url"))
    return f'''<header class="top"><div class="wrap">
<p class="eyebrow"><span>Anchorframe · {esc(DK.get("series",""))} · {esc(ed)} · Episode {esc(DK.get("episode",""))}</span>{edl}</p>
<h1>{esc(P0["title"])} <small>studio</small></h1>
<p class="lede">The working app for this episode: answer the setup questions, store the source and references, connect Higgsfield, make the sheets and the shots, and hand the rest to Claude with one message.</p>
<div class="status" id="status"></div></div></header>
<nav class="tabs" aria-label="Studio"><div class="wrap">
<a id="nav-start" href="#start">Start</a><a id="nav-questions" href="#questions">Questions</a><a id="nav-uploads" href="#uploads">Uploads</a><a id="nav-higgsfield" href="#higgsfield">Higgsfield</a><a id="nav-generate" href="#generate">Generate</a><a id="nav-parity" href="#parity">Parity</a>
<span class="sep"></span><a class="out" href="{esc(L["desk"])}">Desk</a><a class="out" href="{esc(L["board"])}">Board</a><a class="out" href="{esc(L["workflow"])}">Workflow</a><a class="out" href="{esc(L["links"])}">Links</a></div></nav>
<main class="wrap">
<div class="banner" id="banner" hidden></div>

<section id="tab-start">
<div class="sec-h"><h2>Start Episode 2 here</h2></div>
<p class="sec-p">Five steps get the episode from a screenplay to shots you can generate. Everything you do here is saved for everyone you share the studio with, and Claude reads it when you ask for a sync.</p>
<div class="steps" id="start-steps"></div>
<div class="grid2" style="margin-top:24px">
<div class="card"><h3 style="font:600 16px var(--body)">Hand back to Claude</h3><p class="muted" style="margin:6px 0 0;font-size:14px">When the questions are answered and the sheets assigned, send Claude this message in the session that built the studio. Claude reads the answers, uploads, ideas, shot notes, ledger and assignments; writes them into <code>project.json</code> and the codex; creates the elements from the assigned sheet images; fills every pending id; rebuilds the board; and republishes this studio.</p>
<div class="copybox"><code>Sync SoM V2</code><button type="button" class="btn sm" id="sync-copy">Copy</button></div></div>
<div class="card ask" id="ask" hidden><h3 style="font:600 16px var(--body)">Ask Claude about this project</h3><p class="muted" style="margin:6px 0 10px;font-size:14px">Claude sees the board, the cast briefs and what you have saved here. Each question costs a little of your usage.</p>
<label class="lb" for="ask-q">Your question</label><textarea id="ask-q" placeholder="Which sheets should I make first if I only have 60 credits?"></textarea><div class="row" style="margin-top:8px"><button type="button" class="btn pri" id="ask-go">Ask</button></div><div class="ans" id="ask-a"></div></div>
</div>
<h3 class="qsec" style="margin-top:30px">Where things go</h3>
<div class="tw card" style="padding:4px 8px"><table><thead><tr><th>What</th><th>Put it</th><th>Note</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>

<section id="tab-questions" hidden>
<div class="sec-h"><h2>The setup questions</h2><span class="muted" id="q-progress"></span></div>
<p class="sec-p">These sixteen questions are the Anchorframe intake: the same form starts every project in the template. Here each one carries a proposal written from what the project already knows. Accept it, change it, or ask Claude for a better one. Answers save as you type.</p>
<div id="q-list"></div>
</section>

<section id="tab-uploads" hidden>
<div class="sec-h"><h2>Uploads</h2></div>
<p class="sec-p">Files stored with the studio, shared with everyone you invite. Up to 20 MB each: PDF, Markdown, plain text, CSV, JSON, images, MP4 and WebM.</p>
<div class="grid2">
<div class="card"><div id="up-form" hidden>
<label class="lb" for="up-file">Files</label><input type="file" id="up-file" multiple>
<div class="grid2" style="margin-top:10px;gap:10px"><div><label class="lb" for="up-kind">Category</label><select id="up-kind"></select></div><div><label class="lb" for="up-tag">Tag</label><input type="text" id="up-tag" placeholder="element or shot, e.g. ammon or S11"></div></div>
<label class="lb" for="up-note" style="margin-top:10px">Note</label><input type="text" id="up-note" placeholder="What this is for">
<div class="row" style="margin-top:12px"><button type="button" class="btn pri" id="up-go">Upload</button></div><div class="msg" id="up-msg"></div><div id="up-usage" style="margin-top:12px"></div></div>
<p id="up-ro" class="muted">Uploading needs the studio opened in claude.ai by someone who can edit it.</p></div>
<div class="card"><h3 style="font:600 16px var(--body)">Ideas</h3><p class="muted" style="margin:4px 0 10px;font-size:14px">Anything you want Claude to fold in: a scene idea, a line, a look, a change.</p>
<label class="lb" for="idea-text">Idea</label><textarea id="idea-text" placeholder="Stardust should hum the first four notes of the main title as she fades"></textarea>
<div class="row" style="margin-top:8px"><input type="text" id="idea-tag" placeholder="tag: a shot, a character or a song" style="flex:1;min-width:160px"><button type="button" class="btn pri" id="idea-go">Add idea</button></div>
<div id="idea-list" style="margin-top:12px"></div></div>
</div>
<div id="up-list" style="margin-top:22px"></div>
</section>

<section id="tab-higgsfield" hidden>
<div class="sec-h"><h2>Higgsfield</h2></div>
<p class="sec-p">The studio calls Higgsfield with your own connector: no keys, and it only ever sees this project, <code>{esc(P0["hf"]["project_id"])}</code>. Generations made here are filed into the project, the same folder the web app uses, so the two stay one place.</p>
<div class="grid2"><div class="card" id="hf-state"></div>
<div class="card"><h3 style="font:600 16px var(--body)">How making things works</h3><ul style="margin:8px 0 0;padding-left:18px;font-size:14px;color:var(--ink-2)">
<li>Every Generate button asks Higgsfield for the cost first; nothing is spent until you press the button that shows the price.</li>
<li>Stills use <code>{esc(P0["hf"]["image_model"])}</code>; video uses <code>{esc(P0["hf"]["video_model"])}</code> at 21:9, 720p by default, with the model's own audio off unless you tick it.</li>
<li><b>Animate</b> on any finished still makes a video that starts on that frame: a remix, filed into the same folder.</li>
<li>Chained start and end frames, Souls and audio references still go through the web app: copy the lane's prompt there.</li>
<li>Whatever you make, assign it below to the sheet or shot lane it belongs to. That is what Claude reads on sync.</li></ul></div></div>
<h3 class="qsec" style="margin-top:26px">In this project</h3><div id="hf-items"></div><p class="msg bad" id="hf-items-msg"></p>
</section>

<section id="tab-generate" hidden>
<div class="sec-h"><h2>Generate</h2></div>
<div class="seg" role="group" aria-label="Generate view"><button type="button" id="seg-sheets" aria-pressed="true">Cast sheets · {len(sheets)}</button><button type="button" id="seg-shots" aria-pressed="false">Shots · {len(shots)}</button><button type="button" id="seg-ledger" aria-pressed="false">Ledger</button></div>
<div id="gen-sheets"></div><div id="gen-shots" hidden></div><div id="gen-ledger" hidden></div>
</section>

<section id="tab-parity" hidden>
<div class="sec-h"><h2>Feature parity</h2></div>
<p class="sec-p">What the Director's Bible, the V1 desk, this studio and the template service each do, and what is built next. The studio is the first version where the work happens in the app; the service is the same studio for any film.</p>
<div class="grid2" id="par-cols" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))"></div>
<div id="par-table" style="margin-top:18px"></div>
<h3 class="qsec" style="margin-top:28px">The build plan</h3><div class="plan" id="par-plan"></div>
</section>
<footer>Built by anchorframe/studio.py from desk.json, intake.json, parity.json and projects/{esc(slug)}/ · {esc(data["built"])} · regenerate, don’t hand-edit</footer>
</main>'''

title = DK.get("title", "Anchorframe")
head = f'<title>{esc(title)}</title><meta name="description" content="{esc(DK.get("description",""))}"><style>{CSS}</style>'
tail = f'<script type="application/json" id="studio-data">{DATA}</script><script>{JS}</script>'
full = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">{head}</head><body>{body("index.html")}{tail}</body></html>'
(D / "studio.html").write_text(full, encoding="utf-8")
# the published copy is the artifact's main page, so the desk front door rides beside it as desk.html
if opt("--fragment"): pathlib.Path(opt("--fragment")).write_text(head + body(opt("--desk-href", "desk.html")) + tail, encoding="utf-8")
print(f"wrote studio.html · {len(full)//1024} KB · {len(I['questions'])} questions · {len(sheets)} sheets · {len(shots)} shots · {sum(len(g['rows']) for g in PAR['groups'])} parity rows")
