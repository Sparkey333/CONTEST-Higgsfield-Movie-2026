#!/usr/bin/env python3
"""Build the contest radar: every contest worth aiming the next film, song or book at.

    python3 anchorframe/contests.py            ->  anchorframe/contests.html

Reads contests.json (the researched list: Higgsfield first, then the five closest platforms, then
the wider and traditional ones) and borrows the desk's colour and type tokens from desk.py so the
two pages read as one system. Opened from claude.ai the page keeps each contest's tracking status
and note, and any contest you add, in the artifact's shared store; opened as a file it is the list,
read-only. Regenerate, don't hand-edit: add or correct a contest in contests.json and rebuild.
"""
import json, re, html, pathlib, datetime
D = pathlib.Path(__file__).resolve().parent
esc = lambda t: html.escape(str(t), quote=True)
C = json.load(open(D / "contests.json"))
CSS = re.search(r'^CSS = """(.*?)"""', (D / "desk.py").read_text(), re.S | re.M).group(1)
NOW = datetime.datetime.utcnow().strftime("%d %b %Y")
DESK = C.get("desk_url", "")

page = f'''<title>Contest Radar</title>
<style>{CSS}
/* Contest Radar: the desk's tokens; one column of contests sorted by deadline, filters above, your tracking inline on each row. */
.k{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-top:22px}} .k div{{background:var(--surface);border:1px solid var(--line);border-radius:9px;padding:12px 14px}} .k b{{display:block;font:400 30px/1.05 var(--display);font-variant-numeric:tabular-nums}} .k span{{font:600 10px/1.3 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}}
.soon{{display:flex;gap:8px;overflow-x:auto;padding-bottom:6px;scrollbar-width:thin}} .soon a{{flex:0 0 auto;min-width:190px;max-width:240px;text-decoration:none;background:var(--surface);border:1px solid var(--line);border-radius:9px;padding:10px 12px}} .soon a:hover{{border-color:var(--gold-line)}} .soon .d{{font:600 11px/1 var(--mono);color:var(--gold)}} .soon .t{{display:block;font-size:14px;margin-top:6px;line-height:1.3}} .soon .o{{font-size:12px;color:var(--ink-3)}}
.bar{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 14px}} .bar input[type=search]{{flex:1 1 220px;min-width:0;font:15px var(--body);padding:9px 12px;border-radius:8px;border:1px solid var(--line);background:var(--surface);color:var(--ink)}} .bar select{{font:13px var(--body);padding:8px 10px;border-radius:8px;border:1px solid var(--line);background:var(--surface);color:var(--ink)}}
.chips{{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}} .chips button{{font:600 10.5px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;padding:8px 11px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--ink-2);cursor:pointer}} .chips button[aria-pressed=true]{{background:var(--ink);color:var(--ground);border-color:var(--ink)}}
.chips button:focus-visible,.row a:focus-visible,.row select:focus-visible,.row input:focus-visible,.bar *:focus-visible{{outline:2px solid var(--gold);outline-offset:2px}}
.count{{font:500 12px var(--mono);color:var(--ink-3);margin:0 0 10px}}
.rows{{display:grid;gap:10px}} .row{{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--line);border-radius:10px;padding:14px 16px;display:grid;grid-template-columns:minmax(0,1fr) 210px;gap:8px 18px}} .row[data-st=open]{{border-left-color:var(--jade)}} .row[data-st=upcoming]{{border-left-color:var(--gold-line)}} .row[data-st=recurring]{{border-left-color:var(--void-line)}} .row[data-st=closed]{{opacity:.72}}
.row h3{{margin:0;font:600 17px/1.3 var(--body);text-wrap:balance}} .row .org{{font-size:13px;color:var(--ink-3)}} .row .meta{{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}} .pill{{font:600 10px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;padding:5px 8px;border-radius:5px;border:1px solid var(--line);background:var(--surface-2);color:var(--ink-2)}} .pill.open{{background:var(--jade-soft);color:var(--jade);border-color:var(--jade-line)}} .pill.upcoming{{background:var(--gold-soft);color:var(--gold);border-color:var(--gold-line)}} .pill.recurring{{background:var(--void-soft);color:var(--void);border-color:var(--void-line)}} .pill.free{{background:var(--jade-soft);color:var(--jade);border-color:var(--jade-line)}} .pill.ai-bad{{background:var(--coral-soft);color:var(--coral);border-color:var(--coral-line)}}
.row dl{{display:grid;grid-template-columns:auto minmax(0,1fr);gap:3px 12px;margin:8px 0 0;font-size:13.5px}} .row dt{{font:600 10px/1.9 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}} .row dd{{margin:0;color:var(--ink-2);overflow-wrap:anywhere}} .row .fit{{margin:8px 0 0;font-size:14px}}
.row .side{{display:grid;gap:8px;align-content:start}} .dl{{font:400 26px/1 var(--display);font-variant-numeric:tabular-nums}} .dl small{{display:block;font:500 11px/1.4 var(--mono);color:var(--ink-3);margin-top:4px}} .row select,.row input{{width:100%;font:13px var(--body);padding:7px 9px;border-radius:7px;border:1px solid var(--line);background:var(--ground);color:var(--ink)}} .links{{display:flex;flex-wrap:wrap;gap:8px;font-size:13px}} .links a{{color:var(--ink-2)}} .tr{{font:500 11px var(--mono);color:var(--ink-3)}} .saved{{color:var(--jade)}} .err{{color:var(--coral)}}
.rank{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:10px}} .rank div{{background:var(--surface);border:1px solid var(--line);border-radius:9px;padding:12px 14px}} .rank b{{font:600 11px var(--mono);color:var(--gold)}} .rank h3{{margin:4px 0;font-size:16px}} .rank p{{margin:0;font-size:13.5px;color:var(--ink-2)}}
form.add{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));gap:8px;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px}} form.add input,form.add button{{font:14px var(--body);padding:9px 10px;border-radius:7px;border:1px solid var(--line);background:var(--ground);color:var(--ink);min-width:0}} form.add button{{background:var(--ink);color:var(--ground);cursor:pointer}}
@media (max-width:700px){{.row{{grid-template-columns:minmax(0,1fr)}}}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
</style>
<header class="top"><div class="wrap"><span class="eyebrow">{f'<a href="{esc(DESK)}" target="_blank" rel="noopener">Anchorframe SoM V2</a> · ' if DESK else ''}contest radar · built {NOW}</span>
<h1>Contest Radar</h1><p class="tag">Where to aim the next film, song and book.</p>
<p class="lede">{esc(C["_"])}</p>
<div class="k" id="kpis"></div></div></header>
<nav class="jump"><div class="wrap"><a href="#soon">Closing soon</a><a href="#list">All contests</a><a href="#platforms">The five platforms</a><a href="#add">Add one</a></div></nav>
<main class="wrap">
<section id="soon"><div class="sec-head"><h2>Closing soon</h2><p>The next deadlines among open and upcoming contests, soonest first. Dates are the organisers'; check the page before you submit.</p></div><div class="soon" id="soonlist"></div></section>
<section id="list"><div class="sec-head"><h2>All contests</h2><p>Higgsfield first, then the five closest platforms, then the wider and traditional ones. A coloured edge means open (green), upcoming (gold) or recurring (violet). Your status and note on each are kept for everyone who opens this page from claude.ai.</p></div>
<div class="chips" id="tiers" role="group" aria-label="Group"></div>
<div class="chips" id="sts" role="group" aria-label="Status"></div>
<div class="bar"><input type="search" id="q" placeholder="Search name, organiser, prize, rules" aria-label="Search contests">
<select id="sort" aria-label="Sort"><option value="deadline">Soonest deadline</option><option value="prize">Biggest top prize</option><option value="name">Name</option><option value="mine">My status</option></select>
<select id="fee" aria-label="Entry fee"><option value="">Any entry fee</option><option value="free">Free entry only</option></select>
<select id="ai" aria-label="AI policy"><option value="">Any AI policy</option><option value="ok">AI welcome or allowed</option></select></div>
<p class="count" id="count"></p><div class="rows" id="rows"></div></section>
<section id="platforms"><div class="sec-head"><h2>The five platforms</h2><p>{esc(C.get("platforms_note",""))}</p></div><div class="rank" id="rank"></div></section>
<section id="add"><div class="sec-head"><h2>Add a contest</h2><p>Found one that is not here? Add it; it joins the list for everyone with this page, marked as added. Claude folds added contests into contests.json on the next rebuild.</p></div>
<form class="add" id="addf"><input id="a-name" required placeholder="Contest name" aria-label="Contest name"><input id="a-url" type="url" placeholder="https:// official page" aria-label="Official page"><input id="a-dl" type="date" aria-label="Deadline"><input id="a-fee" placeholder="Entry fee (free, $10…)" aria-label="Entry fee"><input id="a-prize" placeholder="Top prize" aria-label="Top prize"><button type="submit" id="a-go">Add contest</button><span class="tr" id="a-msg"></span></form></section>
<footer>Built by <code>anchorframe/contests.py</code> from <code>contests.json</code> on {NOW}. Entries marked verified were read on the organiser's page that day; the others come from search results and need a check. Regenerate, don't hand-edit.</footer></main>
<script>
const DATA = {json.dumps(C, ensure_ascii=False)};
const ITEMS = DATA.items;
const TIER = {{higgsfield:'Higgsfield', platform:'Five platforms', wider:'Wider', traditional:'Traditional'}};
const STATUS = ['Not tracking','Interested','Planning','Entering','Submitted','Won','Passed'];
const S = {{tier:'all', st:'live', q:'', sort:'deadline', fee:'', ai:'', mine:{{}}, added:[], db:null}};
const $ = s => document.querySelector(s);
function h(tag, attrs, ...kids){{ const e = document.createElement(tag); for (const [k,v] of Object.entries(attrs||{{}})){{ if (v == null || v === false) continue; if (k.startsWith('on')) e.addEventListener(k.slice(2), v); else e.setAttribute(k, v === true ? '' : v); }} for (const c of kids.flat()) if (c != null) e.append(c.nodeType ? c : document.createTextNode(String(c))); return e; }}
const today = () => {{ const d = new Date(); d.setHours(0,0,0,0); return d; }};
function daysLeft(iso){{ if (!iso) return null; const d = new Date(iso + 'T23:59:59'); return Math.ceil((d - today()) / 86400000); }}
function status(x){{ const n = daysLeft(x.deadline); if (n != null && n < 0 && x.status !== 'recurring') return 'closed'; return x.status || 'unknown'; }}
const isFree = x => /free|\\$0\\b|no fee|no entry/i.test(x.entry_fee || '');
const aiOk = x => !x.ai_policy || /welcome|allowed|not stated/i.test(x.ai_policy);
function all(){{ return ITEMS.concat(S.added); }}
function shown(){{
  let xs = all().filter(x => S.tier === 'all' || x.tier === S.tier);
  if (S.st === 'live') xs = xs.filter(x => ['open','upcoming','recurring','unknown'].includes(status(x)));
  else if (S.st !== 'all') xs = xs.filter(x => status(x) === S.st);
  if (S.fee === 'free') xs = xs.filter(isFree);
  if (S.ai === 'ok') xs = xs.filter(aiOk);
  if (S.q){{ const q = S.q.toLowerCase(); xs = xs.filter(x => [x.name,x.organizer,x.prize,x.requirements,x.kind,x.fit,x.dates_note].join(' ').toLowerCase().includes(q)); }}
  const tierOrder = {{higgsfield:0, platform:1, wider:2, traditional:3}};
  const dl = x => {{ const n = daysLeft(x.deadline); return n == null || n < 0 ? 1e9 : n; }};
  const cmp = {{deadline:(a,b) => dl(a)-dl(b) || (tierOrder[a.tier]??9)-(tierOrder[b.tier]??9),
    prize:(a,b) => (b.prize_usd_top||0)-(a.prize_usd_top||0), name:(a,b) => a.name.localeCompare(b.name),
    mine:(a,b) => STATUS.indexOf(myStatus(b))-STATUS.indexOf(myStatus(a)) || dl(a)-dl(b)}}[S.sort];
  return xs.sort(cmp);
}}
const myStatus = x => (S.mine[x.id] && S.mine[x.id].status) || 'Not tracking';
function money(n){{ return n ? '$' + (n >= 1e6 ? (n/1e6).toFixed(n % 1e6 ? 1 : 0) + 'M' : n >= 1e3 ? Math.round(n/1e3) + 'K' : n) : '—'; }}
function kpis(){{
  const xs = all(), live = xs.filter(x => ['open','upcoming'].includes(status(x)));
  const soon = live.filter(x => {{ const n = daysLeft(x.deadline); return n != null && n >= 0 && n <= 30; }});
  const box = (n, t) => h('div', null, h('b', null, String(n)), h('span', null, t));
  $('#kpis').replaceChildren(box(xs.length, 'contests on the radar'), box(xs.filter(x => status(x) === 'open').length, 'open now'), box(soon.length, 'closing in 30 days'),
    box(xs.filter(isFree).length, 'free to enter'), box(xs.filter(x => x.tier === 'higgsfield').length, 'from Higgsfield'), box(Object.values(S.mine).filter(m => m.status && m.status !== 'Not tracking').length, 'you are tracking'));
}}
function soon(){{
  const xs = all().filter(x => ['open','upcoming'].includes(status(x)) && daysLeft(x.deadline) != null && daysLeft(x.deadline) >= 0).sort((a,b) => daysLeft(a.deadline) - daysLeft(b.deadline)).slice(0, 10);
  $('#soonlist').replaceChildren(...(xs.length ? xs.map(x => h('a', {{href:'#c-' + x.id}}, h('span', {{class:'d'}}, daysLeft(x.deadline) === 0 ? 'today' : daysLeft(x.deadline) + ' days · ' + x.deadline), h('span', {{class:'t'}}, x.name), h('span', {{class:'o'}}, x.organizer || ''))) : [h('p', {{class:'tr'}}, 'No dated deadlines ahead in the list; see the recurring ones below.')]));
}}
function chips(){{
  const t = [['all','All']].concat(Object.entries(TIER));
  $('#tiers').replaceChildren(...t.map(([k,v]) => h('button', {{type:'button', 'aria-pressed': S.tier === k ? 'true' : 'false', onclick: () => {{ S.tier = k; render(); }}}}, v + ' · ' + (k === 'all' ? all().length : all().filter(x => x.tier === k).length))));
  const st = [['live','Open, upcoming, recurring'],['open','Open'],['upcoming','Upcoming'],['recurring','Recurring'],['closed','Closed'],['all','Everything']];
  $('#sts').replaceChildren(...st.map(([k,v]) => h('button', {{type:'button', 'aria-pressed': S.st === k ? 'true' : 'false', onclick: () => {{ S.st = k; render(); }}}}, v)));
}}
let timers = {{}};
function save(x, patch, msg){{
  if (!S.db){{ msg.textContent = 'Open this page from claude.ai to keep your tracking.'; msg.className = 'tr err'; return; }}
  const cur = Object.assign({{}}, S.mine[x.id] || {{}}, patch, {{at: new Date().toISOString()}});
  S.mine[x.id] = cur; msg.textContent = 'Saving…'; msg.className = 'tr';
  clearTimeout(timers[x.id]); timers[x.id] = setTimeout(async () => {{
    try {{ await S.db.collection('tracks').doc(x.id).set({{status: cur.status || 'Not tracking', note: cur.note || '', at: cur.at}}); msg.textContent = 'Saved'; msg.className = 'tr saved'; }}
    catch(e){{ msg.textContent = (e && e.code === 'permission_denied') ? 'You can view this page but not change it.' : 'Could not save: ' + ((e && e.message) || 'try again'); msg.className = 'tr err'; }}
  }}, 500);
}}
function row(x){{
  const st = status(x), n = daysLeft(x.deadline), m = S.mine[x.id] || {{}}, msg = h('span', {{class:'tr'}}, m.at ? 'Updated ' + new Date(m.at).toLocaleDateString() : '');
  const sel = h('select', {{'aria-label':'My status for ' + x.name, id:'st-' + x.id, onchange: e => save(x, {{status: e.target.value}}, msg)}}, ...STATUS.map(s => h('option', {{value:s, selected: (m.status || 'Not tracking') === s}}, s)));
  const note = h('input', {{type:'text', id:'nt-' + x.id, placeholder:'Note', 'aria-label':'Note for ' + x.name, value: m.note || '', oninput: e => save(x, {{note: e.target.value}}, msg)}});
  const pills = [h('span', {{class:'pill ' + st}}, st), h('span', {{class:'pill'}}, x.kind || 'other'), h('span', {{class:'pill'}}, TIER[x.tier] || x.tier || 'added')];
  if (x.platform_rank) pills.push(h('span', {{class:'pill'}}, 'platform #' + x.platform_rank));
  if (isFree(x)) pills.push(h('span', {{class:'pill free'}}, 'free entry'));
  if (x.ai_policy && /restrict|ban/i.test(x.ai_policy)) pills.push(h('span', {{class:'pill ai-bad'}}, x.ai_policy));
  if (x.added) pills.push(h('span', {{class:'pill'}}, 'added'));
  const dl = [['Entry', x.entry_fee], ['Prize', x.prize], ['Dates', x.dates_note], ['Rules', x.requirements], ['AI', x.ai_policy || x.tool_lock], ['Effort', x.effort]].filter(r => r[1]);
  const src = (x.sources || []).filter(u => u && u !== x.url);
  return h('article', {{class:'row', id:'c-' + x.id, 'data-st': st}},
    h('div', {{style:'min-width:0'}}, h('h3', null, x.name), h('div', {{class:'org'}}, x.organizer || ''), h('div', {{class:'meta'}}, pills),
      h('dl', null, ...dl.flatMap(([k,v]) => [h('dt', null, k), h('dd', null, v)])), x.fit ? h('p', {{class:'fit'}}, x.fit) : null,
      h('div', {{class:'links'}}, x.url ? h('a', {{href:x.url, target:'_blank', rel:'noopener'}}, 'Official page ↗') : null, ...src.slice(0, 4).map((u, i) => h('a', {{href:u, target:'_blank', rel:'noopener'}}, 'source ' + (i + 1) + ' ↗')), h('span', {{class:'tr'}}, x.verified === 'snippet' ? 'from search results — check' : /^\d{{4}}-/.test(x.verified || '') ? 'verified ' + x.verified : 'not checked — from memory, confirm everything'))),
    h('div', {{class:'side'}}, h('div', {{class:'dl'}}, n == null ? '—' : n < 0 ? 'closed' : n === 0 ? 'today' : n + 'd', h('small', null, x.deadline ? 'deadline ' + x.deadline : 'no fixed deadline')),
      h('div', {{class:'tr'}}, 'Top prize ' + money(x.prize_usd_top)), sel, note, msg));
}}
function render(){{
  chips(); kpis(); soon();
  const xs = shown(); $('#count').textContent = xs.length + ' shown';
  $('#rows').replaceChildren(...(xs.length ? xs.map(row) : [h('p', {{class:'tr'}}, 'Nothing matches these filters. Clear the search or pick Everything.')]));
}}
function rank(){{
  const rs = (DATA.platforms || []).slice().sort((a,b) => a.rank - b.rank);
  $('#rank').replaceChildren(...rs.map(r => h('div', null, h('b', null, '#' + r.rank), h('h3', null, r.name), h('p', null, r.why), r.url ? h('p', null, h('a', {{href:r.url, target:'_blank', rel:'noopener'}}, 'contests page ↗')) : null)));
}}
$('#q').addEventListener('input', e => {{ S.q = e.target.value; render(); }});
$('#sort').addEventListener('change', e => {{ S.sort = e.target.value; render(); }});
$('#fee').addEventListener('change', e => {{ S.fee = e.target.value; render(); }});
$('#ai').addEventListener('change', e => {{ S.ai = e.target.value; render(); }});
$('#addf').addEventListener('submit', async e => {{
  e.preventDefault(); const msg = $('#a-msg');
  if (!S.db){{ msg.textContent = 'Open this page from claude.ai to add contests.'; msg.className = 'tr err'; return; }}
  const name = $('#a-name').value.trim(); if (!name) return;
  const doc = {{name, url: $('#a-url').value.trim(), deadline: $('#a-dl').value || null, entry_fee: $('#a-fee').value.trim(), prize: $('#a-prize').value.trim(), at: new Date().toISOString()}};
  $('#a-go').disabled = true;
  try {{ await S.db.collection('added').add(doc); e.target.reset(); msg.textContent = 'Added'; msg.className = 'tr saved'; }}
  catch(err){{ msg.textContent = 'Could not add: ' + ((err && err.message) || 'try again'); msg.className = 'tr err'; }}
  $('#a-go').disabled = false;
}});
rank(); render();
(async () => {{
  const db = window.claude && window.claude.use ? await window.claude.use('db') : null;
  if (!db) return;
  S.db = db;
  db.collection('tracks').onSnapshot(snap => {{ const m = {{}}; snap.docs.forEach(d => {{ m[d.id] = d.data(); }}); S.mine = m; render(); }}, () => {{}});
  db.collection('added').onSnapshot(snap => {{ S.added = snap.docs.map(d => Object.assign({{id: 'added-' + d.id, tier: 'added', kind: 'other', status: 'unknown', added: true, organizer: 'added by you'}}, d.data())); render(); }}, () => {{}});
}})();
</script>'''
(D / "contests.html").write_text(page)
print(f"wrote contests.html · {len(page)//1024} KB · {len(C['items'])} contests")
