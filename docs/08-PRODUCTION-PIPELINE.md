# 08 — The Production Pipeline

**The canonical order of operations for building any short film on this stack.** Not
Vantage-specific — this is the reusable process. Swap the story, keep the pipeline.

Eight stages, each with an explicit **entry condition**, **work**, **consistency check** and
**exit gate**. A stage does not begin until the previous stage's gate passes. Every gate exists
because skipping it costs more later than passing it costs now.

```
0 LOCK ──▶ 1 CALIBRATE ──▶ 2 CHARACTER ──▶ 3 LOCATION ──▶ 4 KEYFRAMES ──▶ 5 MOTION ──▶ 6 ASSEMBLY ──▶ 7 FINISH
  no gens      ~150            ~800            ~250           ~600          ~1,800        re-shoot 5      no gens
```

**The one-line summary:** *lock the plan, prove the tools, build the people, build the place,
freeze every first frame, then and only then generate motion.*

---

## The governing economics

Everything below is shaped by three numbers:

| | |
|---|---|
| Video acceptance | **~1.5%** (65–100 generations per kept shot) |
| Image acceptance | **~1.0%** |
| **Cost ratio** | **A still costs roughly a tenth of a clip** |

That last line is the one nobody acts on, and it drives Stage 4. **Every decision you can make on
a still instead of a clip, you make on a still.** Framing, blocking, wardrobe, light direction,
lens feel, colour — all of it resolves in images at a tenth the burn. By the time you generate
motion, the only open question should be *the motion*.

Most failed AI shorts are people iterating framing decisions at video prices.

---

# STAGE 0 — LOCK
### No generation. This is the cheapest stage and the one that decides everything.

**Entry:** a concept and a rough story.

**Work**
1. **Verify platform constraints.** Max runtime, which surface the deliverable must be built in,
   entry limits, rights. Model duration ceilings.
2. **Score concepts through the harness.** Film grade, judge fit, make-ability, multipliers.
   Apply the kill criteria honestly. **Lock one.** No revisiting.
3. **Five-pass script breakdown** — dramatic shape → collapse locations → emotional units →
   envelope into generations → assign transitions.
4. **Build the shot ledger.** Every shot: ID, duration, model, framing, camera, beat,
   transition in/out.
5. **Freeze the Style Prefix.** After this it is edited once and re-propagated everywhere, never
   per-shot.
6. **Assemble the Story Bible** from all of the above.

**Consistency check** — read the ledger's framing + camera column top to bottom as a single
column. This is the only place the monotony failure is visible.

> ### GATE 0
> - [ ] The turn is stateable in one sentence
> - [ ] Durations sum to the target runtime **exactly**
> - [ ] No run of three consecutive shots shares shot size AND camera move
> - [ ] Shot-length distribution sits inside its target bands
> - [ ] ≤2 locations, ≤2 locked characters
> - [ ] Story Bible exists and names one light source per location

---

# STAGE 1 — CALIBRATE
### ~150 generations, all at the lowest resolution available. Buy information, not frames.

**Entry:** Gate 0 passed.

**Work**
1. **Style probe.** One representative frame from the middle of your film. Same prompt, run
   through every candidate model. Compare at 480p. Pick the look, and record which model won
   for which job.
2. **Duration probe.** Prove the long-take route *actually works* before the plan depends on it.
   Generate one clip at your longest planned duration. Then prove the continuation chain: extend
   it once and check whether identity and light survive the seam.
3. **Filter probe.** Run your character and location descriptors through a cheap generation and
   confirm nothing trips content moderation. Finding this in Stage 5 costs a day.
4. **Aspect probe.** Confirm your target ratio is available on every model you plan to use.

**Consistency check** — generate the same prompt twice. How far apart are the two results? That
spread is your baseline noise, and it tells you how many takes a shot will really need.

> ### GATE 1
> - [ ] Model routing decided and written into the ledger
> - [ ] The longest planned shot has been generated successfully at least once
> - [ ] The continuation chain has been proven, or the plan has been restructured without it
> - [ ] No descriptor trips the content filter
> - [ ] Target aspect ratio confirmed available

**If the duration probe fails, go back to Stage 0 and re-envelope the shots.** Do not proceed
hoping it will work later. It will not.

---

# STAGE 2 — CHARACTER
### ~800 generations for a lead. This is the long pole. Budget for it and do not flinch.

**Entry:** Gate 1 passed.

**Work — strictly in this order**

1. **Face close-up, 3/4 view, large.** Generate wide, cull hard. This single image is the source
   of truth for every face in the film. Nothing else starts until it is locked.
2. **Full body, front — HEADLESS.** Built *from* the locked face image.
   *Why headless:* on wide shots the model sources the face from whichever panel it likes, and
   the tiny blurry face on a full-body panel wins often enough to break a whole class of shots.
   Remove that head and there is exactly one place the face can come from.
3. **Full body, back.**
4. **Assemble the three-panel sheet.**
5. **State variants** — every version the story needs (dirty, wet, wounded, older). **Build them
   now.** Asking the model to "make her dirty" in week three makes it improvise and the face
   drifts.
6. **Lock the voice descriptor** — register, tempo, accent, manner. Pasted verbatim every time
   they speak, forever.
7. **Lock the behaviour paragraph** — movement, hands, habits, eye behaviour, how they break
   under pressure.

**Sheet discipline:** neutral grey background, flat even light, real skin with visible pores, no
retouch. **Deliberately boring.** Bake a cinematic lens or film grain into the sheet and the
character carries that look into every scene and stops reacting to new light.

**Never run an image through a model twice in full.** Point changes — a scar, a jacket, blood —
are made on the original, then composited back with a mask. Two full passes and the face goes
symmetrical, plastic, and lifeless — and dead texture damages the *acting* later.

**Consistency check — the three-lighting stress test.** Generate the character in three different
lighting setups from your film. Hard side light. Soft frontal. Near-darkness with one rim. If the
face drifts between them, **the sheet is wrong — fix the sheet, do not proceed.** Every hour spent
here saves ten in Stage 5.

> ### GATE 2
> - [ ] Face survives three lighting setups with no drift
> - [ ] Three-panel sheet assembled, front panel headless
> - [ ] Every state variant built and locked
> - [ ] Voice descriptor written
> - [ ] Behaviour paragraph written
> - [ ] All tags registered in the platform's reference/Elements panel under glossary names

---

# STAGE 3 — LOCATION
### ~250 generations for one location.

**Entry:** Gate 2 passed.

**Work**
1. **Primary angle in 3/4 view — never frontal.** A frontal "pretty picture" becomes flat
   wallpaper on wides, and past its edges the model invents new surroundings every time. A 3/4
   view gives depth to read and covers close to a full circle of angles.
2. **Name the anchor object.** A column, a lamp, a table. All staging ties to it. *"At the lamp,
   facing the door"* works; *"in the room"* is a lottery.
3. **Declare the light logic.** One source, one shadow direction. Never two suns.
4. **Reverse angles — the walkthrough trick.** Generate a *video* of the empty location with the
   camera walking slowly through the space. The model draws the other sides consistently with the
   sheet. Screenshot the angles you need, then upscale and texture-improve them as stills. **A
   full location sheet from a single image.**
5. **Write and freeze the GEO SPATIAL LAYOUT block** — landmarks, distances in metres, the 180°
   axis, the light logic. No characters, no action. Pasted unchanged into every shot in that scene.

**Consistency check** — place the character in the location at two different angles. Does the room
hold? Does the light still come from the same side? Does the anchor object stay put?

> ### GATE 3
> - [ ] Location reads consistently from three or more angles
> - [ ] Anchor object named and used in staging language
> - [ ] One light source, one shadow direction, in every angle
> - [ ] GEO block written and frozen
> - [ ] Reference role explicitly ties inheritance — *"take only space and texture; do not inherit
>       composition, angle or grade"*

---

# STAGE 4 — KEYFRAMES
### ~600 generations. **The stage everyone skips, and the one that pays for itself twice.**

**Entry:** Gate 3 passed.

**Work.** For every shot in the ledger, generate its **first frame as a still** and lock it.

**Why this stage exists.** A still costs roughly a tenth of a clip. Every decision that can be made
in an image — framing, blocking, wardrobe state, light direction, lens feel, depth staging,
composition — is made here at a tenth the price. Then the locked frame feeds the video model
directly as its start frame, so motion generation begins from a known-good image instead of
gambling on one.

**A bad first frame guarantees a bad clip.** No amount of motion prompting rescues a shot whose
opening composition was wrong.

**Order:** work through the ledger in shot order. It is mechanical and it should feel mechanical.

**Also lock the END frame** for any shot using start+end control, and for both sides of a
match-on-action seam — the anchor gesture has to exist in both frames or the cut will not work.

**Consistency check — the contact sheet.** Lay every locked keyframe out in film order and look at
them together as one grid. You are checking four things:
- **Identity** — is it the same person in all of them?
- **Light** — does one source govern every frame, from a consistent direction?
- **Palette** — do they belong to the same film?
- **Rhythm** — read the framings across the grid. Does the composition vary the way the ledger says?

**This grid is the closest thing to seeing your film before you make it.** If it looks like a
coherent movie in stills, the motion stage is execution. If it looks like a mood board, stop —
fixing it now costs a tenth of fixing it later.

> ### GATE 4
> - [ ] Every shot has a locked first frame
> - [ ] Start+end shots and match-cut seams have both frames
> - [ ] The contact sheet reads as one film — identity, light, palette, rhythm
> - [ ] Keyframes filed in `FINAL KEYFRAMES`

---

# STAGE 5 — MOTION
### ~1,800 generations. The expensive stage. You enter it with every decision already made.

**Entry:** Gate 4 passed.

## Shot order — deliberately not chronological

| # | What | Why this order |
|---|---|---|
| 1 | **The hardest shot** (usually the turn / anchor take) | If it cannot be made, the film has to change — and you need to know that on day one of this stage, not day nine |
| 2 | **Cold open + last image, as one unit** | They must rhyme. Generating them apart produces two shots that nearly match, which is worse than not rhyming at all |
| 3 | **Act I** | Establishes the space; earliest shots teach you the most about the location's behaviour |
| 4 | **Middle acts** | Bulk work, now with everything learned |
| 5 | **The burst** | Short clips, cheap, high hit rate. Safe to leave late |
| 6 | **Connective tissue** | Cheapest and most forgiving. The buffer if you run out of days |

**Never generate chronologically.** Chronological order spends your best energy and credits on the
opening and leaves the ending — the thing the jury remembers — to whatever is left.

## The per-shot iteration loop

```
  ┌─▶ 1. PROMPT — from the builder; keyframe attached as start frame
  │   2. BATCH  — generate N at low resolution
  │   3. TRIAGE — reject / maybe / keep, in one pass, fast
  │   4. GATES  — run the four review gates on any keep
  │   5. ONE VARIABLE — change exactly one line, log it
  └───  6. repeat
      7. LOCK — regenerate the winner at full resolution, file it
```

**Rules that make the loop converge:**

- **One variable per iteration.** Rewrite a prompt fully and you lose the parts that worked, and
  you can no longer attribute the change. Log every version: what changed, what happened.
- **Cull at low resolution, commit at full.** Never iterate at 4K.
- **Generate long, harvest short.** For a 2-second burst cut, generate 15 seconds and take the
  best 2. Cheaper per usable second than generating short.
- **The 10–15 rule.** If a shot has not converged in 10–15 iterations, **the problem is not the
  wording.** Simplify the shot: split it in two, remove an action, change the angle. Do it the
  same day. This rule is what stops one shot eating a week.
- **Complex action opens the prompt.** A door that will not break, a punch that will not land —
  the character shuffles and freezes. Fix: the action is *already underway* in the first frame
  ("already mid-swing, the door already cracking"), and the approach becomes its own shot.
  **States, not transitions.**
- **The best-second splice is normal practice.** A finished shot is often one take's opening
  spliced to another take's ending. The film is assembled from the best seconds of many takes,
  not from whole kept takes.

## The four review gates — every keep passes all four

| Gate | Question | Common failure |
|---|---|---|
| **A · Technical** | Does it render clean? | Jitter, flicker, morphing limbs, warped hands, temporal artifacts |
| **B · Consistency** | Same person, same place, same light? | Face drift, room geometry changing, shadow direction flipping |
| **C · Photographic** | Would a naturalist DP accept this light? | Two suns, sourceless glow, over-lighting, plastic skin, unmotivated camera |
| **D · Dramatic** | Does the beat actually land? | Dead face on a long hold, emotion announced not built, no micro-life |

**Gate D is the one people skip**, because a technically clean shot feels like success. A shot can
be flawless and still be worthless. Ask it out loud: *did the thing that was supposed to happen in
this shot happen?*

**Assemble as you go.** Drop every accepted shot onto the timeline the day you make it. You need
to *see* the film's shape accumulating, not imagine it.

> ### GATE 5
> - [ ] Every shot in the ledger exists at usable quality
> - [ ] A complete rough cut runs start to finish at target runtime
> - [ ] Every kept shot passed all four review gates
> - [ ] Iteration log complete

**If you are behind schedule at this gate, cut a scene — do not extend the stage.** A film with a
weak middle and a finished ending beats a film with a beautiful opening and no ending. Always.

---

# STAGE 6 — ASSEMBLY

**Entry:** Gate 5 passed.

**Work**
1. **Watch the rough cut whole, uninterrupted, on the largest screen available.** Take no notes
   during. Notes during a first watch are notes about details; you need the shape.
2. **Then write down the five shots that carry the film.** Almost always: the cold open, the turn,
   the peak, the last shot before the ending, and the final image.
3. **Re-shoot only those five.** Everything else is done. This is the discipline that makes the
   schedule survive.
4. **Re-run the monotony audit on the actual cut**, not the plan. Things drift during production.

> ### GATE 6
> - [ ] The five carrying shots are at final quality
> - [ ] Monotony audit passes on the assembled cut
> - [ ] No new scope added

---

# STAGE 7 — FINISH
### No generation. This is where a pile of clips becomes a film. Do not compress it.

**Work, in this order**

1. **Sound bridges on every seam.** The audio of the next scene starts 1–2 seconds before the
   picture cuts. **This is the highest-leverage work in the entire pipeline** — the ear commits to
   continuity before the eye notices the change, and it is what makes independently-generated
   clips read as one continuous world. Two hours here beats two days of extra generation.
2. **One continuous ambient bed** under the whole film. One room tone that never cuts.
3. **Diegetic SFX with real weight** — footsteps, breath, contact, material.
4. **Dialogue mix** — clean and close, ambience dipping beneath.
5. **Score last, and sparingly.** Consider none at all.
6. **Grade for one light logic** across the whole film. This is where residual inconsistencies get
   partially rescued.
7. **Match grain to a reference plate** — never applied globally as a quality plea.
8. **Titles** — minimal, late, quiet.
9. **Export** to the required spec.

> ### GATE 7
> - [ ] Every seam has a sound bridge
> - [ ] Ambient bed continuous across the whole film
> - [ ] Grade consistent with the film's declared light logic
> - [ ] Runtime within spec
> - [ ] Delivered with time to spare

---

# THE FOLDER STRUCTURE

Adopt on day one. It costs nothing and it is how you find a good take three weeks later.

```
/TESTS               calibration, model bake-offs. The BIGGEST folder. Expect ~60% of all
                     generations to live here. Budget the tests as the work, not as overhead.
/CHARACTER           sheets, variants, stress tests
/LOCATION            angles, walkthroughs, GEO reference
/FINAL KEYFRAMES     the locked frame each shot was built from
/FINAL GENERATIONS   accepted takes
/FAILED GENERATIONS  discards, kept on purpose — knowing what didn't work is navigation
/scene-01 … /scene-N
```

---

# THE FIVE LAWS

Everything above compresses to these. When in doubt, apply them in order.

1. **Assets first.** Not one narrative shot until every character and location is locked and
   stress-tested. This saves more money than everything else combined.
2. **Describe everything, every time.** The model has no memory. Descriptors go in verbatim,
   never shortened. Consistency is not a setting; it is repetition.
3. **Decide on stills, execute in motion.** A still costs a tenth of a clip.
4. **Change one thing at a time, and log it.**
5. **If a shot will not come together, simplify the shot — not the words.**

---

# ADAPTING THIS PIPELINE TO ANY SHORT FILM

The stages and gates are invariant. These scale:

| Film shape | What changes |
|---|---|
| **2 characters** | Stage 2 roughly doubles (~1,600 gens). Add a two-shot consistency check: both faces in one frame, at distance |
| **3+ locations** | Stage 3 multiplies per location. Each needs its own GEO block and its own light logic. Strongly reconsider |
| **Dialogue-heavy** | Add a lip-sync probe to Stage 1. Trim lines to 3–8s. Lock camera to static or slow push during speech |
| **Action-heavy** | Stage 4 matters more, not less — lock the start frame of every beat. Generate in slow motion, speed up in post |
| **Crowds** | One crowd asset with a height/clothing range. State the count explicitly. Leads get their own sheets |
| **Longer runtime** | Stages scale linearly except Stage 2, which is fixed per character — so longer films are *cheaper per minute* |
| **Team instead of solo** | Parallelise Stages 2 and 3 across people; keep Stage 0 and Gate 4 centralised, or the film splits into several films |

---

## Related

- [`04-SEQUENCE-ARCHITECTURE.md`](04-SEQUENCE-ARCHITECTURE.md) — the Stage 0 breakdown method
- [`03-HIGGSFIELD-PLAYBOOK.md`](03-HIGGSFIELD-PLAYBOOK.md) — prompt grammar, model routing, the Papamichael filter
- [`02-DIRECTING-DOCTRINE.md`](02-DIRECTING-DOCTRINE.md) — why the shots are shaped this way
- [`07-PRODUCTION-SCHEDULE.md`](07-PRODUCTION-SCHEDULE.md) — these stages mapped onto 24 calendar days
- [`../prompts/`](../prompts/) — the ready-to-run prompts, in pipeline order
- [`../script/STORY-BIBLE.md`](../script/STORY-BIBLE.md) — the grounding document Stage 0 produces
