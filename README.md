# Besir Zeneli — personal website

Live at https://besirbio.github.io/my-personal-website/

## Structure

| Page | File |
| --- | --- |
| Home | `index.html` |
| Study materials hub (search + grades) | `studying-materials/studyingmaterials.html` |
| Grade pages | `studying-materials/grade7.html` … `grade13.html`, `ScienceClub.html` |
| Mind maps | `studying-materials/*.html` (Markmap pages) |
| Writing | `writings.html`, `essay1.html` … `essay4.html` |
| CV | `Portfolio.html` |

Shared styles and scripts live in `assets/` (`site.css`, `site.js`, `mindmap.css`, `img/`). PDFs stay in `pdfs/<grade>/`.

## Adding a lesson or a PDF

All pages are generated from one file, `tools/build.py`. The lesson list for each grade is the `GRADES` list near the top.

1. Put the PDF in `pdfs/<grade>/`.
2. Add a line to that grade in `tools/build.py`, for example
   `L('14.2', 'Food chains', pdf('grade9', '14.2 Food chains.pdf'), mm('MFood chains.html')),`
3. Run `python3 tools/build.py` from the repository folder and commit.

This updates the grade page, the lesson counts and the search on the study page together.
