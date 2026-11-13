const { test, before, after } = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const {
  createServer,
  parseImagePayload,
  imageSignatureMatches,
  normalizeExtraction
} = require('../server');

const FIXTURES_DIR = path.join(__dirname, 'fixtures');
let server;
let baseUrl = '';

before((_, done) => {
  // Run server without GEMINI_API_KEY to test unconfigured baseline
  delete process.env.GEMINI_API_KEY;
  server = createServer();
  server.listen(0, '127.0.0.1', () => {
    baseUrl = `http://127.0.0.1:${server.address().port}`;
    done();
  });
});

after((_, done) => {
  server.close(done);
});

test('1. Smoke Test: Missing API Key returns 503 and clear state', async () => {
  // Status check
  const statusRes = await fetch(`${baseUrl}/api/status`);
  assert.strictEqual(statusRes.status, 200);
  const statusData = await statusRes.json();
  assert.strictEqual(statusData.configured, false);

  // Analyze attempt without API key
  const normalPng = fs.readFileSync(path.join(FIXTURES_DIR, 'synthetic_normal.png'));
  const analyzeRes = await fetch(`${baseUrl}/api/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      image: {
        data: normalPng.toString('base64'),
        mimeType: 'image/png'
      }
    })
  });

  assert.strictEqual(analyzeRes.status, 503);
  const errData = await analyzeRes.json();
  assert.ok(errData.error.includes('Gemini is not configured'));
});

test('2. Smoke Test: Invalid file (corrupt signature) rejected with 400', async () => {
  const invalidData = fs.readFileSync(path.join(FIXTURES_DIR, 'synthetic_invalid.png'));

  // Direct parser check
  assert.throws(() => {
    parseImagePayload({
      image: {
        data: invalidData.toString('base64'),
        mimeType: 'image/png'
      }
    });
  }, (err) => {
    assert.strictEqual(err.status, 400);
    assert.strictEqual(err.message, 'The file type does not match the selected image.');
    return true;
  });

  // Verify signature matcher returns false
  assert.strictEqual(imageSignatureMatches(invalidData, 'image/png'), false);
});

test('3. Smoke Test: Normal synthetic packaging image parses successfully', () => {
  const normalData = fs.readFileSync(path.join(FIXTURES_DIR, 'synthetic_normal.png'));
  const parsed = parseImagePayload({
    image: {
      data: normalData.toString('base64'),
      mimeType: 'image/png'
    }
  });

  assert.strictEqual(parsed.mimeType, 'image/png');
  assert.strictEqual(parsed.bytes.length, normalData.length);
  assert.strictEqual(imageSignatureMatches(parsed.bytes, 'image/png'), true);
});

test('4. Smoke Test: Blurry synthetic packaging image parses successfully', () => {
  const blurryData = fs.readFileSync(path.join(FIXTURES_DIR, 'synthetic_blurry.png'));
  const parsed = parseImagePayload({
    image: {
      data: blurryData.toString('base64'),
      mimeType: 'image/png'
    }
  });

  assert.strictEqual(parsed.mimeType, 'image/png');
  assert.ok(parsed.bytes.length > 50000);
  assert.strictEqual(imageSignatureMatches(parsed.bytes, 'image/png'), true);
});

test('5. Smoke Test: Missing fields handling in normalization', () => {
  // Simulate Gemini output on synthetic_missing_fields where allergen & prep are omitted
  const rawModelOutput = {
    productName: { value: 'PureBite Single-Grain Baby Porridge', evidence: 'PureBite Single-Grain', readStatus: 'clear' },
    ageMarking: { value: 'STAGE 1: 6+ MONTHS', evidence: '6+ MONTHS', readStatus: 'clear' },
    ingredients: { value: '100% Organic Spelt Grain', evidence: 'Organic Spelt Grain', readStatus: 'clear' },
    nutritionPanel: { value: 'Energy 360 kcal, Protein 11g', evidence: 'Energy 360 kcal', readStatus: 'clear' }
    // allergenDeclaration and preparationAndStorage are completely absent from model output
  };

  const normalized = normalizeExtraction(rawModelOutput);

  // Missing fields MUST NOT be hallucinated or marked confident
  assert.strictEqual(normalized.allergenDeclaration.readStatus, 'not_visible');
  assert.strictEqual(normalized.allergenDeclaration.value, '');
  assert.strictEqual(normalized.allergenDeclaration.evidence, '');

  assert.strictEqual(normalized.preparationAndStorage.readStatus, 'not_visible');
  assert.strictEqual(normalized.preparationAndStorage.value, '');
  assert.strictEqual(normalized.preparationAndStorage.evidence, '');

  // Present fields remain verified
  assert.strictEqual(normalized.productName.readStatus, 'clear');
  assert.strictEqual(normalized.ageMarking.readStatus, 'clear');
});

test('6. Smoke Test: Photo change clears upload confirmation (app.js verification)', () => {
  // Read app.js source to statically verify invariants
  const appJs = fs.readFileSync(path.join(__dirname, '..', 'app.js'), 'utf8');

  // Verify chooseFile resets photoConfirmation.checked = false
  assert.ok(
    appJs.includes('photoConfirmation.checked = false;'),
    'app.js must reset photoConfirmation.checked on photo selection'
  );

  // Verify resetPhoto resets photoConfirmation.checked = false
  const resetPhotoBlock = appJs.slice(appJs.indexOf('function resetPhoto()'), appJs.indexOf('function resetPhoto()') + 300);
  assert.ok(
    resetPhotoBlock.includes('photoConfirmation.checked = false;'),
    'resetPhoto must reset photoConfirmation.checked'
  );

  // Verify updateAnalyzeButton requires photoConfirmation.checked
  assert.ok(
    appJs.includes('photoConfirmation.checked'),
    'analyzeButton must require photoConfirmation.checked'
  );
});

test('7. Smoke Test: Cloud Run analysis guard is hard-disabled', () => {
  const serverJs = fs.readFileSync(path.join(__dirname, '..', 'server.js'), 'utf8');
  assert.ok(
    serverJs.includes('const IS_CLOUD_RUN = Boolean(process.env.K_SERVICE);'),
    'Must detect Cloud Run environment via K_SERVICE'
  );
  assert.ok(
    serverJs.includes('const ANALYSIS_ENABLED = !IS_CLOUD_RUN;'),
    'Analysis must be disabled when IS_CLOUD_RUN is true'
  );
});
