// Capture des états de la carte de décision (v2/prototype-carte) pour la vidéo.
// Prérequis : `uv run python v2/prototype-carte/server.py 8767` lancé.
// Sorties : public/textures/*.png (2x) + src/layout.json (bbox en px CSS 1920x1080).
import puppeteer from 'puppeteer';
import fs from 'fs';
const BASE = process.env.BASE || 'http://localhost:8767';
const OUT = 'public/textures';
fs.mkdirSync(OUT, {recursive: true});
const layout = {};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const b = await puppeteer.launch({executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--use-angle=d3d11', '--hide-scrollbars']});
const p = await b.newPage();
await p.setViewport({width: 1920, height: 1080, deviceScaleFactor: 2});
await p.goto(BASE, {waitUntil: 'networkidle0'});
await p.evaluate(() => document.fonts.ready);
await sleep(3000);

async function box(name, sel) {
  const r = await p.evaluate((s) => {const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return {x: b.x, y: b.y, w: b.width, h: b.height};}, sel);
  return r;
}
async function shot(name, boxes = {}, cut = []) {
  await p.mouse.move(1919, 1079);
  await sleep(400);
  await p.screenshot({path: `${OUT}/${name}.png`});
  layout[name] = {};
  for (const [k, s] of Object.entries(boxes)) layout[name][k] = await box(k, s);
  for (const [k, s] of cut) {const el = await p.$(s); if (el) await el.screenshot({path: `${OUT}/${name}-${k}.png`, omitBackground: true});}
  console.log('ok', name);
}
async function search(txt) {
  await p.evaluate(() => {const q = document.querySelector('#q'); q.value = ''; q.focus();}); await p.keyboard.type(txt, {delay: 40}); await sleep(500);
  await p.keyboard.press('Enter'); await sleep(2600);
}

// A1 France, kinés (vue évolution)
await shot('a1-france', {levers: '#levers', legend: '#legend', search: '#q', profs: '#profs'});
// Vue "Écart au tendanciel" en France, sans politique (tout neutre) : avant
await p.evaluate(() => [...document.querySelectorAll('button')].find((b) => b.textContent.includes('Écart au'))?.click());
await sleep(1200);
await shot('b1-ecart-avant', {scen: '#scen', levers: '#levers'});
// Preset Former 20 % de plus : après
await p.evaluate(() => [...document.querySelectorAll('.preset')].find((b) => b.dataset.p === 'former')?.click());
await sleep(2500);
await shot('b2-ecart-apres', {scen: '#scen', levers: '#levers', slider: '#levers input[type=range]'}, [['scen', '#scen']]);
// Retour tendance + vue évolution
await p.evaluate(() => document.querySelector('#reset')?.click());
await sleep(800);
await p.evaluate(() => [...document.querySelectorAll('button')].find((b) => b.textContent.includes('Évolution 2026'))?.click());
await sleep(1500);
// A2 région
await search('Auvergne-Rh');
await shot('a2-region');
// A3 département + fiche
await search('Puy-de-D');
// laisse la fiche se poser
await sleep(800);
await shot('a3-dep', {card: '#card'}, [['card', '#card']]);
// C : phrase
await p.goto(BASE, {waitUntil: 'networkidle0'}); await sleep(3000);
await shot('c0-vide', {nlq: '#nlq', nlbtn: '#nlf button', levers: '#levers'});
await p.click('#nlq'); await p.keyboard.type('former 20 % de kinés en plus en Auvergne', {delay: 30});
await shot('c1-tape', {nlq: '#nlq'});
await p.evaluate(() => document.querySelector('#nlf button')?.click());
await sleep(2500);
await shot('c2-compris', {nl: '#nl', ok: '#nlok'}, [['nl', '#nl']]);
await p.evaluate(() => document.querySelector('#nlok')?.click());
await sleep(3000);
await shot('c3-applique', {scen: '#scen', card: '#card'});
fs.writeFileSync('src/layout.json', JSON.stringify(layout, null, 1));
await b.close();
