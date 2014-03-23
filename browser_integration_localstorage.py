import json

from .browser_integration import *


get_local_storage_js = """
    result = {}

    for (var key in localStorage) {
        if (key.substr(0, 5) != '__bi_') {
            var item = localStorage[key];
            result[key] = JSON.parse(item);
        }
    }

    return result;
"""


class BrowserIntegrationLocalstorageCommand(sublime_plugin.WindowCommand):
    plugin_name = "LocalStorage Content"
    plugin_description = "View and modify the content of the localStorage."

    @staticmethod
    def visible():
        return browser.connected()

    @async
    @require_browser
    def run(self):
        with loading("Dumping localStorage content."):
            local_storage = browser.execute(get_local_storage_js)

        if local_storage is not None:
            view = self.window.new_file()
            view.set_name('localStorage')
            view.run_command("insert_into_view",
                             {"text": json.dumps(local_storage, indent=4)})
        else:
            warning("LocalStorage cannot be accessed right now.")
