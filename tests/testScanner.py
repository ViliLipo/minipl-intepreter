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

    def testScanNextToken2(self):
        src = Source('./tests/test.minipl')
        src.lines = ["var x : int;\n",
                     "for x in 0..5 do\n",
                     "print x;\n",
                     "end for;\n"]
        scanner = Scanner(src)
        tokens = [('var', 'var'), ('identifier', 'x'),
                  (':', ':'), ('int', 'int'),
                  (';', ';'), ('for', 'for'),
                  ('identifier', 'x'), ('in', 'in'),
                  ('integer', '0'), ('..', '..'), ('integer', '5'),
                  ('do', 'do'), ('print', 'print'),
                  ('identifier', 'x'), (';', ';'),
                  ('end', 'end'), ('for', 'for'), (';', ';')]
        for t in tokens:
            token = scanner.scanNextToken()
            tokenType, lexeme = t
            self.assertEqual(token.tokenType, tokenType)
            self.assertEqual(token.lexeme, lexeme)

    def testReal(self):
        src = Source('./tests/test.minipl')
        scanner = Scanner(src)
        symbol = scanner.scanNextToken()
        while symbol.tokenType != 'eof':
            symbol = scanner.scanNextToken()
            print(symbol)


if __name__ == '__main__':
    unittest.main()
