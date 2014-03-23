from .browser_integration import *


select_js = """
    elements = document.querySelectorAll("%s");

    for (var i=0; i<elements.length; i++) {
        var el = elements[i];
        el.setAttribute("data-bi-outline", el.style.outline);
        el.style.outline = "%s";
    }
"""


unselect_js = """
    elements = document.querySelectorAll("%s");

    for (var i=0; i<elements.length; i++) {
        var el = elements[i];
        el.style.outline = el.getAttribute("data-bi-outline");
    }
"""


class BrowserIntegrationSelectCommand(sublime_plugin.WindowCommand):
    plugin_name = "Select elements"
    plugin_description = "Select DOM elements either by CSS or XPath."

    @require_browser
    def run(self):
        old_selector = browser.old_selector

        def cancel():
            browser.execute(unselect_js % browser.old_selector)

            if self.selector:
                browser.execute(unselect_js % self.selector)

            if old_selector:
                browser.execute(select_js % (old_selector,
                                             setting('highlight_outline')))
                browser.select_css(old_selector)

        view = self.window.show_input_panel('Selector', browser.old_selector,
                                            None, self.highlight, cancel)

        view.sel().add(sublime.Region(0, view.size()))

    @require_browser
    def highlight(self, selector):
        if browser.old_selector:
            browser.execute(unselect_js % browser.old_selector)

        if selector:
            self.selector = selector
            browser.execute(select_js % (selector,
                                         setting('highlight_outline')))

        browser.select_css(selector)
