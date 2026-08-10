# The Early-Warning System

Twenty-one days is short enough that nobody forgets the deadline and long enough
that everybody forgets the *gates*. This is the machinery that makes the calendar
speak up on its own.

Three layers, in order of how much they can actually do for you.

---

## Layer 1 · On demand — always available

```bash
bash scripts/deadline.sh          # countdown, warning level, every milestone gate
bash scripts/standup.sh           # the above + today's focus + live blockers from STATE.md
bash scripts/standup.sh --brief   # one line: "T-21d · GREEN · next: GATE 1 …"
```

`standup.sh` reads blockers **live out of `memory/STATE.md`** rather than carrying its
own copy, so it can never report a blocker we already cleared or miss one we found an
hour ago.

The `--brief` line is meant for a status bar, a tmux segment, or a shell prompt:

```bash
# ~/.bashrc — the deadline follows you around
PS1="\[\033[2m\]\$(cd ~/CONTEST-Higgsfield-Movie-2026 && bash scripts/standup.sh --brief)\[\033[0m\]\n$PS1"
```

---

## Layer 2 · Local cron — durable, no permissions needed

Installs the whole gate ladder into your user crontab. Each entry fires a desktop
notification (`notify-send` on Linux, Notification Center on macOS, terminal bell as
fallback) and appends the full standup to `reminders.log`.

```bash
bash scripts/install-reminders.sh            # dry run — prints exactly what it would add
bash scripts/install-reminders.sh --install
bash scripts/install-reminders.sh --remove
```

| Local time | Fires |
|---|---|
| **8:12 AM daily, all August** | Daily standup |
| 9:00 AM · Aug 10 | Official project opens — verify submission mechanics |
| 9:00 AM · Aug 12 | **Gate 1** — concept locked + compliance cleared |
| 9:00 AM · Aug 16 | **Gate 2** — script, shotlist, character refs locked |
| 9:00 AM · Aug 23 | **Gate 3** — rough cut assembled end-to-end |
| 9:00 AM · Aug 27 | **Gate 4** — picture lock |
| 9:00 AM · Aug 29 | **Gate 5** — sound locked, final render, watermark |
| **8:00 AM · Aug 30** | **Gate 6 — SUBMIT TODAY** |
| 8:00 AM · Aug 31 | Final day — buffer only, deadline 11:59 PM PT |

Entries are tagged `# higgsfield-festival-2026`; `--remove` takes out exactly those and
touches nothing else in your crontab.

⚠️ Cron needs the machine awake. On a laptop that sleeps, this is a reminder system,
not a guarantee — pair it with Layer 3.

---

## Layer 3 · Claude Routines — the ones that do the work

Cron can only shout. A Routine wakes a **Claude session inside this repo**, which reads
`memory/STATE.md`, runs the standup, updates state, and commits — the difference between
being reminded the rough cut is due and finding out whether it exists.

**Status: not yet created.** Routine creation needs interactive approval, and the
session that built this ran headless. To create them, in an interactive session say:

> Create the festival Routines from `docs/09-reminders.md`.

### The specs, ready to create

Each runs in a **fresh session** so `CLAUDE.md` and the session-start protocol load
clean, and each is scoped to **report and escalate only** — no Routine spends credits,
generates footage, or posts publicly on its own.

| Routine | Schedule (UTC) | Local | Notify |
|---|---|---|---|
| `Higgsfield · Daily Standup (CATMULL)` | `12 15 * * *` | 8:12 AM PT daily | push |
| `Higgsfield · AUG 10 — Project opens` | one-shot `2026-08-10T16:05:00Z` | 9:05 AM PT | push + email |
| `Higgsfield · AUG 12 — Gate 1 concept lock` | one-shot `2026-08-12T16:00:00Z` | 9:00 AM PT | push |
| `Higgsfield · AUG 23 — Gate 3 rough cut` | one-shot `2026-08-23T16:00:00Z` | 9:00 AM PT | push |
| `Higgsfield · AUG 30 — SUBMIT DAY` | one-shot `2026-08-30T15:00:00Z` | 8:00 AM PT | push + email |
| `Higgsfield · AUG 31 — Final buffer` | one-shot `2026-08-31T15:00:00Z` | 8:00 AM PT | push + email |

Gates 2, 4 and 5 are deliberately left to the daily standup — it prints every gate, and
six separate alarms in three weeks is how people learn to ignore alarms.

#### Daily standup prompt

> HIGGSFIELD DAILY STANDUP. You are CATMULL (地 Earth). Run the session-start protocol
> in `CLAUDE.md`: read `memory/STATE.md`, run `bash scripts/standup.sh`, read
> `memory/DECISIONS.md` (do not relitigate anything settled there), skim
> `docs/00-verification-queue.md`.
>
> Report in exactly this shape, no longer: **T-minus / level** · **Next gate** (with a
> straight yes/no on whether we hit it) · **Blocked** · **Today's one thing** ·
> **RED FLAG** (only if a hard rule is at risk, the deadline is unrecoverable, the
> budget is exhausted, or the film cannot place).
>
> Update `memory/STATE.md` if anything changed and commit to
> `claude/higgsfield-film-festival-strategy-6ogspo` — a PR is already open for that
> branch; push to it, do not open another.
>
> If nothing has moved in 48 hours, say so plainly and name what is stalling it. A
> standup that reads fine while the project sits still is a failed standup. Do not spend
> credits, generate footage, or post publicly from this Routine.

#### Submit-day prompt (Aug 30)

> 🚨 AUG 30 — SUBMIT DAY. Per **D-003** we submit today; Aug 31 is buffer, not the plan.
>
> Run the final gate and report PASS/FAIL on every line.
>
> **COMPLIANCE — CATMULL, binding, any FAIL blocks submission:** runtime ≥ 3:00 (state
> the measured runtime) · official Higgsfield watermark on the uploaded file · no
> copyrighted IP, movie characters or brand logos in any frame · music royalty-free or
> original · no NSFW · no political statement · no religious statement · film is inside
> the official festival project · public post live with prompts and generation history
> published · team ≤ 4, all 18+, subscription active.
>
> **FINAL — BRAINTRUST, speaks last, holds the lock veto:** is this finished, or are we
> shipping something we know is broken?
>
> Then tell the human: submitted or not, and if not, exactly what is missing and how many
> hours it needs. Update `memory/STATE.md` and append to `memory/COUNCIL-LOG.md`.

---

## Why three layers

The deadline is the one thing in this project that cannot be renegotiated. A single
reminder channel that depends on a laptop being awake, a session being alive, or a
person remembering to run a script is a single point of failure on the only
unforgiving constraint we have.

Layer 1 works if you type it. Layer 2 works if the machine is on. Layer 3 works even
when nobody is looking — and it is the only one that can notice the rough cut doesn't
exist yet.
