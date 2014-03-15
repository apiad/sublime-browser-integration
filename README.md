# Browser Integration

A Sublime Text 3 plugin for interacting with the browser and do web development related tasks.


### Disclaimer:

This plugin is in development state, which means is unstable, and it might not work in your system. It **should** work with *Google Chrome* and *Chromium Browser* versions 31 to 34, on modern versions of Linux, MacOSX and Windows, **but** it has only been tested so far with:

* Ubuntu Linux 13.10 + ST3 + Chrome 31

Current iterations are constantly changing the names, key bindings, and semantics of most commands, so every time you upgrade something will likely not work the way it used to. Sorry for the inconvenience, I'm working as hard as possible to get a stable version out, but it will take me some time...


## What is this?

This plugin fires up browser (Chrome only, for now), and keeps a connection open with it, that allows you to send commands and control to the browser from within ST3.

I made this plugin inspired by the work of _Bret Victor_ and his idea of multimedia connection. Basically, it means that developers should be as close as possible to their creations, and I wasn't happy with the current level of connectivity I can reach in my web development environment.

As web developers, must of the time we work in two different environments: our text editor, and the browser. We have to constantly change form typing code to refreshing the browser, from test short scripts in the browser's development console to writing more complex scripts in the server, from inspecting DOM elements and changing CSS in the browser, to go back to the text editor and figure out where those new CSS rules fit in.

This plugin is my attempt to bring both tools a little closer, and create a connection between browser and text editor that really lets you feel you are working with a single connected tool, not two disconnected different pieces of technology.


## Installation

The recommended method is using [Sublime Package Control](https://sublime.wbond.net). If you don't know it, go check it out.

You can also [clone directly](https://github.com/apiad/sublime-browser-integration.git) from Github, or download a [zip](https://github.com/apiad/sublime-browser-integration/archive/master.zip), and unpack it in your Sublime Text 3 packages folder. If you don't know how to do this, you definitely need the Package Control plugin.

Besides that, you need a recent version of Chrome (31 to 34) and the `Chrome WebDriver` executable. Upon installation of the plugin, it will attempt to download the right executable for your platform (its about 5 MBs) directly from [sublime.apiad.net](http://sublime.apiad.net/browser-integration/chromedriver/) and place it in the same folder as the plugin (this only has to be done once). If this doesn't work, you can try to download it manually, rename it to `chromedriver`, place it alongside the *.sublime-package file, and give it execution permissions. If this happens to you, please consider filling up the corresponding [issue](https://github.com/apiad/sublime-browser-integration/issues) to help me improve the plugin.


## Configuration

Hit `ctrl+shift+p` and go to 'Browser Integration: Settings (Default)' to read (and possible change) all available configuration parameters.


## Features:

Right now, this is what it can do:

### Main Menu

**Key binding:** `ctrl+alt+shift+b`

Will open a menu panel, where you can find all available commands, navigate, view descriptions, etc. If in doubt, start here. All commands are accessible through this menu, but most of them also have direct key bindings.

When first run, it will only show one command: **Launch Browser**. This is a necessary step before running any other browser-related command.

### Launch Browser

**Key binding:** `ctrl+shift+b,l`

Opens a new Google Chrome instance. All other browser commands require this one to be called first, and will complain (in your status bar) if Chrome is not open, or if the plugin has lost the connection somehow.
After the browser has been opened, the main menu will show more commands. You can directly interact with the opened browser, create new tabs, click in stuff, etc. However, only the first opened tab will be controlled by the plugin, and if closed, connection will be lost and you'll need to launch the browser again. A browser instance can only be controlled if opened through this command, it will not work with an already opened browser.

After opening the browser, it will navigate automatically to your configured starting page. This can changed in the default configuration, under the `home` settings.

### Other

**Go To URL** (`ctrl+shift+b` `g`) tells Chrome to navigate to a new URL. By default, it open the one specified in the plugin settings, under the `home` key (`localhost:8000` for a start).

**Reload Chrome** (`ctrl+shift+b` `r`) does what it says, reloads Chrome.

**Evaluate in Chrome** (`ctrl+shift+b` `e`) takes the selected JavaScript source and evaluates it in the Chrome instance, in the currently open tab. If the code returns something, it will be opened in a new tab.

**View load CSS (stylesheets)** (`ctrl+shift+b` `s`) open a quick panel with the `href`s of all stylesheets that are currently loaded in the active tab. Selecting one of the entries attempts to download and open the corresponding file in a new tab in Sublime.

**Highlight in Chrome** (`ctrl+shift+b` `h`) opens a tiny input box, where you can type any valid CSS selector. Matching items are highlighted in the Chrome instance as you type, and stay highlighted
after you close.

These highlighted elements can be used in other commands, to make specific DOM manipulations:

**Click selected elements** (`ctrl+shift+b` `c`) clicks all elements previously selected.

**Type into selected elements** (`ctrl+shift+b` `t`) opens an input box to type into the previously selected elements.

With these commands in combination you can easily automatize boring tasks. For instance, every time I work on my site's project, I open ST3, start my development server, open Chrome, navigate to `localhost:9090`, type in my credentials, and then I can start developing.

Right now I'm working on a macro utility for the plugin, that will be available shortly. We need a special macro system, because most of these commands are asynchronous, and hence don't get along very well with the macro system integrated into Sublime.


## How does it work?

The plugin ships with a modified version of [selenium for Python](https://pypi.python.org/pypi/selenium), which does the browser controlling magic. That and a few handy JavaScript and Python gets the work done.


## What's next?

I'm working on a few exciting new features:

* Automatic reload on save.
* Live CSS editing.
* Live highlight of selected jQuery selectors.
* Macro recording and playing.
* Support for other browsers (Firefox, Opera, perhaps even IE).
* And many more...


## Collaborating

Sure, come to [Github](https://github.com/apiad/sublime-browser-integration).

There are many ways to collaborate: just by trying it out and filling up any issues, it will be of great help. It's very hard to develop a multi-platform Sublime Text plugin, specially when you have to deal with different implementations of browsers, and I can not possible test every combination of Sublime Text + Chrome + OS out there, so beta testing is the most precious help you can offer.

If you want to put some code into the plugin, then even better! As usual, fork it, and make your pull request. I'm eager to see what other awesome developers like you come up with... ;)
