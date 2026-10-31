"""Content and stable asset references for the AUREVIA static portfolio demo."""

SITE_NAME = "AUREVIA"
PAGES_ORIGIN = "https://sksakin031-byte.github.io/AUREVIA/"
ASSET_ORIGIN = "https://aurevia-hoajclxw.manus.space"

# Exact stable paths returned by the image-generation service. The known public
# Manus origin is prefixed so the images also render from the GitHub Pages site.
ASSET_PATHS = {
    "hero-home": "/manus-storage/async-images/ZBsbReBGLxy5SdeJqJGqSG/image-1.webp",
    "studio-story": "/manus-storage/async-images/ZBsbReBGLxy5SdeJqJGqSG/image-2.webp",
    "team-elara": "/manus-storage/async-images/ZBsbReBGLxy5SdeJqJGqSG/image-3.webp",
    "team-eli": "/manus-storage/async-images/ZBsbReBGLxy5SdeJqJGqSG/image-4.webp",
    "team-nia": "/manus-storage/async-images/ZBsbReBGLxy5SdeJqJGqSG/image-5.webp",
    "maison-cover": "/manus-storage/async-images/rcFBIiFbnK6P4epWckYKOZ/image-1.webp",
    "maison-detail": "/manus-storage/async-images/rcFBIiFbnK6P4epWckYKOZ/image-2.webp",
    "halden-cover": "/manus-storage/async-images/rcFBIiFbnK6P4epWckYKOZ/image-3.webp",
    "halden-detail": "/manus-storage/async-images/rcFBIiFbnK6P4epWckYKOZ/image-4.webp",
    "casa-cover": "/manus-storage/async-images/rcFBIiFbnK6P4epWckYKOZ/image-5.webp",
    "casa-detail": "/manus-storage/async-images/zuxCaWuQOTGSxVJmJufsn4/image-1.webp",
    "orchard-cover": "/manus-storage/async-images/eVNGuxcsYBy5BlAHMV53mw/image-1.webp",
    "orchard-detail": "/manus-storage/async-images/dibUGxnbn98npTrVPQ4pTr/image-1.webp",
    "ember-cover": "/manus-storage/async-images/eVNGuxcsYBy5BlAHMV53mw/image-2.webp",
    "ember-detail": "/manus-storage/async-images/dibUGxnbn98npTrVPQ4pTr/image-2.webp",
    "atelier-cover": "/manus-storage/async-images/dibUGxnbn98npTrVPQ4pTr/image-3.webp",
    "atelier-detail": "/manus-storage/async-images/dibUGxnbn98npTrVPQ4pTr/image-4.webp",
}

PROJECTS = [
    {
        "title": "Maison Verra",
        "file": "project-maison-verra.html",
        "category": "Residential",
        "location": "Lisbon Heights, Demo City",
        "type": "Family residence",
        "short": "A sunlit family home shaped by travertine, oak and quiet curves.",
        "concept": "A flexible family home where shared moments and quieter corners can sit in balance.",
        "challenge": "An open-plan living space made it difficult to find privacy without losing its generous flow.",
        "space_plan": "The main living and dining area anchors the shared zone, while sliding oak screens create an adjustable boundary to quieter rooms.",
        "solution": "Sliding oak screens and layered lighting let the rooms open toward one another or become more private as the day changes.",
        "materials": ["Travertine", "European oak", "Brushed brass", "Natural linen"],
        "objectives": ["Keep the shared rooms bright and connected", "Create adaptable privacy", "Use tactile finishes that feel calm over time"],
        "cover": "maison-cover",
        "detail": "maison-detail",
        "related": ["project-atelier-noor.html", "project-casa-lumen.html"],
    },
    {
        "title": "Halden Offices",
        "file": "project-halden-offices.html",
        "category": "Commercial",
        "location": "Northgate Quarter, Demo City",
        "type": "Workplace concept",
        "short": "A composed workplace concept for a fictional advisory firm.",
        "concept": "A workplace that gives focused work and informal exchange equal weight.",
        "challenge": "A large open floor made concentration difficult and left the shared areas feeling noisy.",
        "space_plan": "Focused work areas sit along calmer edges; shared meeting and lounge spaces connect through a legible circulation route.",
        "solution": "Acoustic timber ceilings, wool-felt surfaces and carefully zoned work lounges create quieter places without closing the plan off.",
        "materials": ["Acoustic oak", "Wool felt", "Matte steel", "Clear glass"],
        "objectives": ["Support both focus and collaboration", "Soften sound across the open plan", "Make circulation easy to understand"],
        "cover": "halden-cover",
        "detail": "halden-detail",
        "related": ["project-ember-lounge.html", "project-orchard-pavilion.html"],
    },
    {
        "title": "Casa Lumen",
        "file": "project-casa-lumen.html",
        "category": "Luxury Homes",
        "location": "Coral Bay, Demo Coast",
        "type": "Coastal home concept",
        "short": "A coastal retreat arranged around soft daylight and sea views.",
        "concept": "A low-key coastal home that frames the horizon while protecting the rooms from strong sun and salt air.",
        "challenge": "Bright coastal exposure called for shade, durable surfaces and a more comfortable transition between inside and out.",
        "space_plan": "Living and dining areas face the sea; shaded thresholds separate the brightest perimeter from sheltered places for rest.",
        "solution": "Deep overhangs, lime plaster and resilient stone finishes temper the light and give the interior a quiet, tactile character.",
        "materials": ["Lime plaster", "Pale limestone", "Teak", "Washed linen"],
        "objectives": ["Frame the view without overpowering it", "Control strong daylight", "Choose finishes suited to a coastal concept"],
        "cover": "casa-cover",
        "detail": "casa-detail",
        "related": ["project-maison-verra.html", "project-atelier-noor.html"],
    },
    {
        "title": "Orchard Pavilion",
        "file": "project-orchard-pavilion.html",
        "category": "Architecture",
        "location": "Willow Vale, Demo County",
        "type": "Garden pavilion concept",
        "short": "A garden pavilion concept that brings its mature orchard into the plan.",
        "concept": "A small, light-framed retreat that treats the existing trees as the architecture's first organizing element.",
        "challenge": "A narrow site and mature trees left little room for a conventional footprint.",
        "space_plan": "A slender linear plan bends around the existing tree positions and keeps the route from sheltered interior to garden readable.",
        "solution": "A slim timber frame bends around the existing oaks, with glass and slate making the threshold between shelter and garden feel continuous.",
        "materials": ["Charred timber", "Clear glass", "Slate", "Natural stone"],
        "objectives": ["Respect the existing trees", "Keep the new footprint visually light", "Make indoor and outdoor use feel connected"],
        "cover": "orchard-cover",
        "detail": "orchard-detail",
        "related": ["project-halden-offices.html", "project-casa-lumen.html"],
    },
    {
        "title": "The Ember Lounge",
        "file": "project-the-ember-lounge.html",
        "category": "Commercial",
        "location": "Old Mill District, Demo City",
        "type": "Hospitality concept",
        "short": "A warm, low-lit lounge concept for a fictional boutique hotel.",
        "concept": "An intimate sequence of seating moments within a taller hospitality room.",
        "challenge": "The tall room felt too open for relaxed conversation and informal gathering.",
        "space_plan": "Curved banquettes divide the tall room into intimate seating pockets while leaving a clear path through the lounge.",
        "solution": "Curved banquettes, a suspended brass ceiling detail and pools of soft light bring a more human scale to the room.",
        "materials": ["Rust velvet", "Walnut", "Brushed brass", "Textured plaster"],
        "objectives": ["Create smaller social settings", "Give the tall room a warmer scale", "Balance low lighting with comfortable visibility"],
        "cover": "ember-cover",
        "detail": "ember-detail",
        "related": ["project-halden-offices.html", "project-maison-verra.html"],
    },
    {
        "title": "Atelier Noor",
        "file": "project-atelier-noor.html",
        "category": "Residential",
        "location": "Summit Road, Demo City",
        "type": "62 m² studio concept",
        "short": "A compact studio apartment composed like a warm, quiet jewel box.",
        "concept": "A small home with a clear place for each daily ritual and storage that disappears into the architecture.",
        "challenge": "The 62-square-metre studio needed to support rest, dining and daily work without feeling crowded.",
        "space_plan": "An integrated joinery wall combines storage, a work surface and a foldaway bed so the centre of the compact plan can remain open.",
        "solution": "Built-in walnut joinery conceals storage and a foldaway bed, while pale marble and smoked glass keep the compact plan visually light.",
        "materials": ["Walnut veneer", "Pale marble", "Smoked glass", "Soft linen"],
        "objectives": ["Make one compact plan support several uses", "Keep storage visually quiet", "Use reflective surfaces with restraint"],
        "cover": "atelier-cover",
        "detail": "atelier-detail",
        "related": ["project-maison-verra.html", "project-casa-lumen.html"],
    },
]

SERVICES = [
    {
        "title": "Residential Interior Design",
        "description": "A home concept shaped around everyday routines, natural light and the way rooms connect.",
        "benefit": "A clear, considered home plan rather than a collection of disconnected rooms.",
        "includes": ["Room-by-room spatial direction", "Lighting and material story", "Joinery and furniture concepts"],
        "image": "maison-cover",
        "alt": "AI-generated conceptual image of a calm oak-and-stone family living room.",
        "projects": ["project-maison-verra.html", "project-atelier-noor.html"],
    },
    {
        "title": "Commercial Interior Design",
        "description": "Workplace and hospitality concepts that balance focus, circulation and a welcoming atmosphere.",
        "benefit": "A spatial experience aligned with the way a fictional team or guest would use the space.",
        "includes": ["Use-zone planning", "Acoustic and lighting direction", "Furniture and finish palette"],
        "image": "halden-cover",
        "alt": "AI-generated conceptual view of a quiet contemporary workplace lounge.",
        "projects": ["project-halden-offices.html", "project-the-ember-lounge.html"],
    },
    {
        "title": "Luxury Home Design",
        "description": "A refined residential concept built from proportion, material, light and meaningful detail.",
        "benefit": "A cohesive design language that keeps comfort at the center of a high-end brief.",
        "includes": ["Interior concept direction", "Material and finish selection", "Key-room visual studies"],
        "image": "casa-cover",
        "alt": "AI-generated conceptual image of a light-filled coastal residence interior.",
        "projects": ["project-casa-lumen.html", "project-maison-verra.html"],
    },
    {
        "title": "Architectural Planning",
        "description": "Early spatial and architectural studies that respond to site, light, circulation and context.",
        "benefit": "A legible concept that connects the building idea to its setting.",
        "includes": ["Site and threshold studies", "Massing and circulation ideas", "Material and opening concepts"],
        "image": "orchard-cover",
        "alt": "AI-generated conceptual image of a timber garden pavilion set among mature trees.",
        "projects": ["project-orchard-pavilion.html", "project-casa-lumen.html"],
    },
    {
        "title": "Space Planning",
        "description": "A practical plan for movement, proportion and multi-use rooms, from a compact studio to a larger home.",
        "benefit": "More clarity about how each part of a space can work together.",
        "includes": ["Furniture and circulation studies", "Flexible-use options", "Storage and room-relationship ideas"],
        "image": "atelier-cover",
        "alt": "AI-generated conceptual image of a compact studio apartment with integrated walnut joinery.",
        "projects": ["project-atelier-noor.html", "project-maison-verra.html"],
    },
    {
        "title": "Furniture & Material Selection",
        "description": "A coordinated palette of surfaces, textiles, lighting and furniture for a more complete interior story.",
        "benefit": "Finishes and objects considered together, with texture and longevity in mind.",
        "includes": ["Hard and soft finish direction", "Furniture and lighting concepts", "Tactile palette board"],
        "image": "maison-detail",
        "alt": "AI-generated conceptual view of travertine, oak joinery and natural linen in a dining space.",
        "projects": ["project-maison-verra.html", "project-the-ember-lounge.html"],
    },
    {
        "title": "3D Visualization & Rendering",
        "description": "Conceptual visual studies to help communicate volume, light and material relationships before decisions are made.",
        "benefit": "A more tangible way to review a concept; visualizations remain illustrative, not construction documents.",
        "includes": ["Key-view image studies", "Material and lighting explorations", "Concept presentation frames"],
        "image": "orchard-detail",
        "alt": "AI-generated conceptual interior of a timber pavilion looking into an orchard.",
        "projects": ["project-orchard-pavilion.html", "project-casa-lumen.html"],
    },
    {
        "title": "Complete Design Consultation",
        "description": "A guided concept conversation about goals, space, preferred atmosphere and the decisions that matter most.",
        "benefit": "A useful starting point for organizing a brief; this fictional demo does not book real consultations.",
        "includes": ["Brief and priority prompts", "Initial spatial questions", "A suggested next-step outline"],
        "image": "studio-story",
        "alt": "AI-generated conceptual image of a design studio table with material samples and an architectural model.",
        "projects": ["project-maison-verra.html", "project-halden-offices.html"],
    },
]

TEAM = [
    {
        "name": "Elara Voss",
        "title": "Creative Director",
        "focus": "Connects each concept to the way people move, gather and rest.",
        "image": "team-elara",
        "alt": "AI-generated fictional portrait of Elara Voss, an imaginary creative director.",
    },
    {
        "name": "Eli Rowan",
        "title": "Architectural Planner",
        "focus": "Studies proportion, circulation and the relationship between a room and its setting.",
        "image": "team-eli",
        "alt": "AI-generated fictional portrait of Eli Rowan, an imaginary architectural planner.",
    },
    {
        "name": "Nia Sol",
        "title": "Materials & Lighting Designer",
        "focus": "Builds tactile palettes and quiet lighting layers that support the larger idea.",
        "image": "team-nia",
        "alt": "AI-generated fictional portrait of Nia Sol, an imaginary materials and lighting designer.",
    },
]

FAQS = [
    {
        "question": "What services are represented in this portfolio?",
        "answer": "The fictional AUREVIA concept covers residential and commercial interiors, luxury homes, architectural planning, space planning, furniture and material selection, 3D visualization, and consultation. No real design service is being offered through this demo.",
    },
    {
        "question": "How long would a project take?",
        "answer": "A real schedule depends on the brief, approvals and delivery scope. This fictional portfolio cannot promise a project timeline; any example timings elsewhere on the site are illustrative only.",
    },
    {
        "question": "How does the consultation work?",
        "answer": "The consultation page is a demonstration of a possible enquiry journey. AUREVIA is not a real studio, so no consultation can be booked here.",
    },
    {
        "question": "How is a project budget considered?",
        "answer": "The demo form includes budget ranges to show how an enquiry might be structured. They are not a price list, quote, or minimum project value.",
    },
    {
        "question": "What happens when I submit the contact form?",
        "answer": "The form validates entries in your browser only. It does not send or store your name, email, phone number, or project details.",
    },
    {
        "question": "How many design revisions are included?",
        "answer": "There is no live contract or revision policy for this fictional demo. A real project would define its review stages and scope in a written agreement.",
    },
]

PROCESS = [
    ("01", "Discover", "Clarify the brief, priorities and the way the space should feel and function."),
    ("02", "Concept", "Explore a spatial direction, material language and the key idea behind the project."),
    ("03", "Develop", "Refine planning, lighting and selected details into a coherent design story."),
    ("04", "Deliver", "Present the agreed concept and outline the next steps for a real-world team."),
]

VALUES = [
    ("01", "Use before ornament", "Start with how a room is used, then let material and detail support that purpose."),
    ("02", "Light as a material", "Let daylight and carefully layered lighting shape the atmosphere."),
    ("03", "Fewer, better decisions", "Keep the palette composed so each chosen surface or object has room to matter."),
]


VISION = "Imagine spaces that make calm, practical living feel considered in every day."
MISSION = "Translate each brief into a clear spatial concept shaped by light, movement and material."
