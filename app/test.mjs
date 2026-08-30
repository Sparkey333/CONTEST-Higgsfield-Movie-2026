import { chromium } from 'playwright';
import fs from 'fs';

const EXE  = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const URL  = 'http://127.0.0.1:8899/index.html';
const SHOT = '/home/user/CONTEST-Higgsfield-Movie-2026/app/screenshots';
fs.mkdirSync(SHOT, { recursive: true });

const pass = [], fail = [];
const ok  = (n, c, extra='') => (c ? pass : fail).push(n + (extra ? ` — ${extra}` : ''));

const browser = await chromium.launch({ executablePath: EXE, args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 1440, height: 950 } });

const errors = [];
page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
page.on('dialog', d => d.accept());

await page.goto(URL, { waitUntil: 'networkidle' });
await page.evaluate(() => localStorage.clear());
await page.reload({ waitUntil: 'networkidle' });

// ---------- 1. boot ----------
ok('Page boots with no JS errors', errors.length === 0, errors.join(' | '));
ok('Title correct', (await page.title()).includes('Ghost Light'));
ok('Sidebar has 10 nav items', (await page.locator('#nav button').count()) === 10);

// ---------- 2. dashboard ----------
const days = await page.locator('#dDays').textContent();
ok('Countdown computes', /^\d+$/.test(days.trim()), `= ${days}`);
ok('Gates rendered', (await page.locator('#gates .card').count()) === 6);
ok('Blockers surface on empty state', (await page.locator('#blockers .alert').count()) >= 2);
ok('Top concept card present', await page.locator('#dTop .ccard').isVisible());
const topName = await page.locator('#dTop .ccard h4').textContent();
ok('Top concept is Vantage (95.7)', topName.includes('Vantage'), topName.trim());
await page.screenshot({ path: `${SHOT}/01-dashboard-empty.png`, fullPage: true });

// ---------- 3. concepts ranking ----------
await page.click('[data-p="concepts"]');
const cards = await page.locator('#conceptList .ccard').count();
ok('All 6 seed concepts render', cards === 6, `got ${cards}`);
const scores = await page.locator('#conceptList .score').allTextContents();
const nums = scores.map(parseFloat);
ok('Concepts sorted descending', nums.every((v, i) => i === 0 || nums[i-1] >= v), scores.join(', '));
ok('Vantage scores 95.7', Math.abs(nums[0] - 95.7) < 0.05, String(nums[0]));
await page.screenshot({ path: `${SHOT}/02-concepts.png`, fullPage: true });

// ---------- 4. ledger + gates ----------
await page.click('[data-p="ledger"]');
await page.click('#shotSeed');
await page.waitForTimeout(250);
const rows = await page.locator('#shotBody tr').count();
ok('Skeleton loads 26 shots', rows === 26, `got ${rows}`);
const sumAlert = await page.locator('#gateSum .alert').getAttribute('class');
ok('Sum check passes after seed', sumAlert.includes('ok'), sumAlert);
const monoAlert = await page.locator('#gateMono .alert').getAttribute('class');
ok('Monotony audit clean on skeleton', monoAlert.includes('ok'), monoAlert);
const stats = await page.locator('#shotStats').textContent();
ok('Shot stats computed', stats.includes("26 shots"), stats.trim());
await page.screenshot({ path: `${SHOT}/03-ledger.png`, fullPage: true });

// ---------- 5. monotony DETECTION (deliberately break it) ----------
// rows 1,2,3 -> make framing+camera identical
for (const i of [0, 1, 2]) {
  await page.fill(`#shotBody tr:nth-child(${i+1}) input[data-f="framing"]`, 'MEDIUM');
  await page.fill(`#shotBody tr:nth-child(${i+1}) input[data-f="camera"]`, 'slow push-in');
}
await page.waitForTimeout(250);
const monoBad = await page.locator('#gateMono .alert').getAttribute('class');
ok('Monotony audit CATCHES a 3-run', monoBad.includes('bad'), monoBad);
const monoTxt = await page.locator('#gateMono').textContent();
ok('Monotony names the failing shots', /1a\s*→\s*2a\s*→\s*2b/.test(monoTxt), monoTxt.slice(0, 160));
await page.screenshot({ path: `${SHOT}/04-monotony-fail.png`, fullPage: true });

// dashboard should now show the blocker
await page.click('[data-p="dash"]');
const dashTxt = await page.locator('#blockers').textContent();
ok('Dashboard surfaces monotony blocker', dashTxt.includes('Monotony audit failing'));

// revert
await page.click('[data-p="ledger"]');
await page.fill('#shotBody tr:nth-child(1) input[data-f="framing"]', 'WIDE');
await page.fill('#shotBody tr:nth-child(1) input[data-f="camera"]', 'static hold');
await page.fill('#shotBody tr:nth-child(3) input[data-f="framing"]', 'CLOSE');
await page.fill('#shotBody tr:nth-child(3) input[data-f="camera"]', 'static hold');
await page.waitForTimeout(200);
ok('Monotony clears after fix',
   (await page.locator('#gateMono .alert').getAttribute('class')).includes('ok'));

// ---------- 6. sum check breaks when duration edited ----------
await page.fill('#shotBody tr:nth-child(1) input[data-f="dur"]', '40');
await page.waitForTimeout(200);
ok('Sum check FAILS when runtime drifts',
   (await page.locator('#gateSum .alert').getAttribute('class')).includes('warn'));
await page.fill('#shotBody tr:nth-child(1) input[data-f="dur"]', '25');
await page.waitForTimeout(200);
ok('Sum check recovers',
   (await page.locator('#gateSum .alert').getAttribute('class')).includes('ok'));

// ---------- 7. status -> locked propagates to dashboard ----------
await page.selectOption('#shotBody tr:nth-child(1) select[data-f="status"]', '🟢');
await page.waitForTimeout(200);
await page.click('[data-p="dash"]');
ok('Locked shot counts on dashboard', (await page.locator('#dShots').textContent()).trim() === '1');

// ---------- 8. wargame interactivity ----------
await page.click('[data-p="wargame"]');
await page.selectOption('#wgPick', { label: 'Second Language' });
await page.waitForTimeout(200);
const before = parseFloat(await page.locator('#wgForm .score').first().textContent());
ok('Second Language scores 72.9', Math.abs(before - 72.9) < 0.05, String(before));
const hint = await page.locator('#wgForm .hint').first().textContent();
ok('Anderson-ceiling warning fires', hint.includes('Anderson score is the ceiling'), hint.trim().slice(0,60));
// raise Anderson 2 -> 8
await page.locator('#wgForm input[data-k="and"]').fill('8');
await page.locator('#wgForm input[data-k="and"]').dispatchEvent('input');
await page.waitForTimeout(250);
const after = parseFloat(await page.locator('#wgForm .score').first().textContent());
ok('Slider changes final score', after > before, `${before} -> ${after}`);
// toggle a multiplier
await page.locator('#wgForm [data-x="crowd"]').check();
await page.waitForTimeout(250);
const withCrowd = parseFloat(await page.locator('#wgForm .score').first().textContent());
ok('Crowd multiplier reduces score', withCrowd < after, `${after} -> ${withCrowd}`);
ok('Crowd multiplier is x0.85', Math.abs(withCrowd - after * 0.85) < 0.06);
await page.screenshot({ path: `${SHOT}/05-wargame.png`, fullPage: true });

// ---------- 9. schedule ----------
await page.click('[data-p="schedule"]');
ok('6 phases render', (await page.locator('#schedule .phase').count()) === 6);
await page.check('#schedule input[data-sched="0-1"]');
await page.check('#schedule input[data-sched="0-2"]');
await page.waitForTimeout(200);
await page.click('[data-p="dash"]');
const bl2 = await page.locator('#blockers').textContent();
ok('Rules blocker clears when boxes ticked', !bl2.includes('Contest rules unverified'));
await page.click('[data-p="schedule"]');
await page.screenshot({ path: `${SHOT}/06-schedule.png`, fullPage: true });

// ---------- 10. daily log ----------
await page.click('[data-p="log"]');
await page.fill('#lgDate', '2026-08-13');
await page.fill('#lgGen', '400');
await page.fill('#lgKept', '6');
await page.fill('#lgNote', 'character sheet lock, three lighting stress test');
await page.click('#lgAdd');
await page.waitForTimeout(250);
ok('Day logged', (await page.locator('#logBody tr').count()) === 1);
const rate = await page.locator('#logBody tr td:nth-child(4)').textContent();
ok('Acceptance rate computed (6/400 = 1.5%)', rate.trim() === '1.5%', rate.trim());
await page.click('[data-p="dash"]');
ok('Dashboard acceptance updates', (await page.locator('#dAcc').textContent()).trim() === '1.5%');
ok('Projection computed', (await page.locator('#dProj').textContent()).trim() !== '—');
await page.screenshot({ path: `${SHOT}/07-dashboard-live.png`, fullPage: true });

// ---------- 11. ideas + promote ----------
await page.click('[data-p="ideas"]');
await page.fill('#ideaText', 'A night-shift lock keeper raises a boat she recognises.');
await page.click('#ideaAdd');
await page.waitForTimeout(200);
ok('Idea added', (await page.locator('#ideaList .card').count()) === 1);
ok('Spark prompts render', (await page.locator('#sparks .card').count()) === 8);
await page.click('[data-promote="0"]');
await page.waitForTimeout(300);
await page.click('[data-p="concepts"]');
ok('Promoted idea becomes a 7th concept', (await page.locator('#conceptList .ccard').count()) === 7);

// ---------- 12. prompt builder ----------
await page.click('[data-p="prompt"]');
await page.fill('#pbChars', 'KEEPER');
await page.fill('#pbId', '5a');
await page.fill('#pbDur', '28');
await page.fill('#pbGeo', '— LAMP = tungsten desk lamp, CENTER of the map table.\n— 180° AXIS: camera ALWAYS stays door-side.');
await page.fill('#pbCharDesc', 'KEEPER — weathered field jacket, sleeves to the elbow; burn scar on the left forearm.');
await page.fill('#pbVoice', 'dry worn alto; slow deliberate pacing; flat vowels');
await page.fill('#pbLine', "Ridge line's gone. Move them west.");
await page.fill('#pbAction', '0.0–4.0s — she holds the handset against her jaw, eyes down on the map.');
await page.click('#pbGen');
await page.waitForTimeout(200);
const out = await page.locator('#pbOut').textContent();
ok('Prompt contains character count header', out.includes('EXACT 1 CHARACTER — NO DUPLICATES: KEEPER'));
ok('Prompt contains GEO block', out.includes('GEO SPATIAL LAYOUT'));
ok('Prompt contains micro-life rule', out.includes('DOUBLE-BLINK'));
ok('Prompt contains silence lock', out.includes('stays completely silent'));
ok('Prompt embeds the quoted line', out.includes("Ridge line's gone. Move them west."));
ok('Prompt carries duration into tag tail', out.includes('28s. SFX only.'));
ok('Word counter present', (await page.locator('#pbCount').textContent()).includes('words'));
await page.screenshot({ path: `${SHOT}/08-prompt-builder.png`, fullPage: true });

// ---------- 13. reference pages ----------
await page.click('[data-p="judges"]');
ok('3 judge cards', (await page.locator('#judges .judgecard').count()) === 3);
await page.screenshot({ path: `${SHOT}/09-jury.png`, fullPage: true });
await page.click('[data-p="models"]');
ok('7 model rows', (await page.locator('#modelBody tr').count()) === 7);
ok('9 Papamichael-filter rows', (await page.locator('#filterBody tr').count()) === 9);
await page.screenshot({ path: `${SHOT}/10-models.png`, fullPage: true });

// ---------- 14. persistence ----------
await page.reload({ waitUntil: 'networkidle' });
await page.click('[data-p="ledger"]');
await page.waitForTimeout(250);
ok('Shots survive reload', (await page.locator('#shotBody tr').count()) === 26);
await page.click('[data-p="concepts"]');
ok('Concepts survive reload', (await page.locator('#conceptList .ccard').count()) === 7);
await page.click('[data-p="log"]');
ok('Log survives reload', (await page.locator('#logBody tr').count()) === 1);
await page.click('[data-p="schedule"]');
ok('Checkboxes survive reload', await page.locator('#schedule input[data-sched="0-1"]').isChecked());

// ---------- 15. export ----------
await page.click('[data-p="dash"]');
const dl = page.waitForEvent('download', { timeout: 5000 }).catch(() => null);
await page.click('#btnExport');
const d = await dl;
ok('Export produces a file', d !== null, d ? d.suggestedFilename() : 'no download event');

// ---------- 16. responsive ----------
await page.setViewportSize({ width: 700, height: 900 });
await page.waitForTimeout(300);
const bodyW = await page.evaluate(() => document.body.scrollWidth);
ok('No horizontal overflow at 700px', bodyW <= 710, `scrollWidth=${bodyW}`);
await page.screenshot({ path: `${SHOT}/11-narrow.png`, fullPage: false });
await page.setViewportSize({ width: 1440, height: 950 });

ok('No JS errors across the whole run', errors.length === 0, errors.slice(0, 3).join(' | '));

await browser.close();

console.log('\n\x1b[32mPASS (' + pass.length + ')\x1b[0m');
pass.forEach(p => console.log('  ✓ ' + p));
if (fail.length) {
  console.log('\n\x1b[31mFAIL (' + fail.length + ')\x1b[0m');
  fail.forEach(f => console.log('  ✗ ' + f));
}
console.log(`\n${pass.length}/${pass.length + fail.length} passed`);
process.exit(fail.length ? 1 : 0);
