import unittest
from intepreter.source import Source
from intepreter.scanner import Scanner


class TestSourceMethods(unittest.TestCase):

    def testScanNextToken(self):
        src = Source('./tests/test.minipl')
        src.lines = ["var X : int : 4 + (6 * 2);", "print X;"]
        tokens = [('var', 'var'), ('identifier', 'X'),
                  (':', ':'), ('int', 'int'),
                  (':', ':'), ('integer', '4'), ('+', '+'),
                  ('(', '('), ('integer', '6'), ('*', '*'),
                  ('integer', '2'), (')', ')'), (';', ';')]
        scanner = Scanner(src)
        for t in tokens:
            token = scanner.scanNextToken()
            tokenType, lexeme = t
            self.assertEqual(token.tokenType, tokenType)
            self.assertEqual(token.lexeme, lexeme)


if __name__ == '__main__':
    unittest.main()
