#!/usr/bin/env bash
# Install the festival reminder ladder into your user crontab.
#
# Durable, local, and needs no cloud permission — this is the fallback that always
# works. The richer option is Claude Routines (see docs/09-reminders.md), which can
# actually DO the work rather than just remind you of it.
#
#   bash scripts/install-reminders.sh            show what would be installed
#   bash scripts/install-reminders.sh --install  install it
#   bash scripts/install-reminders.sh --remove   remove it
#
# Times are LOCAL. Every entry fires a desktop notification and appends the full
# standup to reminders.log at the repo root.
set -euo pipefail
cd "$(dirname "$0")/.."
REPO="$PWD"

TAG="# higgsfield-festival-2026"
RUN="cd '$REPO' && bash scripts/standup.sh --notify >> '$REPO/reminders.log' 2>&1"

# Date-pinned entries mirror the milestone gates in docs/03-production-plan.md.
# Field order: minute hour day-of-month month day-of-week
read -r -d '' BLOCK <<EOF || true
$TAG start — managed by scripts/install-reminders.sh, do not hand-edit
12 8 * 8 *   $RUN   $TAG daily standup
0 9 10 8 *   $RUN   $TAG project opens — verify submission mechanics
0 9 12 8 *   $RUN   $TAG GATE 1 concept lock
0 9 16 8 *   $RUN   $TAG GATE 2 script + shotlist lock
0 9 23 8 *   $RUN   $TAG GATE 3 rough cut exists
0 9 27 8 *   $RUN   $TAG GATE 4 picture lock
0 9 29 8 *   $RUN   $TAG GATE 5 sound + watermark
0 8 30 8 *   $RUN   $TAG GATE 6 SUBMIT TODAY
0 8 31 8 *   $RUN   $TAG FINAL DAY — buffer only, deadline 11:59 PM PT
$TAG end
EOF

current() { crontab -l 2>/dev/null || true; }

case "${1:-}" in
  --install)
    { current | grep -vF "$TAG" || true; echo "$BLOCK"; } | crontab -
    echo "Installed. Active festival entries:"
    crontab -l | grep -F "$TAG" | grep -v 'start —\|end$'
    echo
    echo "Log: $REPO/reminders.log"
    ;;
  --remove)
    { current | grep -vF "$TAG" || true; } | crontab -
    echo "Removed all $TAG entries."
    ;;
  *)
    echo "DRY RUN — nothing installed. This is what --install would add:"
    echo
    echo "$BLOCK"
    echo
    echo "Run:  bash scripts/install-reminders.sh --install"
    ;;
esac
