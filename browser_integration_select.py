from .browser_integration import *


def highlight(selector):
    global chrome
    global old_selector

    if chrome is None:
        warning("Chrome is not running.")
        return

    if old_selector:
        chrome.execute_script(unselect_js % old_selector)

    chrome.execute_script(select_js % (selector, setting('highlight_outline')))
    old_selector = selector


class BrowserIntegrationSelectCommand(sublime_plugin.WindowCommand):
    plugin_name = "Select elements"
    plugin_description = "Select DOM elements either by CSS or XPath."

    def run(self):
        global chrome

        if chrome is None:
            warning("Chrome is not running.")
            return

        self.window.show_input_panel('Selector', old_selector or '',
                                     None, highlight, None)
