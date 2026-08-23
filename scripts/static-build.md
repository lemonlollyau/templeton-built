# Regenerating `site/`

`site/` is a static snapshot of the WordPress staging site. Vercel's Root
Directory points at it, so whatever is committed there is what goes live.

## 1. Export from WordPress

Simply Static is installed on the staging site.

- Settings already set: **delivery method ZIP**, **URLs relative**, **force
  replace URLs on**, and every published page/post listed under Additional URLs
  so nothing unlinked (the `lp-*` ad landing pages, `thank-you`) gets missed.
- Simply Static → **Generate** → download the zip. Takes about 40 seconds.

## 2. Post-process

`scripts/build-static.py` turns the raw export into the build. Point `SRC` at
the unzipped export, then run it and copy `/tmp/build` over `site/`.

It does six things:

1. Deletes the twelve legacy Rank Math redirect stubs — `vercel.json` owns
   those redirects, and a real 301 beats a meta-refresh page.
2. Rewrites `templetonbuilt.com.au/ll-build` → `templetonbuilt.com.au` and
   `/ll-build/` → `/`.
3. Strips Divi's stock `#main-header` / `#main-footer`. The child theme hides
   them with `display:none`, but they still shipped ~460 links to WordPress
   category, date and author archives that do not exist in the build.
4. Removes xmlrpc, RSD and RSS `<link>` tags.
5. Makes canonicals, `og:`/`twitter:` image URLs and JSON-LD absolute, without
   trailing slashes to match `"trailingSlash": false` in `vercel.json`.
6. Prunes every asset nothing references — 1,637 files, 67 MB of unused
   WordPress core CSS and JS. Reference walking follows HTML → CSS → fonts, so
   nothing in use gets dropped.

Result: 37 pages, 200 files, 28 MB.

## 3. Check before pushing

- 37 `index.html` files
- no `ll-build` left in any HTML
- every `href`/`src` resolves to a file that exists
- canonicals absolute

## `vercel.json` lives in two places

Vercel's Root Directory is `site`, so Vercel reads **`site/vercel.json`** and
ignores the one at the repo root. Edit the root copy — `build-static.py` mirrors
it into the build. If you hand-edit `site/vercel.json`, the next build overwrites it.
