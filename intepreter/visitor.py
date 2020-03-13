from abc import ABC, abstractmethod


class Visitor(ABC):

    @abstractmethod
    def visitDeclarationNode(self, node):
        pass

    @abstractmethod
    def visitAssignNode(self, node):
        pass

    @abstractmethod
    def visitRefNode(self, node):
        pass

    @abstractmethod
    def visitPrintNode(self, node):
        pass

    @abstractmethod
    def visitReadNode(self, node):
        pass

    @abstractmethod
    def visitAssertNode(self, node):
        pass

    @abstractmethod
    def visitExprNode(self, node):
        pass

    @abstractmethod
    def visitIntegerNode(self, node):
        pass

    @abstractmethod
    def visitStringNode(self, node):
        pass

    @abstractmethod
    def visitTypeNode(self, node):
        pass

    @abstractmethod
    def visitStatementListNode(self, node):
        pass

    @abstractmethod
    def visitForNode(self, node):
        pass

    @abstractmethod
    def visitForConditionNode(self, node):
        pass

    @abstractmethod
    def visitRangeNode(self, node):
        pass

    @abstractmethod
    def visitUnaryExprNode(self, node):
        pass
