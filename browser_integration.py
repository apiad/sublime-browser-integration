import sublime
import sublime_plugin
import os
import sys
import threading
import time

sys.path.append(os.path.dirname(__file__))

from .selenium.webdriver import Chrome


SETTINGS_FILE = 'BrowserIntegration.sublime-settings'
chrome = None


def async(function):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=function, args=args, kwargs=kwargs)

        try:
            thread.start()
            return thread
        except Exception as e:
            warning(str(e))

    return wrapper


def setting(setting, cmd=None, default=None):
        settings = sublime.load_settings(SETTINGS_FILE)

        if cmd and hasattr(cmd, 'view'):
            view_settings = cmd.view.settings()
        else:
            view_settings = {}

        global_value = settings.get(setting, default)
        local_value = view_settings.get(setting, global_value)

        return local_value


def status(msg):
    sublime.status_message("Browser Integration :: %s" % msg)


def warning(msg):
    sublime.status_message("(!) Browser Integration :: %s" % msg)


class Loader:
    def __init__(self, msg):
        self.msg = msg
        self.stop = False

    def __enter__(self):
        self.run()

    def __exit__(self, _type, _value, _traceback):
        self.stop = True

    @async
    def run(self):
        count = 0
        up = True

        while not self.stop:
            load = "[" + " " * count + "=" + " " * (5 - count) + "]"
            sublime.status_message(load + " Browser Integration :: " + self.msg)
            time.sleep(0.1)
            if up:
                count += 1
                if count >= 5:
                    up = False
            else:
                count -= 1
                if count <= 0:
                    up = True

        sublime.status_message("")


def loading(msg):
    return Loader(msg)


@async
def install_chromedriver():
    if sublime.platform() == 'linux':
        if sublime.arch() == 'x32':
            dl_path = 'chromedriver-linux-32'
        elif sublime.arch() == 'x64':
            dl_path = 'chromedriver-linux-64'
    elif sublime.platform() == 'windows':
        dl_path = 'chromedriver-windows'
    elif sublime.platform() == 'osx':
        dl_path = 'chromedriver-osx'

    bin_name = 'chromedriver'
    bin_folder = os.path.dirname(__file__)
    bin_path = os.path.join(bin_folder, bin_name)

    dl_path = 'http://sublime.apiad.net/browser-integration/'\
              'chromedriver/%s' % dl_path

    if not os.path.exists(bin_path):
        with loading("Downloading chromedriver executable."):
            from urllib.request import urlopen

            with urlopen(dl_path) as response, open(bin_path, 'wb') as f:
                f.write(response.read())

            if sublime.platform() == 'linux':
                os.chmod(bin_path, 511)


install_chromedriver()


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

            home = setting('startup_location', self)

            with loading("Loading %s" % home):
                local_chrome.get(home)

            status("Chrome is up and running!")
            chrome = local_chrome

        open_chrome()


class BrowserIntegrationReloadCommand(sublime_plugin.ApplicationCommand):
    plugin_name = "Reload"
    plugin_description = "Reloads the current tab."

    def run(self):
        global chrome

        if chrome is None:
            warning("Chrome is not running (or detached).")
            return

        @async
        def refresh_browser():
            with loading("Refreshing browser"):
                chrome.refresh()

        refresh_browser()


class BrowserIntegrationNavigateCommand(sublime_plugin.WindowCommand):
    plugin_name = "Navigate To"
    plugin_description = "Opens a input panel to enter a URL to load in Chrome."

    def run(self):
        global chrome

        if chrome is None:
            warning("Chrome is not running.")
            return

        @async
        def onDone(str):
            with loading("Opening %s" % str):
                chrome.get(str)
            status("Loaded %s" % str)

        self.window.show_input_panel('Enter URL', chrome.current_url,
                                     onDone, None, None)


class BrowserIntegrationExecuteCommand(sublime_plugin.TextCommand):
    plugin_name = "Execute selected code"
    plugin_description = "Executes selected JavaScript code in the browser."

    def run(self, edit):
        global chrome

        if chrome is None:
            warning("Chrome is not running.")
            return

        @async
        def run_javascript():
            for region in self.view.sel():
                if region.empty():
                    continue

                s = self.view.substr(region)
                status("Executing `%s`" % s)
                result = chrome.execute_script(s)

                if result is not None:
                    view = sublime.active_window().new_file()
                    view.set_syntax_file(
                        "Packages/JavaScript/JavaScript.tmLanguage")
                    view.run_command("insert_into_view", {"text": str(result)})

        run_javascript()


class InsertIntoViewCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        self.view.insert(edit, 0, text)


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

old_selector = None


def highlight(selector):
    global chrome
    global old_selector

    if chrome is None:
        warning("Chrome is not running.")
        return

    if old_selector:
        chrome.execute_script(unselect_js % old_selector)

    chrome.execute_script(select_js % (selector, setting('highlight_outline')))
    old_selector = selector


class BrowserIntegrationSelectCommand(sublime_plugin.WindowCommand):
    plugin_name = "Select elements"
    plugin_description = "Select DOM elements either by CSS or XPath."

    def run(self):
        global chrome

        if chrome is None:
            warning("Chrome is not running.")
            return

        self.window.show_input_panel('Selector', old_selector or '',
                                     None, highlight, None)


class BrowserIntegrationClickCommand(sublime_plugin.WindowCommand):
    plugin_name = "Click elements"
    plugin_description = "Click currently selected items in the browser."

    def run(self):
        global chrome

        if chrome is None:
            warning("Chrome is not running.")
            return

        if not old_selector:
            warning("No items are currently selected.")
            return

        @async
        def click():
            status('Clicking all selected items')

            for e in chrome.find_elements_by_css_selector(old_selector):
                e.click()

        click()


class BrowserIntegrationTypeCommand(sublime_plugin.WindowCommand):
    plugin_name = "Type into selected elements"
    plugin_description = "Opens an input panel to type text into the browser."

    def run(self):
        global chrome

        if chrome is None:
            warning("Chrome is not running.")
            return

        if not old_selector:
            warning("No items are currently selected.")
            return

        @async
        def send_keys(str):
            status('Clicking all selected items')

            for e in chrome.find_elements_by_css_selector(old_selector):
                e.send_keys(str)

        self.window.show_input_panel('Input', '',
                                     send_keys, None, None)


get_css_hrefs_js = """
    var styleSheets = document.styleSheets;
    var results = [];

    for (var i=0; i < styleSheets.length; i++) {
        results.push(styleSheets[i].href);
    }

    return results;
"""


class BrowserIntegrationStylesheetsCommand(sublime_plugin.ApplicationCommand):
    plugin_name = "View loaded CSS (stylesheets)"
    plugin_description = "Lists all loaded stylesheets."

    def run(self):
        global chrome

        if chrome is None:
            warning("Chrome is not running.")
            return

        @async
        def view_css():
            @async
            def load_css(i):
                from urllib.request import urlopen

                if i >= 0:
                    response = urlopen(results[i])
                    text = response.read().decode('utf8')
                    view = sublime.active_window().new_file()
                    view.set_name(results[i])
                    view.set_syntax_file('Packages/CSS/CSS.tmLanguage')
                    view.run_command("insert_into_view", {"text": text})

            results = chrome.execute_script(get_css_hrefs_js)

            if results:
                sublime.active_window().show_quick_panel(results, load_css)
            else:
                status("There are no CSS style sheets loaded.")

        view_css()


class BrowserIntegrationSourceCommand(sublime_plugin.ApplicationCommand):
    plugin_name = 'View page source'
    plugin_description = "Open the page source in a new tab."

    @async
    def run(self):
        if chrome is None:
            warning("Chrome instance not running.")
            return

        source = chrome.page_source
        view = sublime.active_window().new_file()
        view.set_name(chrome.current_url)
        view.set_syntax_file('Packages/HTML/HTML.tmLanguage')
        view.run_command("insert_into_view", {"text": source})


class BrowserIntegrationMainMenuCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        if chrome is None:
            main_menu_commands = [
                BrowserIntegrationLaunchCommand,
            ]
        else:
            main_menu_commands = [
                BrowserIntegrationReloadCommand,
                BrowserIntegrationNavigateCommand,
                BrowserIntegrationExecuteCommand,
                BrowserIntegrationStylesheetsCommand,
                BrowserIntegrationSelectCommand,
                BrowserIntegrationSourceCommand,
            ]

            if old_selector:
                main_menu_commands.extend([
                    BrowserIntegrationClickCommand,
                    BrowserIntegrationTypeCommand,
                ])

        def select_command(i):
            if i < 0:
                return

            cls = main_menu_commands[i]
            cmd = command_str(cls)

            if issubclass(cls, sublime_plugin.ApplicationCommand):
                sublime.run_command(cmd)
            elif issubclass(cls, sublime_plugin.WindowCommand):
                sublime.active_window().run_command(cmd)
            elif issubclass(cls, sublime_plugin.TextCommand):
                sublime.active_window().active_view().run_command(cmd)

        def command_str(cls):
            name = cls.__name__
            return "browser_integration_" + name[18:-7].lower()

        def command_name(cls):
            return cls.plugin_name

        def command_description(cls):
            return cls.plugin_description

        sublime.active_window().show_quick_panel([
            [command_name(cls)] + command_description(cls).split("\n")
            for cls in main_menu_commands
        ], select_command)
