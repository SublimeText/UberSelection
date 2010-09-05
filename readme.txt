TODO: rewrite in reST

README

Examples:

10,20V/this/

Select lines containing "this" between lines 10 and 20 (inclusive).

10,20V/this/i

Same performing case insensitive search.

10,20-V/this/

Exclude lines containing "this".

Range anchors/operators:

% => all lines in the active view
. => current line in the active view.
$ => last line in the active view.
/what/ => next line containing "what"
?what? => previous line containing "what"

It is also possible to specify offsets.

Examples:

%V// => select all lines in the active view.
.+10V// => select tenth line down from the current selection (first cursor)
.-10V// => selection tenth line up from the current selection (frist cursor)
?^BIO HAZARD WARNING$?+1,/^END OF WARNING$/-1V// => select every line comprised between the marks (excluding the marks' lines)
.,$ => select all lines from current selection (first cursor) up to the end of the file (inclusive)

Transformation operators

V/what/ => add lines to selection if line matches what
-V/what/ => remove lines from selection if line matches what
s/what/repl/ => replace what with repl in every selected line

Transformation operators can be chained:

49,/Mobile/V/Windows/;-V/7/;s/Windows/WINDOZE/

Try the above here (place the cursor under this line, otherwise "Mobile" will match early):

    Windows 3.1
    Windows 98SE
    Wine: Windows on Linux
    Wine: Windows 7 on Linux
    Ubuntu
    Windows 98
    Windows 7
    Windows ME
    BSD
    Windows 7 Standard
    Windows Mobile