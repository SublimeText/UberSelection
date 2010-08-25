import sublime, sublimeplugin
import functools
import re

# My own modules
import us_range_parser
import us_line_numbers
import us_commands
import selections
import actions

_PACKAGE_NAME = "Uberselection"

def parseRange(r):

    parsed = us_range_parser.parse(r)

    simple_cmd = parsed.cmd
    rng = parsed.range
    commands = us_range_parser.parse(r).cmds

    # FIXME: if not rng1 is None
    lineNos = None
    if rng:
        if not rng[1]:
            rng[1] = rng[0]
        lineNos = us_line_numbers.getLineNrs(rng[0], rng[1])

    return simple_cmd, lineNos, commands


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
        simple_cmd, rng, cmds = parseRange(s)
        self.lastCmdLine = s

        if simple_cmd:
            actions.dispatch(simple_cmd, view)
        else:
            selections.selectSpanningLines(rng, view)

            for cmd in cmds:
                parsed_cmd = us_commands.parse(cmd)
                if not parsed_cmd: break
                if parsed_cmd[0] == "-":
                    actions.exclude(view, parsed_cmd[1])
                if parsed_cmd[0] == "rep":
                    actions.replace(view, parsed_cmd[1], parsed_cmd[2])
            self.showInputPanel(view)
