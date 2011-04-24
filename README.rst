Uberselection
=============

- Description_
- `Getting Started`_
- Examples_
- `Four ways to issue commands`_
- Tokens_
    - `Sublime commands`_
    - `Line references`_
    - `Text commands`_

Description
***********
Make complex selections and replace text in a buffer via text commands.
Inspired in Vim's ex mode.

Getting Started
***************

Download and install the `latest release`_ of UberSelection.

Clone repository under ``sublime.packagesPath() + "\\Uberselection"``.

.. _latest release: https://bitbucket.org/guillermooo/uberselection/downloads/UberSelection.sublime-package

Install AAAPackageDev (dependency).

Usage
*****
#. Run from Sublime's console with ``view.runCommand("uberSelection")``.
#. Issue command as explained below.

Examples
********

``10,20V/this/``
    Select lines containing ``this`` between lines 10 and 20 (inclusive).

``.,.+20-V/this/``
    Select lines **not** containing ``this`` from the current line to 20 lines down
    from it.

``%s/this/that/``
    Replace ``this`` with ``that`` in the whole file.

Four ways to issue commands
***************************

1. ``<SUBLIME COMMAND>[ <ARG>]``
2. ``<LINE REF>[,<LINE REF>]``
3. ``<BUFFER COMMAND>[;<BUFFER COMMAND>]*``
4. ``<LINE REF><BUFFER COMMAND>[;<BUFFER COMMAND>]*``

All tokens are explained in the following sections

Tokens
******

Sublime commands
----------------

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


Line references
---------------

Designates lines or ranges of lines in the active view.

``[1-9]+``
    Designates line by number.

``.``
    Desigates the current line (first cursor in selection).

``$``
    Designates the last line in the view.

``%``
    Designates all lines in the view.

You can also specify offsets with ``[+-][1-9]+``.

In order to designate a range, use two comma separated line references.

Text commands
-------------

Select lines and perform replacements in the view.

``V/what/<flags>``
    Selects all lines containing ``what``. Case insensitive by default. Use the
    flag ``c`` to make a case-sensitive search. By default, searches are case
    insensitive.

``-V/what/<flags>``
    Same as above, but excludes the lines matching ``what``.

``s/what/with/``
    Replaces all instances of ``what`` with ``with``.
    The separator ``/`` can be any of: ``! $ % & = / : ;``

You can chain commands by separating them with a semicolon (``;``).
