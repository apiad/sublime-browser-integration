from .browser_integration import *


class BrowserIntegrationTypeCommand(sublime_plugin.WindowCommand):
    plugin_name = "Type into selected elements"
    plugin_description = "Opens an input panel to type text into the browser."

    def run(self):
        global chrome

        if chrome is None:
            warning("Chrome is not running.")
            return

        if not old_selector:
            warning("No items are currently selected.")
            return

        @async
        def send_keys(str):
            status('Clicking all selected items')

            for e in chrome.find_elements_by_css_selector(old_selector):
                e.send_keys(str)

        self.window.show_input_panel('Input', '',
                                     send_keys, None, None)
