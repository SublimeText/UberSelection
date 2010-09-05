import pyparsing as p
import sublime

offset = p.Optional(p.Group(p.Word("+-", max=1) + p.Word(p.nums)))
number = p.Word(p.nums) + offset
anchor = p.Word(".$", max=1) + offset
range_op = p.QuotedString(quoteChar="/", escChar="\\", unquoteResults=False) + offset
range_op2 = p.QuotedString(quoteChar="?", escChar="\\", unquoteResults=False) + offset

the_range = p.delimitedList(p.Group(number) | p.Group(anchor) | p.Group(range_op) | p.Group(range_op2)) | "%"

# =========================

# selection operator
selection = p.Group(p.Optional("-") + "V").setResultsName("command") + p.Group(p.QuotedString(quoteChar="/", escChar="\\")).setResultsName("argument") + p.Group(p.Optional(p.Word("iS"))).setResultsName("flags")
selection = p.delimitedList(p.Group(selection), delim=";")

trans = p.Group(p.Optional(the_range)).setResultsName("range") + p.Group(p.Optional(selection)).setResultsName("operator")
cmd = p.Word("weqnN") | "ls"
cmd = cmd + p.Optional(p.Word(p.alphas))

grammar = cmd.setResultsName("vim_cmd") | trans.setResultsName("trans")

def parse(this):
    tokens = grammar.parseString(this)
    vim_cmd, trans = tokens.vim_cmd, tokens.trans
    print vim_cmd, "///", trans
    if vim_cmd:
        return

    if trans:
        aRange, cmd = trans.range, trans.operator
        print "Range:", parseRange(aRange)
        print "Command:", cmd.command, cmd.argument, cmd.flags

def parseRange(the_range):
    if not the_range:
        return calculateRelativeRef(".")
    else:
        try:
            a, b = the_range
        except ValueError as e:
            a, b = the_range[0], '0'
            if a == "%":
                a, b = "1", "$"
        finally:
            x, y = parseRangePart(a), parseRangePart(b)
            return x, y or x

def parseRangePart(part):
    mainPart = part[0]

    modif = 0
    if len(part) > 1:
        modif = int("".join(part[1]))

    if mainPart.isdigit():
        return int(mainPart) + modif

    if mainPart in ("$", "."):
        return calculateRelativeRef(mainPart) + modif

    if mainPart.startswith("/") or mainPart.startswith("?"):
        return search(mainPart[1:-1], mainPart.startswith("?")) + modif

def calculateRelativeRef(where):
    view = sublime.activeWindow().activeView()
    if where == "$":
        return view.rowcol(view.size())[0] + 1
    if where == ".":
        return view.rowcol(view.sel()[0].begin())[0] + 1

def search(what, backward=False):
    view = sublime.activeWindow().activeView()
    if not backward:
        reg = view.find(what, view.sel()[0].begin())
        return (view.rowcol(reg.begin())[0] + 1) if reg else calculateRelativeRef(".")
    else:
        return 5000

if __name__ == "__main__":
    print selection.parseString("-V/this/i")
    print "="*80
    parse("10+10,.-20-V/this/iS")
    parse(".+10,$V/this/S")
    parse("V/for/s")
    parse("w eco")
