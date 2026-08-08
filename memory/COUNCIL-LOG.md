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
- Five-element council (Earth/Water/Fire/Wind/Void) in `.claude/agents/` — persistent
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
3. Wind starts posting
4. Void mines the Hell Grind breakdown
5. **Aug 10: enter the official project, verify everything, update the dossier**

---
