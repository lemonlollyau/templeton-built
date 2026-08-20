# Templeton Built — WordPress build status

`https://templetonbuilt.com.au/ll-build/wp-admin/`

---

## Do this first (30 seconds)

**Upload the child theme.** Appearance → Themes → Add New → Upload Theme →
`templeton-built-child-theme.zip` → Install → **Activate**.

Nothing will look right until this is active. It carries the entire design system:
palette, Archivo + Newsreader typography, Divi resets, font loading and the
scroll-reveal script.

Then tell me it's done and I'll verify it's rendering before we build on it.

---

## Done

| Item | Status |
|---|---|
| Rank Math installed + configured | ✅ Small Business Site, **GeneralContractor** schema |
| Rank Math Redirections module | ✅ Enabled |
| Permalinks → post name | ✅ `/extensions`, not `/?p=42` |
| Archivo + Newsreader webfonts | ✅ Via Divi → Integration → head |
| Page structure — 19 pages | ✅ All drafts, correct slugs |
| 4 project case studies | ✅ Children of `/projects` |
| 3 journal posts | ✅ Drafts |
| Child theme package | ✅ Built — **needs your upload** |
| Home set as static front page | ✅ Published |
| WordPress Sample Page | ✅ Deleted |

### Pages created (all draft)
`home` · `custom-homes` · `extensions` · `renovations` · `projects` ·
`open-book` · `about` · `journal` · `contact` · `architect-guide` ·
`cost-benchmark` · `thank-you` · `lp-extensions` · `lp-custom-homes` ·
`lp-renovations`

Under `/projects`: `stirling-residence` · `semaphore-extension` ·
`hawthorn-renovation` · `meadows-new-home`

Posts: `what-sets-a-build-budget` · `renovate-or-rebuild` ·
`living-through-a-renovation`

---

## Not done

**Every page is an empty shell.** Titles and URLs only — no content or layout yet.
That's the bulk of the remaining work.

- Divi Theme Builder header + footer (global — everything depends on these)
- Page content, hybrid build: native Divi modules for editable content,
  Code modules for the costing schedule and spec annotations
- Rank Math title + meta description on all 22 URLs
- The 21-item redirect map — Rank Math has no REST endpoint for redirections,
  so these need the UI at Rank Math → Redirections
- Menus

**Useful discovery for next session:** Divi's `_et_pb_use_builder` flag is writable
through the REST API, which means page layouts can be created programmatically
rather than clicked together module by module. That should cut the build time
down substantially.
- Logo upload (still need the SVG) and the brand blue hex

---

## Two things to keep in view

**`/ll-build/` is baked into every URL right now.** Since this moves to the root
domain, budget a proper database search-replace at launch. Do it as a deliberate
step — don't let hardcoded staging URLs get discovered afterwards.

**Privacy Policy** is still a WordPress default — rewrite it before launch. Sample Page is gone.

---

## Realistic estimate

Roughly three to four working sessions to finish, in this order:

1. Child theme active + verified
2. Theme Builder header/footer
3. Homepage as the reference page
4. Three service pages (shared structure — fast once the first is done)
5. Projects, About, Open Book, Contact
6. Journal + migrated blog posts
7. Lead magnet + ad landing pages
8. Rank Math meta, redirects, menus, final QA

---

## In the meantime

The static build is complete and reviewable — open `templeton-preview/index.html`
and click through. Everything we're rebuilding in Divi is already designed and
written there, so it's the best thing to review while the WordPress version
catches up.
