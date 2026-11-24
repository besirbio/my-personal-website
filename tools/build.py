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
  'intro': 'Energy and nutrition, the circulatory system, species and variation.',
  'terms': [('Lessons', [
     L('Exam', 'First exam material', pdf('grade8', '8th Grade First Exam.pdf')),
     L('7.2', 'The amount of energy in a type of food', pdf('grade8', '7.2 The amount of energy of a certain type of food.pdf'), mm('energycalories.html')),
     L('8.2', 'Basal metabolic rate (BMR) and total daily energy expenditure (TDEE)', pdf('grade8', '8.2 Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure.pdf'), mm('bmrandtdee.html'), ('interactive', 'BMR calculator', 'https://gemini.google.com/share/bb4677329f17')),
     L('9.1', 'Proteins', pdf('grade8', '9.1 Proteins.pdf'), mm('proteins.html')),
     L('9.2', 'Digestion', pdf('grade8', '9.2 Digestion.pdf'), mm('digestion.html')),
     L('10.1', 'Circulatory system', pdf('grade8', '10.1 Circulatory System.pdf'), mm('MCirculatory System.html')),
     L('10.2', 'Blood composition', pdf('grade8', '10.2 Blood composition.pdf'), mm('MBlood Composition.html')),
     L('11.1', 'Species', pdf('grade8', '11.1 Species.pdf'), mm('MSpecies.html')),
     L('11.2', 'Species and hybrids', pdf('grade8', '11.2 Species and hybrids.pdf'), mm('MSpecies and Hybrids.html')),
     L('12.1', 'Types of variation', pdf('grade8', '12.1 Types of variations.pdf'), mm('MTypes of Variations.html')),
     L('12.2', 'Measuring variation', pdf('grade8', '12.2 Measurement of variations.pdf'), mm('MMeasurement of variations.html')),
  ])]},
 {'id': 'grade9', 'num': '9', 'label': 'Grade 9', 'mm_page': 'mindmappings9thgrade.html',
  'intro': 'Human reproduction and development, breathing, classification and adaptation.',
  'terms': [
   ('First semester', [
     L('Exam', 'First exam material', pdf('grade9', '9th Grade - 1st Exam Material.pdf')),
   ]),
   ('Second semester', [
     L('9.1', 'Understanding the menstrual cycle', pdf('grade9', '9.1 Understanding Menstrual Cycle.pdf'), mm('menstruation.html')),
     L('10.1', 'Fertilisation', pdf('grade9', '10.1 Fertilization.pdf'), mm('fertilization.html')),
     L('10.2', 'Fetal development', pdf('grade9', '10.2 Fetal Development - READ.pdf', 'Reading'), sl('grade9', '10.2 Fetal Developmentp - PRESENTATION.pdf'), mm('fetaldevelopment.html')),
     L('11.2', 'Respiratory system', pdf('grade9', '11.2 Respiratory System.pdf'), mm('MRespiratory System.html')),
     L('12.1', 'Breathing and ventilation', pdf('grade9', '12.1 Breathing and ventilation.pdf'), mm('MBreathing and Ventilation.html')),
     L('12.2', 'Dichotomous keys', sl('grade9', '12.2B dichotomous_key_pp.pdf')),
     L('13.1', 'Adaptation of plants and animals', pdf('grade9', '13.1 Adaptation of plants and animals.pdf'), mm('MAdaptation of Plants and Animals.html')),
     L('13.2', 'Adaptation of detritivores', pdf('grade9', '13.2 Adaptation of detritivores.pdf'), mm('MDetritivores.html')),
     L('14.1', 'Decomposers', pdf('grade9', '14.1 Decomposers.pdf'), mm('MDecomposers.html')),
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
        ext = h.startswith('http') or h.lower().endswith(('.pdf', '.pptx'))
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
ESSAYS = [
 {'file': 'essay4.html', 'kind': 'science', 'kind_label': 'Science', 'date': '2025-11-05', 'date_h': '5 November 2025',
  'title': 'Silent killers', 'sub': 'the strange world of prions',
  'summary': 'Prions carry no DNA or RNA, yet a single misfolded protein can turn healthy proteins into copies of itself and destroy the brain. A look at Creutzfeldt–Jakob disease, mad cow disease, scrapie and kuru — and why prions are so hard to kill.',
  'author': 'Ayşegül Sarıarslan, student at Maarif International Schools · mentored by Besir Zeneli'},
 {'file': 'essay3.html', 'kind': 'science', 'kind_label': 'Science', 'date': '2025-02-02', 'date_h': '2 February 2025',
  'title': 'Asteroid Bennu’s secrets', 'sub': 'building blocks of life found in space',
  'summary': 'Uncontaminated samples from asteroid Bennu hold ammonia and amino acids, some unknown in Earth’s biology. They do not prove life came from space, but they show its ingredients may be common across the solar system.',
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
    <p class="lede">Essays on biology, the human body and the questions around it — plus a translation I return to often. Some are written with my students.</p>
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
<p>Scientists have made an exciting discovery that could help us understand how life began — not just on Earth, but possibly elsewhere in the universe. Samples collected from asteroid Bennu, brought back by Japan’s Hayabusa spacecraft, contain ingredients essential for life. While this doesn’t prove life came from space, it reveals the universe might be full of the tools needed to create it.</p>
<h2>Why Bennu’s samples are special</h2>
<p>For decades, scientists studied meteorites (space rocks that land on Earth) to find clues about life’s origins. The problem? Meteorites get contaminated when they crash through Earth’s atmosphere. Heat, impact, and exposure to our environment make it hard to confirm if their contents truly came from space.</p>
<p><strong>Bennu’s samples are different.</strong> The Hayabusa spacecraft collected them directly from the asteroid and sealed them in a protective capsule, shielding them from Earth’s contaminants. This makes Bennu’s rocks the “purest” space samples we’ve ever analyzed.</p>
<h2>Key discoveries in the space dust</h2>
<ul>
<li><strong>Ammonia overload:</strong> 75× more ammonia than other asteroid samples</li>
<li><strong>Alien amino acids:</strong> 19 types not found in Earth biology</li>
<li><strong>Saltwater history:</strong> evidence of ancient liquid water reactions</li>
</ul>
{fig("assets/img/amino-acids.jpg", "Molecular diagram of amino acid structures")}
<h2>The life recipe connection</h2>
<p>While Bennu’s samples contain life’s ingredients, this doesn’t confirm the <strong><em>panspermia</em> hypothesis</strong> (life spreading through asteroids). What it does show is that asteroids could have delivered life’s raw materials to Earth. As one scientist noted: <q>We’ve found the LEGO blocks, but we still don’t know how they were assembled.</q></p>
<h2>Looking beyond Bennu</h2>
<p>Scientists are now targeting icy moons like Jupiter’s Europa and Saturn’s Enceladus. NASA’s upcoming Europa Clipper mission will explore the moon’s subsurface ocean — a potential hotspot for alien life. As researcher Dr. Jane Smith explains: <q>Where there’s water and organic molecules, there’s potential for life’s chemistry.</q></p>
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
      <p class="role-sub">I teach grades 7 to 13 at Maarif International Schools, lead our science department, and spent three years running PCR diagnostics in a clinical lab. This site holds my class materials, my writing and my CV.</p>
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
      <li><a href="writings.html"><span class="who">Readers</span><span class="what">Writing<small>Essays on prions, asteroid chemistry, stress biology, and a translation of Sezai Karakoç.</small></span><span class="go">Read</span></a></li>
      <li><a href="Portfolio.html"><span class="who">Colleagues</span><span class="what">CV<small>Molecular diagnostics, teaching, education and skills.</small></span><span class="go">View</span></a></li>
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
      <p>I studied molecular biology at Hacettepe University in Ankara, then led the molecular biology department of a diagnostic laboratory in Skopje, running real-time PCR for SARS-CoV-2, HPV and chlamydia.</p>
      <p>Since 2021 I have taught Biology at Maarif International Schools. In class I care less about memorising isolated facts and more about helping students observe, question, connect evidence and think for themselves. My students have taken first place in national Biology competitions.</p>
      <p>Outside the classroom I write, translate, read, and run — I competed for the national athletics team.</p>
      <blockquote>“Science is the poetry of reality.”<cite>Richard Dawkins</cite></blockquote>
      <dl class="facts">
        <div><dt>Based in</dt><dd>Skopje, North Macedonia</dd></div>
        <div><dt>Teaching</dt><dd>Biology, grades 7–13</dd></div>
        <div><dt>Languages</dt><dd>Albanian, Macedonian, English, Turkish</dd></div>
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
        b = ''.join(f'<li>{x}</li>' for x in bullets)
        t = ('<ul class="chips">' + ''.join(f'<li>{x}</li>' for x in tags) + '</ul>') if tags else ''
        return f'<li class="role-item"><span class="when">{when}</span><h3>{title}</h3><p class="org">{org}</p><ul>{b}</ul>{t}</li>'
    body = f'''
<div class="wrap">
  <header class="page-head">
    <h1>Curriculum vitae</h1>
    <p class="lede">Molecular biologist and Biology educator, working where molecular diagnostics, science communication and student development meet.</p>
  </header>
  <div class="cv">
    <aside class="cv-side">
      <img src="assets/img/portrait.jpg" alt="Besir Zeneli" width="818" height="997">
      <h2>Details</h2>
      <dl>
        <dt>Based in</dt><dd>Skopje</dd>
        <dt>Born</dt><dd>24.06.1996, Skopje</dd>
        <dt>Nationality</dt><dd>Macedonian</dd>
        <dt>Licence</dt><dd>Category B</dd>
        <dt>Open to</dt><dd>Relocation and remote work</dd>
      </dl>
      <h2>Languages</h2>
      <ul>
        <li>Albanian <span>Native</span></li>
        <li>Macedonian <span>Fluent</span></li>
        <li>English <span>Fluent</span></li>
        <li>Turkish <span>Fluent</span></li>
      </ul>
      <a class="btn btn-solid" href="mailto:{EMAIL}">Email me</a>
    </aside>

    <div class="cv-main">
      <section>
        <h2>Profile</h2>
        <p class="intro">Molecular biologist with three years of experience in diagnostic laboratories, leading research and diagnostic projects. Skilled in real-time PCR, DNA/RNA extraction and molecular diagnostics of infectious disease, with careful laboratory management. Designs engaging curricula and interactive lessons that bring students into real science.</p>
      </section>

      <section id="experience">
        <h2>Experience</h2>
        <ul class="role-list">
          {role("September 2021 – present · Skopje", "Biology teacher", "Maarif International Schools",
                ["Designs and teaches Biology curricula aligned with international standards.", "Runs laboratory experiments and interactive learning activities.", "Mentors students in research projects and science fairs.", "Guided students to first place in national Biology competitions."],
                ["Education", "Curriculum design", "Mentoring"])}
          {role("April 2021 – August 2023 · Skopje", "Molecular biologist", "VFV Laboratory",
                ["Led the Molecular Biology Department, overseeing research and diagnostic projects.", "Ran real-time PCR analysis for SARS-CoV-2, HPV and Chlamydia detection.", "Managed DNA/RNA isolation, sample preparation and thermocycler operation.", "Prepared master mixes and worked with Viasure, Algimed, Bio-Speedy, AmpliSens and GeneProof kits.", "Trained and supervised laboratory staff."],
                ["PCR", "Diagnostics", "Laboratory management"])}
          {role("January – July 2020 · Ankara", "Medical translator", "Liv Hospital",
                ["Translated between Turkish and Albanian for medical staff and patients.", "Supported accurate medical communication and patient care coordination."],
                ["Translation", "Medical communication"])}
        </ul>
      </section>

      <section id="education">
        <h2>Education</h2>
        <ul class="role-list">
          <li class="role-item"><span class="when">2015 – 2019 · Ankara</span><h3>BSc in Molecular Biology</h3><p class="org">Hacettepe University</p>
            <ul><li>GPA 3.43, honours student.</li><li>Coursework: molecular biology, biochemistry, histology, ecology.</li><li>Lab techniques: PCR, electrophoresis, protein purification, DNA extraction, spectrophotometry.</li></ul></li>
        </ul>
      </section>

      <section id="internships">
        <h2>Internships</h2>
        <ul class="role-list">
          {role("July 2019 – July 2020", "Biochemistry intern", "Clinical Center Tetovo",
                ["Performed urine microscopy and equipment calibration.", "Worked with TOSOH AIA-360, SmartLyte Plus and Architect c4000 systems."])}
          {role("June – August 2018", "Microbiology intern", "Center for Public Health",
                ["Ran bacterial cultures and antimicrobial susceptibility testing.", "Assisted with sanitary inspections and microbial analysis."])}
        </ul>
      </section>

      <section>
        <h2>Training and community</h2>
        <ul class="role-list">
          {role("2021", "COVID-19 and SARS-CoV-2 course", "Massachusetts Institute of Technology (MIT)", [])}
          {role("2015 – 2019", "Community volunteer", "Albanian Cultural Center, Ankara",
                ["Five years of contribution to cultural and educational activities.", "Community Volunteer Recognition Award."])}
        </ul>
      </section>

      <section id="skills">
        <h2>Skills</h2>
        <div class="skill-groups">
          <div><h3>Laboratory and science</h3><ul class="chips"><li>Molecular biology</li><li>PCR</li><li>DNA/RNA extraction</li><li>Biotechnology</li><li>Data analysis</li><li>Quality control</li><li>Lab management</li></ul></div>
          <div><h3>Teaching and communication</h3><ul class="chips"><li>Curriculum development</li><li>Scientific writing</li><li>Teamwork</li><li>Adaptability</li><li>Working under pressure</li></ul></div>
          <div><h3>Digital</h3><ul class="chips"><li>Microsoft Office</li><li>Adobe Photoshop</li></ul></div>
        </div>
        <p style="margin-top:28px;color:var(--muted)">Interests: running, writing, reading, translation, poetry and film.</p>
      </section>
    </div>
  </div>
</div>'''
    page('Portfolio.html', 'CV — Besir Zeneli', 'CV of Besir Zeneli — molecular biologist and Biology educator in Skopje.', body, current='cv')

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
