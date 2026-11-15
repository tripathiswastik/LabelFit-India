const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { parseCsv, loadManifest, scanOne, runScan, parseArgs, resolveImagePath } = require('../scripts/scan_benchmark.js');
const { PROMPT_FINGERPRINT } = require('../server.js');

const PNG = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10, 1, 2, 3]);
const FIELDS = ['productName', 'ageMarking', 'ingredients', 'allergenDeclaration', 'nutritionPanel', 'preparationAndStorage'];

function mockFetch(counter = { calls: 0 }, { fail = false, model = 'gemini-responded' } = {}) {
  const impl = async () => {
    counter.calls += 1;
    if (fail) return { ok: false, status: 500, json: async () => ({}) };
    const field = { value: 'Rice flour', evidence: 'Rice flour', readStatus: 'clear' };
    const text = JSON.stringify(Object.fromEntries(FIELDS.map(name => [name, field])));
    return { ok: true, json: async () => ({ model, steps: [{ type: 'model_output', content: [{ type: 'text', text }] }] }) };
  };
  impl.counter = counter;
  return impl;
}

function workspace(rows = [['IMG-A', 'SKU-A', 'a.png'], ['IMG-B', 'SKU-B', 'b.png']]) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'labelfit-scan-'));
  const images = path.join(dir, 'images');
  fs.mkdirSync(images);
  for (const [, , file] of rows) if (file && !file.startsWith('missing')) fs.writeFileSync(path.join(images, file), PNG);
  const manifest = path.join(dir, 'manifest.csv');
  fs.writeFileSync(manifest, ['image_id,sku_id,image_file', ...rows.map(r => r.join(','))].join('\n'));
  return { dir, images, manifest, out: path.join(dir, 'runs') };
}
const base = ws => ({ manifestPath: ws.manifest, imagesDir: ws.images, outDir: ws.out, runId: 'run1', delayMs: 0, apiKey: 'k', log: () => {} });
const readRecord = (ws, id) => JSON.parse(fs.readFileSync(path.join(ws.out, 'run1', `${id}.json`), 'utf8'));

test('parseCsv handles BOM, quotes, commas, escaped quotes and embedded newlines', () => {
  const rows = parseCsv('\uFEFFa,b,c\r\n1,"x, y","say ""hi"""\r\n2,"line1\nline2",z\r\n');
  assert.deepEqual(rows, [{ a: '1', b: 'x, y', c: 'say "hi"' }, { a: '2', b: 'line1\nline2', c: 'z' }]);
});

test('manifest validation rejects missing columns, duplicate and unsafe ids', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'labelfit-m-'));
  const write = text => { const p = path.join(dir, 'm.csv'); fs.writeFileSync(p, text); return p; };
  assert.throws(() => loadManifest(write('image_id,sku_id\nA,B\n')), /image_file/);
  assert.throws(() => loadManifest(write('image_id,sku_id,image_file\nA,S,a.png\nA,S,b.png\n')), /Duplicate/);
  assert.throws(() => loadManifest(write('image_id,sku_id,image_file\n../evil,S,a.png\n')), /Invalid image_id/);
  assert.throws(() => loadManifest(write('image_id,sku_id,image_file\n')), /no rows/);
});

test('image paths cannot escape the images folder', () => {
  assert.throws(() => resolveImagePath('/tmp/images', '../secret.png'), /outside/);
  assert.throws(() => resolveImagePath('/tmp/images', '/etc/passwd'), /outside/);
  assert.ok(resolveImagePath('/tmp/images', 'sub/a.png').endsWith(path.join('sub', 'a.png')));
});

test('a scan writes a complete audit record and never stores the image', async () => {
  const ws = workspace();
  const fetchImpl = mockFetch();
  const { summary } = await runScan({ ...base(ws), fetchImpl, model: 'gemini-test' });
  assert.deepEqual(summary, { scanned: 2, skipped: 0, failed: 0, invalid: 0, planned: 0 });
  const record = readRecord(ws, 'IMG-A');
  assert.equal(record.sku_id, 'SKU-A');
  assert.equal(record.model_requested, 'gemini-test');
  assert.equal(record.model_responded, 'gemini-responded');
  assert.equal(record.prompt_fingerprint, PROMPT_FINGERPRINT);
  assert.match(record.image_sha256, /^[0-9a-f]{64}$/);
  assert.equal(record.image_bytes, PNG.length);
  assert.equal(record.error, null);
  assert.equal(record.normalized.ingredients.readStatus, 'clear');
  assert.ok(record.raw_model_output.includes('Rice flour'));
  assert.ok(record.parsed && record.scanned_at && record.latency_ms >= 0);
  const files = fs.readdirSync(path.join(ws.out, 'run1')).sort();
  assert.deepEqual(files, ['IMG-A.json', 'IMG-B.json', 'run.json']);
  assert.equal(JSON.stringify(record).includes(PNG.toString('base64')), false);
});

test('re-running the same run id resumes without paying twice', async () => {
  const ws = workspace();
  const counter = { calls: 0 };
  await runScan({ ...base(ws), fetchImpl: mockFetch(counter) });
  assert.equal(counter.calls, 2);
  const { summary } = await runScan({ ...base(ws), fetchImpl: mockFetch(counter) });
  assert.equal(counter.calls, 2);
  assert.equal(summary.skipped, 2);
});

test('failed scans are recorded, reported, and retried on the next run', async () => {
  const ws = workspace();
  const first = await runScan({ ...base(ws), fetchImpl: mockFetch({ calls: 0 }, { fail: true }) });
  assert.equal(first.summary.failed, 2);
  const record = readRecord(ws, 'IMG-A');
  assert.equal(record.error.stage, 'model');
  assert.equal(record.error.status, 502);
  assert.equal(record.normalized, undefined);
  const counter = { calls: 0 };
  const second = await runScan({ ...base(ws), fetchImpl: mockFetch(counter) });
  assert.equal(counter.calls, 2, 'failed images are scanned again');
  assert.equal(second.summary.scanned, 2);
  assert.equal(readRecord(ws, 'IMG-A').error, null);
});

test('one bad image does not stop the rest, and is recorded as an image error', async () => {
  const ws = workspace([['IMG-A', 'SKU-A', 'a.png'], ['IMG-B', 'SKU-B', 'missing.png'], ['IMG-C', 'SKU-C', 'c.heic']]);
  const { summary } = await runScan({ ...base(ws), fetchImpl: mockFetch() });
  assert.equal(summary.scanned, 1);
  assert.equal(summary.failed, 2);
  assert.equal(readRecord(ws, 'IMG-B').error.stage, 'image');
  assert.match(readRecord(ws, 'IMG-C').error.message, /Unsupported image type/);
});

test('a file whose bytes do not match its extension is rejected before any API call', async () => {
  const ws = workspace();
  fs.writeFileSync(path.join(ws.images, 'a.png'), Buffer.from('not an image at all'));
  const counter = { calls: 0 };
  const { summary } = await runScan({ ...base(ws), fetchImpl: mockFetch(counter), only: ['IMG-A'] });
  assert.equal(counter.calls, 0);
  assert.equal(summary.failed, 1);
});

test('dry run validates files and makes no API call or output', async () => {
  const ws = workspace([['IMG-A', 'SKU-A', 'a.png'], ['IMG-B', 'SKU-B', 'missing.png']]);
  const counter = { calls: 0 };
  const { summary } = await runScan({ ...base(ws), fetchImpl: mockFetch(counter), dryRun: true, apiKey: '' });
  assert.equal(counter.calls, 0);
  assert.deepEqual([summary.planned, summary.invalid], [1, 1]);
  assert.equal(fs.existsSync(ws.out), false);
});

test('--only limits the scan by sku_id or image_id', async () => {
  const ws = workspace();
  const counter = { calls: 0 };
  await runScan({ ...base(ws), fetchImpl: mockFetch(counter), only: ['SKU-B'] });
  assert.equal(counter.calls, 1);
  assert.equal(fs.existsSync(path.join(ws.out, 'run1', 'IMG-B.json')), true);
  assert.equal(fs.existsSync(path.join(ws.out, 'run1', 'IMG-A.json')), false);
  await assert.rejects(() => runScan({ ...base(ws), fetchImpl: mockFetch(), only: ['NOPE'] }), /No manifest rows match/);
});

test('a run cannot silently mix two models', async () => {
  const ws = workspace();
  await runScan({ ...base(ws), fetchImpl: mockFetch(), model: 'model-one', only: ['IMG-A'] });
  await assert.rejects(() => runScan({ ...base(ws), fetchImpl: mockFetch(), model: 'model-two' }), /new --run-id/);
  const { summary } = await runScan({ ...base(ws), fetchImpl: mockFetch(), model: 'model-two', force: true });
  assert.ok(summary.scanned >= 1);
});

test('run.json records what is needed to reproduce the run', async () => {
  const ws = workspace();
  await runScan({ ...base(ws), fetchImpl: mockFetch(), model: 'gemini-test' });
  const meta = JSON.parse(fs.readFileSync(path.join(ws.out, 'run1', 'run.json'), 'utf8'));
  assert.equal(meta.model_requested, 'gemini-test');
  assert.equal(meta.prompt_fingerprint, PROMPT_FINGERPRINT);
  assert.match(meta.manifest_sha256, /^[0-9a-f]{64}$/);
  assert.ok(meta.code_commit && meta.node_version && meta.api_revision);
});

test('run id and options are validated', async () => {
  const ws = workspace();
  await assert.rejects(() => runScan({ ...base(ws), runId: '../x', fetchImpl: mockFetch() }), /run-id/);
  await assert.rejects(() => runScan({ ...base(ws), apiKey: '', fetchImpl: mockFetch() }), /API key/);
  assert.throws(() => parseArgs(['--manifest', 'm.csv']), /Required/);
  assert.throws(() => parseArgs(['--bogus']), /Unknown option/);
  const args = parseArgs(['--manifest', 'm.csv', '--images', 'i', '--run-id', 'r', '--only', 'A, B', '--dry-run']);
  assert.deepEqual(args.only, ['A', 'B']);
  assert.equal(args.dryRun, true);
});

test('scanOne reports image problems without throwing', async () => {
  const ws = workspace();
  const record = await scanOne({
    entry: { image_id: 'IMG-X', sku_id: 'S', image_file: '' }, imagesDir: ws.images, apiKey: 'k',
    model: 'm', fetchImpl: mockFetch(), runId: 'r', git: { commit: 'abc', dirty: false },
  });
  assert.equal(record.error.stage, 'image');
});
