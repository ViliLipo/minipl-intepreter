import unittest
from intepreter.source import Source
from intepreter.scanner import Scanner
from intepreter.parser import Parser
from tests.testScanner import MockSource


class TestParserMethod(unittest.TestCase):

    def testParser(self):
        src = Source('./tests/test.minipl')
        scanner = Scanner(src)
        parser = Parser(scanner)
        parser.program()

    def testParseDeclaration(self):
        lines = ['var x: int := 3;\n']
        src = MockSource(lines)
        scanner = Scanner(src)
        parser = Parser(scanner)
        declaration = parser.statement(['eof'])
        self.assertEqual('var', declaration.symbol.lexeme)
        ref = declaration.getRefChild()
        t = declaration.getTypeChild()
        self.assertEqual('x', ref.symbol.lexeme)
        self.assertEqual('identifier', ref.symbol.tokenType)
        self.assertEqual('int', t.symbol.lexeme)
        self.assertEqual('int', t.symbol.tokenType)

    def testParseAssignment(self):
        lines = ['x := 3;\n']
        src = MockSource(lines)
        scanner = Scanner(src)
        parser = Parser(scanner)
        assignment = parser.statement(['eof'])
        self.assertEqual(':=', assignment.symbol.lexeme)
        self.assertEqual(':=', assignment.symbol.tokenType)
        refchild = assignment.getRefChild()
        refClass = refchild.__class__.__name__
        rhsChild = assignment.getRhsChild()
        self.assertEqual('x', refchild.symbol.lexeme)
        self.assertEqual('integer', rhsChild.symbol.tokenType)
        rhsClass = rhsChild.__class__.__name__
        self.assertEqual('IntegerNode', rhsClass)
        self.assertEqual('RefNode', refClass)

