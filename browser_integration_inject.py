from .browser_integration import *


browser_macros_js = """
if (!window.biMacros) {
    window.biMacros = {};

    window.biMacros.createXPathFromElement = function (elm) {
        var allNodes = document.getElementsByTagName('*');

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

    window.biMacros.lookupElementByXPath = function (path) {
        var evaluator = new XPathEvaluator();

        var result = evaluator.evaluate(path, document.documentElement,
            null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);

        return  result.singleNodeValue;
    }

    window.biMacros.eventHandler = function (evt) {
        if (!localStorage.__bi_tracking_events) return;

        var counter = Number(localStorage.__bi_counter);
        localStorage.__bi_counter = counter + 1;

        var eventData = {
            type: evt.type,
            x: evt.pageX,
            y: evt.pageY,
            btn: evt.which,
            altKey: evt.altKey,
            metaKey: evt.metaKey,
            ctrlKey: evt.ctrlKey,
            shiftKey: evt.shiftKey,
            idx: counter,
            el: window.biMacros.createXPathFromElement(evt.target),
        }

        localStorage['__bi_event_' + counter] = JSON.stringify(eventData);
    }

    document.addEventListener('click', window.biMacros.eventHandler);
    document.addEventListener('keyup', window.biMacros.eventHandler);
    document.addEventListener('keydown', window.biMacros.eventHandler);

    var meta = document.createElement('meta');
    meta.setAttribute('content', 'browser-integration');
    document.querySelector('head').appendChild(meta);
}
"""


@async
def inject_browser_macros_js():
    while True:
        if browser.connected():
            try:
                browser.find_element_by_css_selector(
                    'meta[content=browser-integration]')
            except:
                browser.execute(browser_macros_js)
                print("Injecting browser macros")

        time.sleep(0.1)


# inject_browser_macros_js()
