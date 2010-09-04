import sublime

# TODO: add what=lines arg
def move(view, backward=False, amount=1):
    """Wrapper around built-in command `move`. A bug in Sublime seems to prevent
    using this command with amounts larger than 1.
    """
    if amount > 1000:
            sublime.errorMessage("Uberselection: Current limit for ranges is set to 1000.")
            amount = 0
    if not amount == 0:
        for time in range(amount):
            view.runCommand('move lines', [str(1 if not backward else -1)])


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
    resetSels(view)
    startOffset, endOffset = min(lines) - 1, max(lines)
    move(view, amount=startOffset)
    startPoint = view.sel()[0].begin()

    resetSels(view)
    move(view, amount=endOffset)
    endPoint = view.sel()[0].begin()

    view.sel().clear()
    view.sel().add(sublime.Region(startPoint, endPoint))
