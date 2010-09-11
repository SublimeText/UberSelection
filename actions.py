import re
import sublime
import selection
import sublimeplugin

def runFirst(*cmd):
    """Takes any number of commands and runs them before calling the decorated
    function.

    Expects the first arg of decorated function to be a view instance.

    Example:

        @runFirst("splitSelectionIntoLines")
        def my_func(view, blah):
            ...
    """
    def catchDecoratedFunc(func):
        def newFunc(*args, **kwargs):
            try:
                for c in cmd:
                    args[0].runCommand(c)
            except AttributeError:
                print "runFirst decorator got bad arg."
                return
            func(*args, **kwargs)
        return newFunc
    return catchDecoratedFunc

def asTextCommand(f):
    """Decorator to run `f` through a TextCommand.run method. Useful to group
    buffer edits atomically so they can be undone in one go.

    Usage:
        `f` is expected to be passed a `view` instance as its first argument.
    """
    def runThruTextCommand(*args, **kwargs):
        i = sublimeplugin.textCommands["textCommandRunner"]
        i.prime(f, args, kwargs)
        args[0].runCommand("textCommandRunner")
    return runThruTextCommand

def dispatch(cmd, *args):
    if cmd in CMDS["simple_cmds"].keys():
        CMDS["simple_cmds"][cmd](*args)
    else:
        unknownCommand()

@runFirst("splitSelectionIntoLines")
def exclude(view, cmd):
    what = cmd[0]
    flags = 0
    flags |= re.IGNORECASE if "i" in cmd[1] else 0
    flags ^= re.IGNORECASE if "c" in cmd[1] else flags

    for r in reversed(view.sel()):
        if re.search("%s" % what, view.substr(r), flags):
            view.sel().subtract(r)

    view.show(view.sel())

@runFirst("splitSelectionIntoLines")
def include(view, cmd):
    what = cmd[0]
    flags = 0
    flags |= re.IGNORECASE if "i" in cmd[1] else 0
    flags ^= re.IGNORECASE if "c" in cmd[1] else flags

    for r in reversed(view.sel()):
        if not re.search("%s" % what, view.substr(r), flags):
            view.sel().subtract(r)

    view.show(view.sel())

@asTextCommand
@runFirst("splitSelectionIntoLines")
def replace(view, what, with_this):
    print what, with_this
    for r in view.sel():
        view.replace(r, re.sub(what, with_this, view.substr(r)))

def unknownCommand():
    sublime.statusMessage("Command unknown.")

def saveBuffer(view):
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
