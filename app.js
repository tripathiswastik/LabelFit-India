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

const MAX_IMAGE_BYTES = 7 * 1024 * 1024; // what the server accepts (after resizing)
const MAX_SOURCE_BYTES = 30 * 1024 * 1024; // what we will try to resize in the browser
const MAX_EDGE_PX = 2560; // long edge after resizing; small print needs resolution
const JPEG_QUALITIES = [0.9, 0.82, 0.74, 0.66];
let selectedFile = null;
let previewUrl = null;
let analysisReady = false;
let analysisInProgress = false;

function updateAnalyzeButton() {
  analyzeButton.disabled = !selectedFile || !analysisReady || !photoConfirmation.checked || analysisInProgress;
}

function setServiceState(configured, model, message) {
  analysisReady = configured;
  apiState.classList.toggle('ready', configured);
  apiState.classList.toggle('error', !configured);
  apiStateText.textContent = message || (configured ? `Gemini ready · ${model}` : 'Gemini is not configured on this server yet.');
  updateAnalyzeButton();
}

async function loadServiceState() {
  try {
    const response = await fetch('/api/status', { cache: 'no-store' });
    if (!response.ok) throw new Error('status');
    const status = await response.json();
    setServiceState(Boolean(status.configured), status.model, status.configured ? '' : 'Gemini is not configured on this server yet.');
  } catch {
    setServiceState(false, '', 'LabelFit server is unavailable. Start it with npm start.');
  }
}

function showError(message) {
  resultsEmpty.hidden = true;
  resultsContent.replaceChildren();
  const header = document.createElement('div');
  header.className = 'result-header';
  const heading = document.createElement('div');
  const eyebrow = document.createElement('p');
  eyebrow.className = 'eyebrow';
  eyebrow.textContent = 'LABEL NOT READ';
  const title = document.createElement('h3');
  title.textContent = 'Let’s try once more';
  heading.append(eyebrow, title);
  header.append(heading);
  const errorText = document.createElement('p');
  errorText.className = 'field-value';
  errorText.textContent = message;
  resultsContent.append(header, errorText);
  resultsContent.hidden = false;
  loading.hidden = true;
}

// Tags results written in an Indian script so screen readers pick the right voice.
// One language per script; Devanagari is also used for Marathi and Nepali, and Bengali for
// Assamese, so this is a best guess for the common case. Mixed text is tagged only when the
// Indian script has more letters than Latin; otherwise it is left untagged (page language).
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
  return best && bestCount > latin ? best : null;
}

function renderResult(result, model) {
  const fields = [
    ['Product name', result.productName],
    ['Age marking', result.ageMarking],
    ['Ingredients', result.ingredients],
    ['Allergen declaration', result.allergenDeclaration],
    ['Nutrition panel', result.nutritionPanel],
    ['Preparation & storage', result.preparationAndStorage],
  ];

  resultsContent.replaceChildren();
  const header = document.createElement('div');
  header.className = 'result-header';
  const heading = document.createElement('div');
  const eyebrow = document.createElement('p');
  eyebrow.className = 'eyebrow';
  eyebrow.textContent = 'LABEL PHOTO READOUT';
  const title = document.createElement('h3');
  title.textContent = 'Review the printed details';
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
    status.textContent = readStatus === 'not_visible' ? 'Not visible' : readStatus === 'clear' ? 'Readable' : 'Check text';
    top.append(name, status);

    const value = document.createElement('div');
    value.className = 'field-value';
    value.textContent = data.value || 'No text found in the photo.';
    const valueLanguage = languageOf(data.value);
    if (valueLanguage) value.lang = valueLanguage;
    row.append(top, value);

    if (data.evidence) {
      const evidence = document.createElement('div');
      evidence.className = 'field-evidence';
      const evidenceLabel = document.createElement('b');
      evidenceLabel.textContent = 'Model-provided snippet: ';
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
  reminder.textContent = 'Compare the readout with the package. The status is a model read, not an accuracy score.';
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
    img.onerror = () => { URL.revokeObjectURL(url); reject(new Error('Could not read that photo. Try a JPG, PNG or WebP image.')); };
    img.src = url;
  });
}

function canvasToBlob(canvas, type, quality) {
  return new Promise(resolve => canvas.toBlob(resolve, type, quality));
}

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
  throw new Error('This photo is still too large after resizing. Try a closer photo of one label panel.');
}

function chooseFile(file) {
  if (!file) return;
  if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type) || file.size > MAX_SOURCE_BYTES) {
    resetPhoto();
    showError('Choose a JPG, PNG or WebP label photo under 30 MB. Large photos are resized automatically.');
    return;
  }

  if (previewUrl) URL.revokeObjectURL(previewUrl);
  photoConfirmation.checked = false;
  selectedFile = file;
  previewUrl = URL.createObjectURL(file);
  preview.src = previewUrl;
  preview.alt = `Selected label photo: ${file.name}`;
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
dropzone.addEventListener('keydown', event => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    fileInput.click();
  }
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
  const timeout = setTimeout(() => controller.abort(), 65_000);

  try {
    const prepared = await prepareImage(analyzingFile);
    const imageData = await new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(String(reader.result).split(',')[1]);
      reader.onerror = () => reject(new Error('Could not read that file. Choose the photo again.'));
      reader.readAsDataURL(prepared.blob);
    });
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
      throw new Error(payload?.error || `The LabelFit server could not read this photo (error ${response.status}). Please try again.`);
    }
    renderResult(payload.result, payload.model);
  } catch (error) {
    if (selectedFile === analyzingFile) {
      const message = error.name === 'AbortError'
        ? 'This scan timed out. Try a smaller, clearer photo.'
        : error instanceof TypeError
          ? 'Could not reach the LabelFit server. Check that it is running and try again.'
          : (error.message || 'Could not process this photo.');
      showError(message);
    }
  } finally {
    clearTimeout(timeout);
    loading.hidden = true;
    analysisInProgress = false;
    updateAnalyzeButton();
  }
});

loadServiceState();
