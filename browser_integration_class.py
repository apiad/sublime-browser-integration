from .browser_integration import *


set_class_js = """
    var items = document.querySelectorAll('%s');

    for (var i=0; i < items.length; i++) {
        items[i].className = '%s';
    }
"""


class BrowserIntegrationClassCommand(sublime_plugin.WindowCommand):
    plugin_name = "Change selected elements class"
    plugin_description = "Opens an input panel to modify selected items class."

    @staticmethod
    def visible():
        return browser.connected() and browser.selected_items

    @require_browser
    def run(self):
        if not browser.selected_items:
            warning("No items are currently selected.")
            return

        classes = set()

        for e in browser.selected_items:
            for cl in e.get_attribute('class').split():
                classes.add(cl)

        @async
        def change_class(classes):
            status('Setting items classes.')
            browser.execute(set_class_js % (browser.old_selector, classes))

        classes = " ".join(classes)

        @async
        def cancel_class():
            browser.execute(set_class_js % (browser.old_selector, classes))

        view = self.window.show_input_panel('Input', classes,
                                            None, change_class, cancel_class)

        view.sel().add(sublime.Region(0, view.size()))
