import json, math, polyline, pathlib
TRIP=pathlib.Path(__file__).resolve().parent.parent
days=json.load(open(TRIP/'data/days.json'))
LON0,LON1,LAT0,LAT1=-9.15,-8.05,41.05,43.0
W=440; k=math.cos(math.radians(42.0))
H=W*(LAT1-LAT0)/((LON1-LON0)*k)
def xy(lon,lat): return ((lon-LON0)/(LON1-LON0)*W, (LAT1-lat)/(LAT1-LAT0)*H)
def path(coords):
    out=[]; 
    for i,(lon,lat) in enumerate(coords):
        x,y=xy(lon,lat); out.append(f"{'M' if i==0 else 'L'}{x:.1f} {y:.1f}")
    return ''.join(out)
def inb(lon,lat,pad=0.3): return LON0-pad<=lon<=LON1+pad and LAT0-pad<=lat<=LAT1+pad
def lines(fn):
    g=json.load(open(fn)); res=[]
    for f in g['features']:
        geom=f['geometry']; parts=geom['coordinates'] if geom['type']=='MultiLineString' else [geom['coordinates']]
        for part in parts:
            if any(inb(lon,lat) for lon,lat in part):
                # split into segments within bbox
                seg=[]
                for lon,lat in part:
                    if inb(lon,lat): seg.append((lon,lat))
                    else:
                        if len(seg)>1: res.append(seg)
                        seg=[]
                if len(seg)>1: res.append(seg)
    return res
coast=lines(TRIP/'data/ne/ne_10m_coastline.geojson')
border=lines(TRIP/'data/ne/ne_10m_admin_0_boundary_lines_land.geojson')
rivers=[s for s in lines(TRIP/'data/ne/ne_10m_rivers_lake_centerlines.geojson')]
print(len(coast),len(border),len(rivers), round(H))
svg={'W':W,'H':round(H,1),'coast':' '.join(path(s) for s in coast),'border':' '.join(path(s) for s in border),'rivers':' '.join(path(s) for s in rivers)}
svg['days']=[]
for d in days:
    pts=polyline.decode(d['pl']); coords=[(lon,lat) for lat,lon in pts]
    sx,sy=xy(*coords[0]); ex,ey=xy(*coords[-1])
    svg['days'].append({'day':d['day'],'path':path(coords),'start':[round(sx,1),round(sy,1)],'end':[round(ex,1),round(ey,1)]})
# towns
towns={'Porto':(-8.611,41.149),'Matosinhos':(-8.69,41.18),'Póvoa de Varzim':(-8.763,41.383),'Barcelos':(-8.618,41.531),'Ponte de Lima':(-8.584,41.767),'Tui':(-8.644,42.047),'Redondela':(-8.61,42.283),'Pontevedra':(-8.645,42.431),'Caldas de Reis':(-8.643,42.605),'Padrón':(-8.661,42.738),'Santiago de Compostela':(-8.545,42.878),'Vigo':(-8.72,42.24),'Braga':(-8.42,41.55),'Viana do Castelo':(-8.83,41.69)}
for d in days:
    pts=polyline.decode(d['pl']); towns[d['from']]=(pts[0][1],pts[0][0])
    if d['day']==10: towns['Santiago de Compostela']=(pts[-1][1],pts[-1][0])
svg['towns']={k:[round(v,1) for v in xy(*p)] for k,p in towns.items()}
json.dump(svg,open(TRIP/'data/svg.json','w'))
