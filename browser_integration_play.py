from .browser_integration import *
from .selenium.webdriver.common.action_chains import ActionChains


class BrowserIntegrationPlayCommand(sublime_plugin.WindowCommand):
    plugin_name = 'Play macro'
    plugin_description = 'Plays a previously recorded macro.'

    @staticmethod
    def visible():
        return browser.connected()

    @require_browser
    @async
    def run(self):
        def get_macro_info(path):
            name = os.path.basename(path)
            name, ext = os.path.splitext(name)
            return [name, path]

        folders = self.window.folders()
        print("Searching macros in folders: {}".format(folders))

        with loading("Searching saved macros."):
            macros = []

            for folder in folders:
                for dirpath, dirnames, filenames in os.walk(folder,
                                                            followlinks=True):
                    if '.git' in dirnames:
                        dirnames.remove('.git')

                    for filename in filenames:
                        name, ext = os.path.splitext(filename)
                        if ext == '.macro':
                            macros.append(
                                get_macro_info(os.path.join(dirpath,
                                                            filename)))

        print("Found macros: {}".format(macros))

        @async
        def play_macro(i):
            if i < 0:
                return

            with open(macros[i][1]) as f:
                macro = sublime.decode_value(f.read())

            with loading("Replaying macro."):
                for action in macro:
                    self.perform_action(action)

        if macros:
            self.window.show_quick_panel(macros, play_macro)
        else:
            warning('No macros defined in the project.')

    def delay(self, delay):
        pass

    def perform_action(self, action):
        attr = action['type']

        delay = action['delay']

        if delay > 10:
            self.delay(delay)

        if hasattr(self, attr):
            f = getattr(self, attr)
            print("Executing macro action: {}".format(attr))
            print("    on {}".format(action['el']))
            try:
                f(action)
            except Exception as e:
                warning(str(e))
                print(str(e))
        else:
            print("Unknown macro action: {}".format(attr))
            warning('Unknown macro action: %s' % action['type'])

    def mousedown(self, action):
        element = browser.find_element_by_xpath(action['el'])

        chain = ActionChains(browser.webdriver)
        chain.move_to_element_with_offset(element, action['x'], action['y'])
        chain.click_and_hold()
        chain.perform()

    def mouseup(self, action):
        element = browser.find_element_by_xpath(action['el'])

        chain = ActionChains(browser.webdriver)
        chain.move_to_element_with_offset(element, action['x'], action['y'])
        chain.release()
        chain.perform()

    def keypress(self, action):
        element = browser.find_element_by_xpath(action['el'])

        chain = ActionChains(browser.webdriver)
        chain.move_to_element(element)
        chain.send_keys(chr(action['which']))
        chain.perform()


class BrowserIntegrationPlaydelayCommand(BrowserIntegrationPlayCommand):
    plugin_name = 'Play macro (with delays)'
    plugin_description = "Plays a previously recored macro"\
                         " honoring input delay."

    def delay(self, delay):
        time.sleep(delay / 1000)
