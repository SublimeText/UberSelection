import re
import sublime
import selection
import decorators

def compute_flags(textFlags):
    flags = 0
    flags |= re.IGNORECASE
    flags ^= re.IGNORECASE if "c" in textFlags else 0
    return flags


@decorators.runFirst("split_selection_into_lines")
def exclude(view, what, flags):
    for r in reversed(view.sel()):
        if re.search("%s" % what, view.substr(r), compute_flags(flags)):
            view.sel().subtract(r)

    view.show(view.sel())


@decorators.runFirst("split_selection_into_lines")
def include(view, what, flags):
    for r in reversed(view.sel()):
        if not re.search("%s" % what, view.substr(r), compute_flags(flags)):
            view.sel().subtract(r)

    view.show(view.sel())


@decorators.runFirst("split_selection_into_lines")
def replace(view, edit, what, with_this):
    edit = view.begin_edit()
    try:
        for r in view.sel():
            view.replace(edit, r, re.sub(what, with_this, view.substr(r)))
    finally:
        view.end_edit(edit)
