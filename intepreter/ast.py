class Node:
    def __init__(self, parent, symbol):
        self.children = []
        self.parent = parent
        self.symbol = symbol

    def isLeaf(self):
        return len(self.children) == 0

    def addChild(self, node):
        self.children.append(node)


class AST:

    def __init__(self, symbol):
        self.root = Node(None, symbol)


