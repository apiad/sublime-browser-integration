from .browser_integration import *


inject_embedded_css_js = """
    var sheet = document.querySelector('style[data-bi-css="%s"]');
    sheet.innerHTML = %s;
"""


class BrowserIntegrationLiveCss(sublime_plugin.EventListener):
    def on_modified_async(self, view):
        if not browser.connected():
            return

        content = view.substr(sublime.Region(0, view.size()))
        name = view.name()

        if name and name.startswith('embedded-stylesheet-'):
            idx = name[len('embedded-stylesheet-'):].split('.')[0]

            code = inject_embedded_css_js % (idx, repr(content))
            print(code)
            browser.execute(code)
            status('Live editing CSS')
