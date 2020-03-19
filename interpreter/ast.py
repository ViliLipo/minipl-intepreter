class Node:
    def __init__(self, symbol):
        self.children = []
        self.symbol = symbol
        self.evalType = None
        self.evalValue = None

    def __str__(self):
        string = "-----\n| {}, class: {}\n|".format(
            str(self.symbol), self.__class__.__name__)
        for child in self.children:
            lines = str(child).splitlines()
            lines = list(map(lambda l: "|\t" + l, lines))
            childStr = ''
            for chidlLine in lines:
                childStr = childStr + "\n" + chidlLine
            string = string + childStr
        return string

    def __repr__(self):
        return str(self)

    def isLeaf(self):
        return len(self.children) == 0

    def addChild(self, node):
        self.children.append(node)

    def accept(self, visitor):
        visitor.visitNode(self)

    def setEvalType(self, evalType):
        self.evalType = evalType

    def setEvalValue(self, evalValue):
        self.evalValue = evalValue


class ExprNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def getLhsChild(self):
        return self.children[0]

    def getRhsChild(self):
        return self.children[1]

    def accept(self, visitor):
        visitor.visitExprNode(self)


class AssignNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitAssignNode(self)

    def getRefChild(self):
        return self.children[0]

    def getRhsChild(self):
        return self.children[1]


class PrintNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitPrintNode(self)

    def getPrintableChild(self):
        return self.children[0]


class ReadNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitReadNode(self)

    def getTargetChild(self):
        return self.children[0]


class AssertNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitAssertNode(self)

    def getArgumentChild(self):
        return self.children[0]


class RefNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitRefNode(self)


class DeclarationNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitDeclarationNode(self)

    def hasAssignment(self):
        return len(self.children) == 3

    def getRefChild(self):
        return self.children[0]

    def getTypeChild(self):
        return self.children[1]

    def getAssignChild(self):
        return self.children[2]


class IntegerNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitIntegerNode(self)


class StringNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitStringNode(self)


class TypeNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitTypeNode(self)


class ForNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitForNode(self)

    def getConditionChild(self):
        return self.children[0]

    def getBodyChild(self):
        return self.children[1]


class ForConditionNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitForConditionNode(self)

    def getRefChild(self):
        return self.children[0]

    def getRangeChild(self):
        return self.children[1]


class RangeNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitRangeNode(self)

    def getStartNode(self):
        return self.children[0]

    def getEndNode(self):
        return self.children[1]


class StatementListNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitStatementListNode(self)


class UnaryExprNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitUnaryExprNode(self)

    def getRhsChild(self):
        return self.children[0]


class ErrorNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)


def makeNode(symbol=None):
    if symbol is None:
        return StatementListNode(None)
    tokenType = symbol.tokenType
    if tokenType == 'var':
        return DeclarationNode(symbol)
    elif tokenType == 'read':
        return ReadNode(symbol)
    elif tokenType == 'print':
        return PrintNode(symbol)
    elif tokenType == 'assert':
        return AssertNode(symbol)
    elif tokenType == 'identifier':
        return RefNode(symbol)
    elif tokenType == ':=':
        return AssignNode(symbol)
    elif tokenType in ['+', '-', '*', '/', '=']:
        return ExprNode(symbol)
    elif tokenType == '!':
        return UnaryExprNode(symbol)
    elif tokenType == "string_literal":
        return StringNode(symbol)
    elif tokenType == "integer":
        return IntegerNode(symbol)
    elif tokenType in ['string', 'int', 'bool']:
        return TypeNode(symbol)
    elif tokenType == "for":
        return ForNode(symbol)
    elif tokenType == "in":
        return ForConditionNode(symbol)
    elif tokenType == "do":
        return StatementListNode(symbol)
    elif tokenType == '..':
        return RangeNode(symbol)
    elif tokenType == 'error':
        return ErrorNode(symbol)
    return Node(symbol)
