from interpreter.ast import makeNode
from interpreter.ast import ErrorNode


class ParsingError(Exception):
    pass


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

    operators = ['+', '-', '/', '*', '&', '|', '=', '<']

    def nextToken(self):
        self.symbol = self.scanner.scanNextToken()

    def match(self, typeString):
        if self.symbol.tokenType == typeString:
            node = makeNode(self.symbol)
            self.nextToken()
            return node
        else:
            raise ParsingError('Expected {}, got {} at line {}.'.format(
                typeString, self.symbol.tokenType,
                self.symbol.startposition[1]))

    def matchOperator(self):
        if self.symbol.tokenType in Parser.operators:
            node = makeNode(self.symbol)
            self.nextToken()
            return node
        else:
            raise ParsingError('Expected operator, got {} at line {}.'.format(
                self.symbol.tokenType, self.symbol.startposition[1]))

    def matchType(self):
        if self.symbol.tokenType in ['int', 'string', 'bool']:
            node = makeNode(self.symbol)
            self.nextToken()
            return node
        else:
            raise ParsingError('Expected type definition, got {} at line {}'
                               .format(
                                   self.symbol.tokenType,
                                   self.symbol.startposition[1]))

    def first(symbol):
        if symbol == 'statement':
            return ['identifier', 'var', 'for', 'assert', 'read', 'print']
        if symbol == 'expression':
            return Parser.first('operand') + ['!']
        if symbol == 'operand':
            return ['indentifier' 'int', 'string_literal', '(']
        if symbol == 'operator':
            return Parser.operators

    def program(self):
        stmntlist = makeNode()
        while self.symbol.tokenType != "eof":
            try:
                stmntlist.addChild(self.statement(['eof']))
                self.match(';')
            except ParsingError as e:
                self.errors.append(e)
        return stmntlist

    def statement(self, followset):
        try:
            node = ErrorNode(self.symbol)
            for stmnt in self.statementVariants:
                node = stmnt()
                if node:
                    return node
            else:
                line = self.symbol.startposition[1]
                raise ParsingError(
                    "Statement can not start with lexeme {} on line {}."
                    .format(self.symbol, line))
        except ParsingError as e:
            while True:
                if self.symbol.tokenType in Parser.first('statement'):
                    self.errors.append(e)
                    return self.statement(followset)
                elif self.symbol.tokenType == 'eof':
                    raise e
                elif self.symbol.tokenType in followset:
                    self.errors.append(e)
                    return ErrorNode(self.symbol)
                self.nextToken()

    def assignStatement(self):
        tokenType = self.symbol.tokenType
        if tokenType == 'identifier':
            lhs = makeNode(self.symbol)
            self.nextToken()
            node = self.match(':=')
            rhs = self.expression([';'])
            node.addChild(lhs)
            node.addChild(rhs)
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
            lhs = self.expression(['..'])
            rangeNode = self.match('..')
            rhs = self.expression(['do'])
            condition.addChild(variable)
            rangeNode.addChild(lhs)
            rangeNode.addChild(rhs)
            condition.addChild(rangeNode)
            node.addChild(condition)
            body = self.match('do')
            node.addChild(body)
            while not self.symbol.tokenType == 'end':
                try:
                    body.addChild(self.statement(Parser.first('statement')
                                                 + ['end']))
                    self.match(';')
                except ParsingError:
                    if self.symbol.tokenType == 'eof':
                        line = node.symbol.startposition[1]
                        error = ParsingError(
                            'Runaway for statement at line {}.'
                            .format(line))
                        self.errors.append(error)
                        return node
            self.match('end')
            self.match('for')
            return node
        else:
            return False

    def declarationStatement(self):
        tokenType = self.symbol.tokenType
        if tokenType == 'var':
            node = makeNode(self.symbol)
            self.nextToken()
            ref = self.match('identifier')
            node.addChild(ref)
            self.match(':')
            node.addChild(self.matchType())
            if self.symbol.tokenType == ':=':
                assign = makeNode(self.symbol)
                self.nextToken()
                node.addChild(assign)
                assign.addChild(ref)
                assign.addChild(self.expression([';']))
            return node
        else:
            return False

    def assertStatement(self):
        tokenType = self.symbol.tokenType
        if tokenType == 'assert':
            node = makeNode(self.symbol)
            self.nextToken()
            self.match('(')
            node.addChild(self.expression([')']))
            self.match(')')
            return node
        else:
            return False

    def readStatement(self):
        tokenType = self.symbol.tokenType
        if tokenType == 'read':
            node = makeNode(self.symbol)
            self.nextToken()
            node.addChild(self.match('identifier'))
            return node
        else:
            return False

    def printStatement(self):
        tokenType = self.symbol.tokenType
        if tokenType == 'print':
            node = makeNode(self.symbol)
            self.nextToken()
            node.addChild(self.expression([';']))
            return node
        else:
            return False

    def expression(self, followset):
        try:
            if self.symbolIsUnary():
                node = makeNode(self.symbol)
                self.nextToken()
                rhs = self.operand(followset)
                node.addChild(rhs)
                return node
            lhs = self.operand(Parser.first('operator') + followset)
            if self.symbol.tokenType in Parser.operators:
                node = self.operation(Parser.first('operand'))
                rhs = self.operand(followset)
                node.addChild(lhs)
                node.addChild(rhs)
                return node
            else:
                return lhs
        except ParsingError as e:
            # Only error operand or operator will raise is eof
            raise e

    def operand(self, followset):
        try:
            tokenType = self.symbol.tokenType
            if tokenType in ['integer', 'string_literal', 'identifier']:
                node = makeNode(self.symbol)
                self.nextToken()
                return node
            elif tokenType == '(':
                self.nextToken()
                node = self.expression([')'])
                self.match(')')
                return node
            else:
                raise ParsingError(
                    'Operand can not start with {} on line {}.'
                    .format(tokenType,
                            self.symbol.startposition[1]))
        except ParsingError as e:
            while True:
                if self.symbol.tokenType in Parser.first('operand'):
                    self.errors.append(e)
                    node = self.operand(followset)
                    return node
                elif self.symbol.tokenType in followset:
                    self.errors.append(e)
                    return ErrorNode(self.symbol)
                elif self.symbol.tokenType == 'eof':
                    raise e
                self.nextToken()

    def operation(self, followset):
        try:
            node = self.matchOperator()
            return node
        except ParsingError as e:
            self.errors.append(e)
            while True:
                if self.symbol.tokenType in Parser.first('operation'):
                    node = self.operation(followset)
                    return node
                elif self.symbol.tokenType in followset:
                    return ErrorNode(self.symbol)
                elif self.symbol.tokenType == 'eof':
                    raise e
                self.nextToken()

    def symbolIsUnary(self):
        return self.symbol.tokenType == '!'
