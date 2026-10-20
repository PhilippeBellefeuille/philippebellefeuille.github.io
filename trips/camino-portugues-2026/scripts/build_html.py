import json, datetime as dt, html, pathlib
TRIP=pathlib.Path(__file__).resolve().parent.parent
OUT=TRIP.parent.parent/'docs'/'trips'/TRIP.name/'index.html'
days=json.load(open(TRIP/'data/days.json')); svg=json.load(open(TRIP/'data/svg.json'))
W,H=svg['W'],svg['H']
def hm(s): return f"{s//3600}h{(s%3600)//60:02d}"
tot_d=sum(d['d'] for d in days); tot_eg=sum(d['eg'] for d in days); tot_mt=sum(d['mt'] for d in days); tot_et=sum(d['et'] for d in days)
FR_DAYS=['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']; FR_MON={10:'octobre'}
def fdate(s,lang):
    if lang=='en': return s.strftime('%A %-d %B %Y')
    return f"{FR_DAYS[s.weekday()]} {s.day} {FR_MON[s.month]} {s.year}"
# map svg
towns=svg['towns']
route=''.join(f'<path class="route" d="{d["path"]}"/>' for d in svg['days'])
marks=''
for d in svg['days']:
    x,y=d['start']; marks+=f'<circle class="mk" cx="{x}" cy="{y}" r="4.5"/><text class="mkn" x="{x+8}" y="{y+3.5}">{d["day"]}</text>'
ex,ey=svg['days'][-1]['end']; marks+=f'<circle class="mk end" cx="{ex}" cy="{ey}" r="6"/>'
labels=''
for name,(x,y) in towns.items():
    stage=name in {d['from'] for d in days}|{'Santiago de Compostela'}
    anchor='end' if name in ('Vigo','Viana do Castelo','Póvoa de Varzim','Matosinhos','Paredes de Coura') else 'start'
    dx=-10 if anchor=='end' else (22 if stage else 8)
    labels+=f'<text class="town{" stage" if stage else ""}" x="{x+dx}" y="{y+4}" text-anchor="{anchor}">{html.escape(name)}</text>'
    if not stage: labels+=f'<circle class="ctx" cx="{x}" cy="{y}" r="2.5"/>'
mapsvg=f'''<svg viewBox="0 0 {W} {H}" role="img" aria-label="Route map, Matosinhos to Santiago de Compostela" preserveAspectRatio="xMidYMid meet">
<rect width="{W}" height="{H}" class="sea"/>
<path class="coast" d="{svg['coast']}"/>
<path class="river" d="{svg['rivers']}"/>
<path class="pt-es" d="{svg['border']}"/>
{route}{labels}{marks}
<text class="ocean" x="40" y="{H*0.55:.0f}" transform="rotate(-90 40 {H*0.55:.0f})">OCEANO ATLÂNTICO</text>
<text class="country" x="{W-16}" y="{towns["Tui"][1]-60:.0f}" text-anchor="end">GALICIA · ES</text>
<text class="country" x="{W-16}" y="{towns['Tui'][1]+40:.0f}" text-anchor="end">PORTUGAL</text>
</svg>'''
# day cards
cards=''
for d in days:
    s=dt.datetime.fromisoformat(d['start']); e=s+dt.timedelta(seconds=d['et'])
    desc=html.escape(d['desc']).replace('\n','<br>')
    descblk=f'<blockquote class="strava"><div class="small-text muted upper">Strava</div>{desc}</blockquote>' if d['desc'] else ''
    cards+=f"""
<article class="border day" id="day{d['day']}">
  <div class="head">
    <div class="dnum">{d['day']}</div>
    <div>
      <h2 class="dtitle">{html.escape(d['from'])} <span class="to">→</span> {html.escape(d['to'])}</h2>
      <div class="muted when"><span lang="fr">{fdate(s,'fr')}</span><span lang="en">{fdate(s,'en')}</span> · {s.strftime('%H:%M')} – {e.strftime('%H:%M')}</div>
    </div>
  </div>
  <dl class="stats">
    <div><dt><span lang="fr">Distance</span><span lang="en">Distance</span></dt><dd>{d['d']/1000:.1f} <small>km</small></dd></div>
    <div><dt><span lang="fr">Dénivelé +</span><span lang="en">Elevation gain</span></dt><dd>{d['eg']:.0f} <small>m</small></dd></div>
    <div><dt><span lang="fr">En marche</span><span lang="en">Moving time</span></dt><dd>{hm(d['mt'])}</dd></div>
    <div><dt><span lang="fr">Durée totale</span><span lang="en">Elapsed</span></dt><dd>{hm(d['et'])}</dd></div>
  </dl>
  {descblk}
  <div class="notes"><span lang="fr">Vos notes pour cette étape viendront ici.</span><span lang="en">Your own notes for this day will go here.</span></div>
  <div class="photos"><span lang="fr">Photos de l’étape à venir</span><span lang="en">Photos for this day coming soon</span></div>
</article>"""
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
<link rel="stylesheet" href="../../assets/site.css">
<style>
/* Layout: route map pinned in a left column, totals and the ten stages flow on the right; stacks on phones. */
.eyebrow {{ color: var(--primary); font-size: .875rem; font-weight: 500; letter-spacing: .08em; text-transform: uppercase; }}
.hero h1 {{ font-size: clamp(2rem, 5vw, 3rem); font-weight: 400; line-height: 1.15; margin: .5rem 0 1rem; text-wrap: balance; }}
.hero p {{ max-inline-size: 62ch; font-size: 1.125rem; }}
.totals {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(9.5rem, 1fr)); gap: .75rem; margin-block-start: 2rem; }}
.totals > div {{ background: var(--surface-container-low); border: 1px solid var(--outline-variant); border-radius: .75rem; padding: 1rem; }}
.totals dt, .stats dt {{ font-size: .75rem; font-weight: 500; letter-spacing: .06em; text-transform: uppercase; color: var(--on-surface-variant); }}
.totals dd {{ font-size: 1.75rem; line-height: 1.2; margin-block-start: .25rem; font-variant-numeric: tabular-nums; }}
.totals dd small, .stats dd small {{ font-size: .875rem; color: var(--on-surface-variant); }}
.layout {{ display: grid; grid-template-columns: minmax(16rem, 23rem) 1fr; gap: 2.5rem; margin-block-start: 2.5rem; align-items: start; }}
.mapcol {{ position: sticky; top: 1rem; }}
h2.section {{ font-size: 1.375rem; font-weight: 400; margin-block-end: .75rem; }}
.mapcol svg {{ inline-size: 100%; block-size: auto; display: block; border: 1px solid var(--outline-variant); border-radius: .75rem; background: var(--surface-container-low); fill: none; }}
.sea {{ fill: var(--surface-container-low); }}
.coast {{ fill: none; stroke: var(--outline); stroke-width: 1.1; }}
.river {{ fill: none; stroke: var(--outline-variant); stroke-width: .9; }}
.pt-es {{ fill: none; stroke: var(--on-surface-variant); stroke-width: 1; stroke-dasharray: 4 3; }}
.route {{ fill: none; stroke: var(--primary); stroke-width: 2.6; stroke-linejoin: round; stroke-linecap: round; }}
.mk {{ fill: var(--primary); stroke: var(--surface); stroke-width: 1.5; }} .mk.end {{ fill: var(--on-surface); }}
.mkn {{ font: 700 10px var(--font); fill: var(--on-surface); }}
.town {{ font: 11px var(--font); fill: var(--on-surface-variant); }} .town.stage {{ font-weight: 500; fill: var(--on-surface); }}
.ctx {{ fill: var(--on-surface-variant); }}
.ocean, .country {{ font: 500 10px var(--font); letter-spacing: .2em; fill: var(--outline); }}
.legend {{ font-size: .8125rem; }}
.days {{ min-inline-size: 0; }}
article.day {{ --_padding: 1.25rem 1.5rem; margin-block-end: 1rem; background: var(--card); }}
.day .head {{ display: flex; gap: 1rem; align-items: flex-start; }}
.dnum {{ flex: none; inline-size: 2.5rem; block-size: 2.5rem; border-radius: 50%; background: var(--primary-container); color: var(--on-primary-container); font-weight: 500; font-size: 1.125rem; display: grid; place-items: center; }}
.dtitle {{ font-size: 1.25rem; font-weight: 500; line-height: 1.3; margin-block: .125rem; text-wrap: balance; }}
.to {{ color: var(--primary); }}
.when {{ font-size: .875rem; }} .when [lang]::first-letter {{ text-transform: uppercase; }}
.stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: .75rem; margin-block-start: 1.25rem; }}
.stats dd {{ font-size: 1.25rem; font-variant-numeric: tabular-nums; }}
blockquote.strava {{ margin-block-start: 1.25rem; background: var(--surface-container-low); font-style: italic; }}
blockquote.strava .upper {{ font-style: normal; letter-spacing: .1em; margin-block-end: .25rem; }}
.notes {{ margin-block-start: 1rem; padding: .75rem 1rem; border: 1px dashed var(--outline-variant); border-radius: .5rem; color: var(--on-surface-variant); font-size: .9375rem; }}
.photos {{ margin-block-start: 1rem; aspect-ratio: 3/1; display: grid; place-items: center; border: 1px dashed var(--outline-variant); border-radius: .5rem; color: var(--on-surface-variant); font-size: .875rem; background: var(--surface-container-low); }}
@media (max-width: 820px) {{ .layout {{ grid-template-columns: 1fr; gap: 2rem; }} .mapcol {{ position: static; }} .mapcol svg {{ max-block-size: 80vh; }} .stats {{ grid-template-columns: repeat(2, 1fr); }} article.day {{ --_padding: 1rem; }} }}
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
    <div><dt><span lang="fr">Dénivelé positif</span><span lang="en">Elevation gain</span></dt><dd>{tot_eg:,.0f} <small>m</small></dd></div>
    <div><dt><span lang="fr">Temps en marche</span><span lang="en">Moving time</span></dt><dd>{hm(tot_mt)}</dd></div>
    <div><dt><span lang="fr">Durée totale</span><span lang="en">Elapsed time</span></dt><dd>{hm(tot_et)}</dd></div>
    <div><dt><span lang="fr">Moyenne par jour</span><span lang="en">Daily average</span></dt><dd>{tot_d/1000/len(days):.1f} <small>km</small></dd></div>
    <div><dt><span lang="fr">Plus longue étape</span><span lang="en">Longest stage</span></dt><dd>{longest['d']/1000:.1f} <small>km · <span lang="fr">jour</span><span lang="en">day</span> {longest['day']}</small></dd></div>
  </dl>
</section>

<div class="layout">
  <aside class="mapcol">
    <h2 class="section"><span lang="fr">Le parcours</span><span lang="en">The route</span></h2>
    {mapsvg}
    <p class="legend muted"><span lang="fr">Les numéros marquent le départ de chaque étape. Tracés GPS de Strava, fond de carte Natural Earth.</span><span lang="en">Numbers mark the start of each stage. GPS tracks from Strava, base map from Natural Earth.</span></p>
  </aside>
  <section class="days">
    <h2 class="section"><span lang="fr">Étape par étape</span><span lang="en">Day by day</span></h2>
    {cards}
  </section>
</div>
<footer class="site"><span lang="fr">Distances, dénivelés et temps tels qu’enregistrés par Strava (temps en marche = sans les pauses).</span><span lang="en">Distances, elevation and times as recorded by Strava (moving time excludes breaks).</span></footer>
</main>
<script src="../../assets/site.js"></script>
</body>
</html>
"""
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(page); print(OUT, len(page))
