import sublime
# import grammar
import re

def findLine(view, start=0, end=-1, target=0):
    """Performs a binary search to find line number `target`.

    Normally you should only specify your `target` line number.
    """
    if target == 0: return 0
    if target > view.rowcol(view.size())[0] + 1: return view.line(view.size()).begin()
    if end == -1: end = view.size()

    total_lines = (view.rowcol(end)[0] + 1)
    relative_target = target
    if start:
        total_lines = total_lines +1 - (view.rowcol(start)[0] + 1)
        relative_target = target + 1 - (view.rowcol(start)[0] + 1)

    guessed_pos = int((end - (start -1 if start > 0 else start)) * (relative_target / float(total_lines)) + start)

    if view.rowcol(guessed_pos)[0] + 1 == target:
        return view.line(guessed_pos).begin()
    else:
        if view.rowcol(guessed_pos)[0] + 1 < target:
            return findLine(view, guessed_pos, end, target)
        else:
            return findLine(view, start, guessed_pos, target)

def search(what, backward=False):
    view = sublime.activeWindow().activeView()

    if not backward:
        reg = view.find(what, view.sel()[0].begin())
        return (view.rowcol(reg.begin())[0] + 1) if reg else calculateRelativeRef('.')

    else:
        sublime.statusMessage("Uberselection: performing reverse search...")
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
