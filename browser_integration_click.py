from browser_integration import *


class BrowserIntegrationClickCommand(sublime_plugin.WindowCommand):
    plugin_name = "Click elements"
    plugin_description = "Click currently selected items in the browser."

    def run(self):
        global chrome

        if chrome is None:
            warning("Chrome is not running.")
            return

        if not old_selector:
            warning("No items are currently selected.")
            return

        @async
        def click():
            status('Clicking all selected items')

            for e in chrome.find_elements_by_css_selector(old_selector):
                e.click()

        click()
