# STORY BIBLE — upload-ready grounding document

**Purpose:** this is the single file you upload into any Higgsfield "Background" / "upload the full
story to prevent hallucinations" slot, and the file you paste from when writing prompts by hand in
Cinema Studio. It is the whole locked system in one place.

**Worked for `Vantage`** — the top-scoring concept on the harness. If you lock a different concept,
replace §2–§6 and keep §1 and §7–§9 exactly as they are; those sections are concept-independent.

**Export as PDF or TXT before uploading.** Keep it under 10 MB (it will be ~30 KB).

> ⚠️ **This document is grounding, not a prompt.** Never paste the whole thing into a generation
> box. Prompts are built per shot from §4–§7 using the Prompt Builder in `../app/`.

---

# 1. HARD RULES — these override any suggestion a tool makes

1. **This is not viral content.** No hooks, no retention engineering, no cut-every-three-seconds.
   Do not restructure the film for engagement.
2. **Long takes are the form.** Roughly 90% of the film runs 12–40 seconds per shot. Fast cutting
   exists in exactly one 13-second passage and nowhere else.
3. **One light source per location, named, never violated.** Every shadow in every frame resolves
   to it.
4. **Age: adult band on the character sheet, never in shot prompts.**
   - *On the sheet:* state an explicitly **adult** age band ("a woman in her late thirties").
     Higgsfield's own character-sheet workflow requires it, and it prevents the babyface drift
     their guidance warns about.
   - *In every shot prompt:* no age at all. Role, clothes, action — the locked reference carries
     the face.
   - What stays banned everywhere: young, ambiguous, or unstated age. The content filter tightens
     the moment it can read a minor. (Reconciles Hell Grind's "never write age" with the platform
     workflow — see [`../prompts/RUNBOOK.md`](../prompts/RUNBOOK.md) § 0.)
5. **Positive form only.** The model ignores "does NOT fall backward" or does the opposite. Write
   "falls on her stomach."
6. **Diegetic sound only.** No score in any generation. Music, if any, is added in post.
7. **No brand names, no real-person names, no IP.** Describe by appearance.
8. **Never run an image through a model twice in full.** Every pass destroys texture and drifts
   colour. Point-edits go on with masks, over the original.
9. **Describe everything, every time.** The model has no memory between generations. Descriptors
   are pasted verbatim, never shortened.
10. **Decide on stills, execute in motion.** A still costs roughly a tenth of a clip. Framing,
    blocking, wardrobe, light direction and composition are all settled as keyframes before any
    video is generated. By the time motion runs, the only open question is the motion.

---

# 2. THE FILM

**Title:** Vantage
**Runtime:** 4:30 (270s) · 26 shots · 2.39:1 · 24fps

**Logline:** A fire lookout, alone in a tower, keeps calling positions on the radio as the fire
that will reach her becomes the only light she has left to see by.

**The want:** to keep reporting — her coordinates are still routing crews away from a valley where
people are sleeping.

**The turn (2:20):** command tells her to evacuate. The road is already gone. She stays, and the
staying stops being duty and becomes choice.

**The cost:** the tower's electric light fails. She keeps working by the light of the thing that is
killing her.

**The last image:** the radio handset, still keyed open on the desk, the room empty, someone's
voice still answering.

### The three truths — never stated aloud, only built
1. *Surface:* a woman refuses to abandon her post.
2. *Beneath:* being useful is not the same as being saved, and she chooses useful.
3. *Underneath:* the fire is the only reason she can see her maps. What destroys you can be what
   illuminates you. **This lives entirely in the lighting change. No line of dialogue touches it.**

---

# 3. STYLE PREFIX — paste verbatim into every prompt, never edit per shot

```
Style: 4K anamorphic widescreen, 2.39:1. Photoreal live-action — no 3D render, no game engine,
       no animated-film aesthetic.
Lighting: ONE motivated source per act. ACT I–II: a single tungsten desk lamp inside the tower,
       warm, hard-edged, low; everything beyond the glass is black. ACT III: the lamp is DEAD and
       the fire is the key — flickering orange from frame-right, reaching only one side of the
       face; the other side falls to black with no fill.
Color: 60:30:10 — desaturated slate blue / warm tungsten amber / one reserved accent.
       The accent is ember-orange and belongs ONLY to the fire.
Camera: Physical cine lens. 180° shutter motion blur. Subtle motivated moves only.
       One move per shot.
Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush, pore-shadow matching
       on-set light.
Acting: Micro-pauses before reactions, precise eye-line, living eyes with catch-lights, chest rise
       from breathing. Never standing — always reacting.
Physics: Gravity and inertia respected — mass has real weight, correct contact shadows.
       Embers fall with real drift. No floating props.
Composition: Staged in depth — foreground, midground and background occupied in every frame.
Continuity: Character, props and environment locked to references across every cut.
       No identity drift.
Technical: 24fps. 8K detail. No jitter, no flicker. Subject in sharp focus.
Audio: Diegetic dialogue and environmental SFX only. No music. No subtitles.
```

**The lighting change is a plot event, not a grade.** It happens once, at 2:50, and it is the most
important photographic decision in the film. Papamichael will notice it inside ten seconds.

---

# 4. CHARACTER — paste verbatim, never shortened

```
@keeper — KEEPER. A fire lookout. Weathered olive field jacket over a grey wool shirt, sleeves
pushed to the elbow; heavy canvas trousers; scuffed boots. Short dark hair pushed back off the
face, damp at the temples. A burn scar across the left forearm, pale and old. Build: compact,
square-shouldered, economical. Posture: still, weight settled, everything held. Hands: square,
short nails, a pencil habitually turned end over end.
```

```
VOICE @keeper (paste into the audio field every time she speaks):
Dry, worn alto; slow deliberate pacing; flat vowels; speaks as if continuing a conversation with
someone who is not there. She never raises her voice, including when she should.
```

```
BEHAVIOUR @keeper (the source of truth — each scene adapts it, the core never changes):
Economical to the point of stillness. Moves only when there is a reason. The thumb rides the
transmit key even when she is not speaking. The pencil turns end over end between reports. She
reads the map with her whole body angled to it rather than turning her head. Under pressure she
does not speed up — she slows down, and the stillness stops being calm and becomes effort. When
she is frightened, the breath goes shallow and high in the chest while the hands stay perfectly
steady. That gap is the performance.
```

**States built up front — never ask the model to change her mid-project:**
- `@keeper` — clean, Act I
- `@keeper_smoke` — soot on the jaw and neck, hair damp, eyes red-rimmed, Act III

**Character sheet construction.** Built from Higgsfield's own `character-sheet` workflow — split
screen, full body standing left, tight chest-up close-up right, pure white seamless studio
background, flat even light, **no cinematic grade baked in**. The full prompt is in
[`../prompts/RUNBOOK.md`](../prompts/RUNBOOK.md) § 2.1.

**The headless question is open and gets settled by probe, not by opinion.** Hell Grind requires
the front full-body panel be headless so the model can only source the face from the close-up;
Higgsfield's workflow keeps both heads. Run the A/B in RUNBOOK § 1.4 — about 20 generations — and
record the winner here before Stage 4:

> **Headless A/B result:** ☐ not yet run · winner: ______

**Why the sheet must be boring:** bake film grain or a cinematic lens into the reference and the
character carries that look into every scene and **stops reacting to new light** — which would
destroy the Act III fire-key change that is the whole photographic idea of this film.

---

# 5. LOCATION

```
@loc_tower — for location reference. Take only the space and the texture: a small square fire
lookout tower, glass on all four walls, plank floor, a map table at the centre, a wood-framed
Osborne firefinder, a steel-framed cot against the back wall, a radio set on a shelf. Weathered
timber, dust, scratched glass. Do NOT use as a starting frame. Do NOT inherit the composition,
the angle, or the grade.
```

## GEO SPATIAL LAYOUT — locked, pasted unchanged into every shot

```
GEO SPATIAL LAYOUT (locked across every shot — pure spatial map):
— MAP TABLE = the centre of the room, waist height, the firefinder mounted on it.
— DESK LAMP: on the map table, MID-RIGHT relative to the table's centre.
— RADIO SET: on a shelf at frame-LEFT, 1.5 m from the table.
— COT: against the BACK wall, behind the table from camera.
— DOOR + LADDER HATCH: floor, frame-RIGHT rear corner.
— THE RIDGE: visible through the glass BEHIND the table, roughly 4 km out.
— 180° AXIS: camera ALWAYS stays on the door side of the map table — it NEVER crosses to the
  window wall.
— LIGHT LOGIC (ACT I–II): the desk lamp is the ONLY source. Shadows radiate outward from it and
  the glass reads black beyond 2 m.
— LIGHT LOGIC (ACT III): the lamp is DEAD. The fire on the ridge is the ONLY source, entering
  through the glass from frame-RIGHT. Shadows fall away from it, long and moving.
```

**Never shoot toward the glass at an angle.** Camera sits *inside* the tower looking out or across.
Reflections are a known failure mode and this room is made of them.

---

# 6. THE SHOT PLAN

26 shots, 270s. Full editable ledger lives in [`../log/SHOT-LEDGER.md`](../log/SHOT-LEDGER.md) and
in the app.

| Act | Time | Shots | Strategy |
|---|---|---|---|
| Cold open | 0:00–0:25 | 1 × 25s | Loaded stillness. One anchor take, no cut |
| Act I | 0:25–1:20 | 4 | Establish want + space. 10–18s each |
| Act II-a | 1:20–2:20 | 5 | The world resists. 8–16s each |
| **The Turn** | 2:20–2:50 | 1 × 30s | **Anchor take. No cuts. The face carries it** |
| Act II-b | 2:50–3:35 | 10 | **The only burst** — 7 cuts in 13s, then hold |
| Act III | 3:35–4:20 | 4 | The cost, paid. Slowest passage |
| Last image | 4:20–4:30 | 1 × 10s | Recontextualised opening. No music sting |

**Object through-line — the radio handset.** First: routine, held loosely. Middle: gripped white.
Last: keyed open on an empty desk. Its final appearance must reverse its first.

---

# 7. SHOT PROMPT SCAFFOLD

Every generation follows this block order. The Prompt Builder in `../app/` emits it filled.

```
SCENE CONTEXT      — EXACT N CHARACTERS — NO DUPLICATES: KEEPER.
GEO SPATIAL LAYOUT — §5, pasted unchanged
CHARACTERS         — §4 descriptor, verbatim
SPATIAL LAYOUT     — where she is THIS shot, in metres from landmarks, frame-left/right
ACTION TIMING      — 0.0–4.0s / 4.0–9.0s … present tense, ≤3 sentences per beat
CHARACTER ACTING   — state · want · what she hides · body rhythm · habits · what changes
MICRO-LIFE         — one visible micro-event every 1–2s; phased blinking
AUDIO              — voice descriptor + the quoted line + the mix
POSITIVE LOCKS     — counted objects, what IS in frame
STYLE              — §3, verbatim
QUALITY            — 8K, pore-level, no jitter, face stays its reference at every distance
[tag tail]         — Photoreal. NON-IP. 2.39:1. {n}s. SFX only. No music. NO CGI. Cinematic.
```

### Micro-life is mandatory on every shot over 12 seconds
One visible micro-event every one to two seconds — the breath lifts the chest, a nostril moves, a
brow tenses and releases. Phased blinking: *one lazy blink → a quick DOUBLE-BLINK → one HARD
reset-blink.* **Stillness is written as held tension, never as a freeze** — "nobody moves" freezes
the frame.

A 4-second shot survives a dead face. An 18-second shot does not. Holding longer than everyone
else means filling that time with more life than everyone else.

### Emotion is physics, never adjectives
Not "afraid." Write: *the jaw sets and releases twice; a light exhale through the nose; the breath
goes shallow and high while the hands stay steady.*

---

# 8. DIALOGUE RULES

Construction order, every time:
`the voice and its emotion → the line in quotes → the physical action → the facial reaction`

- **Lines live only in the AUDIO block.** Not one word of speech in the action block.
- **Hard-block invented speech.** The engine adds its own "uhms" and whole phrases. State that she
  speaks *only* the quoted line and that any half-breath written in the action is a facial
  expression **with no sound**.
- **Every visible non-speaking face gets a positive at-rest mouth state** — "lips at rest, jaw
  closed, listening." An unmarked mouth is one the model may decide is talking.
- **Short lines are the risk** — a line ending well before the shot does leaves audio air the model
  fills with mumble. Keep lines proportionate, or specify ambience to fill.
- **Seam trick:** open each new generation with the line that closed the previous one, so emotion
  crosses the seam with the text.
- **Radio voices are processed:** thin, band-limited, with squelch on key-up and key-down. Her
  voice in the room is full and close. The contrast is the whole sound design.

---

# 9. BAN DICTIONARY — words the model punishes

| Instead of | Write |
|---|---|
| dark | low key |
| jolting | rapid motion |
| film grain *(trailing, unattached)* | name the stock and its home, or drop it |
| soft focus / dreamy | "a brief focus hunt on the dial before it locks" |
| blurry background | "subject in sharp focus, background falling into soft bokeh" |
| sad / angry / afraid | the muscle work that produces it |
| nobody moves | "she holds, and the held breath is visible" |

Grow this list as you find more. Log every substitution.

### High-risk shots in this film — flag before generating
- **Glass reflections** — the tower is glass on four sides. Camera inside, never angled at the pane.
- **Fire scale drift** — lock it with a scale law and the ridge as a fixed landmark in every prompt.
- **Ember physics** — generate in slow motion, speed up in post.
- **The lighting change** — generate Act III shots as their own batch so the fire key stays
  consistent across all of them.

---

## Provenance

Built from [`../docs/03-HIGGSFIELD-PLAYBOOK.md`](../docs/03-HIGGSFIELD-PLAYBOOK.md) (Hell Grind
block scaffold, Papamichael filter, consistency rules),
[`../docs/02-DIRECTING-DOCTRINE.md`](../docs/02-DIRECTING-DOCTRINE.md) (rhythm, layered truth) and
[`../docs/05-STORY-CONCEPTS.md`](../docs/05-STORY-CONCEPTS.md) § A.
