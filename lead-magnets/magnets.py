#!/usr/bin/env python3
"""Templeton Built — lead magnet PDF generator.
Renders branded A4 guides via WeasyPrint using the site's design tokens."""

import os
from weasyprint import HTML

OUT = "/mnt/user-data/outputs"
os.makedirs(OUT, exist_ok=True)

CSS = """
@page {
  size: A4;
  margin: 22mm 20mm 20mm 20mm;
  @bottom-left {
    content: "Templeton Built  ·  Adelaide  ·  Licence BLD183145";
    font-family: 'DejaVu Sans', sans-serif; font-size: 7pt; font-weight: bold;
    letter-spacing: .16em; color: #8A9499;
  }
  @bottom-right {
    content: counter(page);
    font-family: 'DejaVu Sans', sans-serif; font-size: 7pt; color: #8A9499;
  }
}
@page :first { margin: 0; @bottom-left { content: ""; } @bottom-right { content: ""; } }

* { box-sizing: border-box; }
body {
  font-family: 'DejaVu Serif', Georgia, serif;
  font-size: 10.2pt; line-height: 1.62; color: #33474F; margin: 0;
}
h1, h2, h3, .display {
  font-family: 'DejaVu Sans', Helvetica, sans-serif;
  color: #16232B; font-weight: bold; letter-spacing: -.02em; line-height: 1.1; margin: 0;
}
.label {
  font-family: 'DejaVu Sans', sans-serif; font-size: 7.5pt; font-weight: bold;
  letter-spacing: .2em; text-transform: uppercase; color: #8A9499;
}

/* ---------- Cover ---------- */
.cover {
  background: #16232B; color: #FBFAF8;
  padding: 30mm 20mm; height: 297mm; page-break-after: always;
  position: relative;
}
.cover .label { color: #8A9499; }
.cover h1 {
  color: #FBFAF8; font-size: 34pt; margin: 14mm 0 0; letter-spacing: -.035em; line-height: 1.02;
}
.cover .sub {
  font-size: 12pt; line-height: 1.5; color: rgba(251,250,248,.82);
  margin-top: 8mm; max-width: 120mm;
}
.cover .rule { border-top: 1px solid rgba(255,255,255,.22); margin: 14mm 0 6mm; }
.cover .meta { font-family:'DejaVu Sans',sans-serif; font-size: 8pt; letter-spacing:.18em;
  text-transform: uppercase; color: rgba(251,250,248,.6); line-height: 2; }
.cover-foot { position: absolute; bottom: 26mm; left: 20mm; right: 20mm; }
.wordmark { font-family:'DejaVu Sans',sans-serif; font-weight:bold; font-size: 13pt;
  letter-spacing:.22em; text-transform: uppercase; color:#FBFAF8; }

/* ---------- Contents ---------- */
.toc { page-break-after: always; }
.toc-item {
  display: flex; justify-content: space-between; gap: 8mm;
  border-bottom: 1px solid rgba(22,35,43,.14); padding: 3.4mm 0;
  font-family: 'DejaVu Sans', sans-serif; font-size: 10pt; color: #16232B;
}
.toc-item span { font-family:'DejaVu Sans',sans-serif; font-size: 8pt; letter-spacing:.1em; color:#8A9499; }

/* ---------- Body ---------- */
h2 { font-size: 15pt; margin: 9mm 0 3mm; }
h2.first { margin-top: 0; }
h3 { font-size: 11pt; margin: 6mm 0 2mm; }
p { margin: 0 0 3.4mm; }
.lede { font-size: 12.5pt; line-height: 1.5; color: #16232B; margin-bottom: 6mm; }
.sec-rule { border-top: 2px solid #16232B; margin: 0 0 4mm; }

.item { page-break-inside: avoid; margin-bottom: 7mm; }
.item-no {
  font-family:'DejaVu Sans',sans-serif; font-size: 8pt; font-weight:bold; letter-spacing:.2em;
  text-transform:uppercase; color:#8A9499; display: block; margin-bottom: 1.5mm;
}
.item h3 { margin-top: 0; }

.callout {
  background: #E4DED2; padding: 6mm; margin: 6mm 0; page-break-inside: avoid;
}
.callout .label { display:block; margin-bottom: 2.5mm; }
.callout p:last-child { margin-bottom: 0; }

.dark-box { background:#16232B; color:#FBFAF8; padding: 7mm; margin: 7mm 0; page-break-inside: avoid; }
.dark-box h3 { color:#FBFAF8; margin-top:0; }
.dark-box p { color: rgba(251,250,248,.82); }
.dark-box .label { color:#8A9499; }

table { width:100%; border-collapse: collapse; margin: 5mm 0; page-break-inside: avoid; font-size: 9pt; }
th {
  font-family:'DejaVu Sans',sans-serif; font-size:7.5pt; font-weight:bold; letter-spacing:.18em;
  text-transform:uppercase; color:#8A9499; text-align:left; font-weight:normal;
  border-bottom: 1px solid #16232B; padding: 2.5mm 3mm 2.5mm 0;
}
td { padding: 3mm 3mm 3mm 0; border-bottom: 1px solid rgba(22,35,43,.12); vertical-align: top; }
td.n { font-family:'DejaVu Sans',sans-serif; color:#16232B; white-space: nowrap; }

ul { margin: 0 0 3.4mm; padding-left: 5mm; }
li { margin-bottom: 1.6mm; }

.check { list-style:none; padding-left:0; }
.check li { padding: 2.6mm 0 2.6mm 8mm; border-bottom:1px solid rgba(22,35,43,.12); position:relative; }
.check li:before {
  content:"☐"; position:absolute; left:0; top:2.4mm; font-size:11pt; color:#8A9499;
}

/* ---------- Back cover ---------- */
.back { page-break-before: always; background:#16232B; color:#FBFAF8; padding: 30mm 20mm; height: 297mm; }
.back h2 { color:#FBFAF8; font-size: 24pt; letter-spacing:-.03em; }
.back p { color: rgba(251,250,248,.82); }
.back .label { color:#8A9499; }
.back .rule { border-top:1px solid rgba(255,255,255,.22); margin: 10mm 0; }
.back a { color:#E4DED2; text-decoration:none; }
.big { font-family:'DejaVu Sans',sans-serif; font-size: 15pt; font-weight:bold; letter-spacing:-.02em; color:#FBFAF8; }
"""


def cover(label, title, sub, meta):
    rows = "".join(f"{m}<br>" for m in meta)
    return f"""<div class="cover">
  <div class="wordmark">Templeton Built</div>
  <div style="margin-top:38mm">
    <div class="label">{label}</div>
    <h1>{title}</h1>
    <p class="sub">{sub}</p>
  </div>
  <div class="cover-foot">
    <div class="rule"></div>
    <div class="meta">{rows}</div>
  </div>
</div>"""


BACK = """<div class="back">
  <div class="label">Next step</div>
  <h2 style="margin-top:8mm">If the numbers in this guide<br>made you want a second<br>opinion, that's the point.</h2>
  <p style="margin-top:8mm;max-width:120mm">We price every project open-book: you receive the full costing schedule, every trade,
  every allowance and our margin written plainly at the bottom. It is the fastest way to find out
  whether what you want and what you have are the same size.</p>
  <p style="max-width:120mm">A first conversation costs nothing. Bring a survey, a sketch, or just the address.</p>
  <div class="rule"></div>
  <div class="label">Talk to Jordan or Paul</div>
  <p class="big" style="margin-top:5mm">1800 955 111</p>
  <p class="big">hello@templetonbuilt.com.au</p>
  <p style="margin-top:8mm">12 Stirling Street, Thebarton SA 5033<br>
  templetonbuilt.com.au</p>
  <div class="rule"></div>
  <div class="label">Templeton Built Pty Ltd &nbsp;·&nbsp; ABN 16 067 209 161 &nbsp;·&nbsp; Licence BLD183145</div>
  <p style="font-size:8pt;margin-top:6mm;color:rgba(251,250,248,.55);max-width:130mm">
  This guide is general information for Adelaide homeowners planning a project. It is not a quote,
  a cost estimate for your specific property, or professional advice on your site. Figures reflect
  general market conditions at time of writing and will change.</p>
</div>"""


def build(filename, cover_html, body_html):
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{cover_html}{body_html}{BACK}</body></html>"
    path = os.path.join(OUT, filename)
    HTML(string=html).write_pdf(path)
    return path


# ============================================================ GUIDE A
A_ITEMS = [
    ("The site decides more than the floor plan",
     "Two identical houses on two Adelaide blocks can differ by a six-figure sum. Soil classification, fall across the site, machinery access, how far services have to travel and whether you need retaining are all set before a single room is drawn. Get a builder onto the block before the design is fixed.",
     "Ask for a site assessment, not a price. You want to know what the block will cost you before you decide what to put on it."),
    ("Floor area is the number everyone watches and rarely the one that bites",
     "Clients tighten the plan by a few square metres and feel they've saved money. Meanwhile the glazing schedule, the roof form and the ceiling heights are quietly doing far more damage. Area matters, but it is a blunt lever.",
     "Before cutting rooms, ask which three line items are the largest. It is almost never the extra bedroom."),
    ("Roof form is a budget decision disguised as an aesthetic one",
     "A simple gable is cheap to frame, cheap to flash and unlikely to leak. Every additional plane, valley, box gutter and parapet adds structure, labour, waterproofing risk and future maintenance.",
     "Complex rooflines are worth paying for when they solve something. They're expensive when they're decoration."),
    ("Ceiling height ripples further than people expect",
     "Raising ceilings changes wall framing, window sizes, door heights, joinery, plasterboard sheet sizes, heating and cooling loads and often the roof structure. It's one of the most satisfying things you can spend money on, and one of the least contained.",
     "Decide early and hold it. Changing ceiling height after documentation is a redesign, not a variation."),
    ("Wet areas are the densest cost in the house",
     "Bathrooms, ensuites, laundries and kitchens concentrate plumbing, waterproofing, tiling, joinery and fixtures into small footprints. A fourth bathroom costs far more than the floor area suggests.",
     "Count wet areas early. Relocating one after the slab is poured is expensive; deciding not to have it is free."),
    ("Where you put the kitchen sets the plumbing runs for the whole house",
     "Stacking wet areas and keeping them near the sewer connection is unglamorous and saves real money. Spreading them to the four corners of the plan is a choice you pay for twice — once in installation, once in hot water performance.",
     "Ask your designer to show you where the sewer connection is on the first sketch."),
    ("Glazing is where budgets go quietly",
     "Large format, thermally broken and commercial-grade glazing behaves differently to standard residential windows: different framing, different flashings, sometimes different structure. The upgrade is rarely just the glass.",
     "Get the window schedule priced before documentation is complete, not after."),
    ("Structural spans are invisible and expensive",
     "Every metre of open span without a supporting wall is steel, and steel needs engineering, craneage and often larger footings. Open-plan is a structural decision more than a spatial one.",
     "Ask what the longest span in your design is and what it costs. The answer sometimes reshapes the plan."),
    ("Heritage overlays and council requirements are cheapest to discover first",
     "In parts of Adelaide the front elevation, materials, roof pitch and demolition are all constrained. Finding out after you have paid for a design is the most avoidable expense in this entire list.",
     "Pull the planning overlay for your address before you engage anyone. It takes minutes."),
    ("Selections made late cost more than selections made early",
     "Every undecided finish becomes a provisional sum, and provisional sums are where budgets drift. They also create ordering delays, and delays cost money in a fixed site team.",
     "Aim to have major selections resolved before construction starts, not during."),
    ("Contingency is not pessimism",
     "Older Adelaide homes hide termite history, failed damp courses, unpermitted previous work and footings that were never adequate. A contingency of ten to fifteen per cent is a normal part of a competent budget, not an admission of doubt.",
     "If a builder's number has no contingency in it, ask where the risk went. It did not disappear."),
    ("The costs outside the build contract are real",
     "Consultant fees, council and authority charges, engineering, energy reports, demolition, driveways, landscaping, window furnishings, and temporary accommodation if you move out. None of these usually sit inside a builder's contract sum, and together they are substantial.",
     "Build a project budget, not a construction budget. They are different documents."),
]

a_toc = "".join(
    f'<div class="toc-item">{i+1}. {t}<span>{i+1:02d}</span></div>\n'
    for i, (t, _, _) in enumerate(A_ITEMS))

a_items = "".join(f"""<div class="item">
  <span class="item-no">Decision {i+1:02d}</span>
  <h3>{t}</h3>
  <p>{b}</p>
  <div class="callout"><span class="label">What to do</span><p>{c}</p></div>
</div>""" for i, (t, b, c) in enumerate(A_ITEMS))

A_BODY = f"""<div class="toc">
  <div class="label">Before you brief an architect</div>
  <h2 class="first" style="margin:4mm 0 6mm">Twelve decisions.</h2>
  <div class="sec-rule"></div>
  <div class="dark-box" style="margin-top:0">
    <span class="label">Why this guide exists</span>
    <h3 style="margin-top:3mm">Most expensive mistakes are made before a builder is involved.</h3>
    <p>By the time we are asked to price a project, the decisions that set the budget have usually
    already been made — often months earlier, often without anyone realising a budget decision was
    being made at all. This guide lists the twelve that come up most often on Adelaide projects.</p>
    <p>None of them are about choosing cheaper things. They are about knowing which choices carry
    weight, so you can spend where it matters to you.</p>
  </div>
  <div class="label" style="margin-top:9mm">Contents</div>
  <div style="margin-top:3mm">{a_toc}</div>
</div>

<div class="label">Before you brief an architect</div>
<h2 class="first" style="margin:4mm 0 5mm">The twelve.</h2>
<div class="sec-rule"></div>
{a_items}

<h2>Three questions before you sign a design agreement</h2>
<div class="sec-rule"></div>
<ul class="check">
  <li>What is your budget assumption for this design, and where is it written down?</li>
  <li>At what stage will the design be costed by a builder — and what happens if it comes back over?</li>
  <li>What is included if the design needs to be revised to meet the budget, and what is charged again?</li>
</ul>
<p style="margin-top:5mm">Design agreements vary enormously on these three points. Asking early is
not distrustful; it is the same question a good designer would want you to ask.</p>

<div class="callout">
  <span class="label">One more thing</span>
  <p>Bringing a builder into the conversation before the design is locked usually reduces design
  fees rather than adding to them, because it removes at least one round of redesign. It costs
  nothing to ask.</p>
</div>"""

pa = build("Templeton-Built-Before-You-Brief-An-Architect.pdf",
           cover("Free guide for Adelaide homeowners",
                 "Before you brief an architect.",
                 "Twelve decisions that quietly set your budget long before a single trade quotes — and what each one costs you to change later.",
                 ["Templeton Built · Adelaide", "Fourth-generation builders since 2001",
                  "Licence BLD183145"]),
           A_BODY)

# ============================================================ GUIDE B
B_BODY = """<div class="toc">
  <div class="label">The Adelaide cost benchmark</div>
  <h2 class="first" style="margin:4mm 0 6mm">What's inside.</h2>
  <div class="sec-rule"></div>
  <div class="dark-box" style="margin-top:0">
    <span class="label">Read this first</span>
    <h3 style="margin-top:3mm">A rate per square metre is a starting point, not a price.</h3>
    <p>Every figure in this guide is a range, and every range is wide for a reason. Two houses of
    identical size on two Adelaide blocks can sit at opposite ends of the same range because of
    soil, access, fall, services and the condition of what is already there.</p>
    <p>Use these numbers to work out whether your project is roughly viable. Do not use them to
    choose between builders.</p>
  </div>
  <div class="label" style="margin-top:9mm">Contents</div>
  <div class="toc-item" style="margin-top:3mm">How to read these ranges<span>01</span></div>
  <div class="toc-item">Extensions<span>02</span></div>
  <div class="toc-item">Renovations<span>03</span></div>
  <div class="toc-item">Custom homes<span>04</span></div>
  <div class="toc-item">What sits outside the build contract<span>05</span></div>
  <div class="toc-item">Where provisional sums hide<span>06</span></div>
  <div class="toc-item">Comparing two quotes that aren't comparable<span>07</span></div>
</div>

<div class="label">01</div>
<h2 class="first" style="margin:4mm 0 5mm">How to read these ranges.</h2>
<div class="sec-rule"></div>
<p>The figures below reflect general Adelaide market conditions for quality residential work. They
assume a competent builder, licensed trades, compliant documentation and standard site conditions.
They are not a quote and they are not specific to your property.</p>
<p><strong>Lower end of a range</strong> generally means: flat site, straightforward access, simple
roof form, standard glazing, modest wet-area count, and finishes selected for durability rather
than statement.</p>
<p><strong>Upper end</strong> generally means: sloping or constrained site, structural complexity,
large-format or thermally broken glazing, multiple wet areas, bespoke joinery, and a specification
chosen deliberately.</p>
<p><strong>Above the range</strong> is normal for heritage-constrained sites, difficult access,
significant structural remediation, or a specification driven by an architect's material palette.
It is not a warning sign in itself.</p>

<div class="label">02</div>
<h2 style="margin:4mm 0 5mm">Extensions.</h2>
<div class="sec-rule"></div>
<table>
  <tr><th>Project type</th><th>Typical range</th><th>What moves it</th></tr>
  <tr><td class="n">Ground-floor rear addition</td><td class="n">$2,500–$4,000 / m²</td>
    <td>Site access, roof junction with existing, whether services can be extended or must be replaced</td></tr>
  <tr><td class="n">Second-storey addition</td><td class="n">$3,000–$4,500+ / m²</td>
    <td>Existing footings and structure, temporary weatherproofing, staircase location, whether you move out</td></tr>
  <tr><td class="n">Alfresco / covered outdoor</td><td class="n">Varies widely</td>
    <td>Whether it is genuinely a room (services, lighting, screening) or a roof over paving</td></tr>
</table>
<div class="callout">
  <span class="label">The line most people miss</span>
  <p>The junction between old and new is where extensions succeed or fail, both visually and
  financially. Matching floor levels, resolving the roofline and dealing with a wall that has moved
  for a century are rarely on a square-metre rate.</p>
</div>

<div class="label">03</div>
<h2 style="margin:4mm 0 5mm">Renovations.</h2>
<div class="sec-rule"></div>
<table>
  <tr><th>Project type</th><th>Typical range</th><th>What moves it</th></tr>
  <tr><td class="n">Internal renovation, single zone</td><td class="n">$60,000–$200,000</td>
    <td>Whether walls are structural, whether wet areas move, joinery specification</td></tr>
  <tr><td class="n">Kitchen and scullery</td><td class="n">Highly variable</td>
    <td>Appliance package, stone selection, whether plumbing and electrical relocate</td></tr>
  <tr><td class="n">Whole-home renovation</td><td class="n">Substantial</td>
    <td>Rewiring, replumbing, re-roofing, damp treatment, underpinning — the invisible two-thirds</td></tr>
</table>
<div class="dark-box">
  <span class="label">Older Adelaide homes</span>
  <h3 style="margin-top:3mm">Structure first, finishes second.</h3>
  <p>Rising damp, failed damp courses, inadequate footings, termite history and previous unpermitted
  work are common in Adelaide's stone housing stock. None of it is glamorous and all of it must be
  resolved before a finish is chosen. A renovation quote that goes straight to tiles and tapware has
  not looked hard enough.</p>
</div>

<div class="label">04</div>
<h2 style="margin:4mm 0 5mm">Custom homes.</h2>
<div class="sec-rule"></div>
<p>Custom home costs vary too widely for a single useful range, because the site does so much of the
deciding. What is consistent is the shape of the budget.</p>
<table>
  <tr><th>Component</th><th>Notes</th></tr>
  <tr><td class="n">Site works</td><td>Excavation, retaining, drainage, access, service connections. On a sloping or rural block this can be a significant share before a wall goes up.</td></tr>
  <tr><td class="n">Structure and shell</td><td>Footings, framing, roof, external cladding, windows. Largely set by form and span rather than finish.</td></tr>
  <tr><td class="n">Services</td><td>Hydraulic, electrical, heating and cooling. Driven by wet-area count and how far runs travel.</td></tr>
  <tr><td class="n">Fitout and joinery</td><td>Where specification has the most visible effect on the number, and the most room for you to steer it.</td></tr>
  <tr><td class="n">Rural or bushfire sites</td><td>Water storage, bushfire attack level requirements, access and power can add materially before design is considered.</td></tr>
</table>

<div class="label">05</div>
<h2 style="margin:4mm 0 5mm">What sits outside the build contract.</h2>
<div class="sec-rule"></div>
<p>These are real project costs that usually do not appear in a builder's contract sum. Budget them
separately or they will arrive as a surprise.</p>
<ul class="check">
  <li>Design, documentation and consultant fees</li>
  <li>Structural engineering and soil reports</li>
  <li>Energy efficiency assessment and certification</li>
  <li>Council and authority fees, planning and building consents</li>
  <li>Demolition and site clearing, where not in scope</li>
  <li>Driveways, paths, fencing and landscaping</li>
  <li>Window furnishings, loose furniture and appliances not in the schedule</li>
  <li>Temporary accommodation and storage if you move out</li>
  <li>Contingency of ten to fifteen per cent</li>
</ul>

<div class="label">06</div>
<h2 style="margin:4mm 0 5mm">Where provisional sums hide.</h2>
<div class="sec-rule"></div>
<p>A provisional sum is an allowance for work that cannot be priced exactly yet — usually because a
selection has not been made, or because something is still hidden behind a wall. They are legitimate
and unavoidable. They are also where budgets drift.</p>
<p>The problem is not that a quote contains provisional sums. It is that two quotes can contain very
different allowances for the same work, which makes the headline figures meaningless to compare.</p>
<div class="callout">
  <span class="label">Ask this</span>
  <p>For each provisional sum: what assumption is it based on, and what happens to the difference
  when the real invoice comes in? Under an open-book arrangement, the difference is reconciled and
  returned to you. Under others, it is not.</p>
</div>

<div class="label">07</div>
<h2 style="margin:4mm 0 5mm">Comparing two quotes that aren't comparable.</h2>
<div class="sec-rule"></div>
<p>Two builders pricing the same drawings will rarely produce comparable documents. Before you
compare the totals, compare these.</p>
<ul class="check">
  <li>Are both pricing the same documentation revision?</li>
  <li>What allowances does each carry for site works, and on what information?</li>
  <li>How many provisional sums are in each, and at what values?</li>
  <li>Is contingency included, excluded, or absent entirely?</li>
  <li>What is excluded — landscaping, driveways, window furnishings, connections?</li>
  <li>What is the builder's margin, and can you see it?</li>
  <li>What is the programme, and what happens to cost if it extends?</li>
  <li>Who carries the risk if something unexpected is found in the existing structure?</li>
</ul>
<div class="dark-box">
  <span class="label">The line that matters</span>
  <h3 style="margin-top:3mm">If you cannot see the margin, you cannot check the rest.</h3>
  <p>Every other line in a costing schedule can be verified against a quote or a rate. The builder's
  margin is the only one that is purely a decision. When it is shown plainly, you stop wondering
  whether it has been distributed quietly across the trades. When it is not shown, you never
  entirely stop wondering.</p>
</div>"""

pb = build("Templeton-Built-Adelaide-Cost-Benchmark.pdf",
           cover("Free guide for Adelaide homeowners",
                 "The Adelaide cost benchmark.",
                 "Real cost ranges for extensions, renovations and custom homes — what sits inside each figure, and what almost every quote leaves out.",
                 ["Templeton Built · Adelaide", "Fourth-generation builders since 2001",
                  "Licence BLD183145"]),
           B_BODY)

for p in (pa, pb):
    print(p, os.path.getsize(p) // 1024, "KB")
