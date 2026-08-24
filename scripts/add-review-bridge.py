#!/usr/bin/env python3
"""Install the JUICE review bridge into the static build.

Two jobs:

1. Tag headings and body copy inside the designed sections with stable
   `data-juice-key` attributes, so the Review Room can target content without
   CSS selectors. Only content inside Divi's Code modules
   (`.et_pb_code_inner`) is touched - that is where the hand-built sections
   live. Divi's own chrome, the WordPress post meta and the legacy article
   sidebars are left alone.

2. Insert the bridge loader before `</body>`, guarded so it only runs on
   *.vercel.app. Once the domain points at Vercel, real visitors never load it.

Attributes are inserted into existing opening tags; nothing else in the file is
rewritten, so the diff stays readable.
"""

import os, re, sys
from collections import Counter

SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")

BRIDGE_SRC = "https://lemon-lolly-flow.base44.app/juice-review-bridge.js"
ALLOWED_ORIGIN = "https://lemon-lolly-flow.base44.app"

BRIDGE = f"""<script>
  window.JUICE_REVIEW_CONFIG = {{ allowedOrigins: ["{ALLOWED_ORIGIN}"] }};
</script>
<script>
  /* Review bridge: preview hosts only, never the live domain. */
  if (/(^|\\.)vercel\\.app$/.test(location.hostname)) {{
    var j = document.createElement("script");
    j.src = "{BRIDGE_SRC}";
    j.async = true;
    document.body.appendChild(j);
  }}
</script>
"""

MARKER = "juice-review-bridge.js"
TAGS = ("h1", "h2", "h3", "p")


def code_regions(html):
    """Spans of every .et_pb_code_inner block, with nesting handled."""
    spans = []
    for m in re.finditer(r'<div class="et_pb_code_inner">', html):
        pos, depth = m.end(), 1
        for t in re.finditer(r"<(/?)div\b", html[m.end():]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                pos = m.end() + t.start()
                break
        spans.append((m.end(), pos))
    return spans


def slug(text, limit=28):
    s = re.sub(r"<[^>]+>", " ", text)
    s = re.sub(r"&[a-z]+;|&#\d+;", " ", s)
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_").lower()
    return s[:limit].rstrip("_")


def inner_text(html, start, tag):
    """Text between an opening tag's `>` and its matching close."""
    end = html.find(f"</{tag}", start)
    if end == -1:
        return ""
    return re.sub(r"<[^>]+>", "", html[start:end]).strip()


def tag_page(html):
    regions = code_regions(html)
    if not regions:
        return html, 0

    # Insertions are collected first, then applied right-to-left so earlier
    # offsets stay valid.
    edits = []
    used = Counter()
    sec_no = 0  # counts sections across the whole page, not per block

    for r_start, r_end in regions:
        region = html[r_start:r_end]

        # section boundaries within this region, for readable key prefixes
        # purely presentational classes make poor key prefixes - fall back to
        # a positional name so keys stay stable but never mislead
        PRESENTATIONAL = {"white", "dark", "pad", "pad-sm", "pad-b0", "wrap",
                          "band", "rev", "sec-head", "prose"}
        sections = []
        for sm in re.finditer(r'<(?:section|header)\b([^>]*)>', region):
            sec_no += 1
            attrs = sm.group(1)
            name = (re.search(r'id="([^"]+)"', attrs) or [None, None])[1]
            if not name:
                cls = re.search(r'class="([^"]+)"', attrs)
                first = cls.group(1).split()[0] if cls else None
                name = first if first and first not in PRESENTATIONAL else None
            sections.append((sm.start(), slug(name) if name else f"s{sec_no}"))

        # ranges to skip: legacy sidebars pasted into migrated articles
        skips = [(a.start(), region.find("</aside>", a.start()))
                 for a in re.finditer(r"<aside\b", region)]

        for m in re.finditer(r"<(h1|h2|h3|p)(\s[^>]*)?>", region):
            tag = m.group(1)
            attrs = m.group(2) or ""
            if "data-juice-key" in attrs:
                continue
            if any(s <= m.start() <= (e if e != -1 else len(region)) for s, e in skips):
                continue

            text = inner_text(region, m.end(), tag)
            if len(text) < 3:
                continue

            prefix = "s"
            for pos, name in sections:
                if pos < m.start() and name:
                    prefix = name
            kind = "heading" if tag in ("h1", "h2", "h3") else "body"
            key = f"{prefix}_{kind}"
            used[key] += 1
            if used[key] > 1:
                key = f"{key}_{used[key]}"

            # insert just after the tag name, before any existing attributes
            at = r_start + m.start() + 1 + len(tag)
            edits.append((at, f' data-juice-key="{key}"'))

    for at, text in sorted(edits, reverse=True):
        html = html[:at] + text + html[at:]
    return html, len(edits)


def main():
    if not os.path.isdir(SITE):
        sys.exit(f"no site/ at {SITE}")
    pages = tagged = keys = 0
    for root, _, files in os.walk(SITE):
        for f in files:
            if f != "index.html":
                continue
            p = os.path.join(root, f)
            html = open(p, encoding="utf-8", errors="replace").read()
            orig = html

            html, n = tag_page(html)
            keys += n
            if n:
                tagged += 1

            if MARKER not in html and "</body>" in html:
                html = html.replace("</body>", BRIDGE + "</body>", 1)

            if html != orig:
                open(p, "w", encoding="utf-8").write(html)
                pages += 1

    print(f"pages updated: {pages}")
    print(f"pages with tagged content: {tagged}")
    print(f"data-juice-key attributes added: {keys}")


if __name__ == "__main__":
    main()
