#!/usr/bin/env node
/**
 * Benchmark scan logger for LabelFit India.
 *
 * Runs each package photo listed in a manifest through the SAME Gemini call the web app
 * uses (server.js analyzeImage) and saves one JSON record per image: the raw model text,
 * the parsed and normalized results, and everything needed to reproduce or audit the run
 * (image SHA-256, model requested and responded, prompt fingerprint, code commit, time).
 *
 * It never reads or writes ground truth, and it never edits the worksheet. Use
 * scripts/apply_scan_run.py to copy a finished run into the worksheet.
 *
 * Usage:
 *   node scripts/scan_benchmark.js --manifest docs/benchmark-scan-manifest.csv \
 *        --images D:/label-photos --run-id bf-run-1
 *   Add --dry-run to validate the manifest and image files without calling the API.
 *   Re-run with the same --run-id to resume: finished images are skipped.
 *
 * Images are not copied or stored. Keep them in access-controlled storage (see
 * docs/VALIDATION_PLAN.md). Each paid scan costs money and sends the image to Gemini.
 */

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { execFileSync } = require('node:child_process');
const {
  analyzeImage,
  parseImagePayload,
  resolveApiKey,
  PROMPT_FINGERPRINT,
  API_REVISION,
  MODEL,
  HttpError,
  MAX_IMAGE_BYTES,
} = require('../server');

const REPO_ROOT = path.resolve(__dirname, '..');
const MIME_BY_EXTENSION = { '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp' };
const REQUIRED_MANIFEST_COLUMNS = ['image_id', 'sku_id', 'image_file'];
const SAFE_ID = /^[A-Za-z0-9._-]+$/;

// Minimal RFC 4180 parser: quoted fields, escaped quotes, embedded newlines, BOM.
function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  const source = text.replace(/^\uFEFF/, '');
  for (let i = 0; i < source.length; i += 1) {
    const char = source[i];
    if (inQuotes) {
      if (char === '"') {
        if (source[i + 1] === '"') { field += '"'; i += 1; } else { inQuotes = false; }
      } else {
        field += char;
      }
    } else if (char === '"') {
      inQuotes = true;
    } else if (char === ',') {
      row.push(field); field = '';
    } else if (char === '\n' || char === '\r') {
      if (char === '\r' && source[i + 1] === '\n') i += 1;
      row.push(field); field = '';
      if (row.some(value => value !== '')) rows.push(row);
      row = [];
    } else {
      field += char;
    }
  }
  if (field !== '' || row.length) {
    row.push(field);
    if (row.some(value => value !== '')) rows.push(row);
  }
  if (!rows.length) return [];
  const header = rows[0].map(name => name.trim());
  return rows.slice(1).map(values => Object.fromEntries(header.map((name, index) => [name, (values[index] ?? '').trim()])));
}

function loadManifest(manifestPath) {
  const entries = parseCsv(fs.readFileSync(manifestPath, 'utf8'));
  if (!entries.length) throw new Error(`Manifest has no rows: ${manifestPath}`);
  for (const column of REQUIRED_MANIFEST_COLUMNS) {
    if (!(column in entries[0])) throw new Error(`Manifest is missing required column "${column}".`);
  }
  const seen = new Set();
  for (const entry of entries) {
    if (!SAFE_ID.test(entry.image_id)) throw new Error(`Invalid image_id "${entry.image_id}": use letters, digits, dot, dash, underscore.`);
    if (seen.has(entry.image_id)) throw new Error(`Duplicate image_id "${entry.image_id}" in manifest.`);
    seen.add(entry.image_id);
  }
  return entries;
}

function gitInfo() {
  try {
    const commit = execFileSync('git', ['rev-parse', 'HEAD'], { cwd: REPO_ROOT, encoding: 'utf8' }).trim();
    const dirty = execFileSync('git', ['status', '--porcelain', '--', 'server.js', 'scripts/scan_benchmark.js'], { cwd: REPO_ROOT, encoding: 'utf8' }).trim().length > 0;
    return { commit, dirty };
  } catch {
    return { commit: 'unknown', dirty: null };
  }
}

function sha256(bytes) {
  return crypto.createHash('sha256').update(bytes).digest('hex');
}

function resolveImagePath(imagesDir, imageFile) {
  const base = path.resolve(imagesDir);
  const full = path.resolve(base, imageFile);
  if (full !== base && !full.startsWith(base + path.sep)) throw new Error(`image_file "${imageFile}" points outside the images folder.`);
  return full;
}

// Reads and validates one image the same way the server does. Returns what scanning needs.
function loadImage(imagesDir, entry) {
  if (!entry.image_file) throw new Error('image_file is blank in the manifest.');
  const mimeType = MIME_BY_EXTENSION[path.extname(entry.image_file).toLowerCase()];
  if (!mimeType) throw new Error('Unsupported image type. Convert to JPEG, PNG or WebP first.');
  const bytes = fs.readFileSync(resolveImagePath(imagesDir, entry.image_file));
  if (bytes.length > MAX_IMAGE_BYTES) throw new Error(`Image is ${(bytes.length / 1048576).toFixed(1)} MB; the app limit is 7 MB. Resize it first.`);
  const image = parseImagePayload({ image: { data: bytes.toString('base64'), mimeType } });
  return { image, sha256: sha256(bytes), bytes: bytes.length, mimeType };
}

async function scanOne({ entry, imagesDir, apiKey, model, fetchImpl, runId, git, now = () => new Date() }) {
  const base = {
    run_id: runId,
    image_id: entry.image_id,
    sku_id: entry.sku_id,
    image_file: entry.image_file,
    panel_note: entry.panel_note || '',
    scanned_at: now().toISOString(),
    model_requested: model,
    api_revision: API_REVISION,
    prompt_fingerprint: PROMPT_FINGERPRINT,
    code_commit: git.commit,
    code_dirty: git.dirty,
  };
  let loaded;
  try {
    loaded = loadImage(imagesDir, entry);
  } catch (error) {
    return { ...base, error: { stage: 'image', status: error instanceof HttpError ? error.status : null, message: error.message } };
  }
  const record = { ...base, image_sha256: loaded.sha256, image_bytes: loaded.bytes, image_mime: loaded.mimeType };
  const started = Date.now();
  try {
    const analysis = await analyzeImage({ apiKey, model, image: loaded.image, fetchImpl });
    return {
      ...record,
      latency_ms: Date.now() - started,
      model_responded: analysis.modelResponded,
      raw_model_output: analysis.rawOutputText,
      parsed: analysis.parsed,
      normalized: analysis.result,
      error: null,
    };
  } catch (error) {
    return { ...record, latency_ms: Date.now() - started, error: { stage: 'model', status: error instanceof HttpError ? error.status : null, message: error.message } };
  }
}

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function runScan(options) {
  const {
    manifestPath, imagesDir, outDir = path.join(REPO_ROOT, 'benchmark-runs'), runId,
    only = null, force = false, dryRun = false, delayMs = 1500, model = MODEL,
    apiKey = dryRun ? '' : resolveApiKey(), fetchImpl = globalThis.fetch, log = console.log,
    now = () => new Date(),
  } = options;
  if (!SAFE_ID.test(runId || '')) throw new Error('Provide --run-id using letters, digits, dot, dash, underscore.');
  if (!dryRun && !apiKey) throw new Error('No Gemini API key found. Set GEMINI_API_KEY or add it to this project\'s .env file.');

  let entries = loadManifest(manifestPath);
  if (only) entries = entries.filter(entry => only.includes(entry.sku_id) || only.includes(entry.image_id));
  if (!entries.length) throw new Error('No manifest rows match --only.');

  const runDir = path.join(outDir, runId);
  const git = gitInfo();
  const metaPath = path.join(runDir, 'run.json');
  const meta = {
    run_id: runId,
    model_requested: model,
    api_revision: API_REVISION,
    prompt_fingerprint: PROMPT_FINGERPRINT,
    code_commit: git.commit,
    code_dirty: git.dirty,
    manifest_sha256: sha256(fs.readFileSync(manifestPath)),
    node_version: process.version,
    started_at: now().toISOString(),
  };

  if (!dryRun) {
    fs.mkdirSync(runDir, { recursive: true });
    if (fs.existsSync(metaPath)) {
      const previous = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
      // One run = one model + one prompt. Mixing them would make results incomparable.
      if (!force && (previous.model_requested !== model || previous.prompt_fingerprint !== PROMPT_FINGERPRINT)) {
        throw new Error(`Run "${runId}" was started with model ${previous.model_requested} and prompt ${previous.prompt_fingerprint}; current is ${model} / ${PROMPT_FINGERPRINT}. Use a new --run-id (or --force to override).`);
      }
    } else {
      fs.writeFileSync(metaPath, JSON.stringify(meta, null, 2));
    }
  }

  const summary = { scanned: 0, skipped: 0, failed: 0, invalid: 0, planned: 0 };
  for (const entry of entries) {
    const recordPath = path.join(runDir, `${entry.image_id}.json`);
    if (dryRun) {
      try {
        loadImage(imagesDir, entry);
        summary.planned += 1;
        log(`ok      ${entry.image_id} (${entry.sku_id}) ${entry.image_file}`);
      } catch (error) {
        summary.invalid += 1;
        log(`INVALID ${entry.image_id}: ${error.message}`);
      }
      continue;
    }
    if (!force && fs.existsSync(recordPath)) {
      const existing = JSON.parse(fs.readFileSync(recordPath, 'utf8'));
      if (!existing.error) {
        summary.skipped += 1;
        log(`skip    ${entry.image_id} (already scanned)`);
        continue;
      }
    }
    const record = await scanOne({ entry, imagesDir, apiKey, model, fetchImpl, runId, git, now });
    fs.writeFileSync(recordPath, JSON.stringify(record, null, 2));
    if (record.error) {
      summary.failed += 1;
      log(`FAILED  ${entry.image_id}: [${record.error.stage}] ${record.error.message}`);
    } else {
      summary.scanned += 1;
      log(`scanned ${entry.image_id} (${entry.sku_id}) in ${record.latency_ms} ms`);
    }
    if (delayMs > 0) await sleep(delayMs);
  }
  return { summary, runDir, meta };
}

function parseArgs(argv) {
  const args = { force: false, dryRun: false, delayMs: 1500, model: MODEL, only: null, outDir: undefined };
  for (let i = 0; i < argv.length; i += 1) {
    const flag = argv[i];
    const next = () => { i += 1; if (i >= argv.length) throw new Error(`${flag} needs a value.`); return argv[i]; };
    if (flag === '--manifest') args.manifestPath = next();
    else if (flag === '--images') args.imagesDir = next();
    else if (flag === '--out') args.outDir = next();
    else if (flag === '--run-id') args.runId = next();
    else if (flag === '--only') args.only = next().split(',').map(value => value.trim()).filter(Boolean);
    else if (flag === '--model') args.model = next();
    else if (flag === '--delay-ms') args.delayMs = Number(next());
    else if (flag === '--force') args.force = true;
    else if (flag === '--dry-run') args.dryRun = true;
    else throw new Error(`Unknown option ${flag}.`);
  }
  if (!args.manifestPath || !args.imagesDir || !args.runId) {
    throw new Error('Required: --manifest <csv> --images <folder> --run-id <name>');
  }
  if (!Number.isFinite(args.delayMs) || args.delayMs < 0) throw new Error('--delay-ms must be a non-negative number.');
  return args;
}

async function main() {
  let args;
  try {
    args = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(error.message);
    console.error('See the header of scripts/scan_benchmark.js for usage.');
    process.exit(2);
  }
  try {
    const { summary, runDir } = await runScan(args);
    console.log(`\nDone. ${JSON.stringify(summary)}`);
    if (!args.dryRun) console.log(`Records: ${runDir}\nNext: python scripts/apply_scan_run.py --run ${runDir} --worksheet <worksheet.csv> --dry-run`);
    process.exit(summary.failed || summary.invalid ? 1 : 0);
  } catch (error) {
    console.error(error.message);
    process.exit(2);
  }
}

if (require.main === module) main();

module.exports = { parseCsv, loadManifest, loadImage, scanOne, runScan, parseArgs, resolveImagePath };
