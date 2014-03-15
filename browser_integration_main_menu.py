from .browser_integration import *

from .browser_integration_launch import *
from .browser_integration_reload import *
from .browser_integration_navigate import *
from .browser_integration_execute import *
from .browser_integration_stylesheets import *
from .browser_integration_select import *
from .browser_integration_source import *
from .browser_integration_click import *
from .browser_integration_type import *


class BrowserIntegrationMainMenuCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        if not browser.connected():
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

            if browser.old_selector:
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
