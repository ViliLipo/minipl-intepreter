from sys import argv
from interpreter.source import Source
from interpreter.scanner import Scanner
from interpreter.parser import Parser
from interpreter.interpretingvisitor import InterpretingVisitor
from interpreter.typecheckvisitor import TypeCheck
from interpreter.printvisitor import PrintVisitor


def header():
    msg = 'Mini-pl interpreter by Vili Lipo. \n' \
        + 'Licence GPL 3 \n' \
        + 'Helsinki, Finland  2020\n' \
        + '------------------------- '
    print(msg)


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
    header()
    try:
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
    except KeyboardInterrupt:
        pass
    except SystemExit:
        pass
    finally:
        print('\nGoodbye!\n')


if __name__ == "__main__":
    main()
