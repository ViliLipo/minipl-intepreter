from sys import argv
from intepreter.source import Source
from intepreter.scanner import Scanner
from intepreter.parser import Parser
from intepreter.interpretingvisitor import InterpretingVisitor
from intepreter.typecheckvisitor import TypeCheck
from intepreter.printvisitor import PrintVisitor


def setup(filename):
    src = Source(filename)
    scanner = Scanner(src)
    parser = Parser(scanner)
    ast = parser.program()
    return ast


def run(ast):
    tc = TypeCheck()
    ast.accept(tc)
    if len(tc.errors) == 0:
        iv = InterpretingVisitor(tc.symbolTable)
        ast.accept(iv)
    else:
        for error in tc.errors:
            print(error)


def main():
    if len(argv) == 2:
        fname = argv[1]
        ast = setup(fname)
        run(ast)

    else:
        print("Give filename as param")
    pass


if __name__ == "__main__":
    main()
