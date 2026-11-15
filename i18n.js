/*
 * Interface-language helpers for LabelFit India. Loaded by the page as a plain script and
 * by Node tests as a module.
 *
 * Only the interface is translated. Transcribed label text is never translated: the prompt
 * tells the model to keep the printed language, script and wording.
 *
 * A language is offered in the picker only when its locale file says "reviewed": true.
 * An unreviewed draft can be previewed by a reviewer with ?lang=<code>, and the page then
 * shows a draft banner. See docs/TRANSLATION_REVIEW.md.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LabelFitI18n = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const DEFAULT_LANGUAGE = 'en';

  // Replaces {name} placeholders. Unknown placeholders are left visible rather than dropped.
  function format(template, vars) {
    const values = vars || {};
    return String(template).replace(/\{(\w+)\}/g, (match, name) => (name in values ? String(values[name]) : match));
  }

  function placeholders(template) {
    return Array.from(String(template).matchAll(/\{(\w+)\}/g), match => match[1]).sort();
  }

  function isSelectable(meta) {
    return Boolean(meta && meta.reviewed === true);
  }

  // available: { code: { reviewed: boolean, ... } }
  // requested: value of ?lang= (may preview an unreviewed draft); stored: saved choice.
  // Returns { language, preview } where preview is true for an unreviewed draft.
  function pickLanguage({ requested, stored, available }) {
    const languages = available || {};
    if (requested && Object.prototype.hasOwnProperty.call(languages, requested)) {
      return { language: requested, preview: !isSelectable(languages[requested]) };
    }
    if (stored && Object.prototype.hasOwnProperty.call(languages, stored) && isSelectable(languages[stored])) {
      return { language: stored, preview: false };
    }
    return { language: DEFAULT_LANGUAGE, preview: false };
  }

  // Codes shown in the language picker: reviewed languages, plus the draft being previewed.
  function pickerCodes({ available, previewCode }) {
    const languages = available || {};
    const codes = Object.keys(languages).filter(code => isSelectable(languages[code]));
    if (previewCode && languages[previewCode] && !codes.includes(previewCode)) codes.push(previewCode);
    return codes.sort((a, b) => (a === DEFAULT_LANGUAGE ? -1 : b === DEFAULT_LANGUAGE ? 1 : a.localeCompare(b)));
  }

  return { DEFAULT_LANGUAGE, format, placeholders, isSelectable, pickLanguage, pickerCodes };
});
