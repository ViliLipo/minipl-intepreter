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


class ExprNode(Node):
    def __init__(self, parent, symbol):
        super().__init__(parent, symbol)

    def getLhand(self):
        return self.children[0]

    def getRightHand(self):
        return self.children[1]


class AST:

    def __init__(self, symbol):
        self.root = Node(None, symbol)


def makeNode(symbol):
    return Node(symbol)
