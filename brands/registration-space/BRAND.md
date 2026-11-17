# registration.space — Brand guidelines

**Version 1.0 · November 2026**
Brand name: **registration.space** · registration.space (a JMA Event Services Ltd product)

Logos, icons, favicons, fonts and design tokens for registration.space. It is the sister brand of jma.events: same type, same construction system, its own colour.

## 1. The logo

- **The r icon:** a geometric r made of two pieces with a narrow parallel split, white on a rounded violet tile.
- **The wordmark:** `registration.space` in Onest. **registration** is Bold (700), the **full stop** is violet, and **space** is Regular (400), all tracked at −0.035em.

| File | Use it for |
|---|---|
| `logo/registration-space-horizontal-colour.svg` | **Default.** Light backgrounds |
| `logo/registration-space-horizontal-reversed.svg` | Dark backgrounds |
| `logo/registration-space-stacked-*.svg` | Square or tall spaces |
| `logo/registration-space-wordmark-*.svg` | When the icon is already shown nearby |
| `icon/registration-space-icon.svg` | App icons, avatars and favicons |
| `icon/registration-space-mark*.svg` | The r without its tile |
| `*-mono-black` / `*-mono-white` | One-colour print, embroidery and etching |

Lettering is converted to outlines, so the files don't need Onest installed.

**Clear space:** keep a gap of ¼ of the icon tile's height on every side.
**Minimum sizes:** horizontal lockup 160 px / 40 mm wide · stacked lockup 100 px / 25 mm · icon 16 px / 6 mm.
**At 32 px and below,** use `icon/registration-space-icon-small.svg`. Its wider split stays visible.

### Icon construction
- **Grid unit u** is the stem width. The stem is 1u × 2.5u with a quarter-circle top-left (radius u); the shoulder is 1.125u × 1u.
- **Two radii only:** u for the stem, ¾u for the shoulder's top-left and bottom-right curves.
- **The split** is 4% of the r's height (10% in the small cut).
- Built on the same system as the jma.events J, so the two marks read as a family.
- **In the tile,** the mark is 56% of the tile height and mathematically centred. The tile's corner radius is 22% of its size.

### Don't
- Change the colours, or put a coloured mark on a coloured tile.
- Close or remove the split.
- Re-type the wordmark, add capitals, or drop the full stop.
- Stretch, rotate, outline, or add shadows or gradients.

## 2. Colour

| Name | Hex | Role |
|---|---|---|
| **Violet** | `#6D4AFF` | Icon tile, full stop, primary actions |
| **Ink** | `#1A1238` | Text, dark backgrounds |
| **Accent** | `#B7A6FF` | Full stop and highlights on ink |
| **Surface** | `#F5F3FF` | Light tinted backgrounds |
| **White** | `#FFFFFF` | Backgrounds, text on colour |

| Pairing | Ratio | Passes |
|---|---|---|
| White on Violet | 5.15:1 | AA for all text |
| Violet on White | 5.15:1 | AA for all text |
| Violet on Surface | 4.70:1 | AA for all text |
| Ink on White | 17.68:1 | AAA |
| Ink on Surface | 16.12:1 | AAA |
| White on Ink | 17.68:1 | AAA |
| Accent on Ink | 8.35:1 | AAA |
| Violet on Ink | 3.43:1 | Large text and graphics only |

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
- `tokens/brand.css`: `@font-face` rules and `--rs-*` variables.
- `tokens/tailwind.theme.css`: the Tailwind v4 theme.
- `tokens/tailwind.preset.js`: the Tailwind v3 preset.
- `tokens/filament-panel.php`: Filament panel branding.
- `favicon/`: the favicon files and a `head-snippet.html` to paste into your layout.
- `png/`: PNG exports. Use the logo PNGs in emails.

## 5. Using it in a Laravel app

Install the `joelinit1/brand` package as a development dependency, then run `php artisan brand:sync registration-space`. The command copies everything an app needs into the app itself, so production servers never need access to the brand repo:

- `public/brand/`: logos, icons, PNGs, fonts and tokens.
- `public/`: the favicon files and `site.webmanifest`.
- `resources/css/brand.css`: the Onest `@font-face` rules, the `--rs-*` variables and, for Tailwind v4, the `@theme` block.
- `resources/views/components/brand/`: the `<x-brand.logo />`, `<x-brand.icon />` and `<x-brand.favicons />` Blade components.

To pick up a new brand release, run `composer update joelinit1/brand`, re-run `brand:sync` and commit the changes.
