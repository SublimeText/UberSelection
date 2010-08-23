import sublime, sublimeplugin
import functools
import us_range_parser
import us_line_numbers
import us_commands
import re

def parseRange(r):
    parsed = us_range_parser.parse(r).range
    if not parsed[1]:
        parsed[1] = parsed[0]

    return us_line_numbers.getLineNrs(parsed[0], parsed[1])


def move(view, backward=False, amount=1):
    """
    Wrapper around built-in command `move`. A bug in Sublime seems to prevent
    usi
    ng this command with amounts larger than 1.
    """
    if amount > 750: amount = 0
    if not amount == 0:
        for time in range(amount):
            view.runCommand('move lines', [str(1 if not backward else -1)])


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
        self.select(r, view)
        rrr = us_range_parser.parse(s).cmds
        if rrr:
            for the_cmd in rrr:
                parsed_cmd = us_commands.parse(the_cmd)
                if not parsed_cmd: break
                print parsed_cmd
                if parsed_cmd[0] == "-":
                    print ("%s" % (str(parsed_cmd)))
                    exclude(view, parsed_cmd[1])
                if parsed_cmd[0] == "rep":
                    replace(view, parsed_cmd[1], parsed_cmd[2])

        self.showInputPanel(view)

    def select(self, lines, view):
        self.resetSel(view)
        startOffset, endOffset = min(lines) - 1, max(lines)
        # TODO: Report bug: move lines 0 moves the cursor
        move(view, amount=startOffset)
        startPoint = view.sel()[0].begin()

        self.resetSel(view)
        move(view, amount=endOffset)
        endPoint = view.sel()[0].begin()

        view.sel().clear()
        view.sel().add(sublime.Region(startPoint, endPoint))

    def resetSel(self, view, default=(0, 0)):
        """
        Clears the selected regions and adds the `default` region to the
        selection.
        """
        view.sel().clear()
        view.sel().add(sublime.Region(*default))


def exclude(view, what):
    view.runCommand("splitSelectionIntoLines")
    for r in reversed(view.sel()):
        # if what.lower() in view.substr(r):
        #     view.sel().subtract(r)
        if re.match("%s" % what, view.substr(r)):
            view.sel().subtract(r)

def replace(view, what, with_this):
    view.runCommand("splitSelectionIntoLines")
    for r in view.sel():
        view.replace(r, re.sub(what, with_this, view.substr(r)))
