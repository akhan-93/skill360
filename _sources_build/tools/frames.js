// usage: node frames.js <page.html> <outDir> <w> <h> <t1,t2,...> [clipSelector] [scale]
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const { pathToFileURL } = require('url');
(async () => {
  const [inp, outDir, w = 1440, h = 900, times = '0,1,2,3,4,5', clipSel = '', scale = 1] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true, args: ['--no-sandbox', '--allow-file-access-from-files', '--font-render-hinting=none']
  });
  const page = await browser.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errors.push(m.type() + ': ' + m.text()); });
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  await page.setViewport({ width: +w, height: +h, deviceScaleFactor: +scale });
  await page.goto(pathToFileURL(path.resolve(inp)).href, { waitUntil: 'networkidle0' });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => { if (window.__skill360Intro) window.__skill360Intro.pause(); });
  let clip;
  if (clipSel) {
    clip = await page.evaluate((s) => { const r = document.querySelector(s).getBoundingClientRect(); return { x: Math.max(0, r.x - 40), y: Math.max(0, r.y - 60), width: r.width + 80, height: r.height + 120 }; }, clipSel);
  }
  for (const t of times.split(',').map(Number)) {
    await page.evaluate((t) => { const tl = window.__skill360Intro; if (tl) { tl.pause(); tl.seek(t, false); } }, t);
    await new Promise(r => setTimeout(r, 120));
    const file = path.join(outDir, `f_${t.toFixed(2).padStart(5, '0')}.png`);
    await page.screenshot({ path: file, clip });
  }
  console.log('duration', await page.evaluate(() => window.__skill360Intro && window.__skill360Intro.duration()));
  console.log(errors.length ? errors.join('\n') : 'no console errors');
  await browser.close();
})();
