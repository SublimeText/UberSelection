# In dev.
# Not in use.

import pyparsing as p

# Vim commands like: :e, :ls, etc.
vim_cmd_name = p.Word(p.alphanums)
vim_cmd_arg = p.Word(p.alphanums)
vim_cmd = vim_cmd_name + p.Optional(vim_cmd_arg)

# Range
offset = p.Word("+-", max=1) + p.Word(p.nums)
search_op = p.QuotedString(quoteChar="?", escChar="\\", unquoteResults=False) ^ p.QuotedString(quoteChar="/", escChar="\\", unquoteResults=False)
position = p.Word(p.nums) ^ p.Word("$.", max=1) ^ search_op
line_range = position.setResultsName("a") + p.Optional(offset).setResultsName("offset_a") + p.Optional("," + position.setResultsName("b") + p.Optional(offset).setResultsName("offset_b")) ^ "%"

# Cmd
flags = p.Word("i")
visual = p.Optional("-") + p.QuotedString(quoteChar="V/", escChar="\\", endQuoteChar="/", unquoteResults=False) + p.Optional(flags)
separator = p.Word(":;,=/\\&$!", max=1)
replacement = p.Literal("s") + separator + p.SkipTo(p.matchPreviousLiteral(separator), include=True).setResultsName("search") + p.SkipTo(p.matchPreviousLiteral(separator), include=True).setResultsName("replace") + p.Optional(flags).setResultsName("flags")
cmd = p.Group(p.delimitedList(p.Group(visual | replacement), delim=";"))
complex_cmd = line_range.setResultsName("range") + cmd.setResultsName("commands")

uberselection_syntax = vim_cmd.setResultsName("vim_cmd") ^ line_range.setResultsName("line_range") ^ cmd.setResultsName("cmd") ^ complex_cmd.setResultsName("complex_cmd")

# parse
# if tokens.vim_cmd: do_vim_cmd

if __name__ == "__main__":
    print "="*50
    print "Testing vim commands"
    print "="*50
    print vim_cmd.parseString("w"), ["w"]
    print vim_cmd.parseString("ls"), ["ls"]
    print vim_cmd.parseString("help"), ["help"]
    print vim_cmd.parseString("h topic"), ["h", "topic"]
    print "="*50
    print line_range.parseString("?hey?+10")
    print line_range.parseString("?hey?+10,$")
    print line_range.parseString("?hey?+10,/$/-100")
    x = line_range.parseString("/hey/+10")
    print x.a, "//", x.offset_a, "::", x.b, "//", x.offset_b
    print line_range.parseString("%")
    print "="*50
    print "Test complex cmd"
    print complex_cmd.parseString("10,20s/a/b/")
    print complex_cmd.parseString("10,20V/eco/;s/a/b/")
    print "="*50
    print "Test Uberselection syntax"
    print uberselection_syntax.parseString("10")
    print uberselection_syntax.parseString("10+20")
    print uberselection_syntax.parseString("10+20,10")
    print uberselection_syntax.parseString("10+20,10-5")
    print uberselection_syntax.parseString(".+20,$-5")
    print uberselection_syntax.parseString("/./+20,$-5")
    print uberselection_syntax.parseString("-V//")
    print uberselection_syntax.parseString("V//;-V/a/")
    print uberselection_syntax.parseString("10,20V//;-V/a/")
    print uberselection_syntax.parseString("w")
    x = uberselection_syntax.parseString("10+5,20V//;-V/a/")
    print "Range:", x.a, x.offset_a, x.b, x.offset_b, "Commands", x.complex_cmd.commands
