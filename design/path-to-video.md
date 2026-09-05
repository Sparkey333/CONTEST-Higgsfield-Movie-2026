# Path to video — the delta from where the production stands to a compliant film

Written Sep 5, revised the same afternoon once the deadline and the day's generations were confirmed. This is
a delta against the bible's 34-step RUN, not a rewrite of it. Step numbers below are RUN step numbers. Where
this file and the bible disagree on the account's state, this file is current.

---

## 1. Where we are

**Submissions close Sep 14 at 11:59 PM UTC** — 4:59 PM Pacific — and it is Saturday Sep 5. That is nine days.
The bible recorded Sep 3 from the festival's first revised timeline; the festival page now says Sep 14, the
second move. Check it again before every gate.

Of the 34 RUN steps: steps 1–3, 5, 11, 13 and 14 are done; **steps 12 and 15 finished on Sep 5** — every one of
the 42 asset sheets now has an A-lane generation in the account, and every one of the 26 that were empty that
morning (four plates, six locations, seven props and creatures, four effects, five Turned variants) has a clean
production-name element handle. Steps 4 and 7–10 are done to the point of Gate A: five Souls exist
(`alder`, `wren`, `oriane` ready; `caedom-mortal` and `caedom-ascended` training), and the five A lanes that had
been rendered by two engines were re-rendered on one. Step 16, Gate A, is the next thing to attempt and can be
attempted today. **Steps 17–34 have not begun: 0 of 39 anchors exist, 0 of 23 shots exist.**

The film is image-first — every shot is a motion pass between two anchor stills — so the nine days divide
cleanly: roughly three for the anchors (Stages 6–7 below), three for the motion pass (Stage 8), two for
finish and delivery (Stage 9), and one of margin that is not to be spent. That is tight and it is possible. It
is not possible if the anchors slip, because everything downstream is a move between two of them.

One thing this file does not do: it does not tell you the film can be submitted on the 14th. It tells you
the order that makes it possible. Whether each gate holds is decided at the gate.

---

## 2. The order that does not waste generations

The dependency chain, with the RUN step each stage corresponds to, the tool, the generation count, the
approval step and the gate it must clear. Batch size is 12 throughout for `generate_image_batch`; identity
work is approved as **batch of 4, select 1**; world work is **one image per sheet, lane A only** — no B, C or
D lanes until Gate A, exactly as RUN 15 says.

### Stage 1 — Plates (RUN 14) · done Sep 5
- **What:** PLATE-mv1-light-A, PLATE-mv2-light-A, PLATE-mv3-light-A, PLATE-mv3b-A. No characters.
- **Tool:** `generate_image_batch`, nano_banana_pro, 21:9, 4K. Already in batch 1.
- **Count:** 4 (part of batch 1's 12).
- **Approval:** judge at thumbnail size (lumen). mv2 must contain no warm colour at all. mv2 and mv3 get the
  dark-ground / high-local-contrast bias (section 6); mv1 does not.
- **Then:** `show_reference_elements create` — one clean handle per plate (`plate-sun`, `plate-ocean`,
  `plate-island`, `plate-bombardment`). The API cannot rename or delete, so the name is final on creation.
- **Why first:** every location inherits its key from a plate. A plate made late invalidates every location
  made before it.

### Stage 2 — Locations (RUN 15) · done Sep 5
- **What:** courtyard, Nacre Beach, the corals and abyss, the white temple, Keeper's Isle, Machira from orbit.
- **Tool:** `generate_image_batch`, nano_banana_pro, 21:9, with the matching plate attached as an image
  reference so the light is inherited rather than re-described. Batch 1 carries these; regenerate any
  location whose plate is rejected at Stage 1.
- **Count:** 6. **Approval:** one per sheet; reject anything whose key direction disagrees with its plate.
- **Then:** `show_reference_elements create` for each (`courtyard`, `nacre-beach`, `bloom`, `temple`,
  `keepers-isle`, `machira-orbit`).

### Stage 3 — Props and creatures (RUN 15) · done Sep 5
- **What:** the Founding Stone, the aura shell (batch 1), coral plating, the whole leviathan, the iron spears,
  the twelve ships, the frozen tear.
- **Tool:** `generate_image_batch`, nano_banana_pro, plain backgrounds on props, full 21:9. Attach the
  location a prop is held in (leviathan → plate-ocean; ships → nacre-beach + plate-bombardment; tear →
  courtyard).
- **Count:** 7. **Approval:** one per sheet. The leviathan is the one to be strict about — S10 locks identity
  to this image and there is no other reference for it.
- **Then:** handles for `stone`, `shell`, `coral`, `leviathan`, `ore`, `ships`, `tear`.

### Stage 4 — Effects and Turned variants (RUN 12 + 15) · done Sep 5
- **What:** FX-hollow, FX-mind, FX-mountain, FX-strike-blast; then the five missing Turned domain sheets.
- **Tool:** `generate_image_batch`, nano_banana_pro. The hollow sheet defines the hollow as a lens, not a
  glow — attach the aura rule sheet as reference so it is decided once. Turned variants attach the `turned`
  handle and the attunement ladder so the three ranks match the group sheet.
- **Count:** 9. **Approval:** one per sheet. Turned: no armour, no uniforms, no glowing eyes.
- **Then:** handles for the four effects. The Turned variants do not need handles; they are modifiers.

### Stage 5 — Single-model re-renders and Soul training (RUN 4, 7, 8, 9, 10) · done Sep 5, two Souls still training
- **Re-render:** Alder, Wren, Caedom mortal, Threadwright, Turned-Water. Each A lane is currently split
  across two engines. **Why single-model matters:** a Soul trained on two engines' renderings of one face
  learns the average of two faces, and drift is then baked into the identity that 39 anchors inherit — the
  exact failure Gate A exists to catch. Re-render each on the engine that already holds its majority
  (nano_banana_2 for the four characters; the Turned family all on nano_banana_2 so the ranks match).
- **Tool:** `generate_image_batch`, batch of 4 per character, select the frames that hold the same face
  (typically 3–4 of 4). Then the height check: Alder and Wren side by side, equal height, age only in the
  face — reject any Wren frame where he is shorter. 20 images total.
- **Caedom ascended:** lane A is in batch 1 (previously the only character with no A lane; the live
  `caedom-ascended` handle was built from lane B as a stopgap and must be replaced — create
  `caedom-ascended-a` since the old handle cannot be deleted from the API).
- **Train Souls:** `show_characters train` for **Caedom** (from the ascended A lane plus the re-rendered
  mortal A lane, so the bone structure carries across both forms), **Alder** and **Wren** (separate Souls,
  never one element for two people). **Oriane** already has a Soul — the one named Caedom; rename it
  `oriane-soul` in the web UI, do not retrain. **Threadwright and Keepers do not need Souls**: the
  Threadwright's face is never shown and the Keepers are an order, not a face; their existing handles serve.
- **Why now:** Soul training is the one stage with wall-clock latency that cannot be parallelised away.
  Start it the moment the re-renders are selected, while Stages 2–4 are still generating.
- **Gate A (RUN 16):** everything from Stages 1–5 on one screen, in the canvas. Look for a face that moved.
  Nothing in Stage 6 begins before this holds.

### Stage 6 — 39 anchors in film order (RUN 17, 18, 19)
- **Tool:** `generate_image_batch`, 21:9. Two engines by frame type:
  - Anchors with a face at medium or closer (F04–F08, F15, F21, F34, F35, F36): **soul_2 with the
    character's soul_id**, the movement's plate attached. Verify soul_2 offers 21:9 first; if it caps at
    16:9, generate identity at 16:9 and extend to 21:9 with `outpaint_image` rather than cropping.
  - Everything else: **nano_banana_pro** with plate + location + element handles as references.
- **Count:** 39 anchors × 4 = 156 images in 13 batches of 12; F35 gets 8–12 (the bible's "largest batch and
  longest look"). Select 1 per anchor. Shared joins (F02, F11, F12, F17, F30, B01, B02) are generated once
  and the same media id serves both shots.
- **Order:** section 3, exactly.
- **Gate B (RUN 20):** all 39 on one contact sheet, read left to right twice. Drift here costs an image.

### Stage 7 — Stills reel and Gate C (RUN 21, 22)
- **Tool:** an NLE (or the Cinema Studio timeline): 21:9 at 24 fps, each anchor held for its shot's `d`,
  dialogue read aloud, temp sound. No generation. Watch all five minutes without stopping.
- **Gate C:** runtime (300 s), shot order and shot count freeze. After this, a structural change costs
  video, not images. This is where the splice findings in section 4 (S4, S5, S22 durations) must be resolved.

### Stage 8 — Motion pass (RUN 23–27)
- **Cheap pass (RUN 23), compressed:** the bible runs all 23 at budget tier. On this timeline run it only
  on the shots that carry a seam that can fail — S1/S2, S6, S7, S8, S10, S11, S12, S18, S19, S20 — at
  kling2_6 or veo3_1_lite, 1080p, 21:9. About 11 clips. You are testing whether each A-frame can reach its
  B-frame, not quality.
- **Gate D (RUN 24):** any draft frame that beats its anchor is extracted and promoted.
- **Final (RUN 25–27):** `generate_video_batch`, model per the SHOTS array (section 4), strict shot order
  inside each movement, 4K where the model allows. Budget two attempts per shot; S20 gets six. A shot that
  fails three times leaves the queue for the escalation ladder and does not block the shots behind it.
  Roughly 50–60 video generations. Check `balance` before starting the final pass and reserve at least half
  the remaining credits for it — the images can move to the canvas's unlimited allowance if credits thin;
  the videos mostly cannot.

### Stage 9 — Finish, lock, deliver (RUN 28–34)
- **Deflicker → upscale (2K then 4K, `upscale_video` aigc preset) → grade**, in that order. Three grades:
  gold-on-black, cold blue-grey, golden hour. S2 (720p) needs the most lift.
- **Gate E:** picture lock. No further generation.
- **Sound:** made anywhere, then every file uploaded into the submission project. S13 stays silent.
- **Watermark and packshot** in Cinema Studio; **rights sweep** of every prompt for surviving novel terms;
  end card "Adapted from the novel *Anchor Stone*"; **public post** checked in a logged-out browser; verify
  every generation is still in the project; submit.

---

## 3. Anchors — the 39 FRAMES, joins, bridges and the exact generation order

**Frame roles.** Single: 27. Shared joins (one image is shot N's last frame and shot N+1's first): **F02**
(S1/S2), **F11** (S6/S7), **F12** (S7/S8), **F17** (S10/S11), **F30** (S19/S20). Bridge frames (hidden cut
through near-black): **B01** (S11/S12, the leviathan's flank), **B02** (S18/S19, the dust wall). Match pairs
(two different images designed together): **F09/F10** (the tear's facet becomes the ocean — 108 years),
**F22/F23** (the Stone's streak — a day and three thousand miles). Two frames carry a `look` override:
F19, F20 and F22 replace the Movement II storm look with the orbital vacuum look (no rain, no spray, no
haze, hard terminator) — the composed prompt must not inherit "sea spray on the lens" from LOOK[2].

**Generation order.** Three sessions, one per lighting plate, in the order below. Every anchor attaches its
movement's plate; frames that depend on a previous frame attach that frame as an image reference — the
model cannot see "the previous frame" unless you hand it over.

**Session I — the Sun (plate-sun, courtyard, oriane-soul, caedom Soul, tear). 11 anchors.**
1. **F02** — courtyard resolving out of glare, no figures. First, because every other Sun frame inherits
   this room, and because it needs no Soul, so it can start before Caedom finishes training. The glare must
   be genuinely blinding at centre: the S1→S2 extension seam lives inside it.
2. **F01** — near-black, plasma at the bottom edge. Trivial; generate it so the from-scratch rule is met.
3. **F03** — two figures from behind, worlds on stems. Handles are enough (backs), F02 attached.
4. **F04** — reverse two-shot, 40 mm. Both Souls. Same room, different lens — attach F03.
5. **F05** — Oriane turning her head. oriane-soul, F04 attached.
6. **F06** — locked MCU, 75 mm, lit from below. oriane-soul. Then immediately:
7. **F07** — identical framing, wet eyes. Generate with **F06 attached as reference** and the prompt
   restating lens, height and framing in full. "Identical to F06" specifies nothing on its own.
8. **F08** — Caedom's hands on her face. Both Souls.
9. **F36** — Caedom alone at the courtyard edge. Made here, under this plate, with F03 attached so he
   stands where two people stood — not in the Movement III session weeks later.
10. **F09** — macro on the frozen tear, one facet, interior a moving blue. `tear` handle. Then, before
    anything else in Movement II:
11. **F37** — the tear as one point of light on the luminous floor; rhymes with F01. F02 attached.

**Session II — the Ocean (plate-ocean, oriane-soul, oriane-ascended, oriane-damaged, turned,
threadwright, leviathan, coral, ore, lev-rider, machira-orbit). 14 anchors.**
12. **F10** — open storm ocean at the exact scale, colour and shape of F09's facet. **F09 attached.** This
    pair is made in the pairing, not in the edit.
13. **F11** (shared S6/S7) — Oriane running, camera beside, world streaked. Greaves on.
14. **F12** (shared S7/S8) — flat against the grey ice wall, hair spread, unhurt. F11 attached for
    costume and damage state.
15. **F13** — the wall collapsing into seawater.
16. **F14** — over the Threadwright's shoulder, quarry small and distant. No warmth anywhere; this frame is
    graded from the dark side. `threadwright` handle, face never shown.
17. **F15** — her fingers mid-gesture, marionettes answering. F14 attached.
18. **F16** — the leviathan erupting, camera low. `leviathan` + `coral` handles.
19. **F17** (shared S10/S11) — Oriane tiny between the jaws. From here on she is **barefoot**
    (oriane-ascended) — the greaves coming off is the escalation.
20. **B01** (bridge) — the flank filling frame to genuinely near-black. Reject anything at 70 % obscured.
21. **F18** — she launches forward, lightning circulating in the shell. oriane-damaged marks from here.
22. **F19** — orbital, the vortex eye open. Orbital look override, `machira-orbit` handle.
23. **F20** — the eye beginning to close. **F19 attached**; same framing.
24. **F21** — Oriane falling upward, fractures filling with light. oriane-soul + damaged.
25. **F22** — empty sky, planetary curvature, the green streak. Orbital look; F19 attached for the limb.

**Session III — the Island (plate-island, then plate-bombardment from F27 onward, alder Soul, wren Soul,
keeper, keeper-kneel, temple, keepers-isle, nacre-beach, ships, fx-mountain). 14 anchors.**
26. **F23** — Nacre Beach at dawn, the streak's residue as a low star. **F22 attached** for the streak's
    exact colour. Warm for the first time in three minutes.
27. **F24** — two brothers stopped at the tide line, small in a very wide frame. Both Souls at this size are
    optional; handles suffice. Height check applies.
28. **F25** — underwater reef, two silhouettes crossing far above. `bloom` handle.
29. **F26** — the shelf edge and the black past it. Never resolve what is down there.
30. **F27** — brothers staggering out of the surf. **Switch to plate-bombardment.**
31. **F28** — boys flat on the sand, twelve ships in the same frame, backlit red. F27 attached; `ships`.
32. **F29** — the white temple taking hits, no reaction. `temple`.
33. **B02** (bridge) — the dust wall, brown shadow, no legible shapes.
34. **F30** (shared S19/S20) — two lines of Keepers kneeling, shot falling around them. `keeper-kneel`.
35. **F31** — the mountain's particles falling, ships going under, heads still bowed. `fx-mountain`, F30
    attached.
36. **F32** — flat open ocean, nothing left. Plate-island again (aftermath).
37. **F33** — temple doors closing, garden replanted.
38. **F34** — both brothers in the beach grass, Wren mid-sentence, Alder already elsewhere. Both Souls.
39. **F35** — Alder in close-up at the end of the push, one dark cloud out of focus behind him. alder
    Soul. **Batch of 8–12, the longest look in the film.** If any single image is worth moving to the canvas
    and iterating on unlimited, it is this one.

**Lumen's judgement — which anchors can be held for their full shot duration.** This matters twice:
first as the stills reel at Gate C, and second as the degraded fallback if a shot's motion pass fails on
deadline. A frame survives a hold when the eye has somewhere to go after second six.

- **Holds for its full duration as a still (with at most a 2–3 % NLE push):** F01 (near-black — it *is* a
  hold), F19 and F20 (orbital scale moves slowly; a slow push on the still reads as orbit — S13 is the
  film's best degraded-fallback shot), F26 (withholding is the job; stillness helps), F32 (designed to be
  almost boring), F37 (last frame, into black), B01 and B02 (they hold for one beat each anyway).
- **Holds for 6–8 s, not 12–14:** F24 and F28 (Movement III's locked wides — the grammar is a static
  witness, so a still is on-grammar, but the ships in F28 must move eventually), F02 (the glare carries
  three or four seconds of "resolving", no more), F23 (a dawn can hold while the star fades).
- **Cannot be held at all:** F06/F07 (the shot's only content is a face changing over fourteen seconds — a
  frozen face reads as a freeze), F11 (speed is the content), F16/F17 (the leviathan must erupt), F30/F31
  (the mountain is the miracle; a still of it is a painting), F35 (the push *is* the thesis).
- **Composition warning for the long locked shots:** S4 (F06→F07, 14 s locked) and S15 (F23→F24, 12 s
  locked) need something inside the frame that moves — refraction crawling on the crystal in S4, the low
  star fading in S15 — stated in the video prompt, not assumed.

---

## 4. Motion pass — per shot

Durations sum correctly: Movement I 80 s, II 118 s, III 102 s, total 300 s. Ceilings are from MATRIX.
"Seam" is the join *out* of the shot.

| Shot | d | Model (ceiling) | Camera | Anchors | Seam type out | Risk |
|---|---:|---|---|---|---|---|
| S1 | 16 | wan3_0 (30 s) | vertical crane out of flame | F01→F02 | continuous, forward extension into S2 inside the glare | **High** — cross-model extension (wan → seedance_2_5), 1080p→720p inside a "no cut" oner |
| S2 | 18 | seedance_2_5 video_extension (30 s, 720p) | forward drift, chest height | F02→F03 | first cut (S3), on her head turn | Medium — 720p; must be deflicked and upscaled |
| S3 | 14 | cinematic_studio_3_0 (15 s) | reverse, slow lateral dolly | F04→F05 | honest cut, motivated (POV) | Low |
| S4 | 14 | minimax_hailuo 10 s **+ 4 s hold** or cinematic_studio_3_0 14 s | locked | F06→F07 | none | **Fix at Gate C** — a 4 s freeze of a face is a freeze; use cinematic_studio_3_0 at 14 s with both frames |
| S5 | 18 | cinematic_studio_3_0 15 s **+ 3 s ext** | push past them to the floor, into macro | F08→F09 | match cut F09/F10 | **Fix at Gate C** — cinematic_studio_3_0 has no extension listed in MATRIX; either 15 s and give 3 s to S4/S3, or take S5 on wan3_0/flux_3_video (both 20 s+, both frames, refs) |
| S6 | 14 | cinematic_studio_video_v2 12 s + 2 s ext | travelling beside her | F10→F11 | shared F11 into S7 | Medium — extension must land on F11 |
| S7 | 12 | kling3_0 (15 s) start+end | one swing from beside to behind | F11→F12 | shared F12 into S8 | Medium |
| S8 | 14 | cinematic_studio_video_v2 12 s + 2 s ext, speedramp | crane up the face, ramp on the kill | F12→F13 | motivated cut (POV) into S9 | Medium — ramp + extension |
| S9 | 12 | veo3_1 8 s + 4 s ext, or cinematic_studio_3_0 12 s | Threadwright POV | F14→F15 | honest cut into S10 | Low — no end frame needed, veo has none; cut is legal here |
| S10 | 16 | seedance_2_0 15 s + ext, refs | low, wide, held | F16→F17 | shared F17 into S11 | Medium — identity lock via `leviathan` reference; extension must end on F17 |
| S11 | 10 | kling3_0 motion_control from a driving clip | lateral track along the flank | F17→B01 | **bridge**: flank to near-black | **High** — motion_control may not accept an end frame; if it cannot reach B01, cut honestly on the darkest rendered frame |
| S12 | 12 | cinematic_studio_video_v2, speedramp slowmo | pull off the black | B01→F18 | hard cut to scale (S13) | Low |
| S13 | 15 | wan3_0, **generate_audio: false** | orbital, silent | F19→F20 | hard cut back to intimate | Low — and the best still-fallback in the film |
| S14 | 13 | cinematic_studio_3_0 | intimate, then hold the empty frame two beats | F21→F22 | match F22/F23 (the streak) | Medium — the empty-frame hold must be in the prompt |
| S15 | 12 | cinematic_studio_3_0 | locked-off wide | F23→F24 | straight cut, time passing | Low |
| S16 | 12 | kling2_6 10 s + ext or seedance_2_0 12 s (water physics) | held underwater wide | F25→F26 | cut on the tremor | Low |
| S17 | 10 | cinematic_studio_3_0, genre epic | static wide, violence enters | F27→F28 | cut to the temple (revelation) | Low |
| S18 | 10 | cinematic_studio_video_v2 multi_shots + multi_prompt | three angles inside one gen | F29→B02 | **bridge**: dust wall | Medium — internal cut placement is the model's; B02 as end frame |
| S19 | 10 | seedance_2_0, start_image from dust | emerge, walk out, stand | B02→F30 | shared F30 into S20 | Low |
| S20 | 14 | wan3_0, enable_thinking | one unbroken wide, slow rise | F30→F31 | straight cut on stillness | **Highest attempt count** — six budgeted; cannot be rescued in the edit |
| S21 | 8 | veo3_1_lite or cinematic_studio_3_0 | locked wide, aftermath | F32→F33 | straight cut | Low |
| S22 | 14 | veo3_1 8 s + ext, or minimax_hailuo 10 s | the only push-in in the movement | F34→F35 | V.O. transition; hard cut to the Sun | **Fix at Gate C** — hailuo caps at 10 s (4 s short), veo has no end frame and its extension is unspecified; a push that stops early fails the thesis. Use cinematic_studio_3_0 at 14 s with F34/F35, or wan3_0 |
| S23 | 12 | cinematic_studio_3_0 | crane away from the tear, to black | F36→F37 | end | Low |

**Splice's judgement — where the seams are riskiest, worst first.**
1. **S11→S12 (B01).** A hidden cut needs genuine near-black. The tool named for S11 (motion_control) is the
   one least likely to hit a specified end state. Plan the honest cut now: if the rendered S11 does not reach
   near-black, cut on its darkest frame and open S12 on B01 as generated — an honest cut beats a 70 %
   failed hide.
2. **S1→S2.** Extending a wan3_0 1080p clip with seedance_2_5 at 720p inside the film's opening oner puts a
   resolution step exactly where the film promises no cut. Two mitigations: make the glare in F02 truly
   blinding so the step hides in white; and consider generating S1+S2 as **one 30 s wan3_0 generation**
   (F01→F03, 34 s specced, so trim 2 s each from S1 and S2 — a 4 s change that is free before Gate C and
   costs two videos after it).
3. **The chain S6→S7→S8 (F11, F12).** Three models, two shared frames, two extensions. Rule: **chain from
   the rendered frame, not the anchor.** S7's start frame is the *extracted last frame of the rendered S6*,
   and S8's start is the extracted last frame of S7. The anchor is the target; the render is the truth.
4. **S10→S11 (F17).** Seedance extension has to end on F17 and kling motion_control has to start there,
   with Oriane changing to barefoot/damaged in the same frame. Same rule: extract, do not re-use the still.
5. **S18→S19 (B02).** Multi-shot generation with an end frame; dust must go to brown shadow with no legible
   shape. If cinematic_studio_video_v2 will not hold the end frame through internal cuts, generate S18 as
   two 5 s shots instead — the source text already wrote this cut.
6. **F09/F10 and F22/F23.** Not seams in motion but seams in design; they are won or lost at Stage 6, which
   is why F10 is generated with F09 attached and F23 with F22 attached.
7. **Three silent shortfalls to close at Gate C:** S4 (10 + 4 s hold), S5 (15 + 3 s extension on a model
   with no extension), S22 (10 s model, 14 s shot). Each has a same-duration alternative on
   cinematic_studio_3_0 (S4, S22) or wan3_0/flux_3_video (S5) — pick before the timing lock, because after
   it the fix is a re-render.

---

## 5. What the canvas is for vs what the API is for

The two surfaces cannot see each other. The API cannot see what is on the canvas, cannot rename or delete
an element or a Soul, cannot apply the watermark or packshot, and cannot submit. The canvas cannot run
twelve prompts in one call, wait on a batch, or hand a media id to the next stage without a human copying
it. The analysis side of this project has also never looked at a single image (asset-ranks.md is explicit
about that) — every selection so far has been structural, not visual.

**The API does everything countable and orderable:**
- `generate_image_batch` for all 26 world sheets, the 5 re-renders, and the 39 anchors in the order in
  section 3 — batches of 12, references attached by media id or handle.
- `show_reference_elements create` for every plate, location, prop and effect the moment its A lane is
  selected. Name it right the first time (`<thing>` or `<thing>-<state>`, lowercase, hyphens, no version
  numbers); a wrong name is permanent from this side.
- `show_characters train` for Caedom, Alder and Wren from the single-model A lanes.
- `generate_video_batch` for the motion pass, `jobs_wait` then one `show_generation_by_ids`, `upscale_video`
  for the finish, `virality_predictor` (free) on every social cut before it posts.
- `balance` before each stage that bills.

**The canvas (and Cinema Studio) does everything that needs eyes or a hand:**
- **Selecting 1 of 4.** Every approval step in section 2 happens here. The API generates the four; the
  human picks the one and reports the media id back.
- **Arranging plate beside location** so the light is inherited by proximity when a location reference is
  weak.
- **Unlimited iteration on the images that decide the film:** F35 above all, then F06/F07, F17 and the
  F09/F10 pair. Do not spend API credits on the tenth variant of F35; that is what the canvas's allowance
  is for.
- **The renames and deletes the API cannot do:** Soul `Caedom` → `oriane-soul`; the off-doctrine element
  names listed in element-cleanup.md; deletion of the superseded `_v1…_v5` handles so nothing generates
  from the wrong one.
- **Cinema Studio:** the stills reel at Gate C, the assembly at Gate E, watermark and packshot, the
  submission itself.

**The recommended split, in one line:** the API generates and creates; the user selects, names, arranges and
submits; the anchors' selected media ids are the only thing that has to cross from one side to the other,
and they cross once, at the end of each anchor session.

---

## 6. Apply the virality finding

The measured result (nine clips, three models, three aspect ratios, no exception): high-contrast images on a
dark ground score 51–56, diffuse bright fields 47–49, and the mind-wandering proxy orders the whole table on
its own. Model choice does not separate the set; luminance does. Movement I is the Sun and scored worst
four out of four.

**Where the dark-ground bias goes:**
- **plate-ocean (l2)** and everything under it: F10–F22, the storm, the leviathan, the lightning river.
  Push the ground dark, put the contrast in the crystal and the lightning. F14 (the Threadwright's POV, "no
  warmth anywhere") and F19/F20/F22 (the orbital frames, absolutely black sky above the limb) are already
  in the winning regime by design.
- **plate-island (l3)** and **plate-bombardment (mv3b):** low sun, long shadows, backlit red at F28, dust
  to brown shadow at B02, the abyss at F26. Golden hour is not a bright field if the shadows are long.
- **Movement III's underwater frames (F25, F26)** — the coral-reef flyover was the third-best clip in the
  set with no subject in frame at all.

**Where it must not go:**
- **Movement I — plate-sun and F01–F09, F36, F37.** A sustained bright oner on the Sun is the film's opening
  argument and the festival cut keeps it. Do not spend a single extra pass trying to make the Sun perform on
  a metric it structurally cannot win. **Never cut a social post from S1–S5 or S23.**
- F23 (Nacre Beach at dawn, "warm for the first time in three minutes") is warm on purpose; its job is
  contrast with the 118 seconds before it, not a score.

**The two rules for social cuts** (the film keeps its own order; these apply to posts only):
1. **Open on the payoff frame, then earn it back.** Every tested clip peaked on its final second inside a
   hook window that only counts the first three. A social cut opens on the shot's *last* frame — F17 for
   the leviathan, F31 for the mountain, F20 for the vortex — then plays the shot.
2. **Vertical 3:4 at 9–10 s.** The vertical 10 s cut was the only clip whose visual response rose over time
   instead of decaying from frame one. Reframe from the 21:9 master with `reframe` to 3:4, 9–10 s, and run
   each candidate through `virality_predictor` (free, ≤16 s, two concurrent) before posting; rank on
   dmn_mean first, attention_mean second when the headline numbers tie.

Candidates in order: S10 (leviathan), S20 (mountain), S13 (vortex, silent — post it silent), S12 (lightning
river), S16 (the abyss). All dark-ground, all Movement II or III, none of them containing a face that the
finished film could later contradict.

---

## 7. One-screen checklist

**Done on Sep 5 — do not redo:**
- [x] 4 plates, 6 locations, 7 props/creatures, 4 effects, 5 Turned variants generated · 27 clean handles created
- [x] Alder, Wren, Caedom-mortal, Threadwright, Turned-Water re-rendered on one engine (request Pro; it lands on the `nano_banana_2` label)
- [x] Souls trained: `alder`, `wren`, `oriane` ready · `caedom-mortal`, `caedom-ascended` training
- [ ] In the web UI: delete the five `-1` junk handles Soul training created · swap `caedom-ascended` to its new A sheet · delete the Soul named `Caedom` (it is Oriane) · clear the 23 legacy novel-vocabulary handles

**The film — nine days, Sep 5 to Sep 14:**
- [ ] **Look at every sheet generated on Sep 5.** They were made one per asset and never seen by the person who ordered them; approve or regenerate each in the canvas before anything is built on it
- [ ] Alder/Wren height check side by side
- [ ] **Gate A** — every reference on one screen; no face moved
- [ ] Anchors Session I (F02 first, F09 last-but-one, F36/F37 here) · Session II (F10 with F09 attached;
      barefoot from F17; B01 truly black) · Session III (plate-bombardment from F27; F23 with F22 attached;
      F35 batch of 8–12)
- [ ] **Gate B** — 39 on one contact sheet, read twice
- [ ] Stills reel at real durations · resolve S4, S5, S22 model/duration · decide S1+S2 as one 30 s gen or not
- [ ] **Gate C** — 300 s, 23 shots, order frozen
- [ ] Cheap pass on the 11 seam-bearing shots only · **Gate D** — promote any better frame
- [ ] Final pass in strict shot order per movement; chain from rendered last frames, not stills; S13 audio
      off; S20 six attempts; three fails → escalation ladder
- [ ] Deflicker → upscale (2K, 4K, aigc) → grade (three grades) · **Gate E**
- [ ] Sound (S13 silent) → upload every audio file into the project
- [ ] Prompt sweep for novel terms · end card "Adapted from the novel *Anchor Stone*"
- [ ] Watermark + packshot · public post (logged-out check) · verify project · **submit before Sep 14, 11:59 PM UTC, with a day in hand**
- [ ] Social cuts from S10/S20/S13/S12/S16 only: open on payoff frame, 3:4, 9–10 s, predictor-tested
