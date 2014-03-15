from .browser_integration import *


class BrowserIntegrationSourceCommand(sublime_plugin.ApplicationCommand):
    plugin_name = 'View page source'
    plugin_description = "Open the page source in a new tab."

    @async
    def run(self):
        if chrome is None:
            warning("Chrome instance not running.")
            return

        source = chrome.page_source
        view = sublime.active_window().new_file()
        view.set_name(chrome.title)
        view.set_syntax_file('Packages/HTML/HTML.tmLanguage')
        view.run_command("insert_into_view", {"text": source})
