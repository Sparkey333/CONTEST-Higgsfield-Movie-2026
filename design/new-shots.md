# The generation run — 1080p, paired, in order

Rebuilt 14 Sep against **what you are actually generating with**, not against this repo's older notes.
Reading your latest 16 video generations changed four things:

| | Was in this file | Is now |
| --- | --- | --- |
| Model | `cinematic_studio_video` (v2) | **`cinematic_studio_video_4_0`** — what all 16 of your last renders used |
| Ceiling | 12s | **16s** — you have already run 14s and 16s on it |
| Resolution | 720p | **1080p** — you have been on 720p (1344×576); 1080p is the ask and v4.0 takes it |
| Ships / courtyard | `prop_enemy_ships`, `loc_loc_starsun_v3_courtyard` | **`twelve-ships`**, **`courtyard-of-worlds`** — the ones you switched to |

The two element swaps are now applied everywhere: **34 references across the Director's Bible**,
plus `recreate-prompts.md` and `shot-element-ids.json`. The full picture is in `cast-latest.json`.

**Every prompt below: `cinematic_studio_video_4_0` · 21:9 · 1080p.** Duration and audio are stated per shot.

---

# PAIR 1 — the two the film is missing dramatically

Run these first. If nothing else gets made, make these.

## NEW-1 · "The mind divides" · **16s** · audio **OFF** · goes between S13 and S14

```
Extreme slow motion, camera held wide and low over a storm ocean, no cuts and no camera move at all. ORIANE (@[char_oriane_v3_battle](30b9bf89-3fcf-4544-b110-a74aeccbb7c1)) hangs in the air at the centre of frame, arms loose at her sides, barefoot, head tilted slightly back. A ring of sixteen translucent warping lenses opens at arm's reach around her and immediately doubles — thirty-two, sixty-four, then more than two hundred — until she is a silhouette seen through layered refraction (@[fx-segmented-mind](99737c53-c69a-43a8-af60-8a29fcffa072)). Her eyes are closed. Her face is not strained: it is concentration and open joy. Her lips move, forming words, and no sound comes out.

Behind and around her, spread across miles of black water, the enormous armoured leviathans (@[prop_leviathan_v1](b353d96f-721a-4ea9-98e4-6adea64b4e76)) come apart in total silence. Lightning runs along every seam in the dead-coral plating (@[leviathan-plating](cb3d6271-76d8-4a73-90c5-5165a4bde473)) and the flesh lifts cleanly away from the bone beneath in long sheets, unwinding outward like paper in wind, leaving pale skeletons standing upright in the air for a full second before they too disperse. No blood. No gore. No fire, no explosion, no shockwave — the separation is clean and slow and looks like something being undone rather than destroyed.

The whole frame is at peace. Nothing accelerates. Hold to the last frame. 21:9, near-black storm ocean and sky with lightning and the pale unwinding sheets as the only bright shapes in frame, extreme contrast, photoreal, anamorphic. No score, no effect, no sound at all.

REFERENCES — attach before generating: @[char_oriane_v3_battle](30b9bf89-3fcf-4544-b110-a74aeccbb7c1); @[fx-segmented-mind](99737c53-c69a-43a8-af60-8a29fcffa072); @[prop_leviathan_v1](b353d96f-721a-4ea9-98e4-6adea64b4e76); @[leviathan-plating](cb3d6271-76d8-4a73-90c5-5165a4bde473); @[plate-ocean-dark](398d0b9f-e0c6-4a98-b75d-5a727b604632); @[fx-hollow](89a74d62-615e-4e52-b745-8bb8ceab1628).
```

**Why 16s and not 12.** The shot is one continuous decelerating unwind and it has three beats to get through —
the lenses multiplying, the silent words, the flesh leaving the bone. At 12s the third beat is clipped.
Sixteen is the ceiling and this is the shot to spend it on.

**Audio off is deliberate.** S13 is fifteen seconds of specified silence and this sits inside it. Seeing her
speak and hearing nothing is stronger than any line. Every one of your last 16 renders had audio on — this is
the one place to turn it off.

## NEW-2 · "The mound" · **16s** · audio **ON** · goes between S20 and S21

```
Locked-off wide from the shoreline, static, no camera shake at any point, low red sun directly behind the subject line. A hill-sized mass of compacted sand, rock and dead coral hangs above open water, turning slowly (@[fx-floating-mountain](9ca46e73-1df6-41c3-8ace-7fd4c324850f)). It does not drift — it MOVES, tracking laterally across the frame with the deliberate, heavy, side-to-side undulation of a snake finding its line, the whole mass flexing as it goes. It crosses the sky above twelve tall wooden sailing ships (@[twelve-ships](c661f844-e65e-4eb0-b9ff-076b9edf1746)) and stops directly over them. Everything hangs.

Then it falls — not dropping, DRIVEN, straight down and far faster than gravity, the whole mass separating into a million particles on the way and punching the sea white. The ships are simply gone under it. Great waves crash outward toward camera and break at the bottom of frame.

The camera does not react, does not pan, does not shake, and does not cut. Everything is backlit and rimmed, thick dust and smoke, crimson and rust and deep shadow with no cool tone anywhere (@[plate-bombardment](389aa7b5-5de8-495f-b899-b588e51c7ab8)). No glow, no beams, no energy, no visible force, nobody gesturing. 21:9, photoreal, immense scale, anamorphic.

REFERENCES — attach before generating: @[fx-floating-mountain](9ca46e73-1df6-41c3-8ace-7fd4c324850f); @[twelve-ships](c661f844-e65e-4eb0-b9ff-076b9edf1746); @[plate-bombardment](389aa7b5-5de8-495f-b899-b588e51c7ab8); @[keeper-kneel](d1faba5a-bf3e-49bf-886d-e632823f4836); @[iron-spears](e1f4220b-7d1f-45bf-a6d1-4358a09061aa).
```

**Why 16s.** The lateral crossing is what sells the snake, and it needs roughly eight seconds of travel before
the stop reads as a stop. Then the hang, then the drive. Twelve seconds forces the crossing into three seconds
and it reads as drift.

---

# PAIR 2 — the two transitions

## NEW-3 · "Transition A" · **8s** · audio **OFF** · goes between S5 and S6

```
Macro, locked, no camera move. A single faceted bead of clear ice fills the frame (@[frozen-tear](58952962-9241-4a19-aedc-031a2374e484)), lying on a floor of pure light. It rotates very slowly until one facet squares up to camera and fills the whole frame. Inside that facet the interior is a moving, living blue.

Hold. Then, without a cut and without the frame ever changing shape or colour, the blue inside the facet BECOMES open ocean seen from above — the same blue, the same movement, the same brightness, now water to the horizon under a bruised violet sky. The caustics inside the ice become sunlight on waves. Nothing else changes. The match is on shape and colour alone and it must be seamless enough that a viewer cannot name the moment it happened.

21:9, photoreal, anamorphic, extreme contrast. Warm gold on the ice at the start, fully desaturated storm ocean by the end. No sound.

REFERENCES — attach before generating: @[frozen-tear](58952962-9241-4a19-aedc-031a2374e484); @[plate-sun](03dbcec8-c65f-482c-8c11-58782c673c93); @[plate-ocean-dark](398d0b9f-e0c6-4a98-b75d-5a727b604632); @[courtyard-of-worlds](afc4fc5d-86be-4072-927c-f890966feaca).
```

**Stays at 8s.** A match cut that lingers stops being a match cut. This is the one shot in the run that would
be made worse by more time.

## NEW-4 · "Transition B" · **12s** · audio **ON** · goes between S14 and S15

```
Extreme wide, camera high above the curve of a blue-green world (@[machira-orbit](e7b2e80e-59db-44be-a654-7534a042e2c8)), looking down and along the horizon line. A single green-white streak crosses the frame left to right, very fast, very small, trailing a thin line of green light behind it (@[founding-stone](45c4d884-b89b-4694-af1f-e06eef545e30)). It is the only moving thing and the only warm colour in a cold frame.

The camera descends with it — through the exosphere, through cloud, the light going from black to violet to a deep warm orange — and the streak stays exactly the same size in frame the whole way down. It crosses in front of a low setting sun and, as the sky fills with golden hour, the streak thins, fades, and is gone.

The last two seconds are an empty tropical sunset sky over flat calm water, with iridescent sand just entering the bottom of frame (@[plate-island](527aca60-04e0-4f86-8f4d-8c1f46c0f776)). Nobody in frame. Nothing explained.

21:9, photoreal, anamorphic. Cold and clinical at the top, warm and peaceful at the bottom, one continuous grade between them. No cuts. Sound falls away to wind.

REFERENCES — attach before generating: @[founding-stone](45c4d884-b89b-4694-af1f-e06eef545e30); @[machira-orbit](e7b2e80e-59db-44be-a654-7534a042e2c8); @[plate-island](527aca60-04e0-4f86-8f4d-8c1f46c0f776); @[nacre-beach](db228a3f-576d-4fd0-91c1-1f756d85a4fd).
```

**Raised from 8s to 12s.** It is a descent through four distinct light states — black, violet, orange, golden.
Eight seconds gives each of them two seconds, which reads as a dissolve rather than a fall.

---

# PAIR 3 — the ships shots, with the element you switched to

Both were pointing at the retired `prop_enemy_ships`. They now point at `twelve-ships`.
Full text for both is in `recreate-prompts.md`, already updated — the change is the reference, not the prose.

- **S17 · Twelve ships · 10s · audio OFF** — locked-off wide, the boys drop flat, the ships open fire, the camera refuses to react
- **S18 · The Temple does not answer · 10s · audio ON** — three shots in one generation, the temple taking hits and not reacting

---

# PAIR 4 — the two that changed identity

- **S5 · "Tomorrow" — the tear freezes · 14s + a 4s macro · audio split** — the continuity audit found Caedom
  as the *mortal* sheet in all four takes of this shot while he is `caedom-ascended` everywhere else in the film.
  That is the single worst identity break in the cut and it is in the film's fifth shot.
- **S20 · The mountain · 14s · audio ON** — exists only as a C-lane chroma take.

---

## Where they sit in the cut

```
… S12  S13  [NEW-1]  S14  [NEW-4]  S15  S16  S17  S18  S19  S20  [NEW-2]  S21  S22  S23
                                  and [NEW-3] between S5 and S6
```

Four new shots at 8–16s adds about **52 seconds**. The film goes to roughly **5:52** — fine, the rules set a
3:00 floor and no ceiling.

## Two notes on the run

**1080p costs more than 720p and the difference is worth it here.** You have 540 credits. Every render you
have made so far is 1344×576, which is 0.77 megapixels — below 720p in *height*. Finishing at 1080p scope
means these four new shots need no upscale at all, while the older ones need a 1.9×. Generating the new ones
natively at 1080p is the cheapest quality you will buy today.

**Turn start/end frames on.** Only 2 of your last 16 generations used them, and both of those are the 14s and
16s pairs — the longest shots, which is exactly right. NEW-1 and NEW-2 are also 16s. If F-frames exist for
them, chain them; a 16-second shot is long enough to drift without anchors at both ends.
