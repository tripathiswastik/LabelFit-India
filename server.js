const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = __dirname;
const PORT = Number(process.env.PORT || 4173);
const MAX_IMAGE_BYTES = 7 * 1024 * 1024;

const schema = {
  type: 'object',
  properties: {
    productName: { type: 'object', properties: { value: { type: 'string' }, evidence: { type: 'string' }, confidence: { type: 'string', enum: ['clear', 'uncertain', 'not_found'] } }, required: ['value', 'evidence', 'confidence'] },
    ageMarking: { type: 'object', properties: { value: { type: 'string' }, evidence: { type: 'string' }, confidence: { type: 'string', enum: ['clear', 'uncertain', 'not_found'] } }, required: ['value', 'evidence', 'confidence'] },
    ingredients: { type: 'object', properties: { value: { type: 'string' }, evidence: { type: 'string' }, confidence: { type: 'string', enum: ['clear', 'uncertain', 'not_found'] } }, required: ['value', 'evidence', 'confidence'] },
    allergenStatement: { type: 'object', properties: { value: { type: 'string' }, evidence: { type: 'string' }, confidence: { type: 'string', enum: ['clear', 'uncertain', 'not_found'] } }, required: ['value', 'evidence', 'confidence'] },
    nutritionPanel: { type: 'object', properties: { value: { type: 'string' }, evidence: { type: 'string' }, confidence: { type: 'string', enum: ['clear', 'uncertain', 'not_found'] } }, required: ['value', 'evidence', 'confidence'] },
    preparationAndStorage: { type: 'object', properties: { value: { type: 'string' }, evidence: { type: 'string' }, confidence: { type: 'string', enum: ['clear', 'uncertain', 'not_found'] } }, required: ['value', 'evidence', 'confidence'] },
    notes: { type: 'array', items: { type: 'string' } }
  },
  required: ['productName', 'ageMarking', 'ingredients', 'allergenStatement', 'nutritionPanel', 'preparationAndStorage', 'notes']
};

function send(res, status, body, type = 'application/json; charset=utf-8') {
  res.writeHead(status, { 'Content-Type': type, 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' });
  res.end(type.startsWith('application/json') ? JSON.stringify(body) : body);
}

function collect(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
      if (body.length > MAX_IMAGE_BYTES * 1.5) { reject(new Error('Request too large')); req.destroy(); }
    });
    req.on('end', () => resolve(body));
    req.on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  if (req.method === 'GET' && url.pathname === '/api/status') {
    return send(res, 200, { configured: Boolean(process.env.GEMINI_API_KEY), model: 'gemini-3.8-flash' });
  }
  if (req.method === 'POST' && url.pathname === '/api/analyze') {
    if (!process.env.GEMINI_API_KEY) return send(res, 503, { error: 'Gemini is not configured yet. Set GEMINI_API_KEY in your local terminal and restart the app.' });
    try {
      const payload = JSON.parse(await collect(req));
      if (!payload.image || typeof payload.image.data !== 'string' || !/^image\/(jpeg|png|webp)$/.test(payload.image.mimeType || '')) {
        return send(res, 400, { error: 'Choose a JPEG, PNG or WebP image.' });
      }
      const imageBytes = Buffer.from(payload.image.data, 'base64');
      if (!imageBytes.length || imageBytes.length > MAX_IMAGE_BYTES) return send(res, 413, { error: 'Image must be smaller than 7 MB.' });
      const prompt = `Read the visible text from this packaged complementary food label. Extract only what is legible in these fields: product name, age marking, ingredients, allergen statement, nutrition panel, preparation and storage text. For each field provide a concise value, an exact short evidence snippet copied from the image, and confidence: clear, uncertain, or not_found. If a field is missing, use an empty value and empty evidence with confidence not_found. If characters are blurry, preserve uncertainty; do not guess missing text. Do not assess safety, suitability, health effects, allergy risk, or give feeding or medical advice. Do not infer claims from the product image. Add notes only for image/legibility limits. Respond in English, retaining label wording where possible.`;
      const upstream = await fetch('https://generativelanguage.googleapis.com/v1beta/interactions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-goog-api-key': process.env.GEMINI_API_KEY, 'Api-Revision': '2026-05-20' },
        body: JSON.stringify({
          model: 'gemini-3.8-flash', store: false,
          input: [{ type: 'text', text: prompt }, { type: 'image', data: imageBytes.toString('base64'), mime_type: payload.image.mimeType }],
          response_format: { type: 'text', mime_type: 'application/json', schema }
        })
      });
      const response = await upstream.json();
      if (!upstream.ok) return send(res, 502, { error: response.error?.message || 'Gemini could not read this image. Try a clearer photo of one panel.' });
      const output = response.steps?.flatMap(step => step.content || []).find(item => item.type === 'text')?.text;
      if (!output) return send(res, 502, { error: 'Gemini returned no label text. Try another image.' });
      return send(res, 200, { result: JSON.parse(output), model: response.model || 'gemini-3.8-flash' });
    } catch (error) {
      return send(res, error.message === 'Request too large' ? 413 : 400, { error: error.message === 'Request too large' ? 'Image request is too large.' : 'Could not process that image. Please try again.' });
    }
  }
  if (req.method !== 'GET' && req.method !== 'HEAD') return send(res, 405, { error: 'Method not allowed.' });
  let filePath = path.join(ROOT, url.pathname === '/' ? 'index.html' : decodeURIComponent(url.pathname.slice(1)));
  if (!filePath.startsWith(ROOT)) return send(res, 403, { error: 'Forbidden.' });
  try {
    const content = fs.readFileSync(filePath);
    const ext = path.extname(filePath).toLowerCase();
    const mime = ({ '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.svg': 'image/svg+xml' })[ext] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': mime, 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' });
    return res.end(content);
  } catch { return send(res, 404, 'Not found', 'text/plain; charset=utf-8'); }
});

server.listen(PORT, '127.0.0.1', () => console.log(`LabelFit India prototype at http://127.0.0.1:${PORT}`));
