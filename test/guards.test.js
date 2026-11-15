const test = require('node:test');
const assert = require('node:assert/strict');
const { normalizeField, hasTokenSupport, hasConflictingNumbers, ALLERGEN_DECLARATION_PATTERN } = require('../server.js');

const status = (field, value, evidence) => normalizeField({ value, evidence, readStatus: 'clear' }, field).readStatus;

test('unit spacing does not downgrade a faithful nutrition read', () => {
  assert.equal(status('nutritionPanel', 'Iron 12.5 mg', 'Iron 12.5mg'), 'clear');
  assert.equal(status('nutritionPanel', 'Protein 8.2g', 'Protein 8.2 g'), 'clear');
});

test('a changed number is still downgraded', () => {
  assert.equal(status('nutritionPanel', 'Iron 12.5 mg', 'Iron 1.25mg'), 'uncertain');
  assert.equal(hasConflictingNumbers('12.5 mg', '12.5mg'), false);
  assert.equal(hasConflictingNumbers('12.5 mg', '2.5mg'), true);
});

test('Devanagari digits are treated as the same numbers', () => {
  assert.equal(hasConflictingNumbers('लोह 12.5 mg', 'iron 12.5 mg'), false);
});

test('Devanagari words are not fragmented by the tokenizer', () => {
  assert.equal(hasTokenSupport('रागी आटा', 'रागी आटा 25%'), true);
  assert.equal(hasTokenSupport('रागी आटा', 'गेहूं आटा'), false);
});

test('Hindi allergen declaration with matching evidence can be clear', () => {
  assert.ok(ALLERGEN_DECLARATION_PATTERN.test('इसमें दूध है'));
  assert.equal(status('allergenDeclaration', 'इसमें दूध है', 'इसमें दूध है'), 'clear');
});

test('Hindi allergen in value but not in evidence is downgraded', () => {
  assert.equal(status('allergenDeclaration', 'इसमें दूध और सोया है', 'इसमें दूध है'), 'uncertain');
});

test('English declaration markers still work and ingredient lists are not declarations', () => {
  assert.ok(ALLERGEN_DECLARATION_PATTERN.test('May contain traces of peanut'));
  assert.equal(status('allergenDeclaration', 'Wheat, milk, sugar', 'Wheat, milk, sugar'), 'uncertain');
});

test('newly covered allergens are checked against evidence', () => {
  assert.equal(status('allergenDeclaration', 'Contains shrimp', 'Contains: crustacean'), 'uncertain');
  assert.equal(status('allergenDeclaration', 'Contains sulphites', 'Contains sulphites'), 'clear');
});

test('evidence with no usable text cannot support a value', () => {
  assert.equal(hasTokenSupport('Ragi cereal', '---'), false);
  assert.equal(hasTokenSupport('---', 'Ragi cereal'), true);
});
