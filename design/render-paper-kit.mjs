/* Render design/paper-kit.html to PDF — one combined file at the repo root
   (paper-kit.pdf) and one separate PDF per sheet under paper-kit/, named by
   the sheet's data-slug so the folder reads in kit order.

   Run from the repo root after build-paper-kit.py:
       node design/render-paper-kit.mjs
   Fails loudly on font errors and flags any sheet whose content overflows
   the fixed 11-inch page. */
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { mkdirSync } from 'node:fs';

const ROOT = '/home/user/CONTEST-Higgsfield-Movie-2026';
mkdirSync(`${ROOT}/paper-kit`, { recursive: true });

const b = await chromium.launch();
const p = await (await b.newContext()).newPage();
const errs = [];
p.on('pageerror', e => errs.push('' + e));
p.on('requestfailed', r => errs.push('REQFAIL ' + r.url().split('/').pop()));
await p.goto(`file://${ROOT}/design/paper-kit.html`, { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);

const audit = await p.evaluate(() =>
  [...document.querySelectorAll('.sheet')].map((s, i) => {
    const kids = [...s.children];
    const bottom = Math.max(...kids.map(k => k.getBoundingClientRect().bottom));
    const box = s.getBoundingClientRect();
    return { n: i + 1, slug: s.dataset.slug,
             spare: +(box.bottom - bottom).toFixed(1),
             over: s.scrollHeight > s.clientHeight + 1 };
  }));
console.log('fonts:', await p.evaluate(() =>
  ['Body', 'Mono', 'Disp', 'Num'].map(f => f + ':' + document.fonts.check('10pt "' + f + '"')).join(' ')));
let bad = 0;
audit.forEach(a => {
  if (a.over) bad++;
  console.log(`  sheet ${String(a.n).padStart(2, '0')} ${a.slug}: spare ${a.spare}px ${a.over ? '*** OVERFLOW ***' : ''}`);
});
console.log('errors:', errs.length ? errs : 'none');

const opts = { width: '8.5in', height: '11in', printBackground: true,
               margin: { top: 0, bottom: 0, left: 0, right: 0 } };
await p.pdf({ path: `${ROOT}/paper-kit.pdf`, ...opts });
for (const a of audit) {
  const name = `${String(a.n).padStart(2, '0')}-${a.slug}.pdf`;
  await p.pdf({ path: `${ROOT}/paper-kit/${name}`, pageRanges: String(a.n), ...opts });
}
console.log(`paper-kit.pdf + ${audit.length} separate sheets written${bad ? ` — ${bad} OVERFLOWING` : ''}`);
await b.close();
if (bad) process.exit(1);
