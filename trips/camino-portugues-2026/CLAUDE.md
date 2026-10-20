# Camino Portugués 2026, trip report

One article on philippebellefeuille.github.io (see the root `CLAUDE.md`). Philippe Bellefeuille walked the Camino Portugués
(coastal start, then central route) from Matosinhos to Santiago de Compostela,
10–19 October 2026, 10 stages, all recorded on Strava.

Paths below are relative to this folder (`trips/camino-portugues-2026/`) unless they start with `docs/`, which is the repo-root published folder.

## Current state (handed over from a Claude Cowork session, 20 Oct 2026)

- `docs/trips/camino-portugues-2026/index.html` is the page (generated, do not hand-edit): bilingual FR/EN toggle (default FR),
  totals, an inline SVG route map, and one section per stage with dates, start/end
  times, distance, elevation gain, moving time, elapsed time, and the Strava
  description when there was one. Styled with the site theme (Beer CSS / Material 3,
  see root `CLAUDE.md`); the Cowork v1 warm theme (Bitter, yellow accent) was replaced
  on 20 Oct 2026 at Philippe's request. Layout is unchanged.
- `data/days.json` is the source of truth: one object per stage with Strava
  activity id, stage endpoints (`from`/`to`), description, local start time,
  distance (m), moving/elapsed time (s), elevation gain (m), calories, and the
  reduced encoded polyline from Strava.
- `data/svg.json` is the pre-projected map geometry (coastline, PT/ES border,
  rivers from Natural Earth 10m, plus route paths, markers and town labels).
- `scripts/gen_svg.py` regenerates `data/svg.json`. It needs the Natural Earth
  10m GeoJSON files (coastline, admin_0_boundary_lines_land, rivers_lake_centerlines)
  in `data/ne/` — not committed, fetch from
  https://github.com/nvkelso/natural-earth-vector/tree/master/geojson if needed.
  Only rerun this if a stage endpoint or map extent changes.
- `scripts/build_html.py` regenerates the page from `data/days.json` and
  `data/svg.json`. From the repo root:
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
2. Philippe's own notes per day. Each day card has a `.notes` placeholder.
   He'll supply the text; the page is bilingual, so add both FR and EN
   (`<span lang="fr">` / `<span lang="en">`), translating whichever side he
   doesn't provide.
3. Possibly a per-day elevation profile (Strava altitude streams are available
   through the MCP `get_activity_streams` tool if a Strava connector is present).

## Style conventions

- Philippe's writing/communication preference: concise, opinionated, plain prose,
  no em dashes, no excessive hedging.
- Keep the page bilingual and use the shared theme tokens; no page-specific colours.
- Do not add a hero image or restructure the layout without asking.
