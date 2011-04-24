import sublime, sublime_plugin

import functools
import re

import selection
import location
import actions, vimactions
import newgrammar

import pyparsing


class UberSelectionCommand(sublime_plugin.TextCommand):
    """Executes vim ex-mode like commands.
    """
    grammar = newgrammar.generate_grammar()

    def run(self, edit, command=None):
        if not command:
            self.show_input_panel(edit)
        else:
            self.on_done(self.view, command)

    def show_input_panel(self, edit):
        self.view.window().show_input_panel(
                                "UberSelection:",
                                getattr(self, 'last_cmd_line', ''),
                                functools.partial(self.on_done, edit),
                                None, None)

    def on_done(self, edit, s):
        self.last_cmd_line = s
        try:
            tokens = self.grammar.parseString(s)
        except pyparsing.ParseException:
            sublime.status_message(
                            "[ERROR] UberSelection: Invalid command string.")
            return

        if tokens.vim_cmd:
            vimactions.dispatch(self.view,
                                tokens.vim_cmd[0], *tokens.vim_cmd[1])
            # Avoids showing input panel again.
            return

        elif tokens.complex_cmd:
            selection.select_spanning_lines(self.parseRange(tokens.complex_cmd.range),
                                            self.view)
            for cmd in tokens.complex_cmd:
                if cmd[0] == "V":
                    actions.include(self.view, cmd[1], cmd[2])
                if cmd[0] == "-V":
                    actions.exclude(self.view, cmd[1], cmd[2])
                if cmd[0] == "s":
                    actions.replace(self.view, cmd[2][0], cmd[3][0])
        elif tokens.range:
            selection.select_spanning_lines(self.parseRange(tokens.range), self.view)
        elif tokens.cmd:
            selection.select_spanning_lines(
                                self.parseRange(self.grammar.parseString(".").range),
                                self.view)
            for cmd in tokens.cmd:
                if cmd[0] == "s":
                    actions.replace(self.view, cmd[2][0], cmd[3][0])
        else:
            sublime.status_message("[ERROR] UberSelection: Unknown command.")

        self.show_input_panel(self.view)

    def parseRange(self, r):
        if r.all == "%":
            x, offset_x = "1", "0"
            y, offset_y = "$", "0"
        else:
            x, offset_x = r.a.value, r.a.offset
            y, offset_y = (x, offset_x) if not hasattr(r.b, "value") else (
                                                                        r.b.value,
                                                                        r.b.offset
                                                                        )
        return self.parseRangePart(x) + int(offset_x), self.parseRangePart(y) + int(offset_y)

    def parseRangePart(self, p):
        if p.isdigit():
            return int(p)
        # Order matters! This case can contain the next one with other semantics.
        if p.startswith('/') or p.startswith('?'):
            if p.startswith('?'):
                return location.reverse_search(self.view, p[1:-1],
                                                end=self.view.sel()[0].begin())
            return location.search(self.view, p[1:-1])
        if p in ('$', '.'):
            return location.calculate_relative_ref(p)
