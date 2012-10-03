#console.log 'Base....'
window.log = () ->
    if window.console
        try
            log_line = Array.prototype.slice.call arguments
        catch ex
            log 'Error in console', ex
        console.log log_line

window.document.onselectstart = (ev) ->
    false
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
