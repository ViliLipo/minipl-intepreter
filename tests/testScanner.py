import unittest
from intepreter.source import Source
from intepreter.scanner import Scanner


class MockSource(Source):
    def __init__(self, lines):
        self.lines = lines
        self.rowNumber = 0
        self.columnNumber = 0


class TestScannerMethods(unittest.TestCase):

    def testScanNextToken(self):
        lines = ["var X : int : 4 + (6 * 2);", "print X;"]
        src = MockSource(lines)
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
        lines = ["var x : int;\n",
                 "for x in 0..5 do\n",
                 "print x;\n",
                 "end for;\n"]
        src = MockSource(lines)
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

    def testMultilineComment(self):
        lines = ["/* multi", "line", "comment */\n",
                 "/* multi", "line", "comment */\n"]
        src = MockSource(lines)
        scanner = Scanner(src)
        token = scanner.scanNextToken()
        self.assertEqual('eof', token.tokenType)

    def testRunawayMultilineComment(self):
        lines = ["/* multi", "line", "comment \n",
                 "var x : int : 3;\n"]
        src = MockSource(lines)
        scanner = Scanner(src)
        token = scanner.scanNextToken()
        self.assertEqual('error', token.tokenType)

    def testSingleLineComment(self):
        lines = ["// Single line comment \n", 'var x : int := 0;']
        src = MockSource(lines)
        scanner = Scanner(src)
        token = scanner.scanNextToken()
        print(token)
        self.assertEqual('var', token.tokenType)

    def testReal(self):
        src = Source('./tests/test.minipl')
        scanner = Scanner(src)
        symbol = scanner.scanNextToken()
        while symbol.tokenType != 'eof':
            symbol = scanner.scanNextToken()
            print(symbol)


if __name__ == '__main__':
    unittest.main()
