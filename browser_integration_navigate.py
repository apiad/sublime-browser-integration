from .browser_integration import *


class BrowserIntegrationNavigateCommand(sublime_plugin.WindowCommand):
    plugin_name = "Navigate To"
    plugin_description = "Opens a input panel to enter a URL to load in Chrome."

    @require_browser
    def run(self):
        @async
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

        self.window.show_input_panel('Enter URL', browser.current_url,
                                     onDone, None, None)
