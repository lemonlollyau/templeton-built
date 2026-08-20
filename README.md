# Templeton Built — Website

Source, documentation and design system for **templetonbuilt.com.au**.

Staging: `templetonbuilt.com.au/ll-build/`
Built by [lemonlolly](https://lemonlolly.com)

---

## ⚠️ Read this first — what is and isn't in Git

This is a **WordPress site**. Most of what you see on screen lives in the
WordPress *database*, not in files. Git cannot version it directly.

| Lives in this repo | Lives in the WordPress database |
|---|---|
| Child theme (design system CSS + PHP) | All page content and layouts |
| WPCode snippets (header, footer, styles) | Rank Math titles and descriptions |
| Content importer plugin | The 21 redirects |
| Original static design source | Media library (images, PDFs) |
| Documentation | Menus and settings |

**So this repo is a source-of-truth for code and a reference for content —
not a complete backup.** For a true backup use SiteGround's backup tool or a
WordPress export (`Tools → Export`).

---

## Structure

```
design-source/      Original static HTML build. The reference design.
                    Superseded by the live site — see note below.
wordpress/
  child-theme/      Divi child theme. Holds the full design system.
  snippets/         WPCode snippets. See snippets/README.md.
  plugins/          One-off content importer (now deactivated).
docs/               Handover, SEO migration plan, edit register.
lead-magnets/       The two guide PDFs and the script that builds them.
keyword-research/   Target keywords and negative keyword list.
```

### About `design-source/`

This is the original static build the WordPress site was generated from. It is
**no longer current** — dozens of copy and structural changes have been made
directly in WordPress since. Treat it as the design reference, not as truth.

To bring it back into sync, run `scripts/pull-content.md` (instructions inside).

---

## The design system

| | |
|---|---|
| Display + labels | Archivo |
| Body | Newsreader |
| Bluestone | `#16232B` |
| Bluestone deep | `#0E171D` |
| Slate | `#33474F` |
| Zinc | `#8A9499` |
| Limestone | `#E4DED2` |
| Paper | `#FBFAF8` |

Palette drawn from Adelaide's building vernacular — bluestone, limestone, zinc.

---

## Working on this site

**Global styling, header, footer** → WordPress admin → Code Snippets →
*"Templeton Built — Site Chrome"*. This is the only place that code lives.

**Page content** → Divi Code modules on each page. Editing copy means editing
HTML inside those modules.

**After any change** → Purge SG Cache from the admin bar, or you will not see it.

---

## Status

See `docs/Templeton-Built-Website-Handover.md` for the full picture.

**Not finished:** form submissions go nowhere, guide PDFs aren't linked,
before/after sliders and the reviews section aren't built, seven imported
journal articles are partial.

**Needs client verification:** case study narratives, the quote attributed to
Jordan, the About statistics, and Frank Templeton's inclusion.
