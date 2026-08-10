# Higgsfield Global Film Festival 2026 — Production Bible

A 4–5 minute short film for the **$1,000,000 Higgsfield Global Film Festival**.
Jury: **Ed Catmull**, **Phedon Papamichael ASC**, **Paul W. S. Anderson**.

> ## ⏱ Submission deadline: **September 3, 2026** · 24 days from 2026-08-10
> Internal deadline **September 1** (48-hour buffer).

---

## The thesis, in one paragraph

All three judges independently want the same film: **one coherent space, one motivated light
source, long held takes, a face allowed to carry a scene, real physical weight, and a story that
turns — with cutting used as a weapon rather than a default.** That is also exactly what AI video
is currently best at, exactly the style described in the brief, and — because 24 shots at 100
takes each is achievable where 70 shots at 100 takes each is not — **the only version of this film
that can actually be finished in 24 days.** Four independent constraints pointing the same
direction is the plan.

The modal entry will be a 3-minute montage of 50+ four-second clips, orange-and-teal, scored like
a trailer, with no character you could name afterwards. There will be thousands of them.
**The competitive moat is restraint.**

---

## Read in this order

| # | Document | What it gives you |
|---|---|---|
| **00** | [Contest Brief](docs/00-CONTEST-BRIEF.md) | Rules, timeline, prize structure, **4 unknowns to verify first** |
| **01** | [Judges Dossier](docs/01-JUDGES-DOSSIER.md) | Full careers, last 12 months, what each rewards and punishes, **the convergence thesis** |
| **02** | [Directing Doctrine](docs/02-DIRECTING-DOCTRINE.md) | Why AI films feel like ads, the long-take grammar, **7 ways to hide a cut**, rhythm architecture, layered truth |
| **03** | [Higgsfield Playbook](docs/03-HIGGSFIELD-PLAYBOOK.md) | Model routing + durations, Hell Grind prompt architecture, **the Papamichael filter**, consistency, economics |
| **04** | [Sequence Architecture](docs/04-SEQUENCE-ARCHITECTURE.md) | **The five-pass script breakdown**, envelope rules, tempo gate, risk table |
| **05** | [Story Concepts](docs/05-STORY-CONCEPTS.md) | Six original concepts engineered for this jury |
| **06** | [The Wargame](docs/06-WARGAME.md) | Scoring rubric, judge-by-judge predictions, **intake template for your ideas** |
| **07** | [Production Schedule](docs/07-PRODUCTION-SCHEDULE.md) | Day-by-day for 24 days, credit budget, failure modes |

**Working files:** [`script/SCRIPT.md`](script/SCRIPT.md) ·
[`script/IDEAS-INBOX.md`](script/IDEAS-INBOX.md) · [`log/SHOT-LEDGER.md`](log/SHOT-LEDGER.md)

---

## ⚠️ Two things block progress

### 1. The script isn't here
The brief referenced "this script" and "the doc," but neither was in the repo or the conversation.
**Paste it into [`script/SCRIPT.md`](script/SCRIPT.md)** and the five-pass breakdown runs
immediately — producing the full shot ledger, transition plan, GEO blocks, asset glossary and
anchor-shot prompts.

Meanwhile, everything that doesn't depend on it is done, and
[`docs/05-STORY-CONCEPTS.md`](docs/05-STORY-CONCEPTS.md) offers six alternatives if you'd rather
start fresh.

### 2. Four contest rules need verifying
The official page is blocked by this environment's network proxy. Before generating anything,
confirm: **maximum runtime**, whether *all generation* must occur inside Cinema Studio (this
determines whether the 20–30 second long-take models are legal), entries per person, and the
rights you grant. Details in [`docs/00-CONTEST-BRIEF.md`](docs/00-CONTEST-BRIEF.md).

---

## The numbers that shape everything

| | |
|---|---|
| Video acceptance rate | **~1.5%** (65–100 generations per kept shot) |
| Generations to lock one character | **~800** |
| Target shot count | **~24** (vs. 50–80 for a typical entry) |
| Estimated total generations | **~4,100** |
| Longest single generation available | **30s** (Wan 3.0) / **20s** (FLUX 3 Video) |
| Everything else | caps at 15s — or **12s** inside Cinema Studio |
| Expected field size | 10,000–20,000 entries |

---

## Prize structure

| Placement | Prize |
|---|---|
| 1st | $500,000 |
| 2nd | $200,000 |
| 3rd | $100,000 |
| Audience Choice | $100,000 |
| Honorable Mention ×10 | $10,000 each |

80% of the money is in the top three — design for the podium, not the floor.
Audience Choice is a **separate game with different rules**; see
[`docs/06-WARGAME.md`](docs/06-WARGAME.md) § 4.

---

## Next three actions

1. **Verify the four contest unknowns** (30 minutes, today)
2. **Drop the script** into [`script/SCRIPT.md`](script/SCRIPT.md), or add ideas to
   [`script/IDEAS-INBOX.md`](script/IDEAS-INBOX.md)
3. **Lock one concept by August 12.** Every day spent choosing is a day not spent iterating, and
   only iteration days produce a film.
