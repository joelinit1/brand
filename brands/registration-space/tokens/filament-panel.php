<?php

// registration.space — Filament panel branding. Apply inside your PanelProvider's panel() method.

use Filament\Support\Colors\Color;
use Filament\View\PanelsRenderHook;
use Illuminate\Support\Facades\Blade;

return $panel
    ->colors(['primary' => Color::hex('#6D4AFF'), 'gray' => Color::Slate])
    ->font('Onest')
    ->brandLogo(asset('brand/logo/registration-space-horizontal-colour.svg'))
    ->darkModeBrandLogo(asset('brand/logo/registration-space-horizontal-reversed.svg'))
    ->brandLogoHeight('2rem')
    ->favicon(asset('favicon.svg'))
    ->renderHook(PanelsRenderHook::SIMPLE_LAYOUT_START, fn (): string => Blade::render('<x-brand.auth-aurora />'));
