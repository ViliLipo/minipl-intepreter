from unittest import TestCase
from interpreter.source import Source
from tests.testScanner import MockSource
from interpreter.scanner import Scanner
from interpreter.parser import Parser
from interpreter.typecheckvisitor import TypeCheck
from interpreter.printvisitor import PrintVisitor


class TestTypeCheckVisitor(TestCase):
    def __createAST__(self, lines):
        src = MockSource(lines)
        scanner = Scanner(src)
        parser = Parser(scanner)
        return parser.program(), parser

    def __errortest__(self, lines, correctMsg):
        ast, parser = self.__createAST__(lines)
        tc = TypeCheck()
        ast.accept(tc)
        error = tc.errors[0]
        self.assertEqual(correctMsg, str(error))

    def testTypeCheckVisitor(self):
        return
        src = Source('./tests/test.minipl')
        scanner = Scanner(src)
        parser = Parser(scanner)
        ast = parser.program()
        tc = TypeCheck()
        ast.accept(tc)

    def testDuplicateDeclaration(self):
        lines = ['var x: int;\n', 'var x: int;\n']
        correctMsg = 'Declaration of an existing variable: on line 2.'
        self.__errortest__(lines, correctMsg)

    def testIncompatibleType(self):
        lines = ['var x: int := "asdf";\n']
        correctMsg = 'Assignment to an uncompatible type: on line 1.'
        self.__errortest__(lines, correctMsg)

    def testAssignToUndeclared(self):
        lines = ['x := 3;\n']
        correctMsg = 'Reference to an undefined variable: on line 1.'
        self.__errortest__(lines, correctMsg)

    def testIntLiteralExpression(self):
        lines = ['var x : int;\n', ' x := 5 + ((3*5)/(8 - 4));\n']
        ast, parser = self.__createAST__(lines)
        tc = TypeCheck()
        ast.accept(tc)
        assign = ast.children[1]
        rhs = assign.getRhsChild()
        self.assertEqual('int', rhs.evalType)

    def testStringLiteralExpression(self):
        lines = ['var x : string;\n', ' x := "asd" + "f";\n']
        ast, parser = self.__createAST__(lines)
        tc = TypeCheck()
        ast.accept(tc)
        assign = ast.children[1]
        rhs = assign.getRhsChild()
        self.assertEqual('string', rhs.evalType)

    def testInvalidStringLiteralExpression(self):
        lines = ['var s : string := "asd" - "sd"\n']
        correctMsg = 'Can not apply - to string: on line 1.'
        self.__errortest__(lines, correctMsg)

    def testVarIntExpression(self):
        lines = ['var x: int:= 3;\n',
                 'var y: int := 2;\n',
                 'x := x + (3 * y); \n']
        ast, parser = self.__createAST__(lines)
        tc = TypeCheck()
        ast.accept(tc)
        assign = ast.children[2]
        et = assign.getRhsChild().evalType
        self.assertEqual('int', et)
        self.assertEqual(0, len(tc.errors))

    def testVarStringExpression(self):
        lines = ['var s : string := "asd";\n',
                 's := s + s;\n'
                 ]
        ast, parser = self.__createAST__(lines)
        tc = TypeCheck()
        ast.accept(tc)
        assign = ast.children[1]
        et = assign.getRhsChild().evalType
        self.assertEqual('string', et)

    def testForStatement(self):
        lines = [
            'var x : int;\n',
            'for x in 1 .. 10 do\n',
            '\t print x;\n',
            'end for;\n'
        ]
        ast, parser = self.__createAST__(lines)
        tc = TypeCheck()
        ast.accept(tc)
        self.assertEqual(0, len(tc.errors))

    def testBadForStatement(self):
        lines = [
            'var x : int;\n',
            'for x in I .. 10 do\n',
            '\t print x;\n',
            'end for;\n'
        ]
        ast, parser = self.__createAST__(lines)
        tc = TypeCheck()
        ast.accept(tc)
        self.assertEqual(2, len(tc.errors))

    def testUndeclaredLoopVariable(self):
        lines = [
            'for x in 1 .. 10 do\n',
            '\t print x;\n',
            'end for;\n'
        ]
        correctMsg = 'Reference to an undefined variable: on line 1.'
        self.__errortest__(lines, correctMsg)

    def testPrintStatement(self):
        lines = ['print ( 5 * 10);']
        ast, parser = self.__createAST__(lines)
        tc = TypeCheck()
        ast.accept(tc)
        expr = ast.children[0].getPrintableChild()
        self.assertEqual('int', expr.evalType)

    def testAssertOk(self):
        lines = ['assert( 1 = 1);']
        ast, parser = self.__createAST__(lines)
        tc = TypeCheck()
        ast.accept(tc)
        assertion = ast.children[0]
        rhs = assertion.getArgumentChild()
        self.assertEqual('bool', rhs.evalType)
        self.assertEqual(0, len(tc.errors))

    def testAssertBroken(self):
        lines = ['assert( 5 + 5);']
        correctMsg = 'Assert must have a boolean parameter: on line 1.'
        self.__errortest__(lines, correctMsg)

    def testRead(self):
        lines = ['var x: int;\n', 'read x;']
        ast, parser = self.__createAST__(lines)
        tc = TypeCheck()
        ast.accept(tc)
        self.assertEqual(0, len(tc.errors))

    def testReadFail(self):
        lines = ['var x: bool;\n', 'read x;']
        correctMsg = 'Read must happen to a string or int variable: on line 2.'
        self.__errortest__(lines, correctMsg)

    def testUnaryNot(self):
        lines = ['assert(!(0=0))']
        ast, parser = self.__createAST__(lines)
        tc = TypeCheck()
        ast.accept(tc)
        self.assertEqual(0, len(tc.errors))

    def testUnaryNotError(self):
        lines = ['assert(!(1 + 10))']
        correctMsg = \
            'Unary ! can only operate on boolean expressions: on line 1.'
        self.__errortest__(lines, correctMsg)
