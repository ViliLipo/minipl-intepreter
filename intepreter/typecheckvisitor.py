from intepreter.visitor import Visitor


class TypeError():

    def __init__(self, description, symbol):
        self.description = description
        self.symbol = symbol

    def __str__(self):
        return self.description + ": on line "\
                + str(self.symbol.startposition[1])

    def __repr__(self):
        return self.__str__()


class TypeCheck(Visitor):

    def __init__(self):
        self.symbolTable = {}
        self.errors = []
        self.resultHolder = None

    intOps = ['+', '-', '*', '/', '=', '<']
    strOps = ['+', '=', '<']
    boolOps = ['&', '=', '<']
    returnsBoolOps = ['=', '<']

    def __visit__(self, node):
        for child in node.children:
            child.accept(self)

    def getDefaultValue(typeString):
        if typeString in ['int', 'bool']:
            return 0
        elif typeString == 'string':
            return ''

    def visitDeclarationNode(self, node):
        identifier = node.children[0].symbol.lexeme
        identifierType = node.children[1].symbol.lexeme
        found = self.symbolTable.get(identifier)
        if found is not None:
            symbol = node.children[0].symbol
            error = TypeError('already defined', symbol)
            self.errors.append(error)
        else:
            self.symbolTable[identifier] = (
                identifierType,
                TypeCheck.getDefaultValue(identifierType))
            node.setEvalType(identifierType)
            if len(node.children) == 3:
                assignChild = node.children[2]
                assignChild.accept(self)

    def visitAssignNode(self, node):
        symbol = node.children[0].symbol
        identifier = symbol.lexeme
        var = self.symbolTable.get(identifier)
        if var is not None:
            varType, oldValue = var
            node.children[1].accept(self)
            resultType = self.resultHolder
            if varType != resultType:
                print(varType, resultType)
                error = TypeError('assigment to uncombatible type', symbol)
                self.errors.append(error)
        else:
            error = TypeError('Assigment to undefied variable', node.symbol)
            self.errors.append(error)

    def visitRefNode(self, node):
        lexeme = node.symbol.lexeme
        var = self.symbolTable.get(lexeme)
        if var is not None:
            varType, value = var
            self.resultHolder = varType
        else:
            error = TypeError('Reference to an undefined variable',
                              node.symbol)
            self.resultHolder = None
            self.errors.append(error)

    def visitPrintNode(self, node):
        self.__visit__(node)

    def visitReadNode(self, node):
        self.__visit__(node)

    def visitAssertNode(self, node):
        self.__visit__(node)

    def visitExprNode(self, node):
        # TODO: UNARY !
        op = node.symbol.tokenType
        node.children[0].accept(self)
        lhsType = self.resultHolder
        node.children[1].accept(self)
        rhsType = self.resultHolder
        if lhsType == rhsType:
            if op in TypeCheck.returnsBoolOps:
                self.resultHolder = 'bool'
            elif lhsType == 'int' and op in TypeCheck.intOps:
                self.resultHolder = 'int'
                node.setEvalType('int')
            elif lhsType == 'string' and op in TypeCheck.strOps:
                self.resultHolder = 'string'
                node.setEvalType('string')
            elif lhsType == 'bool' and op in TypeCheck.boolOps:
                self.resultHolder = 'bool'
                node.setEvalType('bool')
            else:
                error = TypeError("Cannot apply {} to {}".format(
                    op, lhsType), node.symbol)
                self.resultHolder = None
                self.errors.append(error)
        else:
            error = TypeError("Mismatched operator types", node.symbol)

    def visitIntegerNode(self, node):
        self.resultHolder = 'int'
        node.setEvalType('int')

    def visitStringNode(self, node):
        self.resultHolder = 'string'
        node.setEvalType('string')

    def visitTypeNode(self, node):
        self.__visit__(node)

    def visitStatementListNode(self, node):
        self.__visit__(node)

    def visitForConditionNode(self, node):
        loopVarNode = node.children[0]
        loopVarNode.accept(self)
        loopVarType = self.resultHolder
        rangeStartNode = node.children[1]
        rangeStartNode.accept(self)
        rangeStartType = self.resultHolder
        rangeEndNode = node.children[2]
        rangeEndNode.accept(self)
        rangeEndType = self.resultHolder
        if loopVarType is not None and loopVarType == 'int':
            if ((rangeStartType is not None and rangeStartType == 'int')
                    and (rangeEndType is not None
                         and rangeEndType == 'int')):
                self.resultHolder = None
            else:
                error = TypeError('Range delimiters must be integers',
                                  loopVarNode.symbol)
                self.errors.append(error)
                pass
        else:
            error = TypeError("Loop variable must be a declared int",
                              node.symbol)
            self.errors.append(error)

        self.__visit__(node)

    def visitForNode(self, node):
        self.__visit__(node)

    def visitUnaryExprNode(self, node):
        self.__visit__(node)

    def visitNode(self, node):
        self.__visit__(node)
