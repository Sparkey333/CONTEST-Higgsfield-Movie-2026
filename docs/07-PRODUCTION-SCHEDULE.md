# 07 — Production Schedule: 24 Days

**Start:** Monday, August 10, 2026 (today)
**Deadline:** Thursday, September 3, 2026
**Your deadline:** **Tuesday, September 1** — a 48-hour buffer. Platform load at a $1M deadline
is a predictable failure mode, and "the site was slow" is not an appeal.

**Working days available: 22.**

---

# THE SHAPE

Adapted from the Hell Grind team's Week 1 / Week 2 discipline, which is the single most important
scheduling insight in the open-sourced corpus:

> **Phase 1: get every shot present, even if rough — the complete shape of the film.
> Phase 2: concentrate all remaining iteration on the shots that carry the emotional weight.**

Without that split, iteration cost runs the project over before the ending exists. The failure
mode this prevents is real and near-universal: a gorgeous first 90 seconds and an unfinished
final act.

| Phase | Days | Dates | Output |
|---|---|---|---|
| **0 — Decide** | 1–3 | Aug 10–12 | Concept locked, script locked, rules verified |
| **1 — Assets** | 4–7 | Aug 13–16 | Character + location sheets locked, style frozen, models tested |
| **2 — Assembly** | 8–16 | Aug 17–25 | **Every shot exists.** Rough cut of the whole film |
| **3 — Refinement** | 17–20 | Aug 26–29 | The 5 shots that matter, re-shot to final |
| **4 — Finish** | 21–22 | Aug 30–31 | Sound, grade, master |
| **5 — Submit** | 23 | Sept 1 | Submitted. Two days spare. |

---

# PHASE 0 — DECIDE (Days 1–3 · Aug 10–12)

The most valuable days in the schedule. Nothing generated.

**Day 1 (Aug 10)**
- [ ] ⚠️ **Read the official rules page.** Resolve all four unknowns in
      [`00-CONTEST-BRIEF.md`](00-CONTEST-BRIEF.md) — especially **maximum runtime** and whether
      *all generation* must happen inside Cinema Studio. The second answer determines whether
      your long-take models are legal.
- [ ] Confirm subscription tier and credit headroom (see § Credit budget below)
- [ ] Create the festival project in Cinema Studio
- [ ] Add your own concepts to [`../script/IDEAS-INBOX.md`](../script/IDEAS-INBOX.md)

**Day 2 (Aug 11)**
- [ ] Score every concept — yours and the six — through
      [`06-WARGAME.md`](06-WARGAME.md) § 5
- [ ] Apply the kill criteria honestly
- [ ] Shortlist to two

**Day 3 (Aug 12)**
- [ ] **Lock ONE concept.** No revisiting.
- [ ] Write / finalise the script into [`../script/SCRIPT.md`](../script/SCRIPT.md)
- [ ] Run the five-pass breakdown ([`04-SEQUENCE-ARCHITECTURE.md`](04-SEQUENCE-ARCHITECTURE.md) § 1)
- [ ] Fill [`../log/SHOT-LEDGER.md`](../log/SHOT-LEDGER.md) completely — every shot, duration,
      model, transition
- [ ] Run the tempo gate: **the sum check and the monotony audit**

> **Gate: do not proceed to Phase 1 until the ledger sums exactly to your target runtime.**

---

# PHASE 1 — ASSETS (Days 4–7 · Aug 13–16)

**Assets first. Do not generate a single narrative shot this week.** This rule saves more money
than everything else combined.

**Day 4 (Aug 13) — Style & model tests**
- [ ] Freeze the Style Prefix ([`03-HIGGSFIELD-PLAYBOOK.md`](03-HIGGSFIELD-PLAYBOOK.md) § 8)
- [ ] Model bake-off at 480p: same prompt through Seedance 2.0 / Kling 3.0 / FLUX 3 / Wan 3.0
- [ ] Decide routing per shot type. Record it in the ledger.
- [ ] **Verify the long-take route works** — generate one 20s FLUX and one 30s Wan. If the
      continuation chain fails here, restructure the anchor shots now, not on Day 18.

**Days 5–6 (Aug 14–15) — Character lock**
- [ ] Character sheet: **3 panels — face CU (3/4 view, large), full body front HEADLESS, full body
      back.** Neutral grey, flat light, real pores, no retouch, no baked-in film look.
- [ ] Budget **~800 generations** for the lead. This is normal. It is not going badly.
- [ ] Build every state variant now (`@hero`, `@hero_after`) — never ask for a state change later
- [ ] Lock the voice descriptor: register, tempo, accent, manner
- [ ] Lock the behaviour paragraph: movement, hands, habits, eye behaviour, how they break
- [ ] **Stress-test:** generate the character in three different lighting setups. If the face
      drifts, fix the sheet — do not proceed.

**Day 7 (Aug 16) — Location lock**
- [ ] Location sheet in **3/4 view, never frontal**
- [ ] A named anchor object in every location
- [ ] **One light logic** — one source, one shadow direction
- [ ] Reverse angles via the empty-location walkthrough trick
- [ ] Write the **GEO SPATIAL LAYOUT** block for every scene. Freeze them.

> **Gate: characters and locations must survive a three-lighting stress test before Phase 2.**

---

# PHASE 2 — ASSEMBLY (Days 8–16 · Aug 17–25)

**The rule: every shot in the film exists by Day 16, at whatever quality.** Rough is fine.
Missing is not.

Nine days, ~24 shots: **roughly 3 shots per day**, ~130 generations/day.

| Days | Target |
|---|---|
| 8–9 (Aug 17–18) | Act I — establish the space and the want |
| 10–11 (Aug 19–20) | Act II-a |
| 12–13 (Aug 21–22) | **The Turn** — the anchor take. Give it two full days. |
| 14 (Aug 23) | The action burst |
| 15 (Aug 24) | Act III |
| 16 (Aug 25) | Cold open + last image |

**Discipline during Phase 2:**
- **The 10–15 rule.** If a shot hasn't converged in 10–15 iterations, the problem is not the
  wording. **Simplify the shot** — split it, remove an action, change the angle. Move on the
  same day.
- **One variable per iteration**, logged. Multi-variable iteration makes diagnosis impossible.
- **Cull at 480p**, commit at 4K. Never iterate at full resolution.
- **Generate long, harvest short.** For action beats, generate 15s and cut the best 2 seconds.
- **Assemble as you go.** Drop every rough shot on the timeline the day you make it. You need to
  *see* the film's shape by Day 16, not imagine it.

> **Gate (Day 16): a complete rough cut exists, start to finish, at the target runtime.**
> If it doesn't, cut a scene. Do not extend Phase 2 into Phase 3 — a film with a weak middle
> and a finished ending beats a film with a beautiful opening and no ending.

---

# PHASE 3 — REFINEMENT (Days 17–20 · Aug 26–29)

Watch the rough cut. Identify the **five shots that carry the film** — almost always: the cold
open, the turn, the peak of the action, the last shot before the ending, and the final image.

**Re-shoot only those five.** Everything else is done.

| Day | Focus |
|---|---|
| 17 (Aug 26) | The turn — the anchor take. The most important shot in the film. |
| 18 (Aug 27) | Cold open + final image (they are one unit — the recontextualisation must work) |
| 19 (Aug 28) | Action peak + one remaining weak shot |
| 20 (Aug 29) | Buffer. **Do not add scope.** Fix, don't extend. |

**Run the monotony audit again on the actual cut** — not the plan. Things drift.

---

# PHASE 4 — FINISH (Days 21–22 · Aug 30–31)

This is where the film stops feeling like generations and starts feeling like a movie. Do not
compress this.

**Day 21 (Aug 30) — Sound**
- [ ] **Sound bridges on every seam.** The highest-leverage two hours in the entire project.
      Audio continuity is what makes independently-generated clips read as one continuous world.
- [ ] Continuous ambient bed under the whole film — one room tone that never cuts
- [ ] Diegetic SFX with real weight: footsteps, breath, contact, material
- [ ] Score last, and sparingly. **Consider none at all** — a film with no music in a festival of
      films with trailer scores is instantly distinctive, and all three judges are people who
      notice silence.
- [ ] Dialogue: clean and close, ambience dipping beneath

**Day 22 (Aug 31) — Picture finish**
- [ ] Grade for **one light logic** across the whole film — this is where two-suns errors get
      partially rescued
- [ ] Match grain across shots (matched to a reference plate, not applied globally)
- [ ] Best-second splices — assemble hero shots from the best seconds of multiple takes
- [ ] Title and credits: minimal, late, quiet
- [ ] Export at the required spec

---

# PHASE 5 — SUBMIT (Day 23 · Sept 1)

- [ ] Final watch, start to finish, uninterrupted, on the largest screen available
- [ ] Runtime ≥ 3:00 and within any confirmed maximum
- [ ] Re-read the rules one final time against the finished file
- [ ] **Submit**
- [ ] Confirm receipt
- [ ] Post the vertical cut for Audience Choice

**Sept 2–3: spare.** Do not use them. If you are using them, something went wrong on Day 16 and
you should have cut a scene.

---

# CREDIT BUDGET

| Item | Generations |
|---|---|
| Style & model tests | 150 |
| Lead character sheet | 800 |
| Second character / variants | 400 |
| Location sheets (1–2) | 250 |
| Phase 2 assembly (24 shots × ~65) | 1,560 |
| Phase 3 refinement (5 shots × ~80) | 400 |
| Contingency (15%) | 540 |
| **Total** | **~4,100** |

At the community-harvest benchmark (13,626 generations for one solo 2–3 minute short) this is a
**disciplined** budget, not a generous one. It assumes the shot count stays at ~24.

> **Every shot you add costs ~65 generations and roughly half a day.** This is the arithmetic
> behind the whole long-take strategy: at a 1.5% acceptance rate, a 24-shot film gets 100 takes
> per shot and a 70-shot film gets 34. **Fewer shots is not a stylistic preference — it is how
> you buy quality.**

- [ ] Verify credit balance covers ~4,100 generations **on Day 1**, not Day 12
- [ ] Set up auto-refill so a mid-iteration wall never costs you a session

---

# THE FIVE FAILURE MODES

Ranked by how often they kill projects like this one.

1. **No ending.** All budget spent on the first 90 seconds. → *Phase 2's "every shot exists by
   Day 16" gate exists solely to prevent this. It is non-negotiable.*
2. **Concept churn.** Changing the film in week two. → *Day 3 lock. No revisiting.*
3. **Perfecting a shot that doesn't matter.** 200 iterations on shot 7. → *The 10–15 rule.*
4. **Skipping asset lock.** Generating narrative shots on Day 5 and fighting drift for three
   weeks. → *Phase 1 gate.*
5. **Rushing the finish.** Submitting a graded-in-an-hour file. → *Two full days, protected.*

---

# DAILY DISCIPLINE

Every day, in the log:

```
## Day N — [date]
Generations: [n]     Kept: [n]     Rate: [%]
Shots advanced: [ids]
Shots locked: [ids]
Blocked on: [ ]
Tomorrow: [ ]
```

Track the acceptance rate. If it is far below 1.5%, the problem is upstream — usually the assets,
occasionally the model routing. **Stop generating and fix the asset.** Iterating against a broken
character sheet is the most expensive mistake available to you.
