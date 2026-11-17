@props([
    'manifest' => true,
])
{{-- __NAME__ favicons. Place inside <head>. Pass :manifest="false" on pages that link their own web app manifest. --}}
<link rel="icon" href="{{ asset('favicon.ico') }}" sizes="48x48">
<link rel="icon" href="{{ asset('favicon.svg') }}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{{ asset('apple-touch-icon.png') }}">
@if ($manifest)
<link rel="manifest" href="{{ asset('site.webmanifest') }}">
@endif
<meta name="theme-color" content="__PRIMARY__">
