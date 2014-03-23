from .browser_integration import *


get_links_js = """
    var links = document.querySelectorAll('a');
    var result = []

    for(var i=0; i < links.length; i++) {
        var link = links[i];

        if (link.href) {
            result.push([link.text, link.href])
        }
    }

    return result;
"""


class BrowserIntegrationNavigateCommand(sublime_plugin.WindowCommand):
    plugin_name = "Navigate To"
    plugin_description = "Opens a input panel to enter a URL to load in Chrome."

    @require_browser
    @async
    def run(self):
        def onDone(str):
            from urllib.parse import urlparse

            url = urlparse(str)

            if not url.netloc:
                url = 'http://' + url.geturl()
            else:
                url = url.geturl()

            with loading("Opening %s" % url):
                browser.get(url)

            status("Loaded %s" % url)

        result = browser.execute(get_links_js) or []

        def onQuickDone(i):
            if i == 0:
                view = self.window.show_input_panel('Enter URL',
                                                    browser.current_url,
                                                    onDone, None, None)

                view.sel().add(sublime.Region(0, view.size()))

            elif i == 1:
                browser.back()
            elif i == 2:
                browser.forward()
            elif i >= 3:
                browser.get(result[i-3][1])

        self.window.show_quick_panel(
            [['Custom URL', 'Enter a custom URL to navigate'],
             ['Back', 'Navigate to previous location'],
             ['Forward', 'Navigate to next location']] + result,
            onQuickDone)
