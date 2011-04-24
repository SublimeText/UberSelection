def run_first(*cmd):
    """I take any number of view commands and run them before calling the
    decorated function.

    Requirements:

        The decorated func's first arg must be a view instance.

    Example:

        @run_first("split_selection_into_lines")
        def my_func(view, blah):
            ...
    """
    def catch_decorated_func(func):
        def new_func(*args, **kwargs):
            try:
                for c in cmd:
                    args[0].run_command(c)
            except AttributeError:
                print "run_first decorator got bad arg."
            return func(*args, **kwargs)
        return new_func
    return catch_decorated_func
