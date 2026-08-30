# 00 — Contest Brief & Hard Constraints

> Compiled 2026-08-10. The official page (`higgsfield.ai/contests/higgsfield-global-film-festival`)
> is blocked by this environment's network egress proxy, so everything below is reconstructed from
> Higgsfield's own announcement posts and secondary coverage. **Every item marked ⚠️ must be
> verified against the official rules page before you commit production time.**

---

## The clock — this is the headline

| Milestone | Date | Days from 2026-08-10 |
|---|---|---|
| Competition opens | **August 10, 2026** | today |
| **Submission deadline** | **September 3, 2026** | **24 days** |
| Shortlist announced | September 24, 2026 | +45 |
| Jury review window | September 25 – October 1, 2026 | +46 to +52 |
| Winners announced | First week of October 2026 | ~+55 |

**24 days.** Not 24 days to "start" — 24 days to a finished, graded, mixed, 4–5 minute film.
Every recommendation in these documents is shaped by that number. See
[`07-PRODUCTION-SCHEDULE.md`](07-PRODUCTION-SCHEDULE.md) for the day-by-day working-back plan.

Note the timeline was revised — Higgsfield pushed the open date to August 10. ⚠️ Watch their
X/Twitter account for further slips *in both directions*; a deadline that moves earlier would be
fatal to a plan built to the wire.

---

## Prize structure — 14 winners, $1,000,000

| Placement | Prize |
|---|---|
| 1st | **$500,000** |
| 2nd | **$200,000** |
| 3rd | **$100,000** |
| Audience Choice | **$100,000** |
| Honorable Mentions ×10 | **$10,000** each |

Two strategic reads fall out of this table:

1. **The distribution is brutally top-heavy.** 80% of the money sits in the top three. Designing
   for "safe honorable mention" is a bad trade — an HM is 1% of the top prize. Design for the
   podium and let HM be the floor, not the target.
2. **Audience Choice is a genuinely separate $100k with a different judging function.** It is not
   decided by Catmull, Papamichael and Anderson — it is decided by a crowd. That means there are
   *two different games* on one board, and they reward different things (jury: restraint,
   craft, story; crowd: hook, shareability, first-15-seconds). A film can be built to compete
   in both, but the tensions are real and must be resolved deliberately rather than by accident.
   See [`06-WARGAME.md`](06-WARGAME.md) § The Two-Games Problem.

---

## Eligibility & entry rules

| Rule | Value | Confidence |
|---|---|---|
| Age | 18+ | reported |
| Geography | Worldwide | reported |
| Subscription | Active Higgsfield subscription required | reported |
| Team size | Solo or teams up to **4** | reported |
| **Minimum length** | **3 minutes** | reported |
| Maximum length | ⚠️ **Not confirmed anywhere in available sources** | **UNKNOWN** |
| Submission route | Must be created through the **festival project in Cinema Studio** | reported |
| Entries per person | ⚠️ Unconfirmed | **UNKNOWN** |
| Aspect ratio / resolution | ⚠️ Unconfirmed | **UNKNOWN** |
| Music/audio licensing | ⚠️ Unconfirmed | **UNKNOWN** |
| Rights granted to Higgsfield | ⚠️ Unconfirmed | **UNKNOWN** |

### The four unknowns that could actually change the plan

These are worth ten minutes of your time on the official page before you write a single prompt:

1. **Is there a maximum runtime?** Your 4–5 minute target sits comfortably above the 3-minute
   floor. If there is a 5-minute ceiling, aim for 4:30 and stop worrying. If the ceiling is
   lower than you think, you lose a scene. *This is the single highest-value unknown.*
2. **"Created through the festival project in Cinema Studio" — how strictly is that enforced?**
   This is the make-or-break technical constraint. If it means *every frame* must be generated
   inside the Cinema Studio festival project, then models reached via other surfaces
   (FLUX 3 Video's 20-second ceiling, Wan 3.0's 30-second ceiling) may be **out of bounds** —
   and those are precisely the models that make your long-take aesthetic mechanically possible.
   If it means the *project must exist* there and assembly happens there, you have far more
   freedom. **Everything in [`03-HIGGSFIELD-PLAYBOOK.md`](03-HIGGSFIELD-PLAYBOOK.md) § Model
   routing is contingent on this answer.** Resolve it first.
3. **Can you submit more than one film?** Changes portfolio strategy entirely — one perfect
   swing versus two differentiated ones (e.g. one jury-optimised, one audience-optimised).
4. **What rights do you grant?** A $500k prize is worth a broad license. A $10k honorable
   mention may not be. Read before you sign.

---

## What Higgsfield open-sourced alongside the contest — and why it matters

Higgsfield released the complete production packages for three of their own films:

- **Hell Grind** — a 95-minute AI feature, made in 14 days for ~$500k, screened at the Cannes
  Market, covered by WSJ / Variety / BBC. Every prompt, character model, asset and workflow is public.
- **Zephyr** — a viral K-pop action series.
- **Mork**.

This is not a courtesy. It is a **published grading rubric**. Higgsfield has told you, in
extraordinary detail, what they consider good. The Hell Grind methodology — 3,000–4,000-word
prompts, GEO SPATIAL LAYOUT blocks, headless character sheets, the one-second opening wide — is
distilled into [`03-HIGGSFIELD-PLAYBOOK.md`](03-HIGGSFIELD-PLAYBOOK.md).

**Strategic caution, and it cuts against the obvious move:** if the open-sourced films are the
rubric, thousands of entrants will also read them, and the shortlist will be full of films that
look like Hell Grind — dark, kinetic, action-forward. *Use their technical discipline; do not
adopt their aesthetic.* The differentiation opportunity is to apply feature-grade rigor to
material Hell Grind is not: quiet, human, photographed. That is also, not coincidentally,
exactly what this jury is built to reward. See [`01-JUDGES-DOSSIER.md`](01-JUDGES-DOSSIER.md).

---

## Scale of the field — what you are actually up against

Higgsfield's *previous* competition (results announced March 18, 2026) drew **~8,800 submissions
from 139 countries** against a $500,000 pool. This one has double the money, Academy-Award-level
jury names, and a month of promotion behind it.

**Plan for 10,000–20,000 entries.** Two consequences:

- **The shortlist filter is not the jury.** Catmull, Papamichael and Anderson review a
  *shortlist* (Sept 25 – Oct 1). Something else — staff, community voting, or an internal
  panel — cuts ~15,000 films down to a reviewable number first. Your film has to survive a
  fast, tired, high-volume triage pass *before* it ever reaches the people you are designing for.
- **Therefore: the first 20 seconds are a separate engineering problem from the film.** They
  must survive triage without cheapening the film for the jury. This is a real design tension
  and it is addressed head-on in [`02-DIRECTING-DOCTRINE.md`](02-DIRECTING-DOCTRINE.md)
  § The Cold Open Problem.

---

## Submission checklist (fill in as verified)

- [ ] ⚠️ Official rules page read end-to-end; every UNKNOWN above resolved
- [ ] Active Higgsfield subscription confirmed, with enough credit headroom (see
      [`07-PRODUCTION-SCHEDULE.md`](07-PRODUCTION-SCHEDULE.md) § Credit budget)
- [ ] Festival project created in Cinema Studio
- [ ] Runtime ≥ 3:00 (target 4:00–4:45) and ≤ any confirmed maximum
- [ ] Title, logline and any required metadata prepared
- [ ] Music cleared / original / diegetic-only per rules
- [ ] Final master exported at the required spec
- [ ] Submitted **≥ 48 hours before the deadline** — never on the last day; platform load at a
      $1M deadline is a predictable failure mode
- [ ] Social cut prepared for the Audience Choice campaign (if pursuing it)

---

## Sources

- [Higgsfield AI — revised timeline announcement (X)](https://x.com/higgsfield_ai/status/2085853524878078290)
- [Higgsfield AI — festival announcement (X)](https://x.com/higgsfield_ai/status/2084359051627131074)
- [Higgsfield Global Film Festival — official contest page](https://higgsfield.ai/contests/higgsfield-global-film-festival) (egress-blocked here)
- [AI Video Sensei — how to actually enter](https://aivideosensei.com/guides/higgsfield-global-film-festival-guide)
- [Hollywood.AI — festival guide](https://hollywood.ai/awards/higgsfield-global-film-festival)
- [RuntimeWire — $1M contest with public project files](https://runtimewire.com/article/higgsfield-1-million-ai-film-festival-public-prompts)
- [PRNewswire — largest AI film competition, trends (prior contest, 8,800 entries)](https://www.prnewswire.com/news-releases/the-largest-ai-film-competition-highlights-emerging-trends-in-global-ai-filmmaking-302717810.html)
- [TechappleGlobal — Hell Grind open-sourced](https://global.techapple.com/2026/08/higgsfield-open-sources-entire-production-of-95-minute-ai-film-hell-grind-made-in-14-days-for-500k/)
