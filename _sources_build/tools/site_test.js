// usage: node site_test.js <index.html> <outDir>
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const { pathToFileURL } = require('url');
(async () => {
  const [inp, outDir] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const url = pathToFileURL(path.resolve(inp)).href;
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true, args: ['--no-sandbox', '--allow-file-access-from-files']
  });
  const log = [];
  const attach = (page, tag) => {
    page.on('console', m => { if (['error', 'warn', 'warning'].includes(m.type())) log.push(`${tag} ${m.type()}: ${m.text()}`); });
    page.on('pageerror', e => log.push(`${tag} pageerror: ${e.message}`));
    page.on('requestfailed', r => log.push(`${tag} requestfailed: ${r.url()}`));
    page.on('response', r => { if (r.status() >= 400) log.push(`${tag} http ${r.status()}: ${r.url()}`); });
  };

  // 1. normal load: skip button jumps to the final state and reveals the UI
  let page = await browser.newPage(); attach(page, '[normal]');
  await page.setViewport({ width: 1280, height: 800 });
  await page.goto(url, { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 1200));
  await page.click('.hero__skip');
  await new Promise(r => setTimeout(r, 1800));
  const afterSkip = await page.evaluate(() => ({
    progress: window.__skill360Intro.progress(),
    promiseOpacity: getComputedStyle(document.querySelector('.hero__promise')).opacity,
    navOpacity: getComputedStyle(document.querySelector('.nav')).opacity,
    heroDone: document.querySelector('.hero').classList.contains('is-done')
  }));
  console.log('after skip', JSON.stringify(afterSkip));
  await page.screenshot({ path: path.join(outDir, 'skip.png') });
  // replay restarts the timeline
  await page.click('.hero__replay');
  await new Promise(r => setTimeout(r, 700));
  console.log('after replay progress', (await page.evaluate(() => window.__skill360Intro.progress())).toFixed(2));
  // form validation + success message
  await page.evaluate(() => document.querySelector('#contact').scrollIntoView());
  await new Promise(r => setTimeout(r, 800));
  await page.evaluate(() => document.querySelector('#contact-form button[type=submit]').click());
  console.log('empty submit:', await page.$eval('.form__status', e => e.textContent));
  await page.type('input[name=nom]', 'Test Recette');
  await page.type('input[name=email]', 'test@example.com');
  await page.select('select[name=profil]', 'Entreprise');
  await page.click('input[name=rgpd]');
  await page.evaluate(() => document.querySelector('#contact-form button[type=submit]').click());
  console.log('valid submit:', await page.$eval('.form__status', e => e.textContent));
  await page.close();

  // 2. reduced motion: final state immediately, no intro
  page = await browser.newPage(); attach(page, '[reduced]');
  await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
  await page.setViewport({ width: 1280, height: 800 });
  await page.goto(url, { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 400));
  const reduced = await page.evaluate(() => ({
    progress: window.__skill360Intro.progress(),
    paused: window.__skill360Intro.paused(),
    promiseOpacity: getComputedStyle(document.querySelector('.hero__promise')).opacity,
    letterFill: getComputedStyle(document.querySelector('.lg-ltr')).fillOpacity
  }));
  console.log('reduced motion', JSON.stringify(reduced));
  await page.screenshot({ path: path.join(outDir, 'reduced.png') });
  await page.close();

  console.log(log.length ? 'LOG:\n' + log.join('\n') : 'no console errors/warnings, no failed requests');
  await browser.close();
})();
