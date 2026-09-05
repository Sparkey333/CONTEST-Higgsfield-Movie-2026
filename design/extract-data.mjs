// Extract the director-bible's data arrays as JSON, so anything printed is
// generated from the same source the app runs on and cannot drift from it.
// Usage: node design/extract-data.mjs > /tmp/bible-data.json
import { readFileSync } from "fs";

const src = readFileSync(new URL("../director-bible.html", import.meta.url), "utf8");

// Pull one top-level `const NAME=[...];` block by bracket-matching from its
// opening `[` to the terminating `];` at line start.
function block(name) {
  const at = src.indexOf(`const ${name}=[`);
  if (at < 0) throw new Error(`missing const ${name}`);
  const end = src.indexOf("\n];", at);
  if (end < 0) throw new Error(`unterminated const ${name}`);
  return src.slice(at, end + 3);
}

const HF = "https://higgsfield.ai/";
const names = ["SHOTS", "PHASES", "FRAMES", "CHECKS", "PROC", "PREP", "RUN"];
const code = names.map(block).join("\n");

const out = {};
// The arrays are plain literals (RUN interpolates HF); evaluate in a bare scope.
new Function(
  "HF", "sink",
  code + `\nsink({${names.join(",")}});`
)(HF, (o) => Object.assign(out, o));

// Strip the huge prompt bodies the sheets don't print. --prompts keeps them:
// the Higgsfield snapshot matches generations back to assets by prompt text,
// so that consumer needs the bodies the printable kits never use.
const KEEP = process.argv.includes("--prompts");
for (const p of out.PREP) for (const v of p.v) { if (!KEEP) delete v.p; delete v.why; }
for (const s of out.SHOTS) for (const v of s.v) { if (!KEEP) delete v.p; delete v.why; }

process.stdout.write(JSON.stringify(out));
