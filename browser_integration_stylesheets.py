from .browser_integration import *


get_css_hrefs_js = """
    var styleSheets = document.styleSheets;
    var results = [];

    for (var i=0; i < styleSheets.length; i++) {
        results.push(styleSheets[i].href);
    }

    return results;
"""


class BrowserIntegrationStylesheetsCommand(sublime_plugin.ApplicationCommand):
    plugin_name = "View loaded CSS (stylesheets)"
    plugin_description = "Lists all loaded stylesheets."

    @require_browser
    @async
    def run(self):
        @async
        def load_css(i):
            from urllib.request import urlopen

            if i >= 0:
                response = urlopen(results[i])
                text = response.read().decode('utf8')
                view = sublime.active_window().new_file()
                view.set_name(results[i])
                view.set_syntax_file('Packages/CSS/CSS.tmLanguage')
                view.run_command("insert_into_view", {"text": text})

        results = browser.execute_script(get_css_hrefs_js)

        if results:
            sublime.active_window().show_quick_panel(results, load_css)
        else:
            status("There are no CSS style sheets loaded.")
