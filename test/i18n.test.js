const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const I18n = require('../i18n.js');
const { createServer, readLocaleCatalog, getStaticAsset } = require('../server.js');
const { buildReviewCsv, csvCell } = require('../scripts/export_locale_review.js');

const ROOT = path.join(__dirname, '..');
const LOCALES = path.join(ROOT, 'locales');
const catalog = readLocaleCatalog(LOCALES);
const english = catalog.en.strings;
const indexHtml = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const appJs = fs.readFileSync(path.join(ROOT, 'app.js'), 'utf8');
const unescape = text => text.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"');

// Words that would make a status label sound like approval. Every language must list its own,
// so adding a language forces someone to think about this.
const APPROVAL_WORDS = {
  en: ['safe', 'ok', 'okay', 'good', 'approved', 'fine'],
  hi: ['सुरक्षित', 'ठीक', 'सही', 'अच्छा', 'मंज़ूर', 'मंजूर'],
};
const STATUS_KEYS = ['statusReadable', 'statusCheck', 'statusNotVisible'];

test('every locale file is well formed and the English source is reviewed', () => {
  assert.ok(catalog.en && catalog.hi, 'en and hi locales present');
  assert.equal(catalog.en._meta.reviewed, true);
  for (const [code, data] of Object.entries(catalog)) {
    assert.equal(data._meta.code, code, `${code}: _meta.code must match the file name`);
    assert.ok(data._meta.nativeName && data._meta.englishName, `${code}: names`);
    assert.equal(typeof data._meta.reviewed, 'boolean', `${code}: reviewed flag`);
    if (data._meta.reviewed && code !== 'en') {
      assert.ok(data._meta.reviewedBy && data._meta.reviewedOn, `${code}: a reviewed language needs reviewedBy and reviewedOn`);
    }
  }
});

test('every locale has exactly the English keys, no empty strings, and the same placeholders', () => {
  for (const [code, data] of Object.entries(catalog)) {
    assert.deepEqual(Object.keys(data.strings).sort(), Object.keys(english).sort(), `${code}: key mismatch`);
    for (const [key, value] of Object.entries(data.strings)) {
      assert.equal(typeof value, 'string', `${code}.${key}`);
      assert.ok(value.trim().length > 0, `${code}.${key} is empty`);
      assert.deepEqual(I18n.placeholders(value), I18n.placeholders(english[key]), `${code}.${key}: placeholders differ from English`);
    }
  }
});

test('status labels never sound like approval, in any language', () => {
  for (const [code, data] of Object.entries(catalog)) {
    assert.ok(APPROVAL_WORDS[code], `add an APPROVAL_WORDS entry for "${code}" in this test`);
    for (const key of STATUS_KEYS) {
      const label = data.strings[key].toLowerCase();
      for (const word of APPROVAL_WORDS[code]) {
        const found = code === 'en' ? new RegExp(`\\b${word}\\b`).test(label) : label.includes(word);
        assert.equal(found, false, `${code}.${key} contains "${word}"`);
      }
    }
  }
});

test('consent, privacy and scope text keep their key facts in every language', () => {
  for (const [code, data] of Object.entries(catalog)) {
    const s = data.strings;
    assert.ok(s.consent.includes('Gemini'), `${code}.consent must say the photo goes to Gemini`);
    assert.ok(s.privacyCopy.includes('Gemini') && s.privacyCopy.includes('store:false'), `${code}.privacyCopy`);
    assert.ok(s.apiReady.includes('{model}'), `${code}.apiReady`);
    assert.ok(s.errServer.includes('{status}'), `${code}.errServer`);
    assert.ok(s.selectedPhotoAlt.includes('{name}'), `${code}.selectedPhotoAlt`);
    assert.ok(s.scopeText.length > 40, `${code}.scopeText`);
  }
});

test('index.html hooks all exist, and its built-in English text equals en.json', () => {
  const textHooks = [...indexHtml.matchAll(/<(\w+)([^>]*?)\sdata-i18n="(\w+)"([^>]*)>([^<]*)</g)];
  assert.ok(textHooks.length > 30);
  for (const [, , , key, , text] of textHooks) {
    assert.ok(key in english, `data-i18n="${key}" has no English string`);
    assert.equal(unescape(text), english[key], `index.html text for "${key}" differs from en.json`);
  }
  const attributeHooks = [...indexHtml.matchAll(/<[^>]*?data-i18n-(aria-label|alt|title)="(\w+)"[^>]*>/g)];
  assert.ok(attributeHooks.length >= 4);
  for (const [tag, attribute, key] of attributeHooks) {
    assert.ok(key in english, `data-i18n-${attribute}="${key}" has no English string`);
    const own = tag.match(new RegExp(`\\s${attribute}="([^"]*)"`));
    assert.ok(own, `${attribute} missing on tag with data-i18n-${attribute}`);
    assert.equal(unescape(own[1]), english[key], `${attribute} text for "${key}" differs from en.json`);
  }
});

test('every key the code uses exists, and no English key is unused', () => {
  // Keys the code asks for must exist in the English source.
  const asked = new Set();
  for (const m of appJs.matchAll(/\bt\('(\w+)'/g)) asked.add(m[1]);
  for (const m of appJs.matchAll(/\bkey: '(\w+)'/g)) asked.add(m[1]);
  for (const m of appJs.matchAll(/LocalizedError\('(\w+)'/g)) asked.add(m[1]);
  for (const m of indexHtml.matchAll(/data-i18n(?:-[a-z-]+)?="(\w+)"/g)) asked.add(m[1]);
  assert.ok(asked.size > 40);
  for (const key of asked) assert.ok(key in english, `code uses unknown string key "${key}"`);
  // Every English string must be referenced somewhere, so translators never translate dead text.
  const unused = Object.keys(english).filter(key => !appJs.includes(`'${key}'`) && !indexHtml.includes(`"${key}"`));
  assert.deepEqual(unused, [], `unused English strings: ${unused.join(', ')}`);
});

test('i18n helpers', () => {
  assert.equal(I18n.format('Gemini ready · {model}', { model: 'x' }), 'Gemini ready · x');
  assert.equal(I18n.format('{a} and {b}', { a: 1 }), '1 and {b}');
  assert.deepEqual(I18n.placeholders('{b} {a} {a}'), ['a', 'a', 'b']);
  assert.equal(I18n.isSelectable({ reviewed: true }), true);
  assert.equal(I18n.isSelectable({ reviewed: 'yes' }), false);
  assert.equal(I18n.isSelectable(undefined), false);
});

test('language choice: an unreviewed draft is only ever previewed on request', () => {
  const available = { en: { reviewed: true }, hi: { reviewed: false }, ta: { reviewed: true } };
  assert.deepEqual(I18n.pickLanguage({ requested: 'hi', available }), { language: 'hi', preview: true });
  assert.deepEqual(I18n.pickLanguage({ requested: 'ta', available }), { language: 'ta', preview: false });
  assert.deepEqual(I18n.pickLanguage({ requested: 'xx', available }), { language: 'en', preview: false });
  assert.deepEqual(I18n.pickLanguage({ stored: 'hi', available }), { language: 'en', preview: false }, 'a stored draft must not be applied');
  assert.deepEqual(I18n.pickLanguage({ stored: 'ta', available }), { language: 'ta', preview: false });
  assert.deepEqual(I18n.pickLanguage({ requested: 'ta', stored: 'hi', available }), { language: 'ta', preview: false });
  assert.deepEqual(I18n.pickLanguage({ available: {} }), { language: 'en', preview: false });
  assert.deepEqual(I18n.pickLanguage({ requested: '__proto__', available }), { language: 'en', preview: false });
});

test('the picker lists reviewed languages only, plus the draft being previewed', () => {
  const available = { en: { reviewed: true }, hi: { reviewed: false }, ta: { reviewed: true }, bn: { reviewed: false } };
  assert.deepEqual(I18n.pickerCodes({ available }), ['en', 'ta']);
  assert.deepEqual(I18n.pickerCodes({ available, previewCode: 'hi' }), ['en', 'hi', 'ta']);
  assert.deepEqual(I18n.pickerCodes({ available, previewCode: 'zz' }), ['en', 'ta']);
});

async function withServer(options, run) {
  const server = createServer({ apiKey: '', analysisEnabled: false, ...options });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  try { await run(`http://127.0.0.1:${server.address().port}`); } finally { server.close(); }
}

test('the server lists languages from the locale files and reports the reviewed flag as written', async () => {
  await withServer({}, async base => {
    const index = await (await fetch(`${base}/locales/index.json`)).json();
    assert.deepEqual(Object.keys(index).sort(), Object.keys(catalog).sort());
    for (const [code, data] of Object.entries(catalog)) assert.equal(index[code].reviewed, data._meta.reviewed === true);
    assert.equal(index.hi.nativeName, 'हिन्दी');
    const hi = await (await fetch(`${base}/locales/hi.json`)).json();
    assert.equal(hi.strings.statusCheck, catalog.hi.strings.statusCheck);
  });
});

test('/locales/ cannot be used to reach anything but locale files', async () => {
  await withServer({}, async base => {
    for (const bad of ['/locales/xx.json', '/locales/../server.js', '/locales/%2e%2e%2fserver.js', '/locales/hi.json/..', '/locales/__proto__.json', '/locales/constructor.json', '/locales/', '/locales/en.JSON']) {
      const res = await fetch(`${base}${bad}`);
      assert.equal(res.status, 404, bad);
    }
    assert.ok(getStaticAsset('/i18n.js').endsWith('i18n.js'));
    assert.equal(getStaticAsset('/locales/en.json'), null, 'locale files are served by code, not as static paths');
  });
});

test('a malformed or incomplete locale file is skipped instead of breaking the server', async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'labelfit-locales-'));
  fs.writeFileSync(path.join(dir, 'en.json'), JSON.stringify(catalog.en));
  fs.writeFileSync(path.join(dir, 'bn.json'), '{ not json');
  fs.writeFileSync(path.join(dir, 'ta.json'), JSON.stringify({ _meta: { code: 'ta' } }));
  fs.writeFileSync(path.join(dir, 'notes.txt'), 'ignored');
  assert.deepEqual(Object.keys(readLocaleCatalog(dir)), ['en']);
  await withServer({ localesDir: dir }, async base => {
    assert.deepEqual(Object.keys(await (await fetch(`${base}/locales/index.json`)).json()), ['en']);
    assert.equal((await fetch(`${base}/locales/bn.json`)).status, 404);
  });
  assert.deepEqual(readLocaleCatalog(path.join(dir, 'does-not-exist')), {});
});

test('the reviewer sheet lists every string with English beside the translation', () => {
  const csv = buildReviewCsv('hi', catalog);
  const lines = csv.trim().split('\r\n');
  assert.match(lines[0], /^key,english,translation,/);
  assert.ok(csv.includes('statusReadable,Readable,'));
  assert.ok(csv.includes('साफ़ पढ़ा गया'));
  assert.equal(csvCell('say "hi", ok'), '"say ""hi"", ok"');
  assert.equal(csvCell('plain'), 'plain');
  assert.throws(() => buildReviewCsv('zz', catalog), /No locale "zz"/);
});
