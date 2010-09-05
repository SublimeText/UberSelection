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
    startPoint, endPoint = findLine(view, target=min(lines)), view.line(findLine(view, target=max(lines))).end()

    view.sel().clear()
    view.sel().add(sublime.Region(startPoint, endPoint))
