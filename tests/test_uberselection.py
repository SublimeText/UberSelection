
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

import uberselection

class RangeParserTestCase(unittest.TestCase):

    def test_CommaSeparatedNumbersAreDetected(self):
        expected = (1, 2)
        actual = uberselection.parseRange("1,2")
        self.assertEquals(expected, actual)


class UberselectionTestCase(unittest.TestCase):

    def test_WeCanShowInputPanel(self):
        view = sublime.View()
        window = mock.Mock()
        view.window = window
        cmd = uberselection.UberSelectionCommand()
        cmd.showInputPanel(view)

        self.assertTrue(view.window().showInputPanel.called)


if __name__ == "__main__":
    unittest.main()
