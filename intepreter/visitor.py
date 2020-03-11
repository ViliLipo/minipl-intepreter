from abc import ABC, abstractmethod


class Visitor(ABC):

    @abstractmethod
    def visitAssignmentNode(self, node):
        raise NotImplementedError("Override this method in subclass")

    @abstractmethod
    def visitRefNode(self, node):
        raise NotImplementedError("Override this method in subclass")

    @abstractmethod
    def visitPrintNode(self, node):
        raise NotImplementedError("Override this method in subclass")

    @abstractmethod
    def visitReadNode(self, node):
        raise NotImplementedError("Override this method in subclass")

    @abstractmethod
    def visitAssertNode(self, node):
        raise NotImplementedError("Override this method in subclass")

    @abstractmethod
    def visitExpr(self, node):
        raise NotImplementedError("Override this method in subclass")
