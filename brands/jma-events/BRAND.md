# jma.events — Brand guidelines

**Version 1.0 · November 2026**
Brand name: **jma.events** · JMA Event Services Ltd

Logos, icons, favicons, fonts and design tokens for jma.events. It is the sister brand of jma.events: same type, same construction system, its own colour.

## 1. The logo

- **The J icon:** a geometric J made of two pieces with a narrow parallel split, white on a rounded electric blue tile.
- **The wordmark:** `jma.events` in Onest. **jma** is Bold (700), the **full stop** is electric blue, and **events** is Regular (400), all tracked at −0.035em.

| File | Use it for |
|---|---|
| `logo/jma-events-horizontal-colour.svg` | **Default.** Light backgrounds |
| `logo/jma-events-horizontal-reversed.svg` | Dark backgrounds |
| `logo/jma-events-stacked-*.svg` | Square or tall spaces |
| `logo/jma-events-wordmark-*.svg` | When the icon is already shown nearby |
| `icon/jma-events-icon.svg` | App icons, avatars and favicons |
| `icon/jma-events-mark*.svg` | The J without its tile |
| `*-mono-black` / `*-mono-white` | One-colour print, embroidery and etching |

Lettering is converted to outlines, so the files don't need Onest installed.

**Clear space:** keep a gap of ¼ of the icon tile's height on every side.
**Minimum sizes:** horizontal lockup 120 px / 30 mm wide · stacked lockup 100 px / 25 mm · icon 16 px / 6 mm.
**At 32 px and below,** use `icon/jma-events-icon-small.svg`. Its wider split stays visible.

### Icon construction
- **Grid unit u** is the stem width. The stem is 1u × 2.75u; the foot is 1.25u × 1.25u.
- **One radius only:** every curve is radius u: the stem's top-left and bottom-right, and the foot's top-right and bottom-left.
- **The split** is 4% of the J's height, widened to 13% in the small-size cut so it survives at 16–32 px.
- **In the tile,** the mark is 64% of the tile height and mathematically centred. The tile's corner radius is 22% of its size.

### Don't
- Change the colours, or put a coloured mark on a coloured tile.
- Close or remove the split.
- Re-type the wordmark, add capitals, or drop the full stop.
- Stretch, rotate, outline, or add shadows or gradients.

## 2. Colour

| Name | Hex | Role |
|---|---|---|
| **Electric blue** | `#2F5BFF` | Icon tile, full stop, primary actions |
| **Ink** | `#0B1026` | Text, dark backgrounds |
| **Accent** | `#8FA6FF` | Full stop and highlights on ink |
| **Surface** | `#F3F5FF` | Light tinted backgrounds |
| **White** | `#FFFFFF` | Backgrounds, text on colour |

| Pairing | Ratio | Passes |
|---|---|---|
| White on Electric blue | 5.17:1 | AA for all text |
| Electric blue on White | 5.17:1 | AA for all text |
| Electric blue on Surface | 4.76:1 | AA for all text |
| Ink on White | 18.81:1 | AAA |
| Ink on Surface | 17.30:1 | AAA |
| White on Ink | 18.81:1 | AAA |
| Accent on Ink | 8.12:1 | AAA |
| Electric blue on Ink | 3.64:1 | Large text and graphics only |

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
- `tokens/brand.css`: `@font-face` rules and `--je-*` variables.
- `tokens/tailwind.theme.css`: the Tailwind v4 theme.
- `tokens/tailwind.preset.js`: the Tailwind v3 preset.
- `tokens/filament-panel.php`: Filament panel branding.
- `favicon/`: the favicon files and a `head-snippet.html` to paste into your layout.
- `png/`: PNG exports. Use the logo PNGs in emails.

## 5. Using it in a Laravel app

Install the `joelinit1/brand` package as a development dependency, then run `php artisan brand:sync jma-events`. The command copies everything an app needs into the app itself, so production servers never need access to the brand repo:

- `public/brand/`: logos, icons, PNGs, fonts and tokens.
- `public/`: the favicon files and `site.webmanifest`.
- `resources/css/brand.css`: the Onest `@font-face` rules, the `--je-*` variables and, for Tailwind v4, the `@theme` block.
- `resources/views/components/brand/`: the `<x-brand.logo />`, `<x-brand.icon />` and `<x-brand.favicons />` Blade components.

To pick up a new brand release, run `composer update joelinit1/brand`, re-run `brand:sync` and commit the changes.
