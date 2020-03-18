import unittest
from intepreter.source import Source
from intepreter.scanner import Scanner
from intepreter.parser import Parser, ParsingError
from tests.testScanner import MockSource


class TestParserMethod(unittest.TestCase):

    def __initparser__(self, lines):
        src = MockSource(lines)
        scanner = Scanner(src)
        return Parser(scanner)

    def testParser(self):
        src = Source('./tests/test.minipl')
        scanner = Scanner(src)
        parser = Parser(scanner)
        parser.program()

    def testParseDeclaration(self):
        lines = ['var x: int := 3;\n']
        parser = self.__initparser__(lines)
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
        parser = self.__initparser__(lines)
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

    def testParseExpression(self):
        lines = ['3 * ( 5 + ( 8 / 4 ));\n']
        parser = self.__initparser__(lines)
        expression = parser.expression([';'])
        lex = expression.symbol.lexeme
        self.assertEqual('*', lex)
        three = expression.getLhsChild()
        self.assertEqual('3', three.symbol.lexeme)
        subExpr1 = expression.getRhsChild()
        self.assertEqual('+', subExpr1.symbol.lexeme)
        subExpr2 = subExpr1.getRhsChild()
        self.assertEqual('/', subExpr2.symbol.lexeme)
        four = subExpr2.getRhsChild()
        self.assertEqual('4', four.symbol.lexeme)

    def testParseUnaryExpression(self):
        lines = ['!( 1 = 0);\n']
        parser = self.__initparser__(lines)
        expression = parser.expression([';'])
        self.assertEqual('!', expression.symbol.lexeme)
        subExpr = expression.getRhsChild()
        self.assertEqual('=', subExpr.symbol.lexeme)

    def testRunawayParenthesis(self):
        lines = ['var ok : bool := !( 1 = 0;\n',
                 'var i : int;']
        parser = self.__initparser__(lines)
        program = parser.program()
        errorNode = program.children[0].getAssignChild()\
            .getRhsChild().getRhsChild()
        self.assertEqual('ErrorNode', errorNode.__class__.__name__)
        nextSmtnt = program.children[1]
        self.assertEqual('var', nextSmtnt.symbol.lexeme)
        ref = nextSmtnt.getRefChild()
        self.assertEqual('i', ref.symbol.lexeme)
        t = nextSmtnt.getTypeChild()
        self.assertEqual('int', t.symbol.lexeme)

    def testDoubleOperator(self):
        lines = ['var i: int ;\n', 'i := 1 ++ 2; \n',
                 'i := 3;']
        parser = self.__initparser__(lines)
        program = parser.program()
        error = parser.errors[0]
        correctMsg = 'Operand can not start with + on line 2.'
        self.assertEqual(correctMsg, str(error))
        print(str(error))
        self.assertEqual(1, len(parser.errors))
        assignment = program.children[2]
        three = assignment.getRhsChild()
        self.assertEqual('3', three.symbol.lexeme)

    def testIllegalStartOfStatement(self):
        lines = ['!( 1 = 0);\n']
        parser = self.__initparser__(lines)
        stmnt = parser.statement([';'])
        self.assertEqual('ErrorNode', stmnt.__class__.__name__)
