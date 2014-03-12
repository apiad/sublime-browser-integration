import sublime
import sublime_plugin
import os
import sys
import threading
import time

from BrowserIntegration.selenium.webdriver import Chrome


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
    sublime.status_message("BrowserIntegration :: %s" % msg)


def warning(msg):
    sublime.status_message("(!) BrowserIntegration :: %s" % msg)


@async
def loading(msg, delay=1):
    start = time.time()
    count = 0
    up = True

    while time.time() - start < delay:
        load = "[" + " " * count + "=" + " " * (5 - count) + "]"
        sublime.status_message(load + " BrowserInteration :: " + msg)
        time.sleep(0.1)
        if up:
            count += 1
            if count == 5:
                up = False
        else:
            count -= 1
            if count == 0:
                up = True


class OpenBrowserCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        global chrome

        if chrome is not None:
            status("Shutting down Chrome instance.")
            chrome.quit()
            chrome = None

        @async
        def open_chrome():
            global chrome

            loading("Opening Chrome new instance.")
            local_chrome = Chrome()
            home = setting('home', self)
            loading("Loading %s" % home)
            local_chrome.get(home)
            status("Chrome is up and running!")
            chrome = local_chrome

        open_chrome()


class ReloadBrowserCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        global chrome

        if chrome is None:
            warning("Chrome is not running (or detached).")
            return

        @async
        def refresh_browser():
            loading("Refreshing browser")
            chrome.refresh()

        refresh_browser()


class GoToUrlCommand(sublime_plugin.WindowCommand):
    def run(self):
        global chrome

        if chrome is None:
            warning("Chrome is not running.")
            return

        @async
        def onDone(str):
            status("Opening %s" % str)
            chrome.get(str)
            status("Loaded %s" % str)

        self.window.show_input_panel('Enter URL', setting('home', self),
                                     onDone, None, None)


class RunJavascriptInBrowserCommand(sublime_plugin.TextCommand):
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
                chrome.execute_script(s)

        run_javascript()


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

    if old_selector is not None:
        chrome.execute_script(unselect_js % old_selector)

    chrome.execute_script(select_js % (selector, setting('highlight-overlay')))
    old_selector = selector


class HighlightInBrowserCommand(sublime_plugin.WindowCommand):
    def run(self):
        global chrome

        if chrome is None:
            warning("Chrome is not running.")
            return

        self.window.show_input_panel('Selector', '',
                                     None, highlight, None)
