# Browser Integration

A Sublime Text 3 plugin for interacting with the browser and perform web development related tasks.


### Disclaimer:

This plugin is in development state, which means is unstable, and it might not work in your system. It **should** work with *Google Chrome* and *Chromium Browser* versions 31 to 34, on modern versions of Linux, MacOSX and Windows, **but** it has only been tested so far with:

* Ubuntu Linux 13.10 + ST3 (3059) + Chrome 31

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

After opening the browser, it will navigate automatically to your configured starting page. This can changed in the default configuration, under the `startup_location` settings.

### Reload

**Key binding:** `ctrl-shift+b,r`

Reloads the browser. You can configure the `reload_on_save` setting to automatically invoke this command upon save. The `reload_on_save_selector` contains a list of regular expressions. Every time you save a file, if its filename matches any of the regular expressions, the browser will be reloaded. By default this options are set so to reload upon saving any HTML, CSS or JavaScript file.

### Navigate To

**Key binding:** `ctrl+shift+b,n`

Opens an input panel to enter a URL, to force the browser to navigate to it. The currently loaded URL is already selected in the input panel. If you don't type a valid locator (`http`, `https`, etc.), then `http://` is appended to the URL.

### Execute selected code

**Key binding:** `ctrl+shift+b,e`

Takes the selected JavaScript source and runs it in the browser. If the code returns something, it will be opened in a new tab. This is done independently for every selected region, and will open as many tabs as necessary, for every selected piece of script that returns something.

### View load CSS (stylesheets)

**Key binding:** `ctrl+shift+b,c`

Opens a quick panel with the list of all stylesheets that are currently loaded in the browser. Imported stylesheets (`link` tags) are listed by URL. Embedded stylesheets (`style` tags) are listed independently, with a small preview of the style code. Upon selecting one of the entries, a new tab is openned with the content of the stylesheet. If it was an imported stylesheet, the command will attempt to download the `link` tag's `href` property, and open it in a new tag. If it was embedded, the command will copy the `innerHTML` property of the `style` tag, and paste it in a new tab.

Right now I'm working on a feature to allow the specification of mappings between URLs and local files, so that the command can identify which URLs are local static files, and load those files instead of downloading the stylesheets.

Another incoming feature is the live editing of these CSS files, with automatic asynchronous browser reload, something I'm very excited of, but still trying to get to work.

### Select elements

**Key binding:** `ctrl+shift+b,s`

Opens an input box, where you can type any valid CSS selector. Matching items are highlighted in the browser as you type, and stay highlighted after you close. These selected elements can be used in other commands, to make specific DOM manipulations. To unselect, launch the command again, and clear the input panel.

### Modify DOM elements

If you have previously selected any DOM elements, the following commands will allow you to make modifications to those elements. These commands will only appear in the main menu if you have selected elements.

### Click selected elements

**Key binding:** `ctrl+shift+b,d,c`

Sends a click to selected elements.

### Type into selected elements

**Key binding:** `ctrl+shift+b,d,t`

Opens an input box to type a text, that will be sent to the browser and typed into the selected elements.

### Change selected elements class

**Key binding:** `ctrl+shift+b,d,s`

Open an input box with the value of the `class` attribute of selected elements. If there are more than one selected element, with different classes, the input box will show the union of the elements `class` attributes. Typing into the input panel will update the selected elements `class` attribute in real-time.

## (Experimental) Task automation

With these commands in combination you can easily automatize boring tasks. For instance, every time I work on my site's project, I open ST3, start my development server, open Chrome, navigate to `localhost:9090`, type in my credentials, and then I can start developing.

Right now I'm working on a macro utility for the plugin, that will be available shortly. We need a special macro system, because most of these commands are asynchronous, and hence don't get along very well with the macro system integrated into Sublime.

For the time being, you can record macros, save them, and play them again later. Right now the plugin only stores click events, and it doesn't work very well, so play with care. Select `Record macro` from the main menu, and then interact with the browser. Select `Stop recording macro` once done, a small input panel will pop out asking for a macro name. Enter a name and hit enter, and the macro data will be shown on a new file (its a JSON with all the evens information). Save it somewhere in your project, and when you later call `Play macro`, a small quick panel will show you all macros stored in your project (files with `.macro` extension).


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

You can also suggest changes, features, and any interesting idea.
