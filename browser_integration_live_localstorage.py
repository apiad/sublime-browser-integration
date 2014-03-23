from .browser_integration import *


set_local_storage_js = """
    storage = %s;
    localStorage.clear();

    for (var key in storage) {
        localStorage[key] = JSON.stringify(storage[key]);
    }
"""


class BrowserIntegrationLiveLocalStorage(sublime_plugin.EventListener):
    def on_modified_async(self, view):
        if not browser.connected():
            return

        if view.name() == 'localStorage':
            content = view.substr(sublime.Region(0, view.size()))
            browser.execute(set_local_storage_js % content)
