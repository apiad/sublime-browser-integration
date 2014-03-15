from .browser_integration import *


class BrowserIntegrationReloadCommand(sublime_plugin.ApplicationCommand):
    plugin_name = "Reload"
    plugin_description = "Reloads the current tab."

    @require_browser
    @async
    def run(self):
        with loading("Refreshing browser"):
            browser.refresh()
