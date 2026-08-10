#!/usr/bin/env bash
# Higgsfield Global Film Festival — the daily standup.
#
# The early-warning system's front end. deadline.sh answers "how long do we have";
# this answers "so what do we do today, and is anything actually on fire".
#
#   bash scripts/standup.sh            full report
#   bash scripts/standup.sh --brief    one line (for notifications, status bars)
#   bash scripts/standup.sh --notify   fire a desktop notification, then print
#
# Install it on a schedule:  bash scripts/install-reminders.sh
set -euo pipefail
cd "$(dirname "$0")/.."

MODE="${1:-full}"

DEADLINE_UTC="2026-09-01T06:59:59Z"
now_epoch=$(date -u +%s)
dl_epoch=$(date -u -d "$DEADLINE_UTC" +%s 2>/dev/null || date -u -jf "%Y-%m-%dT%H:%M:%SZ" "$DEADLINE_UTC" +%s)
secs=$(( dl_epoch - now_epoch ))
days=$(( secs / 86400 ))

# ── Level + the one directive that governs today ─────────────────────────────
# Phase discipline: what we are ALLOWED to be working on at this range. The
# point of a gate is that it closes. Past a gate, the previous phase is over.
if   [ "$secs" -le 0 ]; then
  LEVEL="CLOSED";   FOCUS="Submissions have closed."
elif [ "$days" -le 1 ]; then
  LEVEL="CRITICAL"; FOCUS="FINAL HOURS. Submit. Nothing else matters."
elif [ "$days" -le 3 ]; then
  LEVEL="RED";      FOCUS="Finishing, uploading, posting. No new shots. No re-cuts."
elif [ "$days" -le 7 ]; then
  LEVEL="ORANGE";   FOCUS="Picture is locked. Sound, watermark, and campaign only."
elif [ "$days" -le 14 ]; then
  LEVEL="YELLOW";   FOCUS="A rough cut must exist end-to-end. No new concepts."
else
  LEVEL="GREEN";    FOCUS="Build. Lock the concept, then generate — the calendar tightens without warning."
fi

# ── Next unpassed gate ───────────────────────────────────────────────────────
GATES="2026-08-10T23:59:59Z|Official project OPENS — verify submission mechanics
2026-08-12T23:59:59Z|GATE 1 · Concept locked + compliance cleared
2026-08-16T23:59:59Z|GATE 2 · Script, shotlist, character refs locked
2026-08-23T23:59:59Z|GATE 3 · Rough cut assembled end-to-end
2026-08-25T03:59:59Z|Adathon closes (concurrent contest)
2026-08-27T23:59:59Z|GATE 4 · Picture lock
2026-08-29T23:59:59Z|GATE 5 · Sound locked + final render + watermark
2026-08-30T23:59:59Z|GATE 6 · SUBMIT (24h safety margin)"

NEXT_GATE="—"; NEXT_IN=""
while IFS='|' read -r iso label; do
  [ -z "$iso" ] && continue
  g=$(date -u -d "$iso" +%s 2>/dev/null || date -u -jf "%Y-%m-%dT%H:%M:%SZ" "$iso" +%s)
  if [ "$g" -gt "$now_epoch" ]; then
    NEXT_GATE="$label"
    NEXT_IN=$(( (g - now_epoch) / 86400 ))
    break
  fi
done <<< "$GATES"

BRIEF="T-${days}d · ${LEVEL} · next: ${NEXT_GATE}"

if [ "$MODE" = "--brief" ]; then
  echo "$BRIEF"
  exit 0
fi

if [ "$MODE" = "--notify" ]; then
  title="Higgsfield T-${days}d · ${LEVEL}"
  if   command -v notify-send >/dev/null 2>&1; then
    notify-send -u normal "$title" "$FOCUS"
  elif command -v osascript   >/dev/null 2>&1; then
    osascript -e "display notification \"${FOCUS//\"/}\" with title \"${title//\"/}\""
  else
    printf '\a'   # no notifier available — ring the terminal instead of failing
  fi
fi

# ── Full report ──────────────────────────────────────────────────────────────
bash scripts/deadline.sh

echo "  TODAY"
printf "    Focus       %s\n" "$FOCUS"
if [ -n "$NEXT_IN" ]; then
  printf "    Next gate   %s  (T-%dd)\n" "$NEXT_GATE" "$NEXT_IN"
fi
echo ""

# Blockers are read live from STATE.md rather than hardcoded — the standup should
# never report a blocker we already cleared, or miss one we just found.
if [ -f memory/STATE.md ]; then
  echo "  FROM memory/STATE.md"
  grep -nE '^\s*[-*|].*(🔴|BLOCKED|BLOCKER)' memory/STATE.md 2>/dev/null \
    | head -8 | sed 's/^/    /' || echo "    (no blocker lines found)"
  echo ""
fi

cat <<'EOF'
  THE STANDUP QUESTIONS
    1. What moved since yesterday?
    2. What is on the critical path today?
    3. What is blocked, and who unblocks it?
    4. Are we still going to make the next gate — yes or no?

  Raise a RED FLAG immediately if a hard rule is at risk, the deadline has become
  unrecoverable, the budget is exhausted, or the film cannot place. Do not bury it.

EOF
