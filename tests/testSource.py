import unittest
from interpreter.source import Source


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
        self.assertEqual(src.getCurrentPosition(), (1, 1))
        src.getChar()
        src.getChar()
        self.assertEqual(src.getCurrentPosition(), (3, 1))
        src.rowNumber = 1
        src.columnNumber = 0
        self.assertEqual(src.getCurrentPosition(), (1, 2))

    def testEof(self):
        pass


if __name__ == '__main__':
    unittest.main()
