# The Snowflake Method, Adapted for a 4-Minute Film

Randy Ingermanson's Snowflake Method was built for novels: ten steps of controlled fractal expansion, each one refining the last rather than replacing it. The premise is that a story should be *grown* from a seed at a constant level of internal consistency, never assembled from parts.

That premise survives the jump to short film intact. The step definitions do not. A 4-minute film is not a compressed novel — it is a **single value shift, dramatized once, with one reversal.** Below is the adaptation used throughout this package.

---

## The Adaptation

| # | Novel Snowflake | **Film Snowflake (this package)** | Deliverable |
|---|---|---|---|
| 1 | One-sentence summary | **The Concept Sentence** — ≤ 15 words, contains a character, an engine, and an irony | 1 line |
| 2 | One-paragraph summary | **The Beat Paragraph** — 5 sentences = 5 beats. Sentence 3 is the reversal. | 5 lines |
| 3 | Character summaries | **The Want / Need / Lie / Ghost** — for the protagonist only | 4 lines |
| 4 | One-page synopsis | **The Runtime Map** — each of the 5 beats given a timecode and a shot count | table |
| 5 | Character synopses | **The Turn** — what exactly changes, in what shot, and what the audience sees change | 1 para |
| 6 | Expanded synopsis | **The Look Bible** — lens, light, palette, grain, camera grammar, and the 3 rules you never break | 1 page |
| 7 | Character charts | **The Consistency Sheet** — character card, wardrobe lock, location lock, prompt fragments to reuse verbatim | 1 page |
| 8 | Scene list | **The Shot List** — every shot, duration, lens, light source, motion, audio | table |
| 9 | Scene narrative | **The Prompt Cards** — the generation prompt per shot, with the locked fragments pasted in | 1 per shot |
| 10 | Write the draft | **Generate, select, cut, score** | the film |

**Rules of the method.** You may go back and revise any earlier step at any time — that is the point of it — but you may not skip forward. If Step 1 is weak, no amount of Step 9 will save it, and you will find that out having burned 400 generations.

---

## Why Each Step Exists Here

**Step 1 — the Concept Sentence.** Fifteen words is a brutal constraint on purpose. It is also, not coincidentally, Anderson's test: *what's the pitch?* If you can't say it in a breath, the jury can't repeat it to each other in deliberation, and a film the jury can't repeat does not win.

The sentence must contain three things:
- a **character** with a job or a role (not "a man"),
- an **engine** — the thing that forces motion,
- an **irony** — the reason this particular person is the worst or most painful choice for this particular situation.

> *A dam engineer walks into a drained reservoir to find the town his family lost — still keeping time.*

Character (dam engineer), engine (the drawdown clock), irony (he maintains the structure that drowned his own family). Fifteen words.

**Step 2 — the Beat Paragraph.** Five sentences, and sentence three is always the reversal. This is the whole architecture of a short. Most failed shorts have four sentences of setup and no third sentence. Write the third one first if you have to.

**Step 3 — Want / Need / Lie / Ghost.** Straight out of the schema you're already running in `story-fractal.json`. In a 4-minute film there is room for exactly one character to have an interior. Give it to the protagonist and let everyone else be pressure.
- **Want:** the stated, external, achievable goal.
- **Need:** the thing they actually require, which is usually the opposite.
- **Lie:** the sentence they believe that makes the Want feel like the Need.
- **Ghost:** the event in the past that installed the Lie.

**Step 4 — the Runtime Map.** Timecodes early, before you fall in love with anything. This is where films get saved. A beat that can't fit in 40 seconds isn't a beat, it's a feature.

**Step 5 — the Turn.** Name the exact shot where the protagonist stops believing the Lie. If you cannot point at a shot number, the film does not have an arc, it has a mood. **This is the step that wins or loses Catmull**, and it is the step everyone skips.

**Step 6 — the Look Bible.** This wins or loses Papamichael. Lens language, light motivation, palette, grain. Crucially it includes **three rules you never break** — because consistency across 50 AI shots comes from constraint, not from effort.

**Step 7 — the Consistency Sheet.** The single hardest technical problem in AI filmmaking is that your protagonist's face drifts. The solution is not better prompting per shot; it is **locked fragments reused verbatim** across every shot, plus a shot design that limits how often you need a clean, well-lit, frontal close-up. *(Hell Grind used ~3,000-word prompts for exactly this reason.)*

**Step 8 — the Shot List.** Now, and only now, does the film become a production. Every row carries duration, lens, light source, motion, and audio, because those five columns are what you paste into the prompt.

**Step 9 — the Prompt Cards.** One card per shot. The locked fragments from Step 7 pasted in verbatim, then the shot-specific content. These cards are *also* your open-source deliverable — which means the documentation you owe the festival is a byproduct of the method rather than a chore at the end. That is worth real Platform Engagement points.

**Step 10 — Generate, select, cut, score.** Budget by keep rate, not by shot count. See `docs/08-production-plan.md`.

---

## The One-Page Version

```
1. CONCEPT SENTENCE   ≤15 words. Character + engine + irony.
2. BEAT PARAGRAPH     5 sentences. #3 is the reversal.
3. WANT/NEED/LIE/GHOST  Protagonist only.
4. RUNTIME MAP        Timecodes + shot counts per beat.
5. THE TURN           The exact shot where the Lie dies.
6. LOOK BIBLE         Lens, light, palette, grain + 3 unbreakable rules.
7. CONSISTENCY SHEET  Locked prompt fragments, verbatim reuse.
8. SHOT LIST          Duration, lens, light, motion, audio.
9. PROMPT CARDS       One per shot. Locked fragments + specifics.
10. PRODUCE           Generate → select → cut → score → grade → mix.
```

A blank, fillable version is in `templates/snowflake-template.md`.

---

## How This Package Uses It

- **Slate A** (`04-slate-a-personal.md`) — five concepts taken to **Step 4**. Enough to judge, cheap to kill.
- **Slate B** (`05-slate-b-contenders.md`) — four judge-triangulated concepts taken to **Step 4**, each with an explicit score projection against the rubric.
- **SILT** (`06-silt-full-build.md`) — the greenlit film, taken to **Step 8**, plus the finished screenplay in `screenplay/SILT.md`.

Steps 9–10 begin on Aug 12 per the calendar, after the rules verification in `01-contest-brief.md` §6 is answered.
