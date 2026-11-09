# How this site is built

`site/` is **generated**. Edit `src/`, then run:

```bash
python3 build.py              # all 37 pages
python3 build.py home about   # just those
```

## Where things live

| | |
|---|---|
| `src/layout.html` | the shell — head, nav, footer. Change the nav once, it changes everywhere. |
| `src/pages/<slug>/body.html` | that page's content |
| `src/pages/<slug>/meta.json` | title, description, canonical, robots, OG tags, schema, and whether the page shows the nav / footer CTA |
| `src/assets/site.css` | the whole design system |
| `src/assets/site.js` | nav, scroll reveals, costing-schedule animation |
| `src/journal-order.json` | optional — order, titles and blurbs for the Journal index |

Generated on every build: all `index.html` files, `site/assets/`,
`sitemap.xml` (noindex pages excluded) and `robots.txt`.

**Not** generated, so safe to edit directly: `site/api/`, `site/vercel.json`,
`site/wp-content/uploads/`.

## Adding an article

Create `src/pages/<slug>/` with `body.html` and `meta.json` (set
`"is_article": true`), then build. It appears on `/journal` automatically —
articles can't go orphaned the way they did before.

## Page chrome

`meta.json` controls it per page:

- `"nav": false` — no site nav. The five `lp-*` ad landing pages and
  `/thank-you` use this; landing pages carry their own `lp-nav` header in
  their body so visitors don't click away from the ad.
- `"foot_top": true` — shows the "Let's talk about what you're picturing"
  block above the footer columns. Homepage only.
