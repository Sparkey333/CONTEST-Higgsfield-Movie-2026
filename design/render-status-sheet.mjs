/* Render design/status-sheet.html to status.pdf at the repo root.
   Fails loudly on page errors and on any sheet that overflows 11in — a status
   sheet that silently drops its last row is worse than no status sheet. */
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const ROOT = '/home/user/CONTEST-Higgsfield-Movie-2026';
const b = await chromium.launch();
const p = await (await b.newContext()).newPage();
const errs = [];
p.on('pageerror', e => errs.push('' + e));
await p.goto(`file://${ROOT}/design/status-sheet.html`, { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
const audit = await p.evaluate(() =>
  [...document.querySelectorAll('.sheet')].map((s, i) => {
    const kids = [...s.children].filter(k => !k.classList.contains('fn'));
    const bottom = Math.max(...kids.map(k => k.getBoundingClientRect().bottom));
    const fn = s.querySelector('.fn');
    const limit = fn ? fn.getBoundingClientRect().top : s.getBoundingClientRect().bottom;
    return { n: i + 1, spare: +(limit - bottom).toFixed(1) };
  }));
await p.pdf({ path: `${ROOT}/status.pdf`, format: 'Letter', printBackground: true });
await b.close();
audit.forEach(a => console.log(`sheet ${a.n}: ${a.spare}px spare${a.spare < 0 ? '  ** OVERFLOW **' : ''}`));
if (errs.length) { console.error(errs.join('\n')); process.exit(1); }
if (audit.some(a => a.spare < 0)) process.exit(2);
console.log('status.pdf written');
