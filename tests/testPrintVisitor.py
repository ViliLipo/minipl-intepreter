import unittest

from interpreter.source import Source
from interpreter.scanner import Scanner
from interpreter.parser import Parser
from interpreter.printvisitor import PrintVisitor


class TestPrintVisitor(unittest.TestCase):

    def testPrintVisitor(self):
        src = Source('./tests/test.minipl')
        scanner = Scanner(src)
        parser = Parser(scanner)
        ast = parser.program()
        pv = PrintVisitor()
        ast.accept(pv)
        print(pv.result)
