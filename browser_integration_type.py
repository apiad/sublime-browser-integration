from .browser_integration import *
from .browser_integration_select import *


class BrowserIntegrationTypeCommand(sublime_plugin.WindowCommand):
    plugin_name = "Type into selected elements"
    plugin_description = "Opens an input panel to type text into the browser."

    @require_browser
    def run(self):
        if not browser.selected_items:
            warning("No items are currently selected.")
            return

        @async
        def send_keys(str):
            status('Typing into all selected items.')

            for e in browser.selected_items:
                e.send_keys(str)

        self.window.show_input_panel('Input', '',
                                     send_keys, None, None)
