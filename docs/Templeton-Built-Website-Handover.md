# Templeton Built — Website Handover

**Prepared by lemonlolly**
Staging site: `templetonbuilt.com.au/ll-build/`

---

## 1. What has been built

A complete rebuild of the Templeton Built website, repositioned around custom homes, extensions and renovations for the upper end of the Adelaide market.

**Twenty-four pages plus sixteen journal articles**, built on WordPress with the Divi theme.

### Core pages
| Page | URL |
|---|---|
| Home | `/` |
| Custom Homes | `/custom-homes` |
| Extensions | `/extensions` |
| Renovations | `/renovations` |
| Projects | `/projects` |
| The Open Book | `/open-book` |
| About | `/about` |
| Journal | `/journal` |
| Contact | `/contact` |

### Project case studies
`/projects/stirling-residence` · `/projects/semaphore-extension` · `/projects/hawthorn-renovation` · `/projects/meadows-new-home`

### Advertising landing pages
Built for Google Ads. Stripped-back header, form above the fold, no navigation, set to `noindex` so they don't compete with the main site in search.

`/lp-custom-homes` · `/lp-extensions` · `/lp-renovations` · `/lp-knockdown-rebuild` · `/lp-adelaide-hills`

### Lead magnet pages
`/architect-guide` — *Before You Brief An Architect*
`/cost-benchmark` — *The Adelaide Cost Benchmark*

---

## 2. The strategic position

The previous site offered six service lines — renovations, extensions, custom homes, property development, commercial construction and retail fitouts. At the upper end of the market, breadth reads as generalism, and generalists get compared on price.

The new site does three things and says so plainly: **custom homes, extensions, renovations.**

**Open-book pricing is the spine of the site.** Showing every trade, every allowance and the builder's margin is a genuine differentiator that competitors cannot copy without actually doing it. It appears on the homepage, has its own page, and features on every landing page.

**Language changed throughout.** "Request a quote" became "start a conversation". Price-led copy became certainty-led copy. At this level the buyer's anxiety is not cost — it is losing control of a two-year process.

---

## 3. What needs your review

These items were written or assembled by lemonlolly and **require Templeton Built's confirmation before launch.**

### Content that is not yet verified

| Item | Where | Status |
|---|---|---|
| **Four project case studies** | `/projects/*` | Narratives are plausible reconstructions based on the old site, **not fact**. Each needs Jordan's account of what actually happened. |
| **Quote attributed to Jordan** | `/open-book` | *"People don't distrust builders because of the price..."* — Jordan did not say this. Approve, rewrite in his words, or remove. |
| **Statistics** | `/about` | 64 bespoke homes, 400+ renovations, 200+ extensions. Taken from the previous site. Confirm still current. |
| **Frank Templeton** | `/about` | Named as third generation, from the old site. Confirm he should appear. |
| **"Around thirty years"** | `/about` | From the old site. Confirm. |
| **Cost figures** | Cost Benchmark PDF | Ranges taken from existing blog content. Harder to correct once distributed. |
| **Project metadata** | Project cards | Suburb and scope shown. Build durations not yet supplied. |

### Decisions outstanding

- **Logo** — an SVG version is needed. Currently using a PNG.
- **Brand blue** — a placeholder hex is in use pending the correct value.
- **Journal thumbnails** — imported articles use stock images with text baked into them ("7 BEST BUILDERS" etc). These undercut the premium positioning and should be replaced with Templeton Built's own photography.

---

## 4. What is not finished

| Item | Notes |
|---|---|
| **Form submissions** | **No form on the site currently sends anywhere.** All forms redirect to a thank-you page. Connecting these to Klaviyo is the single highest priority before launch. |
| **Guide PDFs** | Both lead magnets are written and designed but not yet uploaded or linked to the download forms. |
| **Before/after sliders** | Requested for Extensions and Renovations. Not yet built. |
| **Reviews section** | Requested for Renovations, sourced from the old site. Not yet built. |
| **Nepenthe Cellar Door project** | To be added to Projects. |
| **Journal article quality** | Seven of the imported articles came across with partial content and need completion. Several also promote competitors and need editing. |
| **Photography** | The site currently uses images from the old website. A proper shoot is recommended. |

---

## 5. How the site is maintained

### Editing page content
Pages are built in Divi. Content sits inside **Code modules** — editing text means editing HTML within those modules. This was a deliberate trade: it preserves the design exactly, at the cost of visual editing.

For routine copy changes, contact lemonlolly.

### Site-wide elements
The header, footer, navigation and global styling are controlled by a single snippet:

**WordPress admin → Code Snippets → "Templeton Built — Site Chrome"**

This is the only place that code lives. Editing it changes every page at once.

### Navigation menu
**Appearance → Menus**, location *"Templeton Built — Primary"*. If no menu is set, the site falls back to a built-in list.

### SEO
**Rank Math** manages titles, meta descriptions, sitemaps and redirects. Page titles and descriptions for the main pages are set within the Site Chrome snippet rather than per-page, so they stay consistent.

### Caching
SiteGround caches aggressively. After any change, use **Purge SG Cache** in the admin bar or changes may not appear.

---

## 6. Search engine migration

The existing site has significant organic traffic that must be protected.

**Completed:**
- 21 redirects installed for retired pages
- 13 blog articles migrated at their original URLs, preserving their rankings
- Titles, descriptions and structured data set across the site
- XML sitemap generating

**Still required at launch:**
- A full URL inventory from Google Search Console, cross-checked against the redirect list
- Google Search Console and Google Analytics connected
- Monitoring of 404 errors weekly for the first month

A 10–20% dip in traffic in weeks one to three is normal and typically recovers by week six to eight. A dip that deepens past week four indicates a problem and should be investigated immediately.

**Critical:** the site currently lives at `/ll-build/`. Moving it to the main domain requires a database search-and-replace. Internal links depend on this step. If it is skipped or run carelessly, navigation across the site will break.

---

## 7. Pre-launch checklist

- [ ] Forms connected and tested end to end
- [ ] Guide PDFs uploaded and download links working
- [ ] Case study content confirmed by Jordan
- [ ] Statistics and quotes verified
- [ ] Logo SVG and brand colour supplied
- [ ] Journal thumbnails replaced
- [ ] Database search-and-replace completed for the domain move
- [ ] Confirm no page carries `noindex` except the five landing pages and the thank-you page
- [ ] Google Search Console and Analytics connected
- [ ] Mobile tested across the full site
- [ ] Full backup taken before go-live
- [ ] Old site retained for at least 60 days after launch

---

## 8. Technical summary

| | |
|---|---|
| Platform | WordPress with Divi theme |
| Child theme | Templeton Built (holds the design system) |
| Hosting | SiteGround |
| SEO | Rank Math |
| Code management | WPCode |
| Typography | Archivo (headings, labels) and Newsreader (body) |
| Palette | Bluestone, limestone and paper, drawn from Adelaide's building materials |

---

*Prepared by lemonlolly for Templeton Built Pty Ltd.*
