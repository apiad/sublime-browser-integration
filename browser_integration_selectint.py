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
    plugin_name = "Interactive Selection"
    plugin_description = "Opens a tree view of the DOM to select an element."

    @staticmethod
    def visible():
        return browser.connected()

    @async
    @require_browser
    def run(self):
        with loading("Creating DOM tree."):
            dom_tree = browser.execute(get_dom_tree_js)

        def build_subtree(tree, path=[], depth=0, curr=[]):
            result = []

            node = path.pop(0) if path else None

            for i, t in enumerate(tree):
                result.append(("    " * depth + t['tag'],
                               t['xpath'], curr + [i]))

                if i == node or len(tree) == 1:
                    result.extend(build_subtree(t['children'], path,
                                                depth + 1, curr + [i]))

            return result

        @async
        def select(i):
            if i < 0:
                return

            tag, xpath, path = self.items[i]
            self.items = build_subtree(dom_tree, path)

            self.window.show_quick_panel([x for x, y, z in self.items],
                                         select, 0, i, self.highlight)

        self.items = build_subtree(dom_tree)
        self.window.show_quick_panel([x for x, y, z in self.items],
                                     select, 0, 0, self.highlight)

    def highlight(self, i):
        selector = self.items[i][1]
        browser.select_xpath(selector)
