import unittest

from intepreter.source import Source
from intepreter.scanner import Scanner
from intepreter.parser import Parser
from intepreter.printvisitor import PrintVisitor


class TestPrintVisitor(unittest.TestCase):

    def testPrintVisitor(self):
        src = Source('./tests/test.minipl')
        scanner = Scanner(src)
        parser = Parser(scanner)
        ast = parser.program()
        pv = PrintVisitor()
        ast.accept(pv)
        print(pv.result)
