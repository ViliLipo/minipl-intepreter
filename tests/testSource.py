import unittest
from intepreter.source import Source


class TestSourceMethods(unittest.TestCase):

    def testGetChar(self):
        src = Source('./tests/test.minipl')
        self.assertEqual(src.getChar(), 'v')
        self.assertEqual(src.getChar(), 'a')
        src.rowNumber = 1
        src.columnNumber = 0
        self.assertEqual(src.getChar(), 'p')

    def testGetPos(self):
        src = Source('./tests/test.minipl')
        src.getChar()
        src.getChar()
        self.assertEqual(src.getCurrentPosition(), (2, 1))
        src.rowNumber = 1
        src.columnNumber = 0
        src.getChar()
        self.assertEqual(src.getCurrentPosition(), (1, 2))

    def testEof(self):
        src = Source('./tests/test.minipl')
        src.columnNumber = 1000
        src.rowNumber = len(src.lines) - 1
        self.assertEqual(src.getChar(), False)


if __name__ == '__main__':
    unittest.main()
