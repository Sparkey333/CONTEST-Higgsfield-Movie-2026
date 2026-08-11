# COUNCIL LOG

Running session record. **Append a new entry at the end of every session.** Newest at
the bottom. This is how the council remembers what it has already tried.

Format: date · phase · what happened · what changed · what's next.

---

## 2026-08-08 · Session 001 · Founding

**Phase:** Pre-production · **T-23 days** · **Level:** 🟢 GREEN

### What happened

**Intelligence.** `higgsfield.ai` turned out to be blocked by this environment's
network egress proxy, as were every third-party guide we tried. Reconstructed the full
contest picture from search-engine extractions of the official page plus corroborating
coverage across 11 sources, then confirmed our own account state directly through the
Higgsfield MCP.

**Key findings:**
- $1,000,000 · 14 winners · $500K/$200K/$100K/$100K Audience Choice/10×$10K
- Closes **Aug 31, 11:59 PM PT**; official project opens **Aug 10**
- Jury: **Edwin Catmull** (5× Oscar, Pixar co-founder), **Phedon Papamichael** (2×
  Oscar-nominated cinematographer). Not internal marketing staff — career craftspeople
  who judge story, pacing, and sound.
- **Weighted rubric found:** Cinematic 25 · Story 25 · Technical 20 · Platform
  Engagement 15 · Social Engagement 15
- Screening → Shortlist → Jury. **Most entries die at Screening.**
- Entries are **unlimited**. Prompts and generation history must be **published**.
- Hard bans include **political and religious statements** — a serious creative
  constraint most entrants will underestimate.
- Hell Grind / Zephyr / Mork fully open-sourced with every prompt public.

**Two findings that reshaped the strategy:**
1. **30% of the score is engagement** — the least contested surface in the contest.
   Became D-002.
2. **MCP credit balance is 0** on an Ultra plan. Hard blocker on all generation.

### What was built
- Five-element council (Catmull/Phedon/Edwin/Anderson/Braintrust) in `.claude/agents/` — persistent
- `CLAUDE.md` project memory with session-start protocol
- `memory/` ledger: STATE, DECISIONS, COUNCIL-LOG
- Full docs set: dossier, verification queue, scoring model, production plan,
  platform playbook, council protocol, concepts, reference films
- `scripts/deadline.sh` — countdown, warning levels, milestone gates
- Decisions D-001 through D-005 ratified

### Decisions made
D-001 council · D-002 engagement is first-class · D-003 submit Aug 30 ·
D-004 wordless film · D-005 runtime 3:15–4:30

### Open at session end
- 🔴 **Credits = 0** — blocks all generation
- 🔴 **Campaign not started** — forfeiting engagement score daily
- 🟡 Concept not ratified (council recommends A · *Understudy*)
- 🟡 P0 verification items outstanding — rubric weights, aspect ratio, project rules

### Next session
1. Unblock credits
2. Full council review → ratify the concept (Gate 1, Aug 12)
3. Anderson starts posting
4. Braintrust mines the Hell Grind breakdown
5. **Aug 10: enter the official project, verify everything, update the dossier**

---

## 2026-08-08 · Session 002 · The Third Juror

**Phase:** Pre-production · **T-23 days** · **Level:** 🟢 GREEN

### What happened

A screenshot of the official contest page surfaced a fact no text source had given us:
**there is a third judge — Paul W. S. Anderson.** *Mortal Kombat*, the *Resident Evil*
franchise, *Alien vs. Predator*, *Event Horizon*. The page bills him as "the man who
brought video games to the big screen."

Confirmed via search: the festival describes a juror as a "billion dollar franchise
director… director of Mortal Kombat, Resident Evil franchise and Alien vs. Predator."

**Also captured from the page:**
- Entry flow framed as **"Four steps from idea to award"** — shape the idea and gather
  a crew → **create in Cinema Studio** → submit the film → judging begins.
- **Cinema Studio** is named explicitly as the creation environment. It exposes camera
  type, lens, movement, and style anchors including **ARRI and Panavision** — which is
  precisely the vocabulary Papamichael judges in.
- A tutorial track: *"Learn to make movies, not just generations."*
- Confirms $1,000,000 / fourteen winners / Audience Choice / 10 Honorable Mentions.

### Why it mattered

Our entire concept ranking had assumed a two-person jury: Catmull (story) and
Papamichael (light). On that basis we recommended the quietest, most intimate concept —
a wordless puppeteer film. **That was a one-vote-of-three strategy.**

Anderson has spent thirty years on the one discipline most festival filmmakers never
learn: holding an audience against its will. A beautiful, static, contemplative short
loses his vote outright.

### Decisions made

- **D-006** — the council is renamed for the jury. Each agent now argues the way its
  patron judges, so internal review rehearses the real one:
  **CATMULL** (地) · **PHEDON** (水) · **EDWIN** (火) · **ANDERSON** (風) ·
  **BRAINTRUST** (空). Catmull holds two seats; Braintrust is named for his own Pixar
  candid-feedback council.
- **D-007** — concept ranking revised. **C · *Tidewalker*** becomes primary: the only
  concept scoring ★★★★+ with all three jurors, with a built-in ticking clock, the
  strongest Audience Choice hook, and a double-dip into *Make Your Action Scene*.
  *Understudy* moves to secondary; *The Keeper* stays the reserve pivot.

### Open at session end

- 🔴 Credits still 0 — blocks all generation
- 🔴 Campaign still not started
- 🟡 Concept revision not yet ratified through the full gate
- 🟡 Deadline reminder Routines not yet created

### Next session

1. Unblock credits
2. Ratify *Tidewalker* through the full council gate (Gate 1, Aug 12)
3. **Phedon: test a returning-tide shot before Gate 1** — if it can't be made to work,
   pivot to *The Keeper* now, not at day 15
4. Anderson starts posting
5. Aug 10: enter the project, verify Cinema Studio submission mechanics

---

## 2026-08-10 · Session 003 · The Void Room opens

**Phase:** Pre-production · **T-21 days** · **Level:** 🟢 GREEN

### What happened

Two pieces of infrastructure that had been outstanding since Session 001 got finished:
the project became a **place** you can walk into, and the calendar learned to speak.

**The Void Room shipped.** The whole repo — mission, jury, council, library, theater —
is now one self-contained page with no dependencies and no network calls. The film
library grew from 8 titles to **16 across four tiers**, top tier preserved as
instructed; every entry can be dragged to re-rank or moved between tiers, and the
order persists in the browser. The fourth room is a CSS-3D auditorium with procedural
SVG posters for our own three concepts.

Published and shareable:
**https://claude.ai/code/artifact/6cc9a223-2104-418d-9ac3-de09167d3f07**

Split into a source document and a generated publish fragment (`scripts/build-artifact.sh`)
so there is exactly one place to edit and no chance of the two drifting apart.

**The early-warning system was built out to three layers** (`docs/09-reminders.md`):
`standup.sh` on demand, a cron ladder covering all six gates, and Claude Routines that
wake a session in the repo and actually run the standup.

### What did not happen

**The Routines were not created.** Creating one requires interactive approval and this
session ran headless — two attempts, both refused at the permission layer. This is
called out rather than buried: layers 1 and 2 are live and layer 3 is written, specced,
and one sentence away in any interactive session. Reported to the human directly.

### Open at session end

- 🔴 Credits still 0 — blocks all generation
- 🔴 Campaign still not started — T-21 and every silent day is forfeited score
- 🟡 Concept revision (*Tidewalker*) not yet ratified through the full gate
- 🟡 Routines pending human approval
- 🟡 **Aug 10 is today** — the official project opens; submission mechanics unverified

### Next session

1. Unblock credits
2. **Enter the official project and verify submission mechanics** — this is today's job
3. Ratify *Tidewalker* through the full council gate (Gate 1, Aug 12 — T-2)
4. Anderson starts posting
5. Create the Routines

---
