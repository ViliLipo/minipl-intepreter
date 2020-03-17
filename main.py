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
    return ast, parser.errors


def run(ast, errors):
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
        ast, errors = setup(fname)
        if len(errors) == 0:
            run(ast, errors)
        else:
            for error in errors:
                print(error)

    else:
        print("Give filename as cli parameter.")
    pass


if __name__ == "__main__":
    main()
