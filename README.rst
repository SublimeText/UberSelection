=============
Uberselection
=============

Make complex selections and replace text in a buffer via textual commands.
Inspired in Vim's line-oriented ex mode.


Getting Started
===============

* Install `AAAPackageDev`_ (dependency)
* Install `UberSelection`_

.. _AAAPackageDev: https://bitbucket.org/guillermooo/uberselection/downloads/UberSelection.sublime-package
.. _UberSelection: https://bitbucket.org/guillermooo/uberselection/downloads/UberSelection.sublime-package

If you're running a full installation, simply doubleclick on the `.sublime-package` files.
If you're running a portable installation, perform an `installation by hand`_.

.. _installation by hand: http://sublimetext.info/docs/extensibility/packages.html#installation-of-packages-with-sublime-package-archives

Usage
=====

#. Run from Sublime's console with ``view.run_command("uber_selection")``
#. Issue command as explained further below

Examples
========

``10,20V/this/``
    Select lines containing ``this`` between lines 10 and 20 (inclusive).

``.,.+20-V/this/``
    Select lines **not** containing ``this`` from the current line to 20 lines down
    from it.

``%s/this/that/``
    Replace ``this`` with ``that`` in the whole file.

Four Ways of Issuing Commands
=============================

#. ``<SUBLIME COMMAND>[ <ARG>]``
#. ``<LINE REF>[,<LINE REF>]``
#. ``<BUFFER COMMAND>[;<BUFFER COMMAND>]*``
#. ``<LINE REF><BUFFER COMMAND>[;<BUFFER COMMAND>]*``

All tokens are explained in the following sections

Tokens
======

Sublime Commands
****************

(Not all commands work.)

``w [arg]``
    Save the active buffer. If you pass an arg to it, the Save As dialog will
    show up. At the moment, the passed arg is ignored.
``wall``
    Save all opened buffers.
``wq``
    Save the active buffer and exit.
``ZZ``
    Save the active buffer and exit.
``ls``
    Show list of opened views.
``e``
    Show list of files in current directory.
``q``
    Exit.
``n``
    Next view.
``N``
    Previous view.

Line References
***************

Select lines or ranges of lines in the active view.

``[1-9]+``
    Designates line by number.

``.``
    Desigates the current line (first cursor in selection).

``$``
    Designates the last line in the view.

``%``
    Designates all lines in the view.

``/what/``
    Looks forwards to find first line matching ``what`` or returns current line
    if none found.

``?what?``
    Looks backwards to find first line matching ``what`` or returns current
    line if none found.

You can also specify offsets with ``[+-][1-9]+``.

In order to designate a range, use two comma separated line references::

    .+5,/end$/-3

Text Commands
*************

Select lines and perform replacements in the view.

``V/what/<flags>``
    Selects all lines containing ``what``. Case insensitive by default. Use the
    flag ``c`` to make a case-sensitive search.

``-V/what/<flags>``
    Same as above, but excludes the lines matching ``what``.

``s/what/with/``
    Replaces all instances of ``what`` with ``with``. Case sensitive.
    The separator ``/`` can be substituted by any of: ``! $ % & = / : ;``

You can chain commands by separating them with a semicolon (``;``)::

    .+5,/end$/-3V/foo/;-V/bar/;s/foo/BOO!/