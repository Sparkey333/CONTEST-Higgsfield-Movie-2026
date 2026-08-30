# Production Control — the app

A single self-contained HTML file. No build step, no dependencies, no network. Open
[`index.html`](index.html) in any browser and it works — including offline, on a plane, on a
phone.

All state lives in `localStorage`, so it persists across reloads on that browser. **Export
regularly** (sidebar → Export) — the JSON round-trips through Import, and it's the only backup.

---

## What it does that the markdown can't

The documents in [`../docs/`](../docs/) are the reasoning. This is the instrument. Four things
here are computed, not written down:

### The monotony audit
Reads the framing + camera column as a sequence and flags any run of **three consecutive shots
sharing both shot size and camera move**. This is the single most common tell of a generated
shotlist, and it is *invisible* when you review shot by shot — it only appears when you read the
column. The app names the failing shot IDs.

### The sum check
Planned durations must total the target runtime **exactly**. A budget that doesn't add up ships
either dead air or an impossible cut, and the error stays hidden until you're on the timeline.
The gate goes green only on an exact match.

### The wargame harness
Live scoring across Film Grade (/50), Judge Fit (/30) and Make-ability (/20), with the four
multipliers applied. Move a slider and the ranking re-sorts. It also fires two specific warnings:
when Anderson's score is capping a concept, and when make-ability drops below 12/20 for a solo
creator — the trap of the best idea you cannot execute in the time available.

### The acceptance-rate tracker
Log generations and keeps per day; the app computes the running rate against the ~1.5% benchmark
and projects total burn against the 4,100-generation envelope. If your rate sits far below 1.5%,
the problem is upstream — usually the assets. Stop generating and fix the asset.

---

## Views

| View | Purpose |
|---|---|
| **Dashboard** | Countdown, runtime, locked shots, acceptance rate, six gates, credit burn, blockers |
| **Schedule** | All 24 days across six phases with gates. Ticking boxes clears dashboard blockers |
| **Daily Log** | Per-day generations/keeps, running acceptance rate |
| **Concepts** | Live ranked scoreboard |
| **Wargame** | The full scoring harness for one concept, plus kill criteria |
| **Ideas Inbox** | Raw capture, with spark prompts. Promote an idea straight into a scored concept |
| **Shot Ledger** | Editable ledger, both tempo gates, shot-length distribution vs target bands |
| **Prompt Builder** | Emits the Hell Grind block scaffold — GEO block, micro-life rule, silence lock, tag tail |
| **The Jury** | Each judge's rewards, punishes, and the strategic read |
| **Models** | Duration ceilings and routing; the Papamichael filter |

**Load 3-act skeleton** (Shot Ledger) seeds 26 shots totalling exactly 270s / 4:30, built to the
spine in [`../docs/04-SEQUENCE-ARCHITECTURE.md`](../docs/04-SEQUENCE-ARCHITECTURE.md) § 5. It
passes both gates and lands inside all four distribution bands — 3 anchors, 9 sustained,
7 connective, 7 bursts, with the bursts quarantined to a single passage.

---

## Tests

53 assertions driven through real Chromium via Playwright — including negative cases (the
monotony audit is deliberately broken and must catch it; the sum check is knocked out of balance
and must fail, then recover), persistence across reload, export, and a responsive check.

```bash
python3 -m http.server 8899 --bind 127.0.0.1 &   # from this directory
npm i playwright                                  # PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 if Chromium is preinstalled
node test.mjs
```

`test.mjs` writes screenshots to `screenshots/` (gitignored).

---

## Notes

- The dashboard clock is real — the countdown reflects the actual date against the internal
  Sept 1 deadline.
- `Reset` restores the six seed concepts and clears everything else. It asks first.
- The app makes no network requests of any kind.
