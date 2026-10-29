// usage: node shot.js <input.html|svg> <output.png> [width] [height] [scale] [waitMs] [transparent] [fullPage]
const puppeteer = require('puppeteer-core');
const path = require('path');
const { pathToFileURL } = require('url');
(async () => {
  const [inp, out, w = 1600, h = 900, s = 1, wait = 300, transparent = '0', full = '0'] = process.argv.slice(2);
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true,
    args: ['--no-sandbox', '--allow-file-access-from-files', '--font-render-hinting=none']
  });
  const page = await browser.newPage();
  page.on('console', m => console.log('[console]', m.type(), m.text()));
  page.on('pageerror', e => console.log('[pageerror]', e.message));
  await page.setViewport({ width: +w, height: +h, deviceScaleFactor: +s });
  await page.goto(pathToFileURL(path.resolve(inp)).href, { waitUntil: 'networkidle0' });
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await new Promise(r => setTimeout(r, +wait));
  await page.screenshot({ path: out, fullPage: full === '1', omitBackground: transparent === '1' });
  await browser.close();
})();
