from .browser_integration import *
from .selenium.webdriver import Chrome


class BrowserIntegrationLaunchCommand(sublime_plugin.ApplicationCommand):
    plugin_name = "Launch Browser"
    plugin_description = "Launches a new browser instance."

    def run(self):
        @async
        def open_chrome():
            global chrome

            if chrome is not None:
                with loading("Shutting down Chrome instance."):
                    chrome.quit()
                    chrome = None

            with loading("Opening Chrome new instance."):
                local_chrome = Chrome(os.path.join(os.path.dirname(__file__),
                                                   'chromedriver'))
                if setting('maximize_on_startup', self):
                    local_chrome.maximize_window()
                else:
                    x, y = setting('window_position', self)
                    w, h = setting('window_size', self)
                    local_chrome.set_window_position(x, y)
                    local_chrome.set_window_size(w, h)

            home = setting('startup_location', self)

            with loading("Loading %s" % home):
                local_chrome.get(home)

            status("Chrome is up and running!")
            chrome = local_chrome

        open_chrome()
