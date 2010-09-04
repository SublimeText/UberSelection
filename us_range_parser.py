import pyparsing as p
import pprint

opt_modif = p.Group(p.Optional(p.Word("+-") + p.Word(p.nums)))

simple_cmd = p.Word("weqnN") | p.Literal("ls")
nrng = p.Word(p.nums) + opt_modif
hrng = p.Word(".$") + opt_modif
fs = "/" + p.Word(p.alphas) + "/" + opt_modif
bs = "?" + p.Word(p.alphas) + "?" + opt_modif

the_range = p.delimitedList(p.Group(hrng) | p.Group(fs) | p.Group(bs) | p.Group(nrng))
cmd = p.Optional(p.Literal("-")) + p.Literal("V") + "/" + p.CharsNotIn("/") + "/" + p.Group(p.Optional(p.Word("i")))
cmd2 = p.Literal("rep") + "/" + p.CharsNotIn("/") + "/" + p.CharsNotIn("/") + "/" + p.Group(p.Optional(p.Word("i")))
grammar = simple_cmd.setResultsName("cmd") | p.Group(p.Optional(the_range)).setResultsName("range") + p.Group(p.delimitedList(p.Group(p.Optional(cmd | cmd2)), delim=";")).setResultsName("cmds")

def parse(a):
    return grammar.parseString(a)

if __name__ == "__main__":
    import sys
    print grammar.parseString(sys.argv[1])
    # x = grammar.parseString(".-10,$-5")
    # print x
    # x = grammar.parseString(".,$+10")
    # print x
    # x = grammar.parseString("/cana/+10")
    # print x
    # x = grammar.parseString("?cana?-10")
    # print x
    # x = grammar.parseString(".,/whatever/+10 -sel/this/i;sel/that/")
    # print x.range, "//", x.cmds
    # x = grammar.parseString("rep;rep")
    # print x.range, "//", x.cmds
