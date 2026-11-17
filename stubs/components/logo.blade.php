@props([
    'layout' => 'horizontal',
    'tone' => 'colour',
    'height' => '2rem',
])
{{-- __NAME__ logo. layout: horizontal | stacked | wordmark · tone: colour | reversed | mono-black | mono-white --}}
<img
    src="{{ asset('brand/logo/__SLUG__-'.$layout.'-'.$tone.'.svg') }}"
    alt="__NAME__"
    {{ $attributes->merge(['style' => 'height: '.$height.'; width: auto;']) }}
>
