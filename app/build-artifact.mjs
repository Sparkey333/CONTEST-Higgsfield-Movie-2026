/* Generates artifact.html from index.html.
 *
 * index.html is the single source of truth — a complete, standalone HTML document
 * you can open by double-clicking. The Artifact host supplies its own
 * <!doctype>/<head>/<body> skeleton, so the hosted copy must be body content only.
 * This strips the document shell and keeps the <style> block and everything inside
 * <body>, so the two never drift.
 *
 *   node build-artifact.mjs
 */
import fs from 'fs';
import path from 'path';

const dir = path.dirname(new URL(import.meta.url).pathname);
const src = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');

const style = src.match(/<style>[\s\S]*?<\/style>/);
const body  = src.match(/<body>([\s\S]*)<\/body>/);

if (!style) throw new Error('No <style> block found in index.html');
if (!body)  throw new Error('No <body> found in index.html');

const banner =
`<!-- Generated from index.html by build-artifact.mjs — do not edit directly.
     Edit index.html, then re-run: node build-artifact.mjs -->\n`;

const out = banner + style[0] + '\n' + body[1].trim() + '\n';
fs.writeFileSync(path.join(dir, 'artifact.html'), out);

const forbidden = /<\/?(?:!doctype|html|head|body)\b/i;
if (forbidden.test(out)) throw new Error('Output still contains document-shell tags');

console.log(`artifact.html written — ${out.length.toLocaleString()} bytes`);
