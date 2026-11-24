#!/usr/bin/env python3
"""Generates the BioBesir site pages into the repo. Run from the repo: python3 tools/build.py"""
import html, json, os, re, sys
from urllib.parse import quote

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SM = 'studying-materials/'
E = html.escape

SITE = 'https://besirbio.github.io/my-personal-website/'
EMAIL = 'besirzeneli@gmail.com'
SOCIALS = [
    ('LinkedIn', 'https://www.linkedin.com/in/besir-zeneli-0174688b/'),
    ('Instagram', 'https://www.instagram.com/besirzeneli/'),
    ('Facebook', 'https://www.facebook.com/besirxx'),
    ('X', 'https://x.com/besir_zeneli'),
]

def u(path):
    """URL-encode a local path (keeps slashes)."""
    if path.startswith('http'):
        return path
    return quote(path, safe='/#?=&.-_~')

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,500;1,7..72,400&family=Schibsted+Grotesk:wght@400;500;600;700;800&display=swap" rel="stylesheet">')

def page(path, title, desc, body, current=None, extra_head='', extra_js=''):
    depth = path.count('/')
    b = '../' * depth
    nav_items = [('Study', SM + 'studyingmaterials.html', 'study'), ('Writing', 'writings.html', 'writing'),
                 ('CV', 'Portfolio.html', 'cv'), ('Contact', 'index.html#contact', 'contact')]
    nav = '\n'.join(f'      <a href="{b}{h}"{" aria-current=\"page\"" if k == current else ""}>{n}</a>' for n, h, k in nav_items)
    footer_social = ''.join(f'<li><a href="{h}" target="_blank" rel="noopener">{n}</a></li>' for n, h in SOCIALS)
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#352a73">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE}assets/img/portrait.jpg">
<meta property="og:url" content="{SITE}{u(path)}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@besir_zeneli">
<link rel="icon" type="image/png" href="{b}android-chrome-192x192.png">
{FONTS}
<link rel="stylesheet" href="{b}assets/site.css">
{extra_head}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{b}index.html"><span class="brand-cell" aria-hidden="true"></span>Besir Zeneli</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav id="site-nav" class="nav" aria-label="Main">
{nav}
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div>
      <a class="brand" href="{b}index.html"><span class="brand-cell" aria-hidden="true"></span>Besir Zeneli</a>
      <p class="note" style="margin-top:14px">Biology teacher and molecular biologist at Maarif International Schools, Skopje.</p>
    </div>
    <div>
      <h2>On this site</h2>
      <ul>
        <li><a href="{b}{SM}studyingmaterials.html">Study materials</a></li>
        <li><a href="{b}writings.html">Writing</a></li>
        <li><a href="{b}Portfolio.html">CV</a></li>
      </ul>
    </div>
    <div>
      <h2>Elsewhere</h2>
      <ul><li><a href="mailto:{EMAIL}">Email</a></li>{footer_social}</ul>
    </div>
    <p class="copy">© <span data-year>2025</span> Besir Zeneli</p>
  </div>
</footer>
{extra_js}<script src="{b}assets/site.js"></script>
</body>
</html>
'''
    with open(os.path.join(ROOT, path), 'w', encoding='utf-8') as f:
        f.write(doc)

# =====================================================================
# STUDY MATERIALS DATA
# resource tuple: (type, label, href relative to site root)
# types: textbook, slides, mindmap, interactive, video
# =====================================================================
P = lambda g, f: f'pdfs/{g}/{f}'
M = lambda f: SM + f
def L(code, title, *res):
    return {'code': code, 'title': title, 'res': [{'type': t, 'label': l, 'href': h} for t, l, h in res]}
pdf = lambda g, f, label='PDF': ('textbook', label, P(g, f))
sl = lambda g, f, label='Slides': ('slides', label, P(g, f))
mm = lambda f: ('mindmap', 'Mind map', M(f))

GRADES = [
 {'id': 'grade7', 'num': '7', 'label': 'Grade 7', 'mm_page': 'mindmappings7thgrade.html',
  'intro': 'First year of Biology. Start with microorganisms and how to get into EduPage.',
  'terms': [('Lessons', [
     L('', 'Microorganisms', mm('microorganisms.html')),
     L('', 'How to log in to EduPage', pdf('grade7', 'EdupageLogin.pdf', 'Guide')),
  ])]},
 {'id': 'grade8', 'num': '8', 'label': 'Grade 8', 'mm_page': 'mindmappings8thgrade.html',
  'intro': 'Plants as food factories: inside the leaf, chloroplasts and chlorophyll, photosynthesis, and how light intensity changes its rate.',
  'terms': [('Lessons', [
     L('6', 'Internal structure of the leaf', ('interactive', '3D simulation', 'simulations/grade8/6-leaf-structure-3d.html')),
     L('7', 'Chloroplast and chlorophyll', ('interactive', 'Interactive lab', 'simulations/grade8/7-chloroplast-chlorophyll-lab.html')),
     L('9', 'Photosynthesis: the plant’s food factory', ('interactive', 'Simulation', 'simulations/grade8/9-photosynthesis-food-factory.html')),
     L('10', 'Effect of light intensity on photosynthesis', ('interactive', 'Virtual lab', 'simulations/grade8/10-light-intensity-virtual-lab.html')),
  ])]},
 {'id': 'grade9', 'num': '9', 'label': 'Grade 9', 'mm_page': 'mindmappings9thgrade.html',
  'intro': 'Plants: how a leaf is built, chloroplasts and photosynthesis, flowers and pollination, the journey of a pollen grain, and seed germination.',
  'terms': [('Lessons', [
     L('1', 'Leaf structure', pdf('grade9', '1. Leaf Structure.pdf', 'Reading')),
     L('2', 'Chloroplasts and photosynthesis', pdf('grade9', '2. Chloroplast and Photosynthesis.pdf', 'Reading & worksheet')),
     L('6', 'Flowering plants and pollination', pdf('grade9', '6. Flowering Plants and Pollination.pdf', 'Textbook')),
     L('7', 'Pollen grains: structure and journey', pdf('grade9', '7. Pollen Grains - Structure and Journey.pdf', 'Textbook'), ('interactive', 'Interactive lab', 'simulations/grade9/7-pollen-grain-journey.html')),
     L('8', 'Seed germination', pdf('grade9', '8. Seed Germination.pdf', 'Textbook'), ('interactive', 'Simulation', 'simulations/grade9/8-seed-germination.html')),
  ])]},
 {'id': 'grade10', 'num': '10', 'label': 'Grade 10', 'mm_page': 'mindmappings10thgrade.html',
  'intro': 'The chemistry and structure of the cell, then the diversity of life from viruses to animals.',
  'terms': [
   ('First semester', [
     L('1', 'Chemical composition of the cell', pdf('grade10', '1. Chemical composition of the cell - Textbook.pdf', 'Textbook')),
     L('2', 'Organic molecules: the building blocks of life', pdf('grade10', '2.Organic Molecules The Building Blocks of Life - Textbook.pdf', 'Textbook')),
     L('3', 'Non-cellular forms', pdf('grade10', '3 Non-cellular forms - Textbook.pdf', 'Textbook')),
     L('4', 'Two basic cell types and their structure', pdf('grade10', '4. Two basic cell types and the structure - Textbook.pdf', 'Textbook'), sl('grade10', '4. Two basic cell types and the structure - Presentation.pdf')),
     L('5', 'Cell wall, cell membrane, cytoplasm and nucleus', pdf('grade10', '5. Basic cell structures.pdf')),
   ]),
   ('Second semester', [
     L('7.1', 'Viruses', pdf('grade10', '7.1 Viruses.pdf'), mm('viruses.html')),
     L('7.2', 'Bacteria', pdf('grade10', '7.2 Bacteria.pdf'), mm('bacteria.html')),
     L('8.1', 'Bacteria in your life', pdf('grade10', '8.1 Bacteria in your life.pdf'), mm('bacteriainyourlife.html')),
     L('8.2', 'Protists', pdf('grade10', '8.2 Protists.pdf'), mm('protists.html')),
     L('9.1', 'Fungi', pdf('grade10', '9.1 Fungi.pdf'), mm('MFungi.html')),
     L('9.2', 'Plants', pdf('grade10', '9.2 Plants.pdf'), mm('MPlants.html')),
     L('10.1', 'Seedless plants', pdf('grade10', '10.1 Seedless Plants.pdf'), mm('MSeedless plants.html')),
     L('10.2', 'Seed plants', pdf('grade10', '10.2 Seed Plants.pdf'), mm('MSeed plants.html')),
     L('11.1', 'Animals: general features', pdf('grade10', '11.1 Animals General.pdf'), mm('MAnimals General.html')),
     L('11.2', 'Sponges, cnidarians, flatworms and roundworms', pdf('grade10', '11.2 Sponges, Cnidarians, Flatworms, and Roundworms.pdf'), mm('MSponges, Cnidarians, Flatworms, and Roundworms.html')),
     L('12.1', 'Molluscs and segmented worms', pdf('grade10', '12.1 Mollusks and Segmented Worms.pdf'), mm('MMollusks and Segmented Worms.html')),
   ])]},
 {'id': 'grade11', 'num': '11', 'label': 'Grade 11', 'mm_page': 'mindmappings11thgrade.html',
  'intro': 'Biological molecules, cells and transport, DNA, cell division and genetics.',
  'terms': [
   ('First semester', [
     L('1', 'Water, solutions and mixtures', pdf('grade11', '1. Water solutions and mixtures.pdf')),
     L('2', 'The building blocks of life', pdf('grade11', '2. The building blocks of life.pdf')),
     L('3', 'Tests for biological molecules (lab)', pdf('grade11', '3. Tests for Biological Molecules - Lab.pdf', 'Lab sheet')),
     L('4', 'Prokaryotic cells', pdf('grade11', '4. Prokaryotic cell.pdf')),
     L('5', 'Eukaryotic cells', pdf('grade11', '5. Eukaryotic cell.pdf')),
     L('5.2', 'Cellular transport: active and passive', pdf('grade11', '5.2 Cellular Transport - Active and Passive.pdf'), ('interactive', 'PhET simulation', 'https://phet.colorado.edu/en/simulations/membrane-transport/about')),
     L('7.1', 'DNA', pdf('grade11', '7.1 - DNA.pdf')),
     L('7.2', 'DNA replication', pdf('grade11', '7.2 - DNA replication.pdf')),
   ]),
   ('Second semester', [
     L('9.1', 'Chromosome structure', pdf('grade11', '9.1 Chromosome structure.pdf'), mm('chromosomestructure.html')),
     L('9.2', 'Gene mutations', pdf('grade11', '9.2 Gene Mutations.pdf'), mm('genemutations.html')),
     L('10.1', 'Chromosomal mutations', pdf('grade11', '10.1 Chromosomal Mutations.pdf'), mm('chromosomalmutation.html')),
     L('10.2', 'DNA extraction', pdf('grade11', '10.2 DNA extraction.pdf')),
     L('11.1', 'The cell cycle', pdf('grade11', '11.1 Cell Cycle.pdf'), mm('cellcycle.html')),
     L('11.2', 'Mitosis', pdf('grade11', '11.2 Mitosis-The-Process-of-Cell-Division.pdf'), mm('mitosis.html'), ('interactive', 'Mitosis & meiosis simulation', 'https://labaids.s3.us-east-2.amazonaws.com/sgi-sims/mitosis-meiosis-sideways/index.html')),
     L('12.1', 'Meiosis', pdf('grade11', '12.1 Meiosis.pdf'), mm('meiosis.html')),
     L('13.1', 'Mendelian genetics', pdf('grade11', '13.1 Mendelian_Genetics.pdf')),
   ])]},
 {'id': 'grade12', 'num': '12', 'label': 'Grade 12', 'mm_page': 'mindmappings12thgrade.html',
  'intro': 'Human anatomy and physiology: skeleton, muscles, skin, blood, breathing, excretion and the nervous system.',
  'terms': [
   ('First semester', [
     L('1.1', 'The human body plan', pdf('grade12', '1.1 The Human Body Plan - Reading.pdf', 'Textbook'), sl('grade12', '1.1 The Human Body plan - Presentation.pdf')),
     L('1.2', 'The skeletal system', pdf('grade12', '1.2 The Skeletal System - Reading.pdf', 'Textbook'), sl('grade12', '1.2 The Skeletal System - Presentation.pdf')),
     L('1.3', 'The human skeleton: anatomy', pdf('grade12', '1.3 The Human Skeleton - anatomy - Reading.pdf', 'Textbook'), sl('grade12', '1.3 The Human Skeleton - anatomy - presentation.pdf')),
     L('2.1', 'The muscular system: structure and function', pdf('grade12', '2.1 The Muscular System - structure and function - Reading.pdf', 'Textbook'), sl('grade12', '2.1 The Muscular System - structure and function - Presentation.pdf')),
     L('3.1', 'Muscle–bone movement and muscle fatigue', pdf('grade12', '3.1 Muscle-bone movement and muscle fatigue - Textbook.pdf', 'Textbook'), sl('grade12', '3.1 Muscle-bone movement and muscle fatigue - Presentation.pdf')),
     L('3.2', 'The integumentary system', pdf('grade12', '3.2 The Integumentary System - Textbook.pdf', 'Textbook'), sl('grade12', '3.2 The Integumentary System - Presentation.pdf')),
   ]),
   ('Second semester', [
     L('', 'Blood composition', pdf('grade12', 'Blood Composition.pdf')),
     L('', 'Blood groups', pdf('grade12', 'Blood Groups.pdf'), pdf('grade12', 'Blood Types Exercise and Homework.pdf', 'Exercises & homework'), ('interactive', 'Blood typing game', 'https://www.labxchange.org/library/items/lb:LabXchange:9e1a1712:lx_simulation:1'), ('interactive', 'Compatibility chart', 'https://i0.wp.com/www.compoundchem.com/wp-content/uploads/2018/01/Blood-Types-Compatibilities.png?ssl=1')),
     L('', 'Respiratory system', pdf('grade12', 'Respiratory System - Main.pdf'), mm('Respiratory System.html')),
     L('', 'Excretory system', pdf('grade12', 'Excretory system - Main.pdf'), mm('Excretory System.html')),
     L('', 'Excretory system: water control', pdf('grade12', 'Excretory System - Water Control.pdf'), mm('Excretory System - Water Control.html')),
     L('', 'Excretory system disorders', pdf('grade12', 'Excretory System Disorders.pdf'), mm('Excretory System - Disorders.html')),
     L('13.1', 'Neurons and nerve impulses', pdf('grade12', '13.1 Neurons and nerve impulses.pdf'), mm('MNeurons and nerve impulses.html')),
     L('13.2', 'Neurons and nerve impulses, part 2', pdf('grade12', '13.2 Neurons and nerve impulses 1.pdf'), mm('MNeurons and nerve impulses 1.html')),
     L('', 'Central nervous system: the brain', mm('MCNS - Brain.html')),
     L('15.1', 'Central nervous system: the spinal cord', pdf('grade12', '15.1 CNS - Spinal Cord.pdf'), mm('MCNS - Spinal cord.html')),
     L('16.1', 'Sensory systems', pdf('grade12', '16.1 Sensory Systems.pdf'), mm('MSensory systems.html')),
     L('16.2', 'Sensory systems, part 2', pdf('grade12', '16.2 Sensory Systems.pdf'), mm('MSensory Systems 1.html')),
     L('17.1', 'Menstruation', pdf('grade12', '17.1 Menstruation.pdf'), mm('MMenstruation12.html')),
     L('17.2', 'Spermatogenesis', pdf('grade12', '17.2 Spermatogenesis.pdf')),
   ])]},
 {'id': 'grade13', 'num': '13', 'label': 'Grade 13', 'mm_page': 'mindmappings13thgrade.html',
  'intro': 'Cell biology, energy (photosynthesis and respiration), DNA, and homeostasis — State Matura preparation.',
  'terms': [
   ('First semester', [
     L('1', 'Prokaryotic cells', pdf('grade13', '1. Prokaryotic cell.pdf', 'Textbook')),
     L('2', 'Eukaryotic cells', pdf('grade13', '2. Eukaryotic cell.pdf', 'Textbook')),
     L('3', 'Viruses', pdf('grade13', '3. Viruses.pdf', 'Textbook')),
     L('4', 'Levels of organisation: cells to organism', pdf('grade13', '4. Level Of Organization - Cells to Organism.pdf', 'Textbook')),
     L('5', 'Cellular transport', pdf('grade13', '5. Cellular Transport.pdf', 'Textbook')),
     L('6', 'Photosynthesis', pdf('grade13', '6. Photosynthesis - Textbook.pdf', 'Textbook'), ('slides', 'Slides (PowerPoint)', P('grade13', '6. Photosynthesis.pptx'))),
     L('7', 'Aerobic (cellular) respiration', pdf('grade13', '7. Aerobic (cellular) respiration .pdf'), ('video', 'YouTube playlist', 'https://www.youtube.com/watch?v=7V2kRH0K8QU&list=PL3X4Gc6kV7xsm6VEUVNQYxuw3-XW24QLk&index=1')),
     L('8', 'Cell cycle, mitosis and meiosis', pdf('grade13', '8. Cell Cycle, Mitosis and Meiosis.pdf')),
     L('9', 'DNA and ATP', pdf('grade13', '9.DNA and ATP .pdf')),
     L('10', 'DNA replication', pdf('grade13', '10. DNA replication.pdf')),
   ]),
   ('Second semester', [
     L('', 'Homeostasis: principles', pdf('grade13', 'Homeostasis - Principles.pdf'), mm('Homeostasis.html')),
     L('', 'Ectotherms and endotherms', pdf('grade13', 'Ectotherms and Endotherms.pdf'), mm('Ectotherms and Endotherms.html')),
     L('', 'Osmoregulation', pdf('grade13', 'Osmoregulation.pdf'), mm('Osmoregulation.html')),
     L('', 'Neuron structure', pdf('grade13', 'Neurons Structure.pdf'), mm('Neuron structure.html')),
   ])]},
 {'id': 'ScienceClub', 'num': 'Science Club', 'label': 'Science Club', 'mm_page': None,
  'intro': 'Hands-on laboratory work for the school Science Club.',
  'terms': [('Lab exercises', [
     L('', 'Cell staining and microscopy', pdf('ScienceClub', 'Laboratory Exercises in Cell Staining and Microscopy.pdf', 'Lab manual')),
  ])]},
]

# extra mind-map files (duplicates) -> grade for back link
EXTRA_MM = {'CNS - Spinal cord.html': 'grade12', 'CNS - Brain.html': 'grade12', 'Sensory systems.html': 'grade12',
            'Sensory Systems 1.html': 'grade12', 'Neurons and nerve impulses.html': 'grade12',
            'Neurons and nerve impulses 1.html': 'grade12', 'Menstruation12.html': 'grade12'}

TYPE_LABEL = {'textbook': 'Reading (PDF)', 'slides': 'Slides', 'mindmap': 'Mind map', 'interactive': 'Interactive', 'video': 'Video'}

def res_html(res, b):
    out = []
    for r in res:
        h = r['href']
        ext = h.startswith(('http', 'simulations/')) or h.lower().endswith(('.pdf', '.pptx'))
        tgt = ' target="_blank" rel="noopener"' if ext else ''
        out.append(f'<li><a class="t-{r["type"]}" href="{E(b + u(h) if not h.startswith("http") else h)}"{tgt}><span class="dot"></span>{E(r["label"])}</a></li>')
    return '<ul class="res">' + ''.join(out) + '</ul>'

def count(g):
    return sum(len(ls) for _, ls in g['terms'])

def legend():
    return '<ul class="legend" aria-label="Resource types">' + ''.join(
        f'<li><span class="dot t-{k}"></span> {v}</li>' for k, v in TYPE_LABEL.items()) + '</ul>'

def build_grade(g):
    b = '../'
    terms = []
    for name, lessons in g['terms']:
        rows = ''.join(f'''
      <li class="lesson"><span class="code">{E(l["code"])}</span><span class="title">{E(l["title"])}</span>{res_html(l["res"], b)}</li>''' for l in lessons)
        terms.append(f'''
    <section class="term" aria-labelledby="t-{len(terms)}">
      <h2 id="t-{len(terms)}">{E(name)} <small>{len(lessons)} {"lesson" if len(lessons) == 1 else "lessons"}</small></h2>
      <ul class="lessons">{rows}
      </ul>
    </section>''')
    switch = ''.join(f'<a href="{x["id"]}.html"{" aria-current=\"page\"" if x is g else ""}>{E(x["num"] if x["num"].isdigit() else x["label"])}</a>' for x in GRADES)
    body = f'''
<div class="wrap">
  <header class="page-head">
    <p class="crumbs"><a href="studyingmaterials.html">Study materials</a> / {E(g["label"])}</p>
    <h1>{E(g["label"])}</h1>
    <p class="lede">{E(g["intro"])}</p>
    {legend()}
  </header>
  <div style="padding-bottom:96px">{"".join(terms)}
    <nav class="grade-switch" aria-label="Other grades"><span>Other grades</span>{switch}</nav>
  </div>
</div>'''
    page(SM + g['id'] + '.html', f'{g["label"]} Biology materials — Besir Zeneli',
         f'{g["label"]} Biology lessons: readings, slides, mind maps and simulations.', body, current='study')

def build_hub():
    b = '../'
    cards = ''.join(f'''
    <a href="{g["id"]}.html"><span class="num{" word" if not g["num"].isdigit() else ""}">{E(g["num"])}</span><span><span class="lab">{"Grade " + g["num"] if g["num"].isdigit() else "Extra-curricular"}</span><br><span class="cnt">{count(g)} {"lesson" if count(g) == 1 else "lessons"}</span></span></a>''' for g in GRADES)
    flat = []
    for g in GRADES:
        for _, ls in g['terms']:
            for l in ls:
                flat.append({**l, 'gradeLabel': g['label'], 'page': g['id'] + '.html'})
    with open(os.path.join(ROOT, 'assets/materials.js'), 'w', encoding='utf-8') as f:
        f.write('/* Generated list of every lesson, used by the search on the study page. */\nwindow.MATERIALS = ' + json.dumps(flat, ensure_ascii=False, indent=0) + ';\n')
    total = len(flat)
    body = f'''
<div class="wrap">
  <header class="page-head">
    <h1>Study materials</h1>
    <p class="lede">Readings, slides, mind maps and simulations for every Biology class I teach — {total} lessons, grades 7 to 13. Pick your grade, or search for a topic.</p>
  </header>
  <div class="search" role="search">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    <label for="study-search" class="skip">Search lessons</label>
    <input id="study-search" type="search" placeholder="Search lessons, e.g. mitosis, blood, photosynthesis" autocomplete="off" data-base="../">
  </div>
  <p id="search-status" class="search-status" aria-live="polite"></p>
  <div id="results"></div>
</div>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Choose your grade</h2><p>Each grade page lists the lessons in the order we cover them in class, with every resource for a lesson in one row.</p></div>
    <nav class="grade-picker" aria-label="Grades">{cards}
    </nav>
  </div>
</section>'''
    page(SM + 'studyingmaterials.html', 'Study materials — Besir Zeneli',
         'Biology study materials for grades 7–13: readings, slides, mind maps and simulations.', body, current='study',
         extra_js='<script src="../assets/materials.js"></script>\n')

def build_redirects():
    for g in GRADES:
        if not g['mm_page']:
            continue
        target = g['id'] + '.html'
        with open(os.path.join(ROOT, SM + g['mm_page']), 'w', encoding='utf-8') as f:
            f.write(f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>{g["label"]} mind maps</title>
<meta http-equiv="refresh" content="0; url={target}"><link rel="canonical" href="{target}"></head>
<body><p>Mind maps now sit next to each lesson on the <a href="{target}">{g["label"]} page</a>.</p></body></html>
''')

def restyle_mindmaps():
    mm_grade = dict(EXTRA_MM)
    titles = {}
    for g in GRADES:
        for _, ls in g['terms']:
            for l in ls:
                for r in l['res']:
                    if r['type'] == 'mindmap':
                        fn = r['href'][len(SM):]
                        mm_grade[fn] = g['id']
                        titles[fn] = l['title']
    label = {g['id']: g['label'] for g in GRADES}
    for fn, gid in mm_grade.items():
        p = os.path.join(ROOT, SM + fn)
        s = open(p, encoding='utf-8').read()
        # strip previous back-button styles/markup and any earlier injection
        s = re.sub(r'<style>(?:(?!</style>).)*?\.back-button(?:(?!</style>).)*?</style>', '', s, flags=re.S)
        s = re.sub(r'<footer>\s*(<div class="button-container">)?\s*<a [^>]*class="back-button"[^>]*>.*?</a>\s*(</div>)?\s*</footer>', '', s, flags=re.S)
        s = re.sub(r'<a [^>]*class="back-button"[^>]*>.*?</a>', '', s, flags=re.S)
        s = re.sub(r'<!-- bb:start -->.*?<!-- bb:end -->\s*', '', s, flags=re.S)
        title = titles.get(fn, os.path.splitext(fn)[0].lstrip('M') if fn.startswith('M') and fn[1:2].isupper() else os.path.splitext(fn)[0])
        s = re.sub(r'<title>.*?</title>', f'<title>{E(title)} — mind map · {label[gid]}</title>', s, count=1, flags=re.S)
        head_inj = ('<!-- bb:start --><link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@500;600&display=swap" rel="stylesheet">'
                    '<link rel="stylesheet" href="../assets/mindmap.css"><link rel="icon" type="image/png" href="../android-chrome-192x192.png"><!-- bb:end -->\n')
        s = s.replace('</head>', head_inj + '</head>', 1)
        bar = (f'<!-- bb:start --><nav class="mm-bar" aria-label="Mind map navigation"><a class="mm-back" href="{gid}.html">← {label[gid]} lessons</a>'
               f'<span class="mm-title">{E(title)}</span><span class="mm-hint">Drag to move · scroll to zoom · click a dot to fold</span></nav><!-- bb:end -->\n')
        s = s.replace('<body>', '<body>\n' + bar, 1)
        open(p, 'w', encoding='utf-8').write(s)
    return mm_grade

# =====================================================================
# WRITING
# =====================================================================
ESSAY5_META = {'file': 'essay5.html', 'kind': 'science', 'kind_label': 'Psychology & biology', 'date': '2026-11-24', 'date_h': '24 November 2026',
  'title': 'Why we do what we do', 'sub': 'the biology behind human behaviour',
  'summary': 'Following Robert Sapolsky, we trace a single act backwards in time: from the neurons that fired a second before, through hormones, childhood and genes, to culture and evolution. Biology and psychology turn out to be two descriptions of one story.',
  'author': 'Besir Zeneli'}

FIG_BRAIN = '''<figure>
<svg viewBox="0 0 640 400" role="img" aria-labelledby="fb-t" style="width:100%;height:auto;background:#fff;border-radius:14px">
<title id="fb-t">Side view of the brain showing the prefrontal cortex, amygdala, hippocampus and hypothalamus</title>
<path d="M120,210 C100,120 190,48 310,44 C430,40 540,92 548,190 C556,262 512,300 452,304 C420,330 360,334 330,318 C290,332 230,326 196,300 C150,292 126,258 120,210Z" fill="#f4eef8" stroke="#352a73" stroke-width="3"/>
<path d="M452,304 C500,300 532,326 520,352 C506,378 450,380 424,356 C412,342 420,320 452,304Z" fill="#ece6f4" stroke="#352a73" stroke-width="3"/>
<path d="M330,318 C334,344 330,372 318,396 L352,396 C356,370 360,344 360,322Z" fill="#ece6f4" stroke="#352a73" stroke-width="3"/>
<g fill="none" stroke="#b9aed6" stroke-width="2.5" stroke-linecap="round">
<path d="M200,120 C230,100 260,112 280,96"/><path d="M300,70 C320,96 300,120 330,136"/><path d="M360,62 C370,92 400,96 410,120"/><path d="M450,90 C440,120 470,140 460,170"/><path d="M500,150 C480,170 500,200 480,220"/><path d="M180,180 C210,170 220,196 250,186"/><path d="M380,170 C400,200 380,220 410,240"/>
</g>
<path d="M126,216 C110,140 170,80 238,68 C214,112 206,170 222,238 C190,248 150,246 126,216Z" fill="#352a73" opacity=".85"/>
<ellipse cx="300" cy="250" rx="20" ry="15" fill="#c9466f"/>
<path d="M318,252 C350,262 390,262 418,246" fill="none" stroke="#2f8f83" stroke-width="12" stroke-linecap="round"/>
<circle cx="292" cy="214" r="12" fill="#d08a1e"/>
<g font-family="Schibsted Grotesk, system-ui, sans-serif" font-size="19" font-weight="600" fill="#1d1b2c">
<line x1="170" y1="120" x2="70" y2="40" stroke="#1d1b2c" stroke-width="1.5"/><text x="12" y="30">Prefrontal cortex</text>
<line x1="300" y1="250" x2="250" y2="380" stroke="#1d1b2c" stroke-width="1.5"/><text x="150" y="394">Amygdala</text>
<line x1="400" y1="252" x2="560" y2="236" stroke="#1d1b2c" stroke-width="1.5"/><text x="632" y="226" text-anchor="end">Hippocampus</text>
<line x1="292" y1="214" x2="380" y2="150" stroke="#1d1b2c" stroke-width="1.5"/><text x="340" y="140">Hypothalamus</text>
</g>
</svg>
<figcaption>Four brain regions that keep appearing in the story of behaviour (simplified, not to scale). The prefrontal cortex is the brake; the amygdala is the alarm; the hippocampus stores context; the hypothalamus links the brain to hormones.</figcaption>
</figure>'''

FIG_TIMELINE = '''<figure>
<ol class="tl">
<li><b>One second before</b><span>Which neurons fired? The amygdala, the prefrontal cortex, the reward system.</span></li>
<li><b>Seconds to minutes before</b><span>What did we see, hear or smell? Many cues act without our awareness.</span></li>
<li><b>Hours to days before</b><span>Hormones: cortisol, testosterone, oxytocin change how sensitive the brain is.</span></li>
<li><b>Days to months before</b><span>Neuroplasticity: stress, love or trauma physically reshape neurons.</span></li>
<li><b>Adolescence</b><span>The prefrontal cortex is the last region to mature, in the mid-twenties.</span></li>
<li><b>Childhood and the womb</b><span>Early care, nutrition and stress set lifelong patterns.</span></li>
<li><b>Genes</b><span>Not destiny: genes shape how strongly we react to the environment.</span></li>
<li><b>Centuries before</b><span>Culture: the values and habits of the society we grow up in.</span></li>
<li><b>Millions of years before</b><span>Evolution: why our species has these brains and hormones at all.</span></li>
</ol>
<figcaption>Sapolsky’s question, step by step: to explain one act, keep asking “and what came before that?”</figcaption>
</figure>'''

FIG_HPA = '''<figure>
<svg viewBox="0 -40 640 320" role="img" aria-labelledby="fh-t" style="width:100%;height:auto;background:#fff;border-radius:14px">
<title id="fh-t">The stress response: amygdala signals the hypothalamus, then the pituitary and adrenal glands release cortisol, which feeds back to switch the system off</title>
<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10z" fill="#352a73"/></marker>
<marker id="ah2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10z" fill="#c9466f"/></marker></defs>
<g font-family="Schibsted Grotesk, system-ui, sans-serif" font-size="19" font-weight="600" text-anchor="middle">
<rect x="20" y="40" width="170" height="64" rx="14" fill="#fbe6ed" stroke="#c9466f" stroke-width="2.5"/><text x="105" y="70" fill="#1d1b2c">Amygdala</text><text x="105" y="92" font-size="15" font-weight="400" fill="#615e74">“danger!”</text>
<rect x="235" y="40" width="170" height="64" rx="14" fill="#e9e6f5" stroke="#352a73" stroke-width="2.5"/><text x="320" y="70" fill="#1d1b2c">Hypothalamus</text><text x="320" y="92" font-size="15" font-weight="400" fill="#615e74">CRH</text>
<rect x="450" y="40" width="170" height="64" rx="14" fill="#e9e6f5" stroke="#352a73" stroke-width="2.5"/><text x="535" y="70" fill="#1d1b2c">Pituitary</text><text x="535" y="92" font-size="15" font-weight="400" fill="#615e74">ACTH</text>
<rect x="450" y="200" width="170" height="64" rx="14" fill="#e9e6f5" stroke="#352a73" stroke-width="2.5"/><text x="535" y="230" fill="#1d1b2c">Adrenal glands</text><text x="535" y="252" font-size="15" font-weight="400" fill="#615e74">cortisol, adrenaline</text>
<rect x="235" y="200" width="170" height="64" rx="14" fill="#fff6e5" stroke="#d08a1e" stroke-width="2.5"/><text x="320" y="230" fill="#1d1b2c">Body</text><text x="320" y="252" font-size="15" font-weight="400" fill="#615e74">energy for action</text>
<rect x="20" y="200" width="170" height="64" rx="14" fill="#e3f2ef" stroke="#2f8f83" stroke-width="2.5"/><text x="105" y="230" fill="#1d1b2c">Prefrontal cortex</text><text x="105" y="252" font-size="15" font-weight="400" fill="#615e74">“calm down”</text>
</g>
<g stroke="#352a73" stroke-width="3" fill="none">
<line x1="192" y1="72" x2="230" y2="72" marker-end="url(#ah)"/><line x1="407" y1="72" x2="445" y2="72" marker-end="url(#ah)"/><line x1="535" y1="106" x2="535" y2="195" marker-end="url(#ah)"/><line x1="448" y1="232" x2="410" y2="232" marker-end="url(#ah)"/>
<line x1="105" y1="198" x2="105" y2="110" stroke="#2f8f83" marker-end="url(#ah)"/>
</g>
<path d="M622,232 L634,232 L634,12 L320,12 L320,34" fill="none" stroke="#c9466f" stroke-width="2.5" stroke-dasharray="7 6" marker-end="url(#ah2)"/>
<text x="420" y="-8" font-family="Schibsted Grotesk, system-ui, sans-serif" font-size="15" fill="#c9466f" text-anchor="middle">negative feedback: cortisol switches the alarm off</text>
<text x="120" y="160" font-family="Schibsted Grotesk, system-ui, sans-serif" font-size="15" fill="#2f8f83">brake</text>
</svg>
<figcaption>The stress response (HPA axis). In a short emergency it saves us; when it never switches off, it slowly harms the body and the brain.</figcaption>
</figure>'''

ESSAY5_BODY = f'''
<p>Imagine a moment. A student slams the classroom door. Another one helps a classmate pick up dropped books. A third freezes in the middle of an exam. We usually explain these moments with one word: <em>anger</em>, <em>kindness</em>, <em>anxiety</em>. Psychology names the behaviour. Biology asks what physically made it happen. For a long time the two subjects sat in separate buildings. The neurobiologist Robert Sapolsky has spent his career showing that they are two descriptions of the same story.</p>

<h2>Turning the camera backwards</h2>
<p>In his book <em>Behave</em> (2017), Sapolsky uses a simple method. Take any act and ask: what happened one second before? Which neurons fired? Then step further back. What did the person see, hear or smell in the minutes before? Which hormones were acting during the previous hours and days? How had the brain changed during the previous months? What happened in adolescence, in childhood, even in the womb? Which genes were involved, what culture shaped the person, and what did evolution build over millions of years?</p>
{FIG_TIMELINE}
<p>The method is powerful because it removes a false choice. The question is never “is it biology <em>or</em> environment?” Every level shapes the next one. An experience becomes a change in neurons; a hormone changes how we react to an experience; a culture decides which experiences we have in the first place.</p>

<h2>The alarm and the brake</h2>
<p>Two brain regions appear again and again. The <strong>amygdala</strong>, deep in the temporal lobe, reacts fast to threat. It is the brain’s alarm. The <strong>prefrontal cortex</strong>, behind the forehead, holds back the impulses that would make us do something we regret. Sapolsky describes its job as making us do the harder thing when it is the right thing.</p>
{FIG_BRAIN}
<p>This is where psychology meets anatomy. What a teacher calls “self-control” has an address. And like any tissue, the prefrontal cortex can be tired: when we are hungry, sleep-deprived or stressed, it works less well, and the alarm wins more often. It is also the last part of the brain to finish maturing, usually in the mid-twenties. Teenagers are not simply “badly behaved”; they are using a brake that is still being built.</p>

<h2>Hormones change the volume, not the song</h2>
<p>Hormones act over hours and days. They rarely <em>create</em> a behaviour; more often they amplify what is already there. Testosterone, for example, does not make a calm person aggressive out of nowhere. It tends to strengthen whatever behaviour earns status in that situation. Oxytocin, often called the “love hormone”, increases trust and bonding, but mostly towards people we see as part of our own group.</p>
<p>The clearest example is stress. When the amygdala sounds the alarm, the hypothalamus, the pituitary and the adrenal glands release <strong>cortisol</strong> and <strong>adrenaline</strong>. Glucose rises and the heart beats faster: perfect for running from a lion. Sapolsky’s famous point is that zebras don’t get ulcers, because their stress lasts minutes. Humans can switch the same response on for months, just by thinking about rent, exams or the future.</p>
{FIG_HPA}
<p>Chronic stress has measurable effects on the brain. It can weaken the hippocampus, which is important for memory, and strengthen the amygdala. The result is a brain that learns less and fears more. Sapolsky’s years of field work on baboons in Kenya showed something similar: the health of an animal depended strongly on its social rank and on how much control and support it had.</p>

<h2>Early life and genes</h2>
<p>Further back, childhood leaves deep marks. Children who grow up with chronic stress, poverty or neglect often develop a more reactive stress system and a slower-maturing prefrontal cortex. This is not a moral failing; it is biology responding to an environment.</p>
<p>Genes matter too, but rarely in the way people imagine. There is no gene “for” aggression or kindness. Most genes change <em>how sensitive</em> we are to the environment. The same version of a gene can lead to problems in a harsh childhood and to no problems at all in a supportive one. Genes load the dice; the environment decides how often they are thrown.</p>

<h2>Culture and evolution</h2>
<p>At the widest level, culture tells us which behaviours are honoured and which are shameful, and evolution explains why our species has these brains, hormones and social instincts at all. We evolved as a social primate. Cooperation, fairness and empathy are as much part of that inheritance as fear and aggression.</p>

<h2>What this means for us</h2>
<p>Sapolsky pushes his argument very far. In <em>Determined</em> (2023) he concludes that, once all these causes are counted, there is no room left for free will. Many philosophers and scientists disagree, and the debate is far from settled. But even if we stop before his final conclusion, the framework changes how we look at people.</p>
<p>For a teacher, it is a lesson in humility. The student who slammed the door may have slept four hours, faced a crisis at home, or carried years of stress in a body that has learned to expect danger. Understanding the biology is not the same as excusing the behaviour. It is a better starting point for changing it: more sleep, less fear, more support, and a classroom where the brake has a chance to work.</p>
<p class="callout"><strong>The key idea:</strong> behaviour is never caused by a single thing. It is the last link in a chain that runs from neurons and hormones to childhood, culture and evolution. Psychology and biology are two ways of reading the same chain.</p>
<p class="source">Further reading: Robert M. Sapolsky, <em>Behave: The Biology of Humans at Our Best and Worst</em> (Penguin Press, 2017); <em>Determined: A Science of Life Without Free Will</em> (Penguin Press, 2023); <em>Why Zebras Don’t Get Ulcers</em> (3rd ed., 2004). Sapolsky’s Stanford course “Human Behavioral Biology” is freely available on YouTube.<br>Diagrams drawn for this essay; simplified, not to scale.</p>'''


ESSAYS = [
 ESSAY5_META,
 {'file': 'essay4.html', 'kind': 'science', 'kind_label': 'Science', 'date': '2025-11-05', 'date_h': '5 November 2025',
  'title': 'Silent killers', 'sub': 'the strange world of prions',
  'summary': 'Prions carry no DNA or RNA, yet a single misfolded protein can turn healthy proteins into copies of itself and destroy the brain. A look at Creutzfeldt–Jakob disease, mad cow disease, scrapie and kuru — and why prions are so hard to kill.',
  'author': 'Ayşegül Sarıarslan, student at Maarif International Schools · mentored by Besir Zeneli'},
 {'file': 'essay3.html', 'kind': 'science', 'kind_label': 'Science', 'date': '2025-02-02', 'date_h': '2 February 2025',
  'title': 'Asteroid Bennu’s secrets', 'sub': 'building blocks of life found in space',
  'summary': 'Uncontaminated samples from asteroid Bennu, returned by NASA’s OSIRIS-REx, hold ammonia, amino acids and all five DNA and RNA bases. They do not prove life came from space, but they show its ingredients may be common across the solar system.',
  'author': 'Besir Zeneli'},
 {'file': 'essay1.html', 'kind': 'science', 'kind_label': 'Human biology', 'date': '2025-02-02', 'date_h': '2 February 2025',
  'title': 'Understanding stress', 'sub': 'a survival mechanism and a health risk',
  'summary': 'Cortisol, adrenaline and noradrenaline prepared our ancestors to fight or flee. In short bursts the response helps us; kept switched on by modern life, it drives diabetes, heart disease and weakened immunity.',
  'author': 'Besir Zeneli'},
 {'file': 'essay2.html', 'kind': 'philosophy', 'kind_label': 'Philosophy · translation', 'date': '2025-02-02', 'date_h': '2 February 2025',
  'title': 'Beyond the horizon and beyond', 'sub': 'from a metaphysical perspective',
  'summary': 'Sezai Karakoç asks whether eating animals is a right or a blessing, and what responsibility comes with the power humans hold over the living world. Translated from Turkish.',
  'author': 'Sezai Karakoç · translated by Besir Zeneli (2016)'},
]

def essay_list_html(items, b=''):
    return '<ul class="essay-list">' + ''.join(f'''
  <li class="essay-item" data-kind="{e["kind"]}"><a href="{b}{e["file"]}">
    <span class="meta"><b>{E(e["kind_label"])}</b><time datetime="{e["date"]}">{E(e["date_h"])}</time></span>
    <span><h3>{E(e["title"])}: <span>{E(e["sub"])}</span></h3><p>{E(e["summary"])}</p></span>
  </a></li>''' for e in items) + '\n</ul>'

def build_writings():
    body = f'''
<div class="wrap">
  <header class="page-head">
    <h1>Writing</h1>
    <p class="lede">Essays on biology, behaviour, the human body and the questions around them — plus a translation I return to often. Some are written with my students.</p>
  </header>
  <div class="filters" data-filters role="group" aria-label="Filter essays">
    <button type="button" data-filter="all" aria-pressed="true">All</button>
    <button type="button" data-filter="science" aria-pressed="false">Science</button>
    <button type="button" data-filter="philosophy" aria-pressed="false">Philosophy</button>
  </div>
  <div style="padding:24px 0 104px">{essay_list_html(ESSAYS)}</div>
</div>'''
    page('writings.html', 'Writing — Besir Zeneli', 'Essays by Besir Zeneli on biology, the human body, and philosophy.', body, current='writing')

def build_essay(e, content):
    i = ESSAYS.index(e)
    nxt = ESSAYS[(i + 1) % len(ESSAYS)]
    body = f'''
<article class="essay">
  <header class="essay-head">
    <p class="crumbs"><a href="writings.html">Writing</a> / {E(e["kind_label"])}</p>
    <h1>{E(e["title"])}: {E(e["sub"])}</h1>
    <p class="byline"><strong>{E(e["author"])}</strong><br><time datetime="{e["date"]}">{E(e["date_h"])}</time></p>
  </header>
  <div class="essay-body">
{content}
  </div>
  <nav class="essay-foot" aria-label="More writing">
    <a class="btn btn-line" href="writings.html">← All writing</a>
    <a class="btn btn-line" href="{nxt["file"]}">Next: {E(nxt["title"])}</a>
  </nav>
</article>'''
    page(e['file'], f'{e["title"]}: {e["sub"]} — Besir Zeneli', e['summary'], body, current='writing')

def fig(src, alt):
    return f'<figure><img src="{src}" alt="{E(alt)}" loading="lazy"></figure>'

ESSAY_BODIES = {
'essay5.html': ESSAY5_BODY,
'essay1.html': f'''
{fig("assets/img/stress-brain.jpg", "Illustration of the brain under stress")}
<p>Stress is a necessary and useful life mechanism. While this may sound contradictory, it’s crucial for survival.</p>
<p>In primitive conditions, humans, like other animals, faced dangerous situations with two options: <strong>fight or flight</strong>. Survival depended on these responses.</p>
{fig("assets/img/fight-or-flight.jpg", "The fight-or-flight response")}
<p>During stress, the brain activates mechanisms that signal the <strong>adrenal glands</strong>. These glands release <strong>cortisol</strong>, which promotes glucose release into the bloodstream — a vital energy source for “fight or flight.”</p>
<p><strong>Adrenaline and noradrenaline</strong> are also released. Adrenaline increases heart rate and blood flow, while noradrenaline constricts blood vessels, diverting blood to the brain and muscles, enhancing performance. Breathing rate increases, and pupils dilate for better vision.</p>
{fig("assets/img/adrenal-glands.jpg", "The adrenal glands above the kidneys")}
<p>In short, under stress, blood sugar and energy rise, blood circulation and pressure accelerate, and physical performance can increase significantly. This is a natural “doping” mechanism inherited from our ancestors.</p>
<p>While beneficial in short bursts, chronic stress is harmful. Modern life often creates a constant state of perceived danger, making stress a permanent condition.</p>
{fig("assets/img/modern-stress.jpg", "Stress in modern life")}
<p>Prolonged stress disrupts the body’s helpful mechanisms, leading to various diseases. High cortisol levels can cause diabetes and weaken the immune system, increasing the risk of infections, cancer, and autoimmune diseases.</p>
<p>Adrenaline and noradrenaline can lead to hypertension and atherosclerosis, increasing the risk of heart attack, stroke, and dementia. Stress hormones also disrupt sleep, causing insomnia and fatigue.</p>
<p>Chronic stress has far-reaching negative effects. It’s crucial to identify and manage stress triggers. Self-understanding and stress-relieving activities are essential.</p>
<h2>How do we prevent chronic stress?</h2>
<p>Human biology, programmed for “fight or flight,” struggles to adapt to modern socio-political factors like income insecurity, job loss, and debt. These create persistent stress, difficult to escape.</p>
<p>This chronic stress of modern life overwhelms our biology. Our bodies struggle to cope with the resulting diseases.</p>
<p>Perhaps a collective effort is needed to address this “pandemic” of cortisol. Psychological and socio-political approaches may offer solutions.</p>
<p class="source">Reference: Lehninger, <em>Principles of Biochemistry</em>.<br>Written by Besir Zeneli, BSc in Biological Sciences.</p>''',

'essay2.html': f'''
{fig("assets/img/horizon.jpg", "A figure looking towards a distant horizon")}
<p>We feed, protect, and cultivate animals, and in the end, we slaughter them. Yes, we slaughter them, and then we nourish ourselves. Let’s take a moment to reflect on this! To live, we end another life. Do not assume this is our natural right. The Qur’an reminds us that certain types of meat are permitted for us to consume. God has made it lawful (halal) to eat certain meats. Can we understand the significance of this?</p>
<p>It means that the meat of specific animals has been made permissible for us, whereas it could have been prohibited. If it were forbidden, consider the significance and blessing of it being allowed. Reflect on this deeply. Ending the life of an animal is a great power — should we take it for granted? Many cultures live without eating meat, implying that it is not essential for life or survival.</p>
<p>It feels natural to us because we have grown accustomed to it since childhood. But based on this reasoning, we cannot claim that slaughtering animals is our natural right. If it were, the Holy Book would not emphasize it. It does not say the same about drinking water or eating bread, yet it specifically mentions meat.</p>
<p>Therefore, we should not consider this as our inherent right, but as a gift from the Creator-God. This is such a great blessing that, upon deep reflection, even the sacrifice of blood is permitted. Just think about the immense responsibility this places on us! All the gifts we enjoy — earth, mountains, rivers — are they truly for our benefit alone?</p>
<p>Every creature sacrifices more than it receives, sometimes even its entire existence. Can humanity be the only exception? How is this possible? As awareness and perception grow, so does our responsibility and duty. The greater the blessing, the greater the sacrifice required. Does the life of a lesser being have no value, while only human life matters?</p>
<p>The purpose of life, not life itself, is what matters. If plants and animals sacrifice their lives for humans, and if their purpose is this, why should we be an exception to this order? If we are wiser, more logical, and stronger, shouldn’t our responsibility and sacrifice be greater?</p>
<p>If we observe the world around us, we see that all things are subject to humanity. Imagine if all animals united against us — yet they do not have the power to do so. This power has been given only to humans, for the greatest sacrifice is expected from us. The Earth and the Sky have been entrusted to us so that we may show our sacrifice as stewards of goodness.</p>
<p>Man’s responsibility is immense. Not only does he have responsibility to living and non-living things, but most importantly, to the Creator who gave him these blessings. Does man truly deserve these gifts? This should be the central question for humanity.</p>
<p>Plants sacrifice their lives for animals, animals for humans — then the question is: Can humanity sacrifice itself to elevate civilization, as the Creator has entrusted us with this responsibility as Stewards?</p>
<p class="source">Sezai Karakoç, “Beyond the Horizon and Beyond from a Metaphysical Perspective.”<br>Translated by Besir Zeneli, June 2016.</p>''',

'essay3.html': f'''
{fig("assets/img/bennu.jpg", "Asteroid Bennu sample being examined in a laboratory")}
<p>Scientists have made an exciting discovery that could help us understand how life began — not just on Earth, but possibly elsewhere in the universe. Samples collected from asteroid Bennu, brought back by NASA’s OSIRIS-REx spacecraft, contain ingredients essential for life. While this doesn’t prove life came from space, it reveals the universe might be full of the tools needed to create it.</p>
<h2>Why Bennu’s samples are special</h2>
<p>For decades, scientists studied meteorites (space rocks that land on Earth) to find clues about life’s origins. The problem? Meteorites get contaminated when they crash through Earth’s atmosphere. Heat, impact, and exposure to our environment make it hard to confirm if their contents truly came from space.</p>
<p><strong>Bennu’s samples are different.</strong> OSIRIS-REx collected them directly from the asteroid in 2020 and sealed them in a protective capsule, which landed in 2023, shielding them from Earth’s contaminants. This makes Bennu’s rocks the “purest” space samples we’ve ever analyzed.</p>
<h2>Key discoveries in the space dust</h2>
<ul>
<li><strong>Ammonia overload:</strong> about 75× more ammonia than the samples from asteroid Ryugu</li>
<li><strong>Amino acids:</strong> 33 in total — 14 of the 20 that life on Earth uses to build proteins, and 19 that life does not use</li>
<li><strong>Genetic letters:</strong> all five nucleobases found in DNA and RNA</li>
<li><strong>Saltwater history:</strong> evidence of ancient liquid water reactions</li>
</ul>
{fig("assets/img/amino-acids.jpg", "Molecular diagram of amino acid structures")}
<h2>The life recipe connection</h2>
<p>While Bennu’s samples contain life’s ingredients, this doesn’t confirm the <strong><em>panspermia</em> hypothesis</strong> (life spreading through asteroids). What it does show is that asteroids could have delivered life’s raw materials to Earth. We have found the building blocks, but we still don’t know how they were assembled into living things.</p>
<h2>Looking beyond Bennu</h2>
<p>Scientists are now targeting icy moons like Jupiter’s Europa and Saturn’s Enceladus. NASA’s Europa Clipper, launched in October 2024, will explore the moon’s subsurface ocean — a potential hotspot for alien life. Where there is liquid water and organic molecules, the chemistry of life becomes possible.</p>
<h2>A time capsule for future science</h2>
<p>Only 30% of Bennu’s samples have been analyzed. The rest are preserved for future generations using technology we haven’t invented yet. This is a good argument that shows how we still study Moon rocks collected in the 1970s with modern tools.</p>
<p class="source">Scientific reference: <a href="https://www.nature.com/articles/s41550-024-02472-9" target="_blank" rel="noopener">original study in <em>Nature Astronomy</em></a>.</p>''',

'essay4.html': '''
<h2>What is a prion?</h2>
<p>Prions are among the most mysterious and dangerous agents known to science. Unlike any other infectious organism, prions have no DNA or RNA. They are not viruses, bacteria, or fungi. A prion is simply a misfolded protein, yet it has the power to destroy one of the most complex organs in the body — the brain.</p>
<p>Normally, the PrP protein found in our bodies is harmless and helps nerve cells function. However, when a prion appears, it changes the shape of the normal PrP proteins, turning them into more prions. This creates a chain reaction, where each abnormal protein causes others to misfold, leading to spongy holes in the brain tissue. Because of this, prion diseases are called spongiform encephalopathies.</p>
<p>In humans, the most well-known prion disease is Creutzfeldt–Jakob disease (CJD). In animals, they cause diseases such as mad cow disease (BSE) and scrapie in sheep.</p>
<p>What makes prions truly fascinating is their resistance — they can survive heat, radiation, and disinfectants that would normally destroy other infectious agents. In many cases, it’s almost impossible to eliminate them completely.</p>
<h2>The best-known prion diseases</h2>
<h3>1. Creutzfeldt–Jakob disease (CJD) — in humans</h3>
<p>This is the most common prion disease in humans. It causes slow but deadly brain degeneration. Symptoms include memory loss, loss of balance, personality changes, and muscle stiffness.</p>
<ul>
<li><strong>Sporadic CJD:</strong> appears spontaneously (the most common form).</li>
<li><strong>Familial CJD:</strong> inherited through a genetic mutation.</li>
<li><strong>Variant CJD (vCJD):</strong> can occur after eating meat from cows infected with mad cow disease (BSE).</li>
</ul>
<p>CJD usually progresses rapidly and, unfortunately, has no cure.</p>
<h3>2. Mad cow disease (bovine spongiform encephalopathy, BSE) — in cows</h3>
<p>This disease first appeared in the United Kingdom in the 1980s. Cows became infected after eating animal feed contaminated with prions.</p>
<p>Infected cows develop spongy holes in their brains, causing them to act confused, uncoordinated, and aggressive — which is why it’s called “mad cow disease.” Humans who eat meat from infected cows can develop variant CJD (vCJD).</p>
<h3>3. Scrapie — in sheep</h3>
<p>Scrapie is a prion disease known for centuries. It damages the brain and spinal cord of sheep. One of the most unusual symptoms is that sheep rub their bodies against walls or fences, which is why it’s called “scrapie.”</p>
<p>Interestingly, scrapie does not infect humans, but it has helped scientists understand diseases like BSE and CJD.</p>
<p class="callout"><strong>Interesting fact:</strong> some scientists describe prions as “immortal proteins” because they can survive in nature for many years without breaking down. This makes them both fascinating and terrifying.</p>
<h2>Kuru — the prion disease linked to cannibalism</h2>
<p>Kuru is a rare but historically important prion disease found in humans. It was discovered in the mid-1900s among the Fore tribe in Papua New Guinea.</p>
<p>In this tribe, people practiced ritual cannibalism — during funeral ceremonies, they ate the bodies of their deceased relatives to show love and respect. Women and children, who often ate the brain tissue, unknowingly consumed infectious prion proteins. Once inside the body, these prions slowly destroyed brain tissue.</p>
<p>The word “Kuru” means “to shake” in the Fore language, referring to the uncontrollable trembling that patients developed. Patients would:</p>
<ul>
<li>Lose the ability to walk or stand</li>
<li>Experience sudden fits of laughter or crying</li>
<li>Eventually lose control of speech and movement</li>
</ul>
<p>Sadly, the disease was always fatal. After the practice of cannibalism was banned, Kuru almost completely disappeared.</p>
<p class="callout"><strong>Interesting fact:</strong> the study of Kuru helped scientists understand how prion diseases work, leading to major discoveries about Creutzfeldt–Jakob disease (CJD) and mad cow disease (BSE).</p>
<h3>Kuru at a glance</h3>
<p><em>What it is:</em> an infectious, neurological, and degenerative disease caused by abnormal proteins called prions.<br>
<em>Causes:</em> it was transmitted to humans through the funerary cannibalism tradition practiced by the Fore tribe in Papua New Guinea.<br>
<em>First stage:</em> body tremors (the word “kuru” comes from this symptom), difficulty walking, and stuttering while speaking.<br>
<em>Second stage:</em> inability to walk without support, severe trembling, muscle loss, and uncontrollable laughter (“laughing disease”).<br>
<em>Third stage:</em> inability to sit, loss of speech, loss of bladder control, and unresponsiveness.<br>
<em>Today:</em> Kuru is considered an extinct illness, as the last known patient died in 2005.</p>
<p>With the advancement of modern technology, the number of unknown and untreatable diseases has significantly decreased. However, there are still some diseases that remain.</p>
<p class="source">Written by Ayşegül Sarıarslan, student at Maarif International Schools. Mentor: Besir Zeneli, BSc.</p>''',
}

# =====================================================================
# HOME
# =====================================================================
def build_home():
    socials = ''.join(f'<a href="{h}" target="_blank" rel="noopener">{n}</a>' for n, h in SOCIALS)
    total = sum(count(g) for g in GRADES)
    body = f'''
<section class="hero">
  <div class="wrap">
    <div>
      <h1>Besir<br>Zeneli</h1>
      <p class="role">Biology teacher and molecular biologist in Skopje.</p>
      <p class="role-sub">I teach grades 7 to 13 at Maarif International Schools, lead our Science Department, and spent over two years running Real-Time PCR diagnostics in a clinical lab. This site holds my class materials, my writing and my CV.</p>
      <div class="hero-actions">
        <a class="btn btn-solid" href="{SM}studyingmaterials.html">Open study materials</a>
        <a class="btn btn-line" href="Portfolio.html">Read my CV</a>
      </div>
    </div>
    <figure class="scope" style="margin:0">
      <div class="scope-field"><canvas id="scope" aria-label="Animated view of stained tissue under a microscope" role="img"></canvas></div>
      <figcaption class="scope-caption"><span>Epithelial tissue, H&amp;E stain</span><span>×400</span></figcaption>
    </figure>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Where would you like to go?</h2><p>The site has three parts. Students usually want the first one.</p></div>
    <ul class="routes">
      <li><a href="{SM}studyingmaterials.html"><span class="who">Students</span><span class="what">Study materials<small>{total} lessons for grades 7–13: readings, slides, mind maps and simulations, searchable by topic.</small></span><span class="go">Open</span></a></li>
      <li><a href="writings.html"><span class="who">Readers</span><span class="what">Writing<small>Essays on the biology of behaviour, prions, asteroid chemistry and stress, and a translation of Sezai Karakoç.</small></span><span class="go">Read</span></a></li>
      <li><a href="Portfolio.html"><span class="who">Colleagues</span><span class="what">CV<small>Teaching, department leadership, molecular diagnostics and education. Downloadable as PDF.</small></span><span class="go">View</span></a></li>
    </ul>
  </div>
</section>

<section class="section" id="about">
  <div class="wrap about">
    <figure>
      <img src="assets/img/portrait.jpg" alt="Besir Zeneli in a lab coat in a school biology laboratory" width="818" height="997" loading="lazy">
      <figcaption>In the school lab, Skopje.</figcaption>
    </figure>
    <div class="text">
      <h2>About me</h2>
      <p>I studied Biology at Hacettepe University in Ankara, graduating as an honour student, and then worked as a molecular biologist at VFV Laboratory in Skopje, running Real-Time PCR diagnostics for SARS-CoV-2 and HPV through the pandemic. I am now completing an MSc in Phytochemistry &amp; Natural Products at Mother Teresa University.</p>
      <p>Since 2021 I have taught Biology at Maarif International Schools, where I now lead the Science Department and prepare my gymnasium class for the State Matura. In class I care less about memorising isolated facts and more about helping students observe, question, connect evidence and think for themselves — which is why I have built more than 20 interactive simulations for my lessons.</p>
      <p>Outside the classroom I translate books, make Biology videos and posts as @biobesir, and run — I was national U19 champion in the 800 m and 1500 m.</p>
      <blockquote>“Science is the poetry of reality.”<cite>Richard Dawkins</cite></blockquote>
      <dl class="facts">
        <div><dt>Based in</dt><dd>Skopje, North Macedonia</dd></div>
        <div><dt>Teaching</dt><dd>Biology, grades 7–13</dd></div>
        <div><dt>Languages</dt><dd>Albanian, Macedonian, Turkish, English, German</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Latest writing</h2><p><a href="writings.html">See all essays</a></p></div>
    {essay_list_html(ESSAYS[:3])}
  </div>
</section>

<section class="section" id="contact">
  <div class="wrap contact">
    <div>
      <h2>Get in touch</h2>
      <p style="color:var(--muted);margin-top:14px;max-width:44ch">For teaching, science projects, collaborations or questions about the materials.</p>
    </div>
    <div>
      <a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
      <div class="socials">{socials}</div>
    </div>
  </div>
</section>'''
    page('index.html', 'Besir Zeneli — Biology teacher and molecular biologist',
         'Besir Zeneli teaches Biology at Maarif International Schools in Skopje. Study materials for grades 7–13, essays and CV.', body)

# =====================================================================
# CV
# =====================================================================
def build_cv():
    def role(when, title, org, bullets, tags=()):
        b = ('<ul>' + ''.join(f'<li>{x}</li>' for x in bullets) + '</ul>') if bullets else ''
        t = ('<ul class="chips">' + ''.join(f'<li>{x}</li>' for x in tags) + '</ul>') if tags else ''
        return f'<li class="role-item"><span class="when">{when}</span><h3>{title}</h3><p class="org">{org}</p>{b}{t}</li>'
    chips = lambda xs: '<ul class="chips">' + ''.join(f'<li>{x}</li>' for x in xs) + '</ul>'
    body = f'''
<div class="wrap">
  <header class="page-head">
    <h1>Curriculum vitae</h1>
    <p class="lede">Biology educator, molecular biologist and science communicator.</p>
    <div class="hero-actions" style="margin-top:26px">
      <a class="btn btn-solid" href="assets/Besir_Zeneli_CV.pdf" download>Download CV (PDF)</a>
      <a class="btn btn-line" href="mailto:{EMAIL}">Email me</a>
    </div>
  </header>
  <div class="cv">
    <aside class="cv-side">
      <img class="headshot" src="assets/img/headshot.jpg" alt="Besir Zeneli" width="480" height="480">
      <h2>Contact</h2>
      <dl>
        <dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
        <dt>Phone</dt><dd><a href="tel:+38971669905">+389 71 669 905</a></dd>
        <dt>Based in</dt><dd>Skopje, North Macedonia</dd>
        <dt>YouTube</dt><dd><a href="https://www.youtube.com/user/BesirZeneli" target="_blank" rel="noopener">BesirZeneli</a></dd>
        <dt>Licence</dt><dd>Categories B and B1</dd>
      </dl>
      <h2>Languages</h2>
      <ul>
        <li>Albanian <span>Native</span></li>
        <li>Macedonian <span>Native</span></li>
        <li>Turkish <span>C2 · Proficient</span></li>
        <li>English <span>C1 · Advanced</span></li>
        <li>German <span>A2 · Elementary</span></li>
      </ul>
      <h2>Strengths</h2>
      <p style="font-size:.95rem;color:var(--muted);margin:0">Leadership, strategic planning, decision-making, critical thinking, research and analysis, teamwork, conflict resolution, written and verbal communication.</p>
    </aside>

    <div class="cv-main">
      <section>
        <h2>Profile</h2>
        <p class="intro">Biology educator and molecular biologist who pairs hands-on diagnostic laboratory experience with five years of classroom teaching. Head of the Science Department at Maarif International Schools, teaching Biology across Grades 7–13 and creating interactive digital simulations that make complex processes — from glycolysis to PCR — visible and memorable. Former Real-Time PCR diagnostics specialist (SARS-CoV-2, HPV). Honours BSc in Biology from Hacettepe University; MSc in Phytochemistry &amp; Natural Products in progress. Works in five languages.</p>
        <dl class="facts">
          <div><dt>Teaching Biology</dt><dd>5+ years</dd></div>
          <div><dt>Molecular diagnostics</dt><dd>2+ years</dd></div>
          <div><dt>Interactive simulations built</dt><dd>20+</dd></div>
        </dl>
      </section>

      <section id="experience">
        <h2>Professional experience</h2>
        <ul class="role-list">
          {role("September 2021 – present · Skopje", "Head of Science Department &amp; Biology Teacher", "Maarif International Schools",
                ["Lead the Science Department and its teaching staff while teaching Biology from Grade 7 (first-year learners) to Grade 13.",
                 "Homeroom teacher of a gymnasium class, preparing students for the State Matura examination.",
                 "Write exam papers and assessments for Grades 7–13 to the school’s standardised template.",
                 "Designed 20+ interactive simulations and animations in English and Albanian — cell structure, photosynthesis, glycolysis, the Krebs cycle, the electron transport chain, PCR — turning abstract processes into visual, hands-on lessons.",
                 "Build evidence-based reasoning and curiosity through experiments, visual materials and active learning, adapting instruction to mixed-ability groups."],
                ["Department leadership", "State Matura preparation", "Assessment design", "Interactive simulations"])}
          {role("March 2021 – August 2023 · Skopje", "Molecular Biologist", "VFV Medical (VFV Laboratory)",
                ["Detected SARS-CoV-2 and its variants by Real-Time PCR throughout the COVID-19 pandemic.",
                 "Isolated and detected HPV and other pathogens using Real-Time PCR and RT-PCR.",
                 "Ran the full workflow: nucleic-acid isolation, master-mix preparation and thermocycler runs with Bio-Speedy diagnostic kits.",
                 "Performed rapid antigen testing during the pandemic response."],
                ["Real-Time PCR", "RT-PCR", "DNA/RNA extraction"])}
          {role("August 2020 – present", "Book Translator", "Freelance", [])}
        </ul>
      </section>

      <section id="education">
        <h2>Education and research</h2>
        <ul class="role-list">
          {role("In progress · Skopje", "MSc, Phytochemistry &amp; Natural Products", "Mother Teresa University (UNT)",
                ["Thesis: <em>Characterization of bioactive compounds of citrus peels and evaluation of their application as natural additives</em> — orange, lemon and mandarin peels as natural alternatives to the synthetic colourants E110 and E102. Supervisor: Zimere Saiti Musliji."])}
          {role("2014 – 2019 · Ankara, Türkiye", "BSc, Biology — Honour Student", "Hacettepe University · GPA 4.43 · 265 ECTS",
                ["Core training in molecular biology, biochemistry, research methods and biological data analysis.",
                 "Lab techniques: PCR, electrophoresis, DNA extraction, protein purification, spectrophotometry, herbarium methods.",
                 "Special Study, Ecology (grade A1, 95–100): built a database of steppe-plant traits across Anatolia to examine links between climate, topography and plant evolution.",
                 "Special Study, Histology (Toxicology Lab): fixation, paraffin embedding, microtomy, staining and mounting of tissue sections."])}
          {role("Online course", "COVID-19, SARS-CoV-2 and the Pandemic", "Massachusetts Institute of Technology (MIT)", [])}
        </ul>
      </section>

      <section id="earlier">
        <h2>Earlier experience</h2>
        <ul class="role-list">
          {role("July 2019 – July 2020 · Tetovo", "Clinical Biochemistry Intern", "Clinical Center Tetovo",
                ["Operated TOSOH AIA-360, Architect c4000, SmartLyte Plus and i-CHROMA analysers; performed urine microscopy and supported calibration and quality control."])}
          {role("March – July 2020 · Ankara", "Medical Translator (Turkish ⇄ Albanian)", "Liv Hospital Ankara",
                ["Bridged communication between patients, physicians and hospital management, verbally and in writing."])}
          {role("July – September 2018 · Skopje", "Microbiology Intern (Sanitary Review)", "Center for Public Health",
                ["Tested food samples for <em>Salmonella</em>, <em>Shigella</em> and <em>E. coli</em> under ISO methods; prepared daily and summary lab reports."])}
          {role("October 2016 – June 2020 · Ankara", "Albanian Language Course Coordinator", "Albanian Cultural Center",
                ["Ran the course programme for four years: recruited teachers, managed enrolment, schedules, payments and records, and organised cultural events."])}
        </ul>
      </section>

      <section id="honours">
        <h2>Honours and achievements</h2>
        <ul class="role-list">
          {role("2014 – 2019", "Honour Student", "BSc Biology, Hacettepe University · GPA 4.43", [])}
          {role("2020", "Appreciation Plaque", "Embassy of Kosovo in Ankara", ["For five years of cultural and educational contribution."])}
          {role("2013", "National U19 Champion, 800 m and 1500 m", "Athletics", ["Represented Macedonia at the U19 Balkan competition in Edirne."])}
        </ul>
      </section>

      <section id="communication">
        <h2>Science communication</h2>
        <ul class="role-list">
          {role("2020", "The Origin of Coronaviruses", "Educational video in Albanian", ["The history and origin of coronaviruses. <a href=\"https://www.youtube.com/user/BesirZeneli\" target=\"_blank\" rel=\"noopener\">Watch on YouTube</a>."])}
          {role("Ongoing", "@biobesir", "Instagram", ["Biology content for a general audience."])}
        </ul>
      </section>

      <section id="skills">
        <h2>Skills</h2>
        <div class="skill-groups">
          <div><h3>Laboratory and molecular</h3>{chips(["Real-Time PCR", "RT-PCR diagnostics", "DNA/RNA extraction", "Electrophoresis", "Microbiology (ISO)", "Clinical biochemistry", "Histology", "Spectrophotometry", "Quality control"])}</div>
          <div><h3>Education and teaching</h3>{chips(["Department leadership", "State Matura preparation", "Exam and assessment design", "Interactive simulations", "Differentiated instruction", "Science communication"])}</div>
          <div><h3>Digital</h3>{chips(["Microsoft Word", "Excel", "PowerPoint", "Video editing (VideoPad)", "Subtitling", "AI-assisted e-learning"])}</div>
        </div>
      </section>
    </div>
  </div>
</div>'''
    page('Portfolio.html', 'CV — Besir Zeneli', 'CV of Besir Zeneli — Head of Science Department and Biology teacher at Maarif International Schools, molecular biologist and science communicator.', body, current='cv')

def build_chat():
    body = '''
<div class="wrap chat">
  <header class="page-head">
    <p class="crumbs"><a href="studying-materials/studyingmaterials.html">Study materials</a> / Biology chat</p>
    <h1>Biology chat</h1>
    <p class="lede">Ask a Biology question. The chat only answers while its helper server is running, so if it can’t connect, use the study materials instead.</p>
  </header>
  <div id="chat-box" class="chat-box" aria-live="polite"></div>
  <div class="chat-input">
    <label for="user-input" class="skip">Your question</label>
    <input type="text" id="user-input" placeholder="Ask a biology question…">
    <button id="send-btn" class="btn btn-solid" type="button">Send</button>
  </div>
</div>'''
    page('chat.html', 'Biology chat — Besir Zeneli', 'Ask a Biology question.', body, extra_js='<script src="js/chat.js"></script>\n')

if __name__ == '__main__':
    build_home(); build_cv(); build_writings(); build_chat()
    for e in ESSAYS:
        build_essay(e, ESSAY_BODIES[e['file']])
    for g in GRADES:
        build_grade(g)
    build_hub(); build_redirects()
    mm = restyle_mindmaps()
    print('mind maps restyled:', len(mm))
