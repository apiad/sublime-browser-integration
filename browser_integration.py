import sublime
import sublime_plugin
import os
import sys
import threading
import time

sys.path.append(os.path.dirname(__file__))

from .browser import Browser

SETTINGS_FILE = 'BrowserIntegration.sublime-settings'

browser = Browser()
log_file = '/var/log/sublime-browser-integration.log'


def require_browser(function):
    def wrapper(*args, **kwargs):
        if not browser.connected():
            warning("The browser is not open (or detached).")
            return

        return function(*args, **kwargs)

    return wrapper


def async(function):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=function, args=args, kwargs=kwargs)

        try:
            thread.start()
            return thread
        except Exception as e:
            with open(log_file, 'a') as f:
                f.write(str(e) + '\n')

            print(str(e))
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
    msg = "Browser Integration :: %s" % msg
    print(msg)
    sublime.status_message(msg)


def warning(msg):
    msg = "(!) Browser Integration :: %s" % msg
    print(msg)
    sublime.status_message(msg)


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

        print("[Start] Browser Integration :: " + self.msg)

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

        print("[End] Browser Integration :: " + self.msg)
        sublime.status_message("")


def loading(msg):
    return Loader(msg)


class InsertIntoViewCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        self.view.insert(edit, 0, text)
