from .browser_integration import *


class BrowserIntegrationSelectCommand(sublime_plugin.WindowCommand):
    plugin_name = "Select by CSS"
    plugin_description = "Select DOM elements by CSS selector."

    @async
    @require_browser
    def run(self):
        old_selector = browser.old_css_selector

        @async
        def cancel():
            browser.unselect()

            if old_selector:
                browser.browser.select_css(old_selector)

        view = self.window.show_input_panel('CSS Selector',
                                            browser.old_css_selector,
                                            None, self.highlight, cancel)

        view.sel().add(sublime.Region(0, view.size()))

    def highlight(self, selector):
        browser.select_css(selector)


class BrowserIntegrationSelectxpathCommand(sublime_plugin.WindowCommand):
    plugin_name = "Select by XPath"
    plugin_description = "Select DOM elements by XPath selector."

    @async
    @require_browser
    def run(self):
        old_selector = browser.old_xpath_selector

        @async
        def cancel():
            browser.unselect()

            if old_selector:
                browser.browser.select_xpath(old_selector)

        view = self.window.show_input_panel('CSS Selector',
                                            browser.old_xpath_selector,
                                            None, self.highlight, cancel)

        view.sel().add(sublime.Region(0, view.size()))

    def highlight(self, selector):
        browser.select_xpath(selector)
