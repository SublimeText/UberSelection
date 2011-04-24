import sublime, sublime_plugin
import functools
import re

import selection
import location
import actions, vimactions
import newgrammar
import pyparsing

_PACKAGE_NAME = "Uberselection"

class UberSelectionCommand(sublime_plugin.TextCommand):
    """Executes vim ex-mode like commands.
    """
    grammar = newgrammar.generate_grammar()

    def run(self, edit, command=None):
        if not command:
            self.showInputPanel(edit)
        else:
            # XXX What's command?
            self.onDone(self.view, command)

    def showInputPanel(self, edit):
        self.view.window().show_input_panel("Uberselection CMD", getattr(self.view, 'lastCmdLine', ''),
                                        functools.partial(self.onDone, edit), None, None)

    def onDone(self, edit, s):

        self.lastCmdLine = s
        try:
            tokens = self.grammar.parseString(s)
        except pyparsing.ParseException:
            sublime.status_message("Uberselection: Invalid command string.")
            return

        if tokens.vim_cmd:
            vimactions.dispatch(self.view, tokens.vim_cmd[0], *tokens.vim_cmd[1])
            # Return now because we don't want to show input panel again.
            return

        elif tokens.complex_cmd:
            selection.selectSpanningLines(parseRange(tokens.complex_cmd.range), self.view)
            for cmd in tokens.complex_cmd:
                if cmd[0] == "V":
                    actions.include(self.view, cmd[1], cmd[2])
                if cmd[0] == "-V":
                    actions.exclude(self.view, cmd[1], cmd[2])
                if cmd[0] == "s":
                    actions.replace(self.view, edit, cmd[2][0], cmd[3][0])
        elif tokens.range:
            selection.selectSpanningLines(parseRange(tokens.range), self.view)
        elif tokens.cmd:
            selection.selectSpanningLines(parseRange(self.grammar.parseString(".").range), self.view)
            for cmd in tokens.cmd:
                if cmd[0] == "s":
                    actions.replace(self.view, cmd[2][0], cmd[3][0])
        else:
            sublime.status_message("Uberselection: Unknown command.")


        self.showInputPanel(self.view)


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
    # Order matters! This case can contain the next one with other semantics.
    if p.startswith('/') or p.startswith('?'):
        return location.search(p[1:-1], p.startswith('?'))
    if p in ('$', '.'):
        return location.calculateRelativeRef(p)


class TextCommandRunner(sublime_plugin.TextCommand):
    """Generic TextCommand to run delegates so that the modifications they
    perform to the buffer are grouped atomically.

    Example:
        i = sublime_plugin.textCommands['textCommandRunner']
        i.prime(delegate, args, kwargs)
        view.runCommand('textCommandRunner')

    This class is intended to be used from a decorator wrapping a function
    with a `view` instance as first argument.
    """
    def run(self, edit, args):
        if not hasattr(self, 'f'): return
        self.f(self.view, edit, *self.args[2:], **self.kwargs)
        del self.f

    def prime(self, f, args, kwargs):
        self.f = f
        self.args = args
        self.kwargs = kwargs
