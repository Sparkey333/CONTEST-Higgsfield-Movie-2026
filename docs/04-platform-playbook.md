# Higgsfield Platform Playbook

Live model roster pulled from the Higgsfield MCP (`models_explore`) on 2026-08-08.
Our account is on **Ultra**. Choose deliberately — model choice is a craft decision,
not a default.

---

## Video models — what to use when

### Premium finishing (final shots)

| Model | Duration | Max res | Aspect | Why |
|---|---|---|---|---|
| **Cinema Studio Video 3.0** `cinematic_studio_3_0` | 4–15s | **4K** | incl. **21:9** | Higgsfield's most advanced cinema model. Genre hints (`action, horror, noir, drama, epic`). **Our default for hero shots.** |
| **Seedance 2.0** `seedance_2_0` | 4–15s | **4K** | incl. 21:9 | **Reference-driven identity consistency.** Accepts `image_references`, `video_references`, `audio_references`, start/end frames. **The character-consistency workhorse.** |
| **Veo 3.1** `veo3_1` | 4/6/8s | ultra tier | 16:9, 9:16 | Ultra-realistic, top-tier cinematic. |
| **Kling v3.0** `kling3_0` | 3–15s | **4K** | 16:9, 9:16, 1:1 | Multi-shot, audio sync, motion transfer. |
| **MiniMax H3** `minimax_h3` | 4–15s | 2K | incl. 21:9 | Full reference suite + keyframes, batch up to 4. |

### Blocking and tests (cheap)

| Model | Why |
|---|---|
| **Seedance 2.0 Mini** `seedance_2_0_mini` | Fast/budget with the *same* reference inputs — test composition cheaply, then re-run on full Seedance 2.0. |
| **Veo 3.1 Lite** `veo3_1_lite` | Budget batch clips. |
| **Kling 3.0 Turbo** `kling3_0_turbo` | Fast iteration. |

### Specialists

| Need | Model |
|---|---|
| Character-consistent + synced audio | **Wan 2.7** `wan2_7` |
| Long takes up to 30s | **Seedance 2.5** `seedance_2_5` (also video *edit* + *extension*) |
| Multi-frame / continuation / storyboard chaining | **FLUX 3 Video** `flux_3_video` (5–20s, start+end frames) |
| Stylized / experimental | **Wan 2.6** `wan2_6` |
| Natural physics, facial emotion | **Minimax Hailuo** `minimax_hailuo` |

### Post

| Need | Tool |
|---|---|
| Upscale to 2K/4K | `bytedance_video_upscale` (presets incl. **`aigc`**), `topaz_video`, `upscale_video` |
| **Fix flicker** | `video_deflicker` ← *use this; flicker is a top AI tell* |
| Aspect change | `reframe` |
| Lip sync | `sync_so` (Sync Lipsync 3) |
| Motion transfer / recast / puppeteer | `motion_control` |
| Background removal | `sam_3_video`, `video_background_remover` |

---

## The continuity workflow — Phedon's core loop

**This is the single highest-value technique on the platform.**

1. **Build the character sheet first.** Call `get_workflow_instructions` with
   `{workflow: "character-sheet"}` — there is a dedicated official workflow. Generate
   a turnaround / expression sheet before any shot.
2. **Lock identity with references.** Feed the sheet into `image_references` on
   Seedance 2.0 / MiniMax H3 / Wan 3.0 for every shot the character appears in.
3. **Chain shots via frames.** Use the `end_image` of shot N as the `start_image` of
   shot N+1. This is the strongest continuity lever available.
4. **Hold the light.** Same palette, same key direction, every shot. Papamichael reads
   this instantly.
5. **Deflicker before upscaling**, not after.

> Before any multi-step film work, call `get_workflow_instructions` with no argument
> to list official workflows, then load the matching one. Higgsfield built these; use
> them rather than improvising.

---

## Aspect ratio

`[VERIFY]` — the contest's required aspect ratio is not published in any source we
could reach. **Confirm on Aug 10 when the project opens.**

Default assumption: **16:9** for a film festival. If **21:9** is permitted, it is a
strong cinematic signal to a cinematographer juror — `cinematic_studio_3_0`,
`seedance_2_0`, `minimax_h3`, and `flux_3_video` all support it.

Deliver the highest resolution the pipeline supports. 4K is available on Cinema Studio
3.0, Seedance 2.0 (`mode: std`), and Kling v3.0 (`mode: 4k`).

---

## Audio — Anderson's toolkit

| Need | Tool |
|---|---|
| Music / SFX / ambience | `generate_audio`, `generate_audio_batch` |
| Custom voice | `create_voice`, `list_voices`, `voice_change` |
| Dubbing | `dubbing` |
| Speech cleanup | `media_enhance_speech` |
| Native in-model audio | `generate_audio: true` on Seedance / FLUX 3 / Wan 3.0 / Kling / Veo |

> Native model audio is a **starting point, not a deliverable.** Every competitor will
> ship it as-is. Layered, designed sound is one of our cheapest paths to reading as
> professional to a jury that explicitly judges sound.

---

## Campaign tools — Anderson

| Need | Tool |
|---|---|
| **Predict performance before posting** | `virality_predictor` |
| Analyze a cut | `video_analysis_create` |
| TikTok publishing | `tiktok_connect`, `tiktok_prepare_publish`, `tiktok_publish` |
| Trending audio | `tiktok_music_trending`, `tiktok_music_tune` ⚠️ *music rights — Catmull must clear* |
| Vertical cutdowns | `shorts_studio_create`, `personal_clipper_create` |

⚠️ **Trending audio is a disqualification trap.** Licensed music is banned. Use
platform trending audio for *promo clips only if the rules permit it there* — never in
the film. Catmull clears every audio decision.

---

## Batch discipline

For multiple independent generations use `generate_video_batch` / `generate_image_batch`
+ `jobs_wait`, then a single `show_generation_by_ids`. Faster and cheaper than
sequential calls.

---

## Cost control

| Lever | Effect |
|---|---|
| Resolution | 480p → 4K is the biggest multiplier. Test at 480p/720p. |
| `mode: fast` vs `std` | Seedance fast is materially cheaper (480p/720p only) |
| `generate_audio: false` | Cheaper when Anderson is scoring the shot anyway |
| Mini/Lite variants for blocking | Same references, fraction of the cost |
| Duration | Bill scales with seconds — generate the shot, not the scene |
