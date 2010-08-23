import sublime, sublimeplugin
import functools
import re


# My own stuff
import us_range_parser
import us_line_numbers
import us_commands
import selections
import actions

def parseRange(r):
    parsed = us_range_parser.parse(r).range
    if not parsed[1]:
        parsed[1] = parsed[0]

    return us_line_numbers.getLineNrs(parsed[0], parsed[1])


class UberSelectionCommand(sublimeplugin.TextCommand):
    def run(self, view, args):
        self.showInputPanel(view)

    def showInputPanel(self, view):
        view.window().showInputPanel("Uberselection",
                                        getattr(self, "lastCmdLine", ""),
                                        functools.partial(self.onDone, view),
                                        functools.partial(self.onChange, view),
                                        None
                                    )

    def onChange(self, view, s):
        pass

    def onDone(self, view, s):
        r = parseRange(s)
        self.lastCmdLine = s
        selections.selectSpanningLines(r, view)
        rrr = us_range_parser.parse(s).cmds
        if rrr:
            for the_cmd in rrr:
                parsed_cmd = us_commands.parse(the_cmd)
                if not parsed_cmd: break
                print parsed_cmd
                if parsed_cmd[0] == "-":
                    print ("%s" % (str(parsed_cmd)))
                    actions.exclude(view, parsed_cmd[1])
                if parsed_cmd[0] == "rep":
                    actions.replace(view, parsed_cmd[1], parsed_cmd[2])

        self.showInputPanel(view)
