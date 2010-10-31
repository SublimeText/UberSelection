import pyparsing as p

def generate_range():
    searchf = p.QuotedString(quoteChar="/", unquoteResults=False)
    searchb = p.QuotedString(quoteChar="?", unquoteResults=False)

    term = p.Word(p.nums) ^ p.oneOf("$ .") ^ searchf ^ searchb

    offset = p.oneOf("+ -") + p.Word(p.nums)
    offset.setParseAction(lambda x: ''.join(x))

    fullterm = term("value") + p.Optional(offset("offset"), default='0')
    sep = p.Literal(",").suppress()

    wholebuffer = p.Literal("%")

    fullrange = fullterm("a") + p.Optional(sep + fullterm)("b")
    return fullrange ^ wholebuffer("all")

def generate_visual():
    visual = p.QuotedString(quoteChar="V/", unquoteResults=True, endQuoteChar="/")
    visual.setParseAction(lambda x: ["V", x[0]])

    return visual

def generate_visualmin():
    visualmin = p.QuotedString(quoteChar="-V/", unquoteResults=True, endQuoteChar="/")
    visualmin.setParseAction(lambda x: ["-V", x[0]])

    return visualmin

def generate_visual_flags():
    flags = p.Optional(p.Word("ic"), default="i")

    return flags

def generate_fullvisual():
    visual, visualmin, flags = generate_visual(), generate_visualmin(), generate_visual_flags()

    visual = visual + flags
    visualmin = visualmin + flags

    return visual('visual') ^ visualmin('visual_min')

def generate_vim_cmd():
    # Vim commands like: :e, :ls, etc.
    vim_cmd_name = p.Word(p.alphas)
    vim_cmd_arg = p.Word(p.alphas)
    arg = p.Optional(vim_cmd_arg, default='')
    arg.setParseAction(lambda x: x[0])
    vim_cmd = vim_cmd_name + arg
    return vim_cmd

def generate_sub_cmd():
    separator = p.oneOf(": ; , = / \\ & $ !")
    replacement = p.Literal("s").setResultsName("command") + separator + p.SkipTo(p.matchPreviousLiteral(separator), include=True).setWhitespaceChars("\r\n").setResultsName("search") + p.SkipTo(p.matchPreviousLiteral(separator), include=True).setWhitespaceChars("\r\n").setResultsName("replace")
    return replacement

def generate_grammar():
    the_range = generate_range()
    visual = generate_fullvisual()
    visual = visual ^ generate_sub_cmd()
    vim_cmd = generate_vim_cmd()

    complex_cmd = p.Group(the_range)('range') + p.delimitedList(p.Group(visual), delim=";")('cmd')

    return p.Group(vim_cmd)('vim_cmd') ^ p.Group(the_range)('range') ^ p.Group(p.delimitedList(p.Group(visual), delim=";"))('cmd') ^ p.Group(complex_cmd)('complex_cmd')

if __name__ == "__main__":
    x = generate_range()
    c = x.parseString("%")
    print c.all

    x = generate_grammar()
    c = x.parseString("%V/ECO/;-V/AVA/")
    print c.complex_cmd.range, c.complex_cmd.cmd
