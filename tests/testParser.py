import unittest
from interpreter.source import Source
from interpreter.scanner import Scanner
from interpreter.parser import Parser
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

    def testMissingSemiColon(self):
        # TODO
        lines = ['var x : int := 3 + 5\n'
                 'var y: int;']
        parser = self.__initparser__(lines)
        program = parser.program()
        lines = ['x := 3\n'
                 'var y: int;']
        parser = self.__initparser__(lines)
        program = parser.program()
        print(program)

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
        self.assertEqual(1, len(parser.errors))
        assignment = program.children[2]
        three = assignment.getRhsChild()
        self.assertEqual('3', three.symbol.lexeme)

    def testInvalidOperator(self):
        lines = ['k := i $ j;',
                 'var l: int:= 1;']
        parser = self.__initparser__(lines)
        program = parser.program()
        self.assertTrue(len(parser.errors) >= 1)
        secondStmnt = program.children[1]
        lexeme = secondStmnt.symbol.lexeme
        self.assertEqual('var', lexeme)

    def testIllegalStartOfStatement(self):
        lines = ['!( 1 = 0);\n']
        parser = self.__initparser__(lines)
        stmnt = parser.statement([';'])
        self.assertEqual('ErrorNode', stmnt.__class__.__name__)

    def testLoneDotError(self):
        lines = ['for x in 0.5 do\n',
                 'print x;\n',
                 'end for;\n',
                 'assert(x = 5);\n']
        parser = self.__initparser__(lines)
        program = parser.program()
        types = []
        for child in program.children:
            types.append(child.symbol.tokenType)
        self.assertTrue('print' in types)
        self.assertTrue('assert' in types)

    def testRunawayForStatement(self):
        lines = ['var x : int;',
                 'for x in 0..5 do\n',
                 'print x;\n',
                 'assert(x = 5);\n']
        parser = self.__initparser__(lines)
        program = parser.program()
        messages = []
        for e in parser.errors:
            messages.append(str(e))
        self.assertTrue('Runaway for statement at line 2.' in messages)
        self.assertEqual(len(program.children), 2)

    def testMissingExpression(self):
        lines = ['var x: int := ;',
                 'var y: int;']
        parser = self.__initparser__(lines)
        program = parser.program()
        msg = str(parser.errors[0])
        self.assertEqual('Operand can not start with ; on line 1.',
                         msg)
        self.assertTrue(len(program.children) >= 2)

    def testUnmatchedParen(self):
        lines = ['var x: int := 3 + (5 * 4;',
                 'var y: int;']
        parser = self.__initparser__(lines)
        program = parser.program()
        msg = str(parser.errors[0])
        self.assertEqual('Expected ), got ; at line 1.', msg)
        self.assertTrue(len(program.children) >= 2)
        lex = program.children[1].symbol.lexeme
        self.assertEqual(lex, 'var')

    def testInvalidType(self):
        lines = ['var x: double := 3;\n',
                 'y := 1;\n']
        parser = self.__initparser__(lines)
        program = parser.program()
        self.assertTrue(len(program.children) >= 2)

    def testEofInMiddleOfExpression(self):
        lines = ['y := 5 + 3;', 'assert(x +']
        parser = self.__initparser__(lines)
        parser.program()
        e = parser.errors[0]
        correctMsg = 'Operand can not start with eof on line 3.'
        self.assertEqual(correctMsg, str(e))
