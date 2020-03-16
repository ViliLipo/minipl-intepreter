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
        refChild = node.getRefChild()
        identifier = refChild.symbol.lexeme
        typeChild = node.getTypeChild()
        identifierType = typeChild.symbol.lexeme
        found = self.symbolTable.get(identifier)
        if found is not None:
            symbol = refChild.symbol
            error = TypeError('already defined', symbol)
            self.errors.append(error)
        else:
            self.symbolTable[identifier] = (
                identifierType,
                TypeCheck.getDefaultValue(identifierType))
            refChild.setEvalType(identifierType)
            if node.hasAssignment():
                node.getAssignChild().accept(self)

    def visitAssignNode(self, node):
        lhs = node.getRefChild()
        lhs.accept(self)
        symbol = lhs.symbol
        identifier = symbol.lexeme
        var = self.symbolTable.get(identifier)
        if var is not None:
            varType, oldValue = var
            rhs = node.getRhsChild()
            rhs.accept(self)
            resultType = rhs.evalType
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
            node.setEvalType(varType)
        else:
            error = TypeError('Reference to an undefined variable',
                              node.symbol)
            node.setEvalType('ErrorType')
            self.errors.append(error)

    def visitPrintNode(self, node):
        self.__visit__(node)

    def visitReadNode(self, node):
        self.__visit__(node)

    def visitAssertNode(self, node):
        argChild = node.getArgumentChild()
        argChild.accept(self)
        argChildType = argChild.evalType
        if argChildType != 'bool':
            error = TypeError('Assert must have a boolean parameter',
                              node.symbol)

    def visitExprNode(self, node):
        op = node.symbol.tokenType
        lhs = node.getLhsChild()
        lhs.accept(self)
        lhsType = lhs.evalType
        rhs = node.getRhsChild()
        rhs.accept(self)
        rhsType = rhs.evalType
        if lhsType == rhsType:
            if op in TypeCheck.returnsBoolOps:
                node.setEvalType('bool')
            elif lhsType == 'int' and op in TypeCheck.intOps:
                node.setEvalType('int')
            elif lhsType == 'string' and op in TypeCheck.strOps:
                node.setEvalType('string')
            elif lhsType == 'bool' and op in TypeCheck.boolOps:
                node.setEvalType('bool')
            else:
                error = TypeError("Cannot apply {} to {}".format(
                    op, lhsType), node.symbol)
                self.errors.append(error)
                node.setEvalType('error')
        else:
            error = TypeError("Mismatched operator types", node.symbol)

    def visitIntegerNode(self, node):
        node.setEvalType('int')

    def visitStringNode(self, node):
        node.setEvalType('string')

    def visitTypeNode(self, node):
        self.__visit__(node)

    def visitStatementListNode(self, node):
        self.__visit__(node)

    def visitForConditionNode(self, node):
        loopVarNode = node.getRefChild()
        loopVarNode.accept(self)
        loopVarType = loopVarNode.evalType
        rangeNode = node.getRangeChild()
        rangeNode.accept(self)
        if loopVarType is None or loopVarType != 'int':
            error = TypeError("Loop variable must be a declared int",
                              node.symbol)
            self.errors.append(error)

    def visitRangeNode(self, node):
        rangeStartNode = node.getStartNode()
        rangeStartNode.accept(self)
        rangeStartType = rangeStartNode.evalType
        rangeEndNode = node.getEndNode()
        rangeEndNode.accept(self)
        rangeEndType = rangeEndNode.evalType
        if not (rangeStartType == 'int' and rangeEndType == 'int'):
            error = TypeError('Range delimiters must be integers',
                              node.symbol)
            self.errors.append(error)

    def visitForNode(self, node):
        self.__visit__(node)

    def visitUnaryExprNode(self, node):
        rhs = node.getRhsChild()
        rhs.accept(self)
        rhsType = rhs.evalType
        if rhsType == 'bool':
            node.setEvalType('bool')
        else:
            node.setEvalType('error')

    def visitNode(self, node):
        self.__visit__(node)
