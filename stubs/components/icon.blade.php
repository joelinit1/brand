@props([
    'size' => 32,
    'tone' => null,
])
{{-- __NAME__ icon. Uses the small-size cut at 32px and below. tone: null | ink | mono-black | mono-white --}}
@php
    $file = $tone !== null ? '__SLUG__-icon-'.$tone : ((int) $size <= 32 ? '__SLUG__-icon-small' : '__SLUG__-icon');
@endphp
<img
    src="{{ asset('brand/icon/'.$file.'.svg') }}"
    alt="__NAME__"
    width="{{ $size }}"
    height="{{ $size }}"
    {{ $attributes }}
>
