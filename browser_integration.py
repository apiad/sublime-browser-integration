import sublime
import sublime_plugin
import os
import sys
import threading
import time

sys.path.append(os.path.dirname(__file__))


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
