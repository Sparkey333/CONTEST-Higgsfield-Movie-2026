#!/usr/bin/env bash
# Dev server for the Production Control app.
#
#   ./serve.sh          # serve on 8899
#   ./serve.sh 3000     # serve on a different port
#
# The app is a static self-contained file, so any static server works — this
# exists so the port and root are consistent between runs and match test.mjs.
#
# You do not need this to *use* the app: open index.html directly in a browser
# and it works, offline, with no server at all. The server is here so headless
# browsers (Playwright) can drive it over http:// and so localStorage gets a
# stable origin between runs — file:// origins are treated inconsistently
# across browsers and would lose saved state.

set -euo pipefail

PORT="${1:-8899}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found. Any static server works — e.g.: npx serve '$ROOT'" >&2
  exit 1
fi

if command -v ss >/dev/null 2>&1 && ss -ltn 2>/dev/null | grep -q ":${PORT} "; then
  echo "Port ${PORT} is already in use. Stop it first, or pass another port: ./serve.sh 3000" >&2
  exit 1
fi

echo "Production Control  →  http://127.0.0.1:${PORT}/index.html"
echo "Root: ${ROOT}"
echo "Ctrl-C to stop."
exec python3 -m http.server "${PORT}" --bind 127.0.0.1 --directory "${ROOT}"
