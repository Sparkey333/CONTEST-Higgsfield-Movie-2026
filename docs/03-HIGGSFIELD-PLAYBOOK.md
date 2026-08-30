# 03 — Higgsfield Technical Playbook

Everything platform-specific: which model for which shot, how to write the prompt, how to keep a
character and a room consistent for five minutes, and what it will actually cost.

Sourced from the live Higgsfield model catalogue (queried 2026-08-10) and Higgsfield's
open-sourced **Hell Grind** production system.

---

# 1. MODEL ROUTING — the duration table

**This is the most important table in the repo.** Your 10–20 second target is not available on
most models.

| Model | Duration | Max res | Start/End frame | Continuation | Native audio | Notes |
|---|---|---|---|---|---|---|
| **Wan 3.0** | **2–30s** | 1080p | ✅ first/last | ✅ refs | ✅ | **Longest single generation.** Has a `thinking` mode for prompt adherence |
| **FLUX 3 Video** | **5–20s** | 1080p | ✅ start+end | ✅ **video-continuation** | ✅ | **The long-take workhorse.** 21:9 and 2:1 available |
| Seedance 2.0 | 4–15s | **4K** | ✅ start+end | ✅ video refs | ✅ | The Hell Grind engine. Best identity consistency. 21:9 |
| Kling v3.0 | 3–15s | 4K | ✅ start+end | — | ✅ | Multi-shot, motion transfer, best skin realism |
| MiniMax H3 | 4–15s | 2K | ✅ start+end | ✅ refs | — | Batch up to 4 — good for cheap take-culling |
| Cinema Studio Video v2 | **3–12s** | — | ✅ | — | ✅ | Genre + speedramp + multi-shot controls |
| Gemini Omni Flash | 4–10s | 720p | refs only | ✅ | ✅ | Short only |
| Veo 3 | fixed | — | start only | — | ✅ | Reliable, limited control |

### Routing doctrine

| Shot type | Model | Why |
|---|---|---|
| **Anchor long takes (20–40s)** | **FLUX 3 Video** chained via continuation, or **Wan 3.0** single-pass at 30s | Only two models reach past 15s |
| **Sustained dialogue / performance (12–15s)** | **Seedance 2.0** (4K, std mode) | Best identity lock; the Hell Grind grammar is built for it |
| **Faces, skin, emotional close-ups** | **Kling v3.0** | Documented best for realistic skin; avoids the waxy tell |
| **Action bursts (1–3s)** | **Seedance 2.0** at 15s, then cut the best 2 seconds | Generate long, harvest short — standard production practice |
| **Establishing / atmospheric wides** | **Wan 3.0** at 20–30s | Long holds with atmospheric motion are its strength |
| **Cheap exploration / previz** | **Seedance 2.0 Mini** or **MiniMax H3** batch | Cull at 480p before committing |

> ⚠️ **Contingency.** If the contest rules require *all* generation inside the Cinema Studio
> festival project, Cinema Studio Video v2 caps at **12 seconds** and the FLUX/Wan long-take
> route may be unavailable. In that case the anchor shots must be built by **continuation
> chaining at 12s** and the invisible-cut techniques in
> [`02-DIRECTING-DOCTRINE.md`](02-DIRECTING-DOCTRINE.md) § 3 become load-bearing rather than
> decorative. **Resolve this before locking the shot plan** — see
> [`00-CONTEST-BRIEF.md`](00-CONTEST-BRIEF.md) § The four unknowns.

---

# 2. THE PRODUCTION ECONOMICS — read this before you plan anything

From Higgsfield's own disclosed Hell Grind numbers, cross-checked against a 13-project community
harvest:

| Metric | Value |
|---|---|
| **Image acceptance rate** | **~1.0%** |
| **Video acceptance rate** | **~1.5%** |
| Generations per kept shot | **65–100** |
| Iterations to lock ONE lead character sheet | **~800** (600 Soul Cinema + 200 GPT Image 2) |
| Worst-case single 10s establishing shot | **72 generations** |
| Hell Grind total | 108,859 generations / 9.54M credits / 14 days / 15 people |
| Community solo short (~2–3 min) | **13,626 generations** |
| Largest folder in every project | **TESTS — 61% of all generations** |

### What this means for you

A 4:30 film with **25 kept shots** at 65–100 generations each is **1,600–2,500 generations** —
and that excludes character-sheet lock (~800) and style tests.

**Realistic total: 2,500–3,500 generations in 24 days. Roughly 110–150 per day, every day.**

Three consequences, and the first one is the whole strategy:

1. **Fewer, longer shots is not just an aesthetic — it is the only way this ships.** 25 shots at
   100 takes each is achievable. 70 shots at 100 takes each is not. **Your preferred style is
   also your production plan.** This is the single luckiest fact about this project.
2. **Budget the tests as the work, not as overhead.** 61% of generations in real projects are
   tests. If you plan only for final shots you will be 2.5× over budget by day 8.
3. **Adopt the Week 1 / Week 2 split.** Week 1: get *every* shot present and rough — the complete
   shape of the film. Week 2: concentrate all remaining iteration on the 4–5 shots that carry the
   emotional weight. Without this split, iteration cost runs the project over before the ending
   exists.

### Folder discipline (adopt on day 1, it's free)

```
/TESTS              — style calibration, model comparisons. Biggest folder. Expected.
/FINAL KEYFRAMES    — the locked frames each shot was built from
/FINAL GENERATIONS  — selected takes
/FAILED GENERATIONS — discards, kept on purpose. Knowing what didn't work is navigation.
/scene-01 ... /scene-N
```

---

# 3. PROMPT ARCHITECTURE — the Hell Grind block scaffold

Hell Grind's prompts ran **3,000–4,000 words each**. That is not padding. The governing fact:

> **The model has no memory between generations.** If a character is not fully described in
> *every* prompt, the next shot gives them a different face and a different jacket.
> **Consistency is not a setting; it is repetition.**

### The block order

```
SCENE CONTEXT          — EXACT N CHARACTERS — NO DUPLICATES: NAME, NAME.
GEO SPATIAL LAYOUT     — the room's floor plan. Locked, pasted unchanged across every shot in the scene.
CHARACTERS             — full descriptors, verbatim, never shortened
SPATIAL LAYOUT BLOCK   — who is where THIS shot (frame-left/right, metres from landmarks)
ACTION TIMING          — 0.0–3.0s / 3.0–7.0s ... beat by beat, present tense
CHARACTER ACTING       — per character: state · want · what they hide · body rhythm · habits · what changes
AUDIO                  — voice descriptors + the line in quotes + the mix
POSITIVE LOCKS         — counted objects, scale laws, what IS in frame
STYLE                  — the Style Prefix, verbatim
QUALITY                — detail and stability requirements
[tag tail]             — Photoreal. NON-IP. 16:9. 15s. SFX only. NO CGI. Cinematic.
```

### The GEO SPATIAL LAYOUT block — the fix for teleporting characters

The most expensive early problem is characters swapping places and the camera jumping the axis.
The cure is a floor plan in a few lines — **landmarks only, no characters, no action** — written
once per scene and pasted into every shot of that scene without changes.

```
GEO SPATIAL LAYOUT (locked across every shot — pure spatial map):
— GHOST LIGHT = single bare bulb on a stand, CENTER of the bare stage floor.
— PROSCENIUM ARCH: frame-LEFT edge, 4 m from the light.
— SEATING: rows recede into blackness BEHIND camera position.
— 180° AXIS: camera ALWAYS stays house-side of the light — it NEVER crosses to the wings.
— LIGHT LOGIC: the bulb is the ONLY source. Shadows radiate outward from it in every shot.
```

Rules for the map:
- **Sides exist only from the camera.** "frame-left" — the model does not understand "to the left
  of the character."
- **Positions in metres from landmarks.** "at the light", "three metres upstage."
- **Name the axis and the line the camera never crosses.** This keeps every cut legal.
- **After every cut, re-state who stands where and where they look.** The model does not remember.
- **Give a static dialogue a corner of the room, not the whole room.** Less space = less freedom
  to get it wrong.

### The one-second opening wide

Open each scene with **~1 second of no lines and no action** — the model "photographs" the
arrangement and holds it through the following shots. Remove it and characters start swapping
places.

Two refinements: have someone say one short word ("hm") so the engine treats it as a discrete
shot; or feed **the tail of the previous clip's line** into that first second, so the two clips
glue at the seam and the performer answers in the right tone.

### Wording laws

| Law | Detail |
|---|---|
| **Present tense, short sentences** | Always |
| **Camera inside the action** | Not a separate aesthetic paragraph |
| **≤3 sentences per beat** | Overload a beat and the model smears it |
| **Positive form only** | The model ignores "does NOT fall backward" — write "falls on his stomach" |
| **Never write age** | The content filter tightens hard. Give role, clothes, action instead |
| **Physics, not adjectives** | Not "sad" — "the jaw sets and releases twice, a light exhale through the nose" |
| **Describe stillness as held tension** | "Nobody moves" freezes the frame. Write the breath |
| **Ban dictionary** | `dark` → `low key`; `jolting` → `rapid motion`. Grow it as you find words the model punishes |

### The micro-life rule

Against frozen faces in long static shots — **one visible micro-event every 1–2 seconds**: the
chest lifts, a nostril moves, a brow tenses. Plus **phased blinking**: *"one lazy blink → a quick
DOUBLE-BLINK → one HARD reset-blink."*

**This is the single most important technique for your long-take strategy.** A 4-second shot can
survive a dead face. An 18-second shot cannot. If you hold longer than everyone else, you must
also fill that time with more life than everyone else — otherwise the hold exposes the model
rather than the performance.

---

# 4. THE PAPAMICHAEL FILTER — killing the AI tells

Direct countermeasures for the artifacts your most dangerous judge will catch instantly.

| Tell | Countermeasure |
|---|---|
| **Two suns** | One named source in the GEO block, restated every prompt. *"The bulb is the ONLY source. Shadows radiate outward from it."* |
| **Sourceless glow / AI sheen** | Always name the source, its direction, its quality, its colour temperature — and what it does *not* reach |
| **Over-lighting** | Explicitly declare the dark side: *"the left half of the face falls to black; no fill"* |
| **Plastic skin** | *"Pore-level realism — vellus hair, asymmetric moles, capillary flush, pore-shadow matching on-set light"* |
| **Waxy faces** | Route close-ups to Kling v3.0; **never run an image through a model twice in full** — every pass destroys texture. Use masked point-edits instead |
| **Floaty physics** | *"Gravity and inertia respected — mass has real weight, correct contact shadows. No floating props"* |
| **Unmotivated camera** | One move per shot, and it must be justified by blocking or emphasis |
| **Dead-eye stare** | Phased blinking + clear gaze direction + micro-life every 1–2s |

### ⚠️ The film-grain trap

Do **not** trail `film grain`, `soft focus`, `imperfect focus` or `slight natural deviation` at
the end of a prompt as a general plea for realism. These are read as **rendering** instructions
and land on the *whole frame* — your subject goes soft with everything else.

> **The governing distinction: content may be imperfect; image quality must be sharp.**
> Imperfection is a subject choice, never a rendering instruction.

Legal forms:
- **As a declared look, with its stock and home:** *"Super 8MM warm grain, soft vignette"* in the
  Style Prefix
- **As a named optical event on a named element at a named moment:** *"a brief focus hunt on the
  badge before it locks"*
- **As plate matching:** *"grain matched to the reference frame"*

And for depth of field, say which plane stays sharp — `blurry background` blurs the subject too:
- *"sharp focus throughout, deep depth of field"* (wides, geography)
- *"subject in sharp focus, background falling into soft bokeh"* (portraits, dialogue)

---

# 5. CHARACTER & LOCATION CONSISTENCY

### The character sheet is three images — and one has no head

| Panel | Content |
|---|---|
| 1 | Close-up of the face, **large, 3/4 view** (not straight-on) |
| 2 | Full body, front — **HEADLESS** |
| 3 | Full body, back |

**Why headless:** on wide shots the model kept sourcing the face from the tiny blurry face on the
full-body panel. Remove that head and there is exactly one place to take the face from. This
sounds absurd and it fixed an entire class of broken shots.

**Keep the sheet deliberately boring** — neutral grey background, flat light, real skin with
visible pores, no retouch. Bake film grain or a cinematic lens into the sheet and the character
carries that look into every scene and stops reacting to new light.

### Location sheets
- **Shoot in 3/4, never frontal.** A frontal "pretty picture" becomes flat wallpaper on wides,
  and past its edges the model invents new surroundings every time.
- **Leave an anchor in every location** — a column, a lamp, a sofa — and tie staging to it.
  *"At the lamp, facing the door"* works. *"In the room"* is a lottery.
- **One light logic. One source, one shadow direction, never two suns.**
- **Reverse angles:** generate a video of the *empty* location with the camera walking slowly
  through it, screenshot the angle you need, then upscale/relight it. A full location sheet from a
  single image.

### Reference roles must be named, and location inheritance banned

The model decides for itself if you don't, and it decides wrong — copying composition instead of
face, or face instead of palette:

```
@keeper for character reference
@loc_stage for location reference — take only the space and the texture: bare boards, dust,
black void beyond. Do not use as a starting frame, do not inherit the composition, the angle,
or the grade.
```

**One dictionary of names for the whole project** — `@keeper`, `@loc_stage` — used identically in
documents, prompts, and the Elements panel.

### Voice and acting are locked descriptors, not assets

Lock every character's **register, tempo, accent, manner** in pre-production, before any dialogue
is written, and paste it verbatim every time they speak:

```
Voice: dry, worn baritone; slow, deliberate pacing; faint northern vowels;
speaks as if continuing a conversation with someone who isn't there.
```

Same for behaviour: one paragraph per character covering movement, hands, habits, eye behaviour,
and how they break under pressure. **A behaviour that's physically impossible in a scene is
transferred, not deleted** — a character who paces, once seated, doesn't calm down; the energy
moves into swaying and finger-tapping.

---

# 6. DIALOGUE

**Construction order, every time:**
`the voice and its emotion → the line in quotes → the physical action → the facial reaction`

- **Lines live only in the AUDIO section.** Not one word of speech in the action block.
- **Hard-block invented speech.** The engine adds its own "uhms," chuckles and whole phrases.
  State that everyone speaks *only* the quoted line, whoever has no line stays **completely
  silent**, and a "half-laugh" written in the action is a facial expression **with no sound**.
- **Give every non-speaking visible face a positive at-rest mouth state** — *"lips at rest, jaw
  closed, listening."* An unmarked mouth in frame is one the model may decide is talking.
- **Short lines are the risk.** A line ending well before the shot does leaves audio air the
  model fills with invented mumble. Keep lines proportionate to shot length, or add specified
  ambience.
- **Write the mix:** voices clean and close, ambience beneath, ambience dipping when someone speaks.
- **Seam trick:** open every new generation with the line that closed the previous one, so the
  emotion crosses the seam with the text.
- **Lip-sync hygiene:** trim dialogue to 3–8s, remove head/face motion tokens, lock the camera to
  static or a slow dolly-in.

---

# 7. THE ITERATION LOOP

1. **Assets first.** Do not generate a single narrative shot until every character, location and
   prop is locked and stress-tested. *This saves more money than everything else combined.*
2. **Describe everything, every time.** Verbatim, never shortened.
3. **Change exactly one line per iteration.** Rewrite a prompt fully and you lose the parts that
   worked. Multi-variable iteration makes diagnosis impossible.
4. **Give the model less freedom.** A corner instead of a room. An anchor instead of open space.
   A map instead of guesswork. One action per shot.
5. **The 10–15 rule.** If a shot hasn't come together in 10–15 iterations, **the problem is not
   the wording — simplify the shot.** Split it in two, remove an action, change the angle.
6. **Log every generation** — prompt version, what changed, verdict. Without the log you cannot
   reproduce a good shot. Use [`../log/`](../log/).

### Complex action goes at the START of the prompt

A door that wouldn't break: the character shuffled next to it and froze. The fix — **the action
opens the prompt**: *"he is ALREADY mid-swing, the door ALREADY cracking."* The approach to the
door becomes a separate shot. **States, not transitions.**

### The best-second splice

The finished film is assembled from **the best seconds of many takes**, not from whole kept takes.
One generation's opening cut to another's ending, inside a single "shot." Plan for this in the
edit — it is standard practice, not cheating.

---

# 8. THE STYLE PREFIX

One block, glued verbatim to every prompt, edited once and re-propagated everywhere. Fill this in
during pre-production and then **freeze it**:

```
Style: [4K anamorphic widescreen], [2.39:1 / 16:9]. Photoreal live-action — no 3D render,
       no game engine, no animated-film aesthetic.
Lighting: [ONE motivated source — name it, its direction, its colour, and what it does not reach.]
Color: [60:30:10] — dominant / secondary / accent. [The accent is reserved for ONE story element.]
Camera: Physical cine lens. 180° shutter motion blur. Subtle, motivated moves only.
Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush, pore-shadow
      matching on-set light.
Acting: Micro-pauses before reactions, precise eye-line, living eyes with catch-lights,
        chest rise from breathing. Characters never standing — always reacting.
Physics: Gravity and inertia respected — mass has real weight, correct contact shadows.
         No floating props.
Composition: Staged in depth — foreground, midground, background occupied in every frame.
Continuity: Characters, props and environment locked to references across every cut.
            No identity drift.
Technical: 24fps. 8K detail. No jitter, no flicker.
Audio: Diegetic dialogue and environmental SFX only. No music. No subtitles.
```

**On the audio line:** 12 of 13 harvested community productions ban generated music in-prompt and
score in post. Do the same — a generated soundtrack fights your edit, and your sound bridges
(the most important continuity tool you have) require a clean, controllable audio bed.

**One accent colour, reserved for one story element** is a strong, cheap, jury-legible choice: it
reads as design rather than default, and it gives you a visual through-line for free.

---

## Sources

- Higgsfield MCP live model catalogue, queried 2026-08-10 (durations, resolutions, reference roles)
- Higgsfield open-source **Hell Grind** production brief, via [OSideMedia/higgsfield-ai-prompt-skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill) — `HELL-GRIND.md`, `negative-constraints.md`, `production-benchmarks.md`, `higgsfield-camera/SKILL.md`, `higgsfield-shotlist-director/SKILL.md`, `global-style-prefix.md`
- [TechappleGlobal — Hell Grind open-sourced: 3,000-word prompts, physics reminders, avoiding AI sheen](https://global.techapple.com/2026/08/higgsfield-open-sources-entire-production-of-95-minute-ai-film-hell-grind-made-in-14-days-for-500k/)
- [Hell Grind — Higgsfield Originals (YouTube)](https://www.youtube.com/watch?v=t33k2tn4GpA)
