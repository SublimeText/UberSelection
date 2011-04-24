import sublime
from location import findLine


def select_spanning_lines(lines, view):
    """Selects from lines[0].begin() to lines[1].end()
    """
    first_line, last_line = findLine(view, target=min(lines)), findLine(view, target=max(lines))
    # Default to last line if we request line greater than buffer line count.
    if last_line == -1: last_line = view.fullLine(view.size())
    view.sel().clear()
    view.sel().add(sublime.Region(first_line.begin(), last_line.end()))
    view.show(view.sel()[0].begin())