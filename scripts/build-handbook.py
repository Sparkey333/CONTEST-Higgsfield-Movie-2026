#!/usr/bin/env python3
"""
Build THE APERTURE METHOD — a printable, fillable development handbook.

    python3 scripts/build-handbook.py
    -> film/handbook/the-aperture-method.pdf

Part I  · nine sheets for a 3-5 minute generated short
Part II · the Long Aperture — a feature planner and script builder

The content lives in the SHEETS_* tables near the bottom. Edit those, re-run,
re-commit. Nothing here reads the repo, so the handbook stands alone if someone
lifts the PDF out of the project.
"""

import html
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Flowable, KeepTogether, Table, TableStyle,
)

OUT = "film/handbook/the-aperture-method.pdf"

# ── Palette ──────────────────────────────────────────────────────────────────
# This is print, not screen. The Void Room's brass reads muddy on paper, so it
# is darkened until it holds against cream at 9pt; the ink keeps a warm bias so
# it sits with the paper instead of punching a hole in it.
PAPER  = colors.HexColor("#FBF8F3")
INK    = colors.HexColor("#16130F")
BRASS  = colors.HexColor("#9A6F14")
RULE   = colors.HexColor("#D9D0C1")
MUTED  = colors.HexColor("#7C7368")
FAINT  = colors.HexColor("#EFE9DE")
BEAM   = colors.HexColor("#2C6C82")

PW, PH = LETTER
MARGIN = 0.82 * inch


def plain(s):
    """Content is authored with HTML entities for Paragraph. Canvas drawString
    does no parsing, so anything drawn directly must be unescaped first or the
    reader sees a literal &mdash; on the page."""
    return html.unescape(s)


def caps(s):
    """Uppercase a label bound for a Paragraph. Casing has to happen AFTER the
    entities resolve — .upper() on '&mdash;' yields '&MDASH;', which no parser
    resolves — and the result is re-escaped so a literal & still survives."""
    return html.escape(plain(s).upper(), quote=False)

# Times where the book is being a book, Courier where it is being a screenplay,
# Helvetica for the utility layer. The face tells you which mode you are in.
SERIF, SERIF_B, SERIF_I = "Times-Roman", "Times-Bold", "Times-Italic"
SANS,  SANS_B           = "Helvetica", "Helvetica-Bold"
MONO,  MONO_B           = "Courier", "Courier-Bold"


def S(name, **kw):
    kw.setdefault("fontName", SERIF)
    kw.setdefault("fontSize", 10)
    kw.setdefault("leading", 14.5)
    kw.setdefault("textColor", INK)
    return ParagraphStyle(name, **kw)


ST = {
    "body":     S("body", alignment=TA_JUSTIFY),
    "lede":     S("lede", fontSize=10.6, leading=15.2, textColor=colors.HexColor("#2E2820")),
    "small":    S("small", fontSize=8.6, leading=12.4, textColor=MUTED),
    "eyebrow":  S("eyebrow", fontName=SANS_B, fontSize=7.4, leading=10,
                  textColor=BRASS, spaceAfter=4),
    "h2":       S("h2", fontName=SERIF_B, fontSize=15, leading=18, spaceAfter=5),
    "h3":       S("h3", fontName=SANS_B, fontSize=8.6, leading=12,
                  textColor=INK, spaceBefore=6, spaceAfter=3),
    "rule":     S("rule", fontName=SERIF_I, fontSize=10, leading=13.8),
    "mono":     S("mono", fontName=MONO, fontSize=8.4, leading=11.6),
    "ex":       S("ex", fontName=SERIF_I, fontSize=9, leading=12.4, textColor=colors.HexColor("#3A342B")),
    "cover_t":  S("cover_t", fontName=SERIF_B, fontSize=34, leading=36,
                  alignment=TA_CENTER, spaceAfter=2),
    "cover_s":  S("cover_s", fontName=SANS, fontSize=8.4, leading=13,
                  alignment=TA_CENTER, textColor=MUTED),
    "part_n":   S("part_n", fontName=SANS_B, fontSize=8, leading=11,
                  textColor=BRASS, alignment=TA_CENTER),
    "part_t":   S("part_t", fontName=SERIF_B, fontSize=26, leading=30, alignment=TA_CENTER),
}


# ── Flowables ────────────────────────────────────────────────────────────────
class Rule(Flowable):
    """A hairline. Weight and colour carry hierarchy, so they are explicit."""

    def __init__(self, w=None, color=RULE, thickness=0.6, space=0, center=False):
        super().__init__()
        self.w, self.color, self.thickness, self.space = w, color, thickness, space
        self.center = center

    def wrap(self, aw, ah):
        self._w = self.w or aw
        # A short rule under centred type has to be centred too, and a flowable
        # always draws from the frame's left edge unless it claims full width.
        self._x = (aw - self._w) / 2.0 if self.center else 0
        return (aw if self.center else self._w, self.thickness + self.space)

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(self._x, self.space, self._x + self._w, self.space)


class SheetHead(Flowable):
    """Stop badge + sheet name. Drawn in the story, not in onPage, so the
    header can never lag a page behind the content it labels."""

    def __init__(self, stop, num, title, sub):
        super().__init__()
        self.stop, self.num, self.title, self.sub = stop, num, title, sub

    def wrap(self, aw, ah):
        self._w = aw
        return (aw, 50)

    def draw(self):
        c, w = self.canv, self._w
        badge_w, badge_h = 54, 26
        y = 50 - badge_h
        c.setFillColor(BRASS)
        c.roundRect(0, y, badge_w, badge_h, 3, stroke=0, fill=1)
        c.setFillColor(PAPER)
        c.setFont(SANS_B, 11)
        c.drawCentredString(badge_w / 2.0, y + 8.6, plain(self.stop))

        c.setFillColor(MUTED)
        c.setFont(SANS_B, 7.2)
        c.drawString(badge_w + 13, y + badge_h - 9, plain(self.num))
        c.setFillColor(INK)
        c.setFont(SERIF_B, 17)
        c.drawString(badge_w + 13, y + 2, plain(self.title))

        c.setFillColor(MUTED)
        c.setFont(SANS, 7.4)
        c.drawRightString(w, y + badge_h - 9, plain(self.sub))

        c.setStrokeColor(BRASS)
        c.setLineWidth(1.1)
        c.line(0, y - 9, w, y - 9)


class Lines(Flowable):
    """Ruled writing space. This is a workbook — the blank is the point."""

    def __init__(self, n=3, gap=18, label=None, indent=0):
        super().__init__()
        self.n, self.gap, self.label, self.indent = n, gap, label, indent

    def wrap(self, aw, ah):
        self._w = aw - self.indent
        self._h = self.n * self.gap + (12 if self.label else 0)
        return (aw, self._h)

    def draw(self):
        c = self.canv
        top = self._h
        if self.label:
            c.setFillColor(MUTED)
            c.setFont(SANS_B, 6.8)
            c.drawString(self.indent, top - 8, plain(self.label).upper())
            top -= 12
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        for i in range(self.n):
            y = top - (i + 1) * self.gap + 5
            c.line(self.indent, y, self.indent + self._w, y)


class Boxes(Flowable):
    """Checkbox list — used for gates, where the answer is binary on purpose."""

    def __init__(self, items, gap=14.4):
        super().__init__()
        self.items, self.gap = items, gap

    def wrap(self, aw, ah):
        self._w = aw
        self._h = len(self.items) * self.gap
        return (aw, self._h)

    def draw(self):
        c = self.canv
        for i, it in enumerate(self.items):
            y = self._h - (i + 1) * self.gap + 3
            c.setStrokeColor(MUTED)
            c.setLineWidth(0.7)
            c.rect(0, y, 8.5, 8.5, stroke=1, fill=0)
            c.setFillColor(INK)
            c.setFont(SERIF, 9.2)
            c.drawString(15, y + 1, plain(it))


def panel(title, body, style="rule", bg=FAINT, accent=BRASS):
    """A boxed statement. Reserved for the one non-negotiable line per sheet."""
    inner = [Paragraph(f'<font name="{SANS_B}" size="7" color="#9A6F14">{caps(title)}</font>', ST["small"]),
             Spacer(1, 3),
             Paragraph(body, ST[style])]
    t = Table([[inner]], colWidths=[PW - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def field_table(rows):
    """Label / blank pairs, for data that is short and structured."""
    data = [[Paragraph(f'<font name="{SANS_B}" size="7" color="#7C7368">{caps(a)}</font>', ST["small"]),
             Paragraph(b, ST["small"])] for a, b in rows]
    t = Table(data, colWidths=[1.55 * inch, PW - 2 * MARGIN - 1.55 * inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
    ]))
    return t


def h3(t):
    return Paragraph(t, ST["h3"])


def p(t, style="body"):
    return Paragraph(t, ST[style])


# ── Page furniture ───────────────────────────────────────────────────────────
def on_page(canv, doc):
    canv.saveState()
    canv.setFillColor(PAPER)
    canv.rect(0, 0, PW, PH, stroke=0, fill=1)
    if doc.page > 1:
        canv.setStrokeColor(RULE)
        canv.setLineWidth(0.5)
        canv.line(MARGIN, 0.62 * inch, PW - MARGIN, 0.62 * inch)
        canv.setFillColor(MUTED)
        canv.setFont(SANS, 7)
        canv.drawString(MARGIN, 0.44 * inch, "THE APERTURE METHOD")
        canv.drawRightString(PW - MARGIN, 0.44 * inch, str(doc.page))
    canv.restoreState()


def build(story):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = BaseDocTemplate(
        OUT, pagesize=LETTER,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=0.72 * inch, bottomMargin=0.88 * inch,
        title="The Aperture Method — a development handbook for generated film",
        author="The Void Room", subject="Film development handbook",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=on_page)])
    doc.build(story)


# ═════════════════════════════════════════════════════════════════════════════
#  CONTENT
# ═════════════════════════════════════════════════════════════════════════════

SHEETS_SHORT = [
    dict(
        stop="f/1.4", num="SHEET 01", title="The Ember", sub="LOCKS: THE FEELING",
        purpose="Everything downstream is a delivery system for one feeling. Name it before you "
                "own a single image, because every later decision is judged against it and nothing "
                "else. A film that generates beautifully and lands nothing has failed at this sheet, "
                "not at the render.",
        rule="Write the feeling in the viewer&rsquo;s chest at the last frame &mdash; in one sentence, "
             "with no plot in it. If your sentence contains a <i>then</i>, it is a plot and you have not "
             "done this sheet.",
        fields=[("The ember", 2), ("Why this, why you", 2)],
        table=[("Working title", ""), ("Runtime target", "3:15 &ndash; 4:30"),
               ("Last frame is", "&mdash;"), ("One-word tone", "&mdash;")],
        example="<b>Ember:</b> the ache of being seen clearly by something that cannot speak. "
                "<br/><b>Not an ember:</b> &ldquo;a lighthouse keeper meets a creature and <i>then</i> "
                "has to choose.&rdquo; That is a logline wearing a feeling&rsquo;s coat.",
        gate=["The sentence has no plot verb in it.",
              "You can say it aloud without looking down.",
              "Someone who has not read the idea repeats it back correctly."],
    ),
    dict(
        stop="f/2", num="SHEET 02", title="The Turn", sub="LOCKS: THE STRUCTURE",
        purpose="A three-to-five minute film supports exactly one reversal. Not two. The turn is the "
                "whole architecture: everything before it exists to make it land, everything after it "
                "is consequence. Locking it now is what stops the middle from sagging at 2:10, which "
                "is where shorts die.",
        rule="Name one thing that is true at 0:15 and false at 3:00. That flip is your turn. "
             "Place it at <b>60&ndash;70% of runtime</b> so the consequence has room to breathe.",
        fields=[("True at 0:15", 1), ("False at 3:00", 1), ("What flips it", 2)],
        table=[("Turn lands at", "approx. ____ : ____ (60&ndash;70%)"),
               ("Rule established by", "0:15 &mdash; no preamble, ever"),
               ("Ending recontextualises", "the opening image / the first sound / &mdash;")],
        example="<b>Lights Out</b> (2:41): true at 0:15 &mdash; the light protects her. False at the end "
                "&mdash; the light was never the boundary. One rule, set in fifteen seconds, escalated "
                "three times, then broken. That is the entire film.",
        gate=["There is exactly one reversal, not two.",
              "The rule is legible within the first fifteen seconds.",
              "The ending changes the meaning of the opening."],
    ),
    dict(
        stop="f/2.8", num="SHEET 03", title="The Page", sub="LOCKS: THE WHOLE",
        purpose="The film, entire, on one page &mdash; present tense, third person, no dialogue and no "
                "camera directions. This is the last sheet where changing your mind is free. After "
                "this, every change costs credits.",
        rule="Present tense. Behaviour only &mdash; what a stranger with the sound off would see. "
             "If a beat only works because of a line of dialogue, cut the beat or find the behaviour.",
        fields=[("The page", 11)],
        table=None,
        example="Write it as <i>she does, then she does, then the world answers</i>. If you find "
                "yourself typing &ldquo;she realises&rdquo;, stop &mdash; realisation is not "
                "photographable. Find the action that shows it.",
        gate=["No dialogue anywhere on the page.",
              "No interior states &mdash; nothing &lsquo;realises&rsquo;, &lsquo;feels&rsquo;, or &lsquo;remembers&rsquo;.",
              "It fits on one page without shrinking the type."],
    ),
    dict(
        stop="f/4", num="SHEET 04", title="The Subject", sub="LOCKS: IDENTITY",
        purpose="The single most expensive thing to fix later. Models do not remember your character "
                "between generations &mdash; they re-invent it every time. Everything you fail to pin "
                "here, you will pay for in re-rolls, or you will accept a face that changes between "
                "shots and lose the craft score outright.",
        rule="Pin the <b>invariants</b>: the handful of features that must survive every shot. Five to "
             "eight, no more &mdash; a list of thirty invariants is a list of none, because no prompt "
             "carries thirty.",
        fields=[("Invariants (5&ndash;8, non-negotiable)", 4), ("Deliberately variable", 2)],
        table=[("Reference set", "____ stills, locked before any motion"),
               ("Seed / character ID", "&mdash;"),
               ("Silhouette test", "recognisable in black at 3cm?  Y / N"),
               ("Costume changes", "none / ____ &mdash; each one is a new identity to hold")],
        example="<b>Invariants:</b> scar through the left eyebrow &middot; one shoulder permanently "
                "lower &middot; rust-coloured oilskin &middot; hair always wet &middot; never smiles. "
                "<b>Variable:</b> exact hair length, background crowd, cloud cover. Anything on the "
                "left list that drifts is a re-roll; anything on the right, you let go.",
        gate=["Invariants fit in one prompt fragment you can paste unchanged.",
              "The silhouette is identifiable with all detail removed.",
              "The reference set is locked and stored before a single motion generation."],
    ),
    dict(
        stop="f/5.6", num="SHEET 05", title="The World", sub="LOCKS: THE LOOK",
        purpose="Palette, light logic and texture, decided once and applied everywhere. Consistency of "
                "world is what makes generated footage read as photographed rather than assembled, and "
                "it is the cheapest craft score on the board &mdash; it costs discipline, not credits.",
        rule="Choose a <b>narrow</b> palette and a single light source logic, then shift it exactly "
             "once &mdash; at the turn. A palette that changes because the model felt like it reads as "
             "an accident. A palette that changes at the turn reads as authorship.",
        fields=[("Palette &mdash; four colours, named", 2), ("Light logic (source, direction, quality)", 2),
                ("What shifts at the turn", 2)],
        table=[("Era / place", "&mdash;"), ("Weather &amp; time of day", "&mdash;"),
               ("Texture floor", "grain / halation / lens dirt &mdash; pick and keep"),
               ("Forbidden", "colours and textures that must never appear")],
        example="<b>Alike</b> carries its entire plot in saturation &mdash; the world drains as the "
                "father conforms, and returns in one beat. A cinematographer juror reads that in three "
                "seconds and knows a person made a decision.",
        gate=["The palette is four colours or fewer, written as hex or named pigments.",
              "One light source dominates and you can say where it is in every shot.",
              "The shift happens once, at the turn, and nowhere else."],
    ),
    dict(
        stop="f/8", num="SHEET 06", title="The Grammar", sub="LOCKS: THE CAMERA",
        purpose="What the camera is allowed to do. Generated film drifts toward restless drifting "
                "motion because that is what the models reward, and restless motion is the single "
                "clearest tell of an unauthored AI reel. Constraint here is what buys you the "
                "cinematography vote.",
        rule="Write a short list of permissions and one <b>prohibition</b> you will not break. "
             "The prohibition matters more than the permissions.",
        fields=[("Lens set and why", 2), ("Camera height &amp; distance rules", 2),
                ("Movement permitted", 2), ("The prohibition", 1)],
        table=[("Aspect ratio", "&mdash;  (verify against contest rules)"),
               ("Frame rate / shutter feel", "&mdash;"),
               ("Coverage pattern", "e.g. wide &rarr; detail &rarr; face, repeated"),
               ("Camera moves at the turn", "the one place motion is allowed to change")],
        example="<b>Permitted:</b> 35mm, eye height, locked off, one slow push per act. "
                "<b>Prohibited:</b> no handheld, ever. Then break the lock-off exactly once &mdash; at "
                "the turn &mdash; and the movement means something because nothing else moved.",
        gate=["The prohibition is written and you have not broken it.",
              "Every camera move is motivated by a story beat, not by the model.",
              "Lens and height are stated in the shot ledger prompt text itself."],
    ),
    dict(
        stop="f/11", num="SHEET 07", title="The Beat Board", sub="LOCKS: THE CLOCK",
        purpose="The film as beats against a runtime budget. This is where you find out the film is "
                "four minutes long in your head and seven on paper &mdash; while that discovery is "
                "still free.",
        rule="Every beat gets a duration in seconds and a job. A beat with no job is cut. "
             "Sum the column. If it exceeds your target, cut beats &mdash; do not shorten all of them "
             "evenly, which is how films become incomprehensible.",
        fields=[],
        beatgrid=True,
        table=[("Target runtime", "3:15 &ndash; 4:30"), ("Beats", "typically 12&ndash;20"),
               ("Turn beat number", "&mdash;"), ("Running total", "________ sec")],
        example="Budget the ending generously. The last twenty seconds is where the recontextualisation "
                "lands, and it is the part every first-time editor starves.",
        gate=["Every beat has a duration and a one-line job.",
              "The total is inside the target, with the 3:00 floor cleared by margin.",
              "The turn sits at 60&ndash;70% of the running total."],
    ),
    dict(
        stop="f/16", num="SHEET 08", title="The Shot Ledger", sub="LOCKS: THE GENERATION",
        purpose="One row per shot, and the row is written <b>before</b> the credit is spent. This is "
                "the sheet that turns a pile of clips into a film, and in a contest that requires "
                "published prompts, it is also your submission artefact &mdash; it costs nothing extra "
                "if you keep it as you go, and it is unrecoverable if you do not.",
        rule="Never generate a shot that has no row. The row is written first, the credit is spent "
             "second. A shot generated on impulse is a shot you cannot reproduce.",
        fields=[],
        ledger=True,
        table=[("Continuity carry", "what must match the previous shot"),
               ("Keep / re-roll rule", "decide the accept threshold before you see the output"),
               ("Re-roll cap", "____ attempts, then change the shot, not the seed"),
               ("Credits spent", "________ / budget ________")],
        example="The re-roll cap is the discipline that saves the budget. Three attempts and it still "
                "will not hold? The shot is wrong, not the seed. Re-design it &mdash; usually by "
                "hiding the thing that keeps drifting.",
        gate=["Every shot has a row, and every row has a prompt you could paste again.",
              "Seeds and model names are recorded &mdash; you cannot reconstruct these later.",
              "Continuity carry is filled for every shot after the first."],
    ),
    dict(
        stop="f/22", num="SHEET 09", title="The Finish", sub="LOCKS: THE DELIVERY",
        purpose="Sound, music, compliance and publication. Sound is half of what an audience calls "
                "&lsquo;quality&rsquo; and it is where generated films most obviously give themselves "
                "away, because silence under moving images reads as unfinished.",
        rule="Cut picture to sound at least once, not only sound to picture. And run the compliance "
             "gate <b>before</b> the final render, not after &mdash; a disqualified film is worth zero "
             "regardless of how good it is.",
        fields=[("Sound spine (what carries the emotion)", 2), ("Music &mdash; source and licence", 2),
                ("The one silence", 1)],
        table=[("Music rights", "original / royalty-free &mdash; licence held?"),
               ("Watermark", "present on the delivered file?"),
               ("Runtime measured", "________  (floor is 3:00)"),
               ("Prompts published", "yes / no"), ("Public post live", "yes / no")],
        example="Place one deliberate silence. An audience does not notice good sound design, but it "
                "always notices the moment sound stops &mdash; and that is free, which makes it the "
                "best value in the whole production.",
        gate=["Runtime clears the floor with margin, measured on the delivered file.",
              "No copyrighted IP, characters, logos, or licensed music anywhere.",
              "No political and no religious statement, including in the caption.",
              "Watermark present; prompts and generation history published.",
              "Someone who has never seen it watched it end to end without touching the scrub bar."],
    ),
]


SHEETS_FEATURE = [
    dict(
        stop="L/1", num="SHEET 10", title="The Spine", sub="FEATURE &middot; LOCKS: THE ARGUMENT",
        purpose="A feature is long enough to be about something, and long enough to fall apart if it "
                "is not. The spine is the argument the film makes &mdash; stated as a question in the "
                "first act and answered by the last image.",
        rule="Write the theme as a <b>question</b>, never as a moral. &ldquo;What is a person owed by "
             "the family that made them?&rdquo; generates scenes. &ldquo;Family is complicated&rdquo; "
             "generates nothing.",
        fields=[("Theme, as a question", 2), ("The film&rsquo;s answer", 2),
                ("Logline (one sentence, with the irony in it)", 2)],
        table=[("Genre &amp; the promise it makes", "&mdash;"), ("Target runtime", "____ min / ____ pages"),
               ("Comparable films", "&mdash;"), ("Why now", "&mdash;")],
        example="Test: can two intelligent people disagree about the answer? If not, it is not a theme, "
                "it is a slogan, and the second act will have nothing to argue about.",
        gate=["The theme is a question, not a statement.",
              "The logline contains an irony or a reversal.",
              "The answer is delivered by an image, not by a speech."],
    ),
    dict(
        stop="L/2", num="SHEET 11", title="The Dossier", sub="FEATURE &middot; ONE PER CHARACTER",
        purpose="Characters generate plot; plot does not generate characters. Fill one of these for "
                "every character who changes. Anyone who does not change is a function &mdash; that is "
                "allowed, but know which is which.",
        rule="<b>Want</b> is what they chase and can state out loud. <b>Need</b> is what the story will "
             "give them instead. <b>The lie</b> is what they believe that is false. <b>The ghost</b> is "
             "the wound that made the lie reasonable. The arc is the lie breaking.",
        fields=[("Want (stated, pursued, external)", 1), ("Need (unstated, true, internal)", 1),
                ("The lie they believe", 1), ("The ghost that planted it", 1),
                ("What breaks the lie, and on what page", 2)],
        table=[("Name / age / role", "&mdash;"), ("First appearance", "page ____"),
               ("Contradiction", "the two things they are that should not coexist"),
               ("Speech signature", "rhythm, vocabulary, what they never say")],
        example="The antagonist gets this sheet too, and their lie should be the protagonist&rsquo;s "
                "lie taken one step further. That is what makes an antagonist frightening rather than "
                "merely opposed.",
        gate=["Want and need are different, and in tension.",
              "The ghost makes the lie reasonable rather than stupid.",
              "You know the page number where the lie breaks."],
    ),
    dict(
        stop="L/3", num="SHEET 12", title="The Four Movements", sub="FEATURE &middot; LOCKS: SHAPE",
        purpose="Act structure with page targets attached. Pages are the only honest unit &mdash; one "
                "page is roughly one minute, and a second act that runs sixty-five pages is a second "
                "act that is going to be cut by someone less sympathetic than you.",
        rule="Four movements, not three: the second act splits at the midpoint, and pretending it does "
             "not is why second acts sag. Each movement ends on a door closing behind the protagonist.",
        fields=[],
        movements=True,
        table=[("Total target", "____ pages"), ("Inciting incident", "page ____ (by 12)"),
               ("Midpoint reversal", "page ____ (dead centre)"),
               ("All is lost", "page ____ (approx. 75%)"), ("Climax begins", "page ____")],
        example="The midpoint is not a bump &mdash; it is where the protagonist stops reacting and "
                "starts acting, or the reverse. If your midpoint is just an event, you have a "
                "hundred-page first act with an intermission.",
        gate=["Each movement ends with an irreversible door closing.",
              "Page targets are written and the running total is tracked.",
              "The midpoint changes the protagonist's stance, not just the situation."],
    ),
    dict(
        stop="L/4", num="SHEET 13", title="The Eight Sequences", sub="FEATURE &middot; THE REAL UNIT",
        purpose="Features are built from roughly eight sequences of ten to fifteen pages, each with "
                "its own small want and its own turn. This is the working unit &mdash; more tractable "
                "than an act, larger than a scene, and the level at which structural problems are "
                "actually fixable.",
        rule="Every sequence answers a dramatic question posed at its start, and the answer should be "
             "<b>yes but</b> or <b>no and</b> &mdash; never a flat yes.",
        fields=[],
        sequences=True,
        table=None,
        example="If two adjacent sequences pose the same question, you have one sequence written twice. "
                "Merge them and take the pages back &mdash; you will want them at the end.",
        gate=["Eight sequences, each with a question and a complicated answer.",
              "No two sequences ask the same question.",
              "Page counts sum to the target with fewer than ten pages of slack."],
    ),
    dict(
        stop="L/5", num="SHEET 14", title="The Scene Ledger", sub="FEATURE &middot; ONE ROW PER SCENE",
        purpose="Every scene, with the job it does. A scene that cannot state its job is the scene "
                "that gets cut in the edit, after you have paid to shoot or generate it &mdash; find "
                "it here, where deleting it costs one line.",
        rule="Every scene must <b>turn</b>: something is different at the end than at the start. A "
             "scene where nothing changes is exposition wearing a costume.",
        fields=[],
        scenegrid=True,
        table=[("Total scenes", "____"), ("Average length", "____ pages (1.5&ndash;2.5 is healthy)"),
               ("Scenes with no turn", "____ &mdash; this number should be zero"),
               ("Longest scene", "page ____, ____ pages")],
        example="Enter late, leave early. If the scene&rsquo;s turn happens on page two of three, the "
                "third page is a goodbye that the cut will delete anyway.",
        gate=["Every row has a turn written in it.",
              "No scene exists only to deliver information.",
              "Every scene either advances the want or tightens the lie."],
    ),
    dict(
        stop="L/6", num="SHEET 15", title="The Script Builder", sub="FEATURE &middot; PAGE CRAFT",
        purpose="Standard format, and what goes inside it. Format is not decoration &mdash; it is the "
                "reason a page equals a minute, and a script that ignores it announces an amateur "
                "before the first line is read.",
        rule="Action in present tense, active voice, short paragraphs &mdash; three lines maximum. "
             "White space is pace: a dense page reads slow no matter what happens on it.",
        fields=[],
        scriptfmt=True,
        table=[("Font", "Courier 12pt &mdash; non-negotiable"),
               ("Page = ", "approx. 1 minute of screen time"),
               ("Action paragraphs", "1&ndash;3 lines"), ("Dialogue blocks", "rarely over 4 lines")],
        example=None,
        gate=["No camera directions unless you are also directing it.",
              "No unfilmable interiority &mdash; nothing the camera cannot see.",
              "Character names in dialogue are used sparingly; real people rarely say them."],
    ),
    dict(
        stop="L/7", num="SHEET 16", title="The Dialogue Pass", sub="FEATURE &middot; VOICE",
        purpose="A dedicated pass, done after the structure holds, never during. Dialogue written "
                "while the structure is still moving is dialogue you will delete.",
        rule="Characters should <b>not</b> say what they mean. The gap between what is said and what "
             "is wanted is where the audience does its work &mdash; and an audience doing work is an "
             "audience paying attention.",
        fields=[("Who speaks in short sentences, who runs long", 2),
                ("What each character never says", 2),
                ("The line you would cut last", 1)],
        table=[("Name-blind test", "cover the names &mdash; can you tell who is speaking?"),
               ("On-the-nose count", "lines that state the theme aloud: ____ (aim: 0)"),
               ("Longest speech", "page ____ &mdash; can it be halved?")],
        example="Run the name-blind test on ten random pages. If the answer is no, you have one "
                "character with several faces, and the fix is on Sheet 11, not here.",
        gate=["The name-blind test passes on a random sample.",
              "Nobody states the theme out loud.",
              "Every scene's most important line is the one nobody says."],
    ),
    dict(
        stop="L/8", num="SHEET 17", title="The Revision Passes", sub="FEATURE &middot; IN ORDER",
        purpose="Revise in named passes, one concern at a time. Trying to fix structure, voice and "
                "prose simultaneously is how drafts get worse while getting longer.",
        rule="One pass, one concern. Finish the pass before starting the next, and never fix a line "
             "during a structure pass &mdash; write it down and keep going.",
        fields=[],
        passes=True,
        table=[("Draft number", "____"), ("Date started / finished", "____ / ____"),
               ("Pages cut this draft", "____"), ("Rule", "every draft should get shorter")],
        example="If a draft comes back longer, you added rather than revised. The exception is a first "
                "revision of a skeletal draft &mdash; after that, down is the direction.",
        gate=["Each pass was run to completion before the next began.",
              "The page count went down.",
              "Someone who has not read a previous draft has now read this one."],
    ),
    dict(
        stop="L/9", num="SHEET 18", title="The Production Bible", sub="FEATURE &middot; HANDOFF",
        purpose="What the script implies but does not state: cast, locations, continuity, and &mdash; "
                "for a generated feature &mdash; the identity locks from Sheet 04 replicated for every "
                "character who appears more than once.",
        rule="For generated features, this sheet is the whole ballgame. A feature is fifty to a "
             "hundred times more generation than a short, which means fifty to a hundred times more "
             "opportunity for a face to drift.",
        fields=[("Locations, and what each one means", 3),
                ("Continuity risks &mdash; what will drift first", 3)],
        table=[("Speaking roles", "____"), ("Locations", "____"),
               ("Identity locks written", "____ / ____ characters"),
               ("Reference sets stored at", "&mdash;"),
               ("Estimated generations", "____"), ("Credit budget", "____")],
        example="Rank your continuity risks before you start, then generate the riskiest sequence "
                "first &mdash; not the easiest. You want to discover an unsolvable identity problem on "
                "day three, not day forty.",
        gate=["Every recurring character has an identity lock and a reference set.",
              "The riskiest sequence is scheduled first, not last.",
              "The credit budget has a number in it, and a reserve."],
    ),
]


# ── Sheet-specific grids ─────────────────────────────────────────────────────
def grid(headers, widths, rows=10, height=17, note=None):
    data = [[Paragraph(f'<font name="{SANS_B}" size="6.6" color="#7C7368">{caps(h)}</font>',
                       ST["small"]) for h in headers]]
    data += [[""] * len(headers) for _ in range(rows)]
    t = Table(data, colWidths=widths, rowHeights=[15] + [height] * rows)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("BACKGROUND", (0, 0), (-1, 0), FAINT),
        ("LINEBELOW", (0, 0), (-1, 0), 0.9, BRASS),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    out = [t]
    if note:
        out += [Spacer(1, 4), p(note, "small")]
    return out


W = PW - 2 * MARGIN


def beat_grid(full=False):
    return grid(["#", "Beat &mdash; what happens", "Job it does", "Sec"],
                [0.3 * inch, W - 0.3 * inch - 1.7 * inch - 0.5 * inch, 1.7 * inch, 0.5 * inch],
                rows=26 if full else 14, height=20 if full else 17,
                note="Sum the seconds column before you go further. The floor is 3:00 and it is measured "
                     "on the delivered file, not on your timeline.")


def ledger_grid(full=False):
    return grid(["Shot", "Beat", "Prompt / model / seed", "Carry", "Dur", "OK"],
                [0.45 * inch, 0.4 * inch, W - 3.55 * inch, 1.35 * inch, 0.45 * inch, 0.35 * inch],
                rows=22 if full else 13, height=24 if full else 18,
                note="Write the row, then spend the credit. Never the other way round &mdash; a shot "
                     "generated on impulse is a shot you cannot reproduce, and in a contest requiring "
                     "published prompts, cannot submit.")


def scene_grid(full=False):
    return grid(["#", "Slug (INT./EXT. &mdash; PLACE &mdash; TIME)", "Job", "The turn", "Pg"],
                [0.3 * inch, W - 0.3 * inch - 1.3 * inch - 1.5 * inch - 0.4 * inch,
                 1.3 * inch, 1.5 * inch, 0.4 * inch],
                rows=26 if full else 14, height=20 if full else 17,
                note="A scene with an empty turn column is a scene the edit will delete. Find it here, "
                     "where deleting it costs one line.")


def movement_grid(full=False):
    rows = [("I", "Setup &rarr; the door closes", "1 &ndash; 25", "The old life becomes impossible."),
            ("II-A", "Reaction &rarr; the midpoint", "25 &ndash; 55", "They respond, badly, and learn the rules."),
            ("II-B", "Action &rarr; all is lost", "55 &ndash; 85", "They act, and the lie costs them everything."),
            ("III", "Climax &rarr; the answer", "85 &ndash; 105", "The theme's question is answered in an image.")]
    data = [[Paragraph(f'<font name="{SANS_B}" size="6.6" color="#7C7368">{h}</font>', ST["small"])
             for h in ["MOVE", "WHAT IT DOES", "PAGES", "ENDS WHEN", "YOUR PAGES"]]]
    for a, b, c, d in rows:
        data.append([Paragraph(f'<font name="{SANS_B}" size="8.5">{a}</font>', ST["small"]),
                     Paragraph(b, ST["small"]), Paragraph(c, ST["small"]),
                     Paragraph(d, ST["small"]), ""])
    t = Table(data, colWidths=[0.55 * inch, 1.75 * inch, 0.8 * inch,
                               W - 0.55 * inch - 1.75 * inch - 0.8 * inch - 0.9 * inch, 0.9 * inch],
              rowHeights=[15] + [34] * 4)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("BACKGROUND", (0, 0), (-1, 0), FAINT),
        ("LINEBELOW", (0, 0), (-1, 0), 0.9, BRASS),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 1), (-1, -1), 5),
    ]))
    return [t]


def sequence_grid(full=False):
    return grid(["Seq", "Dramatic question", "Answer (yes-but / no-and)", "Pages"],
                [0.45 * inch, (W - 0.45 * inch - 0.7 * inch) * 0.44,
                 (W - 0.45 * inch - 0.7 * inch) * 0.56, 0.7 * inch],
                rows=8, height=26,
                note="A flat &lsquo;yes&rsquo; ends the story early. A flat &lsquo;no&rsquo; stops it dead. "
                     "<i>Yes but</i> and <i>no and</i> are the only two answers that generate the next sequence.")


def pass_list(full=False):
    passes = [
        ("1 &middot; STRUCTURE", "Does every sequence turn? Cut or merge. Do not touch a single line of dialogue."),
        ("2 &middot; CHARACTER", "Does each arc break its lie on the page you planned? Fix the ghost if not."),
        ("3 &middot; SCENE", "Enter late, leave early. Delete first and last lines of every scene, restore only what you miss."),
        ("4 &middot; DIALOGUE", "Name-blind test. Cut every line that states the theme."),
        ("5 &middot; ACTION", "Present tense, active voice, three lines maximum. Reclaim white space."),
        ("6 &middot; POLISH", "Typos, formatting, page count. Read it aloud, start to finish, in one sitting."),
    ]
    data = []
    for a, b in passes:
        data.append([Paragraph(f'<font name="{SANS_B}" size="7.4" color="#9A6F14">{a}</font>', ST["small"]),
                     Paragraph(b, ST["small"]), ""])
    t = Table(data, colWidths=[1.35 * inch, W - 1.35 * inch - 0.85 * inch, 0.85 * inch])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
    ]))
    return [Paragraph('<font name="Helvetica-Bold" size="6.8" color="#7C7368">'
                      'RUN IN ORDER &middot; TICK WHEN COMPLETE</font>', ST["small"]),
            Spacer(1, 4), t]


def script_format(full=False):
    sample = (
        "INT. LIGHTHOUSE - LANTERN ROOM - NIGHT\n"
        "\n"
        "Rain hammers the glass. MAREN, 60s, oilskin still\n"
        "dripping, cranks the mechanism by hand.\n"
        "\n"
        "The beam swings out. Catches something in the water\n"
        "that should not be there.\n"
        "\n"
        "                    MAREN\n"
        "          (not turning)\n"
        "     You're early.\n"
        "\n"
        "She keeps cranking.\n"
    )
    t = Table([[Paragraph(sample.replace("\n", "<br/>").replace(" ", "&nbsp;"), ST["mono"])]],
              colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    specs = [("Left margin", "1.5&Prime;"), ("Right margin", "1.0&Prime;"),
             ("Top / bottom", "1.0&Prime;"), ("Dialogue block", "2.5&Prime; from left"),
             ("Character name", "3.5&Prime; from left, caps"),
             ("Parenthetical", "3.0&Prime; from left"), ("Scene heading", "caps, at left margin"),
             ("Page numbers", "top right, from page 2")]
    half = (len(specs) + 1) // 2
    rows = []
    for i in range(half):
        left, right = specs[i], specs[i + half] if i + half < len(specs) else ("", "")
        rows.append([
            Paragraph(f'<font name="{SANS_B}" size="6.6" color="#7C7368">{caps(left[0])}</font>', ST["small"]),
            Paragraph(left[1], ST["small"]),
            Paragraph(f'<font name="{SANS_B}" size="6.6" color="#7C7368">{caps(right[0])}</font>', ST["small"]),
            Paragraph(right[1], ST["small"])])
    col = W / 2.0
    st = Table(rows, colWidths=[1.32 * inch, col - 1.32 * inch, 1.32 * inch, col - 1.32 * inch])
    st.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("TOPPADDING", (0, 0), (-1, -1), 3),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                            ("LEFTPADDING", (0, 0), (0, -1), 0),
                            ("LEFTPADDING", (2, 0), (2, -1), 8)]))
    return [h3("STANDARD FORMAT"), t, Spacer(1, 10), h3("MEASUREMENTS"), st]


# ── Assembly ─────────────────────────────────────────────────────────────────
# The three big ledgers get a page of their own. Inline, they push each sheet
# about ten percent past the page and leave a nearly-blank verso; given a full
# page they become what a workbook actually needs — room to write.
FULL_PAGE_GRIDS = {"beatgrid": beat_grid, "ledger": ledger_grid, "scenegrid": scene_grid}
INLINE_BLOCKS = {"movements": movement_grid, "sequences": sequence_grid,
                 "passes": pass_list, "scriptfmt": script_format}


def sheet_pages(s):
    out = [SheetHead(s["stop"], s["num"], s["title"], s["sub"]), Spacer(1, 10)]
    out += [p(s["purpose"], "lede"), Spacer(1, 9)]
    out += [panel("The rule", s["rule"]), Spacer(1, 11)]

    if s.get("fields"):
        out.append(h3("FILL THIS IN"))
        for label, n in s["fields"]:
            out += [Spacer(1, 2), Lines(n, label=label), Spacer(1, 5)]

    for key, fn in INLINE_BLOCKS.items():
        if s.get(key):
            out += [Spacer(1, 4)] + fn()

    # Headings travel with their content. Without this a sheet strands its
    # "WORKED EXAMPLE" label at the foot of one page and the example on the next.
    if s.get("table"):
        out += [Spacer(1, 10),
                KeepTogether([h3("AT A GLANCE"), field_table(s["table"])])]

    if s.get("example"):
        out += [Spacer(1, 10),
                KeepTogether([h3("WORKED EXAMPLE"), p(s["example"], "ex")])]

    # Sheets whose ledger moved to its own page have room left over on the
    # teaching page. Ruled notes beat white space in a workbook. This must sit
    # BEFORE the gate and the page break, or it lands on the worksheet page and
    # shoves the grid over the fold.
    if any(s.get(k) for k in FULL_PAGE_GRIDS):
        out += [Spacer(1, 12), Lines(8, label="Notes, false starts, things to try")]

    out += [Spacer(1, 11),
            KeepTogether([Paragraph(
                f'<font name="{SANS_B}" size="7" color="#9A6F14">'
                f'DO NOT STOP DOWN FURTHER UNTIL</font>', ST["small"]),
                Spacer(1, 6), Boxes(s["gate"])]),
            PageBreak()]

    for key, fn in FULL_PAGE_GRIDS.items():
        if s.get(key):
            out += [Paragraph(
                f'<font name="{SANS_B}" size="7" color="#9A6F14">{caps(s["stop"])} '
                f'&nbsp;&middot;&nbsp; {caps(s["title"])}</font>', ST["small"]),
                Spacer(1, 3),
                Paragraph(f'<font name="{SERIF_B}" size="13">Worksheet</font>', ST["small"]),
                Spacer(1, 9), Rule(color=BRASS, thickness=1.1), Spacer(1, 12)]
            out += fn(full=True)
            out += [PageBreak()]
    return out


def cover():
    return [
        Spacer(1, 1.5 * inch),
        Paragraph('<font name="Helvetica-Bold" size="8" color="#9A6F14">'
                  'A DEVELOPMENT HANDBOOK &nbsp;&middot;&nbsp; EIGHTEEN SHEETS, IN ORDER</font>',
                  ST["cover_s"]),
        Spacer(1, 22),
        Paragraph("The Aperture<br/>Method", ST["cover_t"]),
        Spacer(1, 16),
        Rule(w=2.1 * inch, color=BRASS, thickness=1.3, center=True),
        Spacer(1, 20),
        Paragraph("<i>A snowflake grows outward from a seed. An aperture stops down &mdash; "
                  "each stop admits less, and the image gets sharper.</i>",
                  S("x", fontName=SERIF_I, fontSize=12.5, leading=18, alignment=TA_CENTER,
                    textColor=colors.HexColor("#3A342B"))),
        Spacer(1, 1.5 * inch),
        Paragraph("PART I &nbsp;&middot;&nbsp; NINE STOPS FOR A GENERATED SHORT<br/>"
                  "PART II &nbsp;&middot;&nbsp; THE LONG APERTURE &mdash; FEATURE PLANNER &amp; SCRIPT BUILDER",
                  ST["cover_s"]),
        Spacer(1, 1.2 * inch),
        Paragraph('<font name="Helvetica" size="7.4" color="#7C7368">'
                  'THE VOID ROOM &nbsp;&middot;&nbsp; PRINT DOUBLE-SIDED, WRITE ON IT</font>',
                  ST["cover_s"]),
        PageBreak(),
    ]


def how_to_use():
    return [
        Paragraph("Why this is not the Snowflake", ST["h2"]),
        Rule(color=BRASS, thickness=1.1), Spacer(1, 12),
        p("The Snowflake Method expands. One sentence becomes a paragraph, becomes a synopsis, "
          "becomes a draft &mdash; each step growing outward from the one before. That works because "
          "prose revises at zero marginal cost. You can rewrite chapter nine forty times and the only "
          "price is your afternoon.", "lede"),
        Spacer(1, 9),
        p("Generated film does not behave that way. You cannot revise a shot &mdash; you can only "
          "re-roll it, paying credits each time, with no guarantee the new roll matches the take you "
          "already cut around. The expensive failure mode is not bad writing. It is <b>drift</b>: the "
          "face that changes between shots, the palette that wanders, the light that comes from "
          "nowhere in particular."),
        Spacer(1, 9),
        p("So this method inverts the shape. It does not expand &mdash; it <b>narrows</b>. Each sheet "
          "removes freedom, and the sheets are ordered by cost-of-change: whatever is most expensive "
          "to fix after generation begins gets locked first. By the time you spend a credit, every "
          "decision the model could get wrong has already been made by you."),
        Spacer(1, 14),
        panel("The one rule that governs the whole handbook",
              "Do not stop down further until the gate at the foot of the current sheet is clear. "
              "Every sheet ends in a checklist. Those are not suggestions &mdash; they are the "
              "mechanism. Skipping one does not save time, it moves the cost to the most expensive "
              "possible moment."),
        Spacer(1, 16),
        h3("HOW TO USE IT"),
        Boxes(["Print double-sided. This is a workbook &mdash; the blanks are the point.",
               "Work the sheets in order. The order is the method; the sheets alone are just forms.",
               "One project per copy. Do not reuse a filled sheet for a second film.",
               "Part II stands alone &mdash; a feature planner and script builder, same philosophy, longer form.",
               "Sheets 04, 05 and 06 are the ones that pay for themselves. If you skip anything, do not skip those."]),
        PageBreak(),
        Paragraph("All eighteen sheets, in order", ST["h2"]),
        Rule(color=BRASS, thickness=1.1),
        Spacer(1, 10),
        Spacer(1, 3),
        contents_table(),
        PageBreak(),
    ]


def contents_table():
    rows = [(s["stop"], s["title"], s["sub"].replace("LOCKS: ", "").replace("FEATURE &middot; ", ""))
            for s in SHEETS_SHORT]
    rows.append(("", "", ""))
    rows += [(s["stop"], s["title"], s["sub"].replace("FEATURE &middot; LOCKS: ", "")
              .replace("FEATURE &middot; ", "")) for s in SHEETS_FEATURE]
    data = []
    for a, b, c in rows:
        if not a:
            data.append(["", Paragraph('<font name="Helvetica-Bold" size="6.8" color="#9A6F14">'
                                       'PART II &middot; THE LONG APERTURE</font>', ST["small"]), ""])
            continue
        data.append([Paragraph(f'<font name="{SANS_B}" size="7.6" color="#9A6F14">{a}</font>', ST["small"]),
                     Paragraph(f'<font name="{SERIF_B}" size="9.6">{b}</font>', ST["small"]),
                     Paragraph(f'<font name="{SANS}" size="7" color="#7C7368">{c}</font>', ST["small"])])
    t = Table(data, colWidths=[0.62 * inch, 1.85 * inch, W - 2.47 * inch])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.35, RULE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
    ]))
    return t


def part_title(num, title, blurb):
    return [Spacer(1, 2.3 * inch),
            Paragraph(num, ST["part_n"]), Spacer(1, 10),
            Paragraph(title, ST["part_t"]), Spacer(1, 16),
            Rule(w=1.5 * inch, color=BRASS, thickness=1.1, center=True), Spacer(1, 18),
            Paragraph(blurb, S("pb", fontName=SERIF_I, fontSize=11.5, leading=17,
                               alignment=TA_CENTER, textColor=colors.HexColor("#3A342B"))),
            PageBreak()]


def back_matter():
    return [
        Paragraph("The two running sheets", ST["h2"]),
        Rule(color=BRASS, thickness=1.1), Spacer(1, 12),
        p("These are not stops. They run alongside every sheet, from the first to the last.", "lede"),
        Spacer(1, 16),
        h3("THE DRIFT LOG"),
        p("Every time a generated element fails to match its lock, log it. The pattern in this column "
          "tells you what to hide, what to re-frame, and what to stop attempting &mdash; and it is the "
          "single most useful document you will own by the end of production."),
        Spacer(1, 7),
    ] + grid(["Shot", "What drifted", "Against which lock", "Fix applied", "Cost"],
             [0.5 * inch, (W - 1.3 * inch) * 0.3, (W - 1.3 * inch) * 0.25,
              (W - 1.3 * inch) * 0.45, 0.8 * inch], rows=10, height=18) + [
        Spacer(1, 20),
        h3("THE COMPLIANCE GATE"),
        p("Run before every publication, not once at the end. A disqualified film is worth zero "
          "regardless of its quality, which makes this the highest-leverage checklist in the handbook "
          "and the one most likely to be skipped."),
        Spacer(1, 8),
        Boxes(["No copyrighted characters, IP, or brand logos in any frame.",
               "No licensed music. Original composition or royalty-free only, licence held and filed.",
               "No NSFW content.",
               "No political statement &mdash; in the film, the title, or the caption.",
               "No religious statement &mdash; same three places.",
               "Runtime clears the floor, measured on the delivered file.",
               "Required watermark present on the delivered file.",
               "Prompts and generation history published where required.",
               "Team size, ages, and account status all within the rules."]),
        Spacer(1, 22),
        Rule(color=RULE), Spacer(1, 12),
        Paragraph("<i>None of the films worth studying won on render quality. Every one of them won "
                  "on a decision &mdash; and every decision in this handbook is one you make before "
                  "the machine gets a vote.</i>",
                  S("end", fontName=SERIF_I, fontSize=10.5, leading=16, alignment=TA_CENTER,
                    textColor=MUTED)),
    ]


def main():
    story = []
    story += cover()
    story += how_to_use()
    story += part_title(
        "PART I",
        "Nine Stops",
        "A three-to-five minute generated short.<br/>Wide open at f/1.4, everything still possible.<br/>"
        "Stopped down to f/22, nothing left to chance.")
    for s in SHEETS_SHORT:
        story += sheet_pages(s)
    story += part_title(
        "PART II",
        "The Long Aperture",
        "A feature planner and script builder.<br/>Same philosophy, ninety times the runtime &mdash;<br/>"
        "which is ninety times the opportunity to drift.")
    for s in SHEETS_FEATURE:
        story += sheet_pages(s)
    story += back_matter()
    build(story)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
