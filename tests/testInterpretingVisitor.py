import unittest

from intepreter.source import Source
from intepreter.scanner import Scanner
from intepreter.parser import Parser
from intepreter.interpretingvisitor import InterpretingVisitor
from intepreter.typecheckvisitor import TypeCheck
from intepreter.printvisitor import PrintVisitor


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
