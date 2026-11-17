# joelinit1/brand

The single source of truth for the **jma.events** and **registration.space** brands: logos, icons, favicons, Onest fonts, design tokens and Blade components, synced into Laravel apps with one Artisan command.

| Brand | Mark | Primary | Guide |
|---|---|---|---|
| `jma-events` | J | Electric blue `#2F5BFF` | [brands/jma-events/BRAND.md](brands/jma-events/BRAND.md) |
| `registration-space` | r | Violet `#6D4AFF` | [brands/registration-space/BRAND.md](brands/registration-space/BRAND.md) |

## Adding a brand to an app

The package is a **development dependency**. `brand:sync` copies everything into the app and those files are committed, so production servers never need access to this private repo.

**1. Point Composer at this repo** (once per app), in `composer.json`:

```json
"repositories": [
    { "type": "vcs", "url": "https://github.com/joelinit1/brand" }
]
```

**2. Install it and sync a brand:**

```bash
composer require --dev joelinit1/brand
php artisan brand:sync registration-space   # or jma-events
```

**3. Wire it up** (once per app):

- Put `<x-brand.favicons />` inside your layout's `<head>`.
- Import the CSS: `@import './brand.css';` in `resources/css/app.css`. On Tailwind v4, this also gives you `bg-brand`, `text-ink`, `bg-brand-50…950` and `font-sans` set to Onest. On Tailwind v3, add `require('./tailwind.brand.preset.js')` to `presets` in `tailwind.config.js`.
- Use `<x-brand.logo />` and `<x-brand.icon />` in your views.
- For Filament panels, set the colour, font, logos and favicon in the PanelProvider. See `brands/<brand>/tokens/filament-panel.php`.

## What `brand:sync` writes

| Path | Contents |
|---|---|
| `public/brand/` | Logos, icons, PNGs, fonts, tokens, `BRAND.md`, and `brand.json` (which brand and package version) |
| `public/favicon.ico`, `favicon.svg`, `apple-touch-icon.png`, `android-chrome-*.png`, `maskable-512.png`, `site.webmanifest` | Favicons. Existing `favicon-16x16.png`, `favicon-32x32.png`, `android-chrome-192x192.png` and `android-chrome-512x512.png` are refreshed too. It asks before overwriting changed files; `--force` skips the questions |
| `resources/css/brand.css` | Onest `@font-face` rules, CSS variables, and the Tailwind v4 `@theme` when the app uses v4 |
| `tailwind.brand.preset.js` | Only for Tailwind v3 apps |
| `resources/views/components/brand/` | `logo`, `icon` and `favicons` Blade components |

Don't edit the synced files by hand: change this repo and re-sync.

### Blade components

```blade
<x-brand.logo />                                   {{-- horizontal, colour, 2rem tall --}}
<x-brand.logo layout="stacked" tone="reversed" height="6rem" />
<x-brand.logo layout="wordmark" tone="mono-black" />
<x-brand.icon size="48" />                         {{-- 32 and below automatically use the small-size cut --}}
<x-brand.favicons />
```

## Updating a brand

1. Edit `generator/brandkit.py` (colours, marks, wordmark) and regenerate:
   ```bash
   pip install fonttools uharfbuzz brotli cairosvg pillow
   python3 generator/brandkit.py            # all brands, or name one
   ```
2. Commit, then tag a release: `git tag v1.1.0 && git push --tags`.
3. In each app: `composer update joelinit1/brand && php artisan brand:sync <brand> --force`, then commit.

## Adding a new brand

Add an entry to `BRANDS` in `generator/brandkit.py` with its own mark function, wordmark and palette, then regenerate. It becomes available to `brand:sync` straight away.
