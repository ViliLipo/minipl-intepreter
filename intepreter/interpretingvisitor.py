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
        value = str(child.evalValue)
        text = value.replace('\\n', "\n")
        print(text, end='')

    def visitReadNode(self, node):
        child = node.getTargetChild()
        identifier = child.symbol.lexeme
        varType, value = self.symboltable.get(identifier)
        newValue = input()
        if newValue.isdigit() and varType == 'int':
            self.symboltable[identifier] = (varType, int(newValue))
        elif varType == 'string':
            self.symboltable[identifier] = (varType, str(newValue))

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
        refChild = node.getRefChild()
        rangeChild = node.getRangeChild()
        refChild.accept(self)
        rangeChild.accept(self)
        refVal = refChild.evalValue
        ran = rangeChild.evalValue
        node.setEvalValue((refVal, ran))

    def visitRangeNode(self, node):
        start = node.getStartNode()
        start.accept(self)
        startValue = start.evalValue
        end = node.getEndNode()
        end.accept(self)
        endValue = end.evalValue + 1
        node.setEvalValue(range(startValue, endValue))

    def visitForNode(self, node):
        condition = node.getConditionChild()
        condition.accept(self)
        refVal, ran = condition.evalValue
        body = node.getBodyChild()
        identifier = condition.getRefChild().symbol.lexeme
        t, var = self.symboltable[identifier]
        for i in ran:
            self.symboltable[identifier] = (t, i)
            body.accept(self)

    def visitNode(self, node):
        pass

    def visitUnaryExprNode(self, node):
        rhs = node.getRhsChild()
        rhs.accept(self)
        value = rhs.evalValue
        node.setEvalValue(not value)
