from .browser_integration import *
from .browser_integration_select import *


class BrowserIntegrationClickCommand(sublime_plugin.WindowCommand):
    plugin_name = "Click elements"
    plugin_description = "Click currently selected items in the browser."

    @staticmethod
    def visible():
        return browser.connected() and browser.selected_items

    @require_browser
    def run(self):
        if not browser.selected_items:
            warning("No items are currently selected.")
            return

        @async
        def click():
            status('Clicking all selected items.')

            for e in browser.selected_items:
                e.click()

        click()
