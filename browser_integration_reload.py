from .browser_integration import *


class BrowserIntegrationReloadCommand(sublime_plugin.ApplicationCommand):
    plugin_name = "Reload"
    plugin_description = "Reloads the current tab."

    def run(self):
        global chrome

        if chrome is None:
            warning("Chrome is not running (or detached).")
            return

        @async
        def refresh_browser():
            with loading("Refreshing browser"):
                chrome.refresh()

        refresh_browser()
