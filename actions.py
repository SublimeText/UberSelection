import re

def exclude(view, what):
    view.runCommand("splitSelectionIntoLines")
    for r in reversed(view.sel()):
        if re.match("%s" % what, view.substr(r)):
            view.sel().subtract(r)

def replace(view, what, with_this):
    view.runCommand("splitSelectionIntoLines")
    for r in view.sel():
        view.replace(r, re.sub(what, with_this, view.substr(r)))
