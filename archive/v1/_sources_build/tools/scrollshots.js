// usage: node scrollshots.js <page.html> <outDir> <w> <h> [stepFactor] [scale]
// Skips the intro, then scrolls through the page and captures the viewport at each step.
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const { pathToFileURL } = require('url');
(async () => {
  const [inp, outDir, w = 1440, h = 900, stepFactor = 0.85, scale = 1] = process.argv.slice(2);
  fs.rmSync(outDir, { recursive: true, force: true });
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
  await new Promise(r => setTimeout(r, 6500)); // let the intro play
  await page.screenshot({ path: path.join(outDir, 's_000.png') });
  const total = await page.evaluate(() => document.documentElement.scrollHeight);
  const step = Math.round(+h * +stepFactor);
  let i = 1;
  for (let y = step; y < total; y += step, i++) {
    await page.evaluate((y) => window.scrollTo({ top: y, behavior: 'instant' }), y);
    await new Promise(r => setTimeout(r, 1400));
    await page.screenshot({ path: path.join(outDir, `s_${String(i).padStart(3, '0')}.png`) });
  }
  console.log('scrollHeight', total, 'shots', i);
  console.log(errors.length ? errors.join('\n') : 'no console errors');
  await browser.close();
})();
