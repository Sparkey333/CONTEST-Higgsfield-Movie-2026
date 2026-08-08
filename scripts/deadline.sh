#!/usr/bin/env bash
# Higgsfield Global Film Festival — deadline countdown and early-warning system.
# Run at the start of every session:  bash scripts/deadline.sh
set -euo pipefail

# Aug 31 2026 23:59:59 PT (PDT = UTC-7)  ->  Sep 1 2026 06:59:59 UTC
DEADLINE_UTC="2026-09-01T06:59:59Z"
PROJECT_OPENS="2026-08-10T00:00:00Z"
ADATHON_UTC="2026-08-25T03:59:59Z"   # Aug 24 23:59:59 ET (EDT = UTC-4)

now_epoch=$(date -u +%s)
dl_epoch=$(date -u -d "$DEADLINE_UTC" +%s 2>/dev/null || date -u -jf "%Y-%m-%dT%H:%M:%SZ" "$DEADLINE_UTC" +%s)
po_epoch=$(date -u -d "$PROJECT_OPENS" +%s 2>/dev/null || date -u -jf "%Y-%m-%dT%H:%M:%SZ" "$PROJECT_OPENS" +%s)
ad_epoch=$(date -u -d "$ADATHON_UTC" +%s 2>/dev/null || date -u -jf "%Y-%m-%dT%H:%M:%SZ" "$ADATHON_UTC" +%s)

secs=$(( dl_epoch - now_epoch ))
days=$(( secs / 86400 ))
hours=$(( (secs % 86400) / 3600 ))

# ── Warning level ────────────────────────────────────────────────────────────
if   [ "$secs" -le 0 ];   then LEVEL="CLOSED";   COLOR="\033[1;30;41m"; MSG="Submissions have closed."
elif [ "$days" -le 1 ];   then LEVEL="CRITICAL"; COLOR="\033[1;97;41m"; MSG="FINAL HOURS. Submit now. Nothing else matters."
elif [ "$days" -le 3 ];   then LEVEL="RED";      COLOR="\033[1;31m";    MSG="Lock the cut. Only finishing, uploading, and posting from here."
elif [ "$days" -le 7 ];   then LEVEL="ORANGE";   COLOR="\033[1;33m";    MSG="Final week. Picture should be locked. Sound and campaign only."
elif [ "$days" -le 14 ];  then LEVEL="YELLOW";   COLOR="\033[1;93m";    MSG="Two weeks. Rough cut must exist. No new concepts."
else                           LEVEL="GREEN";    COLOR="\033[1;32m";    MSG="Build phase. Move fast — the calendar tightens without warning."
fi
R="\033[0m"

echo ""
echo -e "${COLOR}  HIGGSFIELD GLOBAL FILM FESTIVAL — ${LEVEL}  ${R}"
echo ""
printf "  Deadline    Aug 31, 2026 11:59 PM PT\n"
printf "  Remaining   %d days, %d hours\n" "$days" "$hours"
printf "  Status      %s\n" "$MSG"
echo ""

# ── Milestone gates ──────────────────────────────────────────────────────────
echo "  MILESTONE GATES"
gate () { # $1 = ISO date, $2 = label
  local g_epoch
  g_epoch=$(date -u -d "$1" +%s 2>/dev/null || date -u -jf "%Y-%m-%dT%H:%M:%SZ" "$1" +%s)
  local d=$(( (g_epoch - now_epoch) / 86400 ))
  if [ "$g_epoch" -le "$now_epoch" ]; then
    printf "    \033[1;31m[PASSED]\033[0m  %s\n" "$2"
  else
    printf "    [T-%-3s]  %s\n" "${d}d" "$2"
  fi
}
gate "2026-08-10T23:59:59Z" "Official festival project OPENS — verify submission mechanics"
gate "2026-08-12T23:59:59Z" "GATE 1 · Concept locked + compliance cleared"
gate "2026-08-16T23:59:59Z" "GATE 2 · Script, shotlist, character refs locked"
gate "2026-08-23T23:59:59Z" "GATE 3 · Rough cut assembled end-to-end"
gate "2026-08-25T03:59:59Z" "Adathon closes (concurrent contest)"
gate "2026-08-27T23:59:59Z" "GATE 4 · Picture lock"
gate "2026-08-29T23:59:59Z" "GATE 5 · Sound locked + final render + watermark"
gate "2026-08-30T23:59:59Z" "GATE 6 · SUBMIT (24h safety margin)"
echo ""

# ── Blockers ─────────────────────────────────────────────────────────────────
echo "  OPEN BLOCKERS"
echo "    [!] MCP credit balance was 0 — verify before any generation run"
echo "    [!] Rubric weights are [VERIFY] — confirm on the live contest page"
echo ""
echo "  Next: read memory/STATE.md, then memory/DECISIONS.md"
echo ""
