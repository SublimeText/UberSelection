import sublime

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
            return find_line(view, guessed_pos, end, target)
        else:
            return find_line(view, start, guessed_pos, target)


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
