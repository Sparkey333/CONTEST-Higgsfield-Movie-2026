#!/usr/bin/env bash
# Double-click on a Mac: serves this folder on localhost so the desk can read project.json,
# then opens it. Clips play inline because the page is served, not opened as a file.
cd "$(dirname "$0")" || exit 1
command -v python3 >/dev/null || { echo "python3 is needed (xcode-select --install)"; read -r; exit 1; }
PORT=8741; while lsof -iTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; do PORT=$((PORT+1)); done
( sleep 0.8; open "http://localhost:$PORT/index.html" ) &
echo "anchorframe on http://localhost:$PORT — ctrl-C to stop"; python3 -m http.server "$PORT" --bind 127.0.0.1
