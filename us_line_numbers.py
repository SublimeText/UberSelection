import re
import sublime, sublimeplugin
import functools


class UberselectionCompassCommand(sublimeplugin.TextCommand):
    def run(self, view, args):
        print getattr(self, args[0], False)(view)

    def getLastLineNr(self, view):
        return view.rowcol(view.size())[0] + 1

    def getCurrentLineNr(self, view):
        view.runCommand("singleSelection")
        return view.rowcol(view.sel()[0].begin())[0] + 1


def getLastLine():
    """
    Get last line in buffer.
    """
    return 10

def getCurrentLineNr():
    """
    Get current line from Sublime Text.
    """
    return 5

def searchForward(what):
    """
    Find first occurrence of `what` searching forward
    and return the line numnber.
    """
    return 20

def simpleRange(a):
    return int(a)

def getOffset(offset=[]):
    return int("".join(offset)) if offset else 0

def getMainAction(raw_action=[]):
    """
    Returns a callable to calculate a line number and
    the necessary arguments for the call.
    """

    ACTIONS = {
        r"^\.$": (getCurrentLineNr, ()),
        r"^\d+$": (simpleRange, (raw_action[0],)),
        r"^/$": (searchForward, (raw_action[1],)),
        r"^\$$": (getLastLine, ()),
    }

    for k, v in ACTIONS.iteritems():
        if re.match(k, raw_action[0]):
            return v

def parseRange(r):
    action, arg = getMainAction(r)
    offset = getOffset(r[-1])
    return tuple([action, offset, arg])

def calculateRange(parsedRange):
    return parsedRange[0](*parsedRange[2])

def getLineNr(raw_r):
    parsedRange = parseRange(raw_r)
    calculatedRange = calculateRange(parsedRange)
    return int(calculatedRange) + int(parsedRange[1])

def getLineNrs(a, b):
    return getLineNr(a), getLineNr(b)

if __name__ == "__main__":
    a = ["10", []]
    aa = ["100", ["+", "10"]]
    b = [".", []]
    c = [".", ["+", "10"]]
    d = ["/", "what", "/", ["-", "10"]]
    print getLineNr(aa)
    print getLineNr(a)
    print getLineNr(b)
    print getLineNr(c)
    print getLineNr(d)
    print getLineNrs(aa, d)
