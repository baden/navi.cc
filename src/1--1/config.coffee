
exports.config =
    coffeelint:
        pattern: /^app\/.*\.coffee$/
        options:
            indentation:
                value: 4
            no_trailing_semicolons:
                level: "ignore"
            max_line_length:
                value: 200
                level: 'ignore'
            # Можно разрешить использовать табуляции вместо пробелов:
            #no_tabs:
            #    level: 'ignore'
            #indentation:
            #    value: 1

    # See docs at http://brunch.readthedocs.org/en/latest/config.html.
    modules:
        definition: false
        wrapper: false
    paths:
        public: '_public'
    files:
        javascripts:
            joinTo:
                'js/app.js': /^app/
                'js/vendor.js': /^vendor/
                'test/scenarios.js': /^test(\/|\\)e2e/
            order:
                before: [
                    'app/base.coffee'
                    'vendor/scripts/console-helper.js'
                    'vendor/scripts/jquery-1.7.2.js'
                    'vendor/scripts/jquery-ui.min.js'
                    'vendor/scripts/jquery.ui.datepicker-ru.js'
                    'vendor/scripts/select2.js'
                    'vendor/scripts/angular/angular.js'
                    'vendor/scripts/angular/angular-resource.js'
                    'vendor/scripts/angular/angular-cookies.js'
                    'vendor/scripts/angular/angular-ui.js'
                ]
                after: [
                ]

        stylesheets:
            joinTo:
                'css/app.css': /^(app|vendor)/
        templates:
            joinTo: 'js/templates.js'

    plugins:
        jade:
            pretty: yes # Adds pretty-indentation whitespaces to output (false by default)

    # Enable or disable minifying of result js / css files.
    # minify: true
#console.log 'hello', this
