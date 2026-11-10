/**
 * Enquiry form handler.
 *
 * Every enquiry form on the site POSTs here. The submission is formatted
 * into a plain-text email and sent via Resend, then the browser is sent on
 * to /thank-you with a 303 so a refresh can't resubmit it.
 *
 * Required environment variables (Vercel → Settings → Environment Variables):
 *   RESEND_API_KEY   API key from resend.com
 *   ENQUIRY_TO       where enquiries are delivered, e.g. hello@templetonbuilt.com.au
 *                    (comma-separated for several recipients)
 *   ENQUIRY_FROM     verified sender, e.g. "Templeton Built Website <site@templetonbuilt.com.au>"
 *
 * If the send fails the visitor is shown an honest error with the phone
 * number, rather than a thank-you page for an enquiry that went nowhere.
 */

const PHONE = '1800 955 111';
const FALLBACK_EMAIL = 'hello@templetonbuilt.com.au';

// Field order and labels for the email body. Anything not listed here is
// appended afterwards, so a new form field still comes through.
const LABELS = [
  ['first', 'First name'],
  ['last', 'Last name'],
  ['name', 'Name'],
  ['email', 'Email'],
  ['phone', 'Phone'],
  ['suburb', 'Project suburb'],
  ['type', 'Project type'],
  ['project', 'Project type'],
  ['stage', 'Where they are up to'],
  ['budget', 'Budget'],
  ['message', 'Message'],
];

const SKIP = new Set(['_form', '_hp', '_next', 's']);

const DEFAULT_NEXT = '/thank-you';

/**
 * Where to send the browser after a successful submission.
 *
 * Only a path on this site is allowed — anything with a scheme, a host, or a
 * backslash is discarded. Letting a form post an arbitrary destination here
 * would turn the endpoint into an open redirect.
 */
function nextPath(value) {
  if (typeof value !== 'string') return DEFAULT_NEXT;
  const path = value.trim();
  if (!path.startsWith('/') || path.startsWith('//')) return DEFAULT_NEXT;
  if (/[\\:]|[\x00-\x1f]/.test(path)) return DEFAULT_NEXT;
  return path;
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', (chunk) => {
      raw += chunk;
      if (raw.length > 100_000) reject(new Error('Body too large'));
    });
    req.on('end', () => resolve(raw));
    req.on('error', reject);
  });
}

function parse(raw, contentType = '') {
  if (contentType.includes('application/json')) {
    try { return JSON.parse(raw); } catch { return {}; }
  }
  const out = {};
  for (const [k, v] of new URLSearchParams(raw)) out[k] = v;
  return out;
}

function errorPage(res, status, heading, detail) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.end(`<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Something went wrong</title>
<style>
  :root{color-scheme:light}
  body{margin:0;min-height:100vh;display:grid;place-items:center;background:#FBFAF8;color:#16232B;
       font:400 17px/1.6 Georgia,'Times New Roman',serif;padding:24px}
  .b{max-width:30rem}
  h1{font:600 clamp(1.6rem,4vw,2.2rem)/1.15 'Helvetica Neue',Arial,sans-serif;margin:0 0 14px}
  p{margin:0 0 14px;color:#33474F}
  a{color:#16232B}
</style></head><body><div class="b">
<h1>${heading}</h1>
<p>${detail}</p>
<p>Please call <a href="tel:${PHONE.replace(/\s/g, '')}">${PHONE}</a> or email
<a href="mailto:${FALLBACK_EMAIL}">${FALLBACK_EMAIL}</a> and we'll pick it up straight away.</p>
<p><a href="/">Back to the site</a></p>
</div></body></html>`);
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    res.statusCode = 405;
    return res.end('Method Not Allowed');
  }

  let data;
  try {
    data = parse(await readBody(req), req.headers['content-type'] || '');
  } catch {
    return errorPage(res, 400, "We couldn't read that.", 'The form submission was malformed.');
  }

  // Honeypot: real people leave this hidden field empty. Bots fill it.
  // Return the thank-you page so the bot sees success and doesn't retry.
  if (data._hp) {
    res.statusCode = 303;
    res.setHeader('Location', nextPath(data._next));
    return res.end();
  }

  const email = (data.email || '').trim();
  if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return errorPage(res, 400, 'That email address looks wrong.',
      'We need a valid email address so we can reply to you.');
  }

  const { RESEND_API_KEY, ENQUIRY_TO, ENQUIRY_FROM } = process.env;
  if (!RESEND_API_KEY || !ENQUIRY_TO || !ENQUIRY_FROM) {
    console.error('Enquiry not sent: missing env vars', {
      hasKey: !!RESEND_API_KEY, hasTo: !!ENQUIRY_TO, hasFrom: !!ENQUIRY_FROM,
    });
    return errorPage(res, 500, "Your enquiry didn't send.",
      'Something is misconfigured on our side, and we would rather tell you than pretend it arrived.');
  }

  // Build the email body: known fields in order, then anything else.
  const used = new Set();
  const lines = [];
  for (const [key, label] of LABELS) {
    if (used.has(key)) continue;
    const value = (data[key] || '').trim();
    if (value) { lines.push(`${label}: ${value}`); used.add(key); }
  }
  for (const [key, value] of Object.entries(data)) {
    if (used.has(key) || SKIP.has(key) || !String(value).trim()) continue;
    lines.push(`${key}: ${String(value).trim()}`);
  }

  const who = [data.first, data.last].filter(Boolean).join(' ') || data.name || email;
  const source = data._form || 'website';
  const submitted = new Date().toLocaleString('en-AU', {
    timeZone: 'Australia/Adelaide', dateStyle: 'full', timeStyle: 'short',
  });

  const text = [
    'New Website Enquiry',
    '',
    ...lines,
    '',
    '—',
    `Form: ${source}`,
    `Submitted: ${submitted} (Adelaide)`,
  ].join('\n');

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: ENQUIRY_FROM,
        to: ENQUIRY_TO.split(',').map((s) => s.trim()).filter(Boolean),
        reply_to: email,
        subject: `New Website Enquiry — ${who}`,
        text,
      }),
    });

    if (!r.ok) {
      console.error('Resend rejected the enquiry', r.status, await r.text());
      return errorPage(res, 502, "Your enquiry didn't send.",
        'Our mail service refused it. Nothing was lost on your end.');
    }
  } catch (err) {
    console.error('Enquiry send failed', err);
    return errorPage(res, 502, "Your enquiry didn't send.",
      "We couldn't reach our mail service just then.");
  }

  res.statusCode = 303;
  res.setHeader('Location', nextPath(data._next));
  return res.end();
};
