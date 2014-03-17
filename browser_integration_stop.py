from .browser_integration import *


stop_macro_js = """
    storage = []

    for (var p in localStorage) {
        if (p.substr(0, 10) === '__bi_event') {
            storage.push(JSON.parse(localStorage[p]));
            localStorage.removeItem(p);
        }
    }

    return storage;
"""


class BrowserIntegrationStopCommand(sublime_plugin.WindowCommand):
    plugin_name = "Stop recording macro"
    plugin_description = "Stop recording browser interaction."

    @require_browser
    def run(self):
        @async
        def stop_macro(name):
            storage = browser.execute(stop_macro_js)
            storage.sort(key=lambda x: x['idx'])
            macro = sublime.encode_value(storage, pretty=True)
            browser.recording = False

            view = self.window.new_file()
            # view.set_syntax_file('Packages/JSON/JSON.tmLanguage')
            view.set_name(name + '.macro')
            view.run_command('insert_into_view', {'text': macro})

        self.window.show_input_panel('Macro name:', '', stop_macro, None, None)
