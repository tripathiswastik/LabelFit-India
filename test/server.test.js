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
