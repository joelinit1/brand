<?php

namespace JoelInit1\Brand;

use Illuminate\Support\ServiceProvider;
use JoelInit1\Brand\Console\SyncCommand;

class BrandServiceProvider extends ServiceProvider
{
    /**
     * Register the brand:sync command when running in the console.
     */
    public function boot(): void
    {
        if ($this->app->runningInConsole()) {
            $this->commands([SyncCommand::class]);
        }
    }
}
