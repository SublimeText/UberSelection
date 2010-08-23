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
    rng = parsed.range
    commands = us_range_parser.parse(r).cmds
    # FIXME: if not rng1 is None
    if not rng[1]:
        rng[1] = rng[0]

    return us_line_numbers.getLineNrs(rng[0], rng[1]), commands


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
        rng, cmds = parseRange(s)
        self.lastCmdLine = s
        selections.selectSpanningLines(rng, view)

        for cmd in cmds:
            parsed_cmd = us_commands.parse(cmd)
            if not parsed_cmd: break
            if parsed_cmd[0] == "-":
                actions.exclude(view, parsed_cmd[1])
            if parsed_cmd[0] == "rep":
                actions.replace(view, parsed_cmd[1], parsed_cmd[2])

        self.showInputPanel(view)
