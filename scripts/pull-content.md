# Pulling live content back into the repo

The live WordPress site is ahead of `design-source/`. To snapshot current
content into the repo:

## Option 1 — WordPress export (recommended, complete)

1. WordPress admin → **Tools → Export → All content → Download Export File**
2. Save the `.xml` into `wordpress/content-export/`
3. Commit it

This captures every page, post, and its metadata. It is the closest thing to a
true content backup that is safe to keep in Git.

## Option 2 — Per-page JSON via the REST API

Logged into WP admin, open the browser console and run:

```js
(async () => {
  const R = wpApiSettings.root, N = wpApiSettings.nonce;
  const out = {};
  for (const type of ['pages','posts']) {
    const list = await (await fetch(`${R}wp/v2/${type}?per_page=100&status=publish,draft&_fields=id,slug`,
      {credentials:'same-origin', headers:{'X-WP-Nonce':N}})).json();
    for (const it of list) {
      const f = await (await fetch(`${R}wp/v2/${type}/${it.id}?context=edit&_fields=content,title`,
        {credentials:'same-origin', headers:{'X-WP-Nonce':N}})).json();
      out[it.slug] = { type, title: f.title.raw, content: f.content.raw };
    }
  }
  copy(JSON.stringify(out, null, 2)); // now on your clipboard
})();
```

Paste into `wordpress/content-snapshot.json` and commit.

## The snippets

WPCode snippets are stored in the database. To version them:

1. Code Snippets → open each snippet → copy the code
2. Paste into `wordpress/snippets/<name>.php`
3. Commit

Do this whenever a snippet changes. **This is the most important thing to keep
versioned** — it holds the header, footer and all global styling.
