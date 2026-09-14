#!/bin/bash
# Production Desk — local launcher for macOS.
#
# Double-click this file. The FIRST time, macOS will refuse: right-click it,
# choose Open, then Open again. After that a plain double-click works.
#
# It serves this folder over http://localhost so the service worker can
# register — which is what lets you install the desk as a real Mac app with
# its own Dock icon. Close this window to stop the server.

set -u
cd "$(dirname "$0")" || exit 1

PORT=8733

# If something is already on the port, walk upward until a free one turns up.
while lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; do
  PORT=$((PORT + 1))
  if [ "$PORT" -gt 8760 ]; then
    echo "No free port between 8733 and 8760. Close whatever is using them and try again."
    read -r -p "Press return to close."
    exit 1
  fi
done

PY=""
for c in python3 /usr/bin/python3 /opt/homebrew/bin/python3 /usr/local/bin/python3; do
  if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
done

if [ -z "$PY" ]; then
  echo "python3 was not found."
  echo
  echo "You do not need it — just double-click index.html instead."
  echo "The only thing you lose is installing the desk as an app."
  echo
  read -r -p "Press return to close."
  exit 1
fi

URL="http://localhost:$PORT/index.html"

cat <<BANNER

  ────────────────────────────────────────────────
   PRODUCTION DESK
   Serving this folder at  $URL

   To install it as a Mac app:
     Chrome or Edge  →  File  →  Install page as app

   Leave this window open while you work.
   Close it, or press Control-C, to stop the server.
  ────────────────────────────────────────────────

BANNER

# Give the server a moment to bind before the browser asks for the page.
( sleep 1; open "$URL" ) &

exec "$PY" -m http.server "$PORT" --bind 127.0.0.1
