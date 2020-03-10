from intepreter.ast import makeNode


class Parser:

    def __init__(self, scanner):
        self.scanner = scanner
        self.nextToken()
        self.errors = []
        self.statementVariants = [
                self.assignStatement,
                self.assertStatement,
                self.declarationStatement,
                self.printStatement,
                self.forStatement,
                self.readStatement,
                ]

    operators = ['+', '-', '/', '*', '&', '|', '=']

    def nextToken(self):
        self.symbol = self.scanner.scanNextToken()

    def match(self, typeString):
        if self.symbol.tokenType == typeString:
            node = makeNode(self.symbol)
            self.nextToken()
            return node
        else:
            print('Expected {}, got {}'.format(
                typeString, self.symbol.tokenType))
            return None

    def matchOperator(self):
        if self.symbol.tokenType in Parser.operators:
            node = makeNode(self.symbol)
            self.nextToken()
            return node
        else:
            print('Expected operator, got {}'.format(
                self.symbol.tokenType))
            return None

    def matchType(self):
        if self.symbol.tokenType in ['int', 'string', 'bool']:
            node = makeNode(self.symbol)
            self.nextToken()
            return node
        else:
            return None

    def program(self):
        stmntlist = []
        while self.symbol.tokenType != "eof":
            stmntlist.append(self.statement())
        for stmnt in stmntlist:
            print(stmnt)
        else:
            print('end of file')

    def statement(self):
        node = False
        for stmnt in self.statementVariants:
            node = stmnt()
            if node:
                return node
        else:
            print("statement cant start with lexeme {}".format(self.symbol))

    def assignStatement(self):
        tokenType = self.symbol.tokenType
        if tokenType == 'identifier':
            lhs = makeNode(self.symbol)
            self.nextToken()
            node = self.match(':=')
            rhs = self.expression()
            node.addChild(lhs)
            node.addChild(rhs)
            self.match(';')
            return node
        else:
            return False

    def forStatement(self):
        tokenType = self.symbol.tokenType
        if tokenType == 'for':
            node = makeNode(self.symbol)
            self.nextToken()
            variable = self.match('identifier')
            condition = self.match('in')
            lhs = self.expression()
            ran = self.match('..')
            rhs = self.expression()
            ran.addChild(lhs)
            ran.addChild(rhs)
            condition.addChild(variable)
            condition.addChild(ran)
            node.addChild(condition)
            body = self.match('do')
            node.addChild(body)
            while not self.symbol.tokenType == 'end':
                body.addChild(self.statement())
            self.match('end')
            self.match('for')
            self.match(';')
            return node
        else:
            return False

    def declarationStatement(self):
        tokenType = self.symbol.tokenType
        if tokenType == 'var':
            node = makeNode(self.symbol)
            self.nextToken()
            node.addChild(self.match('identifier'))
            self.match(':')
            node.addChild(self.matchType())
            if self.symbol.tokenType == ':=':
                assign = makeNode(self.symbol)
                self.nextToken()
                node.addChild(assign)
                assign.addChild(self.expression())
            self.match(';')
            return node
        else:
            return False

    def assertStatement(self):
        tokenType = self.symbol.tokenType
        if tokenType == 'assert':
            node = makeNode(self.symbol)
            self.nextToken()
            node.addChild(self.expression())
            self.match(';')
            return node
        else:
            return False

    def readStatement(self):
        tokenType = self.symbol.tokenType
        if tokenType == 'read':
            node = makeNode(self.symbol)
            self.nextToken()
            self.match('identifier')
            self.match(';')
            return node
        else:
            return False

    def printStatement(self):
        tokenType = self.symbol.tokenType
        if tokenType == 'print':
            node = makeNode(self.symbol)
            self.nextToken()
            node.addChild(self.expression())
            self.match(';')
            return node
        else:
            return False

    def expression(self):
        if self.symbolIsUnary():
            node = makeNode(self.symbol)
            self.nextToken()
            rhs = self.operand
            node.addChild(rhs)
            return node
        lhs = self.operand()
        if self.symbol.tokenType in Parser.operators:
            node = self.operation()
            rhs = self.operand()
            node.addChild(lhs)
            node.addChild(rhs)
            return node
        else:
            return lhs

    def operand(self):
        tokenType = self.symbol.tokenType
        node = None
        if tokenType in ['integer', 'string', 'identifier']:
            node = makeNode(self.symbol)
            self.nextToken()
        elif tokenType == '(':
            self.nextToken()
            node = self.expression()
            self.match(')')
        else:
            print("operand can't be {}".format(self.symbol))
        return node

    def operation(self):
        node = self.matchOperator()
        return node

    def symbolIsUnary(self):
        return self.symbol.tokenType == '!'
    
