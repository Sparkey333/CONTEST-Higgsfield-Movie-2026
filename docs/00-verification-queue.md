# Verification Queue — Facts We Are Building On But Have Not Confirmed

**Why this file exists:** `higgsfield.ai` is blocked by this environment's network
egress proxy. The official contest page could not be fetched directly. Every contest
fact was reconstructed from search-engine extractions of that page plus corroborating
coverage.

Most of it is well-corroborated. Some of it is **load-bearing and unconfirmed**. This
file tracks the difference. **Catmull owns it. Braintrust audits it.**

---

## 🔴 P0 — Load-bearing. Confirm before Gate 1.

### 1. The scoring rubric weights
> Cinematic Quality 25% · Storytelling & Creativity 25% · Technical Execution 20% ·
> Platform Engagement 15% · Social Media Engagement 15%

**Why it matters:** our entire strategy — especially the 30%-engagement thesis in
`docs/02-scoring-model.md` — rests on this. If engagement is *not* 30%, Anderson's
priority drops sharply and resources should shift to craft.

**Appeared in:** one search extraction attributed to the official page.
**Corroborated by:** partially — multiple sources agree the jury prioritizes
storytelling over technical polish, consistent with a story-heavy weighting.
**How to confirm:** open the contest page in a normal browser and read the judging
section.

### 2. Aspect ratio, resolution, and file format requirements
**Status: no source found at all.** Not mentioned in any extraction or secondary
coverage.
**Why it matters:** a wrong deliverable spec is a Screening-stage disqualification.
**How to confirm:** the official project opens **Aug 10** — check the upload spec there.

### 3. Where the work must be produced
Sources say the project "opens Aug 10" and that you "generate your shots inside it."
**Unclear whether generating outside the project disqualifies an entry.**
**Why it matters:** determines whether MCP-driven generation counts.
**How to confirm:** Aug 10, in the project.

---

## 🟡 P1 — Should confirm before submission

### 4. Maximum runtime
Only a 3-minute **floor** was found, with 3–5 recommended. No ceiling located.
Assume 5 minutes is the practical maximum; target 3:15–4:30 regardless.

### 5. Audience Choice voting mechanics
$100,000 is confirmed. **How it's decided is not** — who votes, when, on what
platform, and whether views/likes/comments are weighted. Anderson's campaign can be
targeted much more precisely once known.

### 6. ~~Full jury roster~~ ✅ RESOLVED 2026-08-08
Confirmed from the official page (screenshot): **Edwin Catmull**, **Phedon
Papamichael**, and **Paul W. S. Anderson**. Three judges. Anderson's confirmation
triggered a concept-ranking revision — see `memory/DECISIONS.md` D-007.
*Still open:* whether further jurors are added before judging begins.

### 7. Cross-entry rules with concurrent contests
**Make Your Action Scene** ($500K) shares our Aug 31 deadline. Can one film — or a
sequence from it — enter both? Our portfolio strategy depends on the answer.

### 8. Rights and ownership terms in full
Confirmed: entering grants Higgsfield the right to feature the work in galleries and
promotions; prompts and generation history must be published. Exclusivity, duration,
and commercial-use terms unknown.

### 9. Watermark mechanics
Confirmed required. **How it is applied** — automatic on platform export vs. manual —
is unknown.

---

## 🟢 P2 — Confirmed and well-corroborated

These appeared consistently across multiple independent sources. Treat as reliable.

- $1,000,000 total pool, 14 winners
- $500K / $200K / $100K / $100K Audience Choice / 10 × $10K — **arithmetic closes exactly**
- Opens Aug 7 · **closes Aug 31, 11:59 PM PT**
- Project opens Aug 10
- Winners announced late Sept / early Oct
- 18+, worldwide where lawful, active Higgsfield subscription, teams up to 4
- 3-minute minimum, 3–5 recommended, any genre, freeform
- Unlimited entries, each standalone
- Watermark required; submission via public post; prompts must be published
- Judging: Screening → Shortlist → Jury verdict; most entries die at Screening
- Disqualifiers: copyrighted IP, brand logos, licensed music, NSFW, political
  statements, religious statements — serious violations can mean a permanent ban
- Hell Grind / Zephyr / Mork open-sourced with all prompts public

---

## Verification log

| Date | Item | Result | By |
|---|---|---|---|
| 2026-08-08 | Subscription = **Ultra** | ✅ Confirmed live via MCP `balance` | Catmull |
| 2026-08-08 | MCP credits = **0** | ✅ Confirmed live via MCP `balance` | Catmull |
| 2026-08-08 | Model roster + capabilities | ✅ Confirmed live via MCP `models_explore` | Phedon |
| | *P0 items pending* | ⬜ | |
