import unittest
from intepreter.source import Source
from intepreter.scanner import Scanner
from intepreter.parser import Parser


class TestParserMethod(unittest.TestCase):

    def testParser(self):
        src = Source('./tests/test.minipl')
        scanner = Scanner(src)
        parser = Parser(scanner)
        parser.program()
