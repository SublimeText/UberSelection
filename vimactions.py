import sublime
import decorators


def unknownCommand(cmd):
    sublime.statusMessage("UBERSELECTION (vim) -- Command unknown: %s" % cmd)

def saveBuffer(view):
    view.window().runCommand("save")

def saveBufferAll(view):
    view.window().runCommand("saveAll")

def saveBufferAndExit(view):
    saveBuffer(view)
    sublime.statusMessage("Should exit now...")

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
