# Camino Portugués 2026, trip report

One article on philippebellefeuille.github.io (see the root `CLAUDE.md`). Philippe Bellefeuille walked the Camino Portugués
(coastal start, then central route) from Matosinhos to Santiago de Compostela,
10–19 October 2026, 10 stages, all recorded on Strava.

Paths below are relative to this folder (`trips/camino-portugues-2026/`) unless they start with `docs/`, which is the repo-root published folder.

## Current state (handed over from a Claude Cowork session, 20 Oct 2026)

- `docs/trips/camino-portugues-2026/index.html` is the page (generated, do not hand-edit): FR/EN/RU language toggle,
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
  - On desktop, `alignMap()` sizes the overview to the day list's height with every day
    collapsed, capped at the window height so the pinned (sticky) map is always fully
    visible. Philippe wants both: columns lined up and the whole map visible while
    scrolling. If the list is taller than the window, tops align at the start and the
    sticky map's bottom meets the last day at the end. No caption under the map.
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
  `fr`, `en` and `ru` arrays of paragraphs (same paragraph count in each), and `hostel` {name, url} with his Google Maps link.
  Rendered in each stage card as the notes text and a "Où j’ai dormi / Where I slept"
  row; days without notes show a "coming soon" line, days without a hostel show nothing.
  He writes in English; edit lightly (spelling, place names, flow) keeping his voice,
  and write the French and Russian versions. Hostel names come from the Google listing his link opens.
- `scripts/build_html.py` regenerates the page from `data/days.json`, `data/notes.json` and `data/photos.json`. From the repo root:
  `.venv/bin/python trips/camino-portugues-2026/scripts/build_html.py`
  (the venv is Python 3.13 with polyline, osxphotos, pillow, pillow-heif; recreate with
  `/opt/homebrew/bin/python3.13 -m venv .venv && .venv/bin/pip install polyline osxphotos pillow pillow-heif`).
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

1. Photos per day (pipeline built 20 Oct 2026; export from Photos in progress, 336 items).
   - Source: Apple Photos album "Camino Portugese 2026". Reading the library directly
     (osxphotos) fails: Claude Code's commands run under a helper app
     (~/Library/Application Support/Claude/claude-code/<version>/…/claude.app) that macOS
     treats separately for Full Disk Access. So Philippe exports from Photos instead
     (File → Export, JPEG, full size, location info on) into `photos-originals/` at the
     repo root (gitignored). iCloud originals make the export slow (~1–2 photos/min).
   - `scripts/photos.py` converts them: day from the local EXIF date (10 Oct = day 1),
     WebP at 1600 px and 600 px long edge into `docs/…/img/dayN/<name>-1600|600.webp`,
     all metadata stripped (no GPS). Writes `data/photos.json` (src, day, taken, file, w,
     h, featured, caption{fr,en}); keeps featured/caption on re-runs; only converts new or
     changed files. Reports dates outside 10–19 Oct and photos >3 km from the day's track.
     Videos (.mov) are skipped; Philippe hasn't decided whether to include any.
   - Page: each day shows 6 previews (featured ones, else spread evenly through the day)
     with "+N" and "See all", and a full-screen `<dialog id="viewer">` (arrows, keys,
     swipe). Export loses album order, hence the even spread / `featured` flag.
   - Beer CSS traps hit here: buttons have a fixed size and squash child images to 24 px
     (override min/max width/height with !important); dialogs are centred with
     translateX(-50%) (override transform).
   Strava activity URLs: https://www.strava.com/activities/<id> with ids in days.json.
2. Philippe's own notes per day, in `data/notes.json`. Done: all 10 days (day 10's "hostel" is the Porto hotel after the bus back).
3. Possibly a per-day elevation profile (Strava altitude streams are available
   through the MCP `get_activity_streams` tool if a Strava connector is present).

## Style conventions

- Philippe's writing/communication preference: concise, opinionated, plain prose,
  no em dashes, no excessive hedging.
- Keep the page in all three languages and use the shared theme tokens; no page-specific colours.
- Do not add a hero image or restructure the layout without asking.
