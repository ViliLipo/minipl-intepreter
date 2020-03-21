from unittest import TestCase
from unittest.mock import patch
from interpreter.source import Source
from interpreter.scanner import Scanner
from interpreter.parser import Parser
from interpreter.interpretingvisitor import InterpretingVisitor
from interpreter.typecheckvisitor import TypeCheck
from tests.testScanner import MockSource


class TestInterpretingVisitor(TestCase):

    def __createAstAndVisitor__(self, lines):
        src = MockSource(lines)
        scanner = Scanner(src)
        parser = Parser(scanner)
        ast = parser.program()
        tc = TypeCheck()
        ast.accept(tc)
        iv = InterpretingVisitor(tc.symbolTable)
        return ast, iv

    @patch('interpreter.interpretingvisitor.get_input', return_value="5")
    @patch('interpreter.interpretingvisitor.output')
    def testInterpretingVisitorWithAFile(self, output, input):
        src = Source('./tests/test.minipl')
        scanner = Scanner(src)
        parser = Parser(scanner)
        ast = parser.program()
        tc = TypeCheck()
        ast.accept(tc)
        iv = InterpretingVisitor(tc.symbolTable)
        ast.accept(iv)
        output.assert_called_with('120')

    @patch('interpreter.interpretingvisitor.get_input', return_value="8")
    @patch('interpreter.interpretingvisitor.output')
    def testInterpretingExpression(self, output, inpu):
        lines = [
                'var x : int := 3;\n',
                'var y: int;\n',
                'read y;\n',
                'print (x + y) / 2; \n'
                ]
        ast, iv = self.__createAstAndVisitor__(lines)
        ast.accept(iv)
        output.assert_called_with('5')

    @patch('interpreter.interpretingvisitor.output')
    def testInterpretingAssertOk(self, output):
        lines = ['assert(!( 1 = 0 ));\n',
                 'assert( 1 < 2);\n',
                 'assert(((1 = 1) & (0 = 0)));\n']
        ast, iv = self.__createAstAndVisitor__(lines)
        ast.accept(iv)
        output.assert_not_called()

    @patch('interpreter.interpretingvisitor.output')
    def testInterpretingAssertError(self, output):
        lines = ['assert(( 1 = 0));']
        ast, iv = self.__createAstAndVisitor__(lines)
        ast.accept(iv)
        output.assert_called_with('Assertion error at line 1.\n')
        output.reset_mock()
        lines = ['assert(( 2 < 1));']
        ast, iv = self.__createAstAndVisitor__(lines)
        ast.accept(iv)
        output.assert_called_with('Assertion error at line 1.\n')
        lines = ['assert(((2 < 1)&(0 = 0)));']
        ast, iv = self.__createAstAndVisitor__(lines)
        ast.accept(iv)
        output.assert_called_with('Assertion error at line 1.\n')

    @patch('interpreter.interpretingvisitor.output')
    def testInterpretingForStatement(self, output):
        lines = [
                'var i: int;\n',
                'var k: int := 1;\n',
                'for i in 1..10 do\n',
                '\t k := k + i;\n',
                'end for;\n'
                'print k;'
                ]
        ast, iv = self.__createAstAndVisitor__(lines)
        ast.accept(iv)
        output.assert_called_with('56')

    @patch('interpreter.interpretingvisitor.output')
    def testConcatString(self, output):
        lines = [
                'var s:string := "Hello";\n',
                'var s2: string := " World!\\n";\n',
                'print s + s2;\n',
                ]
        ast, iv = self.__createAstAndVisitor__(lines)
        ast.accept(iv)
        output.assert_called_with('Hello World!\n')
