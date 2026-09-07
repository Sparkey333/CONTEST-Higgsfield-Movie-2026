# Canvas skeletons — one board per scene, one anchor per frame

Written Sep 6. This is the layout for the Higgsfield canvas, scene by scene, with the anchor frame that starts and ends every shot already generated and waiting in the account's library. It follows the bible's shot order (23 shots, 39 frames, 300 s), not the screenplay's intercut order; where a screenplay slug line covers a scene it is quoted so the two can be read against each other.

**What exists as of today.** All 39 anchors were generated on Sep 6 as a *skeleton pass*: one image each, `nano_banana_pro` at 21:9 and 2k, the movement's plate and the scene's handles attached by element id, and the previous frame attached as an image reference wherever section 3 of `path-to-video.md` says a frame depends on another. They were made in four dependency rounds (24, then 11, then 3, then 1) so that no frame was generated before the frame it inherits from. One frame (F31) failed on the platform's side and passed unchanged on the second submission. **Nobody has looked at any of them.** They are the placeholders each board is laid out from, not the frames the film is cut from — Gate A still comes first, and the batch-of-four, select-one pass in `path-to-video.md` Stage 6 replaces each one, with `soul_2` for any face at medium or closer.

## How a board is laid out

- **One canvas per lighting plate.** Every frame on a canvas inherits the same plate and the same look line. A board that mixes plates is a board where the light drifts.
- **Top row: the plate, then the location, then the people and props** — dragged from the Elements panel by handle, never described. The handles are listed under each canvas below.
- **Then the anchors in shot order, left to right.** Each shot is a start→end pair. A *shared* frame is one image that ends shot N and starts shot N+1; it sits between them once. A *bridge* frame is a near-black hidden cut. A *match* pair is two different images designed together (F09/F10, F22/F23).
- **Chain from the rendered last frame, never from the anchor still.** When shot N has been generated, extract its last frame and use that as shot N+1's start. The anchor is the target; the render is the truth.
- **Spend the canvas's unlimited allowance on the frames that decide the film:** F35 first, then F06/F07, F17, and the F09/F10 pair. The API made one of each; the canvas makes the tenth.
- **The Souls are for the identity pass.** The skeleton was made from handles so that two people can share a frame. When a placeholder is replaced, any face at medium or closer is regenerated with `soul_2` and the character's Soul (`oriane`, `alder`, `wren`, `caedom-ascended`, `caedom-before`).

## Canvas I — The Sun

**Plate:** `plate-sun`. **Board handles:** `plate-sun`, `courtyard-of-worlds`, `oriane`, `caedom-ascended-1`, `frozen-tear`, `aura-shell`. **Souls for the identity pass:** `oriane`, `caedom-ascended`.

### Scene 1 · Rise, and the courtyard of worlds

*Screenplay: EXT. THE SUN - COURTYARD OF WORLDS.*

| Shot | s | Model (from the bible) | Start anchor | End anchor | Note |
|---|---:|---|---|---|---|
| **S1** Rise out of the fire | 16 | wan3_0 · 16s · 1080p · 21:9 | **F01**<br>`30403126-ae0d-4926-8df8-fcf14da302ef` | **F02** · shared<br>`0e3fbd76-dd81-4105-81c6-6078dacde732` | High risk: cross-model extension into S2 inside a no-cut oner; make the F02 glare truly blinding, or generate S1+S2 as one 30 s wan3_0 clip. |
| **S2** The courtyard of worlds | 18 | seedance_2_5 · video_extension forward · 18s | **F02** · shared<br>`0e3fbd76-dd81-4105-81c6-6078dacde732` | **F03**<br>`06d8c310-c4ba-459d-aef7-b18430ca781c` |  |

Frames on this board, with what each was generated from:

- **F01** (S1 A) — `plate-sun`
- **F02** (S1 B / S2 A) — `plate-sun`, `courtyard-of-worlds`
- **F03** (S2 B) — `plate-sun`, `courtyard-of-worlds`, `oriane`, `caedom-ascended-1` · previous frame **F02** attached

### Scene 2 · “There must be risk” / “He's your brother”

| Shot | s | Model (from the bible) | Start anchor | End anchor | Note |
|---|---:|---|---|---|---|
| **S3** “There must be risk” | 14 | cinematic_studio_3_0 · 14s · genre drama · audio on | **F04**<br>`e4b97ee1-b609-412e-a266-1d6bf0d06b56` | **F05**<br>`9e06d580-23d9-41c9-872e-56545049f2c2` |  |
| **S4** “He's your brother” | 14 | minimax_hailuo (2.3) · 10s + hold, or cinematic_studio_3_0 · 14s | **F06**<br>`39a6cecc-45a6-43ac-b5f9-954a3ac4fbf5` | **F07**<br>`ca631c86-1c40-4551-8107-3514c38e7bca` | Gate C fix: 10 s model + 4 s hold is a freeze of a face. Use cinematic_studio_3_0 at 14 s with both frames. |

Frames on this board, with what each was generated from:

- **F04** (S3 A) — `plate-sun`, `courtyard-of-worlds`, `oriane`, `caedom-ascended-1` · previous frame **F03** attached
- **F05** (S3 B) — `plate-sun`, `oriane` · previous frame **F04** attached
- **F06** (S4 A) — `plate-sun`, `oriane`
- **F07** (S4 B) — `plate-sun`, `oriane` · previous frame **F06** attached

### Scene 3 · “Tomorrow”, the tear freezes

| Shot | s | Model (from the bible) | Start anchor | End anchor | Note |
|---|---:|---|---|---|---|
| **S5** “Tomorrow” — the tear freezes | 18 | cinematic_studio_3_0 · 15s · 4K + 3s extension | **F08**<br>`9293bd47-4e48-4eb4-a098-02f60c506932` | **F09** · match<br>`5a726527-40f7-4405-9859-d56715418592` | Gate C fix: no extension listed for cinematic_studio_3_0. Take 15 s and give 3 s to S3/S4, or use wan3_0. |

Frames on this board, with what each was generated from:

- **F08** (S5 A) — `plate-sun`, `oriane`, `caedom-ascended-1` · previous frame **F06** attached
- **F09** (S5 B) — `plate-sun`, `frozen-tear`

### Coda · Tomorrow, again

*Screenplay: EXT. THE SUN - COURTYARD OF WORLDS - CONTINUOUS.*

| Shot | s | Model (from the bible) | Start anchor | End anchor | Note |
|---|---:|---|---|---|---|
| **S23** Tomorrow, again | 12 | cinematic_studio_3_0 · 12s · 4K · genre drama | **F36**<br>`bf766d12-89ec-4121-93e0-cac2926cb6da` | **F37**<br>`a26c5697-1d07-4e1e-873f-a4fd82092b68` |  |

Frames on this board, with what each was generated from:

- **F36** (S23 A) — `plate-sun`, `courtyard-of-worlds`, `caedom-ascended-1` · previous frame **F03** attached
- **F37** (S23 B) — `plate-sun`, `courtyard-of-worlds`, `frozen-tear` · previous frame **F02** attached

## Canvas II — The Ocean

**Plate:** `plate-ocean-dark`. **Board handles:** `plate-ocean-dark`, `oriane`, `oriane-ascended`, `oriane-damaged`, `turned`, `turned-water`, `threadwright`, `leviathan`, `leviathan-plating`, `aura-shell`, `machira-orbit`, `founding-stone`, `ladder-oriane`, `ladder-attunement`. **Souls for the identity pass:** `oriane`.

### Scene 4 · 108 years later: the run and the wall

*Screenplay: EXT. OPEN OCEAN - MACHIRA - STORM - DAY.*

| Shot | s | Model (from the bible) | Start anchor | End anchor | Note |
|---|---:|---|---|---|---|
| **S6** 108 years later — the run | 14 | cinematic_studio_video_v2 · 12s pro · speedramp auto + 2s ext | **F10** · match<br>`fd757328-a2e8-4ffc-bd6c-961b21bc3db2` | **F11** · shared<br>`c6e868d3-d9c1-4336-9e4c-e774e5cd50b8` | Extension must land on F11, which S7 shares. |
| **S7** Sixteen behind her, and a wall of ice | 12 | kling3_0 · 12s · pro · start+end frame | **F11** · shared<br>`c6e868d3-d9c1-4336-9e4c-e774e5cd50b8` | **F12** · shared<br>`900a2a4c-223b-4fea-956f-400473830731` | Shared F11 in, shared F12 out. Chain from the rendered last frame of S6. |
| **S8** Up the wall | 14 | cinematic_studio_video_v2 · 12s · speedramp impact + 2s ext | **F12** · shared<br>`900a2a4c-223b-4fea-956f-400473830731` | **F13**<br>`87de8feb-f0a4-45e6-8e16-feac0dbb2600` | Ramp plus extension; motivated cut into S9. |

Frames on this board, with what each was generated from:

- **F10** (S6 A) — `plate-ocean-dark` · previous frame **F09** attached
- **F11** (S6 B / S7 A) — `plate-ocean-dark`, `oriane`
- **F12** (S7 B / S8 A) — `plate-ocean-dark`, `oriane`, `turned-water` · previous frame **F11** attached
- **F13** (S8 B) — `plate-ocean-dark`, `turned-water`

### Scene 5 · The Threadwright's eyes

| Shot | s | Model (from the bible) | Start anchor | End anchor | Note |
|---|---:|---|---|---|---|
| **S9** The threadwright's eyes | 12 | veo3_1 · 8s ultra + 4s ext, or cinematic_studio_3_0 · 12s | **F14**<br>`ec69adae-8fc7-4e50-9c5f-1b1e94dccef8` | **F15**<br>`186ee742-3de1-4730-a013-c01e44bd1b30` |  |

Frames on this board, with what each was generated from:

- **F14** (S9 A) — `plate-ocean-dark`, `threadwright`
- **F15** (S9 B) — `plate-ocean-dark`, `threadwright`, `turned` · previous frame **F14** attached

### Scene 6 · The leviathan, the flank, the lightning river

| Shot | s | Model (from the bible) | Start anchor | End anchor | Note |
|---|---:|---|---|---|---|
| **S10** The leviathan | 16 | seedance_2_0 · 15s · 4K · genre epic + ext | **F16**<br>`360d0a10-116c-4581-ad51-1b880707eba7` | **F17** · shared<br>`e47cb162-4e85-4f35-80f6-8a76e12d4a0f` | Identity locked to the leviathan handle; extension must end on F17. |
| **S11** Running the flank | 10 | kling3_0 · 10s · motion_control from a driving clip | **F17** · shared<br>`e47cb162-4e85-4f35-80f6-8a76e12d4a0f` | **B01** · bridge<br>`f3f3ca6e-5f93-4e76-b098-e43c3c9aae74` | High risk: motion_control may not reach B01. If it cannot, cut honestly on the darkest rendered frame. |
| **S12** The lightning river | 12 | cinematic_studio_video_v2 · 12s · speedramp slowmo · pro | **B01** · bridge<br>`f3f3ca6e-5f93-4e76-b098-e43c3c9aae74` | **F18**<br>`75607634-c58d-4fad-84df-f1120567bf35` |  |

Frames on this board, with what each was generated from:

- **F16** (S10 A) — `plate-ocean-dark`, `leviathan`, `leviathan-plating`
- **F17** (S10 B / S11 A) — `plate-ocean-dark`, `leviathan`, `oriane-ascended`
- **B01** (S11 B / S12 A) — `plate-ocean-dark`, `leviathan-plating`
- **F18** (S12 B) — `plate-ocean-dark`, `oriane-damaged`, `aura-shell`

### Scene 7 · The vortex from orbit; the Stone leaves her

*Screenplay: EXT. MACHIRA - FROM ORBIT / EXT. UPPER ATMOSPHERE.*

| Shot | s | Model (from the bible) | Start anchor | End anchor | Note |
|---|---:|---|---|---|---|
| **S13** The vortex, from the Sun | 15 | wan3_0 · 15s · 1080p · generate_audio false | **F19**<br>`35dc71f6-af5b-4621-9e6a-f956e9fdc40f` | **F20**<br>`2c060db4-67f4-4a01-a7f3-507e349abc64` | Silent. generate_audio false. The film's best still-fallback. |
| **S14** The Stone leaves her | 13 | cinematic_studio_3_0 · 13s · 4K · genre drama | **F21**<br>`70a35bb9-7468-4477-861c-6d8532430097` | **F22** · match<br>`fff821a8-7d38-4afe-9aa5-8ab34ca6cd97` | Hold the empty frame two beats; say so in the prompt. |

Frames on this board, with what each was generated from:

- **F19** (S13 A) — `machira-orbit`
- **F20** (S13 B) — `machira-orbit` · previous frame **F19** attached
- **F21** (S14 A) — `plate-ocean-dark`, `oriane-damaged`
- **F22** (S14 B) — `machira-orbit`, `founding-stone` · previous frame **F19** attached

## Canvas III — The Island

**Plate:** `plate-island, then plate-bombardment from F27 to F31`. **Board handles:** `plate-island`, `plate-bombardment`, `nacre-beach`, `corals-abyss`, `keepers-isle`, `white-temple`, `twelve-ships`, `keeper`, `keeper-kneel`, `fx-floating-mountain`, `alder`, `wren`. **Souls for the identity pass:** `alder`, `wren`.

### Scene 8 · Nacre Beach, the same sun; over the abyss

*Screenplay: EXT. NACRE BEACH / EXT. UNDERWATER - THE BLOOM.*

| Shot | s | Model (from the bible) | Start anchor | End anchor | Note |
|---|---:|---|---|---|---|
| **S15** Nacre Beach — the same sun | 12 | cinematic_studio_3_0 · 12s · 4K | **F23** · match<br>`3cb92044-851c-45a8-bccd-e1157967ec7b` | **F24**<br>`c61b4451-f957-432d-b207-438afe2267f3` | Something must move inside the locked frame: the low star fading. |
| **S16** Over the abyss | 12 | kling2_6 · 10s + ext, or seedance_2_0 · 12s (water physics) | **F25**<br>`5ec7049a-d240-48a8-995d-afd84e3eadc1` | **F26**<br>`5edf559f-0009-4abd-86d3-7cd8162e9447` |  |

Frames on this board, with what each was generated from:

- **F23** (S15 A) — `plate-island`, `nacre-beach` · previous frame **F22** attached
- **F24** (S15 B) — `plate-island`, `nacre-beach`, `alder`, `wren`
- **F25** (S16 A) — `corals-abyss`
- **F26** (S16 B) — `corals-abyss`

### Scene 9 · Twelve ships; the Temple does not answer

| Shot | s | Model (from the bible) | Start anchor | End anchor | Note |
|---|---:|---|---|---|---|
| **S17** Twelve ships | 10 | cinematic_studio_3_0 · 10s · 4K · genre epic | **F27**<br>`72f8214a-bacd-47e5-990b-7dfe04918f81` | **F28**<br>`d98fa8ca-876c-4e2e-a6dd-8b233e4c9c06` |  |
| **S18** The Temple does not answer | 10 | cinematic_studio_video_v2 · 10s · multi_shots · multi_prompt | **F29**<br>`778a56cc-c82c-43f3-a221-c55c68900928` | **B02** · bridge<br>`840cbe00-3763-4e3d-8914-80e63760469c` | Multi-shot with an end frame; if the end frame will not hold, make it two 5 s shots. |

Frames on this board, with what each was generated from:

- **F27** (S17 A) — `plate-bombardment`, `nacre-beach`, `alder`, `wren`
- **F28** (S17 B) — `plate-bombardment`, `keepers-isle`, `twelve-ships`, `alder`, `wren` · previous frame **F27** attached
- **F29** (S18 A) — `plate-bombardment`, `white-temple`, `twelve-ships`
- **B02** (S18 B / S19 A) — `plate-bombardment`

### Scene 10 · The Keepers kneel; the mountain; the garden replants itself

*Screenplay: EXT. KEEPER'S ISLE - BEACH - SUNSET.*

| Shot | s | Model (from the bible) | Start anchor | End anchor | Note |
|---|---:|---|---|---|---|
| **S19** The Keepers kneel | 10 | seedance_2_0 · 10s · 4K · start_image from dust | **B02** · bridge<br>`840cbe00-3763-4e3d-8914-80e63760469c` | **F30** · shared<br>`d971d86d-a6b3-42e3-9130-5e57a9f9ef99` |  |
| **S20** The mountain | 14 | wan3_0 · 14s · 1080p · enable_thinking | **F30** · shared<br>`d971d86d-a6b3-42e3-9130-5e57a9f9ef99` | **F31**<br>`41e0a3c1-ae7c-459f-8789-c73ffb38b12e` | Six attempts budgeted. Cannot be rescued in the edit. |
| **S21** The garden replants itself | 8 | veo3_1_lite · 8s, or cinematic_studio_3_0 · 8s | **F32**<br>`26786720-93e0-44f4-b924-31a8c086d67d` | **F33**<br>`492410ef-4316-4873-a910-968918b13df6` |  |

Frames on this board, with what each was generated from:

- **B02** (S18 B / S19 A) — `plate-bombardment`
- **F30** (S19 B / S20 A) — `plate-bombardment`, `keeper-kneel`, `keeper`
- **F31** (S20 B) — `plate-bombardment`, `fx-floating-mountain`, `keeper-kneel` · previous frame **F30** attached
- **F32** (S21 A) — `plate-island`
- **F33** (S21 B) — `plate-island`, `white-temple`

### Scene 11 · What Alder saw

*Screenplay: EXT. KEEPER'S ISLE - BEACH GRASS - GOLDEN HOUR.*

| Shot | s | Model (from the bible) | Start anchor | End anchor | Note |
|---|---:|---|---|---|---|
| **S22** What Alder saw | 14 | veo3_1 · 8s ultra + ext, or minimax_hailuo 2.3 · 10s (emotion) | **F34**<br>`c73d7f62-b0ed-4ecc-8e8f-e42353758386` | **F35**<br>`1b3c8159-88d7-4347-a9cc-6cd0364a361a` | Gate C fix: 10 s model for a 14 s shot. Use cinematic_studio_3_0 at 14 s or wan3_0. |

Frames on this board, with what each was generated from:

- **F34** (S22 A) — `plate-island`, `alder`, `wren`
- **F35** (S22 B) — `plate-island`, `alder`

## The audit that preceded this (Sep 6)

- **Every Sep 5 job is terminal.** 76 jobs across seven batches: 73 completed, 3 rejected by the content filter (the first Thrall sheet, one Alder sheet, one Threadwright sheet), and each rejection was covered by a clean pass of the same or the re-worded prompt. Nothing is missing.
- **Every one of the 42 assets now has a clean production-name handle.** Five were created today from stable A-lane jobs — `turned-hollows`, `turned-water`, `ladder-oriane`, `ladder-attunement`, `aura-grammar` — and `plate-ocean-dark` is the sixth.
- **Two gaps were recorded and not regenerated.** All 49 Sep 5 sheets were generated text-only — no plate attached to a location, no group sheet attached to a Turned variant — and fourteen world sheets landed at 16:9 where the lane asks for 21:9. Under the rule for this pass (regenerate only where more than two attributes improve) neither qualifies on its own, and both are corrected for free at the anchor stage, where the plate and the sheet are attached to every frame.
- **One regeneration: the Ocean plate.** The Sep 5 file promised the dark-ground rule for both the Ocean and the Island plates and only the Island got it. The l2 prompt now carries the rule and was regenerated (job `66da2493-5ab7-4e8d-a86b-f9936370ea7e`) as `plate-ocean-dark`, which every Movement II anchor above was generated against. `plate-ocean` stays only because the API cannot delete it.
- **Souls:** six ready — `alder`, `wren`, `oriane`, `caedom-ascended`, `caedom-before`, and the Aug 19 `Caedom` (Oriane's face; delete). `caedom-mortal` is ready but trained on both forms; use `caedom-before`.

## Left for the web UI

Delete the elements `alder-1`, `wren-1`, `oriane-1`, `caedom-mortal-1`, `caedom-mortal`, `caedom-ascended` and `plate-ocean`; use `caedom-before`, `caedom-ascended-1` and `plate-ocean-dark` in their place. Delete the Souls `Caedom` and `caedom-mortal`. Clear the 23 legacy handles that carry the novel's vocabulary (listed in the local snapshot). None of this can be done from the API.
