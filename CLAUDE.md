# CLAUDE.md — Project Memory

> This file loads automatically at the start of every session in this repository.
> It is the council's **long-term memory**. Anything that must survive a context reset
> lives here or is linked from here.

---

## The mission

Win the **Higgsfield Global Film Festival** — a $1,000,000 AI film contest with 14
winners, judged by Edwin Catmull (5× Oscar, Pixar co-founder) and Phedon Papamichael
(2× Oscar-nominated cinematographer).

**Deadline: August 31, 2026, 11:59 PM PT.** Hard. No extensions assumed.

**Deliverable:** a 3–5 minute AI short film (3:00 hard floor), with the official
Higgsfield watermark, published via public post, with prompts and generation history
made public, produced inside the official festival project (opens Aug 10).

---

## Session start protocol

Every session, in this order:

1. Read `memory/STATE.md` — where we actually are right now.
2. Run `bash scripts/deadline.sh` — days remaining and the current warning level.
3. Read `memory/DECISIONS.md` — what has already been settled. **Do not relitigate
   settled decisions** unless new evidence arrives.
4. Check `docs/00-verification-queue.md` — unconfirmed facts we are building on.
5. Then work.

At session end, update `memory/STATE.md` and append to `memory/COUNCIL-LOG.md`.
**A session that ends without updating memory has partially wasted itself.**

---

## The jury — three judges, three different films

| Juror | Judges | Wants |
|---|---|---|
| **Edwin Catmull** — Pixar co-founder, 5× Oscar, Turing Award | Story, character | **Heart** |
| **Phedon Papamichael** — 2× Oscar-nominated DP (*Nebraska*, *Chicago 7*) | Light, lens, blocking | **Craft** |
| **Paul W. S. Anderson** — *Mortal Kombat*, *Resident Evil*, *Event Horizon* | Pacing, attention | **Propulsion** |

⚠️ **They do not want the same film.** A quiet, beautiful, static short wins Catmull
and loses Anderson. The winning concept must carry **feeling through momentum.**

---

## The council — five elements, named for the jury

Five persistent agents in `.claude/agents/`, each embodying one juror's worldview.
Invoke by name via the Agent tool.

| Agent | Element | Patron juror | Owns | Call it for |
|---|---|---|---|---|
| **`catmull`** | 地 Earth | Catmull *(the President)* | Compliance, rules, structure, logistics, budget, deadline | "Are we allowed to?" "Does it hold?" |
| **`phedon`** | 水 Water | Papamichael | Continuity, character consistency, lens & light, editing, salvage | "Why did the face change?" "Does this cut?" |
| **`edwin`** | 火 Fire | Catmull *(the Storyteller)* | Emotion, concept, hook, ending, empathy | "Do we care?" "Does this land?" |
| **`anderson`** | 風 Wind | Paul W. S. Anderson | Propulsion, sound, music, engagement (30%), Audience Choice | "Why are they still watching at 2:30?" |
| **`braintrust`** | 空 Void | The Pixar Braintrust | Red team, originality, jury psychology, meta-strategy | "What are we missing?" "Break this." |

Catmull holds two seats because he contains two opposed instincts — the executive who
builds the structure, and the storyteller the structure exists to protect. **Braintrust**
is named for his own candid-feedback council at Pixar.

**Operating protocol:** `docs/05-council-protocol.md`.
**Wargame protocol:** `docs/10-wargame.md` — how a concept gets tested before a credit is spent.

### Hard rules of the council

- **Catmull holds veto.** No concept enters production before clearing the compliance
  gate. A disqualified film is worth $0 regardless of quality.
- **Braintrust speaks last** on any lock decision. Nothing is finished until it has
  been attacked. Candor above comfort — but it must ship, not merely object.
- **Edwin holds the spine.** Phedon may change any shot; he may not lose the feeling.
- **Anderson is not optional.** 30% of the rubric is engagement, and his patron is on
  the jury. Treating either as marketing fluff forfeits a third of the score and a vote.
- **If all five agree instantly, something is wrong.** Braintrust must say so.

---

## Scoring rubric — the thing we are optimizing

| Criterion | Weight |
|---|---|
| Cinematic Quality | 25% |
| Storytelling & Creativity | 25% |
| Technical Execution | 20% |
| **Platform Engagement** | **15%** |
| **Social Media Engagement** | **15%** |

**50% is craft. 20% is execution. 30% is engagement — and engagement is the least
contested surface in the contest.** Full analysis: `docs/02-scoring-model.md`.

⚠️ This rubric is `[VERIFY]` — sourced indirectly because `higgsfield.ai` is
egress-blocked in this environment. It is load-bearing. Confirm it against the live
page at the first opportunity.

---

## Hard constraints — never violate

- ❌ No copyrighted IP, movie characters, or brand logos
- ❌ No licensed music — royalty-free or original composition **only**
- ❌ No NSFW
- ❌ **No political statements**
- ❌ **No religious statements**
- ✅ Runtime **≥ 3:00** (target 3:15–4:30 for safety margin)
- ✅ Official Higgsfield watermark on every upload
- ✅ Public post + published prompts and generation history
- ✅ Team ≤ 4 people, 18+, active subscription (**we are on Ultra ✅**)

Violations can mean removal and, for serious cases, a permanent ban from future
contests.

---

## Known blockers

| Blocker | Status |
|---|---|
| **MCP credit balance = 0** on Ultra | 🔴 **OPEN** — gates all generation. See `docs/01-contest-dossier.md` §11 |
| `higgsfield.ai` egress-blocked in this environment | 🟡 Working around via search + MCP tools |
| Official project opens Aug 10 | 🟡 Confirm submission mechanics that day |

---

## Where things live

```
CLAUDE.md                    ← you are here (auto-loaded memory)
memory/
  STATE.md                   ← current state; read first, update last
  DECISIONS.md               ← settled decisions; do not relitigate
  COUNCIL-LOG.md             ← running session log
.claude/agents/              ← the five elements (persistent)
docs/
  00-verification-queue.md   ← unconfirmed facts we depend on
  01-contest-dossier.md      ← all rules, prizes, dates, jury, sources
  02-scoring-model.md        ← rubric exploitation strategy
  03-production-plan.md      ← 23-day schedule + credit budget
  04-platform-playbook.md    ← Higgsfield model selection guide
  05-council-protocol.md     ← roles, responsibilities, soul, memory rules
  06-concepts.md             ← the three candidate films
  07-reference-films.md      ← exemplar shorts to study
scripts/deadline.sh          ← countdown + early-warning level
film/                        ← script, shotlist, continuity bible, assets
campaign/                    ← engagement plan, posts, published prompts
```

---

## Style

Write like a film production, not like a software project. Short, concrete, decisive.
Numbers over adjectives. When something is unconfirmed, tag it `[VERIFY]` — never let
an assumption pass as a fact.
