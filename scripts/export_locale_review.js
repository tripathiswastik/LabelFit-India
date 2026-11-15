#!/usr/bin/env node
/**
 * Writes a review sheet for one interface language: English next to the translation, with
 * empty columns for the reviewer. Open it in Excel or Google Sheets (UTF-8, so Indian
 * scripts display correctly).
 *
 *   node scripts/export_locale_review.js hi --out hi-review.csv
 *
 * See docs/TRANSLATION_REVIEW.md for what a reviewer should check.
 */
const fs = require('node:fs');
const { readLocaleCatalog } = require('../server');

const HEADER = ['key', 'english', 'translation', 'reviewer_ok (yes/no)', 'corrected_translation', 'notes'];

function csvCell(value) {
  const text = String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

function buildReviewCsv(code, catalog) {
  const english = catalog.en && catalog.en.strings;
  const target = catalog[code] && catalog[code].strings;
  if (!english) throw new Error('English locale (locales/en.json) not found.');
  if (!target) throw new Error(`No locale "${code}". Available: ${Object.keys(catalog).join(', ')}`);
  const lines = [HEADER.map(csvCell).join(',')];
  for (const key of Object.keys(english)) {
    lines.push([key, english[key], target[key] ?? '', '', '', ''].map(csvCell).join(','));
  }
  return lines.join('\r\n') + '\r\n';
}

function main(argv) {
  const code = argv[0];
  if (!code || code.startsWith('--')) {
    console.error('Usage: node scripts/export_locale_review.js <language-code> [--out file.csv]');
    return 2;
  }
  const outIndex = argv.indexOf('--out');
  const outFile = outIndex >= 0 ? argv[outIndex + 1] : null;
  let csv;
  try {
    csv = buildReviewCsv(code, readLocaleCatalog());
  } catch (error) {
    console.error(error.message);
    return 2;
  }
  if (outFile) {
    fs.writeFileSync(outFile, '\uFEFF' + csv, 'utf8');
    console.error(`Wrote ${outFile}`);
  } else {
    process.stdout.write('\uFEFF' + csv);
  }
  return 0;
}

if (require.main === module) process.exit(main(process.argv.slice(2)));

module.exports = { buildReviewCsv, csvCell };
