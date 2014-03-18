from .browser_integration import *


inject_embedded_css_js = """
    var sheets = document.querySelectorAll('style');

    for(var i=0; i < sheets.length; i++) {
        if (sheets[i].getAttribute('data-bi-css') == '%s') {
            sheets[i].innerHTML = %s;
            break;
        }
    }
"""


class BrowserIntegrationLiveCss(sublime_plugin.EventListener):
    def on_modified_async(self, view):
        content = view.substr(sublime.Region(0, view.size()))
        name = view.name()

        if name and name.startswith('embedded-stylesheet-'):
            idx = name[len('embedded-stylesheet-'):].split('.')[0]

            if browser.connected():
                code = inject_embedded_css_js % (idx, repr(content))
                print(code)
                browser.execute(code)
                status('Live editing CSS')
