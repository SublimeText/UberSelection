import sublime, sublimeplugin
import functools
import re

import selection
import location
import actions, vimactions
import newgrammar
import pyparsing

_PACKAGE_NAME = "Uberselection"

class UberSelectionCommand(sublimeplugin.TextCommand):
    """Executes vim ex-mode like commands.
    """
    def __init__(self):
        self.grammar = newgrammar.generate_grammar()

    def run(self, view, args):
        if not args:
            self.showInputPanel(view)
        else:
            self.onDone(view, args[0])

    def showInputPanel(self, view):
        view.window().showInputPanel("Uberselection CMD", getattr(self, 'lastCmdLine', ''),
                                        functools.partial(self.onDone, view), None, None)

    def onDone(self, view, s):

        self.lastCmdLine = s
        try:
            tokens = self.grammar.parseString(s)
        except pyparsing.ParseException:
            sublime.statusMessage("Uberselection: Invalid command string.")
            return

        if tokens.vim_cmd:
            vimactions.dispatch(view, tokens.vim_cmd[0], *tokens.vim_cmd[1])
            # Return now because we don't want to show input panel again.
            return

        elif tokens.complex_cmd:
            selection.selectSpanningLines(parseRange(tokens.complex_cmd.range), view)
            for cmd in tokens.complex_cmd:
                if cmd[0] == "V":
                    actions.include(view, cmd[1], cmd[2])
                if cmd[0] == "-V":
                    actions.exclude(view, cmd[1], cmd[2])
                if cmd[0] == "s":
                    actions.replace(view, cmd[2][0], cmd[3][0])
        elif tokens.range:
            selection.selectSpanningLines(parseRange(tokens.range), view)
        elif tokens.cmd:
            selection.selectSpanningLines(parseRange(self.grammar.parseString(".").range), view)
            for cmd in tokens.cmd:
                if cmd[0] == "s":
                    actions.replace(view, cmd[2][0], cmd[3][0])
        else:
            sublime.statusMessage("Uberselection: Unknown command.")


        self.showInputPanel(view)


def parseRange(r):
    if r.all == "%":
        x, offset_x = "1", "0"
        y, offset_y = "$", "0"
    else:
        x, offset_x = r.a.value, r.a.offset
        y, offset_y = (x, offset_x) if not hasattr(r.b, "value") else (r.b.value, r.b.offset)

    return parseRangePart(x) + int(offset_x), parseRangePart(y) + int(offset_y)

def parseRangePart(p):
    if p.isdigit():
        return int(p)
    if p in ('$', '.'):
        return location.calculateRelativeRef(p)
    if p.startswith('/') or p.startswith('?'):
        return location.search(p[1:-1], p.startswith('?'))


class TextCommandRunner(sublimeplugin.TextCommand):
    """Generic TextCommand to run delegates so that the modifications they
    perform to the buffer are grouped atomically.

    Example:
        i = sublimeplugin.textCommands['textCommandRunner']
        i.prime(delegate, args, kwargs)
        view.runCommand('textCommandRunner')

    This class is intended to be used from a decorator wrapping a function
    with a `view` instance as first argument.
    """
    def run(self, view, args):
        if not hasattr(self, 'f'): return
        self.f(*self.args, **self.kwargs)
        del self.f

    def prime(self, f, args, kwargs):
        self.f = f
        self.args = args
        self.kwargs = kwargs
