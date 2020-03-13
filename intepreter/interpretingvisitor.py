from intepreter.visitor import Visitor
from math import floor


class InterpretingVisitor():

    def __init__(self, symboltable):
        self.symboltable = symboltable
        self.errors = []

    def visitDeclarationNode(self, node):
        if node.hasAssignment():
            node.getAssignChild().accept(self)

    def visitAssignNode(self, node):
        lhs = node.getRefChild()
        symbol = lhs.symbol
        identifier = symbol.lexeme
        var = self.symboltable.get(identifier)
        varType, oldVal = var
        rhs = node.getRhsChild()
        rhs.accept(self)
        newVal = rhs.evalValue
        self.symboltable[identifier] = (varType, newVal)

    def visitRefNode(self, node):
        identifier = node.symbol.lexeme
        var = self.symboltable.get(identifier)
        varType, value = var
        node.setEvalValue(value)

    def visitPrintNode(self, node):
        child = node.getPrintableChild()
        child.accept(self)
        value = child.evalValue
        print(value)

    def visitReadNode(self, node):
        child = node.getTargetChild()
        identifier = child.symbol.lexeme
        varType, value = self.symboltable.get(identifier)
        newValue = input()
        if newValue.isdigit() and varType == 'int':
            self.symboltable[identifier] = (varType, newValue)
        elif varType == 'string':
            self.symboltable[identifier] = (varType, newValue)

    def visitAssertNode(self, node):
        argChild = node.getArgumentChild()
        argChild.accept(self)
        value = argChild.evalValue
        if not value:
            print('Assertion error at {}'
                  .format(argChild.symbol.startposition))

    def visitExprNode(self, node):
        op = node.symbol.tokenType
        lhs = node.getLhsChild()
        lhs.accept(self)
        lhsValue = lhs.evalValue
        lhsType = lhs.evalType
        rhs = node.getRhsChild()
        rhs.accept(self)
        rhsValue = rhs.evalValue
        if lhsType == 'int':
            if op == '+':
                node.setEvalValue(rhsValue + lhsValue)
            if op == '-':
                node.setEvalValue(lhsValue - rhsValue)
            if op == '*':
                node.setEvalValue(lhsValue * rhsValue)
            if op == '/':
                node.setEvalValue(floor(lhs / rhs))
            if op == '=':
                node.setEvalValue(lhsValue == rhsValue)
        elif lhsType == 'string':
            if op == '+':
                node.setEvalValue(lhsValue + rhsValue)
            if op == '=':
                node.setEvalValue(lhsValue == rhsValue)
        elif lhsType == 'bool':
            if op == '&':
                node.setEvalValue(lhsValue and rhsValue)
            if op == '=':
                node.setEvalValue(lhsValue == rhsValue)
            if op == '<':
                node.setEvalValue(lhsValue < rhsValue)

    def visitIntegerNode(self, node):
        lexeme = node.symbol.lexeme
        node.setEvalValue(int(lexeme))

    def visitStringNode(self, node):
        lexeme = node.symbol.lexeme
        text = lexeme[1:][:-1]
        node.setEvalValue(text)

    def visitTypeNode(self, node):
        pass

    def visitStatementListNode(self, node):
        for child in node.children:
            child.accept(self)

    def visitForConditionNode(self, node):
        pass

    def visitRangeNode(self, node):
        pass

    def visitForNode(self, node):
        pass

    def visitNode(self, node):
        pass

    def visitUnaryExprNode(self, node):
        rhs = node.getRhsChild()
        rhs.accept(self)
        value = rhs.evalValue
        node.setEvalValue(not value)
