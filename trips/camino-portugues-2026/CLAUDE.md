# Camino Portugués 2026, trip report

One article on philippebellefeuille.github.io (see the root `CLAUDE.md`). Philippe Bellefeuille walked the Camino Portugués
(coastal start, then central route) from Matosinhos to Santiago de Compostela,
10–19 October 2026, 10 stages, all recorded on Strava.

Paths below are relative to this folder (`trips/camino-portugues-2026/`) unless they start with `docs/`, which is the repo-root published folder.

## Current state (handed over from a Claude Cowork session, 20 Oct 2026)

- `docs/trips/camino-portugues-2026/index.html` is the page (generated, do not hand-edit): bilingual FR/EN toggle (default FR),
  totals, an interactive overview map, and one collapsible section per stage with dates, start/end
  times, distance, elevation gain, moving time, elapsed time, and the Strava
  description when there was one. Styled with the site theme (Beer CSS / Material 3,
  see root `CLAUDE.md`); the Cowork v1 warm theme (Bitter, yellow accent) was replaced
  on 20 Oct 2026 at Philippe's request.
- Maps (added 20 Oct 2026, replacing the Cowork SVG map and its `gen_svg.py`/`svg.json`):
  Leaflet 1.9.4 from cdnjs with Esri World Light/Dark Gray Canvas tiles plus their
  `_Reference` label layer (keyless; CARTO basemaps now show an "API key required"
  watermark). Tiles swap with the OS light/dark setting. Tracks are the Strava summary
  polylines from `days.json`, decoded at build time and embedded as `STAGES`.
  - Overview map: each stage is clickable (wide invisible hit line + numbered pin) with
    a hover tooltip; click opens that stage's card, scrolls to it and highlights it.
  - Stage cards are `<details name="stage">` (one open at a time). Opening one builds its
    own map lazily, highlights it on the overview and sets `#dayN`; loading the page
    with `#dayN` opens that stage.
  - Leaflet gotchas: set a view (`fitBounds`) before adding vector layers or it throws
    "reading 'min'"; Beer's `* {border-radius: inherit}` is reset inside `.map`.
  - Full-resolution tracks (`get_activity_streams`, ~1000 points per stage) were tried but
    are too large to move through the Strava connector into files reliably; the summary
    polylines (~330 points, about one per 75 m) look fine at these zooms.
- `data/days.json` is the source of truth: one object per stage with Strava
  activity id, stage endpoints (`from`/`to`), description, local start time,
  distance (m), moving/elapsed time (s), elevation gain (m), calories, and the
  reduced encoded polyline from Strava.
- `data/notes.json` holds Philippe's own content per day (keyed by day number):
  `fr` and `en` arrays of paragraphs, and `hostel` {name, url} with his Google Maps link.
  Rendered in each stage card as the notes text and a "Où j’ai dormi / Where I slept"
  row; days without notes show a "coming soon" line, days without a hostel show nothing.
  He writes in English; edit lightly (spelling, place names, flow) keeping his voice,
  and write the French version. Hostel names come from the Google listing his link opens.
- `scripts/build_html.py` regenerates the page from `data/days.json` and `data/notes.json`. From the repo root:
  `.venv/bin/python trips/camino-portugues-2026/scripts/build_html.py`
  (the venv has `polyline`; recreate with `python3 -m venv .venv && .venv/bin/pip install polyline`).
- Moved from the Cowork zip into this repo on 20 Oct 2026. Changes made then: full HTML
  document wrapper (doctype, head, charset, viewport, description), a home link in the
  top bar, and `[lang]{display:none}` scoped to `body [lang]` so `<html lang>` works.

## Facts already verified (do not "correct" these back)

- Stage endpoints were checked against GPS end coordinates. Strava's location
  labels used municipalities; the real overnight stops are:
  1 Matosinhos → São Pedro de Rates (not Póvoa de Varzim)
  2 São Pedro de Rates → Tamel (about 8 km north of Barcelos)
  3 Tamel → Ponte de Lima
  4 Ponte de Lima → Rubiães (not Paredes de Coura)
  5 Rubiães → Tui, 6 Tui → Redondela, 7 Redondela → Pontevedra,
  8 Pontevedra → Caldas de Reis, 9 Caldas de Reis → Padrón, 10 Padrón → Santiago.
- Totals from Strava: 251.9 km, 4,708 m elevation gain, 53h26 moving, 65h13 elapsed.
- Philippe asked that stage names stay plain place names (no hostel names).

## What is left to do

1. Photos per day. Strava's API/MCP does not expose activity photos, so they
   have to come from the activity pages (logged in) or from Philippe's own
   library. Each day card has an empty `.photos` placeholder; replace it with
   an image strip. Put images in `docs/trips/camino-portugues-2026/img/`. Keep images optimised (max ~1600px wide, WebP or JPEG).
   Activity URLs: https://www.strava.com/activities/<id> with ids in days.json.
2. Philippe's own notes per day, in `data/notes.json`. Done: all 10 days (day 10's "hostel" is the Porto hotel after the bus back).
3. Possibly a per-day elevation profile (Strava altitude streams are available
   through the MCP `get_activity_streams` tool if a Strava connector is present).

## Style conventions

- Philippe's writing/communication preference: concise, opinionated, plain prose,
  no em dashes, no excessive hedging.
- Keep the page bilingual and use the shared theme tokens; no page-specific colours.
- Do not add a hero image or restructure the layout without asking.
