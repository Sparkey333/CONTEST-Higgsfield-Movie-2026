# 04 — Sequence Architecture: Script → Scenes → Generations

The repeatable method for breaking a script into shootable 10–20 second generations **without**
fragmenting it into an ad reel.

> **Status: the method is complete and ready to run. It needs your script.**
> Drop it at [`../script/SCRIPT.md`](../script/SCRIPT.md) and this becomes a filled-in shot plan.
> Section 6 below is the worked template that gets populated.

---

# 1. THE FIVE-PASS BREAKDOWN

Never go from script straight to prompts. Five passes, in order. Each one is cheap; skipping one
is expensive.

### Pass 1 — Find the dramatic shape (read as a director, not a transcriber)

Read the script and mark only four things:

- **The want.** What does the protagonist want, stated in one sentence?
- **The turn.** The single moment where the film stops being about what you thought.
- **The cost.** What it takes from them.
- **The last image.** What the audience carries out.

If any of the four is missing or vague, **fix the script before touching the platform.** A
structural hole costs one afternoon of writing now, or 800 wasted generations later. This is the
Catmull pass — it is the only pass that decides whether you can win.

### Pass 2 — Collapse locations (the consistency pass)

Count distinct locations. Then cut the number as hard as the story allows.

- **Target: 1–2 locations for a 4–5 minute film.** Three is the ceiling.
- Every additional location costs a full location-sheet lock (~50–150 generations), a new light
  logic, and a new opportunity for the world to stop feeling real.
- **This is not a compromise.** Single-location is Anderson's signature register, it is what
  gives Papamichael one coherent light logic to reward, and it is what makes the film feel like a
  *place* rather than a slideshow.

Ask of every scene: *can this happen in the main location instead?* Usually yes, and usually better.

### Pass 3 — Assign the emotional units (the anti-fragmentation pass)

Divide the script into **emotional units**, not script pages. An emotional unit is a continuous
stretch with:
- the same characters in frame
- the same location
- **one continuous emotional or temporal movement** — no time skip, no mood pivot

**Each emotional unit is one long take if it can possibly be one long take.**

> **The load-bearing rule: don't fragment grief.**
> One continuous emotional collapse is ONE generation even if the script writes it as three lines.
> The temptation to give a big moment "coverage" is the single most common way an AI film
> becomes an ad reel. Big moments want *fewer* shots, not more.

### Pass 4 — Envelope the units into generations

Now, and only now, convert units to generations.

**Group into one generation when ALL of these hold:**
1. Same character set in frame
2. Same location or sub-area
3. One continuous emotional/temporal unit
4. Stageable in ≤ the model's ceiling (15s Seedance / 20s FLUX / 30s Wan)

**Split into separate generations when ANY of these fire:**
1. Hard cut between locations
2. A character entrance/exit changes the handle list
3. A setup change that needs its own envelope (wide establish → tight insert)
4. A performance arc that deserves its own envelope
5. An insert/cutaway to a prop or screen

**Complexity budget — any of these means split:**
> more than 2 strong actions · more than 2 camera moves · more than 3 important characters ·
> more than 1 complex VFX event · more than 1 location change

**Duration ladder:**
| Screen time | Content it can carry |
|---|---|
| 4–8s | One strong action |
| 8–12s | One action + a reveal |
| 12–15s | 2–3 simple beats |
| 15–20s (FLUX) | A full emotional arc, or a move through space |
| 20–40s (chained) | An anchor take — an entire scene |
| Complex fight / chase / transformation | Multiple generations, always |

**When in doubt, err toward tighter prompts, not longer ones.** The models handle tight prompts
better than overloaded ones — but note this is about *prompt density*, not clip duration. A 20s
clip with one slow action is easy; a 10s clip with six actions is hard. **Length is not the
enemy; an overloaded beat is.**

### Pass 5 — Assign transitions (the blending pass)

For every seam between generations, choose a transition from
[`02-DIRECTING-DOCTRINE.md`](02-DIRECTING-DOCTRINE.md) § 3 **and write it into both prompts.**

This is the pass everyone skips, and it is the pass that decides whether the film reads as one
movie. A transition is not a post-production decision you can make later — a match-on-action
anchor has to exist in the *generation* on both sides of the seam.

| Seam type | Default transition | Written into the prompt as |
|---|---|---|
| Within a scene, angle change | Match-on-action anchor | Same gesture at end of A and start of B |
| Within a scene, big reframe | Body/object wipe | "A figure crosses full-frame at 14.0s" |
| Scene → scene, same world | Through-object pass + light contrast | "Camera passes the arch: warm amber room → cold blue corridor" |
| Scene → scene, time skip | Repeated frame (rhyme cut) | Identical composition, one element changed |
| Anywhere in action | Whip-pan seam (max 2 per film) | "Ends on a fast pan frame-right, 180°/sec" |
| **Every seam** | **Sound bridge** | Post decision — but plan the audio bed for it |

---

# 2. THE TEMPO GATE

Before generating anything, run both checks.

**Check 1 — the sum.** All planned durations must add to your target runtime *exactly*.

**Check 2 — the monotony audit.** Write out only *framing + camera move* for every shot as one
column, and read it top to bottom. **No three consecutive shots may share both shot size and
camera move.** Per-shot review cannot catch this; only the column can.

```
1a  WIDE          static hold            ✓
1b  WIDE          slow push-in           ✓
1c  MEDIUM        slow push-in           ✓
2a  MEDIUM        slow push-in           ✗ ← three in a row sharing size+move. Fix.
```

---

# 3. THE SHOT LEDGER

The single source of truth. One row per generation. Keep it in
[`../log/SHOT-LEDGER.md`](../log/SHOT-LEDGER.md).

| ID | Scene | Dur | Model | Framing | Camera | Content | Transition IN | Transition OUT | Takes | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1a | 1 | 30s | Wan 3.0 | WIDE | slow crane down | *(from your script)* | — cold open | sound bridge | 0 | ⬜ |
| 1b | 1 | 15s | Seedance 2.0 | MED | static hold | | match-on-action | body wipe | 0 | ⬜ |

Status: ⬜ planned · 🟡 in iteration · 🟢 locked · 🔴 restructure (hit the 10–15 rule)

---

# 4. THE ASSET GLOSSARY

Declare every recurring asset once with a stable `@`-name, and register each under **Elements** in
Higgsfield under the *same* name so pasting a prompt auto-attaches the right references.

```
@[hero]        — protagonist                    [full-preserve]
@[hero_after]  — same character, changed state  [full-preserve]  ← build up front, never "make them dirty" later
@[loc_main]    — primary location, 3/4 view     [attribute-transfer: space + texture only]
@[object]      — the through-line object        [full-preserve]
```

**Multi-state variants get their own locked entry.** Asking the model to "make him bloodied" mid-
project makes it improvise and the face drifts. Build `@hero_after` deliberately in
pre-production.

**Each entry carries a fidelity grade** — *full-preserve* / *partial-preserve (name the parts)* /
*attribute-transfer (name the target)* / *loose-guide*. Without a grade, "use @image4 for the
coat" silently means whatever the model felt like keeping that day.

---

# 5. THE THREE-ACT SPINE FOR 4:30

A structural default to adapt, not obey. Durations assume a 270-second film.

| Act | Time | Screen | Function | Shot strategy |
|---|---|---|---|---|
| **Cold open** | 0:00–0:25 | 25s | The loaded still — arresting image, unanswered question | **1 anchor take.** Zero or one cut |
| **Act I** | 0:25–1:20 | 55s | Establish the want; make the space real | 3–4 sustained shots, 12–18s. Depth staging |
| **Act II-a** | 1:20–2:20 | 60s | Pursuit of the want; the world resists | 4–5 shots. First connective tissue. Rhythm tightens slightly |
| **The Turn** | 2:20–2:50 | 30s | The film becomes about something else | **1 anchor take, 20–30s.** No cuts. The face carries it |
| **Act II-b** | 2:50–3:35 | 45s | Consequence. **The one action passage** | **The burst.** 6–10 cuts in ~15s, then hold |
| **Act III** | 3:35–4:20 | 45s | The cost, paid | 2–3 sustained shots. Slowest passage in the film |
| **Last image** | 4:20–4:30 | 10s | The recontextualised opening | **1 held shot.** No cut. No music sting |

**Total: ~24 generations**, ~4:30. Inside the achievable envelope from
[`03-HIGGSFIELD-PLAYBOOK.md`](03-HIGGSFIELD-PLAYBOOK.md) § 2.

Note the shape of the rhythm: **slow → slightly faster → dead stop (the turn) → detonation →
slowest.** The film's fastest passage sits directly between its two slowest. That contrast is
the entire effect, and it is free.

---

# 6. WORKED TEMPLATE — populate per scene

Copy this block per scene once the script lands.

```markdown
## SCENE [N] — [title]  ·  [location]  ·  [screen time]

**Emotional unit:** [one sentence — what changes across this scene]
**Want in this scene:** [what the protagonist is trying to get]
**Turn:** [the moment inside the scene where it shifts]
**Truth layer:** [which of the six layered-truth devices this scene carries]

**GEO SPATIAL LAYOUT** (locked, pasted into every shot in this scene):
— [LANDMARK] = [description], [position]
— [LANDMARK 2]: [position relative to first, in metres]
— 180° AXIS: camera ALWAYS stays [side] — it NEVER crosses [line]
— LIGHT LOGIC: [the ONE source], [direction], [what it does not reach]

**Generations:**

| ID | Dur | Model | Framing / Camera | Beat | Transition OUT |
|---|---|---|---|---|---|
| Na | | | | | |
| Nb | | | | | |

**Depth staging:** FG [ ] · MG [ ] · BG [ ]
**Micro-life plan (shots >12s):** [what moves every 1–2s]
**Risk flags:** [reflections · doubles · crowds · compound moves · door geometry · named fight moves]
```

---

# 7. HIGH-RISK SHOTS — flag at authoring time, not after burning credits

Known failure modes. If a planned shot contains one of these, either redesign it now or budget
3× the iterations.

| Risk | Why it breaks | Redesign |
|---|---|---|
| **Named martial-arts moves** | Roundhouse kicks etc. need multi-frame choreography the model can't execute | "General fighting energy"; describe the *outcome*, not the technique |
| **Two characters in close contact** | Limb merging; grappling renders as embracing | Keep at arm's length, or split into two shots. Plain text, not @Elements, for action |
| **Reflections / mirrors** | Geometry rarely resolves | Avoid, or shoot the reflection as its own plate |
| **Same character doubled in frame** | Identity collapse | Separate shots, composite in post |
| **Crowds** | Count drifts wildly between takes | One "crowd" asset with height/clothing range; **state the number** — "20+" |
| **Compound camera moves** | Jitter | One move per shot |
| **Door entries** | Geometry breaks | Start the shot with the door **already opening** |
| **Fast action** | Exceeds temporal coherence | Generate in slow motion, speed up in post |
| **Giants / extreme scale** | Model shrinks them back toward human height | Scale law + a human figure in frame + state what a failed shot looks like |

---

# 8. THE FIVE RULES, COMPRESSED

1. **Assets first.** No narrative shot until every character and location is locked and stress-tested.
2. **Describe everything, every time.** The model has no memory.
3. **Change one thing at a time.** And log it.
4. **Give the model less freedom.** A corner, not a room. A map, not guesswork.
5. **If a shot won't come together — simplify the shot, not the words.**

---

## Sources

- Higgsfield `higgsfield-shotlist-director` (density heuristic, complexity budget, tempo/monotony gates, `@`-glossary, fidelity grades)
- Higgsfield `HELL-GRIND.md` (GEO block, assets-first, 10–15 rule, states-not-transitions, crowd/scale handling)
- Higgsfield `negative-constraints.md` (risk table)
- Higgsfield `higgsfield-camera/SKILL.md` (duration ladder, one-move rule)
