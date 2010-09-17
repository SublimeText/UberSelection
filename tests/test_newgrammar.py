
import _setuptestenv
import sys

try:
    import mock
except ImportError:
    print "ERROR: Cannot find mock module in your SYSTEM'S Python library."
    sys.exit(1)

import unittest
import sublime
import sublimeplugin

#===============================================================================
# Add your tests below here.
#===============================================================================

import newgrammar

class RangeTests(unittest.TestCase):

        def setUp(self):
            self.r = newgrammar.generate_range()
            self.parse = self.r.parseString

        def testAbsoluteLineReferences(self):
            values = ("1", "10", "10000")
            results = [self.parse(x).a.value for x in values]
            self.assertEquals(results, list(values))

        def testOffsets(self):
            values = ("1+100", "1-100")
            results = [self.parse(x).a.offset for x in values]
            self.assertEquals(results, ["+100", "-100"])

        def testRelativeLineReferences(self):
            values = (".", "$")
            results = [self.parse(x).a.value for x in values]
            self.assertEquals(results, [".", "$"])

            values = (".+100", "$-100")
            results = [(self.parse(x).a.value, self.parse(x).a.offset) for x in values]
            self.assertEquals(results, [(".", "+100"), ("$", "-100")])

        def testSearchReferences(self):
            values = ("/abc/", "?abc?")
            results = [self.parse(x).a.value for x in values]
            self.assertEquals(results, ["/abc/", "?abc?"])

            values = ("/abc/+10", "?abc?-10")
            results = [(self.parse(x).a.value, self.parse(x).a.offset) for x in values]
            self.assertEquals(results, [("/abc/", "+10"), ("?abc?", "-10")])

        def testRange(self):
            tokens = self.parse("10,10")
            self.assertEquals((tokens.a.value, tokens.b.value), ("10", "10"))

            tokens = self.parse(".+10,$-10")
            results = (tokens.a.value, tokens.a.offset, tokens.b.value, tokens.b.offset)
            self.assertEquals(results, (".", "+10", "$", "-10"))

        def testAllLines(self):
            tokens = self.parse("%")
            self.assertEquals(tokens.all, "%")


class FullVisualTests(unittest.TestCase):

    def setUp(self):
        self.v = newgrammar.generate_fullvisual()
        self.parse = self.v.parseString

    def testInclusiveSelection(self):
        tokens = self.parse("V/abc/")
        cmd, arg, flags = tokens.visual
        self.assertEquals([cmd, arg, flags], ["V", "abc", "i"])

        tokens = self.parse("V/abc/c")
        cmd, arg, flags = tokens.visual
        self.assertEquals([cmd, arg, flags], ["V", "abc", "c"])


    def testExclusiveSelection(self):
        tokens = self.parse("-V/abc/")
        cmd, arg, flags = tokens.visual_min
        self.assertEquals([cmd, arg, flags], ["-V", "abc", "i"])

        tokens = self.parse("-V/abc/c")
        cmd, arg, flags = tokens.visual_min
        self.assertEquals([cmd, arg, flags], ["-V", "abc", "c"])


class SubstCommandTests(unittest.TestCase):

    def setUp(self):
        self.v = newgrammar.generate_sub_cmd()
        self.parse = self.v.parseString

    def testTokensAreDetectedCorrectly(self):
        values = [x.join(["s", "this", "that"]) + x for x in ": ; , = / \\ & $ !".split()]

        results = [(self.parse(x).command,
                    self.parse(x).search[0],
                    self.parse(x).replace[0])
                                                for x in values ]

        self.assertEquals(results, [("s", "this", "that"),] * len(values))


class TestGrammar(unittest.TestCase):

    def setUp(self):
        self.v = newgrammar.generate_grammar()
        self.parse = self.v.parseString

    def testVimMode(self):
        # TODO: What to test? Currently it accepts any number of :alpha:.
        pass

    def testRangeMode(self):
        values = ("10,10", "10+10,10-10", ".,$", ".+10,$-10", "/abc/+10,?abc?-10")
        results = [ getattr(self.parse(x), 'range', None) for x in values]
        self.assertTrue(all(results)) # Do they all return a range?

    def testCmd(self):
        values = "V/abc/;-V/abc/;s/x/y/"
        self.assertEquals(len(self.parse(values).cmd), 3)

    def testComplex_Cmd(self):
        values = ".+1,/abc/-1V/a/;-V/b/;s/y/x/"
        x = self.parse(values).complex_cmd
        self.assertTrue(all((x.range, x.cmd)))


if __name__ == "__main__":
    unittest.main()
