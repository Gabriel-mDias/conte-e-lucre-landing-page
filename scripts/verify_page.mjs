import { chromium } from 'playwright-core';
import { mkdir } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const url = process.argv[2] || 'http://127.0.0.1:4173/';
const chrome = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const output = join(tmpdir(), 'conte-lucre-v2');
await mkdir(output, { recursive: true });

const browser = await chromium.launch({ executablePath: chrome, headless: true });
const results = [];

for (const width of [360, 390, 768, 1024, 1280, 1440]) {
  const context = await browser.newContext({ viewport: { width, height: width === 360 ? 800 : 900 } });
  const page = await context.newPage();
  const errors = [];
  const networkErrors = [];
  page.on('console', (message) => { if (message.type() === 'error') errors.push(message.text()); });
  page.on('pageerror', (error) => errors.push(error.message));
  page.on('requestfailed', (request) => networkErrors.push(`${request.method()} ${request.url()}: ${request.failure()?.errorText}`));
  page.on('response', (response) => { if (response.status() >= 400) networkErrors.push(`${response.status()} ${response.url()}`); });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.locator('#sobre').scrollIntoViewIfNeeded();
  await page.locator('.duo-frame img').evaluate((image) => image.decode());
  await page.locator('#insights').scrollIntoViewIfNeeded();
  await page.locator('.content-open img').evaluateAll((images) => Promise.all(images.map((image) => { image.loading = 'eager'; return image.decode(); })));
  await page.locator('#hero').scrollIntoViewIfNeeded();
  const audit = await page.evaluate(() => ({
    heroHeight: Math.round(document.querySelector('#hero').getBoundingClientRect().height),
    viewportHeight: innerHeight,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    overflowing: [...document.querySelectorAll('body *')].filter((node) => {
      const rect = node.getBoundingClientRect();
      return rect.right > document.documentElement.clientWidth + 1 || rect.left < -1;
    }).slice(0, 12).map((node) => `${node.tagName.toLowerCase()}.${node.className}`),
    missingImages: [...document.images].filter((image) => image.complete && image.naturalWidth === 0).map((image) => image.src),
    ids: ['sobre','solucoes','metodo','lideranca','insights','depoimentos','diagnostico'].every((id) => Boolean(document.getElementById(id))),
    brand: (() => {
      const nav = document.querySelector('.navbar').getBoundingClientRect();
      const image = document.querySelector('.brand-logo img');
      const rect = image.getBoundingClientRect();
      return { natural: [image.naturalWidth, image.naturalHeight], rendered: [Math.round(rect.width), Math.round(rect.height)], contained: rect.top >= nav.top && rect.bottom <= nav.bottom };
    })(),
    heroVideo: (() => {
      const video = document.querySelector('.hero video');
      const style = getComputedStyle(video);
      return { currentSrc: video.currentSrc, poster: video.poster, natural: [video.videoWidth, video.videoHeight], fit: style.objectFit, position: style.objectPosition, sourceCount: video.querySelectorAll('source').length };
    })(),
    duo: (() => {
      const image = document.querySelector('.duo-frame img');
      const rect = image.getBoundingClientRect();
      return { natural: [image.naturalWidth, image.naturalHeight], rendered: [Math.round(rect.width), Math.round(rect.height)], fit: getComputedStyle(image).objectFit };
    })(),
    covers: [...document.querySelectorAll('.content-open img')].map((image) => {
      const rect = image.getBoundingClientRect();
      return { natural: [image.naturalWidth, image.naturalHeight], rendered: [Math.round(rect.width), Math.round(rect.height)], fit: getComputedStyle(image).objectFit };
    }),
    testimonials: (() => {
      const cards = [...document.querySelectorAll('#depoimentos .quote-card')];
      return { images: document.querySelectorAll('#depoimentos img, #depoimentos picture, #depoimentos video').length, cards: cards.length, columns: new Set(cards.map((card) => Math.round(card.getBoundingClientRect().left))).size };
    })(),
    post3Referenced: [...document.querySelectorAll('img, source')].some((node) => (node.src || node.srcset || '').includes('post_3')),
  }));
  await page.screenshot({ path: join(output, `home-${width}.png`), fullPage: true });
  if (width === 360 || width === 1440) {
    for (const id of ['hero', 'sobre', 'lideranca', 'insights', 'depoimentos']) {
      const section = page.locator(`#${id}`);
      await section.scrollIntoViewIfNeeded();
      await page.waitForTimeout(250);
      await section.screenshot({ path: join(output, `${id}-${width}.png`) });
    }
  }
  results.push({ width, ...audit, errors, networkErrors });
  await context.close();
}

const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
const page = await context.newPage();
await page.goto(url, { waitUntil: 'networkidle' });
const galleryResults = {};
for (const [id, count] of [['post-1', 4], ['post-2', 1], ['post-4', 5]]) {
  const trigger = page.locator(`[data-post="${id}"]`);
  await trigger.click();
  galleryResults[id] = {
    slides: await page.locator('#contentGallery .swiper-slide').count(),
    expected: count,
    open: await page.locator('#contentGallery').evaluate((node) => node.open),
    single: await page.locator('[data-gallery-swiper]').evaluate((node) => node.classList.contains('is-single')),
  };
  if (count > 1) {
    await page.locator('.gallery-next').click();
    galleryResults[id].counterAfterNext = await page.locator('.gallery-counter').textContent();
    await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(100);
    galleryResults[id].counterAfterKeyboard = await page.locator('.gallery-counter').textContent();
    await page.locator('.gallery-pagination .swiper-pagination-bullet').first().click();
    await page.waitForTimeout(100);
    galleryResults[id].counterAfterIndicator = await page.locator('.gallery-counter').textContent();
  }
  if (id === 'post-1') await dialogScreenshot(page, join(output, 'gallery-1280.png'));
  await page.keyboard.press('Escape');
  await page.waitForTimeout(50);
  galleryResults[id].focusRestored = await trigger.evaluate((node) => node === document.activeElement);
}

await page.locator('.faq-question').first().click();
const faqOpen = await page.locator('.faq-question').first().getAttribute('aria-expanded');
await page.evaluate(() => { window.__whatsappUrl = ''; window.open = (value) => { window.__whatsappUrl = value; return {}; }; });
await page.locator('#diagNome').fill('Teste');
await page.locator('#diagEmpresa').fill('Empresa teste');
await page.locator('#diagFaturamento').selectOption({ label: 'Até R$ 30 mil' });
await page.locator('#diagDesafio').selectOption({ label: 'Pouca clareza sobre caixa e resultado' });
await page.locator('#formDiagnostico').evaluate((form) => form.requestSubmit());
const whatsappUrl = await page.evaluate(() => window.__whatsappUrl);
await context.close();

const mobileContext = await browser.newContext({ viewport: { width: 360, height: 800 }, hasTouch: true });
const mobilePage = await mobileContext.newPage();
await mobilePage.goto(url, { waitUntil: 'networkidle' });
await mobilePage.locator('#menuToggle').click();
const mobileMenuOpened = await mobilePage.locator('#menuToggle').getAttribute('aria-expanded');
await mobilePage.locator('#navLinks a[href="#sobre"]').click();
const mobileMenuClosed = await mobilePage.locator('#menuToggle').getAttribute('aria-expanded');
const mobileAnchor = await mobilePage.evaluate(() => location.hash);
await mobilePage.locator('[data-post="post-1"]').click();
await mobilePage.locator('#contentGallery').screenshot({ path: join(output, 'gallery-360.png') });
const mobileGallerySlides = await mobilePage.locator('#contentGallery .swiper-slide').count();
const galleryBox = await mobilePage.locator('[data-gallery-swiper]').boundingBox();
const touchClient = await mobileContext.newCDPSession(mobilePage);
const touchY = galleryBox.y + galleryBox.height * .5;
const touchStart = galleryBox.x + galleryBox.width * .8;
const touchEnd = galleryBox.x + galleryBox.width * .2;
await touchClient.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: touchStart, y: touchY }] });
await touchClient.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: (touchStart + touchEnd) / 2, y: touchY }] });
await touchClient.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: touchEnd, y: touchY }] });
await touchClient.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
await mobilePage.waitForTimeout(650);
const mobileTouchCounter = await mobilePage.locator('.gallery-counter').textContent();
await mobilePage.keyboard.press('Escape');
await mobileContext.close();

const reduced = await browser.newContext({ viewport: { width: 768, height: 900 }, reducedMotion: 'reduce' });
const reducedPage = await reduced.newPage();
await reducedPage.goto(url, { waitUntil: 'networkidle' });
const reducedVideoPaused = await reducedPage.locator('.hero video').evaluate((video) => video.paused);
await reduced.close();
await browser.close();

const report = { output, results, galleryResults, faqOpen, whatsappUrl, mobileMenuOpened, mobileMenuClosed, mobileAnchor, mobileGallerySlides, mobileTouchCounter, reducedVideoPaused };
const failures = [];
for (const result of results) {
  const mobile = result.width < 768;
  if (result.heroHeight !== result.viewportHeight) failures.push(`${result.width}: hero nao preenche a viewport`);
  if (result.overflow !== 0) failures.push(`${result.width}: overflow horizontal de ${result.overflow}px`);
  if (result.errors.length || result.networkErrors.length || result.missingImages.length) failures.push(`${result.width}: erros de console, rede ou imagem`);
  if (!result.brand.contained || result.brand.natural.join('x') !== '1246x188') failures.push(`${result.width}: assinatura fora da navegacao ou ativo incorreto`);
  if (!result.heroVideo.currentSrc.endsWith(mobile ? 'hero-mobile.mp4' : 'hero-desktop.mp4')) failures.push(`${result.width}: fonte de video incorreta`);
  if (!result.heroVideo.poster.endsWith(mobile ? 'hero-mobile-poster.webp' : 'hero-desktop-poster.webp')) failures.push(`${result.width}: poster incorreto`);
  if (result.heroVideo.natural.join('x') !== (mobile ? '720x1280' : '1280x720') || result.heroVideo.fit !== 'cover' || result.heroVideo.position !== '50% 50%' || result.heroVideo.sourceCount !== 2) failures.push(`${result.width}: proporcao ou CSS do video incorreto`);
  if (Math.abs(result.duo.natural[0] / result.duo.natural[1] - .8) > .005 || Math.abs(result.duo.rendered[0] / result.duo.rendered[1] - .8) > .005 || result.duo.fit !== 'cover') failures.push(`${result.width}: composicao dos socios incorreta`);
  if (result.covers.some((cover) => !cover.natural[0] || Math.abs(cover.natural[0] / cover.natural[1] - .8) > .005 || Math.abs(cover.rendered[0] / cover.rendered[1] - .8) > .005 || cover.fit !== 'contain')) failures.push(`${result.width}: capa fora do quadro 4:5`);
  if (result.testimonials.images !== 0 || result.testimonials.cards !== 2 || result.testimonials.columns !== (result.width > 820 ? 2 : 1)) failures.push(`${result.width}: estrutura dos depoimentos incorreta`);
  if (result.post3Referenced) failures.push(`${result.width}: post 3 ainda possui referencia visual`);
}
for (const [id, expected] of [['post-1', 4], ['post-2', 1], ['post-4', 5]]) {
  if (galleryResults[id].slides !== expected || !galleryResults[id].focusRestored) failures.push(`${id}: galeria ou retorno de foco incorreto`);
}
if (faqOpen !== 'true' || mobileMenuOpened !== 'true' || mobileMenuClosed !== 'false' || mobileAnchor !== '#sobre' || mobileGallerySlides !== 4 || mobileTouchCounter !== '2 / 4' || !reducedVideoPaused || !whatsappUrl.startsWith('https://wa.me/')) failures.push('interacoes principais ou movimento reduzido falharam');
report.failures = failures;
console.log(JSON.stringify(report, null, 2));
if (failures.length) process.exitCode = 1;

async function dialogScreenshot(page, path) {
  await page.locator('#contentGallery').screenshot({ path });
}
