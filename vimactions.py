import sublime
import decorators

def unknownCommand(cmd):
    sublime.status_message("UBERSELECTION (vim) -- Command unknown: %s" % cmd)

def saveBuffer(view, *args):
    cmd = "save" if not args else "save_as"
    view.window().run_command(cmd)

def saveBufferAll(view):
    view.window().run_command("save_all")

def saveBufferAndExit(view):
    saveBuffer(view)
    exitSublime(view)

def editFile(view):
    view.window().run_command("open_file_in_project")

def exitSublime(view):
    view.window().run_command("exit")

def nextViewInStack(view):
    view.window().run_command("next_view_in_stack")

def previousViewInStack(view):
    view.window().run_command("prev_view_in_stack")

def promptSelectFile(view):
    view.window().run_command("prompt_select_file")

def dispatch(view, cmd, *args):
    try:
        CMDS["simple"][cmd](view, *args)
    except KeyError:
        unknownCommand(cmd)


CMDS = {
     "simple": {
        "wall": saveBufferAll,
        "w": saveBuffer,
        "wq": saveBufferAndExit,
        "ZZ": saveBufferAndExit,
        "e": editFile,
        "q": exitSublime,
        "n": nextViewInStack,
        "N": previousViewInStack,
        "ls": promptSelectFile,
    },
}
