import unittest

from interpreter.source import Source
from interpreter.scanner import Scanner
from interpreter.parser import Parser
from interpreter.interpretingvisitor import InterpretingVisitor
from interpreter.typecheckvisitor import TypeCheck
from interpreter.printvisitor import PrintVisitor


class TestInterpretingVisitor(unittest.TestCase):

    def testInterpretingVisitor(self):
        src = Source('./tests/test.minipl')
        scanner = Scanner(src)
        parser = Parser(scanner)
        ast = parser.program()
        tc = TypeCheck()
        ast.accept(tc)
        print(tc.errors)
        iv = InterpretingVisitor(tc.symbolTable)
        ast.accept(iv)
        pv = PrintVisitor()
        ast.accept(pv)
        print(pv.result)
