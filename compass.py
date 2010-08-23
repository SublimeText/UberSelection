"""Where am I in a Sublime buffer?
"""

def lastLineNr(view):
    """Returns the last line number in view.
    """
    return view.rowcol(view.size())[0] + 1

def currentLine(view):
    """Returns the current line number after
    clearing all selections but the first one.
    """
    raise NotImplemented

def nextOccurrence(view, what, reverseSearch=False):
    """Returns the next occurrence of what in view.
    """
    raise NotImplemented
