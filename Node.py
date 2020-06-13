from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from collections.abc import Iterable, Iterator


class Node(Iterable):
    """
    Patterns:
        Composite
        Iterator

    Base class for iterable expression tree
    """
    def __iter__(self) -> TreeTraversalIterator:
        return TreeIterator(self.root)

    def __repr__(self):
        return self.value()

    def operands(self):
        return OperandIterator(self.root)

    def operations(self):
        return OperationIterator(self.root)

    @property
    def root(self) -> Node:
        return self._root

    @root.setter
    def root(self, root: Node):
        self._root = root

    @property
    def parent(self) -> Node:
        return self._parent

    @parent.setter
    def parent(self, parent: Node):
        self._parent = parent

    @property
    def sibling(self) -> Node:
        return self._sibling

    @sibling.setter
    def sibling(self, sibling: Node):
        self._sibling = sibling

    @property
    def left_child(self) -> Node:
        return self._left_child

    @left_child.setter
    def left_child(self, left_child: Node):
        self._left_child = left_child

    @property
    def right_child(self) -> Node:
        return self._right_child

    @right_child.setter
    def right_child(self, right_child: Node):
        self._right_child = right_child

    @property
    def a(self) -> int:
        return self._a

    @a.setter
    def a(self, value: int):
        self._a = value

    @property
    def b(self) -> int:
        return self._b

    @b.setter
    def b(self, value: int):
        self._b = value

    def is_operation(self) -> bool:
        return False

    def value(self) -> str:
        return self._value


class Operation(Node):
    """
    Composite - Tree node representing arithmetic operations:
    """
    def __init__(self, value: Any) -> None:
        self._left_child = None
        self._right_child = None
        self._parent = None
        self._sibling = None
        self._root = None
        self._value = value
        self._a: int = 1
        self._b: int = 0

    def is_operation(self) -> bool:
        return True


class Operand(Node):
    """
    Tree leaf representing expression operand
    """
    def __init__(self, value: Any) -> None:
        self._left_child = None
        self._right_child = None
        self._parent = None
        self._sibling = None
        self._value = value
        self._root = None
        self._a: int = 1
        self._b: int = 0


class TreeTraversalIterator(ABC, Iterator):
    """
    Patterns:
        Template Method
        Iterator

    Postorder tree traversal Iterator with Template Method
    """
    def __init__(self, tree: Node) -> None:
        self._collection = []
        self._position: int = 0
        self._tree = tree
        self.postorder(self._tree)

    def peek(self, stack):
        if len(stack) > 0:
            return stack[-1]
        return None

    @abstractmethod
    def add_to_collection(self, node: Node):
        self._collection.append(node)

    def postorder(self, node: Node):
        if node is None:
            return
        stack = []

        while True:
            while node:
                if node.right_child is not None:
                    stack.append(node.right_child)
                stack.append(node)
                node = node.left_child
            node = stack.pop()
            if (node.right_child is not None and
                    self.peek(stack) == node.right_child):
                stack.pop()
                stack.append(node)
                node = node.right_child
            else:
                self.add_to_collection(node)
                if node.root:
                    break
                node = None
            if len(stack) <= 0:
                break

    def __next__(self):
        try:
            value = self._collection[self._position]
            self._position += 1

        except IndexError:
            raise StopIteration()

        return value


class TreeIterator(TreeTraversalIterator):
    """
    Method extending TreeTraversalIterator template method
    """
    def add_to_collection(self, node: Node):
        self._collection.append(node)


class OperandIterator(TreeTraversalIterator):
    """
    Method extending TreeTraversalIterator template method
    """
    def add_to_collection(self, node: Node):
        if type(node) is Operand:
            self._collection.append(node)


class OperationIterator(TreeTraversalIterator):
    """
    Method extending TreeTraversalIterator template method
    """
    def add_to_collection(self, node: Node):
        if type(node) is Operation:
            self._collection.append(node)
