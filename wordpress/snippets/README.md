# WPCode snippets

These live in the WordPress database, not in files. Copy them here whenever
they change so the repo stays useful.

| Snippet | Purpose | Status |
|---|---|---|
| `site-chrome.php` | Header, footer, nav, global CSS overrides, SEO title filters, journal grid, costing-schedule animation | **Active** |
| `legacy-blog-importer.php` | One-off import of blog posts from the old site | Can be deactivated once imports are complete |

## site-chrome.php

The single most important file. It controls:

- The site header (two variants: full nav, and stripped-back for landing pages)
- The footer (CTA band on homepage only, four columns, single-line legal bar)
- All CSS overrides that stop Divi fighting the design system
- Rank Math title and description overrides
- `noindex` on landing pages
- The dynamic Journal index
- The animated costing schedule

**To populate this file:** WordPress admin → Code Snippets → open
*"Templeton Built — Site Chrome"* → copy the code → paste here.
