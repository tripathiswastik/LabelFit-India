const test = require('node:test');
const assert = require('node:assert/strict');
const {
  createRateLimiter,
  extractOutputText,
  getStaticAsset,
  isAllowedOrigin,
  normalizeField,
  normalizeExtraction,
  parseImagePayload,
} = require('../server');

test('normalization downgrades a field without a source snippet', () => {
  assert.deepEqual(normalizeField({ value: 'Ingredients text', evidence: '', readStatus: 'clear' }), {
    value: 'Ingredients text', evidence: '', readStatus: 'uncertain',
  });
});

test('normalization does not turn an absent field into a confident result', () => {
  assert.deepEqual(normalizeField({ value: '', evidence: '', readStatus: 'clear' }), {
    value: '', evidence: '', readStatus: 'not_visible',
  });
});

test('normalization ignores extra model fields', () => {
  const result = normalizeExtraction({ notes: ['unexpected text'] });
  assert.equal(result.productName.readStatus, 'not_visible');
  assert.equal(Object.hasOwn(result, 'notes'), false);
});

test('image parser checks base64 and file signature against declared MIME type', () => {
  const png = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10, 1, 2, 3]);
  assert.deepEqual(parseImagePayload({ image: { data: png.toString('base64'), mimeType: 'image/png' } }).bytes, png);
  assert.throws(() => parseImagePayload({ image: { data: png.toString('base64'), mimeType: 'image/jpeg' } }), /file type/);
  assert.throws(() => parseImagePayload({ image: { data: 'not-base64', mimeType: 'image/png' } }), /base64/);
});

test('interaction output extractor returns only completed model text', () => {
  assert.equal(extractOutputText({ status: 'in_progress', steps: [{ type: 'model_output', content: [{ type: 'text', text: 'partial' }] }] }), '');
  assert.equal(extractOutputText({ status: 'completed', steps: [{ type: 'model_output', content: [{ type: 'text', text: '{"ok":true}' }] }] }), '{"ok":true}');
});

test('static file map does not expose arbitrary paths', () => {
  assert.ok(getStaticAsset('/app.js').endsWith('app.js'));
  assert.equal(getStaticAsset('/server.js'), null);
  assert.equal(getStaticAsset('/../README.md'), null);
});

test('origin check permits local same-origin requests and rejects foreign origins', () => {
  assert.equal(isAllowedOrigin({ headers: { origin: 'http://127.0.0.1:4173', host: '127.0.0.1:4173' } }), true);
  assert.equal(isAllowedOrigin({ headers: { origin: 'https://attacker.example', host: '127.0.0.1:4173' } }), false);
  assert.equal(isAllowedOrigin({ headers: { origin: 'https://127.0.0.1:4173', host: '127.0.0.1:4173' } }), false);
  assert.equal(isAllowedOrigin({ headers: { host: '127.0.0.1:4173' } }), true);
});

test('rate limiter allows a fixed burst and resets outside the window', () => {
  let now = 100;
  const allow = createRateLimiter({ limit: 2, intervalMs: 1000, now: () => now });
  assert.equal(allow('client'), true);
  assert.equal(allow('client'), true);
  assert.equal(allow('client'), false);
  now += 1001;
  assert.equal(allow('client'), true);
});

// Step 3: Transcription Error Defense Tests

test('Step 3: unsupported clear read with zero token overlap is downgraded to uncertain', () => {
  const result = normalizeField({
    value: 'Baby Fruit Puree with Mango',
    evidence: 'Manufactured by Organic Foods Ltd',
    readStatus: 'clear'
  }, 'productName');
  assert.equal(result.readStatus, 'uncertain');
});

test('Step 3: conflicting numerals in age marking are downgraded to uncertain', () => {
  const result = normalizeField({
    value: 'From 1 Month',
    evidence: 'Stage 1: From 6 to 24 Months',
    readStatus: 'clear'
  }, 'ageMarking');
  assert.equal(result.readStatus, 'uncertain');
});

test('Step 3: truncated ingredients list ending with comma or ellipsis is downgraded to uncertain', () => {
  const commaTruncated = normalizeField({
    value: 'Organic Rice Flour (55%), Sprouted Moong Dal Flour (25%),',
    evidence: 'Ingredients: Organic Rice Flour (55%), Sprouted Moong Dal Flour (25%),',
    readStatus: 'clear'
  }, 'ingredients');
  assert.equal(commaTruncated.readStatus, 'uncertain');

  const dotTruncated = normalizeField({
    value: 'Organic Rice Flour, Milk Solids...',
    evidence: 'Ingredients: Organic Rice Flour, Milk Solids...',
    readStatus: 'clear'
  }, 'ingredients');
  assert.equal(dotTruncated.readStatus, 'uncertain');
});

test('Step 3: allergen declaration inferred from ingredients without declaration marker is downgraded', () => {
  const inferred = normalizeField({
    value: 'Contains Milk',
    evidence: 'Ingredients: Skimmed milk solids (15%), Rice flour',
    readStatus: 'clear'
  }, 'allergenDeclaration');
  assert.equal(inferred.readStatus, 'uncertain');

  const explicit = normalizeField({
    value: 'Contains Milk',
    evidence: 'Allergen Declaration: Contains Milk.',
    readStatus: 'clear'
  }, 'allergenDeclaration');
  assert.equal(explicit.readStatus, 'clear');
});
