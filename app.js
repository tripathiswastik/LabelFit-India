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

const MAX_IMAGE_BYTES = 7 * 1024 * 1024;
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
    row.append(top, value);

    if (data.evidence) {
      const evidence = document.createElement('div');
      evidence.className = 'field-evidence';
      const evidenceLabel = document.createElement('b');
      evidenceLabel.textContent = 'Model-provided snippet: ';
      evidence.append(evidenceLabel, document.createTextNode(data.evidence));
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

function chooseFile(file) {
  if (!file) return;
  if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type) || file.size > MAX_IMAGE_BYTES) {
    showError('Choose a JPG, PNG or WebP label photo smaller than 7 MB.');
    return;
  }

  if (previewUrl) URL.revokeObjectURL(previewUrl);
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
  analysisInProgress = true;
  updateAnalyzeButton();
  resultsEmpty.hidden = true;
  resultsContent.hidden = true;
  loading.hidden = false;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 65_000);

  try {
    const imageData = await new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(String(reader.result).split(',')[1]);
      reader.onerror = () => reject(new Error('Could not read that file. Choose the photo again.'));
      reader.readAsDataURL(selectedFile);
    });
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: { data: imageData, mimeType: selectedFile.type } }),
      signal: controller.signal,
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || 'Could not read this photo.');
    renderResult(payload.result, payload.model);
  } catch (error) {
    showError(error.name === 'AbortError' ? 'This scan timed out. Try a smaller, clearer photo.' : (error.message || 'Could not process this photo.'));
  } finally {
    clearTimeout(timeout);
    loading.hidden = true;
    analysisInProgress = false;
    updateAnalyzeButton();
  }
});

loadServiceState();
