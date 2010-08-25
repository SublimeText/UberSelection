import re
import sublime


def dispatch(cmd, *args):
    CMDS["simple_cmds"][cmd](*args)

def exclude(view, what):
    view.runCommand("splitSelectionIntoLines")
    for r in reversed(view.sel()):
        if re.match("%s" % what, view.substr(r)):
            view.sel().subtract(r)

def replace(view, what, with_this):
    view.runCommand("splitSelectionIntoLines")
    for r in view.sel():
        view.replace(r, re.sub(what, with_this, view.substr(r)))


def saveBuffer(view):
    view.runCommand("save")
    sublime.statusMessage("Saved %s" % view.fileName())

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
