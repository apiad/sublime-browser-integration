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
        self.old_css_selector = ''
        self.old_xpath_selector = ''
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

    def select_xpath(self, selector, highlight=True):
        from .browser_integration import setting

        self.unselect()

        if selector:
            try:
                self.selected_items = \
                    self.webdriver.find_elements_by_xpath(selector)[:1]

                self.execute(select_xpath_js % (selector,
                                                setting('highlight_outline')))

                self.old_xpath_selector = selector
            except:
                self.unselect()
        else:
            self.unselect()

        return self.selected_items

    def select_css(self, selector, highlight=True):
        from .browser_integration import setting

        self.unselect()

        if selector:
            try:
                self.selected_items = \
                    self.webdriver.find_elements_by_css_selector(selector)

                self.execute(select_css_js % (selector,
                                              setting('highlight_outline')))

                self.old_css_selector = selector
            except:
                self.unselect()
        else:
            self.unselect()

        return self.selected_items

    def unselect(self):
        self.execute(unselect_js)
        self.old_xpath_selector = ""
        self.old_css_selector = ""
        self.selected_items = []

    def execute(self, script):
        from .browser_integration import warning

        print("BrowserIntegration :: Executing script:")
        print(script)

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


select_css_js = """
    elements = document.querySelectorAll("%s");

    for (var i=0; i<elements.length; i++) {
        var el = elements[i];
        el.setAttribute("data-bi-outline", el.style.outline);
        el.classList.add('bi-selected');
        el.style.outline = "%s";
    }
"""


unselect_js = """
    elements = document.querySelectorAll(".bi-selected");

    for (var i=0; i<elements.length; i++) {
        var el = elements[i];
        el.style.outline = el.getAttribute("data-bi-outline");
        el.classList.remove('bi-selected');
    }
"""


select_xpath_js = """
    var evaluator = new XPathEvaluator();

    var result = evaluator.evaluate('%s', document.documentElement,
        null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);

    var el = result.singleNodeValue;

    if (!!el) {
        el.setAttribute("data-bi-outline", el.style.outline);
        el.classList.add('bi-selected');
        el.style.outline = "%s";
    }
"""
