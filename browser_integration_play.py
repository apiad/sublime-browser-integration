from .browser_integration import *
from .selenium.webdriver.common.action_chains import ActionChains


class BrowserIntegrationPlayCommand(sublime_plugin.WindowCommand):
    plugin_name = 'Play macro'
    plugin_description = 'Play a previously recorded macro.'

    @require_browser
    @async
    def run(self):
        def get_macro_info(path):
            name = os.path.basename(path)
            name, ext = os.path.splitext(name)
            return [name, path]

        with loading("Searching saved macros."):
            folders = self.window.folders()
            macros = []

            for folder in folders:
                for dirpath, dirnames, filenames in os.walk(folder):
                    if '.git' in dirnames:
                        dirnames.remove('.git')

                    for filename in filenames:
                        name, ext = os.path.splitext(filename)
                        if ext == '.macro':
                            macros.append(
                                get_macro_info(os.path.join(dirpath,
                                                            filename)))

        @async
        def play_macro(i):
            if i < 0:
                return

            with open(macros[i][1]) as f:
                macro = sublime.decode_value(f.read())

            for action in macro:
                self.perform_action(action)

        self.window.show_quick_panel(macros, play_macro)

    def perform_action(self, action):
        attr = action['type']

        if hasattr(self, attr):
            getattr(self, attr)(action)
        else:
            warning('Unknown macro action: %s' % action['type'])

    def click(self, action):
        chain = ActionChains(browser.webdriver)
        chain.move_by_offset(action['x'], action['y'])
        chain.click()
        chain.perform()
