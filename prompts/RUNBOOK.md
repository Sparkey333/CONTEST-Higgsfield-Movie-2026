# RUNBOOK — every prompt, in the order you run it

Copy-paste ready. Work top to bottom. Do not skip ahead — each block depends on the one above it
being locked.

Worked for **Vantage**. To build a different film, replace the bracketed content and keep every
structural clause exactly as written.

> **Prompt sources.** The character-sheet architecture below is Higgsfield's own bundled
> `character-sheet` workflow, pulled live from their MCP server — slot order, the anti-AI realism
> engine, and the negative tail are theirs and are tuned to their models. The pipeline discipline
> around it is the Hell Grind production method. **Where they conflict, § 0 below resolves it.**

---

# § 0 — TWO CONFLICTS, RESOLVED

I found two places where Higgsfield's official workflow contradicts the Hell Grind brief. Both
matter, and neither should be silently averaged.

### Conflict 1 — age

| Source | Says |
|---|---|
| Hell Grind | **"Never write age, in any language."** The content filter tightens the moment it reads a minor |
| Higgsfield character-sheet workflow | **Specify an age band** — "young woman in her early twenties." Actively avoid babyface; enforce mature structure |

**Resolution: state an explicitly ADULT age band, and never anything else.** The Hell Grind rule
is really a rule about never letting the model read a *minor*. An explicit adult band satisfies
that *and* fixes the babyface problem Higgsfield warns about. What stays banned is any young,
ambiguous, or unstated age.

Note this applies to the **character sheet** only. In shot prompts, Hell Grind's rule stands
unmodified — give role, clothes and action, and let the locked reference carry the face.

### Conflict 2 — the headless panel

| Source | Says |
|---|---|
| Hell Grind | Front full-body panel must be **HEADLESS**, so the model can only source the face from the close-up |
| Higgsfield workflow | Split-screen: full body left, tight close-up right. Both have heads |

**Resolution: generate both, and A/B them in Stage 1.** Higgsfield's negative tail is tuned to
their models and I will not discard it on someone else's report. But the Hell Grind evidence is
specific — the model sourcing the face from the small blurry full-body head broke a whole class of
wide shots. Run the probe in § 1.4. It costs about 20 generations and settles it for the whole film.

Everything else in the two sources agrees.

---

# § 1 — STAGE 1: CALIBRATION
### ~150 generations, lowest resolution. You are buying information, not frames.

## 1.1 · Style probe

Run this **identical** prompt through each candidate model. Compare side by side. Pick the look.

```
A woman stands at a map table inside a small glass fire lookout tower at night. A single tungsten
desk lamp on the table is the only light source — warm, hard-edged, low, throwing her shadow up
and back across the ceiling. Beyond the glass the world is black. She is turned three-quarters
away from camera, one hand resting on the table edge. Deep staging: the lamp in the foreground,
the woman in the midground, the black glass behind her.

Photoreal live-action, 2.39:1 anamorphic widescreen — no 3D render, no game engine, no
animated-film aesthetic. Physical cine lens, 180° shutter. Pore-level skin realism with visible
texture and natural asymmetry. Gravity and inertia respected, correct contact shadows. Subject in
sharp focus, background falling into soft bokeh. 24fps. No text, no watermark, no logos.
```

**Run on:** Seedance 2.0 · Kling v3.0 · FLUX 3 Video · Wan 3.0
**Judge on:** does one light source govern the frame · is the skin real · does the black read as
depth or as flat nothing · does it look photographed

## 1.2 · Duration probe — **run this before the plan depends on it**

Same prompt as 1.1. Generate at your **longest planned duration**:
- FLUX 3 Video at **20s**
- Wan 3.0 at **30s**

Then extend one of them once via continuation and check the seam for identity drift and light shift.

> **If this fails, stop and re-envelope the shot plan.** Shot `6a` is a 30-second anchor take and
> the entire turn depends on it. Finding out in Stage 5 costs a week.

## 1.3 · Filter probe

Generate once with the full KEEPER descriptor (§ 2.1). You are only checking that nothing trips
content moderation — fire, smoke, isolation and distress language can all snag. Cheap now,
expensive later.

## 1.4 · The headless A/B (settles Conflict 2)

Generate the § 2.1 sheet twice — once exactly as written, once with `left panel headless, no head
on the full-body figure, head and face visible ONLY in the right-hand close-up` added to the
composition clause and `no head on left panel figure` in the negative tail.

Then take both into a **wide shot** and compare face fidelity at distance. Whichever holds the face
better is your sheet for the whole film. **Record the winner in the ledger.**

> **GATE 1** — model routing decided · longest shot generated successfully · continuation proven
> or plan restructured · no filter trips · headless question settled

---

# § 2 — STAGE 2: CHARACTER
### ~800 generations. The long pole. This is where the credits actually go.

## 2.1 · The sheet — RUN THIS FIRST

Higgsfield slot architecture, filled for KEEPER. One paragraph, comma-separated, order preserved
— image models weight earlier tokens more heavily, which is why composition and identity lead and
the quality tail trails.

**Model:** Soul Cinema or GPT Image 2 · **Aspect:** 16:9 · **Generate wide, cull hard.**

```
Split-screen character sheet composition, left side a full-body shot of the character standing
upright in a neutral straight standing pose facing the camera with both feet flat on the ground
and arms relaxed at the sides, full head-to-toe framing with the whole body and both feet visible,
right side a tight close-up chest-up portrait of the same character turned slightly
three-quarters, identical original female character on both sides, single subject only exactly one
person with only the character in frame, pure white seamless studio background, professional
character sheet presentation, a woman in her late thirties with fair weather-worn skin, an oval
face with a defined angular jawline, high flat cheekbones, a straight narrow nose, thin lips with
a natural matte finish and no gloss, mature adult bone structure and adult facial proportions,
grey-green deep-set eyes with naturally muted catchlights and no oversized specular glare in the
iris, eye colour muted rather than glowing, straight dark brows with a slight natural gap,
dark brown hair cut short and pushed back off the face, dry matte finish with no styling product,
damp at the temples, visible fine skin texture with natural pores, fine lines at the outer eyes
and across the forehead, subtle asymmetries and texture irregularities, wind-chapped colour across
the cheekbones and nose, no makeup, slight natural sheen rather than a glossy or dewy retouched
finish, no digital smoothing, no beauty filter, no AI-airbrushed look, skin completely free of
artificial glare shine or highlight blooms, matte-to-natural complexion, a pale old burn scar
across the left forearm, a compact square-shouldered athletic build with balanced proportions,
wearing a weathered olive canvas field jacket with the sleeves pushed to the elbow, a heather grey
wool shirt beneath it with the collar open, heavy dark canvas work trousers, scuffed brown leather
lace-up boots, no jewellery, no bag, natural anatomy, high-end but unretouched documentary
photography style, soft diffused studio lighting without harsh reflections, flat and even with no
cinematic grade, clean white background, 4K quality, sharp focus on skin texture detail, single
subject only, exactly one person, only the character in frame, no other people, no duplicate
figures, no mannequin, no reflections, no props, no furniture, no background objects, empty
seamless studio, left panel standing full-body head-to-toe not cropped not sitting, right panel
tight close-up not full body, no babyface, no overly youthful rounded proportions, no beauty
filter, no digital smoothing, no airbrushing, no plastic skin, no glossy skin, no text, no
watermark, no logos, no frame borders
```

### Why this prompt is shaped the way it is

- **"flat and even with no cinematic grade"** — deliberate, and it will feel wrong. A boring sheet
  is the goal. Bake a cinematic look into the reference and the character carries that look into
  every scene and **stops reacting to new light** — which kills the entire Act III fire-key idea.
- **The realism block is the anti-AI engine.** It is long because every clause kills a specific
  failure. Do not trim it.
- **"a woman in her late thirties"** — an explicit adult band, per § 0.
- **"no makeup"** — she is alone on a mountain. Also removes a whole class of AI-glam artifacts.
- **The burn scar** is her only distinguishing mark and it earns its place: a fire lookout with an
  old burn is characterisation with no dialogue.

## 2.2 · Back view

Re-run 2.1 with the composition clause swapped to:

```
Character turnaround model sheet, three consistent full-body views in a row — front view, side
profile, and back view, evenly spaced, identical original female character on all three views,
```

Keep every other slot **byte-identical**. Changing anything else here is how characters drift.

## 2.3 · State variant — `@keeper_smoke`

**Do not ask the model to "make her dirty" later.** Build it now, or the face drifts in Act III.

Take the 2.1 prompt and change **only** these clauses:

- `wind-chapped colour across the cheekbones and nose` → `soot smeared across the jaw, the neck and
  the backs of the hands, wind-chapped and raw across the cheekbones`
- `grey-green deep-set eyes with naturally muted catchlights` → `grey-green deep-set eyes,
  red-rimmed and irritated, with naturally muted catchlights`
- `dark brown hair cut short and pushed back off the face, dry matte finish` → `dark brown hair cut
  short and pushed back, damp and disordered, stuck to the temples`
- Add after the jacket: `the olive field jacket smoke-stained down the left side`

Everything else stays word for word. **One variable at a time, even here.**

## 2.4 · The three-lighting stress test — **the gate**

Take the locked sheet into three lighting setups. Same character prompt, three light clauses:

```
A · HARD SIDE — a single tungsten desk lamp at table height, frame-right, hard-edged; the left
    half of the face falls to black with no fill.

B · SOFT FRONTAL — flat overcast daylight through glass, even and shadowless, from camera.

C · NEAR DARK — the only light is distant orange firelight from frame-right at low intensity,
    rim-lighting the jaw and one cheekbone; everything else is black.
```

**Compare the three faces.** Same bone structure? Same nose? Same scar, same forearm? If the face
drifts, **the sheet is wrong — fix the sheet, do not proceed.** Every hour here saves ten in Stage 5.

## 2.5 · Lock the non-image assets

Paste into the Story Bible and never change:

```
VOICE @keeper — dry, worn alto; slow deliberate pacing; flat vowels; speaks as if continuing a
conversation with someone who is not there. She never raises her voice, including when she should.
```

```
BEHAVIOUR @keeper — economical to the point of stillness; moves only when there is a reason. The
thumb rides the transmit key even when she is not speaking. The pencil turns end over end between
reports. She reads the map with her whole body angled to it rather than turning her head. Under
pressure she does not speed up — she slows down, and the stillness stops being calm and becomes
effort. When frightened, the breath goes shallow and high in the chest while the hands stay
perfectly steady. That gap is the performance.
```

> **GATE 2** — face survives all three lighting setups · sheet assembled · `@keeper_smoke` built ·
> voice and behaviour locked · tags registered in Elements under glossary names

---

# § 3 — STAGE 3: LOCATION
### ~250 generations.

## 3.1 · Primary angle — 3/4, never frontal

**Model:** Soul Cinema / GPT Image 2 · **Aspect:** 2.39:1 or 16:9

```
The interior of a small square fire lookout tower at night, photographed from a three-quarter
angle — not square-on to any wall. Glass on all four walls. A weathered plank floor. A map table
at the centre with an Osborne firefinder mounted on it. A steel-framed cot against the back wall.
A radio set on a shelf at frame-left. A single tungsten desk lamp on the map table, mid-right, is
the only light source in the frame — warm and hard-edged, throwing shadows outward from it in
every direction, the glass reading black beyond two metres. No people in frame.

Photoreal live-action, no 3D render, no game engine. Weathered timber, dust in the air, scratched
glass. Physical cine lens, 180° shutter. Deep staging with foreground, midground and background
all occupied. Sharp focus throughout, deep depth of field. Gravity respected, correct contact
shadows. 4K. No text, no watermark, no logos, no people.
```

**Three-quarter is not a style preference.** A frontal view becomes flat wallpaper on wides, and
past its edges the model invents new surroundings every time.

## 3.2 · Reverse angles — the walkthrough trick

Rather than generating each angle separately and getting four different rooms, generate **one video
of the empty location** and harvest frames from it:

**Model:** Wan 3.0, 20–30s

```
The camera walks slowly through the interior of a small square fire lookout tower at night,
completing a smooth continuous circuit around the central map table. A single tungsten desk lamp
on the table is the only light source; shadows swing consistently as the camera moves around it.
Glass on all four walls reading black beyond two metres. Weathered plank floor, an Osborne
firefinder on the table, a steel cot against one wall, a radio set on a shelf. No people. Dust
drifting in the lamplight. Slow continuous dolly, one single move, no cuts. Photoreal, 24fps.
```

Screenshot every angle you need, then upscale and texture-improve as stills. **A full location
sheet from a single coherent space.**

## 3.3 · The GEO block — write once, paste unchanged into every shot

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

**Reference role — always ban inheritance:**

```
@loc_tower for location reference — take only the space and the texture: weathered timber, dust,
scratched glass, plank floor. Do NOT use as a starting frame. Do NOT inherit the composition, the
angle, or the grade.
```

> ⚠️ **This room is made of glass and reflections are a known failure mode.** Camera sits *inside*
> looking out or across — **never angled at a pane.** Flag every shot in the ledger that risks it.

> **GATE 3** — location holds from 3+ angles · anchor object named · one light source in every
> angle · GEO block frozen · inheritance ban written

---

# § 4 — STAGE 4: KEYFRAMES
### ~600 generations. **A still costs a tenth of a clip. Every framing decision happens here.**

For **every** shot in the ledger, generate its first frame as a **still** and lock it. Then feed
that frame to the video model as its start frame.

## Keyframe template

```
[GEO BLOCK — pasted unchanged from § 3.3]

@keeper for character reference. [KEEPER descriptor, verbatim from § 2.1 wardrobe onward]
@loc_tower for location reference — take only the space and the texture. Do NOT inherit the
composition, the angle, or the grade.

FRAME: [shot size]. KEEPER at [landmark], [n] metres from [landmark 2], facing frame-[left/right],
occupying [screen position]. Eye-line to [target].
FOREGROUND: [ ]  ·  MIDGROUND: [ ]  ·  BACKGROUND: [ ]
LIGHT: [the ONE source], from frame-[side], [quality]. [What it does NOT reach.]

Photoreal live-action, 2.39:1, physical cine lens. Pore-level skin realism. Gravity and inertia
respected, correct contact shadows. [Subject in sharp focus, background falling into soft bokeh
| sharp focus throughout, deep depth of field]. Exactly ONE lamp, never a second light source.
Single subject only, exactly one person. 4K. No text, no watermark, no logos.
```

## Worked example — keyframe for shot 1a (the cold open)

```
GEO SPATIAL LAYOUT (locked across every shot — pure spatial map):
— MAP TABLE = the centre of the room, waist height, the firefinder mounted on it.
— DESK LAMP: on the map table, MID-RIGHT relative to the table's centre.
— RADIO SET: on a shelf at frame-LEFT, 1.5 m from the table.
— COT: against the BACK wall, behind the table from camera.
— THE RIDGE: visible through the glass BEHIND the table, roughly 4 km out.
— 180° AXIS: camera ALWAYS stays on the door side of the map table.
— LIGHT LOGIC: the desk lamp is the ONLY source. Shadows radiate outward from it and the glass
  reads black beyond 2 m.

@keeper for character reference. @loc_tower for location reference — take only the space and the
texture. Do NOT inherit the composition, the angle, or the grade.

FRAME: WIDE, the whole room in frame, camera low and static at table height.
KEEPER stands at the map table, frame-CENTRE-LEFT, turned three-quarters away from camera, her
weight settled on one hip, one hand flat on the map, the other holding a radio handset loosely at
her side. Eye-line down to the map.
FOREGROUND: the desk lamp, blown slightly hot, bottom frame-right.
MIDGROUND: KEEPER and the map table.
BACKGROUND: black glass, and beyond it nothing.
LIGHT: the tungsten desk lamp, frame-right at table height, hard-edged and warm. It reaches her
hands and the near side of her face. The far side of her face falls to black with no fill. The
ceiling above her carries her shadow, thrown up and back.

Photoreal live-action, 2.39:1 anamorphic widescreen, physical cine lens, 180° shutter. Pore-level
skin realism with visible texture and natural asymmetry. Gravity and inertia respected, correct
contact shadows. Sharp focus throughout, deep depth of field. Dust drifting in the lamplight.
Exactly ONE lamp, never a second light source. One handset, one pencil, one folded map. Single
subject only, exactly one person, no other people, no duplicate figures. 4K.
No text, no watermark, no logos.
```

## The contact-sheet check — Gate 4

Lay **every** locked keyframe out in film order as one grid and look at them together:

| Check | Question |
|---|---|
| **Identity** | Is it the same person in all of them? |
| **Light** | Does one source govern every frame, from a consistent direction? |
| **Palette** | Do they belong to the same film? |
| **Rhythm** | Read the framings across the grid — does composition vary the way the ledger says? |

**This grid is the closest you get to seeing the film before you make it.** If it reads as a
coherent movie in stills, motion is execution. If it reads as a mood board, **stop** — fixing it
here costs a tenth of fixing it in Stage 5.

> **GATE 4** — every shot has a locked first frame · start+end pairs and match-cut seams have both
> · contact sheet reads as one film

---

# § 5 — STAGE 5: MOTION
### ~1,800 generations. You enter with every decision already made.

**Shot order — deliberately not chronological:**

1. **6a, the 30s turn** — the hardest shot. If it cannot be made, the film changes, and you need
   that on day one of this stage
2. **1a + 9a as one unit** — they must rhyme; generating them apart yields two shots that *nearly*
   match, which is worse than not rhyming
3. Act I → middle acts → the burst → connective tissue

**Never generate chronologically.** It spends your best energy on the opening and leaves the
ending — the thing the jury remembers — to whatever is left.

## The motion prompt

Take the locked keyframe as the **start frame**, then add only what the keyframe cannot say:
timing, performance, sound. Full scaffold is in the app's Prompt Builder.

```
[Everything from the keyframe prompt above]

ACTION TIMING
0.0–4.0s — [beat, present tense, ≤3 sentences]
4.0–9.0s — [beat]
9.0–15.0s — [beat]

CHARACTER ACTING
KEEPER — emotional state: [ ]. What she wants in this moment: [ ]. What she is hiding: [ ].
Dominant body rhythm: [ ]. Visible habits in this beat: [ ]. What changes across the shot: [ ].

MICRO-LIFE
One visible micro-event every one to two seconds — the breath lifts the chest, a nostril moves, a
brow tenses and releases. Phased blinking: one lazy blink, a quick DOUBLE-BLINK, one HARD
reset-blink. Stillness is held tension, never a freeze.

AUDIO
[ambience]. KEEPER voice (verbatim): "dry, worn alto; slow deliberate pacing; flat vowels; speaks
as if continuing a conversation with someone who is not there." Her line, and nothing else:
"[line]". Nobody else speaks. Radio voices are thin and band-limited with squelch on key-up and
key-down; her voice in the room is full and close. Voices clean, ambience beneath, ambience dips
under the line. No music.

CAMERA: [ONE move only]

Photoreal. NON-IP. 2.39:1. [n]s. SFX only. No music. NO CGI. Cinematic.
```

## The four review gates — every keep passes all four

| Gate | Question | Watch for |
|---|---|---|
| **A · Technical** | Renders clean? | Jitter, flicker, morphing limbs, warped hands |
| **B · Consistency** | Same person, place, light? | Face drift, geometry shift, shadow flip |
| **C · Photographic** | Would a naturalist DP accept this light? | Two suns, sourceless glow, plastic skin |
| **D · Dramatic** | Does the beat land? | Dead face on a long hold, no micro-life |

**Gate D is the one people skip**, because a technically clean shot feels like success. A shot can
be flawless and worthless. Ask it out loud: *did the thing that was supposed to happen happen?*

## Loop rules

- One variable per iteration, logged
- Cull at low res, commit at 4K
- Generate long, harvest short — for a 2s burst cut, generate 15s and take the best 2
- **10–15 rule:** not converged in 15 takes → **simplify the shot**, same day. Split it, remove an
  action, change the angle. This is what stops one shot eating a week
- Complex action **opens** the prompt — "already mid-turn", not "she turns"
- Assemble on the timeline the day you make each shot

---

# YOUR NEXT THREE ACTIONS

1. **Run § 1.1 and § 1.2 today.** Four models, one prompt, plus the 20s and 30s duration tests.
   About 40 generations. **The duration probe is the one that can change the plan** — do not defer it.
2. **Run § 2.1.** This is your first real spend and the start of the ~800-generation character
   block. Generate wide, cull hard, and do not proceed past the § 2.4 stress test until the face
   holds under all three lights.
3. **Log every day in the app** — generations and keeps. If the rate runs far under 1.5%, the
   problem is upstream in the assets, not in the prompt.

**Everything in § 4 and § 5 is blocked until Gates 1–3 pass.** That is the pipeline working, not
the pipeline being slow.
