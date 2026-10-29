// usage: node print_pdf.js <page.html> <out.pdf> [pngDir]
// Prints an HTML document whose pages use CSS @page size; optionally renders each .page to PNG for review.
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const { pathToFileURL } = require('url');
(async () => {
  const [inp, out, pngDir] = process.argv.slice(2);
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true, args: ['--no-sandbox', '--allow-file-access-from-files', '--font-render-hinting=none']
  });
  const page = await browser.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('requestfailed', r => errors.push('requestfailed: ' + r.url()));
  await page.goto(pathToFileURL(path.resolve(inp)).href, { waitUntil: 'networkidle0' });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(async () => { await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))); });
  // overflow check: content running into the footer
  const overflow = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p, i) => {
    const c = p.querySelector('.content'); const f = p.querySelector('.pf');
    if (!c || !f) return null;
    const cb = c.getBoundingClientRect().bottom, fb = f.getBoundingClientRect().top;
    return cb > fb - 2 ? `page ${i + 1}: content bottom ${Math.round(cb - fb)}px over footer` : null;
  }).filter(Boolean));
  if (out) {
    await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
    console.log('pdf', out, fs.statSync(out).size);
  }
  if (pngDir) {
    fs.mkdirSync(pngDir, { recursive: true });
    await page.setViewport({ width: 1123, height: 794, deviceScaleFactor: 1.4 });
    const n = await page.evaluate(() => document.querySelectorAll('.page').length);
    for (let i = 0; i < n; i++) {
      const el = (await page.$$('.page'))[i];
      await el.screenshot({ path: path.join(pngDir, `page_${String(i + 1).padStart(2, '0')}.png`) });
    }
    console.log('pngs', n);
  }
  console.log(overflow.length ? 'OVERFLOW:\n' + overflow.join('\n') : 'no overflow');
  console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no errors');
  await browser.close();
})();
