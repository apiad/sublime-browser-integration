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

    window.biMacros.eventHandler = function (evt) {
        if (!localStorage.__bi_tracking_events) return;

        var counter = Number(localStorage.__bi_counter);
        localStorage.__bi_counter = counter + 1;

        var time = + new Date();
        var delay = time - Number(localStorage['__bi_event_time'])

        var eventData = {
            type: evt.type,
            x: evt.offsetX,
            y: evt.offsetY,
            btn: evt.which,
            altKey: evt.altKey,
            metaKey: evt.metaKey,
            ctrlKey: evt.ctrlKey,
            shiftKey: evt.shiftKey,
            keyCode: evt.keyCode,
            charCode: evt.charCode,
            which: evt.which,
            delay: delay,
            idx: counter,
            el: window.biMacros.createXPathFromElement(evt.target),
        }

        localStorage['__bi_event_' + counter] = JSON.stringify(eventData);
        localStorage['__bi_event_time'] = time;
    }

    document.addEventListener('mousedown', window.biMacros.eventHandler);
    document.addEventListener('mouseup', window.biMacros.eventHandler);
    document.addEventListener('keypress', window.biMacros.eventHandler);
}
"""


@async
def inject_browser_macros_js():
    while True:
        if browser.connected() and browser.recording:
            browser.execute(browser_macros_js)
        else:
            return

        time.sleep(0.1)
