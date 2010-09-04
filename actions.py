import re
import sublime

def dispatch(cmd, *args):
    if cmd in CMDS["simple_cmds"].keys():
        CMDS["simple_cmds"][cmd](*args)
    else:
        unknownCommand()

def exclude(view, cmd):
    view.runCommand("splitSelectionIntoLines")
    what = cmd.argument[0]
    flags = 0
    flags |= re.IGNORECASE if "i" in list(cmd.flags) else 0

    for r in reversed(view.sel()):
        if re.search("%s" % what, view.substr(r), flags):
            view.sel().subtract(r)

def include(view, cmd):
    view.runCommand("splitSelectionIntoLines")
    what = cmd.argument[0]
    flags = 0
    flags |= re.IGNORECASE if "i" in list(cmd.flags) else 0
    for r in reversed(view.sel()):
        if not re.search("%s" % what, view.substr(r), flags):
            view.sel().subtract(r)

def replace(view, what, with_this):
    view.runCommand("splitSelectionIntoLines")
    for r in view.sel():
        view.replace(r, re.sub(what, with_this, view.substr(r)))

def unknownCommand():
    sublime.statusMessage("Command unknown.")

def saveBuffer(view):
    # view.runCommand("save")
    # sublime.statusMessage("Saved %s" % view.fileName())
    sublime.statusMessage("Not implemented. (FILE NOT SAVED!)")

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
