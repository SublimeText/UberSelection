import re
import sublime
import selection
import sublimeplugin
import decorators

def computeFlags(textFlags):
    flags = 0
    flags |= re.IGNORECASE
    flags ^= re.IGNORECASE if "c" in textFlags else 0
    return flags

@decorators.runFirst("splitSelectionIntoLines")
def exclude(view, what, flags):
    for r in reversed(view.sel()):
        if re.search("%s" % what, view.substr(r), computeFlags(flags)):
            view.sel().subtract(r)

    view.show(view.sel())

@decorators.runFirst("splitSelectionIntoLines")
def include(view, what, flags):
    for r in reversed(view.sel()):
        if not re.search("%s" % what, view.substr(r), computeFlags(flags)):
            view.sel().subtract(r)

    view.show(view.sel())

@decorators.asTextCommand
@decorators.runFirst("splitSelectionIntoLines")
def replace(view, what, with_this):
    for r in view.sel():
        view.replace(r, re.sub(what, with_this, view.substr(r)))
