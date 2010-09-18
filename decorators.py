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
            return func(*args, **kwargs)
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
