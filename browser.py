import sys
import os

sys.path.append(os.path.dirname(__file__))

from .selenium.webdriver import Chrome


class Browser:
    def __init__(self):
        print("Intializing BrowserIntegration instance.")

        self.webdriver = None
        self.selected_items = []
        self.old_selector = ''
        self.recording = False

    def connected(self):
        return self.webdriver is not None

    def connect(self):
        self.webdriver = Chrome(os.path.join(os.path.dirname(__file__), '..',
                                             'chromedriver'))

    def quit(self):
        self.webdriver.quit()
        self.webdriver = None

    def select_css(self, selector):
        if selector:
            try:
                self.selected_items = \
                    self.webdriver.find_elements_by_css_selector(selector)

                self.old_selector = selector
            except:
                self.selected_items = []
        else:
            self.selected_items = []
            self.old_selector = ''

        return self.selected_items

    def execute(self, script):
        from .browser_integration import warning

        try:
            return self.webdriver.execute_script(script)
        except Exception as e:
            warning(str(e))

    def __getattr__(self, attr):
        from .browser_integration import warning

        try:
            return getattr(self.webdriver, attr)
        except Exception as e:
            warning(str(e))
