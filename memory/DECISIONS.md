# DECISIONS — The Settled Record

**Append-only.** Never delete a decision. If one is reversed, log the reversal beneath
it with the reason. The reasoning is worth more than the ruling.

**Do not relitigate anything here** unless new evidence arrives.

---

## D-001 · Adopt the Godai five-element council
**Date:** 2026-08-08 · **Decided by:** Human directive · **Status:** ✅ ACTIVE

Five persistent agents — Catmull (地), Phedon (水), Edwin (火), Anderson (風), Braintrust (空) —
each a structurally different way of seeing, defined in `.claude/agents/`.

**Rationale:** a single optimizer converges on its own taste and cannot see its blind
spots. Five agents with opposed priorities cannot. The friction between them *is* the
quality mechanism, and their domains map cleanly onto the five scoring criteria.

---

## D-002 · Engagement is a first-class workstream, not marketing
**Date:** 2026-08-08 · **Decided by:** Braintrust + Anderson · **Status:** ✅ ACTIVE

Platform Engagement (15%) + Social Media Engagement (15%) = **30% of the score**, plus
a separate **$100,000 Audience Choice** prize. Anderson runs a campaign from day one, in
parallel with production — not after it.

**Rationale:** craft criteria are contested by thousands of talented entrants with
brutally non-linear returns. Engagement is contested by almost nobody and converts
effort to points nearly linearly. A very good film with a 23-day campaign beats an
outstanding film posted cold on Aug 31.

**Depends on:** rubric weights, currently `[VERIFY]`. If the weights are wrong, this
decision must be revisited immediately.

---

## D-003 · Submit on Aug 30, not Aug 31
**Date:** 2026-08-08 · **Decided by:** Catmull · **Status:** ✅ ACTIVE

All gates are set against an **Aug 30** submission. Aug 31 is buffer only.

**Rationale:** 24 hours of margin against upload failure, watermark problems, and
platform congestion on the final night. Contests are lost to logistics more often than
to quality.

---

## D-004 · Wordless or near-wordless film
**Date:** 2026-08-08 · **Decided by:** Edwin · **Status:** ✅ ACTIVE

All three concepts are built to carry meaning through behavior, staging, and sound
rather than dialogue.

**Rationale:** two reasons. (1) Lip-sync and vocal performance are where AI film most
visibly breaks — avoiding dialogue removes our largest technical liability. (2) It is
the exact register Edwin Catmull spent forty years building at Pixar (*Piper*,
*Paperman*, the opening of *Up*). It plays to the jury's taste and away from our
weakness simultaneously.

---

## D-005 · Runtime target 3:15–4:30
**Date:** 2026-08-08 · **Decided by:** Catmull · **Status:** ✅ ACTIVE

Hard floor is 3:00. **We never deliver under 3:10.**

**Rationale:** the floor is a disqualifier. Frame-accurate cutting near a hard limit is
how good films get thrown out at Screening. 3–5 is the recommended band; the lower-mid
of it keeps pace tight while preserving margin.

---

## D-006 · Name the council for the jury
**Date:** 2026-08-08 · **Decided by:** Human directive · **Status:** ✅ ACTIVE

The five elements are renamed for the three judges who will actually decide this:

| Agent | Element | Patron |
|---|---|---|
| **CATMULL** | 地 Earth | Edwin Catmull, *the President* |
| **PHEDON** | 水 Water | Phedon Papamichael |
| **EDWIN** | 火 Fire | Edwin Catmull, *the Storyteller* |
| **ANDERSON** | 風 Wind | Paul W. S. Anderson |
| **BRAINTRUST** | 空 Void | Catmull's Pixar Braintrust |

**Rationale:** each agent now argues the way its patron judges, so an internal council
review becomes a rehearsal of the real one. Catmull holds two seats because he
contains two opposed instincts — the executive who builds the structure and the
storyteller the structure exists to protect. Braintrust is named for his own
candid-feedback council at Pixar, which is precisely the function Void performs.

---

## D-007 · Third juror confirmed — concept ranking revised
**Date:** 2026-08-08 · **Decided by:** Braintrust · **Status:** ✅ ACTIVE
**Supersedes the concept ranking in the original `docs/06-concepts.md`.**

The official contest page confirms a **third judge: Paul W. S. Anderson** — *Mortal
Kombat*, the *Resident Evil* franchise, *Alien vs. Predator*, *Event Horizon*.
Billion-dollar franchise director; the page calls him *"the man who brought video
games to the big screen."*

**What changed.** Our original strategy assumed a two-person jury of Catmull (story)
and Papamichael (light), and therefore recommended the quietest, most intimate concept
(*A · Understudy*, a wordless puppeteer film). **That was a one-vote-of-three
strategy.** Anderson has spent thirty years mastering audience retention. A beautiful,
static, contemplative short loses his vote outright.

**New ranking:** **C · *Tidewalker*** becomes primary — the only concept scoring ★★★★
or better with all three jurors, and the only one with a built-in ticking clock and
action set-piece. *Understudy* moves to secondary (entries are unlimited). *The
Keeper* remains the reserve pivot.

**Three independent reasons now point at Tidewalker:** it wins Anderson's vote, it has
the strongest Audience Choice hook ($100K), and it double-dips into *Make Your Action
Scene* ($500K, same deadline).

**Reversal condition:** if early tests show the returning-tide simulation is
unrecoverable, pivot to *B · The Keeper* immediately rather than at day 15.

---

## PENDING — not yet decided

| # | Decision | Owner | Needed by |
|---|---|---|---|
| P-01 | **Which concept is primary?** Council now recommends **C · *Tidewalker*** (revised — see D-007) | All → Catmull ratifies | **Aug 12 (Gate 1)** |
| P-02 | Portfolio strategy — single film, or primary + secondaries? | Braintrust | Aug 16 |
| P-03 | Do we also enter *Make Your Action Scene* ($500K, same deadline)? | Anderson + Catmull | Aug 20 |
| P-04 | Credit budget ceiling | Catmull | **Immediately — blocking** |
| P-05 | Aspect ratio (16:9 vs 21:9) | Phedon | Aug 10, after project opens |
