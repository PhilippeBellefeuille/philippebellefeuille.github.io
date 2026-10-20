# philippebellefeuille.github.io

Philippe Bellefeuille's personal site: trip reports and a blog. Deliberately simple:
hand-written or script-generated static HTML, no framework, no Jekyll.

## Layout

- `docs/` is what GitHub Pages serves (Pages source: `main` / `docs`). `.nojekyll` keeps
  Pages from running Jekyll.
  - `docs/index.html` is the home page. Add each new article to its list by hand.
  - `docs/trips/<slug>/index.html` is a trip article; images go in `docs/trips/<slug>/img/`.
  - `docs/blog/<slug>/index.html` for blog posts (none yet).
- `trips/<slug>/` holds an article's source data, build scripts and its own `CLAUDE.md`.
  Read that file before working on the article.
- `.venv/` (gitignored) has the Python deps for the build scripts.

## Conventions

- Bilingual FR/EN, FR default. Each text has `<span lang="fr">` and `<span lang="en">`;
  a toggle sets `body[data-lang]` and stores the choice in `localStorage('lang')`, shared
  across pages. Hide rule must be `body [lang]{display:none}` (not bare `[lang]`, which
  would hide `<html lang>`).
- Material Design 3 via Beer CSS (`beercss@5.0.3` from jsdelivr, CSS only, no beer.js),
  Roboto from Google Fonts. Neutral grey surfaces, muted slate-blue primary.
- `docs/assets/site.css` holds the M3 colour tokens (light on `:root, body.light`, dark on
  `body.dark`), the app bar and shared helpers. `docs/assets/site.js` toggles `body.dark`
  from the OS setting and runs the FR/EN toggle. Every page links both. Page-specific CSS
  stays inline in the page.
- Beer CSS claims many short class names and restyles bare elements. Before adding a
  class, check it isn't a Beer class: known traps are `.page` (hidden, used for page
  transitions), `.border`, `.top`/`.left`, `.grid`, `.wrap`, `.arrow`, `.overline`.
  Beer makes `body` and `header` CSS grids, hence `.appbar{display:block}`.
- Images: max ~1600px wide, WebP or JPEG, with `loading="lazy"` and `alt` text.
- Philippe's writing preference: concise, opinionated, plain prose, no em dashes.

## Preview

`python3 -m http.server 8000 -d docs`, then http://localhost:8000
