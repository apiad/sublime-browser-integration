import re

from .browser_integration import *


class BrowserIntegrationAutoReload(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        if not browser.connected():
            return

        auto_reload = setting('reload_on_save')

        if not auto_reload:
            return

        selectors = setting('reload_on_save_selectors')
        name = view.file_name()

        for s in selectors:
            if re.match(s, name):
                with loading("Reloading automatically on save."):
                    browser.refresh()

                return
