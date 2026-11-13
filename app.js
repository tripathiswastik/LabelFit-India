const fileInput = document.querySelector('#file-input');
const dropzone = document.querySelector('#dropzone');
const preview = document.querySelector('#preview');
const previewWrap = document.querySelector('#preview-wrap');
const uploadEmpty = document.querySelector('#upload-empty');
const analyzeButton = document.querySelector('#analyze');
const apiState = document.querySelector('#api-state');
const apiStateText = document.querySelector('#api-state-text');
const resultsEmpty = document.querySelector('#results-empty');
const resultsContent = document.querySelector('#results-content');
const loading = document.querySelector('#loading');
let selectedFile = null;

fetch('/api/status').then(response => response.json()).then(status => {
  apiState.classList.toggle('ready', status.configured);
  apiState.classList.toggle('error', !status.configured);
  apiStateText.textContent = status.configured ? `Gemini connected · ${status.model}` : 'Gemini key not set · configure GEMINI_API_KEY to analyze';
}).catch(() => { apiState.classList.add('error'); apiStateText.textContent = 'Local server unavailable · run npm start'; });

function chooseFile(file) {
  if (!file) return;
  if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type) || file.size > 7 * 1024 * 1024) {
    showError('Choose a JPG, PNG or WebP image smaller than 7 MB.'); return;
  }
  selectedFile = file;
  preview.src = URL.createObjectURL(file);
  previewWrap.hidden = false;
  uploadEmpty.hidden = true;
  analyzeButton.disabled = false;
}

function resetPhoto() {
  selectedFile = null; fileInput.value = ''; preview.removeAttribute('src');
  previewWrap.hidden = true; uploadEmpty.hidden = false; analyzeButton.disabled = true;
}

function showError(message) {
  resultsEmpty.hidden = true; resultsContent.hidden = false; loading.hidden = true;
  resultsContent.innerHTML = `<div class="result-header"><div><p class="eyebrow">COULDN’T READ THE LABEL</p><h3>Let’s try once more</h3></div></div><p class="field-value"></p>`;
  resultsContent.querySelector('.field-value').textContent = message;
}

function renderResult(result, model) {
  const fields = [
    ['Product name', result.productName], ['Age marking', result.ageMarking], ['Ingredients', result.ingredients],
    ['Allergen statement', result.allergenStatement], ['Nutrition panel', result.nutritionPanel], ['Preparation & storage', result.preparationAndStorage]
  ];
  resultsContent.replaceChildren();
  const header = document.createElement('div'); header.className = 'result-header';
  const heading = document.createElement('div'); heading.innerHTML = '<p class="eyebrow">VISIBLE LABEL DETAILS</p><h3>Review what we found</h3>';
  const badge = document.createElement('span'); badge.className = 'model-tag'; badge.textContent = model || 'Gemini';
  header.append(heading, badge); resultsContent.append(header);
  for (const [label, data = {}] of fields) {
    const row = document.createElement('div'); row.className = 'field-row';
    const top = document.createElement('div'); top.className = 'field-top';
    const name = document.createElement('span'); name.className = 'field-name'; name.textContent = label;
    const confidence = document.createElement('span'); confidence.className = `confidence ${['clear', 'uncertain', 'not_found'].includes(data.confidence) ? data.confidence : 'uncertain'}`;
    confidence.textContent = data.confidence === 'not_found' ? 'Not visible' : data.confidence === 'clear' ? 'Clear read' : 'Check text';
    const value = document.createElement('div'); value.className = 'field-value'; value.textContent = data.value || 'No text found in the photo.';
    top.append(name, confidence); row.append(top, value);
    if (data.evidence) { const evidence = document.createElement('div'); evidence.className = 'field-evidence'; evidence.innerHTML = '<b>Photo evidence:</b> '; evidence.append(document.createTextNode(data.evidence)); row.append(evidence); }
    resultsContent.append(row);
  }
  if (Array.isArray(result.notes) && result.notes.length) {
    const notes = document.createElement('div'); notes.className = 'note-list'; notes.textContent = `Image notes: ${result.notes.join(' · ')}`; resultsContent.append(notes);
  }
  const reminder = document.createElement('div'); reminder.className = 'note-list'; reminder.textContent = 'Compare this readout with the package. Small, curved, or blurry print can be misread.'; resultsContent.append(reminder);
  resultsContent.hidden = false; resultsEmpty.hidden = true;
}

document.querySelector('#browse').addEventListener('click', event => { event.stopPropagation(); fileInput.click(); });
document.querySelector('#remove-photo').addEventListener('click', event => { event.stopPropagation(); resetPhoto(); });
fileInput.addEventListener('change', () => chooseFile(fileInput.files[0]));
dropzone.addEventListener('click', event => { if (!event.target.closest('button')) fileInput.click(); });
dropzone.addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); fileInput.click(); } });
dropzone.addEventListener('dragover', event => { event.preventDefault(); dropzone.classList.add('dragging'); });
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragging'));
dropzone.addEventListener('drop', event => { event.preventDefault(); dropzone.classList.remove('dragging'); chooseFile(event.dataTransfer.files[0]); });
analyzeButton.addEventListener('click', async () => {
  if (!selectedFile) return;
  analyzeButton.disabled = true; resultsEmpty.hidden = true; resultsContent.hidden = true; loading.hidden = false;
  try {
    const data = await new Promise((resolve, reject) => { const reader = new FileReader(); reader.onload = () => resolve(reader.result.split(',')[1]); reader.onerror = reject; reader.readAsDataURL(selectedFile); });
    const response = await fetch('/api/analyze', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ image: { data, mimeType: selectedFile.type } }) });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || 'Could not read this image.');
    renderResult(payload.result, payload.model);
  } catch (error) { showError(error.message || 'Could not process that image.'); }
  finally { loading.hidden = true; analyzeButton.disabled = !selectedFile; }
});
