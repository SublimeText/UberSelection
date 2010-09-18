import sublimeplugin

def runFirst(*cmd):
    """I take any number of view commands and run them before calling the
    decorated function.

    Requirements:

        The decorated func's first arg must be a view instance.

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
            return func(*args, **kwargs)
        return newFunc
    return catchDecoratedFunc

def asTextCommand(f):
    """I run `f` through a TextCommand.run method. Useful to group buffer edits
    atomically.

    Requirements:

        A TextCommand called TextCommandRunnerCommand must exist and it must
        have a .prime() method.

        `f`'s first argument must be a view instance.

    Usage:

        @asTextCommand
        def do_something(view, x, y):
            view.replace(x, y)

    """
    def runThruTextCommand(*args, **kwargs):
        i = sublimeplugin.textCommands["textCommandRunner"]
        i.prime(f, args, kwargs)
        args[0].runCommand("textCommandRunner")
    return runThruTextCommand
