import pyparsing as p
import sublime
import re
import location

offset = p.Optional(p.Group(p.Word("+-", max=1) + p.Word(p.nums)))

number = p.Word(p.nums) + offset
anchor = p.Word(".$", max=1) + offset
range_op = p.QuotedString(quoteChar="/", escChar="\\", unquoteResults=False) + offset
range_op2 = p.QuotedString(quoteChar="?", escChar="\\", unquoteResults=False) + offset
the_range = p.delimitedList(p.Group(number) | p.Group(anchor) | p.Group(range_op) | p.Group(range_op2)) | "%"

# operators
selection = p.Group(p.Optional("-") + "V").setResultsName("command") + p.Group(p.QuotedString(quoteChar="/", escChar="\\")).setResultsName("argument") + p.Group(p.Optional(p.Word("iS"))).setResultsName("flags")

separator = p.Word(":;,=/\\&$!", max=1)
replacement = p.Literal("s").setResultsName("command") + separator + p.SkipTo(p.matchPreviousLiteral(separator), include=True).setResultsName("search") + p.SkipTo(p.matchPreviousLiteral(separator), include=True).setResultsName("replace")
operator = p.delimitedList(p.Group(selection | replacement), delim=";")

trans = p.Group(p.Optional(the_range)).setResultsName("range") + p.Group(operator).setResultsName("operator")
cmd = p.Word("weqnN") | "ls"
cmd = cmd + p.Optional(p.Word(p.alphas))

grammar = cmd.setResultsName("vim_cmd") | trans.setResultsName("trans")

def parseRange(the_range):
    """Returns a point (pos, pos) after parsing a range like these:

        10+10,/there/+1
        .,$
        %

       Note: The range is already tokenized.
    """

    if not the_range:
        the_range = (".",)

    try:
        a, b = the_range[0:2]

    except ValueError as e:
        a, b = the_range[0], the_range[0]
        if a == '%':
            a, b = '1', '$'

    finally:
        x, y = parseRangePart(a), parseRangePart(b)
        return x, y or x

def parseRangePart(part):
    mainPart = part[0]

    modif = 0
    if len(part) > 1:
        modif = int(''.join(part[1]))

    if mainPart.isdigit():
        return int(mainPart) + modif

    if mainPart in ('$', '.'):
        return location.calculateRelativeRef(mainPart) + modif

    if mainPart.startswith('/') or mainPart.startswith('?'):
        return location.search(mainPart[1:-1], mainPart.startswith('?')) + modif
