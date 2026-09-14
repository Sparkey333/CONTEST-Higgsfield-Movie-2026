# Recreate prompts — continuity pass on the 13 Sep renders

Read from the account's generation history, not from memory. Each prompt is the bible's A lane with the continuity fix applied and the operator-only tail removed, so it pastes straight into Cinema Studio. Attach exactly the `@[name](id)` references named in the prompt.


## S5 · “Tomorrow” — the tear freezes · 18s

**What broke:** Caedom was char_caedom_v2_human — the MORTAL form — in all four takes; he is caedom-ascended in S3 and S23 either side of it. Two takes also had Oriane as char_oriane_v1_human. The centre of Movement I has both leads changing bodies.

**Fix:** Same prompt, correct identities: caedom-ascended and char_oriane_v2_sun. Generate on minimax_h3 with the chosen S5 voice takes as audio_references, 14s, model audio OFF; the tear macro is a second short clip.

```
Continuous 18-second move. Open on CAEDOM (@[caedom-ascended](b86fb7ed-7b58-440b-a807-0831705e47a5)) holding ORIANE (@[char_oriane_v2_sun](217d50aa-b89f-4723-bb4d-d1725f0f12e6))'s face in both hands, tender, unhurried. He releases her and turns to look down past the courtyard's edge at a blue-green planet hanging below. The camera pushes slowly past both of them toward the planet, then tilts down to the floor of light. A single tear falls from frame above, strikes the luminous floor, and freezes instantly into a faceted bead of ice. Camera continues down into macro on the bead until one facet fills the frame and its interior is a moving blue. Hold. Sound drops away to nothing in the final two seconds. DIALOGUE — spoken in English, natural pace, silence around it, no score under it (on camera until the tear; 6 words): ORIANE: "When will you release him?" CAEDOM: "Tomorrow.". AUDIO — generated FROM the voice, and SPLIT. minimax_h3 tops out at fifteen seconds and this shot is eighteen. Generate the two-shot and the push at 14s with the chosen S5 takes as audio_references, then the tear macro as its own short generation — there are no faces in the last four seconds, so the split lands where nothing is speaking. Model audio generation OFF on the first half. REFERENCES — attach these before generating, do not describe them in words: @[plate-sun](03dbcec8-c65f-482c-8c11-58782c673c93) for key direction, colour and contrast; @[char_oriane_v2_sun](217d50aa-b89f-4723-bb4d-d1725f0f12e6) and @[caedom-ascended](b86fb7ed-7b58-440b-a807-0831705e47a5) for identity; @[frozen-tear](58952962-9241-4a19-aedc-031a2374e484) for design.
```


## S14 · The Stone leaves her · 13s

**What broke:** Oriane was char_oriane_v3 (2e8a246e) — a third Oriane element, different from the char_oriane_v3_battle used in S6–S12. Close, intimate, upside-down on her face: the one Movement II shot where a different reference shows.

**Fix:** Same prompt with char_oriane_v3_battle.

```
Close, intimate, back at her level, upside-down as ORIANE (@[char_oriane_v3_battle](30b9bf89-3fcf-4544-b110-a74aeccbb7c1)) falls upward out of the atmosphere. The crystal of her body is fracturing and the fractures are filling with light. The Founding Stone (@[founding-stone](45c4d884-b89b-4694-af1f-e06eef545e30)), green-white the size of a fist emerges from her chest — not torn out, released. She holds it a moment, says something we do not hear, and throws it. It leaves as a green streak across the curve of the world and is gone. She looks up toward the star. Then her body comes apart into particles that fall upward and disperse. HOLD THE EMPTY FRAME for the last two and a half seconds — sky, curvature, nothing else. Sound returns only as wind. REFERENCES — attach these before generating, do not describe them in words: @[plate-ocean-dark](398d0b9f-e0c6-4a98-b75d-5a727b604632) for key direction, colour and contrast; @[char_oriane_v3_battle](30b9bf89-3fcf-4544-b110-a74aeccbb7c1) for identity; @[machira-orbit](e7b2e80e-59db-44be-a654-7534a042e2c8), @[founding-stone](45c4d884-b89b-4694-af1f-e06eef545e30) for design.
```


## S9 · The threadwright's eyes · 12s

**What broke:** Only takes are the C chroma lane. Movement II is specified fully desaturated; the Threadwright reveal in full colour breaks the movement's key.

**Fix:** Lane A.

```
Over-the-shoulder from behind THE THREADWRIGHT (@[threadwright](00c70af8-e0f1-4eda-90ed-c7ff87afc5f5)) in dark rippling cloth, hovering above the storm ocean, watching. Far ahead of her and small in frame, her quarry — ORIANE (@[char_oriane_v3_battle](30b9bf89-3fcf-4544-b110-a74aeccbb7c1)) — runs across the water — distant, fast, hard to hold in the eye. The Threadwright's hands move in small precise gestures at her sides, and every one of the Turned (@[prop_the-turned-ones_v1](3328bfdf-2fd5-4e9b-a821-9b2487d39529)) in the middle distance moves as her fingers move: marionettes on invisible string. She is not hurrying. She is enjoying it. Her face is never fully shown. Long lens, heavy compression, rain in the foreground out of focus. Cold blue-grey grade, no warmth anywhere in frame. REFERENCES — attach these before generating, do not describe them in words: @[plate-ocean-dark](398d0b9f-e0c6-4a98-b75d-5a727b604632) for key direction, colour and contrast; @[threadwright](00c70af8-e0f1-4eda-90ed-c7ff87afc5f5), @[prop_the-turned-ones_v1](3328bfdf-2fd5-4e9b-a821-9b2487d39529) for design; @[char_oriane_v3_battle](30b9bf89-3fcf-4544-b110-a74aeccbb7c1) for identity.
```


## S12 · The lightning river · 12s

**What broke:** Only takes are the C chroma lane, on the lightning-river beat. It will not grade-match S11 or S13.

**Fix:** Lane A.

```
Pull back off a wall of dark wet hide into open air. Extreme slow motion. A bolt of lightning connects with ORIANE (@[char_oriane_v3_battle](30b9bf89-3fcf-4544-b110-a74aeccbb7c1)) and does not pass through her — it is caught in a shell of bent space around her body and forced to circulate, coursing around her limbs like a river held in a channel. She is lit from inside. She smiles, and arcs of electricity spark between her teeth. Two of the Turned (@[prop_the-turned-ones_v1](3328bfdf-2fd5-4e9b-a821-9b2487d39529)) in front of her register the sight and are visibly afraid. Time returns to normal in the final second as she launches at them. Photoreal, volumetric, blue-white key on a black storm. REFERENCES — attach these before generating, do not describe them in words: @[plate-ocean-dark](398d0b9f-e0c6-4a98-b75d-5a727b604632) for key direction, colour and contrast; @[char_oriane_v3_battle](30b9bf89-3fcf-4544-b110-a74aeccbb7c1) for identity; @[leviathan-plating](cb3d6271-76d8-4a73-90c5-5165a4bde473), @[aura-shell](b81752ae-2bda-4a57-ba83-02244d1dbeb4) for design; @[fx-hollow](89a74d62-615e-4e52-b745-8bb8ceab1628) for the hollow — a lens, never a glow; @[fx-kill-beat](dda1e304-4f0b-4e44-aca4-db472c0e18a6) for the strike and blast; @[prop_the-turned-ones_v1](3328bfdf-2fd5-4e9b-a821-9b2487d39529) for the pursuers.
```


## S17 · Twelve ships · 10s

**What broke:** Only takes are the C chroma lane. Bombardment plate, and it sits between two A-lane shots.

**Fix:** Lane A.

```
Locked-off wide, static, no camera shake at any point. ALDER (@[kai_alder_v1](6b8fe17b-3956-43b2-9cfb-4d6903e88781)) and WREN (@[kai_wren_v1](e6a2888e-b4a0-49ed-ab89-281d93e06880)), soaked, stagger up a beach out of the surf, arms out, exhausted and happy. The ground jolts — sand leaps from the surface. They drop flat. Behind them and to the left, entering the static frame from the sea, twelve tall wooden sailing ships with billowing sails advance in line and open fire. Metal shot tears overhead. The camera does not react, does not pan, does not shake. Setting sun behind the ships, everything backlit and hazed red. The stillness of the frame against the violence inside it is the entire point. DIALOGUE — none. This shot plays silent by choice; its lines were cut on Sep 9 because the picture carries the beat alone. REFERENCES — attach these before generating, do not describe them in words: @[plate-bombardment](389aa7b5-5de8-495f-b899-b588e51c7ab8) for key direction, colour and contrast; @[kai_alder_v1](6b8fe17b-3956-43b2-9cfb-4d6903e88781) and @[kai_wren_v1](e6a2888e-b4a0-49ed-ab89-281d93e06880) for identity; @[nacre-beach](db228a3f-576d-4fd0-91c1-1f756d85a4fd), @[loc_sector_isle_v1](a8daccbb-0819-4de2-915a-d72a0374bfdc), @[prop_enemy_ships](43344a12-1cd2-4dd2-893a-76c6c72ee37f) for design.
```


## S18 · The Temple does not answer · 10s

**What broke:** Only takes are the C chroma lane.

**Fix:** Lane A, with multi_shots on for the three internal angles.

```
Three shots inside one generation, world and light locked across all three. [1] Wide: the white temple (@[white-temple](1ed6a464-2d1e-46b2-8840-e90c2175ebb8)) taking direct hits, sand and torn flowers raining down its face, lit blood-red by the setting sun. It does not react. [2] Closer, low: the temple doors — shut. Debris strikes and falls away. Still shut. [3] Wide from behind the temple looking out to sea: twelve ships firing into a structure that is simply standing there. No people in any of the three. No movement except falling debris and drifting smoke. The refusal to respond is the subject. REFERENCES — attach these before generating, do not describe them in words: @[plate-bombardment](389aa7b5-5de8-495f-b899-b588e51c7ab8) for key direction, colour and contrast; @[white-temple](1ed6a464-2d1e-46b2-8840-e90c2175ebb8), @[prop_enemy_ships](43344a12-1cd2-4dd2-893a-76c6c72ee37f) for design; @[white-temple](1ed6a464-2d1e-46b2-8840-e90c2175ebb8) for the temple.
```


## S20 · The mountain · 14s

**What broke:** Only takes are the C chroma lane, on the largest image in the film. Keepers and mountain will pop out of the grade against S19 and S21.

**Fix:** Lane A.

```
One continuous wide shot, fourteen seconds, no cuts, camera rising very slowly and doing nothing else. Two lines of Keepers (@[keeper-kneel](d1faba5a-bf3e-49bf-886d-e632823f4836)) stand facing the sea. Every projectile in the air stops and hangs suspended. The sand of the beach lifts and converges on the floating metal. Only now, with it already happening, do the standing figures take a knee in unison and bow their heads — not to cause it, but to refuse to watch it. Rock and dead coral erupt out of the ocean and ascend to join the mass. It merges into a single floating mountain the size of a hill, turning slowly. It glides out over the twelve ships and stops above them. Figures leap from the decks into the water. Then the mountain comes apart into a million particles and they fall — faster than gravity should allow — pounding the ships down under the surface. From the kneel onward the Keepers never raise their heads. Photoreal, immense, unhurried. REFERENCES — attach these before generating, do not describe them in words: @[plate-bombardment](389aa7b5-5de8-495f-b899-b588e51c7ab8) for key direction, colour and contrast; @[keeper-kneel](d1faba5a-bf3e-49bf-886d-e632823f4836), @[keeper](8a3838aa-6fe1-485d-881c-4c14dfbe492e), @[fx-floating-mountain](9ca46e73-1df6-41c3-8ace-7fd4c324850f) for design; @[iron-spears](e1f4220b-7d1f-45bf-a6d1-4358a09061aa) for the ore — torn from rock, never forged; @[keeper-kneel](d1faba5a-bf3e-49bf-886d-e632823f4836) for the kneeling lines.
```


## Selections — no regeneration, just choose the right take

| Shot | Use | Discard | Why |
|---|---|---|---|
| S10 | `1971bd66` / `bab3224f` (leviathan) | `4abb698e` / `b34943d9` | The discarded pair attached `prop_dragon_v1_dead`. It is a dragon, not the leviathan, and S11 uses the leviathan. |
| S13 | `4779332a` / `820907db` (orbital) | `e4b5998b` / `416f5f35` (sea level) | The spec is orbital, silent, looking down. The sea-level version is a different shot. |
| S22 | `6b0d0fac` / `d35da4ef` (12s, lane A) | `4bb7a3e9` / `4896c8e3` (lane C) | Chroma pass is not for the film. |
| S5 | none — regenerate | all four | See above. |

## Audio — applies to every clip

Every one of the 54 renders was made with `generate_audio` on. **Mute the clip's own audio track on all of them**
in the edit and lay in the voice takes, the score and the sound design. The four speaking shots had their lip
movement driven by the model's invented audio, not by your takes, so they will not match. S4 is the one where
that shows — a held close-up — and `sync_so` with the chosen S4 take as `input_audio` is the cheap fix.

## The structural finding

None of the 54 renders used a start or end frame. `medias` is empty on every one. Each shot was generated from
prompt and elements alone, so no seam is frame-matched: every cut is a hard cut between two independently
generated clips. That is the continuity engine the whole bible was built around, and it was bypassed. Not
recoverable today. Mitigate in the edit by cutting on the seams that were designed to hide a cut — the flank
going to black at S11→S12, the dust wall at S19, the glare at S1→S2 — and by letting the grade do the work
of making 23 clips read as one film.
