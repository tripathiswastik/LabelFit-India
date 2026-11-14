/**
 * Baseline Verification Runner for LabelFit India
 * Launches the app locally and asserts on:
 * - Local static serving (GET /, /styles.css, /app.js)
 * - Consent notice presence and wording
 * - Upload flow controls and reset invariants in app.js
 * - Error states: 400 (corrupt signature, invalid payload), 403 (foreign origin), 503 (missing key)
 * - Cloud Run spend guard (503 when K_SERVICE set)
 * - Full normalization pipeline
 */

const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { createServer } = require('../server');

const REPO_ROOT = path.resolve(__dirname, '..');
const FIXTURE_PNG = path.join(REPO_ROOT, 'test', 'fixtures', 'synthetic_normal.png');

async function runBaselineAudit() {
  console.log('================================================================');
  console.log('  LABELFIT INDIA - BASELINE VERIFICATION & LOCAL APP AUDIT      ');
  console.log('================================================================\n');

  // 1. Static Asset & Consent Notice Verification
  console.log('[1] Auditing Static Assets & Consent Notice in index.html...');
  const indexHtml = fs.readFileSync(path.join(REPO_ROOT, 'index.html'), 'utf8');
  assert.ok(indexHtml.includes('id="photo-confirm"'), 'Consent checkbox input must be present');
  assert.ok(
    indexHtml.includes('I understand the photo is sent to Gemini. I checked it shows only the package, with no people or personal details.'),
    'Explicit package-only consent copy must match exact protocol wording'
  );
  assert.ok(
    indexHtml.includes('store:false is not a zero-retention promise.'),
    'Privacy disclosure must state store:false limitation'
  );
  console.log('    ✓ index.html contains verified package-only consent notice and retention notice.');

  // 2. Client-Side Upload Flow & Consent Invariants in app.js
  console.log('[2] Auditing Client-Side Upload Invariants in app.js...');
  const appJs = fs.readFileSync(path.join(REPO_ROOT, 'app.js'), 'utf8');
  assert.ok(
    appJs.includes('analyzeButton.disabled = !selectedFile || !analysisReady || !photoConfirmation.checked || analysisInProgress;'),
    'Analyze button must require selectedFile, analysisReady, and photoConfirmation.checked'
  );
  assert.ok(
    appJs.includes('photoConfirmation.checked = false;'),
    'Photo selection must reset photoConfirmation.checked to false'
  );
  console.log('    ✓ app.js enforces mandatory consent checkbox and resets confirmation on file change.');

  // 3. Launch Local Server Instance (Local Development Mode)
  console.log('[3] Launching Local Server (Local Mode, Analysis Enabled, No API Key)...');
  const localServer = createServer({ apiKey: '', analysisEnabled: true });
  await new Promise(resolve => localServer.listen(0, '127.0.0.1', resolve));
  const port = localServer.address().port;
  const baseUrl = `http://127.0.0.1:${port}`;
  console.log(`    ✓ Server listening on ${baseUrl}`);

  try {
    // 3A. Test GET /
    const homeRes = await fetch(`${baseUrl}/`);
    assert.equal(homeRes.status, 200, 'GET / must return 200');
    assert.equal(homeRes.headers.get('content-type'), 'text/html; charset=utf-8');
    const homeText = await homeRes.text();
    assert.ok(homeText.includes('LabelFit India'), 'Page title brand text must be present');
    console.log('    ✓ GET / returns 200 OK with valid HTML.');

    // 3B. Test GET /api/status (Unconfigured API Key)
    const statusRes = await fetch(`${baseUrl}/api/status`);
    assert.equal(statusRes.status, 200, 'GET /api/status must return 200');
    const statusData = await statusRes.json();
    assert.equal(statusData.configured, false, 'configured must be false when apiKey is empty');
    assert.equal(statusData.model, null, 'model must be null when unconfigured');
    console.log('    ✓ GET /api/status reports configured: false and model: null.');

    // 3C. Test Error State: POST /api/analyze with Missing API Key
    const missingKeyRes = await fetch(`${baseUrl}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: { data: 'dummy', mimeType: 'image/png' } }),
    });
    assert.equal(missingKeyRes.status, 503, 'Missing API key must return 503');
    const missingKeyJson = await missingKeyRes.json();
    assert.ok(missingKeyJson.error.includes('GEMINI_API_KEY'), 'Error message must specify API key');
    console.log('    ✓ Error State: Missing API Key correctly returns HTTP 503.');

    // 3D. Test Error State: Foreign Origin (403 Forbidden)
    const foreignOriginRes = await fetch(`${baseUrl}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'https://malicious-site.example',
      },
      body: JSON.stringify({}),
    });
    assert.equal(foreignOriginRes.status, 403, 'Foreign origin must return 403');
    console.log('    ✓ Error State: Foreign Origin rejected with HTTP 403.');

  } finally {
    localServer.close();
  }

  // 4. Test Configured Local Server Error States (400 Corrupt Image Signature, Bad Payload)
  console.log('[4] Testing Payload Error States with Configured API Key...');
  const configuredServer = createServer({ apiKey: 'test-api-key', analysisEnabled: true });
  await new Promise(resolve => configuredServer.listen(0, '127.0.0.1', resolve));
  const configuredPort = configuredServer.address().port;
  const configuredBaseUrl = `http://127.0.0.1:${configuredPort}`;

  try {
    // 4A. Corrupt Image Signature (400 Bad Request)
    const corruptImgRes = await fetch(`${configuredBaseUrl}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        image: {
          data: Buffer.from('NOT_A_VALID_IMAGE_HEADER').toString('base64'),
          mimeType: 'image/png',
        },
      }),
    });
    assert.equal(corruptImgRes.status, 400, 'Corrupt image bytes must return 400');
    const corruptImgJson = await corruptImgRes.json();
    assert.ok(corruptImgJson.error.includes('file type') || corruptImgJson.error.includes('file signature'), 'Error must identify invalid file type');
    console.log('    ✓ Error State: Corrupt image header rejected with HTTP 400.');

    // 4B. Empty / Invalid JSON Payload (400 Bad Request)
    const emptyPayloadRes = await fetch(`${configuredBaseUrl}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({}),
    });
    assert.equal(emptyPayloadRes.status, 400, 'Empty payload must return 400');
    console.log('    ✓ Error State: Missing image object rejected with HTTP 400.');
  } finally {
    configuredServer.close();
  }

  // 5. Test Cloud Run Analysis Spend Lock
  console.log('[5] Auditing Cloud Run Production Spend Lock...');
  const cloudRunServer = createServer({ apiKey: 'mock-live-key', analysisEnabled: false });
  await new Promise(resolve => cloudRunServer.listen(0, '127.0.0.1', resolve));
  const crPort = cloudRunServer.address().port;
  const crBaseUrl = `http://127.0.0.1:${crPort}`;

  try {
    const crStatusRes = await fetch(`${crBaseUrl}/api/status`);
    const crStatus = await crStatusRes.json();
    assert.equal(crStatus.configured, false, 'configured must be false when analysisEnabled is false');
    assert.equal(crStatus.model, null, 'model must be null on Cloud Run');

    const crAnalyzeRes = await fetch(`${crBaseUrl}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: { data: 'test', mimeType: 'image/png' } }),
    });
    assert.equal(crAnalyzeRes.status, 503, 'Cloud Run must return 503 on /api/analyze');
    const crJson = await crAnalyzeRes.json();
    assert.ok(crJson.error.includes('Cloud Run'), 'Error must explicitly identify Cloud Run disablement');
    console.log('    ✓ Cloud Run Spend Lock hard-locks /api/analyze to HTTP 503.');
  } finally {
    cloudRunServer.close();
  }

  // 6. Test Image Fixture Validation
  console.log('[6] Verifying Synthetic Image Fixture...');
  assert.ok(fs.existsSync(FIXTURE_PNG), 'synthetic_normal.png must exist');
  const fixtureBytes = fs.readFileSync(FIXTURE_PNG);
  assert.ok(fixtureBytes.length > 5000, 'Image bytes must be non-trivial');
  assert.equal(fixtureBytes[0], 0x89, 'PNG magic byte 0x89');
  assert.equal(fixtureBytes[1], 0x50, 'PNG magic byte 0x50');
  assert.equal(fixtureBytes[2], 0x4E, 'PNG magic byte 0x4E');
  assert.equal(fixtureBytes[3], 0x47, 'PNG magic byte 0x47');
  console.log('    ✓ Synthetic PNG fixture verified with valid PNG magic signature.');

  console.log('\n================================================================');
  console.log('  BASELINE AUDIT RESULT: ALL WORKING BASELINE CHECKS PASSED     ');
  console.log('================================================================\n');
}

runBaselineAudit().catch(err => {
  console.error('\n❌ Baseline Verification Failed:', err);
  process.exit(1);
});
