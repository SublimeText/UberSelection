import sublime
from location import findLine


def resetSels(view, default=(0, 0)):
    """
    Clears the selected regions and adds the `default` region to the
    selection.
    """
    # TODO: make a decorator @resettingSels
    view.sel().clear()
    view.sel().add(sublime.Region(*default))

def selectSpanningLines(lines, view):
    """Selects from lines[0].begin() to lines[1].end()
    """
    firstLine, lastLine = findLine(view, target=min(lines)), findLine(view, target=max(lines))
    # Default to last line if we request line greater than buffer line count.
    if lastLine == -1: lastLine = view.fullLine(view.size())
    view.sel().clear()
    view.sel().add(sublime.Region(firstLine.begin(), lastLine.end()))
    view.show(view.sel()[0].begin())