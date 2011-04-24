import sublime
import decorators


def unknown_command(cmd):
    sublime.status_message("UBERSELECTION (vim) -- Command unknown: %s" % cmd)


def save_buffer(view, *args):
    cmd = "save" if not args else "save_as"
    view.window().run_command(cmd)


def save_buffer_all(view):
    view.window().run_command("save_all")


def save_buffer_and_exit(view):
    save_buffer(view)
    exit_sublime(view)


def edit_file(view):
    view.window().run_command("open_file_in_project")


def exit_sublime(view):
    view.window().run_command("exit")


def next_view_in_stack(view):
    view.window().run_command("next_view_in_stack")


def previous_view_in_stack(view):
    view.window().run_command("prev_view_in_stack")


def prompt_select_file(view):
    view.window().run_command("prompt_select_file")


def dispatch(view, cmd, *args):
    try:
        CMDS["simple"][cmd](view, *args)
    except KeyError:
        unknown_command(cmd)


CMDS = {
     "simple": {
        "wall": save_buffer_all,
        "w": save_buffer,
        "wq": save_buffer_and_exit,
        "ZZ": save_buffer_and_exit,
        "e": edit_file,
        "q": exit_sublime,
        "n": next_view_in_stack,
        "N": previous_view_in_stack,
        "ls": prompt_select_file,
    },
}
