import re

from .browser_integration import *


get_css_hrefs_js = """
    var styleSheets = document.styleSheets;
    var results = [];
    var embedded = 1;

    for (var i=0; i < styleSheets.length; i++) {
        var sheet = styleSheets[i];

        if (sheet.href) {
            var href = sheet.href.split('/');
            results.push([href[href.length-1], sheet.href]);
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
    plugin_name = "StyleSheets (CSS)"
    plugin_description = "Lists all loaded stylesheets."

    @staticmethod
    def visible():
        return browser.connected()

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
                    from urllib.parse import urlparse

                    path = results[i][1]
                    url = urlparse(path)

                    if url.netloc:
                        response = urlopen(results[i][1])
                        text = response.read().decode('utf8')
                        name = results[i][0]
                    else:
                        self.window.open_file(path, sublime.TRANSIENT)
                        return

                view = sublime.active_window().new_file()
                view.set_name(name)
                view.set_syntax_file('Packages/CSS/CSS.tmLanguage')
                view.run_command("insert_into_view", {"text": text})

        results = browser.execute_script(get_css_hrefs_js)
        statics = setting("static_files_mapping")

        if results:
            with loading("Matching CSS files to local static files."):
                for r in results:
                    if not r[0].startswith('Embedded'):
                        r[1] = self.get_local_path(r[1], statics)

            sublime.active_window().show_quick_panel(results, load_css)
        else:
            warning("There are no CSS style sheets loaded.")

    def get_local_path(self, path, statics):
        for mapping in statics:
            selector = mapping['selector']
            matches = mapping['matches']

            match = re.match(selector, path, re.UNICODE)

            if not match:
                continue

            for folder in self.window.folders():
                for dirpath, dirnames, filenames in os.walk(folder,
                                                            followlinks=True):
                    if '.git' in dirnames:
                        dirnames.remove('.git')

                    for filename in filenames:
                        local_path = os.path.join(dirpath, filename)
                        matched_path = local_path[len(folder) + 1:]

                        for pattern in matches:
                            re_pattern = match.expand(pattern)

                            if re.match(re_pattern, matched_path):
                                return local_path

        return path
