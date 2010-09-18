import sublime
import decorators

def dispatch(view, cmd, *args):
    try:
        CMDS["simple_cmds"][cmd](view, *args)
    except KeyError:
        unknownCommand(cmd)

def unknownCommand(cmd):
    sublime.statusMessage("UBERSELECTION (vim) -- Command unknown: %s" % cmd)

def saveBuffer(view):
    view.window().runCommand("save")

def editFile(view):
    view.window().runCommand("openFileInProject")

def exitSublime(view):
    view.window().runCommand("exit")

def nextViewInStack(view):
    view.window().runCommand("nextViewInStack")

def previousViewInStack(view):
    view.window().runCommand("prevViewInStack")

def promptSelectFile(view):
    view.window().runCommand("promptSelectFile")

CMDS = {
     "simple_cmds": {
        "w": saveBuffer,
        "e": editFile,
        "q": exitSublime,
        "n": nextViewInStack,
        "N": previousViewInStack,
        "ls": promptSelectFile,
    },
}
