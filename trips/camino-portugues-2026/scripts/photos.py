"""Turn the photos exported from Apple Photos into web images for the trip page.

Input:  photos-originals/ at the repo root (gitignored, subfolders included), filled with File → Export from
        the "Camino Portugese 2026" album: JPEG, full size, location information on.
Output: docs/trips/camino-portugues-2026/img/dayN/<name>-1600.webp and <name>-600.webp,
        with all metadata stripped (no GPS, no camera info), and data/photos.json.

Each photo goes to a day by its local capture date (10 Oct = day 1 … 19 Oct = day 10).
Photos outside those dates are left out and listed so Philippe can decide. Each photo's
GPS position is checked against that day's track, and far-off ones are flagged.

Re-running only converts new or changed photos and keeps captions/featured flags already
set in photos.json. Run from the repo root:
    .venv/bin/python trips/camino-portugues-2026/scripts/photos.py
"""
import datetime as dt, json, math, pathlib, sys
import polyline
from PIL import Image, ImageOps, ExifTags
import pillow_heif

pillow_heif.register_heif_opener()

TRIP = pathlib.Path(__file__).resolve().parent.parent
ROOT = TRIP.parent.parent
SRC = ROOT / 'photos-originals'
OUT = ROOT / 'docs' / 'trips' / TRIP.name / 'img'
DATA = TRIP / 'data' / 'photos.json'
SIZES = {'1600': 1600, '600': 600}   # long edge in px
QUALITY = {'1600': 78, '600': 72}
FIRST_DAY = dt.date(2026, 10, 10)
FAR_KM = 3.0                         # flag photos further than this from the day's track
EXTS = {'.jpg', '.jpeg', '.heic', '.png'}

days = json.load(open(TRIP / 'data' / 'days.json'))
tracks = {d['day']: polyline.decode(d['pl']) for d in days}


def km(a, b):
    return math.hypot((a[0] - b[0]) * 111.2, (a[1] - b[1]) * 111.2 * math.cos(math.radians(a[0])))


def dms(v, ref):
    d = float(v[0]) + float(v[1]) / 60 + float(v[2]) / 3600
    return -d if ref in ('S', 'W') else d


def read_meta(im):
    ex = im.getexif()
    exif = ex.get_ifd(ExifTags.IFD.Exif)
    gps = ex.get_ifd(ExifTags.IFD.GPSInfo)
    taken = exif.get(36867) or ex.get(306)          # DateTimeOriginal, else DateTime
    taken = dt.datetime.strptime(taken, '%Y:%m:%d %H:%M:%S') if taken else None
    offset = exif.get(36881)                         # OffsetTimeOriginal, e.g. +01:00
    latlon = None
    if gps.get(2) and gps.get(4):
        latlon = (dms(gps[2], gps.get(1)), dms(gps[4], gps.get(3)))
    return taken, offset, latlon


def main():
    old = {p['src']: p for p in json.load(open(DATA))} if DATA.exists() else {}
    # Exports can be split across subfolders (e.g. a first export, then a retry of the
    # failed items). Search them all; the same file name twice counts once.
    all_files = sorted(f for f in SRC.rglob('*') if f.is_file() and not f.name.startswith('.')) if SRC.exists() else []
    files, seen, dupes = [], set(), []
    for f in all_files:
        if f.suffix.lower() not in EXTS: continue
        if f.name in seen: dupes.append(str(f.relative_to(SRC))); continue
        seen.add(f.name); files.append(f)
    skipped_other = sorted(str(f.relative_to(SRC)) for f in all_files if f.suffix.lower() not in EXTS)
    photos, outside, no_date, far, converted = [], [], [], [], 0

    for f in files:
        with Image.open(f) as im:
            taken, offset, latlon = read_meta(im)
            if not taken:
                no_date.append(f.name); continue
            day = (taken.date() - FIRST_DAY).days + 1   # EXIF time is already local time
            if not 1 <= day <= len(days):
                outside.append(f"{f.name} ({taken:%Y-%m-%d %H:%M})"); continue
            stem = f.stem.lower()
            outdir = OUT / f'day{day}'
            targets = {k: outdir / f'{stem}-{k}.webp' for k in SIZES}
            if not all(t.exists() and t.stat().st_mtime >= f.stat().st_mtime for t in targets.values()):
                outdir.mkdir(parents=True, exist_ok=True)
                img = ImageOps.exif_transpose(im).convert('RGB')
                for k, edge in SIZES.items():
                    r = img.copy(); r.thumbnail((edge, edge), Image.LANCZOS)
                    r.save(targets[k], 'WEBP', quality=QUALITY[k], method=6)  # no exif= → metadata stripped
                converted += 1
            with Image.open(targets['1600']) as big:
                w, h = big.size
        dist = min(km(latlon, p) for p in tracks[day]) if latlon else None
        if dist is not None and dist > FAR_KM:
            far.append(f"{f.name}: day {day}, {dist:.1f} km from the track")
        prev = old.get(f.name, {})
        photos.append({
            'src': f.name, 'day': day, 'taken': taken.isoformat(timespec='minutes') + (offset or ''),
            'file': f'img/day{day}/{stem}', 'w': w, 'h': h,
            'featured': prev.get('featured', False),
            'caption': prev.get('caption', {'fr': '', 'en': ''}),
        })

    photos.sort(key=lambda p: (p['day'], p['taken']))
    DATA.write_text(json.dumps(photos, ensure_ascii=False, indent=2) + '\n')

    # Report
    print(f'{len(files)} photos read, {converted} converted, {len(photos)} placed on the page.')
    for d in range(1, len(days) + 1):
        print(f'  day {d:2}: {sum(p["day"] == d for p in photos)}')
    for title, items in (('Outside 10–19 Oct (left out)', outside), ('No date (left out)', no_date),
                         ('Far from that day\'s track (check)', far), ('Not photos (ignored)', skipped_other),
                         ('Same file name exported twice (second copy ignored)', dupes)):
        if items:
            print(f'{title}:'); [print('  ' + i) for i in items]


if __name__ == '__main__':
    sys.exit(main())
