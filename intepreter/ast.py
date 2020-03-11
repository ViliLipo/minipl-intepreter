class Node:
    def __init__(self, symbol):
        self.children = []
        self.symbol = symbol

    def __str__(self):
        string = "-----\n| " + str(self.symbol) + "\n|"
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


def makeNode(symbol):
    tokenType = symbol.tokenType
    if tokenType == "var":
        return AssignNode(symbol)
    elif tokenType == "read":
        return ReadNode(symbol)
    return Node(symbol)
