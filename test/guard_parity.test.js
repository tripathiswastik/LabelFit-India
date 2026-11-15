const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { normalizeField } = require('../server.js');

const { cases } = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'guard_cases.json'), 'utf8'));

// The same cases run against the Python guards in tests/test_guard_parity.py.
for (const c of cases) {
  test(`guard parity (node): ${c.name}`, () => {
    const result = normalizeField({ value: c.value, evidence: c.evidence, readStatus: c.readStatus }, c.field);
    assert.equal(result.readStatus, c.expected);
  });
}

test('guard cases cover every field and all three outcomes', () => {
  assert.ok(cases.length >= 30);
  assert.deepEqual([...new Set(cases.map(c => c.expected))].sort(), ['clear', 'not_visible', 'uncertain']);
  for (const field of ['productName', 'ageMarking', 'ingredients', 'allergenDeclaration', 'nutritionPanel', 'preparationAndStorage']) {
    assert.ok(cases.some(c => c.field === field), `no case for ${field}`);
  }
});
