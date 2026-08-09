# Contest Brief — Higgsfield Global Film Festival (Aug 2026)

**Prepared for:** DarkHearts Ltd. / DarkHearts Short Film Studios
**Prepared:** 2026-08-08
**Status:** Deadline is **23 days out.** This is a sprint, not a season.

---

## 1. The Hard Facts

| Item | Value | Confidence |
|---|---|---|
| Prize pool | **$1,000,000** across **14 winners** | Confirmed (official email) |
| 1st place | $500,000 | Confirmed |
| 2nd place | $200,000 | Confirmed |
| 3rd place | $100,000 | Confirmed |
| **Audience Choice** | **$100,000** | Confirmed |
| Honorable Mentions | 10 × $10,000 | Confirmed |
| Submissions open | August 7, 2026 | Confirmed |
| **Submissions close** | **August 31, 2026 — 11:59 PM PT** | High (trade press, consistent) |
| Winners announced | Late September / early October 2026 | Medium |
| Eligibility | Worldwide, 18+, **active Higgsfield subscription** | Confirmed |
| Team size | Solo or team of **up to 4** | Confirmed |
| Entries per entrant | **Unlimited** — each must be a standalone film | Medium-high |
| **Prizes per entrant** | **One.** Higher placement wins; the other slot cascades | Medium-high |
| Disqualifiers | Copyrighted IP, licensed music, NSFW, **political statements**, **religious statements** | Medium-high |
| Runtime | **3 min minimum**, 3–5 min recommended | Medium-high |
| Watermark | Official Higgsfield watermark **required** on every upload | Medium-high |
| Submission mechanic | **Public post** on the platform, not a private form | Medium-high |
| Judging stages | Screening → Shortlist → Jury verdict | Medium |
| Post-deadline | **All submissions go public** — prompts, assets, generation history | High |

> **Sourcing note.** `higgsfield.ai` is blocked by this environment's network egress proxy, so I could not read the rules page directly. Everything above is drawn from the official festival email in your inbox (Aug 5) plus trade coverage. **Section 6 lists the five things you must personally verify on the rules page before you generate a single frame.**

---

## 2. The Scoring Rubric — and Why It Changes Everything

Five weighted criteria:

| Criterion | Weight |
|---|---|
| Cinematic Quality | **25%** |
| Storytelling & Creativity | **25%** |
| Technical Execution | **20%** |
| Platform Engagement | **15%** |
| Social Media Engagement | **15%** |

**Read that bottom third again. 30% of your score is not in the film.**

This is the single most exploitable fact about this contest. Most entrants will treat the film as the whole deliverable, upload it on Aug 30, and lose thirty points before a juror opens it. The correct model is:

> **70% film + 30% campaign, and the campaign has to start the day the first frame renders — not the day you submit.**

Practical consequences, baked into `docs/08-production-plan.md`:
- Every film needs a **6–15 second standalone hook clip** that works with sound off on X / IG / TikTok. Design the shot for this on purpose; don't harvest it later.
- Build in public. Post the process daily. The open-sourcing is mandatory anyway — turn a compliance burden into 15% of your score.
- Your project page is a scored artifact. A generously documented, browsable project earns Platform Engagement. A dumped folder does not.

---

## 3. The Jury — Read Them Precisely

Three names on the festival page. They do not want the same film, and that tension *is* the design brief.

### Ed Catmull — Pixar co-founder, ex-President of Walt Disney Animation, 5 Oscars, Turing Award
The most famous "story is king" evangelist alive, and the author of *Creativity, Inc.* — a book largely about **honest process and iteration**, not talent.

- **Rewards:** emotional truth, a character who wants something and changes, clarity, restraint. A simple story told with total precision beats a complex one told loosely. He is also a genuine technologist and will respect real invention *in service of story*.
- **Punishes:** spectacle with no one inside it. Vibes. Trailers. A film that is a demo reel wearing a story costume.
- **Test:** *Can you say what the character wants in one sentence, and did they change by the end?*

### Phedon Papamichael, ASC — DP: *Nebraska*, *Ford v Ferrari*, *Walk the Line*, *The Descendants*, *3:10 to Yuma*, *The Trial of the Chicago 7*
A naturalist. *Nebraska* is black-and-white and mostly available light. *Ford v Ferrari* is practical night racing. He does not shoot pretty; he shoots **motivated**.

- **Rewards:** a single consistent lens language; one dominant light source per scene with a visible reason for existing; real grain; restrained color; faces held long enough to read; landscape given room.
- **Punishes:** everything AI video defaults to. Ambient over-lighting from nowhere. Teal-and-orange. Plastic skin. Floaty, unmotivated camera drift. Focal length that changes every shot. Over-saturation.
- **Test:** *Where is the light coming from, and could you point at it?*

### Paul W. S. Anderson — *Resident Evil*, *Mortal Kombat*, *Event Horizon*, *Death Race*, *Monster Hunter*, *Pompeii*
Genre. Propulsion. Hooks. He has built a career on high-concept premises and maximalist production design.

- **Rewards:** a hook you can pitch in one line. One unforgettable set piece. Kinetic energy. Scale that *feels* physical. Cool, unapologetically.
- **Punishes:** four minutes of moody nothing. An art film with no engine.
- **Test:** *What's the poster, and what's the one shot people will screenshot?*

### The Triangulation — This Is the Whole Thesis

> **An emotionally true, simple human story (Catmull), photographed with disciplined naturalistic light and a consistent lens (Papamichael), inside a high-concept genre wrapper with exactly one unforgettable set piece (Anderson).**

Nearly every entrant will nail one and fail two:
- Spectacle reel → dies on Catmull.
- Moody AI art film → dies on Anderson.
- Fake-trailer for an imaginary blockbuster → dies on all three, and it will be *the single most common submission in this contest.*

Hit all three and you are competing against a very small field.

---

## 4. Production Intelligence from *Hell Grind*

Higgsfield open-sourced their 95-minute feature. The numbers are the useful part:

- **253 clips selected from 16,181 generations** — a ~1.6% keep rate, by a funded team.
- **~3,000 words average per prompt**, used to hold shot-to-shot consistency.
- 14 days, ~$500K, **80% of budget on GPU**.
- Also open-sourced: *Zephyr* and *Mork*, with full breakdowns.

**What this means for you.** A 4-minute film is roughly 50–60 shots. Even at a generous 10–15% keep rate for a skilled solo operator with tight references, that is **400–700 generations**. Budget credits and calendar accordingly — and design the film so that the hard shots are few and the repeatable shots are many. (Every concept in this package is engineered around that constraint; see the "Producibility" line on each.)

**Also:** go read the *Hell Grind* breakdown before you write a single prompt. Their 3,000-word prompt structure is free R&D and the jury knows the reference.

---

## 5. Strategic Gotchas

**1. Unlimited entries — but only one prize per entrant.**
You may submit as many standalone films as you like, and a slate is still worth running: two films means two chances at landing in the fourteen, and the probability of at least one placing is higher than either alone. But **the prizes do not stack** — if two of your films place, you take the higher one and the other cascades to someone else. So the second film has to cost you very little, and it must never come out of the flagship's quality. See the revised portfolio logic in `docs/05-slate-b-contenders.md`.

**1a. Ten of the fourteen prizes are $10,000 Honorable Mentions.**
71% of the winning slots are HMs. The realistic target is *landing in the fourteen*, not winning outright. Design for that; let the top three be upside.

**1b. The disqualifier list is stricter than most entrants expect.**
No copyrighted IP (characters, logos, trademarks), no licensed music, no NSFW, **no political statements, and no religious statements.** Serious violations can mean a permanent ban. The religious clause is a live risk for the DarkHearts esoterica material — Enoch, Goetia and Hekhalot sit right on that line. A myth is fine; a theological argument is a removal. Full list in `docs/09-one-pager.md`.

**2. Audience Choice ($100,000) is a separate, winnable game.**
It is very likely popularity-driven, and it pays the same as third place. A wordless, universal, high-shareability short is a completely different optimization from a jury film — and it is the cheapest film in this package to produce.

**3. Open-sourcing is not a tax, it is a channel.**
Your files go public after the deadline regardless. The entrants who treat that as a documentation project — clean prompt cards, annotated shot lists, a readable methodology — will collect Platform Engagement points that the entrants who dump a folder will not.

**4. "Made entirely in Higgsfield" is the highest-stakes ambiguity.**
The official email says the film must be "made entirely in Higgsfield." Third-party coverage says the published rules don't spell out a tool-exclusivity clause beyond the subscription requirement, and that any model is allowed. **These are not the same claim.** Resolve it yourself — see §6. It directly determines whether your score can be composed in your own DAW or must be generated on-platform.

**5. The 3-minute floor is a real disqualifier.**
Target **4:10–4:40** including titles and end card. Long enough to be unambiguously safe, short enough that a juror on submission #300 doesn't check out.

---

## 6. Verify These Five Things Yourself — Before Any Production

I could not reach the rules page from this environment. These five answers change the plan:

1. **Music.** Can the score be composed off-platform in your DAW and married in edit, or must audio be generated in Higgsfield? *(This determines whether DarkHearts scores it live or you build the metal/EDM bed with on-platform audio generation. Both paths are written in `docs/07-score-and-sound.md`.)*
2. **External editing.** Confirmed you may cut in external software but may not *create new content* there. Does that permit grade, grain, sound mix, and titles? Assume yes; verify.
3. **Exact runtime bounds.** Min 3:00 confirmed-ish. Is there a hard max? Does it include credits?
4. **Delivery spec.** Resolution, aspect ratio, frame rate, codec, and whether the Higgsfield watermark must be visible on the final export or is applied by the platform.
5. **Entry cap and eligibility window.** Confirm entries are genuinely unlimited. *(Subscription is settled — the account is on Ultra; see `docs/10-tiers-and-pipeline.md`.)*
6. **Does the one-prize-per-entrant cap include Audience Choice,** or does Audience Choice sit outside the jury placements? **This is the one that decides whether a second film is upside or insurance.**

Log the answers at the top of `docs/08-production-plan.md` before Day 1.

---

## 7. Calendar

```
AUG  8  ── Today. Rules verified. Concept locked. (This document.)
AUG  9–11  Snowflake to Step 8. Screenplay locked. No production.
AUG 12–14  Look dev: character sheet, lens/light bible, 6 test shots.
AUG 15–23  Principal generation. Daily build-in-public posts.
AUG 24–26  Assembly, score, mix, grade.
AUG 27–28  Buffer. (This buffer will be used. It always is.)
AUG 29     Submit. Publish project files. Launch hook clip.
AUG 30–31  Campaign push. Reserve for a second entry.
AUG 31     11:59 PM PT — HARD CLOSE.
```

**Submit on the 29th, not the 31st.** Platform Engagement needs runway, and every contest server on earth falls over in the last six hours.
