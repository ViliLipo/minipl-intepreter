
class Parser:

    def __init__(self, scanner):
        self.scanner = scanner
        self.nextToken()
        self.errors = []

    def nextToken(self):
        self.symbol = self.scanner.scanNextToken()

    def match(self, typeString):
        if self.symbol.tokenType == typeString:
            self.nextToken()
            return True
        else:
            print('Expected {}, got {}'.format(
                typeString, self.symbol.tokenType))
            return False

    def matchOperator(self):
        if self.symbol.tokenType in ['+', '-', '/', '*', '&', '|']:
            self.nextToken()
            return True
        else:
            print('Expected operator, got {}'.format(
                self.symbol.tokenType))
            self.nextToken()
            return False

    def matchType(self):
        if self.symbol.tokenType in ['int', 'string', 'bool']:
            self.nextToken()
            return True
        else:
            return False

    def program(self):
        while self.symbol.tokenType != "eof":
            self.statement()
        else:
            print('end of file')

    def statement(self):
        tokenType = self.symbol.tokenType
        if tokenType == 'identifier':
            self.nextToken()
            self.match(':=')
            self.expression()
            self.match(';')
        elif tokenType == 'read':
            self.nextToken()
            self.match('identifier')
            self.match(';')
        elif tokenType == 'print':
            self.nextToken()
            self.expression()
            self.match(';')
        elif tokenType == 'assert':
            self.nextToken()
            self.expression()
            self.match(';')
        elif tokenType == 'var':
            self.nextToken()
            self.match('identifier')
            self.match(':')
            self.matchType()
            if self.symbol.tokenType == ':=':
                self.nextToken()
                self.expression()
            self.match(';')
        elif tokenType == 'for':
            self.nextToken()
            self.match('identifier')
            self.match('in')
            self.expression()
            self.match('..')
            self.expression()
            self.match('do')
            while not self.symbol.tokenType == 'end':
                self.statement()
            self.match('end')
            self.match('for')
        else:
            print("statement cant start with lexeme {}".format(self.symbol))

    def expression(self):
        self.operand()
        self.operation()
        self.operand()

    def operand(self):
        tokenType = self.symbol.tokenType
        if tokenType == 'integer':
            self.nextToken()
        elif tokenType == 'string':
            self.nextToken()
        elif tokenType == 'identifier':
            self.nextToken()
        elif tokenType == '(':
            self.nextToken()
            self.expression()
            self.match(')')
        else:
            print("operand can't be {}".format(self.symbol))

    def operation(self):
        self.matchOperator()
