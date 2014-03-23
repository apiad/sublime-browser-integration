from .browser_integration import *


get_dom_tree_js = """
    var allNodes = document.getElementsByTagName('*');

    function createXPathFromElement(elm) {
        for (segs = []; elm && elm.nodeType == 1; elm = elm.parentNode)
        {
            if (elm.hasAttribute('id')) {
                    var uniqueIdCount = 0;
                    for (var n=0;n < allNodes.length;n++) {
                        if (allNodes[n].hasAttribute('id') &&
                            allNodes[n].id == elm.id)
                            uniqueIdCount++;
                        if (uniqueIdCount > 1) break;
                    };
                    if (uniqueIdCount == 1) {
                        segs.unshift('id("' + elm.getAttribute('id') + '")');
                        return segs.join('/');
                    } else {
                        segs.unshift(elm.localName.toLowerCase() +
                            '[@id="' + elm.getAttribute('id') + '"]');
                    }
            } else if (elm.hasAttribute('class')) {
                segs.unshift(elm.localName.toLowerCase() +
                    '[@class="' + elm.getAttribute('class') + '"]');
            } else {
                for (i = 1, sib = elm.previousSibling; sib;
                     sib = sib.previousSibling) {
                    if (sib.localName == elm.localName)  i++; };
                    segs.unshift(elm.localName.toLowerCase() + '[' + i + ']');
            };
        };

        return segs.length ? '/' + segs.join('/') : null;
    };

    function getName(el) {
        result = el.tagName.toLowerCase();

        if (!!el.id) {
            result += "#" + el.id;
        }

        if (!!el.className)  {
            result += "." + el.className.split(/\s/).join(".");
        }

        return result;
    }

    var ignore = ['SCRIPT', 'STYLE'];

    function getChildren(el) {
        var result = [];
        var children = el.children;

        for (var i=0; i < children.length; i++) {
            if (ignore.indexOf(children[i].tagName) >= 0) {
                continue;
            }

            result.push({
                'tag': getName(children[i]),
                'children': getChildren(children[i]),
                'xpath': createXPathFromElement(children[i]),
            });
        }

        return result;
    }

    return getChildren(document.body);
"""


class BrowserIntegrationSelectintCommand(sublime_plugin.WindowCommand):
    plugin_name = "Select elements (interactive)"
    plugin_description = "Opens a tree view of the DOM to select an element."

    @async
    @require_browser
    def run(self):
        dom_tree = browser.execute(get_dom_tree_js)

        def on_done(items, parent=None):
            @async
            def select(i):
                if i < 0:
                    return

                if i == 0 and parent:
                    child = parent
                    children = [el['tag'] for el in parent['children']]
                else:
                    if parent:
                        child = items[i-1]
                    else:
                        child = items[i]

                    children = [el['tag'] for el in child['children']]

                if children:
                    if parent is not None:
                        children = ['..'] + children

                    self.items = child['children']
                    self.window.show_quick_panel(children,
                                                 on_done(child['children'],
                                                 None), 0, 0, self.highlight)

            return select

        self.items = dom_tree
        self.window.show_quick_panel([el['tag'] for el in dom_tree],
                                     on_done(dom_tree), 0, 0, self.highlight)

    @async
    @require_browser
    def highlight(self, i):
        selector = self.items[i]['xpath']
        browser.select_xpath(selector)
