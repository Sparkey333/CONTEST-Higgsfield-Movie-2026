# The Wargame — adversarial concept testing

> A concept that has not survived the wargame is an opinion. A concept that has is a
> plan.

Screening kills most entries. The jury kills most survivors. The wargame is where we
find out which one we are before we spend a credit.

This is not a brainstorm and it is not a vote. It is a **simulated jury** — five agents
arguing the way the three real jurors judge, scoring on a fixed scale, followed by a
kill attempt.

---

## 1. When to run it

| Trigger | Scope |
|---|---|
| Concept lock (Gate 1) | Full wargame, all five, all rounds |
| Any new concept proposed after lock | Full wargame — cheaper than a pivot at day 15 |
| Script lock (Gate 2) | Rounds 2–4 only |
| Rough cut (Gate 3) | Rounds 3–5, scored against the real cut |
| Picture lock (Gate 4) | Round 5 only — the kill attempt |

Never run it on a concept that has not cleared **Catmull's compliance gate.** Debating
the merits of a disqualified film is wasted council time.

---

## 2. The five seats and what each one is simulating

| Agent | Simulates | Real vote it predicts |
|---|---|---|
| **CATMULL** 地 | The Screening reader and the studio president | Whether we survive to be judged at all |
| **PHEDON** 水 | Papamichael, watching light and lens | **Craft — 25%** |
| **EDWIN** 火 | Catmull the storyteller, watching for heart | **Story — 25%** |
| **ANDERSON** 風 | Paul W. S. Anderson, watching the clock | **Engagement — 30%**, Audience Choice |
| **BRAINTRUST** 空 | The tired juror on entry #400 | The kill |

**They are not supposed to agree.** A concept that scores 5/5 with all five is almost
always a concept nobody understood. Braintrust must say so out loud when it happens.

---

## 3. The scoring dial

Every agent scores on the same 1–5 scale, in its own domain only. No agent scores
outside its domain — that is how the scores stay honest.

| Score | Means |
|---|---|
| **5** | Would win this criterion against the field |
| **4** | Strong; competitive but not distinctive |
| **3** | Competent; forgettable in a stack of four hundred |
| **2** | Actively weak; costs us the criterion |
| **1** | Fatal in this domain |

A score must be accompanied by **the specific thing that would raise it by one point.**
A score with no lever attached is an opinion, not a note.

### The weighted total

Because the rubric is not evenly weighted, neither is the wargame:

```
TOTAL = (Phedon × 25) + (Edwin × 25) + (Catmull × 20) + (Anderson × 30)
        ─────────────────────────────────────────────────────────────
                                  100
```

Anderson carries the largest single weight — 30% — because platform and social
engagement together outweigh any single craft criterion. Any instinct to treat his seat
as marketing is an instinct to forfeit the largest block on the board.

**A concept below 3.5 weighted does not go into production.** A concept below 3.0 in
*any single* domain does not go into production either, no matter how high the total —
a fatal weakness is not compensated by a strength elsewhere, because the jury does not
average, it remembers.

---

## 4. The five rounds

### Round 1 · The Gate (Catmull, solo, binding)

Before anyone discusses whether it is good. IP, characters, logos, music rights, NSFW,
**political content, religious content**, runtime feasibility, watermark, project
location, team eligibility. Output is **CLEAR** or **BLOCKED + the smallest change that
clears it.**

A BLOCKED concept stops here. Do not proceed to Round 2 to "see if it's worth fixing."

### Round 2 · The Cold Read (all five, independent, no cross-talk)

Each agent receives the concept alone and returns its score and its single strongest
objection. **Run these in parallel, in one message.** Independence is the point —
sequential reads contaminate each other, and a contaminated panel converges on the
first opinion it heard rather than on the truth.

### Round 3 · The Argument (cross-examination)

Each agent reads the other four cold reads and may revise its score **once**, stating
what changed its mind. An agent that revises toward the group without a stated reason
is collapsing into agreement, and Braintrust calls it.

This round is where the real jury's disagreement gets rehearsed: a concept that wins
Edwin and loses Anderson is the exact failure mode that a two-juror strategy would have
missed.

### Round 4 · The Repair (Edwin proposes, Catmull rules)

For each objection scoring 3 or below: the smallest change that raises it, and what
that change costs in the other four domains. Most repairs are trades. Name the trade.

A repair that raises one score and lowers two is not a repair.

### Round 5 · The Kill (Braintrust, solo, speaks last)

Braintrust stops arguing and tries to **destroy** the concept. Not critique — kill.

Five attack vectors, in order:

1. **The 400th entry.** A juror has watched six hours of AI shorts today. Yours starts.
   At what second do they reach for the next one? Name the second.
2. **The doppelgänger.** Someone else entered this exact idea. What is theirs, and why
   is it better? Assume it is better.
3. **The tell.** What in this film announces "AI" to a professional — drift, plastic
   light, restless camera, dead sound, uncanny hands? Name the shot.
4. **The shrug.** Grant that everything works. So what? What does anyone *feel*? If the
   honest answer is "it was well made," that is a loss.
5. **The disqualifier.** What did Catmull's gate miss because we described the concept
   more carefully than we will execute it?

Output is **SURVIVES** or **KILLED + the vector that killed it.**

Braintrust holds the lock veto. **A killed concept does not enter production**, however
much has already been invested in it. Sunk cost is not evidence.

---

## 5. The output format

Every wargame produces one record, appended to `film/wargames/`:

```markdown
# WARGAME — <concept name> — <date>

## Round 1 · Gate
CLEAR / BLOCKED — <reason> — <smallest fix>

## Round 2 · Cold read
| Agent | Score | Strongest objection | Lever to +1 |
|---|---|---|---|
| Catmull  | _/5 | | |
| Phedon   | _/5 | | |
| Edwin    | _/5 | | |
| Anderson | _/5 | | |
| Braintrust | _/5 | | |

## Round 3 · Revisions
<who changed, to what, and why>

## Round 4 · Repairs
<repair — what it costs elsewhere>

## Round 5 · Kill attempt
SURVIVES / KILLED — <vector>

## Weighted total
(Phedon×25 + Edwin×25 + Catmull×20 + Anderson×30) / 100 = __._

## Verdict
PRODUCE / REPAIR AND RE-RUN / DEAD
```

**Dead concepts stay in the folder.** The reasoning is worth more than the ruling, and
a concept killed in August is a concept we do not re-propose in a panic on the 27th.

---

## 6. Invoking it

Rounds 2 and 5 are the ones that matter. Round 2 must be parallel:

```
# Round 2 — one message, five agents, no cross-talk
Agent(subagent_type="catmull",    prompt="WARGAME R2 cold read. Concept: <...>. Score 1-5 on structure and feasibility, one strongest objection, one lever to +1.")
Agent(subagent_type="phedon",     prompt="WARGAME R2 cold read. Concept: <...>. Score 1-5 on craft. Can this be shot? What breaks first?")
Agent(subagent_type="edwin",      prompt="WARGAME R2 cold read. Concept: <...>. Score 1-5 on story. Do we care about anyone?")
Agent(subagent_type="anderson",   prompt="WARGAME R2 cold read. Concept: <...>. Score 1-5 on propulsion and engagement. Where do they check out?")
Agent(subagent_type="braintrust", prompt="WARGAME R2 cold read. Concept: <...>. Score 1-5 on originality. Who else made this?")

# Round 5 — after the argument and repairs
Agent(subagent_type="braintrust", prompt="WARGAME R5 kill attempt on <concept>, all five vectors. SURVIVES or KILLED.")
```

---

## 7. The rules that keep it honest

1. **Score in your domain only.** Anderson does not score lighting; Phedon does not
   score virality.
2. **Every score carries a lever.** What single change adds a point?
3. **Round 2 is blind.** No agent sees another's read before submitting its own.
4. **One revision each, with a reason.** Silent convergence is a failure.
5. **Braintrust speaks last and may kill.** Nothing is locked until it has tried.
6. **Unanimity is a red flag, not a green light.**
7. **A fatal domain score kills the concept regardless of the total.**
8. **The record is written whether we like the answer or not.**
