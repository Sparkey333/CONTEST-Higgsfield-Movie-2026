#!/usr/bin/env python3
"""Build roster.html — what the account must hold when this film is done.

Derived from what the film attaches, not from what the account happens to
contain: handles are counted out of the 23 shot prompts and the 39 anchors, so
a handle listed here earns its place by being used somewhere. Anything the
account holds that does not appear here is on the delete list by definition.
"""
import json, os, re, html, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda p: json.load(open(os.path.join(ROOT, p), encoding="utf-8"))
em, plan, led = R("design/element-map.json"), R("design/anchor-plan.json"), R("design/shot-ledger.json")
prog, dial = R("design/progress.json"), R("design/dialogue.json")
bible = open(os.path.join(ROOT, "director-bible.html"), encoding="utf-8").read()

# --- usage, counted from the film itself -------------------------------------
start = bible.find('{id:"S1",mv:1'); end = bible.find('{id:"S23"')
region = bible[start:bible.find("\n]", end)]
shot = collections.defaultdict(set)
for m in re.finditer(r'\{id:"(S\d+)"', region):
    sid, nxt = m.group(1), region.find('{id:"S', m.end())
    for x in re.findall(r"@([a-z0-9-]+)", region[m.end(): nxt if nxt > 0 else len(region)]):
        shot[x].add(sid)
anc = collections.defaultdict(set)
for f in plan["frames"]:
    for x in (f.get("handles") or []): anc[x].add(f["f"])

GROUPS = [
 ("Lighting plates", "Four. Every frame on a board inherits one of these, which is why there is one canvas per plate and not one per scene.",
  ["plate-sun", "plate-ocean-dark", "plate-island", "plate-bombardment"]),
 ("Characters", "One identity per person. States are generated from the identity, never re-described.",
  ["oriane", "oriane-ascended", "oriane-damaged", "caedom-ascended-1", "caedom-before",
   "alder", "wren", "threadwright"]),
 ("The order", "The Vigil, and its members. A faction reads as one design or it reads as extras.",
  ["keeper", "keeper-kneel"]),
 ("Creatures", "The Turned in two domains, the leviathan, its plating, and the fused rider.",
  ["turned", "turned-water", "leviathan", "leviathan-plating", "lev-rider"]),
 ("Locations", "Six places the film can actually stand in.",
  ["courtyard-of-worlds", "keepers-isle", "nacre-beach", "white-temple",
   "machira-orbit", "corals-abyss"]),
 ("Props", "Objects the camera has to hold on.",
  ["founding-stone", "frozen-tear", "twelve-ships", "iron-spears"]),
 ("Effects", "Five things that are physics in this world, so they need a sheet rather than an adjective.",
  ["fx-hollow", "fx-kill-beat", "fx-segmented-mind", "fx-floating-mountain", "aura-shell"]),
 ("Rule sheets", "Never attached to a shot. They exist so a prompt can be written correctly, and deleting them at the gate is the easy mistake.",
  ["aura-grammar", "ladder-attunement", "ladder-oriane"]),
]

els = em["elements"]
dec = collections.Counter(v.get("decision") for v in els.values())
n_del = dec["delete"] + dec["delete (unreferenced)"]
souls = em["souls"]
soul_keep = {k: v for k, v in souls.items() if v.get("decision") == "keep"}
soul_del = {k: v for k, v in souls.items() if v.get("decision") == "delete"}
used_souls = {"oriane", "alder", "wren", "caedom-ascended"}

MUST = [
 ("Gate A — identity lock", "blocks 17 of the 20 remaining steps",
  "Look at every handle below in the Elements list and say yes or no once. Nothing downstream can "
  "start until it holds, because everything downstream inherits the faces it locks."),
 ("Replace the two Caedom sheets", "compliance and identity, one job",
  "@caedom-ascended-1 and @caedom-before are still backed by uploads rather than generations, and "
  "@caedom-ascended-1 is attached in four shots and four anchors. Eight candidates were generated "
  "on 8 Sep — pick two and swap them."),
 ("Verify six upload-backed handles", "the only disqualification risk on the board",
  "The rule is absolute: no real person's face or voice as an input, including your own. Six handles "
  "trace to a file rather than a generation and the repo cannot prove what that file was. Thirty "
  "seconds each in the account settles it."),
 ("Action the cull", "%d handles, %d legacy names, 2 Souls" % (n_del, len(em["legacy_elements"])),
  "Delete what the film never attaches. Two versions of the same character in the picker is how the "
  "wrong one ends up in a shot at two in the morning."),
 ("Twelve shots have no clip at all", "S3 S4 S5 S9 S13 S14 S15 S16 S17 S21 S22 S23",
  "Eleven of 23 shots have a concept clip. The other twelve have nothing. That is the real gap "
  "between here and a cut, and it is what route two on the three-routes sheet spends the budget on."),
 ("Cast three voices", "Oriane is cast, the rest are not",
  "Oriane is Kiki. Caedom, Alder and Wren have casting takes generated and nobody has chosen. "
  "Voice is 0.1 credits a line — it is the cheapest thing in the production and it is not done."),
 ("File everything into the one project", "Rule 7, and there is no API for it",
  "87 generations belong in the dedicated Cinema Studio project and the platform has no folder call, "
  "so this is hand work. project-1-filing.md is the list to work from."),
 ("Publish, and check it logged out", "the last way to lose",
  "The finished film has to be public. Open it in a private window before you call it submitted."),
]

def esc(s): return html.escape(str(s or ""))
o = []
o.append("""<title>Project Roster</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--ground:#0B0A09;--surface:#141210;--edge:#252019;--ink:#EDE6DA;--muted:#8C8477;--dim:#5F594F;
--gold:#E0A33A;--warn:#D9694E;--ok:#6FA8A0;
--serif:ui-serif,Georgia,"Iowan Old Style","Times New Roman",serif;
--sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.55}
.wrap{max-width:960px;margin:0 auto;padding:52px 24px 90px}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim);margin:0 0 14px}
h1{font-family:var(--serif);font-weight:400;font-size:clamp(28px,4.6vw,44px);margin:0 0 14px;letter-spacing:-.01em;text-wrap:balance}
.standfirst{color:var(--muted);max-width:62ch;margin:0}
header{border-bottom:1px solid var(--edge);padding-bottom:26px;margin-bottom:14px}
.tot{display:flex;flex-wrap:wrap;border:1px solid var(--edge);border-radius:3px;margin:28px 0 46px}
.tot div{flex:1 1 130px;padding:14px 18px;border-right:1px solid var(--edge)}
.tot div:last-child{border-right:0}
.tot b{display:block;font-family:var(--mono);font-size:20px;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.tot span{font-size:12px;color:var(--dim)}
h2{font-family:var(--serif);font-weight:400;font-size:24px;margin:46px 0 5px;letter-spacing:-.01em;
   display:flex;align-items:baseline;gap:12px}
h2 .ct{font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.12em;margin-left:auto}
.gnote{color:var(--dim);font-size:13.5px;margin:0 0 16px;max-width:66ch}
.tablewrap{overflow-x:auto;border:1px solid var(--edge);border-radius:3px}
table{border-collapse:collapse;width:100%;min-width:540px;font-size:14px}
th,td{text-align:left;padding:10px 14px;border-bottom:1px solid var(--edge);vertical-align:top}
thead th{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);font-weight:400;background:var(--surface)}
tbody tr:last-child td{border-bottom:0}
td.h{font-family:var(--mono);color:var(--ink)}
td.n{font-family:var(--mono);font-variant-numeric:tabular-nums;color:var(--muted);white-space:nowrap}
td.w{color:var(--muted);font-size:13px}
.flag{font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;
 border:1px solid;border-radius:2px;padding:1px 5px;margin-left:7px;white-space:nowrap}
.f-rep{color:var(--warn);border-color:var(--warn)}
.f-ref{color:var(--dim);border-color:var(--edge)}
ol.must{list-style:none;counter-reset:m;padding:0;margin:0}
ol.must li{counter-increment:m;border:1px solid var(--edge);border-left:2px solid var(--gold);
 border-radius:3px;background:var(--surface);padding:16px 20px 17px 22px;margin-bottom:11px}
ol.must .t{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px;margin-bottom:6px}
ol.must .num{font-family:var(--mono);font-size:11px;color:var(--dim)}
ol.must .name{font-family:var(--serif);font-size:19px}
ol.must .why{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;
 color:var(--gold);margin-left:auto}
ol.must p{margin:0;color:var(--muted);font-size:14px;max-width:70ch}
.note{border:1px solid var(--edge);border-left:2px solid var(--warn);border-radius:3px;
 padding:16px 20px;margin:16px 0 0;background:var(--surface)}
.note h3{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--warn);margin:0 0 8px;font-weight:400}
.note p{margin:0;color:var(--muted);font-size:14px;max-width:68ch}
footer{border-top:1px solid var(--edge);margin-top:58px;padding-top:18px;color:var(--dim);font-size:12px;font-family:var(--mono)}
</style>
<div class="wrap">
<header>
<p class="eyebrow">Matter of Light &middot; roster &middot; 10 Sep 2026</p>
<h1>What the account holds when this film is finished</h1>
<p class="standfirst">Counted out of the film, not out of the account. Every handle below is attached
by a shot prompt or an anchor. Anything in the account that is not on this page is on the delete list.</p>
</header>""")

tot_keep = sum(len(g[2]) for g in GROUPS)
o.append('<div class="tot">'
 '<div><b>__K__</b><span>reference handles</span></div>'
 '<div><b>__S__</b><span>Souls kept</span></div>'
 '<div><b>__D__</b><span>handles to delete</span></div>'
 '<div><b>__L__</b><span>legacy names</span></div>'
 '<div><b>39</b><span>anchor frames</span></div>'
 '</div>'.replace("__K__", str(tot_keep)).replace("__S__", str(len(soul_keep)))
 .replace("__D__", str(n_del)).replace("__L__", str(len(em["legacy_elements"]))))

for name, note, hs in GROUPS:
    o.append('<h2>%s<span class="ct">%d</span></h2><p class="gnote">%s</p>' % (esc(name), len(hs), esc(note)))
    o.append('<div class="tablewrap"><table><thead><tr><th>Handle</th><th>Shots</th>'
             '<th>Anchors</th><th>Where it earns its place</th></tr></thead><tbody>')
    for x in hs:
        s = sorted(shot.get(x, []), key=lambda v: int(v[1:]))
        d = els.get(x, {}).get("decision", "")
        flag = ('<span class="flag f-rep">replace</span>' if d == "replace"
                else '<span class="flag f-ref">reference only</span>' if not s and not anc.get(x) else "")
        o.append('<tr><td class="h">@%s%s</td><td class="n">%d</td><td class="n">%d</td><td class="w">%s</td></tr>'
                 % (esc(x), flag, len(s), len(anc.get(x, [])),
                    esc(", ".join(s) if s else "written into prompts, never attached")))
    o.append('</tbody></table></div>')

o.append('<h2>Souls<span class="ct">%d kept &middot; %d to delete</span></h2>' % (len(soul_keep), len(soul_del)))
o.append('<p class="gnote">One identity per character, trained once. Every other state of them is '
         'generated from the Soul rather than re-described, which is the whole reason faces do not drift.</p>')
o.append('<div class="tablewrap"><table><thead><tr><th>Soul</th><th>Verdict</th>'
         '<th>Used by the film</th><th>Note</th></tr></thead><tbody>')
for k, v in list(soul_keep.items()) + list(soul_del.items()):
    keep = v.get("decision") == "keep"
    o.append('<tr><td class="h">%s</td><td class="n" style="color:%s">%s</td><td class="n">%s</td><td class="w">%s</td></tr>'
             % (esc(k), "var(--ok)" if keep else "var(--warn)", "keep" if keep else "delete",
                "yes" if k in used_souls else "no",
                esc(v.get("note") or v.get("why") or
                    ("attached in shot prompts" if k in used_souls
                     else "kept for the before/after pair; the film never cuts to the mortal form"))))
o.append('</tbody></table></div>')
o.append('<div class="note"><h3>The one to look at twice</h3><p>Four of the five kept Souls are used '
         'by the film. <b>caedom-before</b> is not — the film only ever attaches the ascended form. '
         'It is kept because the before/after pair is worth having, not because a shot needs it. If '
         'Gate A needs to be shorter, that is the row to drop.</p></div>')

o.append('<h2>Still to do<span class="ct">ordered by what it blocks</span></h2>')
o.append('<p class="gnote">Not a list of everything left. A list of the things that stop other things.</p>')
o.append('<ol class="must">')
for i, (name, why, body) in enumerate(MUST, 1):
    o.append('<li><div class="t"><span class="num">%02d</span><span class="name">%s</span>'
             '<span class="why">%s</span></div><p>%s</p></li>' % (i, esc(name), esc(why), esc(body)))
o.append('</ol>')

o.append('<footer>Built from element-map.json, anchor-plan.json, shot-ledger.json and the bible&rsquo;s '
         'shot prompts &middot; rebuild with design/build-roster.py &middot; %s of 34 steps done, %s days left'
         '</footer></div>' % (prog["rollup"]["done"], prog["days_left"]))

open(os.path.join(ROOT, "roster.html"), "w", encoding="utf-8").write("\n".join(o))
print("roster.html — %d handles, %d Souls kept, %d handles + %d legacy to delete"
      % (tot_keep, len(soul_keep), n_del, len(em["legacy_elements"])))
