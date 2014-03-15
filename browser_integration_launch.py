from .browser_integration import *


class BrowserIntegrationLaunchCommand(sublime_plugin.ApplicationCommand):
    plugin_name = "Launch Browser"
    plugin_description = "Launches a new browser instance."

    def run(self):
        @async
        def open_chrome():
            if browser.connected():
                with loading("Shutting down current Chrome instance."):
                    browser.quit()

            with loading("Opening new Chrome instance."):
                browser.connect()

                if setting('maximize_on_startup', self):
                    browser.maximize_window()
                else:
                    x, y = setting('window_position', self)
                    w, h = setting('window_size', self)
                    browser.set_window_position(x, y)
                    browser.set_window_size(w, h)

            home = setting('startup_location', self)

            with loading("Loading %s" % home):
                browser.get(home)

            status("Chrome is up and running!")

        open_chrome()
