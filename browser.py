import sys
import os

sys.path.append(os.path.dirname(__file__))

from .selenium.webdriver import Chrome
from .selenium.webdriver import Firefox


class Browser:
    def __init__(self):
        from .browser_integration import status
        status("Intializing Browser instance.")

        self.webdriver = None
        self.selected_items = []
        self.old_selector = ''
        self.recording = False

    def connected(self):
        return self.webdriver is not None

    def connect(self, browser):
        if browser == 'Chrome':
            self.webdriver = Chrome(os.path.join(os.path.dirname(__file__),
                                    '..', 'chromedriver'))
        elif browser == 'Firefox':
            self.webdriver = Firefox()
        else:
            from .browser_integration import warning
            warning('Unknow browser driver: {}'.format(browser))

    def quit(self):
        if self.webdriver:
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
        except AttributeError as e:
            raise e
        except Exception as e:
            warning(str(e))
