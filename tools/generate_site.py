"""Generate the crawler-readable static AUREVIA website with Python's standard library."""

from __future__ import annotations

import html
import json
import argparse
from pathlib import Path

from content import (
    ASSET_ORIGIN,
    ASSET_PATHS,
    FAQS,
    MISSION,
    PAGES_ORIGIN,
    PROCESS,
    PROJECTS,
    SERVICES,
    TEAM,
    VALUES,
    VISION,
)

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
PAGE_KEYWORDS = "interior design, architecture, luxury interiors, space planning, AUREVIA portfolio demo"


def e(value: object) -> str:
    return html.escape(str(value), quote=True)


def asset(key: str) -> str:
    """Return the known public URL for an Agent-managed, stable image path."""
    return ASSET_ORIGIN + ASSET_PATHS[key]


def canonical(path: str) -> str:
    return PAGES_ORIGIN + path.lstrip("/")


def img_tag(
    key: str,
    alt: str,
    *,
    classes: str = "",
    eager: bool = False,
    dimensions: tuple[int, int] = (1200, 900),
) -> str:
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    class_attr = f' class="{e(classes)}"' if classes else ""
    width, height = dimensions
    return (
        f'<img src="{e(asset(key))}" alt="{e(alt)}" width="{width}" height="{height}"'
        f'{class_attr} loading="{loading}" decoding="async"{priority}>'
    )


def figure(
    key: str,
    alt: str,
    *,
    classes: str = "",
    caption: str = "",
    eager: bool = False,
    dimensions: tuple[int, int] = (1200, 900),
) -> str:
    class_attr = f' class="{e(classes)}"' if classes else ""
    caption_html = f"<figcaption>{e(caption)}</figcaption>" if caption else ""
    return f"<figure{class_attr}>{img_tag(key, alt, eager=eager, dimensions=dimensions)}{caption_html}</figure>"


def logo() -> str:
    return '''<a class="brand" href="./index.html" aria-label="AUREVIA home">
      <svg class="brand-mark" viewBox="0 0 44 48" aria-hidden="true" focusable="false">
        <path d="M5 44V23a17 17 0 0 1 34 0v21" />
        <path d="M15 44V24a7 7 0 0 1 14 0v20" />
        <path d="M5 44h34" />
      </svg>
      <span class="brand-word">AUREVIA</span>
    </a>'''


NAV_ITEMS = [
    ("home", "Home", "index.html"),
    ("about", "About", "about.html"),
    ("services", "Services", "services.html"),
    ("portfolio", "Portfolio", "portfolio.html"),
    ("faq", "FAQ", "faq.html"),
    ("contact", "Contact", "contact.html"),
]


def header(active: str) -> str:
    links = []
    for key, label, href in NAV_ITEMS:
        current = ' aria-current="page"' if key == active else ""
        links.append(f'<a href="./{href}"{current}>{label}</a>')
    return f'''<a class="skip-link" href="#main-content">Skip to content</a>
    <div class="announcement" role="note">
      <p><span class="announcement-dot" aria-hidden="true"></span> A fictional studio concept · All projects and profiles are illustrative</p>
      <a href="./about.html">The story behind the concept <span aria-hidden="true">↗</span></a>
    </div>
    <header class="site-header">
      <div class="header-inner">
        {logo()}
        <button class="menu-toggle" type="button" aria-label="Open navigation" aria-expanded="false" aria-controls="primary-nav">
          <span></span><span></span>
        </button>
        <nav class="primary-nav" id="primary-nav" aria-label="Primary navigation">
          {''.join(links)}
        </nav>
        <a class="header-cta" href="./contact.html#contact-form">Discuss a concept <span aria-hidden="true">↗</span></a>
      </div>
    </header>'''


def footer() -> str:
    service_links = "".join(
        f'<li><a href="./services.html#{e(service["title"].lower().replace(" & ", "-").replace(" ", "-"))}">{e(service["title"])}</a></li>'
        for service in SERVICES[:4]
    )
    return f'''<footer class="site-footer">
      <div class="footer-main wrap">
        <div class="footer-brand-block">
          {logo()}
          <p class="footer-manifesto">Thoughtful spaces. Clear decisions. A calmer way to create.</p>
          <p class="footer-demo">AUREVIA is a fictional portfolio demonstration—not a real studio or service provider.</p>
        </div>
        <div class="footer-column">
          <h2>Explore</h2>
          <ul>
            <li><a href="./about.html">About the concept</a></li>
            <li><a href="./services.html">Design services</a></li>
            <li><a href="./portfolio.html">Concept portfolio</a></li>
            <li><a href="./faq.html">Questions</a></li>
          </ul>
        </div>
        <div class="footer-column">
          <h2>Selected disciplines</h2>
          <ul>{service_links}</ul>
        </div>
        <div class="footer-column footer-contact">
          <h2>Contact concept</h2>
          <p>hello@aurevia.example</p>
          <p class="small-note">Illustrative details only · No messages are sent or stored</p>
          <a class="footer-text-link" href="./contact.html">View the demo form <span aria-hidden="true">↗</span></a>
        </div>
      </div>
      <div class="footer-bottom wrap">
        <p>© <span data-year>2026</span> AUREVIA · Fictional design-studio concept</p>
        <p>No real client reviews are presented; projects, locations, profiles, imagery and figures are illustrative.</p>
        <a href="./index.html">Back to the beginning ↑</a>
      </div>
    </footer>
    <button class="back-to-top" type="button" id="back-to-top" aria-label="Back to top">↑<span>Top</span></button>'''


def organization_jsonld(url: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "AUREVIA (fictional portfolio demo)",
        "url": url,
        "description": "A fictional interior design and architecture portfolio concept. Not a real business or service provider.",
    }
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def document(
    *,
    title: str,
    description: str,
    path: str,
    active: str,
    image_key: str,
    main: str,
    body_class: str = "",
    noindex: bool = False,
) -> str:
    url = canonical(path)
    title_html = e(title)
    desc_html = e(description)
    keywords = e(PAGE_KEYWORDS)
    image_url = e(asset(image_key))
    canonical_tag = "" if noindex else f'<link rel="canonical" href="{e(url)}">'
    robots_tag = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    jsonld = "" if noindex else f'<script type="application/ld+json">{organization_jsonld(url)}</script>'
    body_class_attr = f' class="{e(body_class)}"' if body_class else ""
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f7f5f0">
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <meta name="keywords" content="{keywords}">
  <meta name="description" content="{desc_html}">
  {robots_tag}
  <title>{title_html}</title>
  {canonical_tag}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="AUREVIA">
  <meta property="og:title" content="{title_html}">
  <meta property="og:description" content="{desc_html}">
  <meta property="og:url" content="{e(url)}">
  <meta property="og:image" content="{image_url}">
  <meta property="og:image:alt" content="AI-generated fictional architectural concept visual for AUREVIA">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title_html}">
  <meta name="twitter:description" content="{desc_html}">
  <meta name="twitter:image" content="{image_url}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  {jsonld}
  <script src="js/main.js" defer></script>
</head>
<body{body_class_attr}>
  {header(active)}
  <main id="main-content">
    {main}
  </main>
  {footer()}
</body>
</html>
'''


def eyebrow(text: str, *, number: str = "") -> str:
    mark = f'<span class="eyebrow-number">{e(number)}</span>' if number else ""
    return f'<p class="eyebrow">{mark}<span>{e(text)}</span></p>'


def text_link(href: str, text: str, *, class_name: str = "text-link") -> str:
    return f'<a class="{e(class_name)}" href="{e(href)}">{e(text)} <span aria-hidden="true">↗</span></a>'


def project_alt(project: dict, detail: bool = False) -> str:
    view = "detail view" if detail else "concept view"
    return f'AI-generated fictional {view} for {project["title"]}: {project["short"]}'


def project_card(project: dict, *, feature: bool = False) -> str:
    klass = "project-card project-card--feature" if feature else "project-card"
    return f'''<article class="{klass}" data-category="{e(project["category"])}" data-reveal>
      <a class="project-card-link" href="./{e(project["file"])}" aria-label="View the {e(project["title"])} fictional concept study">
        <div class="project-card-image">
          {img_tag(project["cover"], project_alt(project), dimensions=(1200, 900))}
          <span class="project-card-arrow" aria-hidden="true">↗</span>
        </div>
        <div class="project-card-meta"><span>{e(project["category"])}</span><span>Concept study</span></div>
        <h3>{e(project["title"])}</h3>
        <p>{e(project["short"])}</p>
        <span class="project-card-location">{e(project["location"])}</span>
      </a>
    </article>'''


def home_page() -> str:
    projects = "".join(project_card(p, feature=(i in (0, 4))) for i, p in enumerate(PROJECTS))
    service_teasers = [
        ("01", "Residential interiors", "Spaces planned around the everyday rhythm of home.", "./services.html#residential-interior-design"),
        ("02", "Work & hospitality", "Welcoming places for focus, gathering and rest.", "./services.html#commercial-interior-design"),
        ("03", "Architecture & space", "A clear relationship between form, flow and setting.", "./services.html#architectural-planning"),
    ]
    service_items = "".join(
        f'''<article class="discipline-card" data-reveal>
          <span class="discipline-number">{number}</span>
          <h3>{e(title)}</h3>
          <p>{e(copy)}</p>
          {text_link(link, "Explore this discipline", class_name="text-link text-link--small")}
        </article>'''
        for number, title, copy, link in service_teasers
    )
    process = "".join(
        f'''<article class="process-step" data-reveal>
          <span class="process-number">{e(number)}</span>
          <h3>{e(title)}</h3>
          <p>{e(copy)}</p>
        </article>'''
        for number, title, copy in PROCESS
    )
    value_cards = "".join(
        f'''<article class="principle-card" data-reveal><span>{e(number)}</span><h3>{e(title)}</h3><p>{e(copy)}</p></article>'''
        for number, title, copy in VALUES
    )
    main = f'''<section class="home-hero" aria-labelledby="home-title">
      <div class="home-hero-media">{img_tag("hero-home", "AI-generated fictional interior concept: a calm living room in warm stone, oak and linen.", classes="home-hero-image", eager=True, dimensions=(2100, 900))}</div>
      <div class="home-hero-shade" aria-hidden="true"></div>
      <div class="home-hero-content wrap" data-reveal>
        {eyebrow("Interior design · Architecture · Concept studio")}
        <h1 id="home-title">Spaces Made to Be<br><em>Lived In, Beautifully.</em></h1>
        <p class="hero-copy">Thoughtful spaces, considered materials and a quieter kind of luxury—imagined around the rituals of everyday life.</p>
        <div class="button-row">
          <a class="button button--dark" href="./portfolio.html">Explore Our Work <span aria-hidden="true">↗</span></a>
          <a class="button button--outline" href="./contact.html#contact-form">Book a Consultation <span aria-hidden="true">↗</span></a>
        </div>
        <p class="hero-disclosure">AUREVIA is a fictional studio concept. All visuals and projects are illustrative.</p>
      </div>
      <a class="hero-scroll" href="#home-intro"><span>Scroll to explore</span><i aria-hidden="true"></i></a>
    </section>

    <section class="section section-intro wrap" id="home-intro" aria-labelledby="intro-title">
      <div class="intro-copy" data-reveal>
        {eyebrow("A considered point of view", number="01")}
        <h2 id="intro-title">Beauty begins with<br><em>how a space feels.</em></h2>
        <p class="lead">AUREVIA imagines interiors that are calm without feeling spare, warm without feeling heavy, and shaped around the details of real life.</p>
        <p>From the first spatial idea to the last material note, each concept is built on clarity, proportion and a strong sense of place.</p>
        {text_link("./about.html", "Discover the studio concept")}
      </div>
      <div class="intro-visual" data-reveal>
        {figure("studio-story", "AI-generated fictional design studio scene with a model and warm natural material samples.", classes="image-frame image-frame--offset", caption="Material studies · Fictional studio concept")}
        <p class="image-note">A small study in light, texture and proportion.</p>
      </div>
    </section>

    <section class="section section--soft" aria-labelledby="disciplines-title">
      <div class="wrap">
        <div class="section-heading section-heading--split" data-reveal>
          <div>{eyebrow("What we imagine", number="02")}<h2 id="disciplines-title">A studio for<br><em>considered spaces.</em></h2></div>
          <div class="section-heading-aside"><p>Eight design disciplines, one shared intention: make the space feel as good to use as it is to look at.</p>{text_link("./services.html", "View all services")}</div>
        </div>
        <div class="discipline-grid">{service_items}</div>
      </div>
    </section>

    <section class="section wrap" aria-labelledby="work-title">
      <div class="section-heading section-heading--split" data-reveal>
        <div>{eyebrow("Selected concept studies", number="03")}<h2 id="work-title">Spaces with<br><em>a point of view.</em></h2></div>
        <div class="section-heading-aside"><p>Six fictional studies explore different scales, settings and ways of living. Every image is an AI-generated concept visualization—not a photograph of completed client work.</p>{text_link("./portfolio.html", "Explore the portfolio")}</div>
      </div>
      <div class="project-grid project-grid--home">{projects}</div>
    </section>

    <section class="section section--charcoal" aria-labelledby="principles-title">
      <div class="wrap">
        <div class="section-heading section-heading--split section-heading--light" data-reveal>
          <div>{eyebrow("Why choose AUREVIA?", number="04")}<h2 id="principles-title">A quieter way<br><em>to make choices.</em></h2></div>
          <div class="section-heading-aside"><p>Not client testimonials: these are the principles that guide the fictional AUREVIA concept.</p></div>
        </div>
        <div class="principle-grid">{value_cards}</div>
      </div>
    </section>

    <section class="section section--metrics wrap" aria-label="Illustrative portfolio snapshot">
      <div class="metrics-heading">{eyebrow("Illustrative site snapshot")}<p>Counts describe this portfolio demonstration only—not business performance.</p></div>
      <dl class="metrics-list">
        <div><dt>06</dt><dd>fictional concept studies</dd></div>
        <div><dt>08</dt><dd>design disciplines outlined</dd></div>
        <div><dt>04</dt><dd>steps in the sample process</dd></div>
      </dl>
    </section>

    <section class="section section-process" aria-labelledby="process-title">
      <div class="wrap">
        <div class="section-heading section-heading--split" data-reveal>
          <div>{eyebrow("A clear process", number="05")}<h2 id="process-title">Good design, in<br><em>thoughtful stages.</em></h2></div>
          <div class="section-heading-aside"><p>A simple sample framework keeps the brief, the design idea and the next steps connected.</p></div>
        </div>
        <div class="process-grid">{process}</div>
      </div>
    </section>

    <section class="closing-panel wrap" aria-labelledby="closing-title">
      <div class="closing-panel-inner" data-reveal>
        <div>{eyebrow("Begin with a question")}<h2 id="closing-title">A better space starts<br><em>with a better brief.</em></h2></div>
        <div class="closing-panel-aside"><p>Explore how an enquiry might take shape in this fictional design-studio demonstration.</p><a class="button button--light" href="./contact.html#contact-form">Book a Consultation <span aria-hidden="true">↗</span></a><p class="small-note">Demo only · no real booking or message transmission</p></div>
      </div>
    </section>'''
    return document(
        title="AUREVIA — Interior Design & Architecture",
        description="Discover AUREVIA, a fictional interior design and architecture portfolio concept shaped around thoughtful spaces, considered materials and everyday life.",
        path="",
        active="home",
        image_key="hero-home",
        main=main,
        body_class="page-home",
    )


def about_page() -> str:
    team_cards = "".join(
        f'''<article class="team-card" data-reveal>
          <div class="team-image">{img_tag(person["image"], person["alt"], dimensions=(900, 900))}<span class="fictional-tag">Fictional profile</span></div>
          <div class="team-card-copy"><p class="eyebrow">{e(person["title"])}</p><h3>{e(person["name"])}</h3><p>{e(person["focus"])}</p></div>
        </article>'''
        for person in TEAM
    )
    values = "".join(
        f'''<article class="value-row" data-reveal><span class="value-index">{e(num)}</span><div><h3>{e(title)}</h3><p>{e(copy)}</p></div></article>'''
        for num, title, copy in VALUES
    )
    vision_mission = (
        f'<article class="value-row" data-reveal><span class="value-index">V</span><div><h3>Vision</h3><p>{e(VISION)}</p></div></article>'
        f'<article class="value-row" data-reveal><span class="value-index">M</span><div><h3>Mission</h3><p>{e(MISSION)}</p></div></article>'
    )
    main = f'''<section class="page-hero wrap" aria-labelledby="page-title">
      {eyebrow("About the concept")}
      <h1 id="page-title">A studio imagined<br><em>around how we live.</em></h1>
      <p class="page-hero-copy">AUREVIA is a fictional design-studio portfolio exploring the meeting point of atmosphere, architecture and everyday rituals.</p>
    </section>
    <section class="section about-story wrap" aria-labelledby="story-title">
      <div class="about-story-visual" data-reveal>{figure("studio-story", "AI-generated fictional studio scene with architectural model, material samples and a calm worktable.", classes="image-frame image-frame--story", caption="A fictional studio study · AI-generated visual")}</div>
      <div class="about-story-copy" data-reveal>
        {eyebrow("The story", number="01")}
        <h2 id="story-title">Less about a look.<br><em>More about a feeling.</em></h2>
        <p class="lead">AUREVIA began as a design idea: spaces can feel elevated and still remain easy to live in.</p>
        <p>This imagined studio brings together spatial planning, natural materials and measured detail. The portfolio is a demonstration of that approach—not a real company, team or record of client work.</p>
        <p>Every room, location and profile shown here is fictional. The architectural imagery was generated specifically as conceptual visualization.</p>
        {text_link("./portfolio.html", "See the concept studies")}
      </div>
    </section>
    <section class="section section--soft" aria-labelledby="beliefs-title">
      <div class="wrap beliefs-layout">
        <div class="beliefs-intro" data-reveal>{eyebrow("Vision · Mission · Values", number="02")}<h2 id="beliefs-title">Design with<br><em>intention.</em></h2><p>Three simple ideas give the fictional studio its direction.</p></div>
        <div class="values-list">{vision_mission}{values}</div>
      </div>
    </section>
    <section class="section why-aurevia wrap" aria-labelledby="why-aurevia-title">
      <div class="section-heading section-heading--split" data-reveal>
        <div>{eyebrow("Why choose AUREVIA?", number="03")}<h2 id="why-aurevia-title">Thoughtful from<br><em>the first plan.</em></h2></div>
        <div class="section-heading-aside"><p>These are the design principles behind the fictional studio concept—not testimonials or claims of real client results.</p></div>
      </div>
      <div class="approach-columns">
        <article data-reveal><span>01</span><h3>Use before ornament</h3><p>Begin with the way a room should work, then shape its material and visual character.</p></article>
        <article data-reveal><span>02</span><h3>Light as a material</h3><p>Consider daylight and layered illumination as part of the spatial concept.</p></article>
        <article data-reveal><span>03</span><h3>Fewer, better decisions</h3><p>Keep a composed palette so each chosen surface and detail has a clear purpose.</p></article>
      </div>
    </section>
    <section class="section wrap" aria-labelledby="approach-title">
      <div class="approach-heading" data-reveal>{eyebrow("The approach", number="04")}<h2 id="approach-title">Clear thinking,<br><em>quiet detail.</em></h2></div>
      <div class="approach-columns">
        <article data-reveal><span>01</span><h3>Start with the room</h3><p>Understand the light, circulation and everyday use before choosing a visual language.</p></article>
        <article data-reveal><span>02</span><h3>Build a material story</h3><p>Combine texture, tone and finish so each decision supports the larger composition.</p></article>
        <article data-reveal><span>03</span><h3>Make the idea legible</h3><p>Use clear plans and concept imagery to communicate how the space could come together.</p></article>
      </div>
    </section>
    <section class="section section--team" aria-labelledby="team-title">
      <div class="wrap">
        <div class="section-heading section-heading--split" data-reveal>
          <div>{eyebrow("The imagined team", number="05")}<h2 id="team-title">People behind<br><em>the perspective.</em></h2></div>
          <div class="section-heading-aside"><p>These names, portraits and roles are fictional placeholders created for this portfolio concept. Portraits are AI-generated.</p></div>
        </div>
        <div class="team-grid">{team_cards}</div>
      </div>
    </section>
    <section class="closing-panel wrap" aria-labelledby="about-cta-title">
      <div class="closing-panel-inner" data-reveal><div>{eyebrow("A considered beginning")}<h2 id="about-cta-title">Explore the work<br><em>behind the idea.</em></h2></div><div class="closing-panel-aside"><p>Move from the studio's point of view to six fictional concept studies.</p><a class="button button--light" href="./portfolio.html">View the portfolio <span aria-hidden="true">↗</span></a></div></div>
    </section>'''
    return document(
        title="About AUREVIA — A Fictional Design Studio",
        description="Learn about AUREVIA's fictional design philosophy, values and imagined team behind this interior design and architecture portfolio concept.",
        path="about.html",
        active="about",
        image_key="studio-story",
        main=main,
        body_class="page-about",
    )


def services_page() -> str:
    rows = []
    for idx, service in enumerate(SERVICES, start=1):
        slug = service["title"].lower().replace(" & ", "-").replace(" ", "-")
        reverse = " service-row--reverse" if idx % 2 == 0 else ""
        inclusions = "".join(f"<li>{e(item)}</li>" for item in service["includes"])
        related = " · ".join(
            f'<a href="./{e(path)}">{e(next(p["title"] for p in PROJECTS if p["file"] == path))}</a>'
            for path in service["projects"]
        )
        rows.append(
            f'''<article class="service-row{reverse}" id="{e(slug)}" data-reveal>
              <div class="service-row-image">{figure(service["image"], service["alt"], classes="image-frame image-frame--service", caption="AI-generated conceptual visual · Fictional portfolio")}</div>
              <div class="service-row-copy">
                {eyebrow("Design discipline", number=f"{idx:02d}")}
                <h2>{e(service["title"])}</h2>
                <p class="service-description">{e(service["description"])}</p>
                <p class="service-benefit"><strong>Design intention</strong> {e(service["benefit"])}</p>
                <h3 class="service-includes-title">A sample scope may explore</h3>
                <ul class="check-list">{inclusions}</ul>
                <p class="service-related"><strong>Related concept studies</strong><br>{related}</p>
                {text_link("./contact.html#contact-form", "Discuss this discipline", class_name="text-link")}
              </div>
            </article>'''
        )
    main = f'''<section class="page-hero page-hero--compact wrap" aria-labelledby="page-title">
      {eyebrow("Services · Eight disciplines")}
      <h1 id="page-title">One clear point<br><em>of view, many scales.</em></h1>
      <p class="page-hero-copy">A set of fictional design disciplines shows how spatial thinking, materials and visual communication can work together.</p>
      <p class="demo-inline-note">AUREVIA is a concept portfolio only. No real service is currently offered.</p>
    </section>
    <section class="section services-intro wrap" aria-labelledby="services-intro-title">
      <div>{eyebrow("The disciplines", number="01")}<h2 id="services-intro-title">A useful place<br><em>to begin.</em></h2></div>
      <p>Explore each area on its own, or follow the related concept studies to see how the design approach shifts with the brief.</p>
    </section>
    <section class="service-list wrap" aria-label="AUREVIA design disciplines">{''.join(rows)}</section>
    <section class="closing-panel wrap" aria-labelledby="services-cta-title"><div class="closing-panel-inner" data-reveal><div>{eyebrow("The next question")}<h2 id="services-cta-title">Which part of your<br><em>space needs clarity?</em></h2></div><div class="closing-panel-aside"><p>Use the contact form to explore a possible brief. It is a local demonstration and will not transmit your details.</p><a class="button button--light" href="./contact.html#contact-form">Open the demo form <span aria-hidden="true">↗</span></a></div></div></section>'''
    return document(
        title="Interior Design Services — AUREVIA Concept",
        description="Explore eight fictional AUREVIA design disciplines, from residential interiors and space planning to architecture, materials and visualization.",
        path="services.html",
        active="services",
        image_key="maison-cover",
        main=main,
        body_class="page-services",
    )


def portfolio_page() -> str:
    filters = ["All", "Architecture", "Commercial", "Luxury Homes", "Residential"]
    buttons = "".join(
        f'<button type="button" class="filter-button" data-filter="{e(label)}" aria-pressed="{"true" if label == "All" else "false"}">{e(label)}</button>'
        for label in filters
    )
    cards = "".join(project_card(p) for p in PROJECTS)
    main = f'''<section class="page-hero page-hero--compact wrap" aria-labelledby="page-title">
      {eyebrow("Portfolio · Fictional concept studies")}
      <h1 id="page-title">Six different briefs.<br><em>One considered approach.</em></h1>
      <p class="page-hero-copy">Browse an illustrative collection of residential, commercial and architectural concepts. Locations and imagery are fictional.</p>
    </section>
    <section class="section portfolio-section wrap" aria-labelledby="projects-title">
      <div class="portfolio-toolbar">
        <div><h2 id="projects-title">The concept archive</h2><p class="small-note">AI-generated visuals · Not completed client projects</p></div>
        <div class="filter-group" role="group" aria-label="Filter concept studies by category">{buttons}</div>
      </div>
      <p class="filter-status" id="filter-status" aria-live="polite">Showing all {len(PROJECTS)} concept studies.</p>
      <div class="project-grid project-grid--portfolio" id="project-grid">{cards}</div>
      <p class="portfolio-disclosure">Every project, place and image on this page is fictional. Images are AI-generated conceptual visualizations.</p>
    </section>
    <section class="closing-panel wrap" aria-labelledby="portfolio-cta-title"><div class="closing-panel-inner" data-reveal><div>{eyebrow("Explore a direction")}<h2 id="portfolio-cta-title">A strong concept<br><em>starts with a brief.</em></h2></div><div class="closing-panel-aside"><p>See how the demo enquiry form organizes a first conversation—without collecting or sending your data.</p><a class="button button--light" href="./contact.html#contact-form">View the contact form <span aria-hidden="true">↗</span></a></div></div></section>'''
    return document(
        title="Interior Design Portfolio — AUREVIA Concepts",
        description="Browse six fictional AUREVIA interior design and architecture concept studies, with category filters and detailed project stories.",
        path="portfolio.html",
        active="portfolio",
        image_key="orchard-cover",
        main=main,
        body_class="page-portfolio",
    )


def project_page(project: dict) -> str:
    related_projects = [p for p in PROJECTS if p["file"] in project["related"]]
    related_cards = "".join(project_card(p) for p in related_projects)
    materials = "".join(f"<li>{e(item)}</li>" for item in project["materials"])
    objectives = "".join(
        f'<li><span class="objective-mark" aria-hidden="true">—</span><span>{e(item)}</span></li>'
        for item in project["objectives"]
    )
    slug = Path(project["file"]).stem
    main = f'''<section class="case-hero wrap" aria-labelledby="page-title">
      <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="./index.html">Home</a><span aria-hidden="true">/</span><a href="./portfolio.html">Portfolio</a><span aria-hidden="true">/</span><span aria-current="page">{e(project["title"])}</span></nav>
      <div class="case-hero-heading">
        <div>{eyebrow(f"{project['category']} · Fictional concept study")}<h1 id="page-title">{e(project["title"])}</h1><p class="case-hero-copy">{e(project["short"])}</p></div>
        <p class="case-hero-aside">A conceptual exploration of light, movement and material—created for this portfolio demonstration.</p>
      </div>
      <div class="case-hero-image">{img_tag(project["cover"], project_alt(project), classes="case-cover-image", dimensions=(1600, 1100))}<span class="image-stamp">Concept visualization · AI-generated</span></div>
      <dl class="case-facts">
        <div><dt>Category</dt><dd>{e(project["category"])}</dd></div>
        <div><dt>Location</dt><dd>{e(project["location"])}</dd></div>
        <div><dt>Project type</dt><dd>{e(project["type"])}</dd></div>
        <div><dt>Status</dt><dd>Fictional concept study</dd></div>
      </dl>
    </section>
    <section class="section case-overview wrap" aria-labelledby="concept-title">
      <div class="case-section-label">{eyebrow("01 · The concept")}</div>
      <div class="case-overview-copy"><h2 id="concept-title">A space shaped<br><em>by its brief.</em></h2><p class="lead">{e(project["concept"])}</p><p>{e(project["short"])} The purpose of this study is to show how a design idea can respond to the needs of a fictional place without losing its atmosphere.</p></div>
    </section>
    <section class="section case-response section--soft" aria-labelledby="response-title">
      <div class="wrap">
        <div class="section-heading section-heading--split" data-reveal><div>{eyebrow("02 · Challenge & response")}<h2 id="response-title">The constraint<br><em>became the cue.</em></h2></div><p class="section-heading-aside">A clear spatial question creates a more useful starting point than a decorative solution.</p></div>
        <div class="challenge-solution-grid">
          <article class="challenge-card" data-reveal><span class="case-index">The challenge</span><p>{e(project["challenge"])}</p></article>
          <article class="solution-card" data-reveal><span class="case-index">The response</span><p>{e(project["solution"])}</p></article>
        </div>
      </div>
    </section>
    <section class="section case-planning wrap" aria-labelledby="planning-title">
      <div class="case-planning-intro" data-reveal>{eyebrow("03 · Design objectives")}<h2 id="planning-title">A few clear<br><em>priorities.</em></h2><p>These fictional objectives guide the concept from the first plan to the finishing palette.</p></div>
      <ol class="objective-list">{objectives}</ol>
    </section>
    <section class="section case-space-plan section--soft" aria-labelledby="space-plan-title">
      <div class="wrap case-space-plan-inner" data-reveal>{eyebrow("04 · Space planning")}<h2 id="space-plan-title">Let the plan<br><em>do the quiet work.</em></h2><p>{e(project["space_plan"])}</p></div>
    </section>
    <section class="section case-materials section--charcoal" aria-labelledby="materials-title">
      <div class="wrap materials-layout" data-reveal><div>{eyebrow("05 · Materials & finishes")}<h2 id="materials-title">Tactile, calm<br><em>and connected.</em></h2></div><div><p>The palette is presented as a concept direction, not a specification for construction.</p><ul class="material-list">{materials}</ul></div></div>
    </section>
    <section class="section case-gallery wrap" aria-labelledby="gallery-title">
      <div class="section-heading section-heading--split" data-reveal><div>{eyebrow("06 · Visual study")}<h2 id="gallery-title">A closer look<br><em>at the concept.</em></h2></div><p class="section-heading-aside">The following AI-generated images are conceptual visualizations. They are not photographs of a completed project.</p></div>
      <div class="case-gallery-grid">
        {figure(project["cover"], project_alt(project), classes="case-gallery-image case-gallery-image--wide", caption=f'{project["title"]} · AI-generated fictional concept visualization')}
        {figure(project["detail"], project_alt(project, detail=True), classes="case-gallery-image case-gallery-image--detail", caption=f'{project["title"]} · Material and spatial detail · AI-generated concept')}
      </div>
      <p class="small-note case-disclaimer">All names, locations, briefs, materials and images are fictional portfolio content.</p>
    </section>
    <section class="section related-projects section--soft" aria-labelledby="related-title"><div class="wrap"><div class="section-heading section-heading--split" data-reveal><div>{eyebrow("Continue exploring")}<h2 id="related-title">Related concept<br><em>studies.</em></h2></div><div class="section-heading-aside">{text_link("./portfolio.html", "Return to all projects")}</div></div><div class="project-grid project-grid--related">{related_cards}</div></div></section>
    <section class="closing-panel wrap" aria-labelledby="case-cta-title"><div class="closing-panel-inner" data-reveal><div>{eyebrow("Next step")}<h2 id="case-cta-title">Bring a brief<br><em>into focus.</em></h2></div><div class="closing-panel-aside"><p>Explore the fictional contact flow. Nothing is sent or stored.</p><a class="button button--light" href="./contact.html#contact-form">Open the demo form <span aria-hidden="true">↗</span></a></div></div></section>'''
    return document(
        title=f"{project['title']} — AUREVIA Concept Study",
        description=f"Explore {project['title']}, a fictional {project['category'].lower()} design concept by AUREVIA, with a project brief, design response, materials and AI-generated visuals.",
        path=project["file"],
        active="portfolio",
        image_key=project["cover"],
        main=main,
        body_class=f"page-project page-{slug}",
    )


def contact_page() -> str:
    services = "".join(f'<option value="{e(s["title"])}">{e(s["title"])}</option>' for s in SERVICES)
    main = f'''<section class="page-hero page-hero--compact wrap" aria-labelledby="page-title">
      {eyebrow("Contact · A demo enquiry")}
      <h1 id="page-title">Tell us what<br><em>you are imagining.</em></h1>
      <p class="page-hero-copy">A considered brief is a good place to start. This page demonstrates a contact experience for the fictional AUREVIA studio.</p>
    </section>
    <section class="section contact-section wrap" aria-labelledby="contact-form-title">
      <aside class="contact-aside" data-reveal>
        {eyebrow("A first conversation", number="01")}
        <h2>Small details<br><em>make a brief.</em></h2>
        <p>Share the space, the way you hope it will work, and the decisions you need help thinking through.</p>
        <div class="contact-details">
          <div><span class="contact-label">Email · illustrative</span><span>hello@aurevia.example</span></div>
          <div><span class="contact-label">Phone · illustrative</span><span>+00 000 000 0000</span></div>
          <div><span class="contact-label">Studio</span><address>Example Avenue<br>Demo City · Fictional address</address></div>
        </div>
        <p class="contact-demo-note"><strong>Demo information only.</strong> AUREVIA is not a real studio. No consultation is available at these contact details.</p>
        <a class="text-link" href="./faq.html">Read common questions <span aria-hidden="true">↗</span></a>
      </aside>
      <div class="contact-form-wrap" data-reveal>
        <section class="contact-form" id="contact-form" role="form" aria-labelledby="contact-form-title">
          <div class="form-heading"><p class="eyebrow">Project enquiry · Interactive demo</p><h2 id="contact-form-title">A few details<br><em>to shape the brief.</em></h2><p>Fields marked <span aria-hidden="true">*</span> are required.</p></div>
          <div class="form-grid">
            <div class="form-field">
              <label for="name">Name <span aria-hidden="true">*</span></label>
              <input id="name" name="name" type="text" autocomplete="name" minlength="2" maxlength="100" required aria-describedby="error-name">
              <p class="field-error" id="error-name" hidden></p>
            </div>
            <div class="form-field">
              <label for="email">Email address <span aria-hidden="true">*</span></label>
              <input id="email" name="email" type="email" autocomplete="email" maxlength="254" required aria-describedby="error-email">
              <p class="field-error" id="error-email" hidden></p>
            </div>
            <div class="form-field">
              <label for="phone">Phone <span class="label-optional">Optional</span></label>
              <input id="phone" name="phone" type="tel" autocomplete="tel" maxlength="32" aria-describedby="error-phone">
              <p class="field-error" id="error-phone" hidden></p>
            </div>
            <div class="form-field">
              <label for="service">Service of interest <span aria-hidden="true">*</span></label>
              <select id="service" name="service" required aria-describedby="error-service">
                <option value="" selected disabled>Choose a discipline</option>{services}<option value="Still shaping the brief">Still shaping the brief</option>
              </select>
              <p class="field-error" id="error-service" hidden></p>
            </div>
            <div class="form-field">
              <label for="budget">Indicative project budget <span aria-hidden="true">*</span></label>
              <select id="budget" name="budget" required aria-describedby="error-budget">
                <option value="" selected disabled>Choose a range</option>
                <option value="Under $25,000">Under $25,000</option>
                <option value="$25,000–$50,000">$25,000–$50,000</option>
                <option value="$50,000–$100,000">$50,000–$100,000</option>
                <option value="$100,000+">$100,000+</option>
                <option value="Not decided">Not decided yet</option>
              </select>
              <p class="field-error" id="error-budget" hidden></p>
            </div>
            <div class="form-field form-field--full">
              <label for="message">Tell us about the project <span aria-hidden="true">*</span></label>
              <textarea id="message" name="message" rows="5" minlength="10" maxlength="2000" required aria-describedby="error-message message-hint"></textarea>
              <p class="field-hint" id="message-hint">A few sentences about the space, location or goal are enough. Please do not include sensitive information.</p>
              <p class="field-error" id="error-message" hidden></p>
            </div>
          </div>
          <div class="form-consent" role="note"><span class="form-consent-icon" aria-hidden="true">i</span><p>This is a browser-only demonstration. The form does <strong>not</strong> send, email or store your information. Do not enter sensitive personal details.</p></div>
          <button class="button button--dark form-submit" id="validate-enquiry" type="button">Check my enquiry <span aria-hidden="true">↗</span></button>
          <p class="form-status" id="form-status" role="status" aria-live="polite" tabindex="-1"></p>
          <noscript><p class="small-note">JavaScript is off, so validation is unavailable. Your entries are not sent or stored.</p></noscript>
          <p class="small-note">Your entries remain in this page only; no network request is made.</p>
        </section>
      </div>
    </section>
    <section class="contact-faq section--soft" aria-labelledby="contact-faq-title"><div class="wrap contact-faq-inner"><div>{eyebrow("A useful next step")}<h2 id="contact-faq-title">Questions before<br><em>you begin?</em></h2></div><div><p>Project timing, scope and pricing are all illustrative in this fictional portfolio.</p>{text_link("./faq.html", "Read the FAQ")}</div></div></section>'''
    return document(
        title="Contact AUREVIA — Interactive Demo Form",
        description="Explore AUREVIA's accessible project enquiry form. This fictional portfolio demo validates in the browser and does not send or store personal information.",
        path="contact.html",
        active="contact",
        image_key="studio-story",
        main=main,
        body_class="page-contact",
    )


def faq_page() -> str:
    items = "".join(
        f'''<details class="faq-item" name="aurevia-faq" data-reveal>
          <summary><span>{e(faq["question"])}</span><span class="faq-toggle" aria-hidden="true"></span></summary>
          <div class="faq-answer"><p>{e(faq["answer"])}</p></div>
        </details>'''
        for faq in FAQS
    )
    main = f'''<section class="page-hero page-hero--compact wrap" aria-labelledby="page-title">
      {eyebrow("FAQ · Clear answers")}
      <h1 id="page-title">A few things<br><em>worth knowing.</em></h1>
      <p class="page-hero-copy">Answers about the fictional studio concept, the sample design approach and the interactive demo form.</p>
    </section>
    <section class="section faq-section wrap" aria-labelledby="faq-list-title">
      <div class="faq-sidebar">{eyebrow("Questions & answers", number="01")}<h2 id="faq-list-title">Start with<br><em>the essentials.</em></h2><p>Nothing on this page represents a real contract, offer or service commitment.</p>{text_link("./contact.html#contact-form", "See the demo form")}</div>
      <div class="faq-list">{items}</div>
    </section>
    <section class="closing-panel wrap" aria-labelledby="faq-cta-title"><div class="closing-panel-inner" data-reveal><div>{eyebrow("Still exploring?")}<h2 id="faq-cta-title">Follow the idea<br><em>to the next page.</em></h2></div><div class="closing-panel-aside"><p>Browse the concept studies or return to the beginning.</p><a class="button button--light" href="./portfolio.html">Explore the portfolio <span aria-hidden="true">↗</span></a></div></div></section>'''
    return document(
        title="FAQ — AUREVIA Design Portfolio Demo",
        description="Answers about AUREVIA's fictional portfolio, sample services, project timelines, budget fields and browser-only contact form.",
        path="faq.html",
        active="faq",
        image_key="studio-story",
        main=main,
        body_class="page-faq",
    )


def not_found_page() -> str:
    main = '''<section class="not-found wrap" aria-labelledby="page-title">
      <span class="not-found-number">404</span>
      <p class="eyebrow">The page has moved on</p>
      <h1 id="page-title">A quiet space<br><em>to begin again.</em></h1>
      <p class="page-hero-copy">We could not find that page in this fictional portfolio. Choose a path below to continue.</p>
      <div class="button-row"><a class="button button--dark" href="./index.html">Return home <span aria-hidden="true">↗</span></a><a class="button button--outline-dark" href="./portfolio.html">Browse concepts <span aria-hidden="true">↗</span></a></div>
    </section>'''
    return document(
        title="Page Not Found — AUREVIA",
        description="This AUREVIA portfolio page was not found.",
        path="404.html",
        active="",
        image_key="hero-home",
        main=main,
        body_class="page-not-found",
        noindex=True,
    )


def write(path: str, contents: str) -> None:
    target = SITE / path
    target.parent.mkdir(parents=True, exist_ok=True)
    normalized = "\n".join(line.rstrip() for line in contents.splitlines()).rstrip() + "\n"
    target.write_text(normalized, encoding="utf-8")
    print(f"Wrote {target.relative_to(ROOT)} ({len(normalized)} chars)")


def write_seo_files() -> None:
    urls = [
        ("", "Home"),
        ("about.html", "About AUREVIA"),
        ("services.html", "Design Services"),
        ("portfolio.html", "Portfolio"),
        ("contact.html", "Contact"),
        ("faq.html", "FAQ"),
    ] + [(p["file"], p["title"]) for p in PROJECTS]
    route_entries = [{"path": "/" if not path else f"/{path}", "title": title} for path, title in urls]
    route_entries.insert(1, {"path": "/index.html", "title": "Home"})
    write("manus-routes.json", json.dumps({"routes": route_entries}, ensure_ascii=False, indent=2) + "\n")
    sitemap_items = "\n".join(f"  <url><loc>{e(canonical(path))}</loc></url>" for path, _ in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_items}\n</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {canonical('sitemap.xml')}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate AUREVIA static HTML and SEO documents.")
    parser.add_argument("--output", default=str(ROOT / "site"), help="Output directory (default: project site/). Use --output . for a GitHub Pages repository root.")
    args = parser.parse_args()
    global SITE
    SITE = Path(args.output).expanduser().resolve()
    SITE.mkdir(parents=True, exist_ok=True)
    write("favicon.svg", '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44 48"><rect width="44" height="48" rx="3" fill="#f7f5f0"/><g fill="none" stroke="#806544" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.7"><path d="M5 44V23a17 17 0 0 1 34 0v21"/><path d="M15 44V24a7 7 0 0 1 14 0v20"/><path d="M5 44h34"/></g></svg>''')
    write("index.html", home_page())
    write("about.html", about_page())
    write("services.html", services_page())
    write("portfolio.html", portfolio_page())
    write("contact.html", contact_page())
    write("faq.html", faq_page())
    for project in PROJECTS:
        write(project["file"], project_page(project))
    write("404.html", not_found_page())
    write_seo_files()
    print(f"Generated {6 + len(PROJECTS) + 1} static HTML pages in {SITE}")


if __name__ == "__main__":
    main()
