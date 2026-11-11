/**
 * Enquiry form handler.
 *
 * Every enquiry form on the site POSTs here. The submission is formatted
 * into a plain-text email and sent via Resend, recorded in the enquiry log
 * (see _log.js), then the browser is sent on to /thank-you with a 303 so a
 * refresh can't resubmit it.
 *
 * Required environment variables (Vercel → Settings → Environment Variables):
 *   RESEND_API_KEY   API key from resend.com
 *   ENQUIRY_TO       where enquiries are delivered, e.g. info@templetonbuilt.com.au
 *                    (comma-separated for several recipients)
 *   ENQUIRY_FROM     verified sender, e.g. "Templeton Built Website <site@templetonbuilt.com.au>"
 *
 * Optional:
 *   FORM_TOKEN_SECRET  signs the token each form carries — see _spam.js.
 *                      While unset, token checking is skipped.
 *   ENQUIRY_ROUTES   JSON, to send particular forms somewhere other than
 *                    ENQUIRY_TO — see routeFor() below
 *   NOTION_TOKEN     } the enquiry log. Without them the email still sends
 *   NOTION_DB_ID     } and the enquiry is written to the function log.
 *
 * If the send fails the visitor is shown an honest error with the phone
 * number, rather than a thank-you page for an enquiry that went nowhere.
 * A logging failure is not shown — the enquiry has been delivered, and the
 * visitor has nothing to do about our bookkeeping.
 */

const { logEnquiry } = require('./_log.js');
const { tokenProblem, spamReasons } = require('./_spam.js');

const PHONE = '1800 955 111';
const FALLBACK_EMAIL = 'info@templetonbuilt.com.au';

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
  ['day', 'Preferred day'],
  ['time', 'Preferred time'],
  ['guests', 'How many coming'],
  ['rooms', 'Rooms or areas'],
  ['package', 'Package of interest'],
  ['timing', 'Timing'],
  ['budget', 'Budget'],
  ['message', 'Message'],
];

const SKIP = new Set(['_form', '_hp', '_next', '_t', 's']);

/**
 * Per-form delivery, for forms that shouldn't land in the general inbox.
 *
 * ENQUIRY_ROUTES is JSON keyed by a form's _form value:
 *   {"Hills Open Day": {"to": "jordan@…", "cc": "indy@…"}}
 *
 * "to" and "cc" each take one address or a comma-separated list. Addresses
 * live in the environment rather than the repo, and anything not listed
 * here goes to ENQUIRY_TO as before. Bad JSON is logged and ignored rather
 * than thrown — a typo in a config value must not stop enquiries arriving.
 */
function routeFor(form) {
  const raw = process.env.ENQUIRY_ROUTES;
  if (!raw) return {};
  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch {
    console.error('ENQUIRY_ROUTES is not valid JSON; using ENQUIRY_TO for every form');
    return {};
  }
  if (!parsed || typeof parsed !== 'object') return {};
  const route = parsed[form];
  return route && typeof route === 'object' ? route : {};
}

/** One address, a comma-separated list, or an array — always an array. */
function addresses(value) {
  const list = Array.isArray(value) ? value : String(value ?? '').split(',');
  return list.map((s) => String(s).trim()).filter(Boolean);
}

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
  // Checkbox groups repeat the same name, so collect repeats rather than
  // letting the last one win.
  const out = {};
  for (const [k, v] of new URLSearchParams(raw)) {
    if (k in out) out[k] = [].concat(out[k], v);
    else out[k] = v;
  }
  return out;
}

/** One value or a checkbox group, as a single readable string. */
function flatten(value) {
  if (Array.isArray(value)) return value.map((v) => String(v).trim()).filter(Boolean).join(', ');
  return value === undefined || value === null ? '' : String(value).trim();
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

  // The page mints a signed token on load and carries it in a hidden field.
  // No token means the submission never rendered the page — which is how
  // every piece of spam this form receives arrives. Unlike the content
  // rules below this is answered honestly rather than silently, because a
  // missing token can also mean JavaScript didn't run, and a real person
  // deserves to know their enquiry didn't go through.
  const badToken = tokenProblem(data._t);
  if (badToken) {
    console.log('enquiry rejected: token', JSON.stringify({
      reason: badToken, form: data._form || 'website', email: (data.email || '').trim(),
    }));
    return errorPage(res, 400, "We couldn't send that.",
      'Your browser session could not be verified. If you have JavaScript turned off, '
      + 'that will be why — reload the page and try again, or just call us.');
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

  // One flattened value per submitted field, shared by the email and the log.
  const fields = {};
  for (const [key, value] of Object.entries(data)) {
    if (SKIP.has(key)) continue;
    const text = flatten(value);
    if (text) fields[key] = text;
  }

  // Build the email body: known fields in order, then anything else.
  const used = new Set();
  const lines = [];
  for (const [key, label] of LABELS) {
    if (used.has(key) || !fields[key]) continue;
    lines.push(`${label}: ${fields[key]}`);
    used.add(key);
  }
  for (const [key, text] of Object.entries(fields)) {
    if (used.has(key)) continue;
    lines.push(`${key}: ${text}`);
  }

  const who = [data.first, data.last].filter(Boolean).join(' ') || data.name || email;
  const source = data._form || 'website';
  const received = new Date();
  const submitted = received.toLocaleString('en-AU', {
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

  // Content that no genuine enquiry would carry. Answered with the ordinary
  // thank-you so whoever sent it learns nothing, but written to the log in
  // full so a false positive can be found and the rule corrected.
  const reasons = spamReasons(fields, who);
  if (reasons.length) {
    console.log('enquiry discarded as spam', JSON.stringify({
      reasons, form: source, who, email, message: fields.message || '',
    }));
    res.statusCode = 303;
    res.setHeader('Location', nextPath(data._next));
    return res.end();
  }

  const route = routeFor(source);
  const to = addresses(route.to).length ? addresses(route.to) : addresses(ENQUIRY_TO);
  const cc = addresses(route.cc);

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: ENQUIRY_FROM,
        to,
        ...(cc.length ? { cc } : {}),
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

  // The enquiry is delivered; now record it. Awaited, because the function
  // can be frozen the moment the response goes out, but it resolves either
  // way and is capped at a few seconds.
  await logEnquiry({
    fields,
    who,
    email,
    source,
    receivedISO: received.toISOString(),
  });

  res.statusCode = 303;
  res.setHeader('Location', nextPath(data._next));
  return res.end();
};
