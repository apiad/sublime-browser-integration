Browser Integration
===================

A Sublime Text 3 plugin for interacting with the
browser and do developer related tasks.


What does it do?
----------------

This plugin fires up browser (Chrome only, for now),
and keeps a connection open with it, that allows you
to send commands to the browser from within ST3.

Right now it provides a few commands:

**Run Chrome** (`ctrl+shift+b` `l`) will open a new Google Chrome instance.
All other commands require this one to be called first,
and will complain (in your status bar) if Chrome is not
open, or if the plugin has lost the connection somehow.

**Go To URL** (`ctrl+shift+b` `g`) tells Chrome to navigate to a new URL.
By default, it open the one specified in the plugin settings,
under the `home` key (`localhost:8000` for a start).

**Reload Chrome** (`ctrl+shift+b` `r`) does what it says, reloads Chrome.

**Evaluate in Chrome** (`ctrl+shift+b` `e`) takes the selected JavaScript source
and evaluates it in the Chrome instance, in the currently
open tab.

**Highlight in Chrome** (`ctrl+shift+b` `h`) opens a tiny input box, where you
can type any valid CSS selector. Matching items are highlighted
in the Chrome instance as you type, and stay highlighted
after you close.

These highlighted elements can be used in other
commands, to make specific DOM manipulations:

**Click selected elements** (`ctrl+shift+b` `c`) clicks all elements
previously selected.

**Type into selected elements** (`ctrl+shift+b` `t`) opens an input
box to type into the previously selected elements.

With these commands in combination you can easily automatize boring tasks.
For instance, every time I work on my site's project, I open ST3, start my
development server, open Chrome, navigate to `localhost:8000`, type in
my credentials, and then I can start developing.

Right now I'm working on a macro utility for the plugin, that
will be available shortly. We need a special macro system,
because most of these commands are asynchronous, and hence don't
get along very well with the integrated Sublime macro system.


How to install
--------------

The recommended method is using [Sublime Package Control](https://sublime.wbond.net).
If you don't know, go check it out.

You can also [clone directly](https://github.com/apiad/sublime-browser-integration.git)
from Github, or download a [zip](https://github.com/apiad/sublime-browser-integration/archive/master.zip),
and unpack it in your Sublime Text 3 packages folder. If you don't know how to do
this, you definitely need the Package Control plugin.

Besides that, you need a recent version of Chrome (31 or greater) and the
[Chrome WebDriver](http://chromedriver.storage.googleapis.com/index.html)
executable in your path (in Linux you can drop it in `/usr/bin/`).


How does it work?
-----------------

The plugin ships with a modified version of
[selenium for Python](https://pypi.python.org/pypi/selenium),
which does the browser controlling magic. That and a few handy JavaScript
and Python gets the work done.


What's next?
------------

We are working on a few exciting new features:

* Automatic reload on save.
* Live CSS editing.
* Live highlight of selected jQuery selectors.
* Macro recording and playing.
* And many more...


Collaborating
-------------

Sure, come to [Github](https://github.com/apiad/sublime-browser-integration).
