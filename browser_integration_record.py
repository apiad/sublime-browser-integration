from .browser_integration import *
from .browser_integration_inject import inject_browser_macros_js


record_macro_js = """
localStorage.__bi_counter = 0;
localStorage.__bi_tracking_events = true;
localStorage.__bi_event_time = + new Date();
"""


class BrowserIntegrationRecordCommand(sublime_plugin.WindowCommand):
    plugin_name = "Record macro"
    plugin_description = "Start recording browser interaction."

    @staticmethod
    def visible():
        return browser.connected() and not browser.recording

    @async
    @require_browser
    def run(self):
        browser.recording = True
        browser.execute(record_macro_js)
        inject_browser_macros_js()
