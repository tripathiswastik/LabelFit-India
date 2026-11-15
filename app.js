const fileInput = document.querySelector('#file-input');
const dropzone = document.querySelector('#dropzone');
const preview = document.querySelector('#preview');
const previewWrap = document.querySelector('#preview-wrap');
const uploadEmpty = document.querySelector('#upload-empty');
const analyzeButton = document.querySelector('#analyze');
const photoConfirmation = document.querySelector('#photo-confirm');
const apiState = document.querySelector('#api-state');
const apiStateText = document.querySelector('#api-state-text');
const resultsEmpty = document.querySelector('#results-empty');
const resultsContent = document.querySelector('#results-content');
const loading = document.querySelector('#loading');
const cropDialog = document.querySelector('#crop-dialog');
const cropCanvas = document.querySelector('#crop-canvas');
const cropContext = cropCanvas.getContext('2d');
const cropPhotoButton = document.querySelector('#crop-photo');
const useCropButton = document.querySelector('#use-crop');

const MAX_IMAGE_BYTES = 7 * 1024 * 1024; // what the server accepts (after resizing)
const MAX_SOURCE_BYTES = 30 * 1024 * 1024; // what we will try to resize in the browser
const MAX_EDGE_PX = 2560; // long edge after resizing; small print needs resolution
const JPEG_QUALITIES = [0.9, 0.82, 0.74, 0.66];
let selectedFile = null;
let previewUrl = null;
let analysisReady = false;
let analysisInProgress = false;
let cropBitmap = null;
let cropPreviewCanvas = null;
let cropSelection = null;
let cropPointerStart = null;

// Interface language. Only the interface is translated, never the label text itself.
const I18n = window.LabelFitI18n;
let englishStrings = {};
let strings = {};
let availableLanguages = {};
let currentLanguage = I18n.DEFAULT_LANGUAGE;
let draftPreview = false;
let serviceState = { configured: false, model: '', key: 'apiChecking' };
let lastView = null; // what the results panel last showed, so it can be redrawn in another language

// Falls back to English, then to the key itself, so a missing string is never blank.
function t(key, vars) {
  return I18n.format(strings[key] ?? englishStrings[key] ?? key, vars);
}

// An error whose message is a translatable string key. Messages sent by the server stay in English.
class LocalizedError extends Error {
  constructor(key, vars) {
    super(key);
    this.key = key;
    this.vars = vars;
  }
}

function updateAnalyzeButton() {
  analyzeButton.disabled = !selectedFile || !analysisReady || !photoConfirmation.checked || analysisInProgress;
}

function setServiceState(configured, model, key) {
  analysisReady = configured;
  serviceState = { configured, model, key: key || (configured ? 'apiReady' : 'apiNotConfigured') };
  apiState.classList.toggle('ready', configured);
  apiState.classList.toggle('error', !configured);
  renderServiceState();
  updateAnalyzeButton();
}

function renderServiceState() {
  apiStateText.textContent = t(serviceState.key, { model: serviceState.model });
}

async function loadServiceState() {
  try {
    const response = await fetch('/api/status', { cache: 'no-store' });
    if (!response.ok) throw new Error('status');
    const status = await response.json();
    setServiceState(Boolean(status.configured), status.model, status.configured ? 'apiReady' : 'apiNotConfigured');
  } catch {
    setServiceState(false, '', 'apiUnavailable');
  }
}

// error is { key, vars } for an interface string, or { text } for a message from the server.
function showError(error) {
  lastView = { type: 'error', error };
  resultsEmpty.hidden = true;
  resultsContent.replaceChildren();
  const header = document.createElement('div');
  header.className = 'result-header';
  const heading = document.createElement('div');
  const eyebrow = document.createElement('p');
  eyebrow.className = 'eyebrow';
  eyebrow.textContent = t('errorEyebrow');
  const title = document.createElement('h3');
  title.textContent = t('errorTitle');
  heading.append(eyebrow, title);
  header.append(heading);
  const errorText = document.createElement('p');
  errorText.className = 'field-value';
  errorText.textContent = error.text ?? t(error.key, error.vars);
  resultsContent.append(header, errorText);
  resultsContent.hidden = false;
  loading.hidden = true;
}

// Tags results written in an Indian script so screen readers pick the right voice.
// One language per script; Devanagari is also used for Marathi and Nepali, and Bengali for
// Assamese, so this is a best guess for the common case. Mixed text takes the language of
// whichever has more letters; text with no letters is left untagged (page language). English
// text is tagged too, so it is not read with a Hindi voice when the interface is in Hindi.
const SCRIPT_LANGUAGES = [
  [/[\u0900-\u097F]/g, 'hi'], [/[\u0980-\u09FF]/g, 'bn'], [/[\u0A00-\u0A7F]/g, 'pa'],
  [/[\u0A80-\u0AFF]/g, 'gu'], [/[\u0B00-\u0B7F]/g, 'or'], [/[\u0B80-\u0BFF]/g, 'ta'],
  [/[\u0C00-\u0C7F]/g, 'te'], [/[\u0C80-\u0CFF]/g, 'kn'], [/[\u0D00-\u0D7F]/g, 'ml'],
];

function languageOf(text) {
  if (!text) return null;
  const latin = (text.match(/[A-Za-z]/g) || []).length;
  let best = null;
  let bestCount = 0;
  for (const [pattern, language] of SCRIPT_LANGUAGES) {
    const count = (text.match(pattern) || []).length;
    if (count > bestCount) { best = language; bestCount = count; }
  }
  if (best && bestCount > latin) return best;
  return latin > 0 ? 'en' : null;
}

function renderResult(result, model) {
  lastView = { type: 'result', result, model };
  const fields = [
    [t('fieldProductName'), result.productName],
    [t('fieldAgeMarking'), result.ageMarking],
    [t('fieldIngredients'), result.ingredients],
    [t('fieldAllergen'), result.allergenDeclaration],
    [t('fieldNutrition'), result.nutritionPanel],
    [t('fieldPreparation'), result.preparationAndStorage],
  ];

  resultsContent.replaceChildren();
  const header = document.createElement('div');
  header.className = 'result-header';
  const heading = document.createElement('div');
  const eyebrow = document.createElement('p');
  eyebrow.className = 'eyebrow';
  eyebrow.textContent = t('resultsEyebrow');
  const title = document.createElement('h3');
  title.textContent = t('resultsTitle');
  heading.append(eyebrow, title);
  const badge = document.createElement('span');
  badge.className = 'model-tag';
  badge.textContent = model || 'Gemini';
  header.append(heading, badge);
  resultsContent.append(header);

  for (const [label, data = {}] of fields) {
    const row = document.createElement('div');
    row.className = 'field-row';
    const top = document.createElement('div');
    top.className = 'field-top';
    const name = document.createElement('span');
    name.className = 'field-name';
    name.textContent = label;
    const readStatus = ['clear', 'uncertain', 'not_visible'].includes(data.readStatus) ? data.readStatus : 'uncertain';
    const status = document.createElement('span');
    status.className = `confidence ${readStatus}`;
    status.textContent = readStatus === 'not_visible' ? t('statusNotVisible') : readStatus === 'clear' ? t('statusReadable') : t('statusCheck');
    top.append(name, status);

    const value = document.createElement('div');
    value.className = 'field-value';
    value.textContent = data.value || t('noText');
    const valueLanguage = languageOf(data.value);
    if (valueLanguage) value.lang = valueLanguage;
    row.append(top, value);

    if (data.evidence) {
      const evidence = document.createElement('div');
      evidence.className = 'field-evidence';
      const evidenceLabel = document.createElement('b');
      evidenceLabel.textContent = t('snippetLabel');
      const snippet = document.createElement('span');
      snippet.textContent = data.evidence;
      const snippetLanguage = languageOf(data.evidence);
      if (snippetLanguage) snippet.lang = snippetLanguage;
      evidence.append(evidenceLabel, snippet);
      row.append(evidence);
    }
    resultsContent.append(row);
  }

  const reminder = document.createElement('div');
  reminder.className = 'note-list';
  reminder.textContent = t('reminder');
  resultsContent.append(reminder);
  resultsContent.hidden = false;
  resultsEmpty.hidden = true;
}

// Phone photos are often 8-12 MB. Resize and re-encode in the browser so they fit
// the server limit. Files already small enough are sent unchanged.
async function loadBitmap(file) {
  if (window.createImageBitmap) {
    try { return await createImageBitmap(file, { imageOrientation: 'from-image' }); } catch { /* fall through */ }
  }
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => { URL.revokeObjectURL(url); resolve(img); };
    img.onerror = () => { URL.revokeObjectURL(url); reject(new LocalizedError('errLoad')); };
    img.src = url;
  });
}

function canvasToBlob(canvas, type, quality) {
  return new Promise(resolve => canvas.toBlob(resolve, type, quality));
}

function drawCropSelection() {
  if (!cropBitmap) return;
  const width = cropCanvas.width;
  const height = cropCanvas.height;
  cropContext.clearRect(0, 0, width, height);
  cropContext.drawImage(cropPreviewCanvas, 0, 0, width, height);
  if (!cropSelection) return;
  cropContext.fillStyle = 'rgba(20, 32, 24, .48)';
  cropContext.fillRect(0, 0, width, height);
  cropContext.clearRect(cropSelection.x, cropSelection.y, cropSelection.width, cropSelection.height);
  cropContext.drawImage(cropBitmap,
    cropSelection.x * cropBitmap.width / width,
    cropSelection.y * cropBitmap.height / height,
    cropSelection.width * cropBitmap.width / width,
    cropSelection.height * cropBitmap.height / height,
    cropSelection.x, cropSelection.y, cropSelection.width, cropSelection.height);
  cropContext.strokeStyle = '#fff';
  cropContext.lineWidth = Math.max(2, width / 500);
  cropContext.strokeRect(cropSelection.x, cropSelection.y, cropSelection.width, cropSelection.height);
}

function cropPoint(event) {
  const bounds = cropCanvas.getBoundingClientRect();
  return {
    x: Math.max(0, Math.min(cropCanvas.width, (event.clientX - bounds.left) * cropCanvas.width / bounds.width)),
    y: Math.max(0, Math.min(cropCanvas.height, (event.clientY - bounds.top) * cropCanvas.height / bounds.height)),
  };
}

async function openCropTool() {
  if (!selectedFile) return;
  try {
    cropBitmap = await loadBitmap(selectedFile);
    const scale = Math.min(1, 1400 / Math.max(cropBitmap.width, cropBitmap.height));
    cropCanvas.width = Math.max(1, Math.round(cropBitmap.width * scale));
    cropCanvas.height = Math.max(1, Math.round(cropBitmap.height * scale));
    cropPreviewCanvas = document.createElement('canvas');
    cropPreviewCanvas.width = cropCanvas.width;
    cropPreviewCanvas.height = cropCanvas.height;
    cropPreviewCanvas.getContext('2d').drawImage(cropBitmap, 0, 0, cropCanvas.width, cropCanvas.height);
    cropSelection = null;
    useCropButton.disabled = true;
    drawCropSelection();
    cropDialog.showModal();
  } catch (error) {
    showError(error instanceof LocalizedError
      ? { key: error.key, vars: error.vars }
      : { text: error.message || 'Could not open the photo crop tool.' });
  }
}

function closeCropTool() {
  if (cropDialog.open) cropDialog.close();
  if (cropBitmap?.close) cropBitmap.close();
  cropBitmap = null;
  cropPreviewCanvas = null;
  cropSelection = null;
}
cropDialog.addEventListener('close', () => {
  if (cropBitmap?.close) cropBitmap.close();
  cropBitmap = null;
  cropPreviewCanvas = null;
  cropSelection = null;
});

cropCanvas.addEventListener('pointerdown', event => {
  if (!cropBitmap) return;
  cropPointerStart = cropPoint(event);
  cropSelection = { x: cropPointerStart.x, y: cropPointerStart.y, width: 0, height: 0 };
  cropCanvas.setPointerCapture(event.pointerId);
  drawCropSelection();
});
cropCanvas.addEventListener('pointermove', event => {
  if (!cropPointerStart) return;
  const point = cropPoint(event);
  cropSelection = {
    x: Math.min(cropPointerStart.x, point.x),
    y: Math.min(cropPointerStart.y, point.y),
    width: Math.abs(point.x - cropPointerStart.x),
    height: Math.abs(point.y - cropPointerStart.y),
  };
  useCropButton.disabled = cropSelection.width < 24 || cropSelection.height < 24;
  drawCropSelection();
});
cropCanvas.addEventListener('pointerup', () => { cropPointerStart = null; });
cropCanvas.addEventListener('pointercancel', () => { cropPointerStart = null; });
cropPhotoButton.addEventListener('click', event => { event.stopPropagation(); openCropTool(); });
document.querySelector('#close-crop').addEventListener('click', closeCropTool);
document.querySelector('#cancel-crop').addEventListener('click', closeCropTool);
useCropButton.addEventListener('click', async () => {
  if (!cropBitmap || !cropSelection) return;
  const sourceScaleX = cropBitmap.width / cropCanvas.width;
  const sourceScaleY = cropBitmap.height / cropCanvas.height;
  const sourceX = cropSelection.x * sourceScaleX;
  const sourceY = cropSelection.y * sourceScaleY;
  const sourceWidth = cropSelection.width * sourceScaleX;
  const sourceHeight = cropSelection.height * sourceScaleY;
  const outputScale = Math.min(1, MAX_EDGE_PX / Math.max(sourceWidth, sourceHeight));
  const output = document.createElement('canvas');
  output.width = Math.max(1, Math.round(sourceWidth * outputScale));
  output.height = Math.max(1, Math.round(sourceHeight * outputScale));
  const context = output.getContext('2d');
  context.fillStyle = '#fff';
  context.fillRect(0, 0, output.width, output.height);
  context.drawImage(cropBitmap, sourceX, sourceY, sourceWidth, sourceHeight, 0, 0, output.width, output.height);
  const blob = await canvasToBlob(output, 'image/jpeg', 0.94);
  if (!blob) {
    closeCropTool();
    showError({ text: 'Could not prepare that crop. Please choose the photo again.' });
    return;
  }
  const croppedFile = new File([blob], selectedFile.name.replace(/\.[^.]+$/, '') + '-crop.jpg', { type: 'image/jpeg' });
  closeCropTool();
  chooseFile(croppedFile);
});

async function prepareImage(file) {
  if (file.size <= MAX_IMAGE_BYTES) return { blob: file, mimeType: file.type };
  const bitmap = await loadBitmap(file);
  const width = bitmap.width || bitmap.naturalWidth;
  const height = bitmap.height || bitmap.naturalHeight;
  const scale = Math.min(1, MAX_EDGE_PX / Math.max(width, height));
  const canvas = document.createElement('canvas');
  canvas.width = Math.max(1, Math.round(width * scale));
  canvas.height = Math.max(1, Math.round(height * scale));
  const context = canvas.getContext('2d');
  context.fillStyle = '#fff'; // PNG/WebP transparency becomes white, not black
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.drawImage(bitmap, 0, 0, canvas.width, canvas.height);
  if (bitmap.close) bitmap.close();
  for (const quality of JPEG_QUALITIES) {
    const blob = await canvasToBlob(canvas, 'image/jpeg', quality);
    if (blob && blob.size <= MAX_IMAGE_BYTES) return { blob, mimeType: 'image/jpeg' };
  }
  throw new LocalizedError('errTooLarge');
}

function chooseFile(file) {
  if (!file) return;
  if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type) || file.size > MAX_SOURCE_BYTES) {
    resetPhoto();
    showError({ key: 'errChoose' });
    return;
  }

  if (previewUrl) URL.revokeObjectURL(previewUrl);
  photoConfirmation.checked = false;
  selectedFile = file;
  previewUrl = URL.createObjectURL(file);
  preview.src = previewUrl;
  preview.alt = t('selectedPhotoAlt', { name: file.name });
  previewWrap.hidden = false;
  uploadEmpty.hidden = true;
  updateAnalyzeButton();
  resultsContent.hidden = true;
  resultsEmpty.hidden = false;
}

function resetPhoto() {
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = null;
  selectedFile = null;
  fileInput.value = '';
  preview.removeAttribute('src');
  previewWrap.hidden = true;
  uploadEmpty.hidden = false;
  photoConfirmation.checked = false;
  resultsContent.hidden = true;
  resultsEmpty.hidden = false;
  updateAnalyzeButton();
}

document.querySelector('#browse').addEventListener('click', event => {
  event.stopPropagation();
  fileInput.click();
});
document.querySelector('#remove-photo').addEventListener('click', event => {
  event.stopPropagation();
  resetPhoto();
});
fileInput.addEventListener('change', () => chooseFile(fileInput.files[0]));
photoConfirmation.addEventListener('change', updateAnalyzeButton);
dropzone.addEventListener('click', event => {
  if (!event.target.closest('button')) fileInput.click();
});
dropzone.addEventListener('dragover', event => {
  event.preventDefault();
  dropzone.classList.add('dragging');
});
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragging'));
dropzone.addEventListener('drop', event => {
  event.preventDefault();
  dropzone.classList.remove('dragging');
  chooseFile(event.dataTransfer.files[0]);
});

analyzeButton.addEventListener('click', async () => {
  if (!selectedFile || !analysisReady || !photoConfirmation.checked) return;
  const analyzingFile = selectedFile;
  analysisInProgress = true;
  updateAnalyzeButton();
  resultsEmpty.hidden = true;
  resultsContent.hidden = true;
  loading.hidden = false;
  const controller = new AbortController();
  let timeout;

  try {
    const prepared = await prepareImage(analyzingFile);
    const imageData = await new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(String(reader.result).split(',')[1]);
      reader.onerror = () => reject(new LocalizedError('errRead'));
      reader.readAsDataURL(prepared.blob);
    });
    timeout = setTimeout(() => controller.abort(), 65_000);
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: { data: imageData, mimeType: prepared.mimeType } }),
      signal: controller.signal,
    });
    // A proxy or crash can return HTML instead of JSON; never show a raw parse error.
    const payload = await response.json().catch(() => null);
    if (selectedFile !== analyzingFile) return;
    if (!response.ok || !payload) {
      throw payload?.error ? new Error(payload.error) : new LocalizedError('errServer', { status: response.status });
    }
    renderResult(payload.result, payload.model);
  } catch (error) {
    if (selectedFile === analyzingFile) {
      let failure;
      if (error instanceof LocalizedError) failure = { key: error.key, vars: error.vars };
      else if (error.name === 'AbortError') failure = { key: 'errTimeout' };
      else if (error instanceof TypeError) failure = { key: 'errNetwork' };
      else failure = error.message ? { text: error.message } : { key: 'errGeneric' };
      showError(failure);
    }
  } finally {
    if (timeout) clearTimeout(timeout);
    loading.hidden = true;
    analysisInProgress = false;
    updateAnalyzeButton();
  }
});

// ---- Interface language -----------------------------------------------------------------

function storedLanguage() {
  try { return localStorage.getItem('labelfit-language'); } catch { return null; }
}

function rememberLanguage(code) {
  try { localStorage.setItem('labelfit-language', code); } catch { /* storage can be unavailable */ }
}

async function fetchJson(url) {
  const response = await fetch(url, { cache: 'no-store' });
  if (!response.ok) throw new Error(url);
  return response.json();
}

function renderDraftBanner() {
  const banner = document.querySelector('#draft-banner');
  banner.replaceChildren();
  banner.hidden = !draftPreview;
  if (!draftPreview) return;
  const english = document.createElement('span');
  english.lang = 'en';
  english.textContent = englishStrings['draftBanner'] || '';
  const translated = document.createElement('span');
  translated.lang = currentLanguage;
  translated.textContent = strings['draftBanner'] || '';
  banner.append(english, ' / ', translated);
}

function applyStrings() {
  document.documentElement.lang = currentLanguage;
  for (const element of document.querySelectorAll('[data-i18n]')) {
    element.textContent = t(element.dataset.i18n);
  }
  for (const attribute of ['aria-label', 'alt', 'title']) {
    for (const element of document.querySelectorAll(`[data-i18n-${attribute}]`)) {
      element.setAttribute(attribute, t(element.getAttribute(`data-i18n-${attribute}`)));
    }
  }
  if (selectedFile) preview.alt = t('selectedPhotoAlt', { name: selectedFile.name });
  renderServiceState();
  renderDraftBanner();
  if (!resultsContent.hidden && lastView) {
    if (lastView.type === 'result') renderResult(lastView.result, lastView.model);
    else showError(lastView.error);
  }
}

function buildLanguagePicker() {
  const picker = document.querySelector('#language-picker');
  const select = document.querySelector('#language-select');
  const codes = I18n.pickerCodes({ available: availableLanguages, previewCode: draftPreview ? currentLanguage : null });
  select.replaceChildren();
  for (const code of codes) {
    const meta = availableLanguages[code];
    const option = document.createElement('option');
    option.value = code;
    option.lang = code;
    option.textContent = meta.reviewed ? meta.nativeName : `${meta.nativeName} (draft)`;
    select.append(option);
  }
  select.value = currentLanguage;
  picker.hidden = codes.length < 2;
}

async function setLanguage(code) {
  try {
    const data = await fetchJson(`/locales/${code}.json`);
    strings = data.strings;
  } catch {
    return;
  }
  currentLanguage = code;
  draftPreview = !I18n.isSelectable(availableLanguages[code]);
  if (!draftPreview) rememberLanguage(code);
  applyStrings();
}

async function initLanguage() {
  try {
    availableLanguages = await fetchJson('/locales/index.json');
    englishStrings = (await fetchJson('/locales/en.json')).strings;
    strings = englishStrings;
    const choice = I18n.pickLanguage({
      requested: new URLSearchParams(window.location.search).get('lang'),
      stored: storedLanguage(),
      available: availableLanguages,
    });
    if (choice.language !== I18n.DEFAULT_LANGUAGE) strings = (await fetchJson(`/locales/${choice.language}.json`)).strings;
    currentLanguage = choice.language;
    draftPreview = choice.preview;
    buildLanguagePicker();
    applyStrings();
  } catch {
    // The page already contains its English text; keep it if the locale files cannot load.
  }
}

document.querySelector('#language-select').addEventListener('change', event => setLanguage(event.target.value));

initLanguage().finally(loadServiceState);
