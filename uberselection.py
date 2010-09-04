import sublime, sublimeplugin
import functools
import re

# My own modules
import us_range_parser
import us_line_numbers
import us_commands
import selections
import actions
import grammar

_PACKAGE_NAME = "Uberselection"

class UberSelectionCommand(sublimeplugin.TextCommand):
    """Executes vim ex-mode like commands.
    """

    def run(self, view, args):
        self.showInputPanel(view)

    def showInputPanel(self, view):
        view.window().showInputPanel("Uberselection CMD",
                                        getattr(self, 'lastCmdLine', ''),
                                        functools.partial(self.onDone, view),
                                        None,
                                        None
                                    )

    def onDone(self, view, s):
        tokens = grammar.grammar.parseString(s)
        vim_cmd, trans = tokens.vim_cmd, tokens.trans

        self.lastCmdLine = s

        if vim_cmd:
            # TODO vim_cmd is a list!!
            actions.dispatch(vim_cmd[0], view)

        if trans:
            aRange, cmds = trans.range, trans.operator
            selections.selectSpanningLines(grammar.parseRange(aRange), view)

            for cmd in cmds:
                if "".join(cmd.command) == "-V":
                    actions.exclude(view, cmd)
                if "".join(cmd.command) == "V":
                    actions.include(view, cmd)
            self.showInputPanel(view)
