"""Generic brand-kit builder: one mark + one wordmark + one palette -> a /brand folder.

Usage: python3 generator/brandkit.py jma-events registration-space
Requires: pip install fonttools uharfbuzz brotli cairosvg pillow
"""
import os, sys, json, io, shutil
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
import cairosvg
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_SRC = os.path.join(ROOT, 'generator', 'fonts')
WHITE = '#FFFFFF'; BLACK = '#000000'

# ---------------- marks ----------------
def j_mark():
    u = 264.0; H = 2.75 * u; fw = 1.25 * u; fh = 1.25 * u
    def gap(small): return (0.13 if small else 0.04) * H
    def width(small): return fw + gap(small) + u
    def paths(ox, oy, s, small=False):
        g = gap(small)
        X = lambda v: f"{ox + v*s:.3f}"; Y = lambda v: f"{oy + v*s:.3f}"; R = lambda v: f"{v*s:.3f}"
        top = H - fh
        foot = (f"M{X(0)} {Y(top)} H{X(fw-u)} A{R(u)} {R(u)} 0 0 1 {X(fw)} {Y(top+u)} V{Y(H)} H{X(u)} "
                f"A{R(u)} {R(u)} 0 0 1 {X(0)} {Y(H-u)} Z")
        sx = fw + g
        stem = f"M{X(sx)} {Y(u)} A{R(u)} {R(u)} 0 0 1 {X(sx+u)} {Y(0)} V{Y(H-u)} A{R(u)} {R(u)} 0 0 1 {X(sx)} {Y(H)} Z"
        return foot + " " + stem
    return dict(height=H, width=width, paths=paths, name='J', share=0.64, maskable_share=0.52,
                construction="- **Grid unit u** is the stem width. The stem is 1u × 2.75u; the foot is 1.25u × 1.25u.\n"
                             "- **One radius only:** every curve is radius u: the stem's top-left and bottom-right, and the foot's top-right and bottom-left.\n"
                             "- **The split** is 4% of the J's height, widened to 13% in the small-size cut so it survives at 16–32 px.")

def r_mark():
    u = 232.0; H = 2.5 * u; SW, SH, SR = 1.125 * u, 1.0 * u, 0.75 * u
    def width(small): return u + (0.10 if small else 0.04) * H + SW
    def paths(ox, oy, s, small=False):
        g = (0.10 if small else 0.04) * H
        X = lambda v: f"{ox + v*s:.3f}"; Y = lambda v: f"{oy + v*s:.3f}"; R = lambda v: f"{v*s:.3f}"
        stem = f"M{X(0)} {Y(u)} A{R(u)} {R(u)} 0 0 1 {X(u)} {Y(0)} V{Y(H)} H{X(0)} Z"
        x0 = u + g
        sh = (f"M{X(x0)} {Y(SR)} A{R(SR)} {R(SR)} 0 0 1 {X(x0+SR)} {Y(0)} H{X(x0+SW)} V{Y(SH-SR)} "
              f"A{R(SR)} {R(SR)} 0 0 1 {X(x0+SW-SR)} {Y(SH)} H{X(x0)} Z")
        return stem + " " + sh
    return dict(height=H, width=width, paths=paths, name='r', share=0.56, maskable_share=0.46,
                construction="- **Grid unit u** is the stem width. The stem is 1u × 2.5u with a quarter-circle top-left (radius u); "
                             "the shoulder is 1.125u × 1u.\n"
                             "- **Two radii only:** u for the stem, ¾u for the shoulder's top-left and bottom-right curves.\n"
                             "- **The split** is 4% of the r's height (10% in the small cut).\n"
                             "- Built on the same system as the jma.events J, so the two marks read as a family.")

BRANDS = {
  'jma-events': dict(slug='jma-events', name='jma.events', legal='JMA Event Services Ltd', bold='jma', regular='events',
                     mark=j_mark(), min_lockup=('120 px', '30 mm'), primary='#2F5BFF', primary_name='Electric blue', ink='#0B1026', accent='#8FA6FF', surface='#F3F5FF'),
  'registration-space': dict(slug='registration-space', name='registration.space', legal='registration.space (a JMA Event Services Ltd product)',
                     bold='registration', regular='space',
                     mark=r_mark(), min_lockup=('160 px', '40 mm'), primary='#6D4AFF', primary_name='Violet', ink='#1A1238', accent='#B7A6FF', surface='#F5F3FF'),
}

TILE_R = 0.22

def rrect(x, y, w, h, r):
    if r == 0: return f"M{x} {y} H{x+w} V{y+h} H{x} Z"
    return (f"M{x+r} {y} H{x+w-r} A{r} {r} 0 0 1 {x+w} {y+r} V{y+h-r} A{r} {r} 0 0 1 {x+w-r} {y+h} "
            f"H{x+r} A{r} {r} 0 0 1 {x} {y+h-r} V{y+r} A{r} {r} 0 0 1 {x+r} {y} Z")

def svg_doc(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')

def lum(h):
    h = h.lstrip('#'); f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = [f(int(h[i:i+2], 16) / 255) for i in (0, 2, 4)]; return 0.2126 * r + 0.7152 * g + 0.0722 * b
def cr(a, b): la, lb = sorted([lum(a), lum(b)], reverse=True); return (la + 0.05) / (lb + 0.05)
def mix(a, b, t):
    A = [int(a[i:i+2], 16) for i in (1, 3, 5)]; B = [int(b[i:i+2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(A[i] + (B[i]-A[i])*t):02X}' for i in range(3))

# ---------------- fonts ----------------
FONTS = {}
for wgt in (400, 700):
    tt = TTFont(f'{FONT_SRC}/onest-latin-{wgt}-normal.woff2'); tt.flavor = None
    buf = io.BytesIO(); tt.save(buf); data = buf.getvalue()
    face = hb.Face(data)
    FONTS[wgt] = dict(tt=TTFont(io.BytesIO(data)), hb=hb.Font(face), upem=face.upem)
UPEM = FONTS[700]['upem']; CAP = FONTS[700]['tt']['OS/2'].sCapHeight
TRACK = -0.035

def run_paths(text, wgt, size, x, y, fill):
    f = FONTS[wgt]; buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(f['hb'], buf, {"kern": True, "liga": True})
    gs = f['tt'].getGlyphSet(); order = f['tt'].getGlyphOrder(); sc = size / f['upem']; px = x; out = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        sp = SVGPathPen(gs)
        gs[order[info.codepoint]].draw(TransformPen(sp, (sc, 0, 0, -sc, px + pos.x_offset*sc, y - pos.y_offset*sc)))
        if sp.getCommands(): out.append(sp.getCommands())
        px += pos.x_advance * sc + TRACK * size
    return f'<path fill="{fill}" d="{" ".join(out)}"/>', px

def build(key):
    B = BRANDS[key]; M = B['mark']
    OUT = os.path.join(ROOT, 'brands', B['slug'])
    if os.path.exists(OUT): shutil.rmtree(OUT)
    for d in ['icon', 'logo', 'png/icon', 'png/logo', 'favicon', 'tokens', 'fonts']: os.makedirs(f'{OUT}/{d}')
    P, INK, ACC, SURF = B['primary'], B['ink'], B['accent'], B['surface']
    files = {}
    def write(rel, s):
        open(f'{OUT}/{rel}', 'w').write(s); files[rel] = s

    def mark_d(size_h, cx, cy, small=False):
        s = size_h / M['height']; w = M['width'](small) * s
        return M['paths'](cx - w/2, cy - size_h/2, s, small)
    def tile(x, y, size, tile_c, fill, small=False, radius=True):
        return (f'<path fill="{tile_c}" d="{rrect(x, y, size, size, size*TILE_R if radius else 0)}"/>'
                f'<path fill="{fill}" d="{mark_d(size*M["share"], x+size/2, y+size/2, small)}"/>')
    def cutout(x, y, size, colour, small=False):
        return (f'<path fill="{colour}" fill-rule="evenodd" d="{rrect(x, y, size, size, size*TILE_R)} '
                f'{mark_d(size*M["share"], x+size/2, y+size/2, small)}"/>')

    def wordmark(x, baseline, size, ink, dot):
        a, x1 = run_paths(B['bold'], 700, size, x, baseline, ink)
        b, x2 = run_paths('.', 700, size, x1, baseline, dot)
        c, x3 = run_paths(B['regular'], 400, size, x2, baseline, ink)
        return a + b + c, x3 - TRACK*size - x
    ymax, ymin = -1e9, 1e9
    for wgt, txt in ((700, B['bold'] + '.'), (400, B['regular'])):
        f = FONTS[wgt]; gs = f['tt'].getGlyphSet(); cmap = f['tt'].getBestCmap()
        for ch in txt:
            bp = BoundsPen(gs); gs[cmap[ord(ch)]].draw(bp)
            if bp.bounds: ymin = min(ymin, bp.bounds[1]); ymax = max(ymax, bp.bounds[3])
    TS = 100; ASC, DESC = ymax*TS/UPEM, ymin*TS/UPEM; ICON = 1.19*TS; GAP = 0.31*TS

    def horizontal(ink, dot, icf):
        mid = CAP*TS/UPEM/2; top = min(-ASC, -mid-ICON/2); bottom = max(-DESC, -mid+ICON/2)
        base = -top; wm, ww = wordmark(ICON+GAP, base, TS, ink, dot)
        return svg_doc(ICON+GAP+ww, bottom-top, icf(0, base-mid-ICON/2, ICON) + wm, B['name']), ICON+GAP+ww, bottom-top
    def stacked(ink, dot, icf):
        _, ww = wordmark(0, 0, TS, ink, dot); isz = ICON*1.5; w = max(ww, isz); base = isz + 0.35*TS + ASC
        wm, _ = wordmark((w-ww)/2, base, TS, ink, dot)
        return svg_doc(w, base-DESC, icf((w-isz)/2, 0, isz) + wm, B['name']), w, base-DESC
    def wmonly(ink, dot):
        _, ww = wordmark(0, 0, TS, ink, dot); wm, _ = wordmark(0, ASC, TS, ink, dot)
        return svg_doc(ww, ASC-DESC, wm, B['name']), ww, ASC-DESC

    variants = {'colour': (INK, P, lambda x, y, s: tile(x, y, s, P, WHITE)),
                'reversed': (WHITE, ACC, lambda x, y, s: tile(x, y, s, P, WHITE)),
                'mono-black': (BLACK, BLACK, lambda x, y, s: cutout(x, y, s, BLACK)),
                'mono-white': (WHITE, WHITE, lambda x, y, s: cutout(x, y, s, WHITE))}
    sizes = {}
    for v, (ink, dot, icf) in variants.items():
        for kind, fn in (('horizontal', horizontal), ('stacked', stacked)):
            s, w, h = fn(ink, dot, icf); write(f'logo/{B["slug"]}-{kind}-{v}.svg', s); sizes[(kind, v)] = (w, h)
        s, w, h = wmonly(ink, dot); write(f'logo/{B["slug"]}-wordmark-{v}.svg', s)

    S = 600; pre = B['slug']
    write(f'icon/{pre}-icon.svg', svg_doc(S, S, tile(0, 0, S, P, WHITE), f'{B["name"]} icon'))
    write(f'icon/{pre}-icon-small.svg', svg_doc(S, S, tile(0, 0, S, P, WHITE, small=True), f'{B["name"]} icon (small sizes)'))
    write(f'icon/{pre}-icon-ink.svg', svg_doc(S, S, tile(0, 0, S, INK, WHITE), f'{B["name"]} icon'))
    write(f'icon/{pre}-icon-mono-black.svg', svg_doc(S, S, cutout(0, 0, S, BLACK), f'{B["name"]} icon'))
    write(f'icon/{pre}-icon-mono-white.svg', svg_doc(S, S, cutout(0, 0, S, WHITE), f'{B["name"]} icon'))
    mw = M['width'](False) / M['height'] * 600
    for suf, col in (('', P), ('-ink', INK), ('-black', BLACK), ('-white', WHITE)):
        write(f'icon/{pre}-mark{suf}.svg', svg_doc(mw, 600, f'<path fill="{col}" d="{mark_d(600, mw/2, 300)}"/>', f'{B["name"]} mark'))

    def render(s, path, w, h=None): cairosvg.svg2png(bytestring=s.encode(), write_to=path, output_width=w, output_height=h)
    for px in (16, 32, 48, 64, 128, 256, 512, 1024):
        render(files[f'icon/{pre}-icon-small.svg' if px <= 32 else f'icon/{pre}-icon.svg'], f'{OUT}/png/icon/{pre}-icon-{px}.png', px, px)
    for v in variants:
        for kind in ('horizontal', 'stacked'):
            w, h = sizes[(kind, v)]
            for t in (600, 1200):
                render(files[f'logo/{pre}-{kind}-{v}.svg'], f'{OUT}/png/logo/{pre}-{kind}-{v}-{t}w.png', t, round(t*h/w))

    render(files[f'icon/{pre}-icon-small.svg'], '/tmp/f16.png', 16, 16)
    render(files[f'icon/{pre}-icon-small.svg'], '/tmp/f32.png', 32, 32)
    render(files[f'icon/{pre}-icon.svg'], '/tmp/f48.png', 48, 48)
    Image.open('/tmp/f48.png').save(f'{OUT}/favicon/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)],
                                    append_images=[Image.open('/tmp/f16.png'), Image.open('/tmp/f32.png')])
    shutil.copy(f'{OUT}/icon/{pre}-icon-small.svg', f'{OUT}/favicon/favicon.svg')
    render(svg_doc(S, S, tile(0, 0, S, P, WHITE, radius=False), 'icon'), f'{OUT}/favicon/apple-touch-icon.png', 180, 180)
    render(files[f'icon/{pre}-icon.svg'], f'{OUT}/favicon/android-chrome-192.png', 192, 192)
    render(files[f'icon/{pre}-icon.svg'], f'{OUT}/favicon/android-chrome-512.png', 512, 512)
    render(svg_doc(S, S, f'<rect width="{S}" height="{S}" fill="{P}"/><path fill="{WHITE}" d="{mark_d(S*M["maskable_share"], S/2, S/2)}"/>', 'icon'),
           f'{OUT}/favicon/maskable-512.png', 512, 512)
    write('favicon/site.webmanifest', json.dumps({"name": B['name'], "short_name": B['name'], "icons": [
        {"src": "/android-chrome-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/android-chrome-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
        "theme_color": P, "background_color": WHITE, "display": "standalone"}, indent=2) + '\n')
    write('favicon/head-snippet.html',
          f'<!-- {B["name"]} favicons — place the favicon/ files at the site root (public/) -->\n'
          '<link rel="icon" href="/favicon.ico" sizes="48x48">\n<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
          '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n<link rel="manifest" href="/site.webmanifest">\n'
          f'<meta name="theme-color" content="{P}">\n')

    for w in (400, 500, 600, 700):
        shutil.copy(f'{FONT_SRC}/onest-latin-{w}-normal.woff2', f'{OUT}/fonts/')
    shutil.copy(f'{FONT_SRC}/OFL.txt', f'{OUT}/fonts/OFL.txt')

    # ---- tokens ----
    scale = {'50': mix(P, WHITE, .94), '100': mix(P, WHITE, .87), '200': mix(P, WHITE, .74), '300': mix(P, WHITE, .55),
             '400': mix(P, WHITE, .30), '500': P, '600': mix(P, INK, .18), '700': mix(P, INK, .36), '800': mix(P, INK, .55),
             '900': mix(P, INK, .75), '950': mix(P, INK, .88)}
    neutral = {'50': '#F7F8FB', '100': '#EEF0F5', '200': '#DDE1EA', '300': '#C3C9D6', '400': '#8F98AB', '500': '#626C82',
               '600': '#475066', '700': '#333B50', '800': '#1F263A', '900': '#141A2E', '950': INK}
    tokens = {"$description": f"{B['name']} brand tokens — single source of truth.",
              "color": {"brand": {"value": P, "description": f"{B['primary_name']} — icon tile, full stop, primary actions"},
                        "ink": {"value": INK}, "accent": {"value": ACC, "description": "Full stop and highlights on ink"},
                        "surface": {"value": SURF}, "white": {"value": WHITE},
                        "brand-scale": {k: {"value": v} for k, v in scale.items()},
                        "neutral": {k: {"value": v} for k, v in neutral.items()}},
              "font": {"family": {"sans": {"value": "Onest, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif"}},
                       "weight": {"regular": {"value": 400}, "medium": {"value": 500}, "semibold": {"value": 600}, "bold": {"value": 700}},
                       "tracking": {"wordmark": {"value": "-0.035em"}, "heading": {"value": "-0.02em"}}},
              "radius": {"sm": {"value": "6px"}, "md": {"value": "10px"}, "lg": {"value": "16px"}, "xl": {"value": "24px"},
                         "icon": {"value": "22%"}},
              "logo": {"mark-height": {"value": "56%"}, "small-cut-max": {"value": "32px"}}}
    json.dump(tokens, open(f'{OUT}/tokens/tokens.json', 'w'), indent=2)
    pfx = '--' + ''.join(w[0] for w in B['slug'].split('-'))  # --je / --rs
    faces = "\n\n".join(f"@font-face {{\n  font-family: 'Onest';\n  font-style: normal;\n  font-weight: {w};\n  font-display: swap;\n"
                        f"  src: url('../fonts/onest-latin-{w}-normal.woff2') format('woff2');\n}}" for w in (400, 500, 600, 700))
    vars_ = [f"  {pfx}-brand: {P};", f"  {pfx}-ink: {INK};", f"  {pfx}-accent: {ACC};", f"  {pfx}-surface: {SURF};"]
    vars_ += [f"  {pfx}-brand-{k}: {v};" for k, v in scale.items()] + [f"  {pfx}-neutral-{k}: {v};" for k, v in neutral.items()]
    vars_ += ["  " + pfx + "-font-sans: Onest, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif;",
              f"  {pfx}-tracking-wordmark: -0.035em;"]
    open(f'{OUT}/tokens/brand.css', 'w').write(f"/* {B['name']} brand — generated from tokens/tokens.json */\n\n{faces}\n\n:root {{\n" + "\n".join(vars_) + "\n}\n")
    tw = ["@theme {", "  --font-sans: Onest, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif;",
          f"  --color-brand: {P};", f"  --color-ink: {INK};", f"  --color-accent: {ACC};", f"  --color-surface: {SURF};"]
    tw += [f"  --color-brand-{k}: {v};" for k, v in scale.items()] + [f"  --color-neutral-{k}: {v};" for k, v in neutral.items()]
    tw += ["  --tracking-wordmark: -0.035em;", "}"]
    open(f'{OUT}/tokens/tailwind.theme.css', 'w').write(f"/* {B['name']} — Tailwind CSS v4 theme. @import after 'tailwindcss'. */\n" + "\n".join(tw) + "\n")
    preset = {"theme": {"extend": {"fontFamily": {"sans": ["Onest", "ui-sans-serif", "system-ui", "sans-serif"]},
              "colors": {"brand": {"DEFAULT": P, **scale}, "ink": INK, "accent": ACC, "surface": SURF, "neutral": neutral},
              "letterSpacing": {"wordmark": "-0.035em"}}}}
    open(f'{OUT}/tokens/tailwind.preset.js', 'w').write("// Tailwind CSS v3 preset\nmodule.exports = " + json.dumps(preset, indent=2) + ";\n")
    open(f'{OUT}/tokens/filament-panel.php', 'w').write(
        f"<?php\n\n// {B['name']} — Filament panel branding. Apply inside your PanelProvider's panel() method.\n\n"
        "use Filament\\Support\\Colors\\Color;\n\nreturn $panel\n"
        f"    ->colors(['primary' => Color::hex('{P}'), 'gray' => Color::Slate])\n    ->font('Onest')\n"
        f"    ->brandLogo(asset('brand/logo/{pre}-horizontal-colour.svg'))\n"
        f"    ->darkModeBrandLogo(asset('brand/logo/{pre}-horizontal-reversed.svg'))\n"
        "    ->brandLogoHeight('2rem')\n    ->favicon(asset('favicon.svg'));\n")

    pairs = [(f"White on {B['primary_name']}", WHITE, P), (f"{B['primary_name']} on White", P, WHITE),
             (f"{B['primary_name']} on Surface", P, SURF), ("Ink on White", INK, WHITE), ("Ink on Surface", INK, SURF),
             ("White on Ink", WHITE, INK), ("Accent on Ink", ACC, INK), (f"{B['primary_name']} on Ink", P, INK)]
    def verdict(c): return "AAA" if c >= 7 else "AA for all text" if c >= 4.5 else "Large text and graphics only" if c >= 3 else "Decorative only"
    rows = "\n".join(f"| {n} | {cr(a, b):.2f}:1 | {verdict(cr(a, b))} |" for n, a, b in pairs)
    md = f"""# {B['name']} — Brand guidelines

**Version 1.0 · November 2026**
Brand name: **{B['name']}** · {B['legal']}

Logos, icons, favicons, fonts and design tokens for {B['name']}. It is the sister brand of jma.events: same type, same construction system, its own colour.

## 1. The logo

- **The {M['name']} icon:** a geometric {M['name']} made of two pieces with a narrow parallel split, white on a rounded {B['primary_name'].lower()} tile.
- **The wordmark:** `{B['name']}` in Onest. **{B['bold']}** is Bold (700), the **full stop** is {B['primary_name'].lower()}, and **{B['regular']}** is Regular (400), all tracked at −0.035em.

| File | Use it for |
|---|---|
| `logo/{pre}-horizontal-colour.svg` | **Default.** Light backgrounds |
| `logo/{pre}-horizontal-reversed.svg` | Dark backgrounds |
| `logo/{pre}-stacked-*.svg` | Square or tall spaces |
| `logo/{pre}-wordmark-*.svg` | When the icon is already shown nearby |
| `icon/{pre}-icon.svg` | App icons, avatars and favicons |
| `icon/{pre}-mark*.svg` | The {M['name']} without its tile |
| `*-mono-black` / `*-mono-white` | One-colour print, embroidery and etching |

Lettering is converted to outlines, so the files don't need Onest installed.

**Clear space:** keep a gap of ¼ of the icon tile's height on every side.
**Minimum sizes:** horizontal lockup {B['min_lockup'][0]} / {B['min_lockup'][1]} wide · stacked lockup 100 px / 25 mm · icon 16 px / 6 mm.
**At 32 px and below,** use `icon/{pre}-icon-small.svg`. Its wider split stays visible.

### Icon construction
{M['construction']}
- **In the tile,** the mark is {round(M["share"]*100)}% of the tile height and mathematically centred. The tile's corner radius is 22% of its size.

### Don't
- Change the colours, or put a coloured mark on a coloured tile.
- Close or remove the split.
- Re-type the wordmark, add capitals, or drop the full stop.
- Stretch, rotate, outline, or add shadows or gradients.

## 2. Colour

| Name | Hex | Role |
|---|---|---|
| **{B['primary_name']}** | `{P}` | Icon tile, full stop, primary actions |
| **Ink** | `{INK}` | Text, dark backgrounds |
| **Accent** | `{ACC}` | Full stop and highlights on ink |
| **Surface** | `{SURF}` | Light tinted backgrounds |
| **White** | `#FFFFFF` | Backgrounds, text on colour |

| Pairing | Ratio | Passes |
|---|---|---|
{rows}

## 3. Typography

**Onest** throughout (SIL Open Font License, see `fonts/OFL.txt`).

| Use | Weight |
|---|---|
| Display / H1 | Bold 700, −0.02em |
| H2–H4 | Semibold 600 |
| UI labels | Medium 500 |
| Body | Regular 400 |

## 4. Files

- `tokens/tokens.json`: the source of truth.
- `tokens/brand.css`: `@font-face` rules and `{pfx}-*` variables.
- `tokens/tailwind.theme.css`: the Tailwind v4 theme.
- `tokens/tailwind.preset.js`: the Tailwind v3 preset.
- `tokens/filament-panel.php`: Filament panel branding.
- `favicon/`: the favicon files and a `head-snippet.html` to paste into your layout.
- `png/`: PNG exports. Use the logo PNGs in emails.

## 5. Using it in a Laravel app

Install the `joelinit1/brand` package as a development dependency, then run `php artisan brand:sync {B['slug']}`. The command copies everything an app needs into the app itself, so production servers never need access to the brand repo:

- `public/brand/`: logos, icons, PNGs, fonts and tokens.
- `public/`: the favicon files and `site.webmanifest`.
- `resources/css/brand.css`: the Onest `@font-face` rules, the `{pfx}-*` variables and, for Tailwind v4, the `@theme` block.
- `resources/views/components/brand/`: the `<x-brand.logo />`, `<x-brand.icon />` and `<x-brand.favicons />` Blade components.

To pick up a new brand release, run `composer update joelinit1/brand`, re-run `brand:sync` and commit the changes.
"""
    open(f'{OUT}/BRAND.md', 'w').write(md)
    json.dump({"slug": B['slug'], "name": B['name'], "primary": P, "ink": INK, "accent": ACC, "surface": SURF},
              open(f'{OUT}/brand.json', 'w'), indent=2)
    print(B['name'], 'built ->', OUT)
    return OUT, files, sizes

if __name__ == '__main__':
    for key in (sys.argv[1:] or list(BRANDS)):
        build(key)
