import sublime
import re

def getLineNr(view, point):
    return view.rowcol(point)[0] + 1

def getEOL(view, point):
    return view.line(point).end()

def getBOL(view, point):
    return view.line(point).begin()

def findLine(view, start=0, end=-1, target=0):
    """Performs binary search to locate `target` line number.
    Returns `Region` comprising line no. `target` or -1 if can't find `target`.
    """
    if  target < 0 or target > view.size():
        return -1

    if end == -1: end = view.size()

    lo, hi = start, end
    while lo <= hi:
        middle = lo + (hi - lo) / 2
        if getLineNr(view, middle) < target:
            lo = getEOL(view, middle) + 1
        elif getLineNr(view, middle) > target:
            hi = getBOL(view, middle) - 1
        else:
            return view.fullLine(middle)
    return -1

def search(what, backward=False):
    view = sublime.activeWindow().activeView()

    if not backward:
        reg = view.find(what, view.sel()[0].begin())
        if not reg is None:
            row = (view.rowcol(reg.begin())[0] + 1)
        else:
            row = calculateRelativeRef('.')

        return row

    else:
        sublime.statusMessage("Performing reverse search (this could take a while)...")
        currLine = calculateRelativeRef('.') - 1
        bkup = view.sel()[0]

        while currLine > 0:
            if re.search(what, view.substr(view.line(view.sel()[0].begin()))):
                view.sel().clear()
                view.sel().add(bkup)
                return currLine + 1

            view.runCommand('move', ['lines', '-1'])
            currLine -= 1

        return view.rowcol(bkup.begin())[0] + 1

def calculateRelativeRef(where):
    view = sublime.activeWindow().activeView()
    if where == '$':
        return view.rowcol(view.size())[0] + 1
    if where == '.':
        return view.rowcol(view.sel()[0].begin())[0] + 1
