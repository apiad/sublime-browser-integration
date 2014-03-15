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
        else {
            results.push(['Embedded stylesheet #' + (embedded++),
                           sheet.ownerNode.innerHTML.substr(0, 55) + '...'])
        }
    }

    return results;
"""


get_embedded_css_text = """
    return document.styleSheets[%i].ownerNode.innerHTML;
"""


class BrowserIntegrationStylesheetsCommand(sublime_plugin.ApplicationCommand):
    plugin_name = "View loaded CSS (stylesheets)"
    plugin_description = "Lists all loaded stylesheets."

    @require_browser
    @async
    def run(self):
        @async
        def load_css(i):
            if i >= 0:
                if (results[i][0].startswith('Embedded')):
                    text = browser.execute(get_embedded_css_text % i)
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
