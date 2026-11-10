/**
 * Durable enquiry log.
 *
 * Every enquiry is written as a row in a Notion database, so there is a
 * record to report from that doesn't depend on anyone's inbox staying tidy.
 * Notion supplies the reporting surface itself — filtered views, grouping by
 * month, CSV export, a status column for follow-up — so there is no admin
 * page here to build, secure or maintain.
 *
 * Environment variables (both optional):
 *   NOTION_TOKEN   secret from a Notion internal integration
 *   NOTION_DB_ID   id of the enquiries database, shared with that integration
 *
 * With either missing the log is skipped. Logging never affects the visitor:
 * every failure is caught, and the request is capped by TIMEOUT_MS so a slow
 * Notion can't hold up the thank-you page. If nothing durable captured the
 * enquiry, the full contact details go to the function log so the lead can
 * still be recovered by hand.
 *
 * Filenames under api/ that start with an underscore are not routed, so this
 * module is private to the function that requires it.
 */

const NOTION_API = 'https://api.notion.com/v1/pages';
const NOTION_VERSION = '2022-06-28';
const TIMEOUT_MS = 3000;

// Form field -> Notion text column.
const TEXT_COLUMNS = {
  suburb: 'Suburb',
  rooms: 'Rooms',
  message: 'Message',
};

// Form field -> Notion single-select column. Notion creates an option it
// hasn't seen before, so a new answer on a form doesn't need a schema change.
const SELECT_COLUMNS = {
  type: 'Project type',
  project: 'Project type',
  stage: 'Stage',
  budget: 'Budget',
  timing: 'Timing',
  package: 'Package',
};

// Fields that already have a column of their own. Anything else is collected
// into "Other details" rather than dropped — the open day's preferred day and
// time arrive that way, and so will fields added to a form later.
const OWN_COLUMN = new Set([
  'name', 'first', 'last', 'email', 'phone',
  ...Object.keys(TEXT_COLUMNS), ...Object.keys(SELECT_COLUMNS),
]);

/** Notion caps a rich text block at 2000 characters. */
function richText(value) {
  return { rich_text: [{ text: { content: String(value).slice(0, 2000) } }] };
}

/**
 * A select option, or undefined if there's nothing to record.
 *
 * Notion rejects a comma in an option name, and a typographic dash would
 * create a near-duplicate of an option that already exists with a hyphen
 * ("$50k–$100k" beside "$50k-$100k"), so both are normalised.
 */
function option(value) {
  const name = String(value)
    .replace(/[‒-―]/g, '-')
    .replace(/,/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 100);
  return name ? { select: { name } } : undefined;
}

function properties({ fields, who, email, source, receivedISO }) {
  const props = {
    Name: { title: [{ text: { content: (who || 'Unknown').slice(0, 200) } }] },
    Received: { date: { start: receivedISO } },
  };

  if (email) props.Email = { email };
  if (fields.phone) props.Phone = { phone_number: fields.phone.slice(0, 200) };

  const form = option(source);
  if (form) props.Form = form;

  for (const [key, column] of Object.entries(TEXT_COLUMNS)) {
    if (fields[key] && !props[column]) props[column] = richText(fields[key]);
  }
  for (const [key, column] of Object.entries(SELECT_COLUMNS)) {
    if (!fields[key] || props[column]) continue;
    const pick = option(fields[key]);
    if (pick) props[column] = pick;
  }

  const extra = Object.entries(fields)
    .filter(([key]) => !OWN_COLUMN.has(key))
    .map(([key, value]) => `${key}: ${value}`);
  if (extra.length) props['Other details'] = richText(extra.join('\n'));

  return props;
}

async function writeToNotion(entry) {
  const { NOTION_TOKEN, NOTION_DB_ID } = process.env;
  if (!NOTION_TOKEN || !NOTION_DB_ID) return { logged: false, reason: 'not configured' };

  const abort = new AbortController();
  const timer = setTimeout(() => abort.abort(), TIMEOUT_MS);
  try {
    const r = await fetch(NOTION_API, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${NOTION_TOKEN}`,
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json',
      },
      signal: abort.signal,
      body: JSON.stringify({
        parent: { database_id: NOTION_DB_ID },
        properties: properties(entry),
      }),
    });
    if (!r.ok) {
      console.error('Enquiry log rejected', r.status, await r.text());
      return { logged: false, reason: `notion http ${r.status}` };
    }
    return { logged: true };
  } catch (err) {
    return { logged: false, reason: `notion request failed: ${err && err.message}` };
  } finally {
    clearTimeout(timer);
  }
}

/**
 * Record one enquiry. Always resolves — a logging problem must never turn a
 * delivered enquiry into an error page for the person who sent it.
 */
async function logEnquiry(entry) {
  let result;
  try {
    result = await writeToNotion(entry);
  } catch (err) {
    result = { logged: false, reason: `unexpected: ${err && err.message}` };
  }

  if (result.logged) {
    console.log('enquiry logged', JSON.stringify({
      form: entry.source, at: entry.receivedISO,
    }));
  } else {
    // Nothing durable holds this enquiry, so the function log is the last
    // copy. Write enough to pick the lead up by hand.
    console.log('enquiry NOT logged', JSON.stringify({
      reason: result.reason,
      form: entry.source,
      at: entry.receivedISO,
      who: entry.who,
      email: entry.email,
      phone: entry.fields.phone || '',
    }));
  }

  return result;
}

module.exports = { logEnquiry };
