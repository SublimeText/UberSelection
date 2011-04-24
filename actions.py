import re
import sublime
import selection
import decorators

from sublime_lib.view import in_one_edit

def compute_flags(text_flags):
    flags = 0
    flags |= re.IGNORECASE
    flags ^= re.IGNORECASE if "c" in text_flags else 0
    return flags


@decorators.run_first("split_selection_into_lines")
def exclude(view, what, flags):
    for r in reversed(view.sel()):
        if re.search("%s" % what, view.substr(r), compute_flags(flags)):
            view.sel().subtract(r)
    view.show(view.sel())


@decorators.run_first("split_selection_into_lines")
def include(view, what, flags):
    for r in reversed(view.sel()):
        if not re.search("%s" % what, view.substr(r), compute_flags(flags)):
            view.sel().subtract(r)
    view.show(view.sel())


@decorators.run_first("split_selection_into_lines")
def replace(view, what, with_this):
    with in_one_edit(view) as edit:
        for r in view.sel():
            view.replace(edit, r, re.sub(what, with_this, view.substr(r)))