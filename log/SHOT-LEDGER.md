# SHOT LEDGER

The single source of truth for the film. One row per generation.
Populated from [`../script/SCRIPT.md`](../script/SCRIPT.md) via the five-pass breakdown in
[`../docs/04-SEQUENCE-ARCHITECTURE.md`](../docs/04-SEQUENCE-ARCHITECTURE.md).

**Status:** ⬜ planned · 🟡 in iteration · 🟢 locked · 🔴 restructure (hit the 10–15 rule)

---

## THE LEDGER

| ID | Scene | Dur | Model | Framing | Camera | Beat | Trans IN | Trans OUT | Takes | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |

**Running total: ___ s** · **Target: ___ s** · **Sum check: ☐ passes exactly**

---

## TEMPO GATE

### Sum check
Planned durations must total the target runtime **exactly**. A budget that doesn't add up ships
dead air or an impossible cut, and the error is invisible until the timeline.

- Target runtime: ______
- Sum of planned durations: ______
- ☐ Match

### Monotony audit
Read **only** the framing + camera column, top to bottom, as a sequence. **No three consecutive
shots may share both shot size AND camera move.**

```
ID    FRAMING       CAMERA MOVE            OK?
──    ───────       ───────────            ───

```

- ☐ No run of three passes

### Shot-length distribution
Compare against the target profile in
[`../docs/02-DIRECTING-DOCTRINE.md`](../docs/02-DIRECTING-DOCTRINE.md) § 4.2:

| Band | Target | Actual |
|---|---|---|
| Anchors (20–40s) | 3–4 | |
| Sustained (12–18s) | 8–10 | |
| Connective (6–10s) | 6–8 | |
| Bursts (0.5–2s) | 6–10, **quarantined to one passage** | |

- ☐ Bursts are concentrated in ONE passage, not scattered

---

## ASSET GLOSSARY

| `@`-tag | Type | Fidelity grade | Status | Gens |
|---|---|---|---|---|
| `@` | character | full-preserve | ⬜ | |
| `@` | location | attribute-transfer: space + texture only | ⬜ | |
| `@` | object | full-preserve | ⬜ | |

**Locked descriptors** (pasted verbatim into every prompt — never shortened):

```
CHARACTER — [tag]:
[full physical descriptor — visible markers only: clothing, build, posture, hair. No age. No names of real people.]

VOICE — [tag]:
[register, tempo, accent, manner]

BEHAVIOUR — [tag]:
[movement, hands, habits, eye behaviour, how they break under pressure]
```

---

## GEO SPATIAL LAYOUT BLOCKS

One per scene. Written once, pasted **unchanged** into every shot in that scene.

### Scene 1
```
GEO SPATIAL LAYOUT (locked across every shot — pure spatial map):
— [LANDMARK] = [what it is], [position]
— [LANDMARK 2]: [position], [metres from landmark 1]
— 180° AXIS: camera ALWAYS stays [which side] — it NEVER crosses [the line]
— LIGHT LOGIC: [the ONE source], [direction], [what it does NOT reach]
```

---

## TRANSITION PLAN

Every seam gets a technique, chosen from
[`../docs/02-DIRECTING-DOCTRINE.md`](../docs/02-DIRECTING-DOCTRINE.md) § 3 — and **written into
the prompts on both sides.**

| Seam | Technique | Written into prompt? |
|---|---|---|
| 1a → 1b | | ☐ |

**Budget checks:**
- Whip-pan seams used: ___ / **2 maximum**
- Sound bridges planned: ___ / **should be ~every seam**
- ☐ The one deliberate hard cut is assigned to: ______

---

## DAILY LOG

```
## Day N — [date]
Generations: ___    Kept: ___    Rate: ___%
Shots advanced: 
Shots locked: 
Blocked on: 
Tomorrow: 
```

---

## ITERATION LOG

One row per meaningful iteration. **One variable changes per row** — multi-variable iteration
makes diagnosis impossible, and without this log you cannot reproduce a good shot.

| Shot | v | What changed (ONE thing) | Verdict | Reject reason |
|---|---|---|---|---|
| | | | | |
