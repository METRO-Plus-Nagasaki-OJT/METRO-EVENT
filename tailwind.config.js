const { colors } = require('laravel-mix/src/Log');

module.exports = {
    content: ['./resources/views/**/*.{js,html}',   "./node_modules/flowbite/**/*.js"],
    theme: {
        extend: {
            fontSize: {
                sm: '0.8rem',
                base: '1rem',
                xl: '1.25rem',
                '2xl': '1.563rem',
                '3xl': '1.953rem',
                '4xl': '2.441rem',
                '5xl': '3.052rem',
            },
            colors: {
                "background" : "#edede9" 
            }
        },
        container: {
            center: true,
        },
        screens: {
            sm: '640px',
            md: '768px',
            lg: '1024px',
            xl: '1280px',
        },
    },
    plugins: [require('flowbite/plugin')],
};