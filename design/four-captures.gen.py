# -*- coding: utf-8 -*-
"""Instrument Dark — the four-capture plate.

The apertures encode the film's own hierarchy law: a core plate is brightest at
its centre with no rim; a detail plate is bright at the rim and dark at the
core. Anyone who knows the bible reads the ranking without a legend.
"""
import io, math

W, H = 1600, 1000
AMBER = "#FFBE4A"
INDIGO = "#9B9DFF"

PLATES = [
    dict(n="01", kind="core",   name="Folder tree, expanded",
         line="Every folder open, counts legible.",
         tail="Take this one even if you take nothing else."),
    dict(n="02", kind="core",   name="Elements<span class='ar'>→</span>Characters",
         line="Every handle with its image count.",
         tail="Drift shows up here first."),
    dict(n="03", kind="detail", name="Assets filtered to Liked",
         line="What you chose, not just what you made.",
         tail="Leave the filter chips visible."),
    dict(n="04", kind="detail", name="The generate bar",
         line="Model, ratio, duration.",
         tail="Ten seconds, and it catches wrong settings."),
]

RULES = [("A", "Full window", "never a crop"),
         ("B", "One screen per image", "never a collage"),
         ("C", "Never scale down", "the counts stop being legible")]


def ticks(cx, cy, r0, r1, count, colour, w=1.0, every=0, longer=0.0):
    """Radial ticks — the repetition that makes the field read as an instrument."""
    out = []
    for i in range(count):
        a = (i / count) * 2 * math.pi - math.pi / 2
        rr = r1 + (longer if (every and i % every == 0) else 0)
        x0, y0 = cx + r0 * math.cos(a), cy + r0 * math.sin(a)
        x1, y1 = cx + rr * math.cos(a), cy + rr * math.sin(a)
        out.append(
            '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
            'stroke-width="%.2f" stroke-linecap="butt"/>' % (x0, y0, x1, y1, colour, w))
    return "".join(out)


def aperture(idx, kind):
    """One observation field. 220 x 220."""
    S = 220
    c = S / 2
    uid = "ap%d" % idx
    core = kind == "core"
    hue = AMBER if core else INDIGO

    if core:
        # brightest at the centre, no edge
        grad = (
            '<radialGradient id="g%s" cx="50%%" cy="50%%" r="50%%">'
            '<stop offset="0%%" stop-color="#FFF6DF" stop-opacity="1"/>'
            '<stop offset="14%%" stop-color="%s" stop-opacity=".92"/>'
            '<stop offset="38%%" stop-color="%s" stop-opacity=".40"/>'
            '<stop offset="68%%" stop-color="%s" stop-opacity=".12"/>'
            '<stop offset="100%%" stop-color="%s" stop-opacity="0"/>'
            '</radialGradient>' % (uid, hue, hue, hue, hue))
        centre = ('<circle cx="%g" cy="%g" r="7.5" fill="#FFF9EC"/>'
                  '<circle cx="%g" cy="%g" r="15" fill="none" stroke="%s" '
                  'stroke-width=".7" opacity=".55"/>' % (c, c, c, c, hue))
    else:
        # bright at the rim, hollow at the centre
        grad = (
            '<radialGradient id="g%s" cx="50%%" cy="50%%" r="50%%">'
            '<stop offset="0%%" stop-color="%s" stop-opacity="0"/>'
            '<stop offset="46%%" stop-color="%s" stop-opacity="0"/>'
            '<stop offset="64%%" stop-color="%s" stop-opacity=".30"/>'
            '<stop offset="78%%" stop-color="%s" stop-opacity=".62"/>'
            '<stop offset="90%%" stop-color="%s" stop-opacity=".16"/>'
            '<stop offset="100%%" stop-color="%s" stop-opacity="0"/>'
            '</radialGradient>' % (uid, hue, hue, hue, hue, hue, hue))
        centre = ('<circle cx="%g" cy="%g" r="7.5" fill="none" stroke="%s" '
                  'stroke-width="1.1" opacity=".8"/>' % (c, c, hue))

    rings = "".join(
        '<circle cx="%g" cy="%g" r="%g" fill="none" stroke="#2A3145" '
        'stroke-width=".6" opacity="%s"/>' % (c, c, r, o)
        for r, o in ((92, ".85"), (68, ".55"), (44, ".38")))

    return (
        '<svg class="ap" width="%d" height="%d" viewBox="0 0 %d %d" aria-hidden="true">'
        '<defs>%s</defs>'
        '<circle cx="%g" cy="%g" r="92" fill="url(#g%s)"/>'
        '%s%s'
        '<circle cx="%g" cy="%g" r="103" fill="none" stroke="#2A3145" stroke-width=".8"/>'
        '%s%s'
        '</svg>'
    ) % (S, S, S, S, grad, c, c, uid, rings, centre, c, c,
         ticks(c, c, 96, 103, 72, "#2A3145", .7, 6, 5),
         ticks(c, c, 103, 110, 4, hue, 1.1))


def registration(x, y, size=13, col="#2A3145"):
    return ('<g stroke="%s" stroke-width=".9">'
            '<line x1="%g" y1="%g" x2="%g" y2="%g"/>'
            '<line x1="%g" y1="%g" x2="%g" y2="%g"/></g>'
            % (col, x - size, y, x + size, y, x, y - size, x, y + size))


def scale_bar(x, y0, y1, n=40):
    """Measurement rule down the left edge — the apparatus this plate came from."""
    out = []
    for i in range(n + 1):
        t = y0 + (y1 - y0) * i / n
        long = (i % 5 == 0)
        out.append('<line x1="%g" y1="%.2f" x2="%g" y2="%.2f" stroke="#2A3145" '
                   'stroke-width=".8" opacity="%s"/>'
                   % (x, t, x + (12 if long else 6), t, "1" if long else ".6"))
    return "".join(out)


cards = []
for i, p in enumerate(PLATES):
    core = p["kind"] == "core"
    cards.append(
        '<article class="plate">'
        '  <div class="apwrap">%s</div>'
        '  <div class="num %s">%s</div>'
        '  <h2>%s</h2>'
        '  <p class="l">%s</p>'
        '  <p class="t">%s</p>'
        '  <div class="tag %s">%s</div>'
        '</article>'
        % (aperture(i, p["kind"]), "c" if core else "d", p["n"], p["name"],
           p["line"], p["tail"], "c" if core else "d",
           "CORE" if core else "ADDS DETAIL"))

rules = "".join(
    '<div class="rule"><span class="rk">%s</span>'
    '<span class="rn">%s</span><span class="rd">%s</span></div>' % r
    for r in RULES)

HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<style>
@font-face{font-family:"Plate";src:url("f/InstrumentSerif-Regular.ttf")format("truetype");font-weight:400}
@font-face{font-family:"Numeral";src:url("f/BigShoulders-Bold.ttf")format("truetype");font-weight:700}
@font-face{font-family:"Body";src:url("f/InstrumentSans-Regular.ttf")format("truetype");font-weight:400}
@font-face{font-family:"Body";src:url("f/InstrumentSans-Bold.ttf")format("truetype");font-weight:700}
@font-face{font-family:"Mark";src:url("f/GeistMono-Regular.ttf")format("truetype");font-weight:400}

:root{
  --ground:#07080D; --ink:#F4F0E6; --ink2:#9BA2B6; --ink3:#565D73;
  --line:#1E2331; --amber:#FFBE4A; --indigo:#9B9DFF;
}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%(W)dpx;height:%(H)dpx}
body{background:var(--ground);color:var(--ink);font-family:"Body",sans-serif;
  position:relative;overflow:hidden;-webkit-font-smoothing:antialiased}

/* the field everything is observed against */
.grid{position:absolute;inset:0;pointer-events:none;
  background-image:radial-gradient(circle at 1px 1px,#161B27 1px,transparent 0);
  background-size:26px 26px;opacity:.5}
.vig{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(ellipse 130%% 105%% at 50%% 42%%,transparent 52%%,rgba(4,5,9,.62) 100%%)}
svg.marks{position:absolute;inset:0;pointer-events:none}

.page{position:absolute;inset:0;padding:66px 78px 58px;display:flex;flex-direction:column}

/* ---------- header ---------- */
header{display:flex;justify-content:space-between;align-items:flex-start;gap:40px}
.eyebrow{font-family:"Mark",monospace;font-size:10.5px;letter-spacing:.42em;
  text-transform:uppercase;color:var(--ink3);margin-bottom:19px}
h1{font-family:"Plate",serif;font-size:75px;line-height:.9;letter-spacing:-.012em;
  color:var(--ink);font-weight:400}
h1 em{font-style:italic;color:var(--amber)}
.sub{margin-top:17px;font-size:15.5px;line-height:1.55;color:var(--ink2);
  max-width:54ch;text-wrap:balance}
.meta{text-align:right;font-family:"Mark",monospace;font-size:10px;line-height:2.15;
  letter-spacing:.15em;color:var(--ink3);text-transform:uppercase;white-space:nowrap;padding-top:4px}
.meta b{color:var(--ink2);font-weight:400}

hr.h{border:0;border-top:1px solid var(--line);margin:38px 0 0}

/* ---------- plates ---------- */
.plates{flex:1;display:grid;grid-template-columns:repeat(4,1fr);
  column-gap:30px;padding:14px 0;align-content:center;align-items:start}
.plate{display:flex;flex-direction:column;align-items:center;text-align:center;
  position:relative;padding:0 6px}
.plate + .plate::before{content:"";position:absolute;left:-15px;top:16px;bottom:16px;
  width:1px;background:linear-gradient(180deg,transparent,var(--line) 22%%,var(--line) 78%%,transparent)}
.apwrap{height:238px;display:flex;align-items:center;justify-content:center}
svg.ap{width:238px;height:238px}
.num{font-family:"Numeral",sans-serif;font-size:82px;line-height:.8;letter-spacing:.005em;
  margin-top:16px;font-weight:700}
.num.c{color:var(--amber)}
.num.d{color:#565C87}
h2{font-family:"Body",sans-serif;font-weight:700;font-size:19.5px;line-height:1.28;
  letter-spacing:-.005em;margin-top:15px;color:var(--ink)}
p.l{font-size:14.5px;line-height:1.55;color:var(--ink2);margin-top:12px;
  max-width:25ch;text-wrap:balance;min-height:3.1em}
p.t{font-size:13px;line-height:1.5;color:var(--ink3);margin-top:8px;
  max-width:25ch;text-wrap:balance;min-height:3em}
.ar{font-family:"Mark",monospace;font-weight:400;font-size:.82em;
  color:var(--ink3);padding:0 .34em;vertical-align:.04em}
.tag{font-family:"Mark",monospace;font-size:9px;letter-spacing:.26em;text-transform:uppercase;
  margin-top:18px;padding:6px 10px;border:1px solid var(--line);border-radius:3px}
.tag.c{color:var(--amber);border-color:#4A3A18}
.tag.d{color:var(--ink3)}

/* ---------- footer ---------- */
hr.f{border:0;border-top:1px solid var(--line);margin:0 0 24px}
footer{display:flex;justify-content:space-between;align-items:flex-end;gap:40px}
.rules{display:flex;gap:52px}
.rule{display:flex;flex-direction:column;gap:6px}
.rk{font-family:"Mark",monospace;font-size:9px;letter-spacing:.3em;color:var(--amber)}
.rn{font-size:15px;font-weight:700;color:var(--ink);letter-spacing:-.003em}
.rd{font-size:12.5px;color:var(--ink3)}
.sig{text-align:right;font-family:"Mark",monospace;font-size:9.5px;line-height:1.95;
  letter-spacing:.19em;text-transform:uppercase;color:var(--ink3);white-space:nowrap}
</style></head><body>

<div class="grid"></div>

<svg class="marks" width="%(W)d" height="%(H)d" viewBox="0 0 %(W)d %(H)d">
  %(reg)s
  %(scale)s
</svg>

<div class="vig"></div>

<div class="page">
  <header>
    <div>
      <div class="eyebrow">Status read &middot; field protocol</div>
      <h1>Four <em>captures</em></h1>
      <p class="sub">Everything the project's state can be read from, in the order it should be
      taken. The first two carry it; the last two make the answer specific rather than approximate.</p>
    </div>
    <div class="meta">
      Plate&nbsp;I&nbsp;of&nbsp;I<br>
      <b>Daily</b> &middot; before work<br>
      Approx.&nbsp;<b>40 seconds</b><br>
      index.html &rarr; Status read
    </div>
  </header>

  <hr class="h">
  <div class="plates">%(cards)s</div>
  <hr class="f">

  <footer>
    <div class="rules">%(rules)s</div>
    <div class="sig">
      Production Desk<br>
      B.L. Barkey
    </div>
  </footer>
</div>
</body></html>""" % dict(
    W=W, H=H, cards="".join(cards), rules=rules,
    reg="".join(registration(x, y) for x, y in
                [(44, 44), (W - 44, 44), (44, H - 44), (W - 44, H - 44)]),
    scale=scale_bar(30, 150, H - 150))

io.open("card.html", "w", encoding="utf-8").write(HTML)
print("card.html written — %d bytes" % len(HTML))
