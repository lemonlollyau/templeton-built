#!/usr/bin/env python3
"""Generate site/ from src/.

    python3 build.py            rebuild every page
    python3 build.py home about rebuild only those pages

Source of truth:
    src/layout.html      the shell — header, nav, footer, head
    src/assets/*         css and js, copied to site/assets/
    src/pages/<slug>/    body.html + meta.json per page

Everything under site/ except wp-content/, api/ and vercel.json is generated
and safe to delete. Edit src/, never site/.
"""
import hashlib
import html as htmllib
import json
import pathlib
import re
import shutil
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
SITE = ROOT / "site"
PAGES = SRC / "pages"

SITE_URL = "https://templetonbuilt.com.au"


def attr(value: str) -> str:
    """Escape a value for an HTML attribute.

    Unescapes first, so a source value that already contains &amp; doesn't
    become &amp;amp;. Apostrophes are left alone — attributes here are
    double-quoted, and &#x27; only adds noise.
    """
    text = htmllib.unescape(str(value))
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )

# Articles, newest first, for the Journal index. (slug, date, category, blurb)
JOURNAL_ORDER = "journal-order.json"


def asset_version() -> str:
    """Cache-bust css/js on content change rather than on every build.

    hashlib, not hash() — the built-in is salted per process, so identical
    assets would get a new version on every run and defeat caching.
    """
    h = hashlib.sha256()
    for f in sorted((SRC / "assets").rglob("*")):
        if f.is_file():
            h.update(f.name.encode())
            h.update(f.read_bytes())
    return h.hexdigest()[:8]


NAV = (
    '<nav class="nav over" id="nav"><div class="wrap nav-in">'
    '<a href="/" class="logo" aria-label="Templeton Built home">'
    '<img src="/wp-content/uploads/2026/10/TempletonBuilt-Logo-White-Horiz.png"'
    ' alt="Templeton Built" width="120" height="40"></a>'
    '<button class="nav-toggle" id="toggle" aria-label="Open menu" aria-expanded="false">'
    '<svg width="26" height="14" viewBox="0 0 26 14" fill="none" aria-hidden="true">'
    '<path d="M0 1h26M0 13h26" stroke="currentColor" stroke-width="1.4"></path></svg></button>'
    '<div class="nav-links" id="links">'
    '<a href="/projects">Projects</a><a href="/custom-homes">Custom homes</a>'
    '<a href="/extensions">Extensions</a><a href="/renovations">Renovations</a>'
    '<a href="/interior-design">Interior design</a>'
    '<a href="/open-book">Pricing</a>'
    '<div class="nav-group">'
    '<button type="button" class="nav-group-btn" id="about-btn"'
    ' aria-expanded="false" aria-controls="about-drop">About</button>'
    '<div class="nav-drop" id="about-drop">'
    '<a href="/about">About Templeton Built</a>'
    '<a href="/journal">Journal</a>'
    '</div></div>'
    "</div></div></nav>\n"
)

# The homepage is the only page that opens its footer with this block; the
# rest would be repeating a call to action they already have on the page.
FOOT_TOP = (
    '<div class="foot-top"><div class="rev"><span class="label">Get in touch</span>'
    '<h2 style="margin-top:22px">Let&rsquo;s talk about what you&rsquo;re picturing.</h2></div>'
    '<div class="rev foot-cta"><a href="/contact" class="btn btn-light">Book A Conversation</a>'
    "</div></div>"
)


def head_meta(meta: dict) -> dict:
    """Render the per-page head fragments."""
    out = {}

    out["robots"] = (
        f'<meta name="robots" content="{meta["robots"]}">\n' if meta.get("robots") else ""
    )

    canonical = meta.get("canonical")
    if not canonical:
        slug = meta["slug"]
        canonical = SITE_URL + ("/" if slug == "home" else f"/{slug}")
    out["canonical"] = f'<link rel="canonical" href="{canonical}">\n'

    og = dict(meta.get("og") or {})
    og.setdefault("title", meta["title"])
    og.setdefault("description", meta["description"])
    og.setdefault("url", canonical)
    og.setdefault("type", "article" if meta.get("is_article") else "website")
    og.setdefault("locale", "en_AU")
    og.setdefault("site_name", "Templeton Built")
    lines = [f'<meta property="og:{k}" content="{attr(v)}">'
             for k, v in og.items()]

    tw = dict(meta.get("twitter") or {})
    tw.setdefault("card", "summary_large_image")
    lines += [f'<meta name="twitter:{k}" content="{attr(v)}">'
              for k, v in tw.items()]
    out["og"] = "\n".join(lines) + "\n"

    schema = meta.get("schema") or []
    out["schema"] = "".join(
        f'<script type="application/ld+json">{s}</script>\n' for s in schema
    )
    return out


def article_heading(slug: str, fallback: str) -> str:
    """The article's own H1, not its SEO title.

    Search titles carry a brand suffix ("... - Templeton Built") that reads
    as spam repeated down an index page. The H1 is what the article calls
    itself.
    """
    body = (PAGES / slug / "body.html").read_text(encoding="utf-8")
    m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    if m:
        text = re.sub(r"<[^>]+>", "", m.group(1))
        text = " ".join(htmllib.unescape(text).split())
        if text:
            return text
    # No H1: fall back to the search title with its brand suffix trimmed.
    return re.sub(r"\s*[|—-]\s*Templeton Built\s*$", "", fallback).strip()


def journal_index(pages: dict) -> str:
    """Build the article list for /journal.

    Every article page becomes a card, so nothing is orphaned. Order and
    blurbs come from src/journal-order.json when present; anything missing
    from that file is appended so a new article can never silently vanish.
    """
    order_file = SRC / JOURNAL_ORDER
    listed = json.loads(order_file.read_text(encoding="utf-8")) if order_file.exists() else []

    articles = {s: m for s, m in pages.items() if m.get("is_article")}
    known = [e for e in listed if e["slug"] in articles]
    rest = sorted(set(articles) - {e["slug"] for e in known})
    entries = known + [{"slug": s} for s in rest]

    cards = []
    for e in entries:
        slug = e["slug"]
        m = articles[slug]
        heading = e.get("title") or article_heading(slug, m["title"])
        blurb = e.get("blurb") or m["description"]
        label = e.get("category", "Journal")
        cards.append(
            f'<a class="jcard rev" href="/{slug}">'
            f'<span class="label">{attr(label)}</span>'
            f"<h3>{attr(heading)}</h3>"
            f'<p class="muted">{attr(blurb)}</p>'
            f'<span class="jcard-more">Read this</span></a>'
        )

    return (
        '<section class="pad-sm"><div class="wrap">'
        '<div class="sec-head" style="margin-bottom:40px">'
        '<span class="label">All articles</span>'
        '<h2 class="rev">Everything we’ve written down.</h2></div>'
        f'<div class="jgrid">{"".join(cards)}</div>'
        "</div></section>"
    )


def write_sitemap(pages: dict) -> int:
    """Generate sitemap.xml from the pages actually built.

    noindex pages are left out, and URLs carry no trailing slash to match
    vercel.json's trailingSlash:false — otherwise every entry redirects.
    """
    urls = []
    for slug, meta in sorted(pages.items()):
        if "noindex" in (meta.get("robots") or "").lower():
            continue
        loc = SITE_URL if slug == "home" else f"{SITE_URL}/{slug}"
        urls.append(
            f"  <url>\n    <loc>{loc}</loc>\n"
            f"    <changefreq>monthly</changefreq>\n  </url>"
        )
    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n",
        encoding="utf-8",
    )
    (SITE / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8"
    )
    return len(urls)


def build(only: list[str] | None = None) -> None:
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    ver = asset_version()

    # assets
    dest = SITE / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    for f in (SRC / "assets").iterdir():
        if f.is_file():
            shutil.copy2(f, dest / f.name)

    pages = {
        d.relative_to(PAGES).as_posix(): json.loads((d / "meta.json").read_text(encoding="utf-8"))
        for d in sorted(PAGES.rglob("*"))
        if (d / "meta.json").exists()
    }

    built = 0
    total = 0
    for slug, meta in pages.items():
        if only and slug not in only:
            continue
        body = (PAGES / slug / "body.html").read_text(encoding="utf-8").strip()

        if slug == "journal":
            body += "\n\n" + journal_index(pages)

        page = layout
        for key, value in head_meta(meta).items():
            page = page.replace("{{" + key + "}}", value)
        page = (
            page.replace("{{title}}", attr(meta["title"]))
            .replace("{{description}}", attr(meta["description"]))
            .replace("{{assetver}}", ver)
            .replace("{{nav}}", NAV if meta.get("nav", True) else "")
            .replace("{{foottop}}", FOOT_TOP if meta.get("foot_top") else "")
            .replace("{{body}}", body)
        )

        if "{{" in page:
            leftover = set(re.findall(r"\{\{(\w+)\}\}", page))
            sys.exit(f"{slug}: unreplaced placeholders {leftover}")

        out = SITE / ("index.html" if slug == "home" else f"{slug}/index.html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        built += 1
        total += len(page)

    print(f"built {built} page(s), {total:,} bytes  (assets v{ver})")
    if built:
        print(f"average page: {total // built:,} bytes")
    if not only:
        print(f"sitemap.xml: {write_sitemap(pages)} indexable urls; robots.txt written")


if __name__ == "__main__":
    t0 = time.time()
    build(sys.argv[1:] or None)
    print(f"done in {time.time() - t0:.2f}s")
