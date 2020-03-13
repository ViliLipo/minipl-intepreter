class Node:
    def __init__(self, symbol):
        self.children = []
        self.symbol = symbol
        self.evalType = None

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


class ExprNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def getLhand(self):
        return self.children[0]

    def getRightHand(self):
        return self.children[1]

    def accept(self, visitor):
        visitor.visitExprNode(self)


class AssignNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitAssignNode(self)


class PrintNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitPrintNode(self)


class ReadNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitReadNode(self)


class AssertNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitAssertNode(self)


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


class ForConditionNode(Node):
    def __init__(self, symbol):
        super().__init__(symbol)

    def accept(self, visitor):
        visitor.visitForConditionNode(self)


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
    elif tokenType in ['+', '-', '*', '=']:
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
    return Node(symbol)
