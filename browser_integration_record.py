from .browser_integration import *


record_macro_js = """
    localStorage.__bi_counter = 0;

    document.onclick = function (evt) {
        var counter = Number(localStorage.__bi_counter);
        localStorage.__bi_counter = counter + 1;

        localStorage['__bi_event_' + counter] = JSON.stringify({
            type: 'click',
            x: evt.pageX,
            y: evt.pageY,
            btn: evt.which,
            altKey: evt.altKey,
            metaKey: evt.metaKey,
            ctrlKey: evt.ctrlKey,
            shiftKey: evt.shiftKey,
            idx: counter,
        });
    }
"""


class BrowserIntegrationRecordCommand(sublime_plugin.WindowCommand):
    plugin_name = "Record macro"
    plugin_description = "Start recording browser interaction."

    @require_browser
    def run(self):
        browser.recording = True
        browser.execute(record_macro_js)
