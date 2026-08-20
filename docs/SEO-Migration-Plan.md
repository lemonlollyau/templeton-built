# Templeton Built — SEO Migration Plan

How to move templetonbuilt.com.au from WordPress to the new static site without losing rankings.

---

## The core principle

Google doesn't rank "your website." It ranks **individual URLs**. Every URL that currently has
rankings, traffic or backlinks is an asset. A migration loses SEO in exactly three ways:

1. **A URL disappears** and nothing tells Google where it went → the ranking dies.
2. **A URL survives but its content is gutted** → the ranking decays over weeks.
3. **The new page is technically worse** (slower, unindexable, missing tags) → gradual decline.

Everything below exists to prevent those three things. Done properly, a migration is neutral to
positive. Done carelessly, a site can lose 40–70% of organic traffic and take 6–12 months to recover.

---

## ⚠️ The most important finding

**Templeton Built has a substantial blog library that is not in the main navigation.** It appears to
be actively published (posts dated through to May 2026) and is almost certainly the site's main
source of organic traffic.

Confirmed URLs found so far include:

- `/luxury-home-builder-adelaide/`
- `/house-extension-cost-adelaide/`
- `/home-extensions-adelaide-cost/`
- `/home-extension-and-renovation-costs/`
- `/home-extension-builders-adelaide/`
- `/home-renovation-builders-adelaide/`
- `/renovation-price-per-square-metre/`
- `/small-builder-near-me/`
- `/building-by-design/`
- `/extension-design-and-build/`
- `/adelaide-restoration-centre/`
- `/benefits-of-boutique-builders-adelaide/`
- `/tag/renovation-cost/` (and likely other tag/category archives)

**This list is incomplete.** Step 1 below is non-negotiable.

### The strategic tension

This content is heavily price-led — square-metre rates, budget guides, "how much does X cost."
That is exactly the audience the new positioning is trying to move away from. But it is also
probably where the traffic and the rankings live.

**Do not resolve this by deleting it.** The correct sequence is:

1. **Migrate everything.** Keep every URL alive and indexed.
2. **Re-angle progressively.** Over the following months, rewrite the strongest performers so they
   still answer the cost question — that's what earns the ranking — but frame the answer around
   scope, site conditions and open-book pricing rather than cheapest-per-square-metre.
3. **Add upper-funnel content** aimed at the $600k+ buyer, and interlink it from the cost pages.

You keep the traffic and change who converts from it. Deleting the pages loses both.

---

## Step 1 — Build the complete URL inventory (do this first)

You cannot redirect what you haven't listed. Pull URLs from **all** of these sources, then
de-duplicate into one spreadsheet:

| Source | What it gives you | How |
|---|---|---|
| `templetonbuilt.com.au/sitemap_index.xml` | Every page WordPress knows about | Open in browser, follow each child sitemap |
| **Google Search Console** → Performance → Pages | Every URL earning impressions/clicks, last 16 months | Export |
| **Google Search Console** → Indexing → Pages | Everything Google has indexed | Export |
| **Google Analytics / GA4** → Landing pages, last 12 months | Every URL that received a visit | Export |
| **Screaming Frog** (free to 500 URLs) | Full crawl, catches orphan pages | Crawl the live site |
| **Ahrefs / Semrush** (free tier or trial) | URLs with **backlinks** — the highest-value ones | Site Explorer → Best by links |

Columns to record for each URL:

`URL | Title | Meta description | H1 | Sessions (12mo) | Clicks (16mo) | Backlinks | New URL | Redirect type | Notes`

**Sort by clicks and by backlinks.** Those two columns tell you which pages matter. Usually 20% of
URLs carry 80% of the value — protect those absolutely, and be pragmatic about the tail.

---

## Step 2 — Decide the fate of every URL

Every URL gets exactly one of four outcomes. No URL may be left undecided.

**A. Keep the URL identical.** Best outcome. If a page is performing, keep its slug and rebuild it
on the new template with equal or better content. No redirect needed, no equity lost. *This should
be the default for every blog post.*

**B. Redirect 301 to the closest equivalent.** For pages being renamed or consolidated. The target
must genuinely answer the same question — redirecting ten different pages to the homepage is treated
by Google as a soft 404 and passes almost nothing.

**C. Keep and merge.** Where two pages cover near-identical ground (e.g. `/house-extension-cost-adelaide/`
and `/home-extensions-adelaide-cost/`), merge the content into the stronger URL and 301 the weaker
one to it. This usually *improves* rankings by ending self-competition.

**D. Let it 410.** Only for genuinely worthless URLs with no traffic and no links (spam tags, empty
archives, test pages). Rare.

---

## Step 3 — The redirect map

Already implemented in `vercel.json`:

```json
{ "source": "/home-renovations-adelaide", "destination": "/renovations",   "permanent": true }
{ "source": "/house-extensions-adelaide",  "destination": "/extensions",    "permanent": true }
{ "source": "/custom-new-homes",           "destination": "/custom-homes",  "permanent": true }
{ "source": "/property-development-adelaide", "destination": "/custom-homes", "permanent": true }
{ "source": "/commercial-builders-adelaide",  "destination": "/",            "permanent": true }
{ "source": "/about-us",                   "destination": "/about",         "permanent": true }
{ "source": "/contact-us",                 "destination": "/contact",       "permanent": true }
{ "source": "/download-renovation-guide",  "destination": "/cost-benchmark",  "permanent": true }
{ "source": "/download-brochure",          "destination": "/architect-guide", "permanent": true }
```

### Still to add — the blog

**Recommendation: migrate every blog post at its existing slug.** Rebuild each one under `/journal/`
*only if* you also 301 the old URL. Simpler and safer: keep them at the root, exactly where they are.

```json
{ "source": "/luxury-home-builder-adelaide", "destination": "/journal/luxury-home-builder-adelaide", "permanent": true }
```
…and so on for every post. Generate these programmatically from the inventory spreadsheet — hand-typing
sixty redirects is how one gets missed.

### Redirect rules that matter

- **301, never 302.** 302 is temporary and doesn't pass equity properly. In `vercel.json` that means
  `"permanent": true`.
- **One hop only.** `/old → /middle → /new` leaks equity and slows crawling. Point every old URL
  directly at its final destination.
- **Redirect to a genuinely equivalent page**, or don't redirect at all.
- **Watch trailing slashes.** WordPress uses them (`/about-us/`); the new config sets
  `"trailingSlash": false`. Vercel handles the normalisation, but test both forms.
- **Case sensitivity.** Test any URL with capitals.

---

## Step 4 — Preserve on-page equity

For every migrated page:

- [ ] **Title tag** — keep the existing one if the page ranks well. A rewritten title on a ranking
      page is a real risk. Improve titles on pages that *don't* rank, not on ones that do.
- [ ] **H1** — same principle.
- [ ] **Word count and depth** — the new page should be at least as substantial. Trimming a
      2,000-word ranking article to 400 words of nicer prose will lose the ranking.
- [ ] **Internal links** — the new site must link to the migrated posts. Orphaned pages decay.
      Link from the relevant service page and from `/journal`.
- [ ] **Images** — keep filenames and alt text where they're descriptive.
- [ ] **Canonical tag** — self-referencing, absolute URL, on every page. Already implemented.
- [ ] **Structured data** — Article schema on posts, FAQPage on service pages, LocalBusiness /
      GeneralContractor on the homepage. Already implemented on the new pages.

---

## Step 5 — Pre-launch checklist

Run all of this on the Vercel preview URL **before** pointing DNS.

- [ ] Every URL in the inventory has a decided destination
- [ ] `noindex` is on `/thank-you` and the `/lp-*` pages only — and **nowhere else**
- [ ] `robots.txt` allows crawling and points at the sitemap
- [ ] `sitemap.xml` lists every live page including migrated blog posts
- [ ] Zero broken internal links (crawl the preview with Screaming Frog)
- [ ] Unique title + meta description on every page
- [ ] Canonical on every page, pointing at the production domain
- [ ] GA4 and Google Tag Manager installed (current container: `GTM-PZD28M3F`)
- [ ] Conversion tracking on form submissions and the guide downloads
- [ ] Mobile passes Core Web Vitals; images compressed and lazy-loaded
- [ ] NAP details identical to Google Business Profile: `Templeton Built Pty Ltd, 12 Stirling Street,
      Thebarton SA 5033, 1800 955 111`
- [ ] **A full backup of the WordPress site and database exists**

> **Critical:** the current site is built with Slider Revolution and a WordPress theme. Do not
> cancel the hosting until the new site has been live and stable for at least 60 days. You may need
> to check old content.

---

## Step 6 — Launch day

1. Deploy the new site to Vercel and confirm it's serving correctly on the `*.vercel.app` URL.
2. Point DNS at Vercel (SiteGround → Site Tools → Domain → DNS Zone Editor:
   A `@` → `76.76.21.21`, CNAME `www` → `cname.vercel-dns.com`).
3. **Leave MX records alone** unless email is also moving — changing them breaks their email.
4. Wait for SSL to issue automatically, then confirm HTTPS works on both apex and www.
5. Pick one canonical version (apex or www) and redirect the other.
6. Spot-check 20 redirects manually, prioritising the highest-traffic old URLs.

---

## Step 7 — Immediately after launch

- **Google Search Console:** submit the new `sitemap.xml`. Keep the old property; add a new one if
  the protocol or subdomain changes.
- **Request indexing** on the 10–15 most important URLs via URL Inspection.
- **Bing Webmaster Tools:** same.
- **Google Business Profile:** update the website link, add new photos.
- **Update backlinks you control:** social profiles, directories, HIA/MBA listings, supplier sites.
  If a high-value external site links to a changed URL, email them and ask for the update — a direct
  link is worth more than a redirected one.

---

## Step 8 — Monitor for 90 days

| When | Check |
|---|---|
| Days 1–7 | GSC **Indexing → Pages** for a spike in 404s or "Not found." Every 404 with traffic means a missed redirect — add it immediately. |
| Weekly, weeks 1–8 | GSC Performance: total clicks and impressions vs the same period before launch. Compare **page by page**, not just sitewide. |
| Weekly | Crawl stats — a sustained drop means Google is struggling to access something. |
| Monthly | Rankings for core terms: *builder Adelaide, home extensions Adelaide, custom home builder Adelaide, renovation builder Adelaide*. |

### What's normal vs what isn't

**Normal:** a 10–20% dip in weeks 1–3 as Google re-crawls and re-evaluates, recovering by week 6–8.

**Not normal:** a drop that keeps deepening past week 4, or one concentrated on specific
high-value pages. That usually means a broken redirect, an accidental `noindex`, or content that
was thinned too far. Diagnose immediately rather than waiting it out.

---

## The single biggest risk on this project

Accidentally shipping `noindex` sitewide. It's the most common catastrophic migration error —
a staging flag left on, or a global setting copied across. It can wipe a site from Google within
days and is invisible unless you look.

**Check `view-source:` on the live homepage on launch day** and confirm there is no
`<meta name="robots" content="noindex">`.

---

*Prepared for Templeton Built · Adelaide*
