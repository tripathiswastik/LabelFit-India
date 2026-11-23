const test = require('node:test');
const assert = require('node:assert/strict');
const net = require('node:net');
const fs = require('node:fs');
const path = require('node:path');
const {
  createRateLimiter,
  createServer,
  getClientKey,
  checkAccessToken,
  resolveTrustProxyHops,
  securityHeaders,
} = require('../server.js');

const PNG = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10, 1, 2, 3]);
const GOOD_BODY = JSON.stringify({ image: { data: PNG.toString('base64'), mimeType: 'image/png' } });

function mockGemini() {
  const field = { value: 'x', evidence: 'x', readStatus: 'clear' };
  const output = JSON.stringify(Object.fromEntries(
    ['productName', 'ageMarking', 'ingredients', 'allergenDeclaration', 'nutritionPanel', 'preparationAndStorage'].map(name => [name, field])
  ));
  return async () => ({
    ok: true,
    json: async () => ({ model: 'mock', steps: [{ type: 'model_output', content: [{ type: 'text', text: output }] }] }),
  });
}

async function start(options = {}) {
  const server = createServer({ apiKey: 'mock-key', analysisEnabled: true, fetchImpl: mockGemini(), rateLimit: 1000, ...options });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  return { server, port: server.address().port };
}

// Opens a raw connection that promises a large body and then never finishes sending it.
function stallUpload(port) {
  const socket = net.connect(port, '127.0.0.1');
  socket.on('error', () => {});
  socket.write(`POST /api/analyze HTTP/1.1\r\nHost: 127.0.0.1:${port}\r\nContent-Type: application/json\r\nContent-Length: 100000\r\n\r\n{"image":`);
  return socket;
}

const post = (port, headers = {}) => fetch(`http://127.0.0.1:${port}/api/analyze`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', ...headers },
  body: GOOD_BODY,
});

test('stalled uploads do not consume analysis slots', async () => {
  const { server, port } = await start({ bodyTimeoutMs: 5000 });
  const stalled = [stallUpload(port), stallUpload(port), stallUpload(port)]; // more than the 2 analysis slots
  try {
    await new Promise(resolve => setTimeout(resolve, 100));
    const res = await post(port);
    assert.equal(res.status, 200);
  } finally {
    stalled.forEach(socket => socket.destroy());
    server.close();
  }
});

test('a stalled upload is cut off after the body timeout', async () => {
  const { server, port } = await start({ bodyTimeoutMs: 150 });
  const socket = stallUpload(port);
  try {
    const started = Date.now();
    await new Promise(resolve => socket.on('close', resolve));
    assert.ok(Date.now() - started < 3000, 'connection should be closed shortly after the timeout');
    const res = await post(port);
    assert.equal(res.status, 200, 'server keeps working after a timed-out upload');
  } finally {
    socket.destroy();
    server.close();
  }
});

test('too many simultaneous uploads are refused with 429', async () => {
  const { server, port } = await start({ bodyTimeoutMs: 5000 });
  const stalled = Array.from({ length: 8 }, () => stallUpload(port));
  try {
    await new Promise(resolve => setTimeout(resolve, 150));
    const res = await post(port);
    assert.equal(res.status, 429);
  } finally {
    stalled.forEach(socket => socket.destroy());
    server.close();
  }
});

test('rate limiter forgets expired clients instead of growing forever', () => {
  let now = 0;
  const allow = createRateLimiter({ limit: 5, intervalMs: 1000, now: () => now });
  for (let i = 0; i < 200; i += 1) allow(`client-${i}`);
  assert.equal(allow.size(), 200);
  now += 1500;
  allow('fresh-client');
  assert.equal(allow.size(), 1, 'expired keys are removed');
});

test('rate limiter refuses new keys when full of live keys but still serves known ones', () => {
  const now = 0;
  const allow = createRateLimiter({ limit: 5, intervalMs: 1000, now: () => now, maxKeys: 3 });
  assert.equal(allow('a'), true);
  assert.equal(allow('b'), true);
  assert.equal(allow('c'), true);
  assert.equal(allow('d'), false);
  assert.equal(allow('a'), true);
});

test('client key ignores X-Forwarded-For unless a proxy is trusted', () => {
  const req = { socket: { remoteAddress: '10.0.0.1' }, headers: { 'x-forwarded-for': '1.2.3.4' } };
  assert.equal(getClientKey(req, 0), '10.0.0.1');
});

test('behind one trusted proxy the client is the last forwarded entry, so spoofed prefixes do not help', () => {
  const real = { socket: { remoteAddress: '10.0.0.1' }, headers: { 'x-forwarded-for': '9.9.9.9, 203.0.113.7' } };
  assert.equal(getClientKey(real, 1), '203.0.113.7');
  const empty = { socket: { remoteAddress: '10.0.0.1' }, headers: {} };
  assert.equal(getClientKey(empty, 1), '10.0.0.1');
  const twoHops = { socket: { remoteAddress: '10.0.0.1' }, headers: { 'x-forwarded-for': '203.0.113.7, 35.1.1.1' } };
  assert.equal(getClientKey(twoHops, 2), '203.0.113.7');
});

test('trusted proxy hops default to 1 on Cloud Run, 0 locally, and reject junk', () => {
  assert.equal(resolveTrustProxyHops({}, true), 1);
  assert.equal(resolveTrustProxyHops({}, false), 0);
  assert.equal(resolveTrustProxyHops({ LABELFIT_TRUST_PROXY_HOPS: '2' }, false), 2);
  assert.equal(resolveTrustProxyHops({ LABELFIT_TRUST_PROXY_HOPS: 'lots' }, true), 0);
  assert.equal(resolveTrustProxyHops({ LABELFIT_TRUST_PROXY_HOPS: '99' }, true), 0);
});

test('access token is enforced when configured and unused otherwise', async () => {
  const mockToken = 'mock-auth-token-hardening-test';
  assert.equal(checkAccessToken({ headers: {} }, ''), true);
  assert.equal(checkAccessToken({ headers: { 'x-labelfit-token': 'nope' } }, mockToken), false);
  assert.equal(checkAccessToken({ headers: { 'x-labelfit-token': mockToken } }, mockToken), true);

  const { server, port } = await start({ accessToken: mockToken });
  try {
    assert.equal((await post(port)).status, 401);
    assert.equal((await post(port, { 'X-LabelFit-Token': 'wrong' })).status, 401);
    assert.equal((await post(port, { 'X-LabelFit-Token': mockToken })).status, 200);
  } finally {
    server.close();
  }
});

test('favicon and static responses carry the same security headers', async () => {
  const { server, port } = await start();
  try {
    for (const route of ['/favicon.ico', '/', '/app.js']) {
      const res = await fetch(`http://127.0.0.1:${port}${route}`);
      assert.equal(res.headers.get('x-content-type-options'), 'nosniff', route);
      assert.equal(res.headers.get('x-frame-options'), 'DENY', route);
      assert.ok(res.headers.get('content-security-policy').includes("default-src 'self'"), route);
    }
    assert.equal(securityHeaders('text/plain')['Referrer-Policy'], 'no-referrer');
  } finally {
    server.close();
  }
});

test('API key lookup never reads parent-directory env files', () => {
  const source = fs.readFileSync(path.join(__dirname, '..', 'server.js'), 'utf8');
  assert.ok(!source.includes("'..', '.env'"));
  assert.ok(!source.includes('.omniroute-data'));
});
