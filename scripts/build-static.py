#!/usr/bin/env python3
"""Turn a Simply Static export of templetonbuilt.com.au/ll-build into the
static build that lives in the repo's site/ directory."""

import os, re, shutil, sys
from urllib.parse import unquote, urljoin

SRC = "/tmp/ex"
OUT = "/tmp/build"

STAGING_ABS = "https://templetonbuilt.com.au/ll-build"
LIVE = "https://templetonbuilt.com.au"

# Legacy URLs that only exist as Rank Math redirect stubs. vercel.json owns these.
REDIRECT_STUBS = [
    "about-us", "adelaide-restoration-centre", "building-by-design",
    "commercial-builders-adelaide", "contact-us", "custom-new-homes",
    "download-brochure", "download-renovation-guide", "home-renovations-adelaide",
    "house-extensions-adelaide", "property-development-adelaide",
    "renovation-price-per-square-metre",
]

# WordPress plumbing that has no meaning on a static host.
CRUFT_TAGS = [
    r'<link rel="EditURI"[^>]*>',
    r'<link rel="wlwmanifest"[^>]*>',
    r'<link rel=(?:"|\')?alternate(?:"|\')?[^>]*type="application/rss\+xml"[^>]*>',
    r'<link[^>]*type="application/rss\+xml"[^>]*>',
    r'<link rel="pingback"[^>]*>',
]

report = {"removed_stubs": [], "notes": []}


def reset():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT)


def drop_stubs():
    for slug in REDIRECT_STUBS:
        p = os.path.join(OUT, slug)
        if os.path.isdir(p):
            shutil.rmtree(p)
            report["removed_stubs"].append(slug)


def strip_element(html, tag, elem_id):
    """Remove <tag id="elem_id">...</tag> including nested same-tag children."""
    m = re.search(rf'<{tag}[^>]*\bid=["\']{elem_id}["\'][^>]*>', html, re.I)
    if not m:
        return html
    start, pos, depth = m.start(), m.end(), 1
    token = re.compile(rf'<(/?){tag}\b', re.I)
    while depth:
        t = token.search(html, pos)
        if not t:
            return html  # unbalanced - leave the document alone
        depth += -1 if t.group(1) else 1
        pos = html.index('>', t.end()) + 1
    return html[:start] + html[pos:]


def absolutise_metadata(s):
    """Simply Static made every URL relative, which is wrong for canonicals,
    Open Graph images and JSON-LD. Put the live origin back on those."""

    def canon(path):
        path = path.split("?")[0]
        if path == "/":
            return LIVE + "/"
        return LIVE + "/" + path.strip("/")  # vercel.json sets trailingSlash: false

    s = re.sub(r'(<link rel="canonical" href=")(/[^"]*)(")',
               lambda m: m.group(1) + canon(m.group(2)) + m.group(3), s)
    s = re.sub(r'(<meta property="og:url" content=")(/[^"]*)(")',
               lambda m: m.group(1) + canon(m.group(2)) + m.group(3), s)
    s = re.sub(r'(<meta (?:property|name)="(?:og:image(?::secure_url)?|twitter:image)" content=")(/[^"]*)(")',
               lambda m: m.group(1) + LIVE + m.group(2) + m.group(3), s)

    # JSON-LD: "@id":"/...", "url":"/...", "contentUrl":"/..."
    s = re.sub(r'"(@id|url|contentUrl|logo|image)":"(/[^"]*)"',
               lambda m: f'"{m.group(1)}":"{LIVE}{m.group(2)}"', s)
    return s


def rewrite_html():
    changed = 0
    for root, _, files in os.walk(OUT):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(root, f)
            s = orig = open(p, encoding="utf-8", errors="replace").read()

            # staging path -> live root
            s = s.replace(STAGING_ABS + "/", LIVE + "/").replace(STAGING_ABS, LIVE)
            s = s.replace('"/ll-build/', '"/').replace("'/ll-build/", "'/")
            s = s.replace('/ll-build/', '/')

            # WordPress default org name leaking into JSON-LD
            s = s.replace('"name":"My WordPress"', '"name":"Templeton Built"')

            for pat in CRUFT_TAGS:
                s = re.sub(pat, "", s, flags=re.I)

            # xmlrpc / RSD endpoints do not exist statically
            s = re.sub(r'<link[^>]*xmlrpc\.php[^>]*>', "", s, flags=re.I)

            # Divi's stock header/footer are display:none via the child theme.
            # They only contribute dead weight and links to WP archives that
            # this static build does not contain.
            s = strip_element(s, "header", "main-header")
            s = strip_element(s, "div", "top-header")
            s = strip_element(s, "footer", "main-footer")

            s = absolutise_metadata(s)

            if s != orig:
                open(p, "w", encoding="utf-8").write(s)
                changed += 1
    report["html_rewritten"] = changed


def rewrite_sitemaps():
    # Rank Math emitted relative <loc> values (invalid). Make them absolute and
    # drop the category sitemap - no category archives exist in the static build.
    cat = os.path.join(OUT, "category-sitemap.xml")
    if os.path.exists(cat):
        os.remove(cat)
        report["notes"].append("Removed category-sitemap.xml (no category archives in build)")

    for name in ("sitemap_index.xml", "sitemap.xml", "page-sitemap.xml", "post-sitemap.xml"):
        p = os.path.join(OUT, name)
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8", errors="replace").read()
        s = s.replace(STAGING_ABS, LIVE)
        s = re.sub(r"<loc>/", f"<loc>{LIVE}/", s)
        s = re.sub(r'href="/main-sitemap\.xsl"', f'href="{LIVE}/main-sitemap.xsl"', s)
        # index no longer lists categories
        s = re.sub(r"\s*<sitemap>\s*<loc>[^<]*category-sitemap\.xml</loc>.*?</sitemap>", "", s, flags=re.S)
        open(p, "w", encoding="utf-8").write(s)


def collect_refs():
    """Walk HTML then CSS, following references, to find every asset actually used."""
    keep = set()
    queue = []

    attr_re = re.compile(r'(?:href|src|content|data-src)\s*=\s*["\']([^"\']+)["\']', re.I)
    srcset_re = re.compile(r'srcset\s*=\s*["\']([^"\']+)["\']', re.I)
    url_re = re.compile(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)', re.I)
    import_re = re.compile(r'@import\s+["\']([^"\']+)["\']', re.I)
    # paths that appear inside inline JS / JSON config
    bare_re = re.compile(r'["\'](/wp-(?:content|includes)/[^"\'\s?]+)', re.I)

    def norm(ref, base_dir):
        ref = ref.strip().split("?")[0].split("#")[0]
        if not ref or ref.startswith(("data:", "mailto:", "tel:", "javascript:", "//", "http")):
            return None
        if ref.startswith("/"):
            rel = ref.lstrip("/")
        else:
            rel = os.path.normpath(os.path.join(base_dir, ref))
        rel = unquote(rel)
        if rel.startswith(".."):
            return None
        return rel

    def add(rel):
        full = os.path.join(OUT, rel)
        if os.path.isfile(full) and rel not in keep:
            keep.add(rel)
            if rel.endswith(".css"):
                queue.append(rel)

    for root, _, files in os.walk(OUT):
        for f in files:
            if not f.endswith((".html", ".xml", ".xsl")):
                continue
            p = os.path.join(root, f)
            base = os.path.relpath(root, OUT)
            base = "" if base == "." else base
            s = open(p, encoding="utf-8", errors="replace").read()
            refs = attr_re.findall(s) + url_re.findall(s) + bare_re.findall(s)
            for ss in srcset_re.findall(s):
                refs += [c.strip().split(" ")[0] for c in ss.split(",")]
            for r in refs:
                rel = norm(r, base)
                if rel:
                    add(rel)

    while queue:
        css = queue.pop()
        p = os.path.join(OUT, css)
        base = os.path.dirname(css)
        s = open(p, encoding="utf-8", errors="replace").read()
        for r in url_re.findall(s) + import_re.findall(s):
            rel = norm(r, base)
            if rel:
                add(rel)
    return keep


def prune(keep):
    removed = 0
    freed = 0
    for area in ("wp-includes", "wp-content"):
        base = os.path.join(OUT, area)
        for root, _, files in os.walk(base):
            for f in files:
                p = os.path.join(root, f)
                rel = os.path.relpath(p, OUT)
                if rel not in keep:
                    freed += os.path.getsize(p)
                    os.remove(p)
                    removed += 1
    # drop now-empty dirs
    for root, dirs, files in os.walk(OUT, topdown=False):
        if not os.listdir(root) and root != OUT:
            os.rmdir(root)
    report["assets_removed"] = removed
    report["assets_freed_mb"] = round(freed / 1e6, 1)


def copy_vercel_config():
    """Vercel's Root Directory is site/, so it reads site/vercel.json - not the
    one at the repo root. Root stays the editable source; this mirrors it in."""
    src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vercel.json")
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(OUT, "vercel.json"))
        report["notes"].append("Copied vercel.json into the build")


if __name__ == "__main__":
    reset()
    drop_stubs()
    rewrite_html()
    rewrite_sitemaps()
    copy_vercel_config()
    keep = collect_refs()
    report["assets_kept"] = len(keep)
    prune(keep)
    for k, v in report.items():
        print(f"{k}: {v}")
