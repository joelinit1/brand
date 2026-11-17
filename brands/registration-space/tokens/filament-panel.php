<?php

// registration.space — Filament panel branding. Apply inside your PanelProvider's panel() method.

use Filament\Support\Colors\Color;

return $panel
    ->colors(['primary' => Color::hex('#6D4AFF'), 'gray' => Color::Slate])
    ->font('Onest')
    ->brandLogo(asset('brand/logo/registration-space-horizontal-colour.svg'))
    ->darkModeBrandLogo(asset('brand/logo/registration-space-horizontal-reversed.svg'))
    ->brandLogoHeight('2rem')
    ->favicon(asset('brand/favicon/favicon.svg'));
