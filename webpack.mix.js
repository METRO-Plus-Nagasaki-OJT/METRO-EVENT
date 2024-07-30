let mix = require('laravel-mix');
const path = require('path');
require('mix-tailwindcss');

mix.setPublicPath('public')


mix.js("resources/js/app.js", "js")
    .js("resources/js/mediapipe.js", "js")
    .js("resources/js/download.js", "js")
    .js("resources/js/plugin.js", "js")

mix.postCss('resources/css/app.css', 'css').tailwind(
    path.resolve(__dirname, 'tailwind.config.js')
);

mix.version()
mix.webpackConfig({
    target: ['web', 'es5'],
    resolve: {
        modules: ['node_modules']
    }
})