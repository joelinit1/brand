@props([
    'environment' => true,
])
{{-- __NAME__ aurora background for Filament auth pages (login, password reset, email verification).
     Register it in your PanelProvider with PanelsRenderHook::SIMPLE_LAYOUT_START (see the brand README).
     environment: show a badge with the app environment on every environment except production. --}}
@php
    $env = app()->environment();
    $showEnvironment = $environment && $env !== 'production';
@endphp
<style>
    .fi-simple-layout { position: relative; isolation: isolate; }
    .brand-aurora { position: fixed; inset: 0; z-index: -1; overflow: hidden; pointer-events: none; background: __INK__; }
    .brand-aurora__glow { position: absolute; border-radius: 50%; will-change: transform; }
    .brand-aurora__glow--a { left: -25%; top: -35%; width: 85vmax; height: 85vmax; background: radial-gradient(closest-side, __PRIMARY__B3, __PRIMARY__00); animation: brand-aurora-a 22s ease-in-out infinite; }
    .brand-aurora__glow--b { right: -30%; bottom: -40%; width: 90vmax; height: 90vmax; background: radial-gradient(closest-side, __ACCENT__80, __ACCENT__00); animation: brand-aurora-b 28s ease-in-out infinite; }
    .brand-aurora__mark { position: absolute; right: 5vh; top: 50%; height: 90vh; width: auto; transform: translateY(-50%); opacity: .045; }
    .brand-aurora-env { position: fixed; left: 50%; bottom: 1.25rem; transform: translateX(-50%); display: flex; align-items: center; gap: .5rem; font-size: .8125rem; color: #C9CEDD; white-space: nowrap; }
    .brand-aurora-env__badge { padding: .1875rem .5rem; border-radius: 999px; font-size: .75rem; font-weight: 600; letter-spacing: .04em; text-transform: uppercase; background: #E3E6EE; color: #2B3142; }
    .brand-aurora-env__badge--staging { background: #FDE8C8; color: #7A4300; }
    @keyframes brand-aurora-a { 0%, 100% { transform: translate(0, 0) scale(1); } 50% { transform: translate(18vw, 10vh) scale(1.2); } }
    @keyframes brand-aurora-b { 0%, 100% { transform: translate(0, 0) scale(1.1); } 50% { transform: translate(-14vw, -12vh) scale(.85); } }
    @media (prefers-reduced-motion: reduce) { .brand-aurora__glow { animation: none; } }
</style>
<div class="brand-aurora" aria-hidden="true">
    <div class="brand-aurora__glow brand-aurora__glow--a"></div>
    <div class="brand-aurora__glow brand-aurora__glow--b"></div>
    <img class="brand-aurora__mark" src="{{ asset('brand/icon/__SLUG__-mark-white.svg') }}" alt="">
</div>
@if ($showEnvironment)
    <div class="brand-aurora-env">
        <span @class(['brand-aurora-env__badge', 'brand-aurora-env__badge--staging' => $env === 'staging'])>{{ $env }}</span>
        <span>{{ config('app.name') }}</span>
    </div>
@endif
