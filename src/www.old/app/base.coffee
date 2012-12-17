#console.log 'Base....'
window.log = () ->
    if window.console
        try
            log_line = Array.prototype.slice.call arguments
        catch ex
            log 'Error in console', ex
        console.log log_line

nodeCanSelect = (el) ->
    if el.className and typeof(className) == 'string' and el.className.match('canselect')
        return true
    else
        if el.parentNode
            #log 'onselectstart:', el
            return nodeCanSelect(el.parentNode)
        else
            #log 'onselectstart:', el
            return false
    #if ev.target.getAttribute and ev.target.getAttribute('canselect')

window.document.onselectstart = (ev) ->
    #log 'window.document.onselectstart', ev
    if nodeCanSelect(ev.target)
        return true
    else
        return false
"""
    #log('this', ev.target.getAttribute, ev.target.getAttribute('contenteditable'), ev.target.parentNode, ev.target.parentNode.getAttribute('contenteditable'));
    ###if(
        (config.tab == 1) ||
        (ev.target.getAttribute && ev.target.getAttribute('contenteditable')) ||
        (ev.target.parentNode && ev.target.parentNode.getAttribute('contenteditable')!=null)
    ) {
        #log('true');
        return true;
    }
    return false;
}
# Запретим выделение (внимание решение может быть не кроссбраузерно)
#log 'Test', 'log', window.log
"""
