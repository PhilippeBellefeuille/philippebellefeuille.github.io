import json, datetime as dt, html, pathlib, polyline
TRIP=pathlib.Path(__file__).resolve().parent.parent
OUT=TRIP.parent.parent/'docs'/'trips'/TRIP.name/'index.html'
days=json.load(open(TRIP/'data/days.json'))
notes=json.load(open(TRIP/'data/notes.json'))  # Philippe's own text per day, FR + EN, and where he slept
def fr_int(x): return f"{x:,.0f}".replace(',', '\u202f')  # French thousands separator: narrow no-break space
def hm(s): return f"{s//3600}h{(s%3600)//60:02d}"
tot_d=sum(d['d'] for d in days); tot_eg=sum(d['eg'] for d in days); tot_mt=sum(d['mt'] for d in days); tot_et=sum(d['et'] for d in days)
FR_DAYS=['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']; FR_MON={10:'octobre'}
def fdate(s,lang):
    if lang=='en': return s.strftime('%A %-d %B %Y')
    return f"{FR_DAYS[s.weekday()]} {s.day} {FR_MON[s.month]} {s.year}"
def fshort(s,lang):
    if lang=='en': return s.strftime('%a %-d %b')
    return f"{FR_DAYS[s.weekday()][:3]}. {s.day} oct."

# Stage tracks for the maps: Strava summary polylines, decoded to [lat,lng].
stages=[{'day':d['day'],'from':d['from'],'to':d['to'],'km':round(d['d']/1000,1),
         'line':[[round(a,5),round(b,5)] for a,b in polyline.decode(d['pl'])]} for d in days]
stages_json=json.dumps(stages,ensure_ascii=False,separators=(',',':'))

cards=''
for d in days:
    s=dt.datetime.fromisoformat(d['start']); e=s+dt.timedelta(seconds=d['et'])
    desc=html.escape(d['desc']).replace('\n','<br>')
    n=notes.get(str(d['day']),{})
    if n.get('en') or n.get('fr'):
        paras=lambda lang: ''.join(f'<p>{html.escape(t)}</p>' for t in n.get(lang,[]))
        notesblk=f'<div class="notes"><div lang="fr">{paras("fr")}</div><div lang="en">{paras("en")}</div></div>'
    else:
        notesblk='<div class="notes empty"><span lang="fr">Notes de l’étape à venir.</span><span lang="en">Notes for this day coming soon.</span></div>'
    h=n.get('hostel')
    hostelblk=f'''<div class="hostel"><i aria-hidden="true">bed</i><div><div class="small-text muted upper"><span lang="fr">Où j’ai dormi</span><span lang="en">Where I slept</span></div><a class="link" href="{html.escape(h['url'])}" target="_blank" rel="noopener">{html.escape(h['name'])}<i aria-hidden="true">open_in_new</i></a></div></div>''' if h else ''
    descblk=f'<blockquote class="strava"><div class="small-text muted upper">Strava</div>{desc}</blockquote>' if d['desc'] else ''
    cards+=f"""
<details class="day" id="day{d['day']}" data-day="{d['day']}" name="stage">
  <summary>
    <div class="dnum">{d['day']}</div>
    <div class="sumtext">
      <h2 class="dtitle">{html.escape(d['from'])} <span class="to">→</span> {html.escape(d['to'])}</h2>
      <div class="muted when"><span lang="fr">{fshort(s,'fr')}</span><span lang="en">{fshort(s,'en')}</span> · {d['d']/1000:.1f} km · +{d['eg']:.0f} m</div>
    </div>
    <i class="chev" aria-hidden="true">expand_more</i>
  </summary>
  <div class="dbody">
    <div class="dmeta">
      <div class="muted when"><span lang="fr">{fdate(s,'fr')}</span><span lang="en">{fdate(s,'en')}</span> · {s.strftime('%H:%M')} – {e.strftime('%H:%M')}</div>
      <a class="button border small strava-link" href="https://www.strava.com/activities/{d['id']}" target="_blank" rel="noopener"><span lang="fr">Voir sur Strava</span><span lang="en">View on Strava</span><i>open_in_new</i></a>
    </div>
    <dl class="stats">
      <div><dt><span lang="fr">Distance</span><span lang="en">Distance</span></dt><dd>{d['d']/1000:.1f} <small>km</small></dd></div>
      <div><dt><span lang="fr">Dénivelé +</span><span lang="en">Elevation gain</span></dt><dd>{d['eg']:.0f} <small>m</small></dd></div>
      <div><dt><span lang="fr">En marche</span><span lang="en">Moving time</span></dt><dd>{hm(d['mt'])}</dd></div>
      <div><dt><span lang="fr">Durée totale</span><span lang="en">Elapsed</span></dt><dd>{hm(d['et'])}</dd></div>
    </dl>
    {notesblk}
    {hostelblk}
    <div class="map stage-map" data-day="{d['day']}" role="img" aria-label="Map of stage {d['day']}, {html.escape(d['from'])} to {html.escape(d['to'])}"></div>
    {descblk}
    <div class="photos"><span lang="fr">Photos de l’étape à venir</span><span lang="en">Photos for this day coming soon</span></div>
  </div>
</details>"""
longest=max(days,key=lambda d:d['d'])
page=f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Camino Portugués 2026 · Philippe Bellefeuille</title>
<meta name="description" content="Dix jours sur le Caminho Português, de Matosinhos à Saint-Jacques-de-Compostelle, octobre 2026.">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/beercss@5.0.3/dist/cdn/beer.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<link rel="stylesheet" href="../../assets/site.css">
<style>
/* Layout: overview map pinned in a left column, totals and the ten collapsible stages on the right; stacks on phones. */
.eyebrow {{ color: var(--primary); font-size: .875rem; font-weight: 500; letter-spacing: .08em; text-transform: uppercase; }}
.hero h1 {{ font-size: clamp(2rem, 5vw, 3rem); font-weight: 400; line-height: 1.15; margin: .5rem 0 1rem; text-wrap: balance; }}
.hero p {{ font-size: 1.125rem; }}
.totals {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: .75rem; margin-block-start: 2rem; }}
.totals > div {{ background: var(--surface-container-low); border: 1px solid var(--outline-variant); border-radius: .75rem; padding: 1rem; }}
.totals dt, .stats dt {{ font-size: .75rem; font-weight: 500; letter-spacing: .06em; text-transform: uppercase; color: var(--on-surface-variant); }}
.totals dd {{ font-size: 1.75rem; line-height: 1.2; margin-block-start: .25rem; font-variant-numeric: tabular-nums; }}
.totals dd small, .stats dd small {{ font-size: .875rem; color: var(--on-surface-variant); }}
.layout {{ display: grid; grid-template-columns: minmax(18rem, 26rem) 1fr; gap: 2.5rem; margin-block-start: 2.5rem; align-items: start; }}
.mapcol {{ position: sticky; top: 1rem; }}
h2.section {{ font-size: 1.375rem; font-weight: 400; margin-block-end: .75rem; }}
.days {{ min-inline-size: 0; margin: 0 !important; }}  /* Beer gives a section after a sibling a 1rem top margin (high-specificity rule); it pushed the day list below the map */

/* Maps (Leaflet). Beer CSS sets border-radius:inherit on everything, which would round every tile. */
.map {{ border: 1px solid var(--outline-variant); border-radius: .75rem; overflow: hidden; background: var(--surface-container-low); z-index: 0; }}
.map * {{ border-radius: 0; }}
#overview {{ block-size: min(78vh, 46rem); }}
.stage-map {{ block-size: 20rem; margin-block-start: 1.25rem; }}
.leaflet-container {{ font-family: var(--font); background: var(--surface-container-low); }}
.leaflet-control-attribution {{ font-size: .6875rem; background: color-mix(in srgb, var(--surface) 80%, transparent) !important; color: var(--on-surface-variant); }}
.leaflet-control-attribution a {{ color: var(--primary); }}
.leaflet-bar a {{ background: var(--surface-container-high); color: var(--on-surface); border-color: var(--outline-variant); }}
.leaflet-bar a:hover {{ background: var(--surface-container-highest); }}
.leaflet-tooltip {{ background: var(--inverse-surface); color: var(--inverse-on-surface); border: 0; border-radius: .5rem !important; box-shadow: var(--elevate2); font-size: .8125rem; padding: .25rem .625rem; }}
.leaflet-tooltip::before {{ display: none; }}
.route {{ stroke: var(--primary); stroke-width: 4; stroke-linecap: round; stroke-linejoin: round; transition: stroke-opacity .2s, stroke-width .2s; }}
.route.dim {{ stroke-opacity: .35; }}
.route.hover, .route.active {{ stroke-width: 7; stroke-opacity: 1; }}
.route-ctx {{ stroke: var(--outline); stroke-width: 3; stroke-opacity: .6; stroke-dasharray: 2 6; stroke-linecap: round; }}
.hit {{ cursor: pointer; }}
.leaflet-interactive:focus {{ outline: none; }}
.pin {{ display: grid; place-items: center; inline-size: 100%; block-size: 100%; border-radius: 50% !important; background: var(--primary); color: var(--on-primary); border: 2px solid var(--surface); font: 500 11px/1 var(--font); box-shadow: var(--elevate1); cursor: pointer; }}
.pin.finish {{ background: var(--on-surface); color: var(--surface); }}
.pin.finish i {{ --_size: 15px; }}
.pin.active {{ background: var(--primary-container); color: var(--on-primary-container); outline: 2px solid var(--primary); }}

/* Stage cards: native <details>, one open at a time (name="stage"). */
details.day {{ background: var(--card); border: 1px solid var(--outline-variant); border-radius: .75rem; margin-block-end: .75rem; scroll-margin-top: 1rem; transition: border-color .2s; }}
details.day[open] {{ border-color: var(--outline); }}
details.day:last-child {{ margin-block-end: 0; }}  /* the pinned map stops at the list's end; no trailing gap */
details.day > summary {{ display: flex; gap: 1rem; align-items: center; padding: 1rem 1.25rem; border-radius: .75rem; }}
details.day > summary:hover {{ background: var(--surface-container-low); }}
.sumtext {{ flex: 1; min-inline-size: 0; }}
.dnum {{ flex: none; inline-size: 2.5rem; block-size: 2.5rem; border-radius: 50%; background: var(--primary-container); color: var(--on-primary-container); font-weight: 500; font-size: 1.125rem; display: grid; place-items: center; }}
.dtitle {{ font-size: 1.125rem; font-weight: 500; line-height: 1.3; text-wrap: balance; }}
.to {{ color: var(--primary); }}
.when {{ font-size: .875rem; }} .when [lang]::first-letter {{ text-transform: uppercase; }}
.chev {{ flex: none; color: var(--on-surface-variant); transition: transform .2s; }}
details[open] > summary .chev {{ transform: rotate(180deg); }}
.dbody {{ padding: 0 1.25rem 1.25rem; }}
.dmeta {{ display: flex; flex-wrap: wrap; gap: .5rem 1rem; align-items: center; justify-content: space-between; }}
.strava-link {{ margin: 0; }}
.strava-link i {{ --_size: 1.125rem; }}
.stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: .75rem; margin-block-start: 1rem; }}
.stats dd {{ font-size: 1.25rem; font-variant-numeric: tabular-nums; }}
blockquote.strava {{ margin-block-start: 1.25rem; background: var(--surface-container-low); font-style: italic; }}
blockquote.strava .upper {{ font-style: normal; letter-spacing: .1em; margin-block-end: .25rem; }}
.notes {{ margin-block-start: 1.25rem; }}
.notes p {{ margin: 0 0 .75rem; }}
.notes.empty {{ padding: .75rem 1rem; border: 1px dashed var(--outline-variant); border-radius: .5rem; color: var(--on-surface-variant); font-size: .9375rem; }}
.hostel {{ display: flex; gap: .75rem; align-items: center; margin-block-start: 1rem; padding: .75rem 1rem; background: var(--surface-container-low); border-radius: .5rem; }}
.hostel > i {{ color: var(--primary); }}
.hostel a {{ display: inline; font-weight: 500; }}
.hostel a i {{ --_size: 1rem; display: inline-flex; vertical-align: -.125rem; margin-inline-start: .25rem; }}
.photos {{ margin-block-start: 1rem; aspect-ratio: 3/1; display: grid; place-items: center; border: 1px dashed var(--outline-variant); border-radius: .5rem; color: var(--on-surface-variant); font-size: .875rem; background: var(--surface-container-low); }}
@media (max-width: 600px) {{ .totals {{ grid-template-columns: repeat(2, 1fr); }} .totals dd {{ font-size: 1.5rem; }} }}
@media (max-width: 820px) {{
  .layout {{ grid-template-columns: 1fr; gap: 2rem; }}
  .mapcol {{ position: static; }}
  #overview {{ block-size: 60vh; }}
  .stats {{ grid-template-columns: repeat(2, 1fr); }}
  .stage-map {{ block-size: 16rem; }}
  details.day > summary {{ padding: .875rem 1rem; gap: .75rem; }}
  .dbody {{ padding: 0 1rem 1rem; }}
}}
</style>
</head>
<body data-lang="fr">
<header class="appbar">
  <nav>
    <a class="brand" href="../../">Philippe Bellefeuille</a>
    <span class="crumb m l">/ Camino Portugués</span>
    <div class="spacer"></div>
    <nav class="group connected" aria-label="Language">
      <button class="small" data-set-lang="fr">FR</button>
      <button class="small" data-set-lang="en">EN</button>
    </nav>
  </nav>
</header>

<main class="container">
<section class="hero">
  <div class="eyebrow"><span lang="fr">10 – 19 octobre 2026 · 10 étapes</span><span lang="en">10 – 19 October 2026 · 10 stages</span></div>
  <h1><span lang="fr">Dix jours vers Saint-Jacques-de-Compostelle</span><span lang="en">Ten days to Santiago de Compostela</span></h1>
  <p class="muted"><span lang="fr">Le Caminho Português par la côte puis le chemin central&nbsp;: départ de Matosinhos, en banlieue de Porto, le samedi 10 octobre, arrivée sur la Praza do Obradoiro le lundi 19 octobre. Chaque étape a été enregistrée sur Strava.</span><span lang="en">The Portuguese Way along the coast, then the central route: out of Matosinhos, just north of Porto, on Saturday 10 October, into the Praza do Obradoiro on Monday 19 October. Every stage was recorded on Strava.</span></p>
  <dl class="totals">
    <div><dt><span lang="fr">Distance totale</span><span lang="en">Total distance</span></dt><dd>{tot_d/1000:.1f} <small>km</small></dd></div>
    <div><dt><span lang="fr">Dénivelé positif</span><span lang="en">Elevation gain</span></dt><dd><span lang="fr">{fr_int(tot_eg)}</span><span lang="en">{tot_eg:,.0f}</span> <small>m</small></dd></div>
    <div><dt><span lang="fr">Temps en marche</span><span lang="en">Moving time</span></dt><dd>{hm(tot_mt)}</dd></div>
    <div><dt><span lang="fr">Durée totale</span><span lang="en">Elapsed time</span></dt><dd>{hm(tot_et)}</dd></div>
    <div><dt><span lang="fr">Moyenne par jour</span><span lang="en">Daily average</span></dt><dd>{tot_d/1000/len(days):.1f} <small>km</small></dd></div>
    <div><dt><span lang="fr">Plus longue étape</span><span lang="en">Longest stage</span></dt><dd>{longest['d']/1000:.1f} <small>km · <span lang="fr">jour</span><span lang="en">day</span> {longest['day']}</small></dd></div>
  </dl>
</section>

<div class="layout">
  <aside class="mapcol">
    <h2 class="section"><span lang="fr">Le parcours</span><span lang="en">The route</span></h2>
    <div class="map" id="overview" role="img" aria-label="Route map, Matosinhos to Santiago de Compostela, ten stages"></div>
  </aside>
  <section class="days">
    <h2 class="section"><span lang="fr">Étape par étape</span><span lang="en">Day by day</span></h2>
    {cards}
  </section>
</div>
<footer class="site"><span lang="fr">Distances, dénivelés et temps tels qu’enregistrés par Strava (temps en marche = sans les pauses).</span><span lang="en">Distances, elevation and times as recorded by Strava (moving time excludes breaks).</span></footer>
</main>
<script src="../../assets/site.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script>
const STAGES = {stages_json};
const dark = window.matchMedia('(prefers-color-scheme: dark)');
// Esri grey canvas basemaps: neutral, keyless, with a separate label layer on top.
const esri = layer => 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/' + layer + '/MapServer/tile/{{z}}/{{y}}/{{x}}';
const tileUrls = () => dark.matches
  ? [esri('World_Dark_Gray_Base'), esri('World_Dark_Gray_Reference')]
  : [esri('World_Light_Gray_Base'), esri('World_Light_Gray_Reference')];
const ATTR = 'Tiles &copy; Esri, HERE, Garmin, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>';
const tileLayers = [];

function baseMap(el, opts) {{
  const map = L.map(el, Object.assign({{ scrollWheelZoom: false, zoomSnap: 0.25, maxZoom: 16 }}, opts));
  const [base, labels] = tileUrls();
  const pane = map.createPane('labels');  // labels above the base, below the routes
  pane.style.zIndex = 350; pane.style.pointerEvents = 'none';
  const pair = [L.tileLayer(base, {{ attribution: ATTR, maxZoom: 16 }}).addTo(map), L.tileLayer(labels, {{ maxZoom: 16, pane: 'labels' }}).addTo(map)];
  tileLayers.push(pair);
  return map;
}}
dark.addEventListener('change', () => {{ const u = tileUrls(); tileLayers.forEach(([b, l]) => {{ b.setUrl(u[0]); l.setUrl(u[1]); }}); }});

function pin(latlng, label, cls, size) {{
  return L.marker(latlng, {{ icon: L.divIcon({{ className: '', html: '<div class="pin ' + (cls || '') + '">' + label + '</div>', iconSize: [size, size] }}), keyboard: false }});
}}
const stageName = s => s.day + ' · ' + s.from + ' → ' + s.to + ' · ' + s.km + ' km';
const card = day => document.getElementById('day' + day);

// Overview: every stage is a clickable line with a wider invisible hit area.
const overview = baseMap('overview', {{ zoomControl: true }});
const allBounds = L.latLngBounds(STAGES.flatMap(s => s.line));
const fitAll = () => overview.fitBounds(allBounds, {{ padding: [24, 24] }});
fitAll();  // a view must exist before vector layers are added
const lines = {{}}, pins = {{}};
const all = L.featureGroup().addTo(overview);
STAGES.forEach(s => {{
  const line = L.polyline(s.line, {{ className: 'route', interactive: false }}).addTo(all);
  const hit = L.polyline(s.line, {{ className: 'hit', weight: 18, opacity: 0 }}).addTo(overview);
  hit.bindTooltip(stageName(s), {{ sticky: true, direction: 'top', offset: [0, -8] }});
  hit.on('mouseover', () => line.getElement().classList.add('hover'));
  hit.on('mouseout', () => line.getElement().classList.remove('hover'));
  hit.on('click', () => openStage(s.day, true));
  const p = pin(s.line[0], s.day, '', 22).addTo(overview);
  p.bindTooltip(stageName(s), {{ direction: 'top', offset: [0, -12] }});
  p.on('click', () => openStage(s.day, true));
  lines[s.day] = line; pins[s.day] = p;
}});
const last = STAGES[STAGES.length - 1];
pin(last.line[last.line.length - 1], '<i>flag</i>', 'finish', 26).addTo(overview)
  .bindTooltip('Santiago de Compostela', {{ direction: 'top', offset: [0, -14] }});

function highlight(day) {{
  STAGES.forEach(s => {{
    const el = lines[s.day].getElement(), on = s.day === day;
    el.classList.toggle('active', on);
    el.classList.toggle('dim', day != null && !on);
    pins[s.day].getElement().firstChild.classList.toggle('active', on);
  }});
  if (day != null) lines[day].bringToFront();
}}

// Stage maps are created the first time a stage opens (Leaflet needs a visible container).
const stageMaps = {{}};
function stageMap(day) {{
  const s = STAGES[day - 1], el = card(day).querySelector('.stage-map');
  if (stageMaps[day]) {{ stageMaps[day].invalidateSize(); return; }}
  const map = baseMap(el, {{ dragging: !L.Browser.mobile, tap: false }});
  map.fitBounds(L.latLngBounds(s.line), {{ padding: [28, 28] }});
  STAGES.forEach(o => {{ if (o.day !== day) L.polyline(o.line, {{ className: 'route-ctx', interactive: false }}).addTo(map); }});
  L.polyline(s.line, {{ className: 'route active', interactive: false }}).addTo(map);
  pin(s.line[0], s.day, '', 22).addTo(map).bindTooltip(s.from, {{ direction: 'top', offset: [0, -12] }});
  if (day === STAGES.length) pin(s.line[s.line.length - 1], '<i>flag</i>', 'finish', 26).addTo(map).bindTooltip(s.to, {{ direction: 'top', offset: [0, -14] }});
  else pin(s.line[s.line.length - 1], s.day + 1, '', 22).addTo(map).bindTooltip(s.to, {{ direction: 'top', offset: [0, -12] }});
  stageMaps[day] = map;
}}

function openStage(day, scroll) {{
  const el = card(day);
  if (!el.open) el.open = true; else onOpen(el);
  if (scroll) requestAnimationFrame(() => el.scrollIntoView({{ behavior: 'smooth', block: 'start' }}));
}}
function onOpen(el) {{
  const day = +el.dataset.day;
  stageMap(day);
  highlight(day);
  history.replaceState(null, '', '#day' + day);
  const top = el.getBoundingClientRect().top;
  if (top < 0 || top > innerHeight * 0.8) el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
}}
document.querySelectorAll('details.day').forEach(el => el.addEventListener('toggle', () => {{
  if (el.open) onOpen(el);
  else if (!document.querySelector('details.day[open]')) {{ highlight(null); history.replaceState(null, '', location.pathname + location.search); }}
}}));

// Desktop: the overview map is as tall as the day list (every day collapsed) so both columns
// line up, but never taller than the window, so the pinned map is always fully visible.
// When the list is taller than the window, the tops line up at the start and the pinned map
// comes to rest with its bottom on the last day at the end. A ResizeObserver re-measures whenever the list or layout changes
// size: window resize, fonts or icons finishing loading, FR/EN switch, scrollbar appearing.
const wide = window.matchMedia('(min-width: 821px)');
const STICKY_TOP = 16;  // matches .mapcol {{ top: 1rem }}
function alignMap() {{
  const ov = document.getElementById('overview');
  if (!wide.matches) {{ if (ov.style.height) {{ ov.style.height = ''; overview.invalidateSize(); }} return; }}
  const cards = [...document.querySelectorAll('details.day')];
  let openExtra = 0;
  cards.forEach(c => {{
    if (c.open) openExtra += c.getBoundingClientRect().height - c.querySelector('summary').getBoundingClientRect().height - 2;
  }});
  const daysTop = document.querySelector('.days').getBoundingClientRect().top;
  const listBottom = cards[cards.length - 1].getBoundingClientRect().bottom - daysTop - openExtra;
  const ovOffset = ov.getBoundingClientRect().top - document.querySelector('.mapcol').getBoundingClientRect().top;
  const fitsWindow = innerHeight - ovOffset - 2 * STICKY_TOP;
  const h = Math.max(320, Math.min(listBottom - ovOffset, fitsWindow));
  if (Math.abs(ov.getBoundingClientRect().height - h) > 0.5) {{ ov.style.height = h + 'px'; overview.invalidateSize(); fitAll(); }}
}}
const ro = new ResizeObserver(() => requestAnimationFrame(alignMap));
ro.observe(document.querySelector('.days'));
ro.observe(document.querySelector('.layout'));
wide.addEventListener('change', alignMap);
window.addEventListener('resize', alignMap);  // window height changes don't resize the list
alignMap();

const m = location.hash.match(/^#day(\\d+)$/);
if (m && card(+m[1])) openStage(+m[1], true);
</script>
</body>
</html>
"""
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(page); print(OUT, len(page))
