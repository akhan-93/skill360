// usage: node render_jobs.js <jobs.json>
// job: { html, out, w, h, transparent?, pdf? }
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const { pathToFileURL } = require('url');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true, args: ['--no-sandbox', '--allow-file-access-from-files', '--font-render-hinting=none']
  });
  const page = await browser.newPage();
  const errors = [];
  page.on('requestfailed', r => errors.push('requestfailed: ' + r.url()));
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  for (const j of jobs) {
    fs.mkdirSync(path.dirname(j.out), { recursive: true });
    if (!j.pdf) await page.setViewport({ width: j.w, height: j.h, deviceScaleFactor: 1 });
    await page.goto(pathToFileURL(path.resolve(j.html)).href, { waitUntil: 'networkidle0' });
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(async () => { await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))); });
    if (j.pdf) await page.pdf({ path: j.out, preferCSSPageSize: true, printBackground: true });
    else await page.screenshot({ path: j.out, omitBackground: !!j.transparent, clip: { x: 0, y: 0, width: j.w, height: j.h } });
  }
  console.log('rendered', jobs.length, 'jobs');
  console.log(errors.length ? errors.join('\n') : 'no errors');
  await browser.close();
})();
