from interpreter.visitor import Visitor


class PrintVisitor(Visitor):

    def __init__(self):
        self.string = ''
        self.childStr = ''
        self.result = ''

    def __visit__(self, node):
        string = "----\n| {}, class: {}, evalType: {}\n|"\
            .format(node.symbol,
                    node.__class__.__name__,
                    node.evalType)
        for child in node.children:
            child.accept(self)
            lines = self.result.splitlines()
            lines = list(map(lambda l: "|\t" + l, lines))
            childStr = ''
            for chidlLine in lines:
                childStr = childStr + "\n" + chidlLine
            string = string + childStr
        self.result = string

    def visitDeclarationNode(self, node):
        self.__visit__(node)

    def visitAssignNode(self, node):
        self.__visit__(node)

    def visitRefNode(self, node):
        self.__visit__(node)

    def visitPrintNode(self, node):
        self.__visit__(node)

    def visitReadNode(self, node):
        self.__visit__(node)

    def visitAssertNode(self, node):
        self.__visit__(node)

    def visitExprNode(self, node):
        self.__visit__(node)

    def visitIntegerNode(self, node):
        self.__visit__(node)

    def visitStringNode(self, node):
        self.__visit__(node)

    def visitTypeNode(self, node):
        self.__visit__(node)

    def visitStatementListNode(self, node):
        self.__visit__(node)

    def visitForConditionNode(self, node):
        self.__visit__(node)

    def visitRangeNode(self, node):
        self.__visit__(node)

    def visitForNode(self, node):
        self.__visit__(node)

    def visitNode(self, node):
        self.__visit__(node)

    def visitUnaryExprNode(self, node):
        self.__visit__(node)
