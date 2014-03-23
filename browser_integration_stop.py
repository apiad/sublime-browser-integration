from .browser_integration import *


stop_macro_js = """
    storage = []
    localStorage.removeItem('__bi_tracking_events');
    localStorage.removeItem('__bi_counter');
    localStorage.removeItem('__bi_event_time');

    for (var p in localStorage) {
        if (p.substr(0, 10) === '__bi_event') {
            storage.push(JSON.parse(localStorage[p]));
            localStorage.removeItem(p);
        }
    }

    return storage;
"""


class BrowserIntegrationStopCommand(sublime_plugin.WindowCommand):
    plugin_name = "Stop recording"
    plugin_description = "Stop recording browser interaction," \
                         " and collect macro data."

    @require_browser
    @async
    def run(self):
        @async
        def cancel_macro():
            if sublime.ok_cancel_dialog("If you cancel the macro saving, "
                                        "all its data will be lost. "
                                        "There is no way to recover "
                                        "this data later. "
                                        "Are you sure you want to "
                                        "forget this macro?",
                                        "Yes, I wan't to forget the macro!"):
                return

            stop_macro()

        @async
        def stop_macro(name='untitled'):
            view = self.window.new_file()
            # view.set_syntax_file('Packages/JSON/JSON.tmLanguage')
            view.set_name(name + '.macro')
            view.run_command('insert_into_view', {'text': macro})

        browser.recording = False
        storage = browser.execute(stop_macro_js)

        if storage:
            with loading('Collecting events.'):
                storage.sort(key=lambda x: x['idx'])
                macro = sublime.encode_value(storage, pretty=True)

            self.window.show_input_panel('Macro name:', '', stop_macro,
                                         None, None)
        else:
            warning('No events recorded.')
