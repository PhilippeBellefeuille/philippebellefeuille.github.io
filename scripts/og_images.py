"""Social preview images (Open Graph, 1200x630) for the site.

Shown by WhatsApp, iMessage, Facebook, LinkedIn, Slack, X… when a link is shared.
The text is language-neutral (place names and numbers) because link previews can't
follow the visitor's language.

    .venv/bin/python scripts/og_images.py

Writes docs/og.jpg (home page) and docs/trips/camino-portugues-2026/og.jpg.
Source photos come from photos-originals/ (gitignored); if missing, the published
1600 px WebP is used instead.
"""
import json, math, pathlib
import polyline
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT = ROOT / 'scripts' / 'fonts' / 'Roboto.ttf'
W, H = 1200, 630
PAD = 72
ACCENT = (163, 201, 234)        # --primary in dark theme
WHITE = (255, 255, 255)
SOFT = (255, 255, 255, 200)


def font(size, weight):
    f = ImageFont.truetype(str(FONT), size)
    f.set_variation_by_axes([weight, 100])
    return f


def photo(name, published):
    src = next(ROOT.glob(f'photos-originals/**/{name}'), None)
    im = Image.open(src) if src else Image.open(ROOT / 'docs' / published)
    return ImageOps.exif_transpose(im).convert('RGB')


def cover(im, focus_y=0.5):
    """Crop to 1200x630 keeping full width, vertical position set by focus_y (0 top, 1 bottom)."""
    scale = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = round((im.height - H) * focus_y)
    return im.crop((x, y, x + W, y + H))


def shade(im, strength=0.9, reach=0.85):
    """Dark gradient from the left so white text stays readable on any photo."""
    grad = Image.new('L', (W, 1))
    for x in range(W):
        t = max(0.0, 1 - x / (W * reach))
        grad.putpixel((x, 0), round(255 * strength * (t ** 1.4)))
    bottom = Image.new('L', (1, H))   # plus a light fade at the bottom for the URL line
    for y in range(H):
        t = max(0.0, (y - H * 0.55) / (H * 0.45))
        bottom.putpixel((0, y), round(255 * 0.55 * t))
    dark = Image.new('RGB', (W, H), (12, 16, 22))
    im = Image.composite(dark, im, grad.resize((W, H)))
    return Image.composite(dark, im, bottom.resize((W, H)))


def text(d, xy, s, f, fill, spacing=0):
    if spacing:
        x, y = xy
        for ch in s:
            d.text((x, y), ch, font=f, fill=fill)
            x += d.textlength(ch, font=f) + spacing
        return x
    d.text(xy, s, font=f, fill=fill)
    return xy[0] + d.textlength(s, font=f)


def arrow(d, x, y, size, fill):
    """A right arrow drawn as a shape (Roboto has no → glyph). Returns the x after it."""
    w, t = size * 0.78, max(3, round(size * 0.085))
    mid = y + size * 0.56
    d.line((x, mid, x + w - t, mid), fill=fill, width=t)
    d.polygon([(x + w, mid), (x + w - size * 0.3, mid - size * 0.24), (x + w - size * 0.3, mid + size * 0.24)], fill=fill)
    return x + w + size * 0.28


def route_trace(d, box, days):
    """Draw the whole Camino as a thin line with a dot per stage start, inside box."""
    pts = [p for day in days for p in polyline.decode(day['pl'])]
    lats = [p[0] for p in pts]; lons = [p[1] for p in pts]
    x0, y0, x1, y1 = box
    k = math.cos(math.radians(sum(lats) / len(lats)))
    sx = (x1 - x0) / ((max(lons) - min(lons)) * k or 1)
    sy = (y1 - y0) / (max(lats) - min(lats))
    s = min(sx, sy)
    cx = (x0 + x1) / 2 - ((max(lons) + min(lons)) / 2 - min(lons)) * k * s
    xy = lambda la, lo: (cx + (lo - min(lons)) * k * s, y1 - (la - min(lats)) * s)
    d.line([xy(*p) for p in pts], fill=ACCENT, width=4, joint='curve')
    for day in days:
        a = polyline.decode(day['pl'])[0]
        x, y = xy(*a); d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=WHITE)
    x, y = xy(*polyline.decode(days[-1]['pl'])[-1])
    d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=ACCENT, outline=WHITE, width=3)


def camino():
    trip = ROOT / 'trips' / 'camino-portugues-2026'
    days = json.load(open(trip / 'data' / 'days.json'))
    km = sum(d['d'] for d in days) / 1000
    climb = sum(d['eg'] for d in days)
    im = shade(cover(photo('IMG_6947.jpeg', 'trips/camino-portugues-2026/img/day10/img_6947-1600.webp'), 0.35), strength=0.9, reach=0.85)
    d = ImageDraw.Draw(im, 'RGBA')

    route_trace(d, (PAD, 150, PAD + 70, H - 120), days)
    x = PAD + 120
    text(d, (x, 150), 'CAMINO PORTUGUÉS · 2026', font(24, 600), ACCENT, spacing=3)
    d.text((x, 196), 'Matosinhos', font=font(66, 700), fill=WHITE)
    ax = arrow(d, x, 272, 66, ACCENT)
    d.text((ax, 272), 'Santiago de', font=font(66, 700), fill=WHITE)
    d.text((x, 348), 'Compostela', font=font(66, 700), fill=WHITE)
    stats = f'{km:.0f} km   ·   +{climb:,.0f} m   ·   10 – 19.10.2026'.replace(',', ' ')
    d.text((x, 452), stats, font=font(30, 500), fill=SOFT)
    d.text((x, H - 112), 'philippebellefeuille.com', font=font(24, 400), fill=(255, 255, 255, 170))
    out = ROOT / 'docs' / 'trips' / 'camino-portugues-2026' / 'og.jpg'
    im.save(out, 'JPEG', quality=86, optimize=True, progressive=True)
    return out


def home():
    im = shade(cover(photo('IMG_6947.jpeg', 'trips/camino-portugues-2026/img/day10/img_6947-1600.webp'), 0.35), strength=0.92, reach=0.8)
    d = ImageDraw.Draw(im, 'RGBA')
    x = PAD
    text(d, (x, 190), 'PHILIPPEBELLEFEUILLE.COM', font(24, 600), ACCENT, spacing=3)
    d.text((x, 236), 'Philippe', font=font(84, 700), fill=WHITE)
    d.text((x, 330), 'Bellefeuille', font=font(84, 700), fill=WHITE)
    d.text((x, 456), 'Récits de voyage  ·  Trip reports  ·  Путевые заметки', font=font(30, 500), fill=SOFT)
    out = ROOT / 'docs' / 'og.jpg'
    im.save(out, 'JPEG', quality=86, optimize=True, progressive=True)
    return out


if __name__ == '__main__':
    for f in (camino(), home()):
        print(f.relative_to(ROOT), f'{f.stat().st_size // 1024} KB')
