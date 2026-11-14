const test = require('node:test');
const assert = require('node:assert/strict');
const {
  createRateLimiter,
  createServer,
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

test('Step 3: nutritionPanel with conflicting numbers is downgraded to uncertain', () => {
  const result = normalizeField({
    value: 'Per 100g: Energy 414 kcal, Iron 75 mg',
    evidence: 'Nutrition: Energy 414 kcal, Iron 7.5 mg',
    readStatus: 'clear'
  }, 'nutritionPanel');
  assert.equal(result.readStatus, 'uncertain');
});

test('Step 3: nutritionPanel with physically impossible macronutrient is downgraded', () => {
  const result = normalizeField({
    value: 'Per 100g: Energy 418 kcal, Protein 152 g, Fat 9.5 g',
    evidence: 'Per 100g: Energy 418 kcal, Protein 15.2 g, Fat 9.5 g',
    readStatus: 'clear'
  }, 'nutritionPanel');
  assert.equal(result.readStatus, 'uncertain');
});

test('Step 3: nutritionPanel with decimal-dropped excessive iron is downgraded', () => {
  const result = normalizeField({
    value: 'Per 100g: Iron 75 mg, Calcium 500 mg',
    evidence: 'Per 100g: Iron 75 mg, Calcium 500 mg',
    readStatus: 'clear'
  }, 'nutritionPanel');
  assert.equal(result.readStatus, 'uncertain');
});

test('Step 3: allergen declaration containing unprinted hallucinated allergen is downgraded', () => {
  const result = normalizeField({
    value: 'Contains Wheat and Milk. May contain gluten, soy, and peanuts.',
    evidence: 'Contains Wheat and Milk.',
    readStatus: 'clear'
  }, 'allergenDeclaration');
  assert.equal(result.readStatus, 'uncertain');
});

test('Step 3: ingredients with unclosed delimiter is downgraded to uncertain', () => {
  const result = normalizeField({
    value: 'Wheat flour (Atta) (51.6%), Milk solids (35.2%',
    evidence: 'Wheat flour (Atta) (51.6%), Milk solids (35.2%',
    readStatus: 'clear'
  }, 'ingredients');
  assert.equal(result.readStatus, 'uncertain');
});

test('Step 3: Devanagari numerals are normalized and evaluated in nutrition check', () => {
  const result = normalizeField({
    value: 'प्रति १०० ग्रॅम: लोह ५० मि.ग्रॅ',
    evidence: 'प्रति १०० ग्रॅम: लोह ५.० मि.ग्रॅ',
    readStatus: 'clear'
  }, 'nutritionPanel');
  assert.equal(result.readStatus, 'uncertain');
});

test('Step 4: ageMarking derived from RDA or caloric guideline footnote is downgraded to uncertain', () => {
  const result = normalizeField({
    value: '8 year old child',
    evidence: '8 year old child',
    readStatus: 'clear'
  }, 'ageMarking');
  assert.equal(result.readStatus, 'uncertain');

  const footnote = normalizeField({
    value: '8 year old child',
    evidence: '*Guideline Daily Amounts of an average 8 year old child (1700 kcal)',
    readStatus: 'clear'
  }, 'ageMarking');
  assert.equal(footnote.readStatus, 'uncertain');

  const validInfantAge = normalizeField({
    value: 'Stage 1: From 6 to 24 Months',
    evidence: 'Stage 1: From 6 to 24 Months',
    readStatus: 'clear'
  }, 'ageMarking');
  assert.equal(validInfantAge.readStatus, 'clear');
});

test('Step 4: ageMarking derived from medicine or supplement dosage instruction is downgraded to uncertain', () => {
  const result = normalizeField({
    value: 'Children: 1 tablet',
    evidence: 'Children: 1 tablet',
    readStatus: 'clear'
  }, 'ageMarking');
  assert.equal(result.readStatus, 'uncertain');

  const drops = normalizeField({
    value: 'Give 5 drops daily',
    evidence: 'Give 5 drops daily',
    readStatus: 'clear'
  }, 'ageMarking');
  assert.equal(drops.readStatus, 'uncertain');
});

// Step 5: Production Security & Cloud Run Spend Locks Tests

test('Step 5: Cloud Run status endpoint reports unconfigured when analysis is disabled', async () => {
  const server = createServer({ apiKey: 'mock-key', analysisEnabled: false });
  await new Promise(resolve => server.listen(0, resolve));
  const port = server.address().port;

  try {
    const res = await fetch(`http://127.0.0.1:${port}/api/status`);
    assert.equal(res.status, 200);
    const data = await res.json();
    assert.equal(data.configured, false);
    assert.equal(data.model, null);
  } finally {
    server.close();
  }
});

test('Step 5: Cloud Run analysis guard hard-disables analysis and returns 503', async () => {
  const server = createServer({ apiKey: 'mock-key', analysisEnabled: false });
  await new Promise(resolve => server.listen(0, resolve));
  const port = server.address().port;

  try {
    const res = await fetch(`http://127.0.0.1:${port}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ image: { data: 'dummy', mimeType: 'image/png' } })
    });
    assert.equal(res.status, 503);
    const data = await res.json();
    assert.match(data.error, /disabled on this Cloud Run/i);
  } finally {
    server.close();
  }
});

test('Step 5: Strict security headers are attached on all responses', async () => {
  const server = createServer({ apiKey: '', analysisEnabled: false });
  await new Promise(resolve => server.listen(0, resolve));
  const port = server.address().port;

  try {
    const res = await fetch(`http://127.0.0.1:${port}/api/status`);
    assert.equal(res.headers.get('x-content-type-options'), 'nosniff');
    assert.equal(res.headers.get('x-frame-options'), 'DENY');
    assert.equal(res.headers.get('referrer-policy'), 'no-referrer');
    assert.equal(res.headers.get('cache-control'), 'no-store');
    assert.ok(res.headers.get('content-security-policy').includes("default-src 'self'"));
    assert.ok(res.headers.get('permissions-policy').includes('camera=()'));
  } finally {
    server.close();
  }
});
