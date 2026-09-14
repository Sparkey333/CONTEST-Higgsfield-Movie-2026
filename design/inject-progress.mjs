// Bake design/progress.json into the bible so the progress bars are the
// verifier's numbers rather than a hand-typed guess.
//
//   node design/extract-data.mjs --prompts > /tmp/bible-data.json
//   python3 design/verify-steps.py /tmp/bible-data.json
//   node design/inject-progress.mjs
//
// Baked rather than fetched on purpose: the bible is read as a file, over a
// plain server, and as a published artifact, and fetch() fails in at least one
// of those. A value in the page works in all three.
import { readFileSync, writeFileSync } from "fs";

const root = new URL("..", import.meta.url);
const progress = JSON.parse(readFileSync(new URL("design/progress.json", root), "utf8"));
const file = new URL("director-bible.html", root);
let src = readFileSync(file, "utf8");

const START = "/* PROGRESS-DATA-START */";
const END = "/* PROGRESS-DATA-END */";
const block = `${START}\nconst PROGRESS=${JSON.stringify(progress)};\n${END}`;

const a = src.indexOf(START);
if (a < 0) throw new Error("no PROGRESS-DATA-START marker in director-bible.html");
const b = src.indexOf(END, a);
if (b < 0) throw new Error("no PROGRESS-DATA-END marker in director-bible.html");
src = src.slice(0, a) + block + src.slice(b + END.length);

writeFileSync(file, src);
const r = progress.rollup;
console.log(`injected: ${r.done}/${r.total} done, ${r.partial} partial, ${r.pct}% weighted, generated ${progress.generated}`);
