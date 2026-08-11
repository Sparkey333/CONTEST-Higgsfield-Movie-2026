# The Scoring Model — How We Actually Win

> ⚠️ `[VERIFY]` — the weights below are sourced indirectly (`higgsfield.ai` is
> egress-blocked here). They are the most load-bearing facts in our entire strategy.
> Confirm against the live page at the first opportunity.

---

## 1. The rubric

| # | Criterion | Weight | Contested by | Our leverage |
|---|---|---|---|---|
| 1 | Cinematic Quality | 25% | Everyone | Medium |
| 2 | Storytelling & Creativity | 25% | Everyone | Medium |
| 3 | Technical Execution | 20% | Most | Medium-high |
| 4 | **Platform Engagement** | **15%** | **Almost nobody** | **Very high** |
| 5 | **Social Media Engagement** | **15%** | **Almost nobody** | **Very high** |

---

## 2. The central insight

**30% of the score is engagement, and engagement is the only criterion where effort
converts to points almost linearly.**

Cinematic Quality and Storytelling are contested by thousands of gifted filmmakers,
and returns there are brutally non-linear — going from good to great might move you
from the 80th to the 90th percentile. But **most filmmakers post their film once and
hope.** They treat the public post as paperwork.

It is not paperwork. It is 30% of the rubric and a separate **$100,000 Audience
Choice prize**.

> **A merely very good film with a disciplined 23-day campaign will beat an
> outstanding film posted cold on August 31.**

That is the thesis. Everything in `docs/03-production-plan.md` follows from it.

---

## 3. Criterion-by-criterion attack

### Cinematic Quality — 25% · owner: Phedon, with Edwin
Judged by **Phedon Papamichael**, a working cinematographer. He reads:
- **Motivated light.** Where is the source? Does it stay on the same side between
  shots? Inconsistent light direction is the fastest way to look amateur.
- **Lens language.** Focal length as emotion — wide for isolation, long for
  compression and dread. Consistency of lens grammar across a sequence.
- **Blocking and eyelines.** Screen direction that holds. Characters who occupy real
  space rather than floating in a render.
- **Color.** One coherent palette with a deliberate shift at the turn.

**Attack:** build a continuity bible before production. Pick a lens grammar and a
palette and *hold them*. Consistency reads as intent; intent reads as craft.

### Storytelling & Creativity — 25% · owner: Edwin
Judged by **Edwin Catmull**, whose entire career rests on *story is king*.
- One idea, one feeling, one turn. A 3–5 minute film cannot hold more.
- Setup and payoff must close. The ending must be **earned by the opening**.
- A character we care about within 30 seconds.
- Originality — Braintrust's job is to keep us off the crowded paths (dystopian cityscape,
  lone samurai, sad robot, cosmic-horror voiceover, neon cyberpunk chase).

**Attack:** wordless or near-wordless emotional storytelling. It is the Pixar house
style Catmull built, and it sidesteps the lip-sync and vocal-performance seams where
AI film looks worst. *Piper*, *Paperman*, and the opening of *Up* are the register.

### Technical Execution — 20% · owner: Catmull, with Phedon
This is where AI film is *actually* judged as AI film.
- **Character consistency across shots** — the #1 amateur tell.
- Temporal stability: no flicker, no morphing hands, no warping backgrounds.
- Clean cuts, correct resolution, professional finishing.
- **Published prompts and generation history.** This is *mandatory*, and it is
  visible. A clean, legible, well-organized prompt trail is a scored artifact. Most
  entrants will dump a messy log. We will publish a *document*.

**Attack:** treat the required prompt publication as a deliverable, not a chore. It
directly feeds this 20%, and Anderson can turn it into campaign content.

### Platform Engagement — 15% · owner: Anderson
Engagement **on Higgsfield itself**: the public post, views, likes, comments, shares,
community response within the platform.

**Attack:** post the *process* from now to Aug 31, not just the film on Aug 31. Build
an audience on-platform before the film exists so the launch lands on a warm crowd.

### Social Media Engagement — 15% · owner: Anderson
X, YouTube, Instagram, TikTok.

**Attack:** the behind-the-scenes breakdown often outperforms the film itself —
Higgsfield proved this with the 19-minute Hell Grind tutorial. We are *required* to
publish prompts anyway. Turn the obligation into the campaign. Run
`virality_predictor` on the hook and the final cut before committing.

---

## 4. The three-stage funnel

```
ALL ENTRIES ──► SCREENING ──► SHORTLIST ──► JURY VERDICT
              (most die here)
```

**Screening is a filter, not a ranking.** It asks *"is this disqualified, broken, or
boring in the first 30 seconds?"* — not *"is this the best film?"*

Two separate jobs, in this order:
1. **Survive Screening.** Compliance perfect. Runtime ≥3:00. Watermark present.
   Prompts published. Public post live. **And a first 15 seconds that stops a tired
   reviewer on entry #400.** This is Edwin's hook, and at Screening it matters more
   than anything in the middle of the film.
2. **Win the Jury.** Now craft, story, and sound decide it.

Optimizing for (2) while failing (1) is the most common way a genuinely good film
loses this kind of contest.

---

## 5. Structural exploits

### A. Unlimited entries
Entries are **unlimited**; each must be a standalone film. With **14 prizes**,
including **ten Honorable Mentions at $10,000**, a portfolio approach has real
expected value. Almost nobody will do this.

**Recommendation:** one **primary** film with everything behind it, plus **1–2
secondary** entries built from surplus assets and a different tonal register. Do not
let secondaries cannibalize the primary. Braintrust owns this call and revisits it as the
calendar tightens.

### B. Two independent money paths
The jury path and the **Audience Choice ($100,000)** path are separate. A film can
lose the jury and still take $100K on reach alone. This makes Anderson's 30% doubly
valuable — it scores *and* it competes for a separate six-figure prize.

### C. The concurrent $500K contest
**Make Your Action Scene** — $500K in prizes, **same Aug 31 11:59 PM PT deadline**.
If our film contains a strong action sequence, that sequence may be separately
submittable. `[VERIFY]` cross-entry rules with Catmull before relying on this.

### D. The published answer key
**Hell Grind** (95-min, $500K, Cannes Market, WSJ/Variety/BBC coverage), **Zephyr**,
and **Mork** are fully open-sourced — prompts, seeds, raw generation files, shot
lists, complete workflow — plus a 19-minute breakdown. Higgsfield published what *it*
considers award-grade. Braintrust mines this first.

---

## 6. Scoreboard model

Rough self-assessment target before we submit. Score each 1–10, weight, and sum.

| Criterion | Weight | Target | Owner |
|---|---|---|---|
| Cinematic Quality | 25% | ≥8 | Phedon |
| Storytelling & Creativity | 25% | ≥9 | Edwin |
| Technical Execution | 20% | ≥8 | Catmull |
| Platform Engagement | 15% | ≥9 | Anderson |
| Social Media Engagement | 15% | ≥9 | Anderson |

**If the weighted total is below 8.0 at the rough-cut gate, we have a problem Braintrust
must escalate — not a polish pass.**
