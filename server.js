/* Session House — demo-host server (websites lane, t_737649d7, 2026-11-22).
   Same shape as copa-cafe/tavern-at-west-bend server.js: static + JSON-LD pages,
   /open?t=<slug>-<touch#> funnel pixel (1px gif, no-cache, host-scoped lane.db log),
   POST /contact relayed to the lane mailbox via Brevo v3 HTTP API over 443
   (SMTP egress is dead on Railway — tavern-at-west-bend DEPLOY.md). */
'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const PUBLIC = path.join(__dirname, 'public');
const PORT = process.env.PORT || 8080;
const LANE_INBOX = 'jarvis@onsmalltalk.com';
const SITE = 'Session House';
const LOG_DIR = process.env.LOG_DIR || '/tmp/logs';

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.gif': 'image/gif',
  '.ico': 'image/x-icon',
};

let logStream = null;
try {
  fs.mkdirSync(LOG_DIR, { recursive: true });
  logStream = fs.createWriteStream(path.join(LOG_DIR, 'form-log.txt'), { flags: 'a' });
} catch (e) { console.error('LOGDIR ' + e.message); }
function audit(line) {
  const entry = JSON.stringify({ ts: new Date().toISOString(), line });
  try { fs.appendFileSync('/tmp/form-fallback.txt', entry + '\n'); } catch (e) {}
  if (logStream) { try { logStream.write(entry + '\n'); } catch (e) {} }
}

const FAVICON = fs.readFileSync(path.join(PUBLIC, 'favicon.svg'));
const PIXEL = fs.readFileSync(path.join(PUBLIC, 'pixel.gif'));

function escapeHtml(s) {
  return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

function serve(res, code, body, ctype) {
  res.writeHead(code, { 'Content-Type': ctype, 'X-Robots-Tag': 'noindex, nofollow' });
  res.end(body);
}

const server = http.createServer((req, res) => {
  let u;
  try { u = new URL(req.url, 'http://localhost'); } catch (e) { return serve(res, 400, 'bad request', 'text/plain'); }
  const p = u.pathname;

  if (p === '/healthz') return serve(res, 200, 'ok', 'text/plain');

  if (p === '/robots.txt') return serve(res, 200, 'User-agent: *\nDisallow: /thanks\nDisallow: /404\n\nSitemap: https://session-house-boston-demo.up.railway.app/sitemap.xml\n', 'text/plain; charset=utf-8');

  if (req.method === 'GET' && p === '/favicon.svg') {
    res.writeHead(200, { 'Content-Type': 'image/svg+xml', 'Cache-Control': 'public, max-age=86400', 'X-Robots-Tag': 'noindex, nofollow' });
    return res.end(FAVICON);
  }

  // funnel pixel: 1x1 gif; ?t=<slug>-<touch#> token from the pitch links.
  // host is already unique per shop (session-house-boston-demo) = shop id;
  // t = which touch/pixel of that shop's mail; ip last-octet salted for dedupe.
  if (req.method === 'GET' && p === '/open') {
    const t = (u.searchParams.get('t') || 'pitch').replace(/[^a-z0-9\-]/gi, '').slice(0, 64);
    const fwd = (req.headers['x-forwarded-for'] || '').split(',')[0].trim();
    const ipRe = /\d{1,3}\.\d{1,3}\.\d{1,3}\.(\d{1,3})/;
    const m = ipRe.exec(fwd) || ipRe.exec(req.socket.remoteAddress || '');
    const salt = m ? '_' + m[1] : '';
    try { fs.appendFileSync(path.join(LOG_DIR, 'open-log.txt'), JSON.stringify({ ts: new Date().toISOString(), t: t + salt }) + '\n'); } catch (e) {}
    res.writeHead(200, {
      'Content-Type': 'image/gif',
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Content-Length': PIXEL.length,
      'X-Robots-Tag': 'noindex, nofollow',
    });
    return res.end(PIXEL);
  }

  if (req.method === 'POST' && p === '/contact') {
    let body = '', done = false;
    req.on('data', c => { if (body.length < 64 * 1024) body += c; });
    req.on('end', () => {
      if (done) return; done = true;
      const f = {};
      new URLSearchParams(body).forEach((v, k) => { f[k] = v.slice(0, 4000); });
      const name = (f.name || 'someone').trim() || 'someone';
      const phone = (f.phone || '').trim();
      const email = (f.email || '').trim();
      const msg = (f.message || '').trim();
      if (!msg && !phone) {
        res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
        return res.end('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Missing message</title></head><body><h1>Please leave a message or phone number</h1><p><a href="/contact">Back to the form</a></p></body></html>');
      }
      const key = process.env.BREVO_API_KEY;
      const subject = `${SITE} pub note: ${name}${phone ? ' — ' + phone : ''}`;
      const text = `New pub note from the site:\n\nName: ${name}\nPhone: ${phone || '-'}\nEmail: ${email || '-'}\n\n${msg || '(no message body)'}\n`;
      const html = `<h2>New pub note from the site</h2><p><b>Name:</b> ${escapeHtml(name)}<br><b>Phone:</b> ${escapeHtml(phone || '-')}<br><b>Email:</b> ${escapeHtml(email || '-')}</p><p>${escapeHtml(msg || '(no message body)').replace(/\n/g, '<br>')}</p>`;
      audit({ name, phone, email, message: msg });
      const deliver = () => {
        res.writeHead(303, { Location: '/thanks' });
        res.end();
      };
      const fail = (err) => {
        console.error('MAILERR ' + err);
        res.writeHead(502, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Try again</title></head><body><h1>We could not send that right now</h1><p>Please try again in a moment, or call the pub.</p><p><a href="/contact">Back to the form</a></p></body></html>');
      };
      if (!key) return fail('BREVO_API_KEY not set');
      fetch('https://api.brevo.com/v3/smtp/email', {
        method: 'POST',
        headers: { 'api-key': key, 'content-type': 'application/json', 'accept': 'application/json' },
        body: JSON.stringify({
          sender: { name: SITE + ' pub site', email: LANE_INBOX },
          to: [{ email: LANE_INBOX }],
          replyTo: /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) ? { email, name } : undefined,
          subject,
          textContent: text,
          htmlContent: html,
        }),
      }).then(r => {
        if (r.ok) { deliver(); }
        else { r.text().then(t => fail('brevo ' + r.status + ' ' + t.slice(0, 200))); }
      }).catch(e => fail(e && e.message ? e.message : String(e)));
    });
    return;
  }

  if (req.method !== 'GET' && req.method !== 'HEAD') return serve(res, 405, 'method not allowed', 'text/plain');

  let file = p === '/' ? '/index.html' : p;
  if (!/\.[a-z0-9]+$/i.test(file)) file += '.html';
  let code = 200, target;
  try {
    target = path.join(PUBLIC, path.normalize(file));
    if (!target.startsWith(PUBLIC)) throw new Error('esc');
    fs.statSync(target);
  } catch (e) {
    target = path.join(PUBLIC, '404.html');
    code = 404;
  }
  const ext = path.extname(target).toLowerCase();
  fs.readFile(target, (err, data) => {
    if (err) return serve(res, 500, 'read error', 'text/plain');
    serve(res, code, data, MIME[ext] || 'application/octet-stream');
  });
});

server.listen(PORT, () => console.log('listening on ' + PORT));
