# Contest Dossier — Higgsfield Global Film Festival

**Compiled:** 2026-08-08 · **Contest URL:** https://higgsfield.ai/contests/higgsfield-global-film-festival

> **Sourcing note.** `higgsfield.ai` is blocked by this environment's network egress
> proxy, so the official page could not be fetched directly. Every fact below was
> reconstructed from search-engine extractions of the official contest page plus
> corroborating secondary coverage. Each fact carries a confidence tag.
> **Anything tagged `[VERIFY]` must be confirmed against the live page before we
> rely on it.** See `docs/00-verification-queue.md` for the checklist.

---

## 1. The headline

| Item | Value | Confidence |
|---|---|---|
| Event | Higgsfield Global Film Festival | High |
| Total prize pool | **$1,000,000 cash** | High |
| Number of winners | **14** | High |
| Submissions open | **August 7, 2026** | High |
| Submissions close | **August 31, 2026, 11:59 PM PT** | High |
| Project workspace opens | **August 10, 2026** | High |
| Winners announced | Late September / early October 2026 | Medium |

**Days remaining as of 2026-08-08: 23.**

---

## 2. Prize breakdown

| Place | Prize |
|---|---|
| 🥇 1st | **$500,000** |
| 🥈 2nd | **$200,000** |
| 🥉 3rd | **$100,000** |
| 🏆 Audience Choice | **$100,000** |
| 🎖 Honorable Mentions (×10) | **$10,000 each** |
| | **= $1,000,000** |

The arithmetic closes exactly, which is a strong signal this breakdown is accurate.

**Strategic read:** there are two independent money paths. The jury path (1st/2nd/3rd)
and the **Audience Choice path ($100,000)**, which is decided by popularity rather
than jury verdict. A film can lose the jury and still take $100K. Ten Honorable
Mentions at $10K also mean the tail is unusually deep — placing *at all* is far more
achievable than in a normal winner-take-all contest.

---

## 3. Eligibility

- Open **worldwide**, wherever local law permits entry.
- Must be **18 or older**.
- Must have an **active Higgsfield subscription**.
- Enter **solo or as a team of up to 4 people**.

> ✅ **Our status: eligible.** Account is on the **Ultra** plan (confirmed live via the
> Higgsfield MCP `balance` call).

---

## 4. The film itself

| Requirement | Value | Confidence |
|---|---|---|
| Type | AI short film | High |
| Genre / subject | **Freeform — any story, any genre** | High |
| Runtime minimum | **3 minutes (hard floor)** | High |
| Runtime recommended | **3–5 minutes** | High |
| Entries per person/team | **Unlimited**, each must be a standalone film | High |
| Watermark | **Official Higgsfield watermark required on every upload** | High |
| Aspect ratio / resolution | **Not published in any source found** | `[VERIFY]` |
| File format / codec | **Not published in any source found** | `[VERIFY]` |
| Max runtime ceiling | **No ceiling found** — only a 3-min floor | `[VERIFY]` |

**The 3-minute floor is a hard disqualifier.** Deliver at 3:15–4:30 to leave safety
margin; never cut it close to 3:00.

**Unlimited entries is the single most exploitable rule in this contest.** See
`docs/02-scoring-model.md` §5.

---

## 5. How to enter

The official page frames this as **"Four steps from idea to award"**:

1. **Shape your idea, gather your crew** — any story, any genre, solo or team of ≤4.
2. **Create in Cinema Studio.** Work inside the official project, which **opens
   August 10**. Generate your shots there, from first try through final cut.
3. **Submit your film** — upload the final cut **with the Higgsfield watermark**, then
   share it in a **public post**. Submission is via public post, *not* a private form.
4. **The judging begins** — Screening → Shortlist → Jury verdict. Then the prize.

Plus: **publish your prompts and generation histories.** Entrants are required to make
the process behind the film public.

> **Cinema Studio is named explicitly as the creation environment.** It exposes
> **camera type, lens selection, movement, and style anchors including ARRI and
> Panavision** — which is, not coincidentally, exactly the vocabulary Papamichael
> judges in. Using those controls deliberately is a craft signal, not a preset choice.
> Corresponds to the `cinematic_studio_3_0` / Cinema Studio Video models in the MCP
> roster (`docs/04-platform-playbook.md`).

The page also promotes a tutorial track — **"Learn to make movies, not just
generations"** — covering AI realism, AI short film, and AI filmmaking. Worth mining.

> ⚠️ Two implications people will miss:
> - Because the work is expected to happen **inside the festival project**, generating
>   everything in a private side workspace may not count. `[VERIFY]` this on Aug 10.
> - Because **prompts and generation history are published**, the process is part of
>   the deliverable. A clean, legible, well-documented prompt trail is itself a
>   scored artifact — and it directly feeds the "Technical Execution" criterion.

---

## 6. Judging

### Structure — three stages

```
   ALL ENTRIES  ──►  SCREENING  ──►  SHORTLIST  ──►  JURY VERDICT
                    (most entries          (finalists)     (final placement)
                     eliminated here)
```

**Most entries are eliminated at Screening.** Screening is a filter, not a ranking.
Our first job is not to be brilliant — it is to be *un-eliminatable*: correct runtime,
correct watermark, correct rights, published prompts, public post. See the Catmull
agent's compliance gate.

### Published weighted criteria `[VERIFY — highest priority]`

| Criterion | Weight |
|---|---|
| Cinematic Quality | **25%** |
| Storytelling & Creativity | **25%** |
| Technical Execution | **20%** |
| Platform Engagement | **15%** |
| Social Media Engagement | **15%** |

This rubric is the most valuable single piece of intelligence we have. Full
exploitation analysis in `docs/02-scoring-model.md`.

### Jury — three judges, three different films

Confirmed from the official contest page (screenshot, 2026-08-08):

| Juror | Credentials | What they judge |
|---|---|---|
| **Edwin Catmull** | Pixar co-founder. **5× Oscar winner.** Ex-President of Pixar & Walt Disney Animation Studios. Executive producer, *Toy Story*. Turing Award laureate. | **Story. Character. Heart.** |
| **Phedon Papamichael** | **2× Oscar-nominated cinematographer** — *Nebraska* (2014) and *The Trial of the Chicago 7* (2021). Also *Ford v Ferrari* (BAFTA + ASC nominations, not an Oscar nomination), *Sideways*, *Walk the Line*, *3:10 to Yuma*, *The Descendants*, *Indiana Jones and the Dial of Destiny*. | **Light. Lens. Craft. Restraint.** |
| **Paul W. S. Anderson** | Billion-dollar franchise director. *Mortal Kombat*, the *Resident Evil* franchise, *Alien vs. Predator*, *Event Horizon*, *Monster Hunter*. Described on the page as *"the man who brought video games to the big screen."* | **Propulsion. Spectacle. Attention.** |

**This is the strategic crux, and it changed when the third name appeared.**

Reporting consistently notes this is the first contest from an AI-video vendor whose
jury is *not* internal marketing staff. These are career craftspeople who judge
**story, pacing, and sound**. Multiple sources state the jury **prioritizes
storytelling and directorial intent over technical polish**, and that *"a technically
flashy AI reel with nothing underneath it is not the play here, no matter how good the
render looks in isolation."*

But the three of them **do not want the same film**:

- **Catmull** built his career on the conviction that *story is king* and that
  technology serves it. He wrote *Creativity, Inc.* on protecting story from tech. He
  will not be impressed by a render. He will be impressed by a **character he cares
  about**.
- **Papamichael** is a *cinematographer*. He reads **lensing, blocking, motivated
  light, and coverage grammar** instantly, and will clock whether shots were *designed*
  or merely *generated*. He shot *Nebraska* in black and white — he is impressed by
  **right**, not by more.
- **Anderson** has spent thirty years mastering the discipline most art-house
  filmmakers never learn: **holding an audience's attention against its will.** He
  knows to the second where a viewer checks out. He builds set-pieces with legible
  geography. He is not sentimental and not fooled by prettiness.

> ⚠️ **Anderson's presence is the strongest signal we have that a beautiful, static,
> purely contemplative film will not sweep this contest.** A quiet festival short may
> win Catmull's vote and lose the room. The winning concept must carry **feeling
> through momentum** — heart *and* craft *and* propulsion.

This directly re-ranked our concepts. See `docs/06-concepts.md`.

---

## 7. Disqualifiers — the hard "no" list

Grounds for removal, and serious violations can mean a **permanent ban from future
contests**:

- ❌ **Copyrighted IP** — no movie characters, no brand logos.
- ❌ **Licensed music** — royalty-free or original composition **only**.
- ❌ Any content you do not hold the rights to.
- ❌ **Pornographic / NSFW** content.
- ❌ **Political statements.**
- ❌ **Religious statements.**

> ⚠️ **The political/religious ban is a serious creative constraint and is easy to
> trip accidentally.** A film about war, protest, a nation-state, a flag, a cross, a
> mosque, an election, or a named real-world conflict is at risk even if the intent is
> apolitical. Every concept must clear the Catmull agent's compliance gate before a
> single credit is spent. Allegory and invented worlds are the safe harbor: universal
> human stakes, no real-world referents.

---

## 8. Rights and ownership

- By entering, you **grant Higgsfield the right to feature your work** in galleries
  and promotional material.
- Entrants are **required to publish prompts and generation histories.**
- Full ownership/exclusivity terms not recoverable from secondary sources. `[VERIFY]`

**Practical implication:** do not build this film on top of anything you intend to
keep proprietary or sell exclusively elsewhere.

---

## 9. Open-sourced reference material — our free film school

As part of the festival, Higgsfield open-sourced its own productions with **every
prompt and asset public**:

| Title | What it is |
|---|---|
| **Hell Grind** | 95-minute AI feature. Made for **$500,000**. Screened at **Cannes Market**. Covered by **WSJ, Variety, BBC News**. Fully open-sourced: prompts, character model seeds, raw generation files, shot lists, complete workflow. |
| **Zephyr** | Open-sourced, prompts public. |
| **Mork** | Open-sourced, prompts public. |

Plus a **19-minute "How It Was Made" breakdown** of Hell Grind covering **character
design, crowd scale, and the battle sequence**, with real prompts on screen.

- Hell Grind: https://www.youtube.com/watch?v=t33k2tn4GpA
- Hell Grind — How It Was Made: https://www.youtube.com/watch?v=s-eeHOkkLss

**This is the answer key.** Higgsfield published the exact production methodology that
its own team considers award-grade — which is, transitively, a strong signal of what
its judging apparatus rewards. Mining these is the Braintrust agent's first assignment.

---

## 10. Concurrent Higgsfield contests (the "other tabs")

Other live contests at https://higgsfield.ai/contests — relevant because assets and
craft developed for the festival may be reusable, and because deadlines collide:

| Contest | Prize | Window |
|---|---|---|
| **Make Your Action Scene** | **$500K** in prizes | Opens Aug 7 → closes **Aug 31, 11:59 PM PT** |
| **Adathon** (with ADWEEK) | 1st: $50K credits + trip for 3; 2nd: $25K credits + trip | Jul 27, 9AM ET → **Aug 24, 11:59 PM ET** |
| **Seedance 2.0 Contest** | $50K total ($20K/$10K/$5K + 15×$1K) | **Closed** (winners selected early July 2026) |

> **"Make Your Action Scene" shares our exact deadline and is worth $500K.** If our
> festival film contains a strong action sequence, that sequence may be separately
> submittable. Anderson agent to assess double-dipping. `[VERIFY]` cross-entry rules.

---

## 11. Our resource position — ⚠️ ACTIVE BLOCKER

| Resource | Status |
|---|---|
| Subscription | **Ultra** ✅ eligible |
| **MCP credit balance** | **0 credits** 🔴 |
| Auto-refill | Disabled (eligible to enable) |

**We cannot generate a single frame through the MCP toolchain at 0 credits.** This is
the top-priority unblock — it gates all production work. Options:

- Enable auto-refill (threshold 300; options 2,000–30,000 credits) —
  https://higgsfield.ai/mcp-credits?show_modal=auto_refill&source=mcp
- One-time top-up — 4,000 credits / $190 (44% off) is the best rate;
  2,000 / $95 · 1,000 / $49 · 500 / $26. Top-up credits expire in 90 days.
- Ultra-plan credits may exist on the **web platform** separately from the MCP
  balance — worth checking before purchasing. `[VERIFY]`

Budget guidance lives in `docs/03-production-plan.md` §Credits.

---

## 12. Sources

- [Higgsfield Global Film Festival — official contest page](https://higgsfield.ai/contests/higgsfield-global-film-festival) *(egress-blocked; accessed via search extraction)*
- [Higgsfield Contests index](https://higgsfield.ai/contests)
- [@higgsfield_ai — festival announcement](https://x.com/higgsfield_ai/status/2084359051627131074)
- [@higgsfield — festival is live](https://x.com/higgsfield/status/2084369858138169509)
- [@higgsfield — Hell Grind open-sourced](https://x.com/higgsfield/status/2084702370764820572)
- [@higgsfield_ai — Hell Grind full tutorial](https://x.com/higgsfield_ai/status/2085042052618981582)
- [Edwin Catmull joins the jury (Facebook)](https://www.facebook.com/higgsfieldai.fb/posts/pixar-co-founder-edwin-catmull-joins-the-higgsfield-global-film-festival-as-a-ju/122195846426777614/)
- [AI Video Sensei — How to Actually Enter (2026)](https://aivideosensei.com/guides/higgsfield-global-film-festival-guide)
- [AI Film Contests — Best AI Film Festivals for Higgsfield Users](https://aifilmcontests.com/topics/best-ai-film-festivals-for-higgsfield-users)
- [RuntimeWire — $1M AI film contest with public project files](https://runtimewire.com/article/higgsfield-1-million-ai-film-festival-public-prompts)
- [AI News Blitz — Higgsfield launches $1M Global Film Festival](https://www.ainewsblitz.com/brief/oRGjTWuOPmRv)
- [Adweek — Higgsfield launches $85,000 Adathon with ADWEEK](https://www.adweek.com/creativity/higgsfield-ai-launches-85000-adathon-contest-in-partnership-with-adweek/)
- Higgsfield MCP — live `balance`, `show_plans_and_credits`, `models_explore` calls
