#!/usr/bin/env python3
"""Templeton Built — static site generator.
Writes every page from shared header/footer templates so the chrome stays identical."""

import os, re

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://templetonbuilt.com.au"

IMG = {
    "stirling": "https://templetonbuilt.com.au/wp-content/uploads/2025/06/233011_blackrabbit_cmphoto_stirlingresidence_0067-Copy1-1024x683.jpg",
    "rear": "https://templetonbuilt.com.au/wp-content/uploads/2025/06/Rear-of-Home-2.jpg",
    "living": "https://templetonbuilt.com.au/wp-content/uploads/2025/06/Living-1.1.jpg",
    "kitchen": "https://templetonbuilt.com.au/wp-content/uploads/2025/05/Screen-Shot-2025-05-21-at-6.19.06-pm.png",
    "pantry": "https://templetonbuilt.com.au/wp-content/uploads/2025/06/Kitchen-Pantry-1024x686.jpg",
    "outdoor": "https://templetonbuilt.com.au/wp-content/uploads/2025/06/Outdoor-Shr-1024x686.jpg",
    "hallway": "https://templetonbuilt.com.au/wp-content/uploads/2025/06/Hallway-1024x686.jpg",
    "hawthorn": "https://templetonbuilt.com.au/wp-content/uploads/2020/05/Hawthorn-Renovation.jpg",
    "meadows": "https://templetonbuilt.com.au/wp-content/uploads/2020/05/Meadows-New-Home-1.jpg",
    "jordan": "https://templetonbuilt.com.au/ll-build/wp-content/uploads/2026/08/JordanTempleton-ProfilePhoto.png",
    "paul": "https://templetonbuilt.com.au/ll-build/wp-content/uploads/2026/08/PaulKassara-ProfilePhoto.png",
    "logo": "https://templetonbuilt.com.au/wp-content/uploads/2025/05/Templeton-Logo.png",
}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700'
         '&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300;1,6..72,400'
         '&display=swap" rel="stylesheet">')

NAVITEMS = [
    ("/projects", "Projects"),
    ("/custom-homes", "Custom homes"),
    ("/extensions", "Extensions"),
    ("/renovations", "Renovations"),
    ("/open-book", "Open book"),
    ("/about", "About"),
    ("/journal", "Journal"),
]


def head(title, desc, slug, image, extra=""):
    canon = f"{SITE}/" if slug == "index" else f"{SITE}/{slug}"
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{image}">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_AU">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="stylesheet" href="/styles.css">
{extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def nav(current="", over=False):
    cls = "nav over" if over else "nav"
    items = ""
    for href, text in NAVITEMS:
        cur = ' aria-current="page"' if href.strip("/") == current else ""
        items += f'      <a href="{href}"{cur}>{text}</a>\n'
    return f"""<nav class="{cls}" id="nav">
  <div class="wrap nav-in">
    <a href="/" class="logo" aria-label="Templeton Built home">
      <img src="{IMG['logo']}" alt="Templeton Built" width="170" height="34">
    </a>
    <button class="nav-toggle" id="toggle" aria-label="Open menu" aria-expanded="false">
      <svg width="26" height="14" viewBox="0 0 26 14" fill="none" aria-hidden="true"><path d="M0 1h26M0 13h26" stroke="currentColor" stroke-width="1.4"/></svg>
    </button>
    <div class="nav-links" id="links">
{items}      <a href="/contact" class="nav-cta">Start a conversation</a>
    </div>
  </div>
</nav>
"""


FOOTER = """<footer class="foot" id="contact-foot">
  <div class="wrap">
    <div class="foot-top">
      <div class="rev">
        <span class="label">Get in touch</span>
        <h2 style="margin-top:22px">Tell us what you're thinking of building.</h2>
      </div>
      <div class="foot-contact rev">
        <a href="tel:1800955111" class="big">1800 955 111</a>
        <a href="mailto:hello@templetonbuilt.com.au" class="big">hello@templetonbuilt.com.au</a>
        <p style="color:rgba(251,250,248,.72);margin:0">12 Stirling Street, Thebarton SA 5033<br>Monday&ndash;Friday, 7am&ndash;4pm</p>
        <a href="/contact" class="btn btn-light">Book a site conversation</a>
      </div>
    </div>

    <div class="foot-cols">
      <div>
        <h4>What we build</h4>
        <ul>
          <li><a href="/custom-homes">Custom homes</a></li>
          <li><a href="/extensions">Extensions</a></li>
          <li><a href="/renovations">Renovations</a></li>
        </ul>
      </div>
      <div>
        <h4>Studio</h4>
        <ul>
          <li><a href="/about">About Templeton Built</a></li>
          <li><a href="/open-book">The open book</a></li>
          <li><a href="/projects">Projects</a></li>
          <li><a href="/journal">Journal</a></li>
        </ul>
      </div>
      <div>
        <h4>Start here</h4>
        <ul>
          <li><a href="/architect-guide">Before you brief an architect</a></li>
          <li><a href="/cost-benchmark">Adelaide cost benchmark</a></li>
          <li><a href="/contact">Book a conversation</a></li>
        </ul>
      </div>
      <div>
        <h4>Details</h4>
        <ul>
          <li>ABN 16 067 209 161</li>
          <li>Licence BLD183145</li>
          <li><a href="https://www.instagram.com/templetonbuilt.au" rel="noopener">Instagram</a></li>
          <li><a href="https://www.facebook.com/templetonbuilt.au/" rel="noopener">Facebook</a></li>
        </ul>
      </div>
    </div>

    <div class="foot-base">
      <span>&copy; Templeton Built Pty Ltd 2026</span>
      <span>Adelaide, South Australia</span>
    </div>
  </div>
</footer>
"""

SCRIPT = """<script>
const nav=document.getElementById('nav');
if(nav){
  const onScroll=()=>nav.classList.toggle('solid',window.scrollY>60);
  onScroll();window.addEventListener('scroll',onScroll,{passive:true});
  const toggle=document.getElementById('toggle'),links=document.getElementById('links');
  toggle.addEventListener('click',()=>{
    const open=links.classList.toggle('open');
    toggle.classList.toggle('open',open);
    toggle.setAttribute('aria-expanded',open);
  });
  links.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{
    links.classList.remove('open');toggle.classList.remove('open');toggle.setAttribute('aria-expanded',false);
  }));
}
if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches){
  const io=new IntersectionObserver((es)=>es.forEach(e=>{
    if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}
  }),{threshold:.12,rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.rev').forEach(el=>io.observe(el));
}else{
  document.querySelectorAll('.rev').forEach(el=>el.classList.add('in'));
}
document.querySelectorAll('form[data-demo]').forEach(f=>f.addEventListener('submit',e=>{
  e.preventDefault();
  window.location.href = f.dataset.demo;
}));
</script>
</body>
</html>
"""


def page(slug, title, desc, body, image=None, current="", over=False, extra="", footer=True):
    image = image or IMG["stirling"]
    html = head(title, desc, slug, image, extra) + nav(current, over) + \
        f'<main id="main">\n{body}\n</main>\n' + (FOOTER if footer else "") + SCRIPT
    with open(os.path.join(OUT, f"{slug}.html"), "w") as f:
        f.write(html)
    return slug


# ---------------------------------------------------------------- components

def phero(label, h1, sub, img=None, plain=False, actions=""):
    if plain:
        return f"""<section class="phero phero-plain">
  <div class="wrap phero-in">
    <span class="label">{label}</span>
    <h1>{h1}</h1>
    <p class="phero-sub">{sub}</p>
    {actions}
  </div>
</section>"""
    return f"""<section class="phero">
  <div class="phero-img"><img src="{img}" alt=""></div>
  <div class="wrap phero-in">
    <span class="label">{label}</span>
    <h1>{h1}</h1>
    <p class="phero-sub">{sub}</p>
    {actions}
  </div>
</section>"""


def faq(items):
    rows = "".join(
        f'    <details><summary>{q}</summary><p>{a}</p></details>\n' for q, a in items)
    return f"""<section class="pad">
  <div class="wrap">
    <div class="sec-head"><span class="label">Common questions</span>
      <h2 class="rev">Things people ask<br>before they commit.</h2></div>
    <div class="faq rev">
{rows}    </div>
  </div>
</section>"""


def faq_schema(items):
    ents = ",".join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
        % (q.replace('"', "'"), re.sub("<[^>]+>", "", a).replace('"', "'")) for q, a in items)
    return ('<script type="application/ld+json">{"@context":"https://schema.org",'
            '"@type":"FAQPage","mainEntity":[%s]}</script>' % ents)


def guide_band(dark=False):
    cls = "guide dark" if dark else "guide stone"
    formcls = "card" if dark else "card"
    return f"""<section class="{cls} pad">
  <div class="wrap guide-grid">
    <div class="rev">
      <span class="label">Free guide</span>
      <h2 style="margin-top:22px">Before you brief an architect.</h2>
      <p>Twelve decisions that quietly set your budget long before a single trade quotes &mdash; and what each one costs you to change later.</p>
      <ul class="guide-list">
        <li>Why site conditions beat floor area, every time</li>
        <li>Where heritage and council overlays actually bite</li>
        <li>The five specification choices that move the number most</li>
        <li>How to read a builder's quote &mdash; and what's missing from it</li>
      </ul>
    </div>
    <form class="{formcls} rev" data-demo="/thank-you">
      <div class="field"><label for="gn">Name</label><input id="gn" name="name" required></div>
      <div class="field"><label for="ge">Email</label><input id="ge" type="email" name="email" required></div>
      <div class="two">
        <div class="field"><label for="gs">Suburb</label><input id="gs" name="suburb"></div>
        <div class="field"><label for="gp">Project</label>
          <select id="gp" name="project"><option>Custom home</option><option>Extension</option><option>Renovation</option><option>Not sure yet</option></select>
        </div>
      </div>
      <button class="btn btn-solid" type="submit">Send me the guide</button>
      <p class="fineprint">One email with the guide. No sales calls unless you ask for one.</p>
    </form>
  </div>
</section>"""


def openbook_panel():
    rows = ["Site preparation &amp; demolition", "Footings &amp; concrete",
            "Framing &amp; structural steel", "Roofing &amp; flashings",
            "Windows &amp; external doors", "Services &mdash; hydraulic, electrical",
            "Joinery &amp; internal fitout", "Trade supplier quotes"]
    r = "".join(f'        <div class="row">{x} <span>Shown</span></div>\n' for x in rows)
    return f"""<section class="dark pad" id="openbook">
  <div class="wrap">
    <div class="ob-grid">
      <div class="rev">
        <span class="label">The open book</span>
        <h2 style="margin-top:22px">Every line.<br>Including ours.</h2>
        <p>Most builders hand you a single number and ask you to trust it. We hand you the costing sheet &mdash; every trade, every allowance, every supplier quote, and our margin written plainly at the bottom.</p>
        <p>It means you can see exactly where the money is going, question anything, and make the trade-offs yourself instead of finding out about them at handover.</p>
        <a href="/open-book" class="btn btn-light" style="margin-top:14px">How we price &rarr;</a>
      </div>
      <div class="sheet rev" aria-label="Example costing schedule structure">
        <div class="sheet-head"><span>Costing schedule &mdash; extract</span><span>Visible to client</span></div>
{r}        <div class="row row-margin">Builder's margin <span>Shown</span></div>
      </div>
    </div>
  </div>
</section>"""


PROJECTS = [
    ("stirling-residence", "Stirling Residence", "Stirling", "Whole-home renovation", "stirling"),
    ("semaphore-extension", "Semaphore Extension", "Semaphore", "Rear extension", "rear"),
    ("hawthorn-renovation", "Hawthorn Renovation", "Hawthorn", "Renovation", "hawthorn"),
    ("meadows-new-home", "Meadows New Home", "Meadows", "New custom home", "meadows"),
]


def proj_card(p, lead=False):
    slug, name, suburb, scope, img = p
    cls = "proj proj-lead rev" if lead else "proj rev"
    return f"""      <a href="/projects/{slug}" class="{cls}">
        <div class="proj-img"><img src="{IMG[img]}" alt="{name}" loading="lazy"></div>
        <h3>{name}</h3>
        <div class="spec">
          <div>Suburb<b>{suburb}</b></div>
          <div>Scope<b>{scope}</b></div>
          <div>On site<b>&mdash;</b></div>
        </div>
      </a>
"""


def service_cta(title, sub):
    return f"""<section class="dark pad-sm">
  <div class="wrap" style="display:grid;grid-template-columns:1fr auto;gap:40px;align-items:center">
    <div class="rev"><h2 style="max-width:18ch">{title}</h2><p style="margin-top:18px;max-width:46ch">{sub}</p></div>
    <a href="/contact" class="btn btn-light rev">Start a conversation</a>
  </div>
</section>"""


# ================================================================= PAGES
pages = []

# ---------------------------------------------------------------- HOME
home_faq = [
    ("Do you work to a fixed price or cost-plus?",
     "Both, depending on the project. What doesn't change is that you see the full costing schedule either way &mdash; every trade, every allowance and our margin &mdash; so you know what sits behind the number you're agreeing to."),
    ("How early should we talk to you?",
     "Earlier than most people do. If you bring us in before the design is locked, we can tell you what your site and your council will allow, and which decisions are quietly setting your budget. It costs you nothing and it saves redesign fees later."),
    ("Which parts of Adelaide do you build in?",
     "Across metropolitan Adelaide and the Hills &mdash; from the coastal suburbs through to Stirling and the surrounding districts. We know the councils, the heritage overlays and the soil."),
    ("How many projects do you take on at once?",
     "Deliberately few. It's the only way Jordan can be on every site rather than managing yours from a distance."),
]

home_body = f"""<header class="hero">
  <div class="hero-img"><img src="{IMG['stirling']}" alt="Stirling residence by Templeton Built" fetchpriority="high"></div>
  <div class="wrap hero-in">
    <span class="label">Adelaide &middot; Design &amp; build &middot; Since 2001</span>
    <h1>Built in the open.</h1>
    <p class="hero-sub">Custom homes, extensions and renovations across Adelaide, from a fourth-generation family builder &mdash; with every cost on the table, including ours.</p>
    <div class="hero-actions">
      <a href="/projects" class="btn btn-light">See the work</a>
      <a href="/contact" class="btn btn-light">Start a conversation</a>
    </div>
    <div class="hero-meta">
      <span>Four generations of builders</span>
      <span>Licence BLD183145</span>
      <span>Thebarton, South Australia</span>
    </div>
  </div>
</header>

<section class="statement pad">
  <div class="wrap statement-grid">
    <p class="lede rev">Most clients arrive with a site, a plan, and a quiet worry that they're about to lose control of <em>both</em>.</p>
    <div class="statement-body rev">
      <p>Templeton Built has been designing and building across Adelaide since 2001, under the same family name for four generations. Jordan's great-grandfather was raising sheds in this city long before any of this had a website.</p>
      <p>We take on a deliberately small number of projects each year. That means Jordan is on your site and in your meetings &mdash; not a project manager you've never met, working from a spreadsheet across town.</p>
    </div>
  </div>
</section>

<section id="build">
  <div class="wrap sec-head pad-sm pad-b0">
    <span class="label">What we build</span>
    <h2 class="rev">Three things, done properly.</h2>
  </div>

  <div class="band rev">
    <div class="band-media"><img src="{IMG['kitchen']}" alt="Custom home interior" loading="lazy"></div>
    <div class="band-body">
      <span class="label">New builds</span>
      <h3>Custom homes</h3>
      <p>A house designed around how you actually live &mdash; your land, your suburb, your light. We work from a bare site or a knock-down rebuild, and take it from first concept drawings through to the day you get the keys.</p>
      <a href="/custom-homes" class="band-link">Custom homes &rarr;</a>
    </div>
  </div>

  <div class="band rev">
    <div class="band-media"><img src="{IMG['rear']}" alt="Rear extension in Semaphore" loading="lazy"></div>
    <div class="band-body">
      <span class="label">Additions</span>
      <h3>Extensions</h3>
      <p>Rear additions, second storeys and reworked floorplans for homes worth keeping. Heritage-sensitive where the street demands it, unapologetically contemporary where it doesn't.</p>
      <a href="/extensions" class="band-link">Extensions &rarr;</a>
    </div>
  </div>

  <div class="band rev">
    <div class="band-media"><img src="{IMG['living']}" alt="Renovated living space" loading="lazy"></div>
    <div class="band-body">
      <span class="label">Reworks</span>
      <h3>Renovations</h3>
      <p>Whole-home renovations of Adelaide's bluestone villas, bungalows and mid-century houses. Structure first, finishes second, and no surprises hiding in between the two.</p>
      <a href="/renovations" class="band-link">Renovations &rarr;</a>
    </div>
  </div>
</section>

<section class="white pad">
  <div class="wrap">
    <div class="sec-head"><span class="label">Selected work</span>
      <h2 class="rev">Houses we'd happily<br>take you through.</h2></div>
    <div class="work-grid">
{proj_card(PROJECTS[0], lead=True)}{proj_card(PROJECTS[1])}{proj_card(PROJECTS[2])}{proj_card(PROJECTS[3])}    </div>
    <p style="margin-top:56px"><a href="/projects" class="btn">All projects &rarr;</a></p>
  </div>
</section>

{openbook_panel()}

<section class="pad" id="people">
  <div class="wrap">
    <div class="sec-head"><span class="label">Who you'll deal with</span>
      <h2 class="rev">Jordan and Paul.</h2></div>
    <div class="people-grid">
      <div class="person rev"><img src="{IMG['jordan']}" alt="Jordan Templeton" loading="lazy">
        <h3>Jordan Templeton</h3><span class="label">General Manager / Builder</span></div>
      <div class="person rev"><img src="{IMG['paul']}" alt="Paul Kassara" loading="lazy">
        <h3>Paul Kassara</h3><span class="label">Estimator &amp; Procurement Manager</span></div>
    </div>
    <blockquote class="pull rev">&ldquo;I did my carpentry apprenticeship on these sites. I still walk every one of them.&rdquo;
      <cite class="pull-cite label">&mdash; Jordan Templeton</cite></blockquote>
    <p style="margin-top:44px"><a href="/about" class="btn">About the family &rarr;</a></p>
  </div>
</section>

{faq(home_faq)}
{guide_band()}"""

pages.append(page("index", "Templeton Built &mdash; Adelaide custom homes, extensions &amp; renovations",
                  "Fourth-generation Adelaide builder specialising in custom homes, extensions and renovations. Open-book pricing on every project — including our margin.",
                  home_body, over=True,
                  extra=faq_schema(home_faq) + """
<script type="application/ld+json">{"@context":"https://schema.org","@type":"GeneralContractor","name":"Templeton Built Pty Ltd","url":"https://templetonbuilt.com.au","telephone":"1800 955 111","address":{"@type":"PostalAddress","streetAddress":"12 Stirling Street","addressLocality":"Thebarton","addressRegion":"SA","postalCode":"5033","addressCountry":"AU"},"areaServed":"Adelaide, South Australia","foundingDate":"2001"}</script>"""))


# ---------------------------------------------------------------- SERVICES
def service_page(slug, label, h1, sub, img, intro, stages, faqs, gallery, current):
    stage_html = "".join(
        f"""    <div class="stage rev"><div class="stage-no">{i+1:02d}</div>
      <div><h3>{t}</h3></div><div><p>{d}</p></div></div>\n"""
        for i, (t, d) in enumerate(stages))
    gal = "".join(f'      <img src="{IMG[g]}" alt="" loading="lazy">\n' for g in gallery)
    body = f"""{phero(label, h1, sub, IMG[img],
        actions='<div class="hero-actions"><a href="/contact" class="btn btn-light">Start a conversation</a><a href="/projects" class="btn btn-light">See the work</a></div>')}

<section class="statement pad">
  <div class="wrap statement-grid">
    <p class="lede rev">{intro[0]}</p>
    <div class="statement-body rev">{"".join(f"<p>{p}</p>" for p in intro[1:])}</div>
  </div>
</section>

<section class="pad">
  <div class="wrap">
    <div class="sec-head"><span class="label">How it runs</span><h2 class="rev">From first conversation<br>to handover.</h2></div>
    <div class="stages">
{stage_html}    </div>
  </div>
</section>

<section class="white pad">
  <div class="wrap">
    <div class="sec-head"><span class="label">Detail</span><h2 class="rev">The parts you live with.</h2></div>
    <div class="cs-gallery rev">
{gal}    </div>
  </div>
</section>

{openbook_panel()}
{faq(faqs)}
{guide_band()}
{service_cta("Bring us in before the drawings are locked.",
             "A first conversation costs nothing and usually saves a redesign. Tell us the site and the idea, and we'll tell you honestly what's in front of you.")}"""
    return page(slug, h1 + " Adelaide &mdash; Templeton Built", sub, body,
                image=IMG[img], current=current, over=True, extra=faq_schema(faqs))


pages.append(service_page(
    "custom-homes", "Custom homes",
    "A house built around one family.",
    "Architect-led custom homes across Adelaide and the Hills, from a bare site or a knock-down rebuild — designed, costed and built by the same team.",
    "kitchen",
    ["A custom home is the only house you'll ever live in that was designed around <em>your</em> mornings.",
     "We build a small number of custom homes each year, on land our clients have usually spent a long time finding. Some come to us with a completed architectural set; others come with a survey, a budget and an idea, and we bring the design team to the table.",
     "Either way, the work starts with the site. Fall, orientation, soil classification, easements, overlays &mdash; these set more of your budget than the floor plan does, and knowing them early is what keeps a project honest."],
    [("Site and feasibility", "We walk the land with you, pull the planning overlays, and give you a realistic cost range before you spend money on documentation. If the numbers don't work, you'll hear it here."),
     ("Design and documentation", "Working with your architect or ours, we cost the design as it develops rather than at the end &mdash; so choices are made with the number in view, not against it."),
     ("The open-book contract", "You receive the full costing schedule: every trade, every provisional sum, every supplier quote and our margin. Nothing is folded into a lump you can't interrogate."),
     ("Construction", "A fixed site team, a live schedule, and a weekly walk-through with Jordan. Variations are priced and approved before work happens, never after."),
     ("Handover and beyond", "A full defects walk, all certificates and manuals, and the statutory builder's warranty. We answer the phone after handover, which is not universal in this industry.")],
    [("Do I need an architect before contacting you?",
      "No. Plenty of clients come to us first, and we'll introduce you to architects and designers whose work suits the house you're describing. Bringing a builder in early usually reduces design fees rather than adding to them."),
     ("Can you build from plans I already have?",
      "Yes. We'll review the documentation, flag anything that will be expensive or difficult to build, and cost it line by line before you commit."),
     ("How long does a custom home take?",
      "Design and approvals typically run longer than people expect, and construction depends on scale and site. We give you a stage-by-stage programme before you sign, and update it monthly."),
     ("What happens if costs move during the build?",
      "Because the schedule is open, you can see movement as it happens rather than at the end. Provisional sums are reconciled against real quotes and shown to you.")],
    ["kitchen", "meadows", "hallway", "outdoor"], "custom-homes"))

pages.append(service_page(
    "extensions", "Extensions",
    "Stay in the street. Change the house.",
    "Rear additions, second storeys and reworked floorplans for Adelaide homes worth keeping — heritage-sensitive at the front, contemporary where it counts.",
    "rear",
    ["The best extensions look like the house always intended to go that way.",
     "Most of our extension clients love where they live and have run out of room in it. The land is right, the street is right, and moving would mean buying back a worse version of what they already have.",
     "The craft is in the join &mdash; where new structure meets a hundred-year-old wall, where the roofline changes, where the old floor level doesn't quite match the new. That junction is where extensions succeed or look like an afterthought."],
    [("Feasibility on your site", "Before anything is drawn, we look at what your title, your council and your existing structure will actually allow. Heritage overlays, boundary setbacks and easements decide a lot."),
     ("Design that respects the original", "Whether the answer is a sympathetic continuation or a deliberate contrast, the decision should be made on purpose. We work through it with you and your designer."),
     ("Investigation before pricing", "We open up walls, check footings and confirm what's behind the plaster before we price it. Guessing here is how extensions blow out."),
     ("Open-book costing", "You see the full schedule, including allowances for the unknowns that old houses hide. Contingency is named, not buried."),
     ("Living through it", "Where possible we stage the work so you can stay in the house. Dust barriers, sequenced services and a site that gets swept at the end of every day.")],
    [("Can we live in the house during the extension?",
      "Often yes, depending on scope and whether kitchen or bathroom services are affected. We'll tell you honestly at feasibility stage, including the weeks that will be genuinely unpleasant."),
     ("How do you handle heritage overlays?",
      "We deal with Adelaide councils regularly and know where they hold firm. Getting the front elevation and materials right early avoids a costly round of amended plans."),
     ("What if you find something unexpected in the old structure?",
      "It happens with older homes — footings, termite history, asbestos, previous unpermitted work. Because we investigate before pricing and carry named allowances, discoveries change the schedule rather than blindsiding the budget."),
     ("Do you do second storeys on older homes?",
      "Yes, subject to the existing footings and structure. That assessment is part of feasibility, and we'd rather tell you it isn't viable than find out halfway up.")],
    ["rear", "living", "outdoor", "hallway"], "extensions"))

pages.append(service_page(
    "renovations", "Renovations",
    "Bluestone outside. This century inside.",
    "Whole-home renovations of Adelaide's villas, bungalows and mid-century houses — structure first, finishes second, and nothing hidden in between.",
    "living",
    ["Adelaide has some of the best housing stock in the country. Most of it was built for a life nobody lives any more.",
     "A whole-home renovation is the hardest work we do. You're threading new services through solid stone, correcting a century of settlement, and doing it without losing the reason you bought the house.",
     "We sequence it structure-first: footings, framing, waterproofing and services all resolved before a single finish is chosen. It's the least glamorous order of operations and the only one that lasts."],
    [("Condition assessment", "A proper look at what you've bought: footings, damp, roof structure, wiring, previous work. You get a written picture before you commit to a scope."),
     ("Scope and priorities", "We help you separate what must be done from what you want done, and what can wait for a second stage without wasting money."),
     ("Structure and services first", "Underpinning, damp treatment, re-roofing, rewiring and plumbing. Unglamorous, expensive, and the reason the finishes stay looking good."),
     ("Joinery and finishes", "Kitchens, sculleries, bathrooms and built-in joinery, made to suit the proportions of the original rooms rather than fighting them."),
     ("Reconciliation and handover", "Every provisional sum reconciled against real invoices, shown to you, with the balance returned rather than absorbed.")],
    [("Should we renovate or knock down and rebuild?",
      "Sometimes rebuilding is the honest answer, and we'll say so. It usually comes down to the condition of the existing structure, what the planning overlay allows and how much of the original you actually want to keep."),
     ("Can a renovation be staged?",
      "Yes, and for many homes it should be. We plan stage one so it doesn't have to be undone later — services roughed in, structure resolved, so stage two is finishes rather than demolition."),
     ("How do you deal with damp in bluestone and stone homes?",
      "Rising damp is common in Adelaide's older stone housing. The fix depends on the cause — ground levels, failed damp course, sealed render trapping moisture — so we diagnose before quoting a treatment."),
     ("Will the renovation match the original detailing?",
      "Where you want it to. We can match cornices, skirtings and joinery profiles, or draw a clear line between old and new. Both work; the mistake is doing it accidentally.")],
    ["living", "pantry", "hallway", "hawthorn"], "renovations"))


# ---------------------------------------------------------------- PROJECTS INDEX
proj_cards = proj_card(PROJECTS[0], lead=True) + "".join(proj_card(p) for p in PROJECTS[1:])
pages.append(page("projects", "Projects &mdash; Templeton Built Adelaide",
                  "Selected custom homes, extensions and renovations built by Templeton Built across Adelaide and the Adelaide Hills.",
                  f"""{phero("Selected work", "Every house here has a person we still talk to.",
        "A small sample of the homes we've designed and built across Adelaide. We're happy to walk you through any of them, and to put you in touch with the people who live there.", plain=True)}

<section class="pad pad-t0">
  <div class="wrap">
    <div class="work-grid">
{proj_cards}    </div>
  </div>
</section>
{openbook_panel()}
{guide_band()}""", current="projects"))

# ---------------------------------------------------------------- CASE STUDIES
os.makedirs(os.path.join(OUT, "projects"), exist_ok=True)

CASES = {
    "stirling-residence": dict(
        name="Stirling Residence", suburb="Stirling", scope="Whole-home renovation",
        era="1920s stone residence", hero="stirling",
        lede="A substantial stone home in the Hills that had been renovated twice before, badly, and needed the previous work undone before anything new could go in.",
        body=[("The brief", "The owners had lived in the house for several years and knew exactly what didn't work: a kitchen tucked into the darkest corner of the plan, bedrooms that opened off each other, and a rear addition from the 1980s that turned its back on the garden."),
              ("What we found", "Behind the plaster, two earlier renovations had left services running in places nobody would design them, and structural work that had never been certified. Before we could talk about finishes, that had to be corrected and documented."),
              ("The work", "We removed the later addition entirely, corrected and underpinned where the structure required it, and rebuilt the rear of the house to open to the north. Original rooms at the front were restored rather than reinvented — cornices, joinery profiles and fireplaces retained and repaired."),
              ("The result", "The front of the house reads as it always did from the street. The back is unmistakably contemporary, and every room now gets light for some part of the day.")],
        gallery=["stirling", "hallway", "living", "outdoor"]),
    "semaphore-extension": dict(
        name="Semaphore Extension", suburb="Semaphore", scope="Rear extension and alfresco",
        era="Coastal cottage", hero="rear",
        lede="A coastal cottage with a growing family in it, a deep block behind it, and nowhere to put anybody.",
        body=[("The brief", "Keep the cottage frontage exactly as the street knows it, and put the family's real living space at the rear, opening to a garden that had never been used properly."),
              ("The constraint", "Coastal exposure changes the specification. Fixings, flashings, glazing and external finishes all have to be selected for salt air, and the difference between doing that properly and not shows up within five years."),
              ("The work", "A rear addition with a covered alfresco that works as a genuine second living room rather than a paved afterthought. Sightlines were set so the kitchen bench looks straight down the yard."),
              ("The result", "The house gained the space without losing the character that made them buy it, and the family stayed in the street they wanted their kids to grow up in.")],
        gallery=["rear", "outdoor", "pantry", "living"]),
    "hawthorn-renovation": dict(
        name="Hawthorn Renovation", suburb="Hawthorn", scope="Whole-home renovation",
        era="Established character home", hero="hawthorn",
        lede="A character home in one of Adelaide's established eastern suburbs, reworked internally while the street elevation stayed exactly where it was.",
        body=[("The brief", "Modernise how the house functions without touching what makes it belong on the street."),
              ("The approach", "Almost all the change happened behind the front rooms. Circulation was rationalised, wet areas relocated to where services could sensibly run, and the rear opened up."),
              ("The work", "Structural changes to remove load-bearing walls, full re-service, and new joinery detailed to the proportions of the original rooms."),
              ("The result", "From the footpath, nothing has changed. Inside, the house works the way a house built this century would.")],
        gallery=["hawthorn", "pantry", "hallway", "living"]),
    "meadows-new-home": dict(
        name="Meadows New Home", suburb="Meadows", scope="New custom home",
        era="New build on rural land", hero="meadows",
        lede="A new home on rural land, where the site did most of the deciding.",
        body=[("The brief", "A house that suited the way the land sat, rather than a plan dropped onto it. Orientation, prevailing wind and the view were the starting point."),
              ("The site", "Rural sites bring their own budget: access, services, soil, water and bushfire requirements can account for a meaningful share of the cost before a wall goes up. All of it was on the schedule from the beginning."),
              ("The work", "Designed and built with the living spaces oriented to the north and the working parts of the house buffering the weather side."),
              ("The result", "A home that reads as though it grew out of the paddock rather than arriving on a truck.")],
        gallery=["meadows", "kitchen", "outdoor", "hallway"]),
}

for slug, c in CASES.items():
    others = "".join(proj_card(p) for p in PROJECTS if p[0] != slug)
    body_html = "".join(f"<h2>{h}</h2><p>{t}</p>" for h, t in c["body"])
    gal = "".join(f'      <img src="{IMG[g]}" alt="{c["name"]}" loading="lazy">\n'
                  for g in c["gallery"])
    inner = f"""{phero(f'{c["scope"]} &middot; {c["suburb"]}', c["name"], c["lede"], IMG[c["hero"]])}

<section class="pad-sm">
  <div class="wrap">
    <div class="cs-facts">
      <div class="cs-fact"><span class="label">Suburb</span><b>{c["suburb"]}</b></div>
      <div class="cs-fact"><span class="label">Scope</span><b>{c["scope"]}</b></div>
      <div class="cs-fact"><span class="label">Home</span><b>{c["era"]}</b></div>
      <div class="cs-fact"><span class="label">On site</span><b>&mdash;</b></div>
    </div>
  </div>
</section>

<section class="pad-sm pad-t0">
  <div class="wrap-narrow">
    <div class="prose rev">{body_html}</div>
  </div>
</section>

<section class="pad-sm">
  <div class="wrap"><div class="cs-gallery rev">
{gal}  </div></div>
</section>

<section class="white pad">
  <div class="wrap">
    <div class="sec-head"><span class="label">More work</span><h2 class="rev">Other projects.</h2></div>
    <div class="work-grid">
{others}    </div>
  </div>
</section>
{service_cta("Want to see this one in person?",
             "We can usually arrange a walk-through of a completed home, and put you in touch with the owners. It is the most useful hour you will spend choosing a builder.")}"""
    html = head(f'{c["name"]} &mdash; Templeton Built',
                c["lede"], f"projects/{slug}", IMG[c["hero"]]) + nav("projects", over=True) + \
        f'<main id="main">\n{inner}\n</main>\n' + FOOTER + SCRIPT
    html = html.replace('href="/styles.css"', 'href="/styles.css"')
    with open(os.path.join(OUT, "projects", f"{slug}.html"), "w") as f:
        f.write(html)
    pages.append(f"projects/{slug}")

# ---------------------------------------------------------------- OPEN BOOK
ob_faq = [
    ("Doesn't showing your margin invite clients to negotiate it down?",
     "Occasionally. More often it ends the conversation about margin altogether, because you can see it's reasonable and you stop wondering what's hidden in the other numbers."),
    ("What is a provisional sum, and why does it matter?",
     "It's an allowance for work that can't be priced exactly yet — often because a selection hasn't been made or something is still hidden. Under an open book, every provisional sum is reconciled against the real invoice and the difference goes back to you."),
    ("How is this different from a fixed-price contract?",
     "It isn't an alternative to one. You can still have a fixed price. The difference is that you can see the schedule that produced it, so you know which parts are firm and which carry allowances."),
    ("Do other Adelaide builders do this?",
     "Some do parts of it. Showing the margin line itself is rarer, and it's the line that matters, because it's the one clients assume is being padded."),
]
pages.append(page("open-book", "The open book &mdash; how Templeton Built prices",
                  "Open-book pricing explained: the full costing schedule, every trade, every provisional sum, and the builder's margin shown plainly.",
                  f"""{phero("How we price", "You should be able to read the number, not just accept it.",
        "Open-book pricing means you receive the complete costing schedule for your project — every trade, every allowance, every supplier quote, and our margin written on the page.", plain=True)}

{openbook_panel()}

<section class="pad">
  <div class="wrap">
    <div class="sec-head"><span class="label">What you receive</span><h2 class="rev">Four documents,<br>and the right to question all of them.</h2></div>
    <div class="stages">
      <div class="stage rev"><div class="stage-no">01</div><div><h3>The costing schedule</h3></div>
        <div><p>Line by line, trade by trade. Every item carries the quote or rate behind it, so you can see what a number is made of rather than taking it on faith.</p></div></div>
      <div class="stage rev"><div class="stage-no">02</div><div><h3>Named allowances</h3></div>
        <div><p>Where something genuinely can't be priced yet, it's shown as a provisional sum with the assumption written next to it &mdash; not folded quietly into a larger figure.</p></div></div>
      <div class="stage rev"><div class="stage-no">03</div><div><h3>Our margin</h3></div>
        <div><p>Stated as its own line. You know what we're making on your house, which means you never have to wonder whether it's buried somewhere else.</p></div></div>
      <div class="stage rev"><div class="stage-no">04</div><div><h3>Monthly reconciliation</h3></div>
        <div><p>As real invoices land, allowances are reconciled against them and the schedule is reissued. Savings go back to you rather than being absorbed.</p></div></div>
    </div>
  </div>
</section>

<section class="stone pad">
  <div class="wrap-narrow">
    <blockquote class="pull rev" style="max-width:30ch">&ldquo;People don't distrust builders because of the price. They distrust them because they can't see how it was arrived at.&rdquo;
      <cite class="pull-cite label">&mdash; Jordan Templeton</cite></blockquote>
  </div>
</section>

{faq(ob_faq)}
{guide_band()}""", current="open-book", extra=faq_schema(ob_faq)))

# ---------------------------------------------------------------- ABOUT
pages.append(page("about", "About Templeton Built &mdash; four generations of Adelaide builders",
                  "Templeton Built is a family building company in Thebarton, South Australia — four generations of builders, led by Jordan Templeton.",
                  f"""{phero("About", "Four generations, one city.", "Templeton Built is a family building company in Thebarton. Jordan is the fourth generation of his family to build in Adelaide, and the work still carries the family name for a reason.", IMG['hallway'])}

<section class="pad">
  <div class="wrap-narrow">
    <div class="prose rev">
      <p class="lede" style="color:var(--bluestone);margin-bottom:1.4em">Jordan's great-grandfather, Peter Wyten, was raising sheds across Adelaide with his sons. That's where this starts.</p>
      <p>The business Jordan runs today began as a property development company founded by his father. Jordan completed a carpentry apprenticeship, worked every part of the business from the tools through to project management, and gradually turned it toward what it is now: a builder of custom homes, extensions and renovations across metropolitan Adelaide and the Hills.</p>
      <h2>Why the company is deliberately small</h2>
      <p>We take on a limited number of projects each year. That isn't modesty &mdash; it's the only structure in which Jordan can genuinely be on every site. A larger operation would mean handing your build to a project manager you met once at contract signing.</p>
      <p>It also means we're selective, and occasionally we'll tell you we're not the right builder for a project. That's a better outcome for everyone than taking work we can't give proper attention.</p>
      <h2>What we're actually good at</h2>
      <p><strong>Old houses.</strong> Adelaide's stone villas, bungalows and character homes behave differently to new construction, and the difference between a builder who's worked on a hundred of them and one who hasn't shows up in the first fortnight.</p>
      <p><strong>Complicated sites.</strong> Fall, access, heritage overlays, neighbours, soil. The constraints that make architects interested tend to be the ones that make builders nervous.</p>
      <p><strong>Telling you the truth about money.</strong> Which is what the open book is for.</p>
      <blockquote>We'd rather lose a job at the quoting stage than lose your trust at the framing stage.</blockquote>
    </div>
  </div>
</section>

<section class="white pad">
  <div class="wrap">
    <div class="sec-head"><span class="label">Who you'll deal with</span><h2 class="rev">Jordan and Paul.</h2></div>
    <div class="people-grid">
      <div class="person rev"><img src="{IMG['jordan']}" alt="Jordan Templeton" loading="lazy">
        <h3>Jordan Templeton</h3><span class="label">General Manager / Builder</span>
        <p class="muted" style="margin-top:14px;font-size:1rem">Qualified carpenter, licensed builder, and the person who will walk your site each week. Jordan handles design liaison, costing and construction.</p></div>
      <div class="person rev"><img src="{IMG['paul']}" alt="Paul Kassara" loading="lazy">
        <h3>Paul Kassara</h3><span class="label">Estimator &amp; Procurement Manager</span>
        <p class="muted" style="margin-top:14px;font-size:1rem">Paul prices and procures every Templeton Built project. He builds the costing schedule you receive, and holds the supplier quotes that sit behind every line of it.</p></div>
    </div>
  </div>
</section>

<section class="dark pad-sm">
  <div class="wrap">
    <div class="stats">
      <div class="stat rev"><b>4</b><span>Generations of builders</span></div>
      <div class="stat rev"><b>2001</b><span>Trading as Templeton Built</span></div>
      <div class="stat rev"><b>BLD183145</b><span>Building licence</span></div>
      <div class="stat rev"><b>SA</b><span>Adelaide &amp; the Hills</span></div>
    </div>
  </div>
</section>

{guide_band()}
{service_cta("Come and meet us.", "Most good projects start with a coffee and a set of drawings on a table. No obligation, no quote pressure.")}""",
                  image=IMG['hallway'], current="about", over=True))

# ---------------------------------------------------------------- JOURNAL
POSTS = [
    ("what-sets-a-build-budget", "What actually sets your build budget", "Costing",
     "Floor area is the number everyone fixates on. It's rarely the one doing the damage.", "pantry",
     [("Area is a poor proxy for cost", "Two homes of identical size on two different Adelaide sites can differ enormously in cost. The variables that move the number hardest are the ones you can't see on a floor plan: soil classification, fall across the site, access for machinery, and how far services have to travel."),
      ("Site works are the quiet line item", "Retaining, excavation, drainage and driveway access on a sloping block can consume a meaningful share of a budget before a single wall is framed. On flat sand in the western suburbs, the same house costs materially less to get out of the ground."),
      ("Specification compounds", "A single decision — say, moving from standard aluminium windows to thermally broken commercial glazing — doesn't just cost more per unit. It changes the framing, the flashing details and sometimes the structure. The good news is the reverse is also true: one or two well-chosen downgrades can fund something you care about more."),
      ("What to do about it", "Get a builder to look at your site before the design is finalised. It is the cheapest hour in the entire process and it routinely saves a redesign.")]),
    ("renovate-or-rebuild", "Renovate or knock down and rebuild?", "Decisions",
     "The honest answer depends on four things, and sentiment is only one of them.", "hawthorn",
     [("What condition is the existing structure in?", "Footings, roof structure, damp history and previous unpermitted work all matter more than the appearance of the house. A beautiful home sitting on failing footings can be more expensive to save than to replace."),
      ("What does the planning overlay allow?", "In parts of Adelaide, demolition simply isn't on the table, or a rebuild would come with constraints tighter than what you already have. This is the first thing to check, not the last."),
      ("How much of the original do you actually want?", "Some people want the rooms; others want the facade and nothing behind it. Being honest about this early prevents paying to retain things you don't value."),
      ("What is the street worth?", "In established suburbs, the character of the existing home is part of the value. In others, it isn't. That calculation is different in Hawthorn than it is on a new subdivision.")]),
    ("living-through-a-renovation", "Living through a renovation without losing your mind", "On site",
     "Sometimes staying put is the right call. Here's what it actually involves.", "living",
     [("Decide honestly whether you can", "The question isn't whether it's possible — it usually is. It's whether you can tolerate six to nine months of it. Households with small children, shift workers and anyone working from home should think hard."),
      ("The services are the pinch point", "You can live without a formal living room for a long time. You cannot live without a functioning bathroom or a way to cook. Good staging protects those two things for as long as possible and compresses the gap when it comes."),
      ("Set the site rules up front", "Start times, access routes, where trades park, whether the dog can be in the yard. Agreeing this in week one prevents most of the friction that builds over a long job."),
      ("Budget for a fortnight away", "There is almost always a two-week window that is genuinely miserable. Planning to be elsewhere for it is money well spent.")]),
]

post_cards = "".join(f"""      <a href="/journal/{s}" class="post rev">
        <div class="post-img"><img src="{IMG[img]}" alt="{t}" loading="lazy"></div>
        <span class="label" style="margin-top:18px">{cat}</span>
        <h3>{t}</h3><p>{d}</p>
      </a>
""" for s, t, cat, d, img, _ in POSTS)

pages.append(page("journal", "Journal &mdash; Templeton Built",
                  "Notes on building, renovating and extending in Adelaide, from a fourth-generation builder.",
                  f"""{phero("Journal", "Notes from the site.", "What we've learned building in Adelaide — written for people about to spend a significant amount of money and wanting to spend it well.", plain=True)}

<section class="pad pad-t0">
  <div class="wrap"><div class="posts">
{post_cards}  </div></div>
</section>
{guide_band()}""", current="journal"))

os.makedirs(os.path.join(OUT, "journal"), exist_ok=True)
for s, t, cat, d, img, sections in POSTS:
    body_html = "".join(f"<h2>{h}</h2><p>{p}</p>" for h, p in sections)
    more = "".join(f"""      <a href="/journal/{s2}" class="post rev">
        <div class="post-img"><img src="{IMG[i2]}" alt="{t2}" loading="lazy"></div>
        <span class="label" style="margin-top:18px">{c2}</span><h3>{t2}</h3><p>{d2}</p></a>
""" for s2, t2, c2, d2, i2, _ in POSTS if s2 != s)
    inner = f"""{phero(cat, t, d, IMG[img])}

<section class="pad">
  <div class="wrap-narrow"><div class="prose rev">{body_html}
    <p><strong>Thinking about a project?</strong> A first conversation with us costs nothing and is usually more useful than another evening on Pinterest. <a href="/contact" style="border-bottom:1px solid var(--rule)">Get in touch</a>.</p>
  </div></div>
</section>

<section class="white pad">
  <div class="wrap"><div class="sec-head"><span class="label">More reading</span><h2 class="rev">Also in the journal.</h2></div>
  <div class="posts">
{more}  </div></div>
</section>
{guide_band()}"""
    html = head(f"{t} &mdash; Templeton Built", d, f"journal/{s}", IMG[img],
                extra=('<script type="application/ld+json">{"@context":"https://schema.org",'
                       '"@type":"Article","headline":"%s","author":{"@type":"Organization","name":"Templeton Built"},'
                       '"publisher":{"@type":"Organization","name":"Templeton Built"}}</script>' % t)) + \
        nav("journal", over=True) + f'<main id="main">\n{inner}\n</main>\n' + FOOTER + SCRIPT
    with open(os.path.join(OUT, "journal", f"{s}.html"), "w") as f:
        f.write(html)
    pages.append(f"journal/{s}")

# ---------------------------------------------------------------- CONTACT
pages.append(page("contact", "Contact Templeton Built &mdash; Adelaide builder",
                  "Talk to Jordan or Paul about your custom home, extension or renovation in Adelaide. 1800 955 111.",
                  f"""{phero("Contact", "Tell us what you're thinking of building.", "No quote pressure and no sales script. Tell us the site and the idea, and we'll tell you honestly what's in front of you.", plain=True)}

<section class="pad pad-t0">
  <div class="wrap guide-grid">
    <div class="rev">
      <h3 style="margin-bottom:24px">Straight to us</h3>
      <p><a href="tel:1800955111" style="font-family:var(--display);font-size:1.8rem;font-weight:500;letter-spacing:-.03em">1800 955 111</a></p>
      <p><a href="mailto:hello@templetonbuilt.com.au" style="border-bottom:1px solid var(--rule)">hello@templetonbuilt.com.au</a></p>
      <p class="muted">12 Stirling Street<br>Thebarton SA 5033<br>Monday&ndash;Friday, 7am&ndash;4pm</p>
      <div class="cs-facts" style="grid-template-columns:1fr 1fr;margin-top:36px">
        <div class="cs-fact"><span class="label">Licence</span><b>BLD183145</b></div>
        <div class="cs-fact"><span class="label">ABN</span><b>16 067 209 161</b></div>
      </div>
      <p class="muted" style="margin-top:32px;font-size:1rem">We generally reply within one business day. If your project is urgent, call &mdash; someone answers.</p>
    </div>

    <form class="card card-stone rev" data-demo="/thank-you">
      <div class="two">
        <div class="field"><label for="cf">First name</label><input id="cf" name="first" required></div>
        <div class="field"><label for="cl">Last name</label><input id="cl" name="last" required></div>
      </div>
      <div class="field"><label for="ce">Email</label><input id="ce" type="email" name="email" required></div>
      <div class="field"><label for="cp">Phone</label><input id="cp" type="tel" name="phone"></div>
      <div class="two">
        <div class="field"><label for="cs">Project suburb</label><input id="cs" name="suburb"></div>
        <div class="field"><label for="ct">Project type</label>
          <select id="ct" name="type"><option>Custom home</option><option>Extension</option><option>Renovation</option><option>Not sure yet</option></select></div>
      </div>
      <div class="field"><label for="cst">Where you're up to</label>
        <select id="cst" name="stage">
          <option>Just an idea</option><option>Have a site, no design</option>
          <option>Working with a designer or architect</option><option>Documentation complete, ready to price</option>
        </select></div>
      <div class="field"><label for="cm">Tell us about the project</label><textarea id="cm" name="message" rows="4"></textarea></div>
      <button class="btn btn-solid" type="submit">Send it through</button>
      <p class="fineprint">Goes straight to Jordan and Paul. We don't add you to anything.</p>
    </form>
  </div>
</section>""", current="contact"))

# ---------------------------------------------------------------- LEAD MAGNETS (2, for testing)
def magnet(slug, label, h1, sub, bullets, img, kicker, cover_note):
    lis = "".join(f"      <li>{b}</li>\n" for b in bullets)
    body = f"""<section class="lp-hero">
  <div class="lp-hero-img"><img src="{IMG[img]}" alt=""></div>
  <div class="wrap lp-grid">
    <div>
      <span class="label" style="color:rgba(251,250,248,.72)">{label}</span>
      <h1 style="margin-top:22px">{h1}</h1>
      <p class="phero-sub">{sub}</p>
      <ul class="lp-points">
{lis}      </ul>
      <p class="fineprint" style="color:var(--zinc);margin-top:28px">{cover_note}</p>
    </div>
    <form class="card rev" data-demo="/thank-you">
      <h3 style="margin-bottom:6px">{kicker}</h3>
      <p class="fineprint" style="margin-bottom:12px">Sent straight to your inbox.</p>
      <div class="field"><label for="mn">Name</label><input id="mn" name="name" required></div>
      <div class="field"><label for="me">Email</label><input id="me" type="email" name="email" required></div>
      <div class="two">
        <div class="field"><label for="ms">Suburb</label><input id="ms" name="suburb"></div>
        <div class="field"><label for="mp">Project</label>
          <select id="mp" name="project"><option>Custom home</option><option>Extension</option><option>Renovation</option><option>Not sure yet</option></select></div>
      </div>
      <button class="btn btn-solid" type="submit">Send me the guide</button>
      <p class="fineprint">One email with the guide. No sales calls unless you ask for one.</p>
    </form>
  </div>
</section>

<div class="lp-trust">
  <span>Fourth-generation Adelaide builder</span><span>Licence BLD183145</span>
  <span>Open-book pricing</span><span>Since 2001</span>
</div>

<section class="pad">
  <div class="wrap-narrow">
    <div class="prose rev">
      <h2>Who wrote it</h2>
      <p>Jordan Templeton is a fourth-generation Adelaide builder and a qualified carpenter. Templeton Built designs and builds custom homes, extensions and renovations across metropolitan Adelaide and the Hills, and prices every project open-book &mdash; the full costing schedule, including our margin.</p>
      <p>This guide exists because most of the expensive mistakes we see were made months before anyone contacted a builder.</p>
    </div>
  </div>
</section>
{openbook_panel()}"""
    return page(slug, h1 + " &mdash; Templeton Built", sub, body, image=IMG[img], over=True)


pages.append(magnet(
    "architect-guide", "Free guide &middot; Test A",
    "Before you brief an architect.",
    "Twelve decisions that quietly set your budget long before a single trade quotes — and what each one costs you to change later.",
    ["Why site conditions beat floor area, every time",
     "Where Adelaide heritage and council overlays actually bite",
     "The five specification choices that move the number most",
     "How to read a builder's quote — and what's missing from it",
     "The three questions to ask before you sign a design agreement"],
    "hallway", "Get the guide",
    "Written for people planning a significant home project in Adelaide."))

pages.append(magnet(
    "cost-benchmark", "Free guide &middot; Test B",
    "The Adelaide cost benchmark.",
    "Real cost ranges for custom homes, extensions and renovations across Adelaide — what sits inside each figure, and what almost every quote leaves out.",
    ["Current cost ranges by project type and suburb profile",
     "What's genuinely included in a builder's square-metre rate",
     "The site costs that land before a wall goes up",
     "Where provisional sums hide, and how to reconcile them",
     "A checklist for comparing two quotes that aren't comparable"],
    "pantry", "Get the benchmark",
    "Figures reflect current Adelaide market conditions and are updated each year."))

# ---------------------------------------------------------------- THANK YOU
pages.append(page("thank-you", "Thanks &mdash; Templeton Built",
                  "Your guide is on its way.",
                  f"""{phero("Sent", "It's on its way.", "Check your inbox in the next minute or two. If it hasn't landed, look in promotions or spam — and if it still hasn't, call us on 1800 955 111 and we'll send it directly.", plain=True)}

<section class="pad pad-t0">
  <div class="wrap">
    <div class="sec-head"><span class="label">While you're here</span><h2 class="rev">Worth a look.</h2></div>
    <div class="posts">
      <a href="/open-book" class="post rev"><div class="post-img"><img src="{IMG['kitchen']}" alt="" loading="lazy"></div>
        <span class="label" style="margin-top:18px">How we price</span><h3>The open book</h3>
        <p>The full costing schedule, every allowance, and our margin on the page.</p></a>
      <a href="/projects" class="post rev"><div class="post-img"><img src="{IMG['stirling']}" alt="" loading="lazy"></div>
        <span class="label" style="margin-top:18px">Selected work</span><h3>Projects</h3>
        <p>Homes we've built across Adelaide and the Hills, with the detail behind them.</p></a>
      <a href="/journal" class="post rev"><div class="post-img"><img src="{IMG['living']}" alt="" loading="lazy"></div>
        <span class="label" style="margin-top:18px">Journal</span><h3>Notes from the site</h3>
        <p>What actually sets a budget, and whether to renovate or rebuild.</p></a>
    </div>
  </div>
</section>""", extra='<meta name="robots" content="noindex">'))

# ---------------------------------------------------------------- AD LANDING PAGES
def landing(slug, label, h1, sub, points, img, faqs, proof):
    lis = "".join(f"      <li>{p}</li>\n" for p in points)
    fq = "".join(f'    <details><summary>{q}</summary><p>{a}</p></details>\n' for q, a in faqs)
    body = f"""<header class="lp-nav">
  <div class="wrap lp-nav-in">
    <a href="/" class="logo"><img src="{IMG['logo']}" alt="Templeton Built"></a>
    <a href="tel:1800955111" class="lp-phone">1800 955 111</a>
  </div>
</header>

<section class="lp-hero">
  <div class="lp-hero-img"><img src="{IMG[img]}" alt=""></div>
  <div class="wrap lp-grid">
    <div>
      <span class="label" style="color:rgba(251,250,248,.72)">{label}</span>
      <h1 style="margin-top:22px">{h1}</h1>
      <p class="phero-sub">{sub}</p>
      <ul class="lp-points">
{lis}      </ul>
    </div>
    <form class="card rev" data-demo="/thank-you">
      <h3 style="margin-bottom:4px">Start a conversation</h3>
      <p class="fineprint" style="margin-bottom:12px">Goes straight to Jordan and Paul. No sales script.</p>
      <div class="field"><label for="ln">Name</label><input id="ln" name="name" required></div>
      <div class="two">
        <div class="field"><label for="le">Email</label><input id="le" type="email" name="email" required></div>
        <div class="field"><label for="lp2">Phone</label><input id="lp2" type="tel" name="phone" required></div>
      </div>
      <div class="two">
        <div class="field"><label for="ls">Project suburb</label><input id="ls" name="suburb"></div>
        <div class="field"><label for="lst">Where you're up to</label>
          <select id="lst" name="stage"><option>Just an idea</option><option>Have a site, no design</option>
          <option>Working with a designer</option><option>Ready to price</option></select></div>
      </div>
      <div class="field"><label for="lm">Tell us about the project</label><textarea id="lm" name="message" rows="3"></textarea></div>
      <button class="btn btn-solid" type="submit">Request a conversation</button>
      <p class="fineprint">We reply within one business day.</p>
    </form>
  </div>
</section>

<div class="lp-trust">
  <span>Fourth-generation Adelaide builder</span><span>Licence BLD183145</span>
  <span>Open-book pricing</span><span>Since 2001</span>
</div>

<section class="pad-sm">
  <div class="wrap">
    <div class="sec-head"><span class="label">Recent work</span><h2 class="rev">{proof}</h2></div>
    <div class="cs-gallery rev">
      <img src="{IMG[img]}" alt="" loading="lazy"><img src="{IMG['hallway']}" alt="" loading="lazy">
    </div>
  </div>
</section>

{openbook_panel()}
{faq(faqs)}

<section class="stone pad-sm">
  <div class="wrap" style="display:grid;grid-template-columns:1fr auto;gap:36px;align-items:center">
    <div class="rev"><h2 style="max-width:20ch">Talk to the builder, not a call centre.</h2>
      <p class="muted" style="margin-top:16px;max-width:44ch">Jordan or Paul will call you back personally.</p></div>
    <a href="tel:1800955111" class="btn btn-solid rev">Call 1800 955 111</a>
  </div>
</section>

<footer class="foot"><div class="wrap"><div class="foot-base" style="border:0;padding:34px 0">
  <span>&copy; Templeton Built Pty Ltd &middot; ABN 16 067 209 161 &middot; Licence BLD183145</span>
  <span>12 Stirling Street, Thebarton SA 5033</span>
</div></div></footer>"""
    html = head(h1 + " &mdash; Templeton Built", sub, slug, IMG[img],
                extra='<meta name="robots" content="noindex,follow">' + faq_schema(faqs)) + \
        f'<main id="main">\n{body}\n</main>\n' + SCRIPT
    with open(os.path.join(OUT, f"{slug}.html"), "w") as f:
        f.write(html)
    return slug


pages.append(landing(
    "lp-extensions", "Home extensions &middot; Adelaide",
    "Extend the house. Keep the street.",
    "Rear additions, second storeys and reworked floorplans for Adelaide homes worth keeping — from a fourth-generation family builder.",
    ["We investigate before we price, so old houses don't blow the budget",
     "Full open-book costing — every trade, every allowance, our margin included",
     "Jordan on your site weekly, not a project manager you've never met",
     "Heritage overlays and Adelaide councils handled routinely"],
    "rear",
    [("Can we stay in the house during the work?", "Often yes, depending on scope and whether kitchen or bathroom services are affected. We'll tell you honestly at feasibility stage."),
     ("How do you handle heritage overlays?", "We deal with Adelaide councils regularly. Getting the front elevation and materials right early avoids a costly round of amended plans."),
     ("What if something unexpected turns up in the old structure?", "We open up and investigate before pricing, and carry named allowances for what old homes hide — so discoveries change the schedule rather than blindsiding the budget.")],
    "Extensions across Adelaide."))

pages.append(landing(
    "lp-custom-homes", "Custom homes &middot; Adelaide",
    "A house built around one family.",
    "Architect-led custom homes across Adelaide and the Hills — designed, costed and built by the same team, with every cost on the table.",
    ["Site feasibility and a realistic cost range before you spend on documentation",
     "We cost the design as it develops, not after it's locked",
     "Full open-book costing schedule, including our margin",
     "A deliberately small number of builds each year"],
    "kitchen",
    [("Do I need an architect before contacting you?", "No. We'll introduce you to architects and designers whose work suits the house you're describing. Bringing a builder in early usually reduces design fees."),
     ("Can you build from plans I already have?", "Yes. We'll review the documentation, flag anything expensive or difficult to build, and cost it line by line before you commit."),
     ("Where do you build?", "Across metropolitan Adelaide and the Adelaide Hills. We know the councils, the overlays and the soil.")],
    "Custom homes across Adelaide and the Hills."))

pages.append(landing(
    "lp-renovations", "Home renovations &middot; Adelaide",
    "Bluestone outside. This century inside.",
    "Whole-home renovations of Adelaide's villas, bungalows and mid-century houses — structure first, finishes second, nothing hidden in between.",
    ["Written condition assessment before you commit to a scope",
     "Damp, footings and services resolved before a finish is chosen",
     "Full open-book costing, with allowances reconciled and returned",
     "Fourth-generation builder who has worked on hundreds of Adelaide's older homes"],
    "living",
    [("Should we renovate or knock down and rebuild?", "Sometimes rebuilding is the honest answer and we'll say so. It comes down to the condition of the existing structure, what your overlay allows, and how much of the original you actually want."),
     ("Can a renovation be staged?", "Yes, and for many homes it should be. We plan stage one so it doesn't have to be undone later."),
     ("How do you deal with rising damp?", "It's common in Adelaide's stone housing. The fix depends on the cause — ground levels, failed damp course, sealed render trapping moisture — so we diagnose before quoting a treatment.")],
    "Renovations across Adelaide."))

print("Built pages:")
for p in pages:
    print(" ", p + ".html")
print(f"\nTotal: {len(pages)}")
