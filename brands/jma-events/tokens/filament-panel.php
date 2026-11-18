<?php

// jma.events — Filament panel branding. Apply inside your PanelProvider's panel() method.

use Filament\Support\Colors\Color;

return $panel
    ->colors(['primary' => Color::hex('#2F5BFF'), 'gray' => Color::Slate])
    ->font('Onest')
    ->brandLogo(asset('brand/logo/jma-events-horizontal-colour.svg'))
    ->darkModeBrandLogo(asset('brand/logo/jma-events-horizontal-reversed.svg'))
    ->brandLogoHeight('2rem')
    ->favicon(asset('favicon.svg'));
