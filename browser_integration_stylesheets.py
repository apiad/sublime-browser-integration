from .browser_integration import *


get_css_hrefs_js = """
    var styleSheets = document.styleSheets;
    var results = [];
    var embedded = 1;

    for (var i=0; i < styleSheets.length; i++) {
        var sheet = styleSheets[i];

        if (sheet.href) {
            results.push([styleSheets[i].href, '']);
        }
    }

    var embeddedStyles = document.querySelectorAll('style')

    for (var i=0; i < embeddedStyles.length; i++) {
        var sheet = embeddedStyles[i];

        results.push(['Embedded Style #' + (i+1),
                      sheet.innerHTML.substr(0, 50) + '...'])
    }

    return results;
"""


get_embedded_css_text = """
    var sheet = document.querySelectorAll('style')[%i];
    sheet.setAttribute('data-bi-css', %i);
    return sheet.innerHTML;
"""


class BrowserIntegrationStylesheetsCommand(sublime_plugin.WindowCommand):
    plugin_name = "Loaded StyleSheets"
    plugin_description = "Lists all loaded stylesheets."

    @require_browser
    @async
    def run(self):
        def load_css(i):
            if i >= 0:
                if (results[i][0].startswith('Embedded')):
                    text = browser.execute(get_embedded_css_text % (i, i))
                    name = 'embedded-stylesheet-%i.css' % i
                else:
                    from urllib.request import urlopen

                    response = urlopen(results[i][0])
                    text = response.read().decode('utf8')
                    name = results[i][0]

                view = sublime.active_window().new_file()
                view.set_name(name)
                view.set_syntax_file('Packages/CSS/CSS.tmLanguage')
                view.run_command("insert_into_view", {"text": text})

        results = browser.execute_script(get_css_hrefs_js)

        if results:
            sublime.active_window().show_quick_panel(results, load_css)
        else:
            warning("There are no CSS style sheets loaded.")
