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

- Three languages: French, English, Russian (RU added 20 Oct 2026). Every text has
  `<span lang="fr">`, `<span lang="en">` and `<span lang="ru">` (or `<div lang>` for block
  content); the trip build has an `L(fr, en, ru)` helper. `site.js` picks the language:
  `?lang=fr|en|ru` in the URL, else the last button choice (`localStorage('lang')`, shared
  across pages), else the browser language (fr*/ru* → that, anything else → EN). Clicking
  a language button writes `?lang=` into the address bar so copied links keep it.
- Russian conventions: decimal comma (37,0 км), units км/м, durations "7 ч 29 мин", dates
  "суббота, 10 октября 2026". Stage headings, map labels and hostel names keep their
  original Latin spelling; Russian prose uses Russian place-name forms (Матозиньюш,
  Понте-де-Лима, Сантьяго-де-Компостела…). Russian first-person past tense is gendered; the notes use masculine forms
  ("я шёл", "я работал"), confirmed by Philippe on 20 Oct 2026.
  Short Strava comments stay untranslated in all languages. Pages that rewrite the URL (the
  trip page sets `#dayN`) must keep `location.search`.
- Analytics: GoatCounter (philippebellefeuille.goatcounter.com), loaded from `site.js` so
  every page is covered. Counts by `location.pathname` only (so `?lang=` doesn't split
  stats). Cookieless, no consent banner. It ignores localhost, so previews don't count.
- French numbers: thousands separator is a narrow no-break space (`fr_int` in the build). Hide rule must be `body [lang]{display:none}` (not bare `[lang]`, which
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
  Beer also adds `margin-block-start: 1rem` to any section/heading/paragraph that
  follows a sibling, with a selector strong enough to need `!important` to undo.
  Beer makes `body` and `header` CSS grids; both are reset to `display:block` (the body
  grid sized the page to its text, so the width changed between FR and EN).
- Link previews (Open Graph): each page has og:* and twitter:card tags in its <head>;
  images are 1200x630 JPEGs made by `scripts/og_images.py` (Roboto from `scripts/fonts/`,
  drawn arrow since Roboto lacks →): `docs/og.jpg` (home) and `docs/trips/<slug>/og.jpg`.
  Text on them is language-neutral. Bump `?v=` on og:image when the image changes, or
  platforms keep showing the old one. New pages need their own tags and image.
- Images: max ~1600px wide, WebP or JPEG, with `loading="lazy"` and `alt` text.
- Philippe's writing preference: concise, opinionated, plain prose, no em dashes.

## Preview

`python3 -m http.server 8000 -d docs`, then http://localhost:8000
