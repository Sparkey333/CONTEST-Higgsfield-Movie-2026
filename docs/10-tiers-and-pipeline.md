# Tiers & Pipeline — Live Account Data

*Pulled directly from the Higgsfield account, 2026-08-08.*

---

## 1. Prize Tiers — 14 Winners, $1,000,000

| Tier | Award | Count | Total | Decided by |
|---|---|---|---|---|
| 🥇 1st place | **$500,000** | 1 | $500,000 | Jury |
| 🥈 2nd place | **$200,000** | 1 | $200,000 | Jury |
| 🥉 3rd place | **$100,000** | 1 | $100,000 | Jury |
| 🎬 **Audience Choice** | **$100,000** | 1 | $100,000 | **Audience** |
| ⭐ Honorable Mention | **$10,000** | 10 | $100,000 | Jury |
| | | **14** | **$1,000,000** | |

**Read the shape of that table.** Ten of the fourteen prizes are $10,000 Honorable Mentions — a **71% chance that any given win is an HM**. The realistic target is not first place; it's *landing in the fourteen*. Design for that, and let the top three be upside.

Note also that Audience Choice pays the same as third place and is decided by a completely different mechanism. That is the second-cheapest prize on the board to compete for, after HM.

### Entry rules

- **Unlimited entries** per person or team.
- **Each entry must be a standalone film.** No submitting five chapters of one story as five entries.
- **One prize per participant.** If two of your films place, you take the higher one; the other slot cascades to another entrant.
- Solo or teams up to 4. Worldwide, 18+. Active subscription required.

> ⚠️ **Unresolved and decision-relevant:** whether **Audience Choice** falls under the one-prize cap or sits outside it. This is question #6 in `01-contest-brief.md` §6. It determines whether a second film is *upside* or merely *insurance*.

---

## 2. Your Account — Live

| | |
|---|---|
| **Plan** | **Ultra** |
| **Credits on hand** | **1,000** |
| Workspace | Private, sole owner |
| Unlimited-generation allowance | **Not currently available** (`unlim.available: false`) |
| Free trial | Not eligible (already on Ultra) |
| Auto-refill | **Disabled**, eligible, threshold 300 |

**Eligibility is settled** — Ultra satisfies the "active subscription" requirement. Nothing blocks you from entering.

---

## 3. Credit Tiers

One-time top-up packs, current pricing:

| Pack | Price | Was | Discount | Credits/$ |
|---|---|---|---|---|
| 500 | $26 | $42.50 | 39% | 19 |
| 1,000 | $49 | $85 | 42% | 20 |
| 2,000 | $95 | $170 | 44% | 21 |
| **4,000** | **$190** | $340 | **44%** | **21** |

Auto-refill is available in 2,000 / 4,000 / 9,000 / 15,000 / 30,000 blocks at ~18 credits per dollar, triggering below 300 credits.

**Top-up credits expire after 90 days.** For a contest closing Aug 31 that is irrelevant — anything you buy now, you'll spend now.

### The budget gap — read this carefully

The production plan estimates **~1,300 generations** across two films (`08-production-plan.md` §1). You hold **1,000 credits**. Those two numbers are not directly comparable, because **a generation is not a credit** — cost varies by model, resolution, duration, and mode, and I could not pull a per-generation price from the API.

**Measure it before you buy anything:**

1. Run **five** test generations at your intended production settings — same model, same resolution, same duration.
2. Check `balance` before and after.
3. Divide. Now you have a real credits-per-shot number.
4. Multiply by 1,300.

If that lands under 1,000, you're fine on the credits you already have. If it lands over, buy the **4,000 pack at $190** — it's the best ratio on the board and it removes the risk of stalling mid-production on Aug 20 with no film. Against a $10,000 floor prize, $190 is not the decision to agonize over. *Do the measurement first, though — buying blind is how people overspend on a contest they were already funded for.*

Auto-refill is the safer structure if you'd rather not think about it again ([setup](https://higgsfield.ai/mcp-credits?show_modal=auto_refill&source=mcp)), but a single deliberate top-up gives you a hard ceiling, which for a 23-day sprint is arguably better discipline.

---

## 4. The Model Pipeline — Mapped to the Films

The model catalog answered the biggest open technical risk in this package. **Character drift across 61 shots was the #1 risk in the register. There is a purpose-built tool for it.**

### Stage 1 — Character identity lock

| Model | What it does | Use |
|---|---|---|
| **Soul Cast** (`soul_cast`) | *"Consistent cinematic character identity."* Has a `budget` parameter (10–500). | **Build Eli here first, before anything else.** This produces the identity you reuse everywhere downstream. |

This is the single highest-leverage call in the entire production. Do it on **Day 1 of look dev (Aug 12)**, spend real budget on it, and do not generate a single film shot until Eli holds.

### Stage 2 — Stills / keyframes

| Model | Why |
|---|---|
| **Soul Cinema** (`soul_cinematic`) | Cinema-grade stills and concept art, and it accepts a **`soul_id`** — so it inherits the locked character. Supports **21:9**. This is your keyframe generator. |
| **Cinema Studio Image 2.5** | Cinematic stills to 4K, 21:9. Use for plates with no character in them — the silt plain, the tower, the steps. |
| **Nano Banana Pro** | 4K, strong text rendering. Use for **the 1961 survey plat** — the one insert in SILT that contains legible text. |

### Stage 3 — Stills → motion

| Model | Strengths | Best for |
|---|---|---|
| **Cinema Studio Video 3.0** (`cinematic_studio_3_0`) | *"Most advanced cinema-grade model."* 4–15s, up to 4K, **21:9**, `genre` hint, start_image + end_image, `generate_audio` defaults **false**. | **The primary film model.** Genre hint `drama` for most of SILT, `epic` for the refill. |
| **Seedance 2.0** | Reference-driven with `image_references` for identity, 21:9, 4K, `mode: std/fast`. | Any shot where identity is drifting — feed it the Soul Cast reference directly. |
| **Kling v3.0** | Multi-shot, motion transfer, `sound: off`. | The refill set piece; motion transfer if you need specific camera behavior. |

### Two settings that matter for SILT specifically

- **Shoot 21:9.** Both primary video models support it. In a contest judged by an ASC cinematographer, a genuine anamorphic-ratio frame is a free signal of intent — and it suits a film about a horizontal landscape and a vertical tower.
- **Turn audio generation OFF.** `generate_audio: false` on Cinema Studio 3.0, `sound: "off"` on Kling. You are scoring this deliberately on an 82.4 Hz spine; you do not want the model's guess at what a bell sounds like. It also **costs fewer credits** — Kling's parameter documentation says so explicitly.

### Credit levers, in order of savings

1. `mode: "fast"` / `mode: "std"` on Seedance — use `fast` at 720p for all look-dev and blocking passes, `std` only for keepers.
2. Audio off everywhere.
3. Test at 480p/720p; final-pass only the selected shots at 1080p/4K.
4. Shorter durations — most SILT shots are 3–5s. Do not generate 10s clips to use 4 seconds.

> **The workflow that saves the most credits isn't a setting.** It's generating the *still* first, judging it for free-ish, and only animating stills you already know are keepers. Two-stage beats one-stage by a wide margin at these keep rates.

---

## 5. Revised Day-1 Look Dev

Replacing the Aug 12–14 block in `08-production-plan.md`:

1. **Soul Cast — build Eli.** Spend real budget. Do not proceed until the identity holds across six varied setups.
2. Capture the `soul_id`. It goes into every Soul Cinema call.
3. Location plates via Cinema Studio Image 2.5 at 21:9 — basin, steps, tower exterior, tower interior.
4. The 1961 plat via Nano Banana Pro.
5. **Measure credits-per-shot** on five generations at production settings. Then decide on the top-up.
6. Six test shots — 4, 22, 37, 40, 56, 60 — through Cinema Studio Video 3.0.

**Gate:** if Eli doesn't hold after Soul Cast, that is not a prompt problem, it's a design decision. Fall back to the shot design where the face is never clean — which SILT is already 93% built for.
