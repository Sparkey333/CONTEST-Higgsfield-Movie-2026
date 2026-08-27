# -*- coding: utf-8 -*-
"""Derive the hosted preview of the Desk from index.html.

The preview exists so the Desk can be opened and driven in a browser without a
local checkout. Four things differ from the real page, and all four are
consequences of a single HTML file being served on its own origin:

  * the three document links have nothing to point at
  * the manifest and service worker have nothing to fetch
  * the artifact CSP blocks the API call behind Send
  * a hosted page cannot hand a viewer a file, so every export is inert
  * a banner has to say which build this is, or the differences read as bugs

Everything else — the capture checklist, the image intake, the block builder,
the log and its deltas, the vault — is the same code as the shipped page.
Run from the repo root:  python3 design/build-preview.py
"""
import io, re, sys

SRC = "index.html"
OUT = "design/desk-preview.html"

s = io.open(SRC, encoding="utf-8").read()
before = len(s)


def once(old, new, what):
    """Replace exactly once, or fail loudly — a silent no-op would ship a
    preview that still claims to be the real thing."""
    global s
    if s.count(old) != 1:
        sys.exit("build-preview: expected 1 occurrence of %s, found %d"
                 % (what, s.count(old)))
    s = s.replace(old, new)


# ── 1 · nothing to fetch on this origin ──────────────────────────────────────
once('<link rel="manifest" href="app.webmanifest">\n', "", "manifest link")
once('''/* ================= SERVICE WORKER ================= */
if("serviceWorker" in navigator && location.protocol.indexOf("http")===0){
  window.addEventListener("load",function(){ navigator.serviceWorker.register("sw.js").catch(function(){}); });
}''',
     '/* Service worker omitted: this build is one file on its own origin. */',
     "service worker")

# ── 2 · the document cards have nowhere to go ────────────────────────────────
s = re.sub(r'<a class="doc( primary)?" href="[^"]+\.html">',
           lambda m: '<div class="doc%s unavail">' % (m.group(1) or ""), s)
s = s.replace("</a>\n  </div>\n</section>", "</div>\n  </div>\n</section>")
if '<a class="doc' in s:
    sys.exit("build-preview: a doc card was left as a link")

once('''    <p>Three files, three jobs. The bible is where you work; the sheet is what you keep open beside
    Higgsfield; the audit is what you check yourself against when something feels thin.</p>''',
     '''    <p>Three files, three jobs. The bible is where you work; the sheet is what you keep open beside
    Higgsfield; the audit is what you check yourself against when something feels thin.</p>
    <p class="unavail-note">These three are not openable here &mdash; this preview is a single page,
    and they are separate files. Open them from the folder on your Mac.</p>''',
     "documents note")

# ── 3 · Send cannot work here, so it says so instead of failing ──────────────
once('<button class="b" id="send" disabled>Send with stored key</button>',
     '<button class="b" id="send" disabled title="Unavailable in the hosted preview">'
     'Send &mdash; local build only</button>',
     "send button")
once('''    document.getElementById("send").disabled=!SHOTS.length;''',
     '''      /* stays disabled: the hosted preview cannot reach the API */''',
     "send enable on build")
once('''    document.getElementById("send").disabled = !(SHOTS.length && document.getElementById("out").dataset.ready);''',
     '''    /* send stays disabled in this build */''',
     "send enable on intake")
once("""    <div class="note warn" style="margin-top:16px">
      <b>Send is the unverified path.</b> The copy-and-paste route is the one to trust &mdash; it works
      offline and always will. <b>Send</b> posts the images straight to the Anthropic API from this
      page using the key in your vault, which means the key is used in the browser and the screenshots
      leave the machine. It has not been exercised end to end from here, so treat a failure as
      expected rather than alarming, and fall back to copy.
    </div>""",
     """    <div class="note warn" style="margin-top:16px">
      PLACEHOLDER
    </div>""",
     "send warning")

# ── 3b · downloads are inert in the viewer, so they say so too ───────────────
# A hosted page cannot hand the viewer a file: the blob link fires and nothing
# lands. Disabling is honest; leaving three dead buttons is not.
once('<button class="b" id="dl-md" disabled>Download .md</button>',
     '<button class="b" id="dl-md" disabled title="Downloads do not work in the hosted preview">'
     'Download .md &mdash; local only</button>', "dl-md button")
once('<button class="b" id="dl-log" disabled>Export log as CSV</button>',
     '<button class="b" id="dl-log" disabled title="Downloads do not work in the hosted preview">'
     'Export CSV &mdash; local only</button>', "dl-log button")
once('<button class="b" id="env">Export .env</button>',
     '<button class="b" id="env" disabled title="Downloads do not work in the hosted preview">'
     'Export .env &mdash; local only</button>', "env button")
once('''    document.getElementById("dl-md").disabled=false;''',
     '''    /* dl-md stays disabled: downloads are inert in this build */''',
     "dl-md enable")
once('''    document.getElementById("dl-log").disabled=!L.length;''',
     '''    /* dl-log stays disabled: downloads are inert in this build */''',
     "dl-log enable")
once('''      PLACEHOLDER''',
     '''      <b>Send and the downloads are off in this build.</b> A hosted page may only talk to a short
      list of hosts, and it cannot hand you a file at all &mdash; so Send, Download&nbsp;.md,
      Export&nbsp;CSV and Export&nbsp;.env would each fail silently. They are disabled rather than left
      to look broken. <b>Copy block</b> works, and it is the route that matters: paste it into a chat
      and drag the screenshots in beside it.''',
     "send warning")

# ── 4 · say which build this is ──────────────────────────────────────────────
once('<span class="badge on">Installable</span>',
     '<span class="badge pv">Hosted preview</span>', "badge")
once('''  <p class="lede">The front door to the three documents that run this film, plus the two things that
  keep it honest &mdash; a status read you can hand to anyone, and one place for the keys. Everything
  here is a plain file on your own disk.</p>''',
     '''  <p class="lede">The front door to the three documents that run this film, plus the two things that
  keep it honest &mdash; a status read you can hand to anyone, and one place for the keys.</p>
  <p class="pv-note"><b>This is the hosted preview.</b> The status read and the vault are the same code
  as the real page and work fully. What is missing is everything that needs the folder around it: the
  three documents, offline install, and anything that saves a file. The real build is
  <code>index.html</code> in the repo.</p>''',
     "lede")

once("a.doc.primary{border-color:var(--gold-line);"
     "background:linear-gradient(180deg,var(--gold-soft),var(--surface) 62%)}",
     """a.doc.primary,.doc.primary{border-color:var(--gold-line);background:linear-gradient(180deg,var(--gold-soft),var(--surface) 62%)}
.doc.unavail{cursor:default;box-shadow:none;opacity:.72}
.doc.unavail:hover{transform:none;border-color:var(--line)}
.doc.unavail.primary:hover{border-color:var(--gold-line)}
.unavail-note{margin-top:10px !important;font-size:13.5px;color:var(--ink-3);font-style:italic}
.badge.pv{background:var(--void-soft);color:var(--void);border-color:var(--void-line)}
.pv-note{margin:16px 0 0;max-width:64ch;font-size:14.5px;line-height:1.6;color:var(--ink-2);
  border-left:3px solid var(--void);padding-left:15px}
.pv-note b{color:var(--ink)}""",
     "doc primary style")

# the cards keep .doc styling, which was written for an <a>
s = s.replace(".docs{display:grid", "div.doc{text-decoration:none}\n.docs{display:grid")

once("<title>Production Desk</title>",
     "<title>Production Desk</title>", "title")

io.open(OUT, "w", encoding="utf-8").write(s)
print("%s -> %s  (%d -> %d bytes)" % (SRC, OUT, before, len(s)))
