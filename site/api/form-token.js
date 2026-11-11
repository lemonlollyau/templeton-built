/**
 * Mints the short-lived token the enquiry forms carry.
 *
 * The page fetches this on load (see site.js) and puts the value in a hidden
 * field. A script POSTing straight at /api/enquiry never runs that code, so
 * it has no token and cannot produce one without the signing secret.
 *
 * Deliberately uncached: a stale token from a CDN would defeat the expiry.
 */

const { mintToken, TOKEN_TTL_MS } = require('./_spam.js');

module.exports = function handler(req, res) {
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET');
    res.statusCode = 405;
    return res.end('Method Not Allowed');
  }

  res.statusCode = 200;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store, max-age=0');
  return res.end(JSON.stringify({ token: mintToken(), ttl: TOKEN_TTL_MS }));
};
