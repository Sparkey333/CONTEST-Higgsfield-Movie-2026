<div align="center">

# 🎬 CONTEST — Higgsfield Global Film Festival 2026

### `$1,000,000` · `14 winners` · `Deadline Aug 31, 2026 11:59 PM PT`

**地 EARTH · 水 WATER · 火 FIRE · 風 WIND · 空 VOID**

*The Council of Five*

</div>

---

## The mission

Win the **Higgsfield Global Film Festival** — a $1,000,000 AI film contest judged by
**Edwin Catmull** (5× Oscar winner, Pixar co-founder, ex-President of Walt Disney
Animation), **Phedon Papamichael** (2× Oscar-nominated cinematographer), and
**Paul W. S. Anderson** (*Mortal Kombat*, *Resident Evil*, *Event Horizon*).

**Deliverable:** a 3–5 minute AI short film. Any story, any genre. Watermarked,
published by public post, with all prompts and generation history made public.

| Prize | Amount |
|---|---|
| 🥇 1st | **$500,000** |
| 🥈 2nd | **$200,000** |
| 🥉 3rd | **$100,000** |
| 🏆 Audience Choice | **$100,000** |
| 🎖 10 × Honorable Mention | **$10,000 each** |

---

## 🎟 The Void Room — our theater

Everything in this repo is also a **single self-contained web app**:
**[`app/index.html`](app/index.html)** — a small repertory cinema with four rooms.

### ▶ **[Open The Void Room](https://claude.ai/code/artifact/6cc9a223-2104-418d-9ac3-de09167d3f07)**

*Published and shareable. Private until shared from the page's share menu.*

| Room | What's in it |
|---|---|
| **01 · The Mission** | Live countdown, prize ladder, the three-judge jury, rubric, milestone gates, open blockers |
| **02 · The Council** | The five agents, their patrons, and the one line each would die on |
| **03 · The Library** | The short-film library — **drag any title to re-rank it or move it between tiers.** Saves to your browser |
| **04 · The Theater** | A 3D auditorium. Drag to look around, hang a poster on the screen, watch from the seats |

Every room is hash-routed, so any room links directly — `…/artifact/…#library`,
`#theater`, `#council`, `#mission`.

No dependencies, no network calls, one file. Two forms of it:

| File | For |
|---|---|
| [`app/index.html`](app/index.html) | **The source.** A complete HTML document — open it locally, or serve it |
| [`app/void-room.artifact.html`](app/void-room.artifact.html) | Generated fragment for publishing. Never hand-edit |

```bash
bash scripts/build-artifact.sh   # regenerate the fragment after editing app/index.html
```

---

## Start here

```bash
bash scripts/deadline.sh        # countdown, warning level, milestone gates
bash scripts/standup.sh         # the above + today's focus + live blockers
```

Then read, in order:

1. **[`memory/STATE.md`](memory/STATE.md)** — where we are right now
2. **[`memory/DECISIONS.md`](memory/DECISIONS.md)** — what is already settled
3. **[`docs/00-verification-queue.md`](docs/00-verification-queue.md)** — what we
   haven't confirmed yet

---

## The jury

| Juror | Credentials | Wants |
|---|---|---|
| **Edwin Catmull** | Pixar co-founder · 5× Oscar · ex-President, Disney Animation · Turing Award | **Heart** |
| **Phedon Papamichael** | 2× Oscar-nominated cinematographer · *Nebraska*, *Ford v Ferrari* | **Craft** |
| **Paul W. S. Anderson** | *Mortal Kombat* · *Resident Evil* · *Alien vs. Predator* · *Event Horizon* | **Propulsion** |

⚠️ **They do not want the same film.** A beautiful, static, contemplative short wins
Catmull's vote and loses the room. The winner carries *feeling through momentum*.

---

## The Council of Five

Five persistent agents built on the **Godai** — the five elements Musashi used to
organize mastery in *The Book of Five Rings* — each named for and aligned in spirit
with a member of the jury. Their disagreement is the quality mechanism.

| | Agent | Element | Patron | Asks |
|---|---|---|---|---|
| 地 | **[CATMULL](.claude/agents/catmull.md)** | Earth | Catmull, *the President* | *Does it hold?* |
| 水 | **[PHEDON](.claude/agents/phedon.md)** | Water | Papamichael | *Does it flow?* |
| 火 | **[EDWIN](.claude/agents/edwin.md)** | Fire | Catmull, *the Storyteller* | *Do we care?* |
| 風 | **[ANDERSON](.claude/agents/anderson.md)** | Wind | Paul W. S. Anderson | *Why are they still watching?* |
| 空 | **[BRAINTRUST](.claude/agents/braintrust.md)** | Void | Catmull's Pixar Braintrust | *What are we missing?* |

**Catmull holds compliance veto. Edwin holds the spine. Braintrust speaks last.**
Full doctrine: **[`docs/05-council-protocol.md`](docs/05-council-protocol.md)**

---

## The strategy in one paragraph

The rubric is **Cinematic 25 · Storytelling 25 · Technical 20 · Platform Engagement 15
· Social Engagement 15**. That means **30% of the score is engagement** — the only
criterion where effort converts to points almost linearly, and the one virtually every
entrant treats as paperwork. Meanwhile the jury is composed of career craftspeople who
explicitly reward story over polish, so the film itself must be a *wordless emotional
short* in the Pixar register rather than a flashy AI reel. We build one deeply-felt
film, run a disciplined 23-day campaign alongside it, and submit a day early.

Full analysis: **[`docs/02-scoring-model.md`](docs/02-scoring-model.md)**

---

## The map

| File | What it is |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Auto-loaded project memory + session protocol |
| [`docs/00-verification-queue.md`](docs/00-verification-queue.md) | Unconfirmed facts we depend on |
| [`docs/01-contest-dossier.md`](docs/01-contest-dossier.md) | Every rule, prize, date, jury detail, source |
| [`docs/02-scoring-model.md`](docs/02-scoring-model.md) | Rubric decoded into a plan of attack |
| [`docs/03-production-plan.md`](docs/03-production-plan.md) | 23-day schedule, gates, credit budget |
| [`docs/04-platform-playbook.md`](docs/04-platform-playbook.md) | Higgsfield model selection guide |
| [`docs/05-council-protocol.md`](docs/05-council-protocol.md) | Roles, responsibilities, memory, soul |
| [`docs/06-concepts.md`](docs/06-concepts.md) | The three candidate films |
| [`docs/07-reference-films.md`](docs/07-reference-films.md) | Exemplar shorts + what to steal |
| [`docs/08-film-library.md`](docs/08-film-library.md) | The 16-film library, flat mirror of The Library room |
| [`docs/09-reminders.md`](docs/09-reminders.md) | The three-layer early-warning system |
| [`memory/`](memory/) | State, decisions, session log |
| [`app/index.html`](app/index.html) | The Void Room — the whole repo as one web app |
| [`scripts/deadline.sh`](scripts/deadline.sh) | Countdown, warning level, milestone gates |
| [`scripts/standup.sh`](scripts/standup.sh) | Daily standup — countdown + focus + live blockers |
| [`scripts/install-reminders.sh`](scripts/install-reminders.sh) | Install the gate ladder into cron |
| [`scripts/build-artifact.sh`](scripts/build-artifact.sh) | Rebuild the publishable fragment from the app |

---

## Milestone gates

| Gate | Date | Requirement |
|---|---|---|
| — | **Aug 10** | Official project opens — verify submission mechanics |
| **1** | Aug 12 | Concept locked + compliance cleared |
| **2** | Aug 16 | Script, shotlist, character refs locked |
| **3** | Aug 23 | Rough cut assembled end-to-end |
| **4** | Aug 27 | Picture lock |
| **5** | Aug 29 | Sound locked, final render, watermark verified |
| **6** | **Aug 30** | **SUBMIT** — Aug 31 is buffer only |

Make the calendar speak up on its own:

```bash
bash scripts/install-reminders.sh            # dry run — shows what it would add
bash scripts/install-reminders.sh --install  # desktop alerts on every gate above
```

Full ladder, including the Claude Routines that run the standup for you:
**[`docs/09-reminders.md`](docs/09-reminders.md)**

---

## Hard constraints — never violate

❌ No copyrighted IP, movie characters, or brand logos
❌ No licensed music — royalty-free or original only
❌ No NSFW · ❌ **No political statements** · ❌ **No religious statements**
✅ Runtime ≥ 3:00 · ✅ Higgsfield watermark · ✅ Public post + published prompts

*Serious violations can mean a permanent ban from future contests.*

---

<div align="center">

**Contest page:** [higgsfield.ai/contests/higgsfield-global-film-festival](https://higgsfield.ai/contests/higgsfield-global-film-festival)

*"There is nothing outside of yourself that can ever enable you to get better,
stronger, richer, quicker, or smarter. Everything is within."* — Musashi

</div>
