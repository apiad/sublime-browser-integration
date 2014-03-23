from .browser_integration import *


record_macro_js = """
localStorage.__bi_counter = 0;
localStorage.__bi_tracking_events = true;
"""


class BrowserIntegrationRecordCommand(sublime_plugin.WindowCommand):
    plugin_name = "Record macro (experimental)"
    plugin_description = "Start recording browser interaction."

    @require_browser
    def run(self):
        browser.recording = True
        browser.execute(record_macro_js)
