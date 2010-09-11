
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

class RangeComponent(unittest.TestCase):

        def setUp(self):
            self.r = newgrammar.generate_range()
            self.parse = self.r.parseString

        def testSimpleCases(self):
            self.assertEquals(self.parse("10"), 20)




if __name__ == "__main__":
    unittest.main()
