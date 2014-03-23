from .browser_integration import *


class BrowserIntegrationSourceCommand(sublime_plugin.ApplicationCommand):
    plugin_name = 'Page Source'
    plugin_description = "Open the page source in a new tab."

    @require_browser
    @async
    def run(self):
        source = browser.page_source
        view = sublime.active_window().new_file()
        view.set_name(browser.title)
        view.set_syntax_file('Packages/HTML/HTML.tmLanguage')
        view.run_command("insert_into_view", {"text": source})
