import sublime, sublimeplugin
import functools
import re

import selection
import actions
import grammar
import pyparsing

_PACKAGE_NAME = "Uberselection"

class UberSelectionCommand(sublimeplugin.TextCommand):
    """Executes vim ex-mode like commands.
    """
    def __init__(self):
        self.grammar = grammar.generate()

    def run(self, view, args):
        self.showInputPanel(view)

    def showInputPanel(self, view):
        view.window().showInputPanel("Uberselection CMD", getattr(self, 'lastCmdLine', ''),
                                        functools.partial(self.onDone, view), None, None)

    def onDone(self, view, s):

        try:
            tokens = self.grammar.parseString(s)
            vim_cmd, trans = tokens.vim_cmd, tokens.trans
        except pyparsing.ParseException:
            sublime.statusMessage("Uberselection: Error parsing command string.")
            return
        finally:
            self.lastCmdLine = s

        if vim_cmd:
            # TODO vim_cmd is a list!!
            actions.dispatch(vim_cmd[0], view)

        if trans:
            aRange, cmds = trans.range, trans.operator
            if any([aRange, cmds]):
                selection.selectSpanningLines(grammar.parseRange(aRange), view)

                for cmd in cmds:
                    if ''.join(cmd.command) == '-V':
                        actions.exclude(view, cmd)
                    if ''.join(cmd.command) == 'V':
                        actions.include(view, cmd)
                    if ''.join(cmd.command) == 's':
                        view.runCommand("uberSelectionReplace", [cmd.search[0], cmd.replace[0]])

            self.showInputPanel(view)


class UberSelectionReplace(sublimeplugin.TextCommand):
    def run(self, view, args):
        actions.replace(view, args[0], args[1])
