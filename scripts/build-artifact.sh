#!/usr/bin/env bash
# Build the publishable fragment from the standalone app.
#
#   app/index.html            ← canonical, full HTML document (open locally, GitHub Pages)
#   app/void-room.artifact.html ← generated fragment for Claude Artifact publishing
#
# The Artifact host supplies its own <!doctype>/<html>/<head>/<body> wrapper, so the
# published file must contain the page content only. Everything else is identical —
# one source of truth, one derived file. Never hand-edit the generated file.
#
# Usage:  bash scripts/build-artifact.sh

set -euo pipefail
cd "$(dirname "$0")/.."

SRC="app/index.html"
OUT="app/void-room.artifact.html"

[ -f "$SRC" ] || { echo "missing $SRC" >&2; exit 1; }

python3 - "$SRC" "$OUT" <<'PY'
import io, re, sys

src, out = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8").read()

title = re.search(r"<title>(.*?)</title>", s, re.S).group(1)

# Everything the host would otherwise duplicate gets dropped: doctype, <html>,
# the <head> shell, and <body>. The <style> and <title> ride along inside the body.
css = re.search(r"<style>.*?</style>", s, re.S).group(0)
body = re.search(r"<body>(.*)</body>", s, re.S).group(1).strip()

io.open(out, "w", encoding="utf-8").write(
    "<title>%s</title>\n\n%s\n\n%s\n" % (title, css, body)
)

txt = io.open(out, encoding="utf-8").read()
# \b keeps <header> from tripping the <head> check.
leak = re.search(r"</?(!doctype|html|head|body)\b", txt, re.I)
assert not leak, "wrapper tag leaked into fragment: %s" % leak.group(0)

print("built %s (%d bytes) from %s" % (out, len(txt), src))
PY

# Sanity: the script inside must still parse.
if command -v node >/dev/null 2>&1; then
  python3 - "$OUT" <<'PY' > /tmp/voidroom.check.js
import io, re, sys
s = io.open(sys.argv[1], encoding="utf-8").read()
io.open(1, "w", encoding="utf-8", closefd=False).write(
    re.search(r"<script>(.*)</script>", s, re.S).group(1))
PY
  node --check /tmp/voidroom.check.js && echo "js ok"
  rm -f /tmp/voidroom.check.js
fi
