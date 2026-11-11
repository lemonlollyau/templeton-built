/**
 * Spam defences for the enquiry endpoint.
 *
 * Two independent layers, because the spam this site actually receives
 * arrives two different ways.
 *
 * 1. A signed form token. The page fetches one from /api/form-token on load
 *    and carries it in a hidden field. Scripted posts that never render the
 *    page have no token and can't forge one. This is the layer that matters:
 *    the spam hitting this site sends `first` and `last` fields to a form
 *    that has neither, which means it is POSTing at the endpoint directly
 *    rather than filling anything in.
 *
 * 2. Content rules, as a backstop. Deliberately narrow — only patterns a
 *    real enquiry from an Adelaide homeowner would never contain. A client
 *    pasting one link to their Pinterest board must still get through, so
 *    a single URL is not a signal here.
 *
 * Environment:
 *   FORM_TOKEN_SECRET   signing key. While unset, token checking is skipped
 *                       entirely so a deploy can't lock the forms.
 */

const crypto = require('crypto');

// How long a minted token stays valid. Long enough that someone can leave a
// tab open over lunch and still send their enquiry.
const TOKEN_TTL_MS = 6 * 60 * 60 * 1000;
// Tolerance for a clock running ahead of ours.
const TOKEN_SKEW_MS = 2 * 60 * 1000;

function secret() {
  return process.env.FORM_TOKEN_SECRET || '';
}

function sign(stamp) {
  return crypto.createHmac('sha256', secret()).update(String(stamp)).digest('base64url').slice(0, 27);
}

/** A token for the page to carry back. */
function mintToken() {
  const stamp = Date.now().toString(36);
  return `${stamp}.${sign(stamp)}`;
}

/**
 * Why a token is unacceptable, or null if it's fine.
 *
 * Returns null when no secret is configured — an unset env var must not
 * silently close the forms.
 */
function tokenProblem(token) {
  if (!secret()) return null;
  if (typeof token !== 'string' || !token.includes('.')) return 'missing';

  const [stamp, provided] = token.split('.', 2);
  const expected = sign(stamp);
  const a = Buffer.from(provided || '');
  const b = Buffer.from(expected);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return 'bad signature';

  const issued = parseInt(stamp, 36);
  if (!Number.isFinite(issued)) return 'unreadable timestamp';
  const age = Date.now() - issued;
  if (age > TOKEN_TTL_MS) return 'expired';
  if (age < -TOKEN_SKEW_MS) return 'issued in the future';
  return null;
}

// Scripts an Adelaide builder's enquiries are never written in.
const CYRILLIC = /[Ѐ-ӿ]/;
const CJK = /[一-鿿぀-ヿ가-힯]/;
// Markup nobody types into a textarea by hand.
const MARKUP_LINK = /<a\s[^>]*href\s*=|\[url[=\]]|\[link[=\]]/i;

/**
 * Reasons this submission looks like spam. Empty means it doesn't.
 *
 * Every rule here has to be one a genuine enquiry could not plausibly trip,
 * because a false positive means a real customer is quietly ignored. That
 * is a worse outcome than a spam email, so the bar is set accordingly: no
 * keyword lists, no scoring, no penalising a single shared link.
 */
function spamReasons(fields = {}, who = '') {
  const reasons = [];
  const message = String(fields.message || '');
  const all = [who, fields.email, fields.suburb, message].filter(Boolean).join('\n');

  if (MARKUP_LINK.test(all)) reasons.push('markup link');
  if (CYRILLIC.test(all)) reasons.push('cyrillic');
  if (CJK.test(all)) reasons.push('cjk');

  const links = (all.match(/https?:\/\//gi) || []).length;
  if (links >= 3) reasons.push(`${links} links`);

  if (message.length > 2500) reasons.push(`message ${message.length} chars`);

  return reasons;
}

module.exports = { mintToken, tokenProblem, spamReasons, TOKEN_TTL_MS };
