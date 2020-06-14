from __future__ import annotations
from Node import *
from infixToPostfix import infix_to_postfix as parse_expr


class Builder(ABC):
    """
    Tree Builder interface

    """

    @property
    def node(self) -> None:
        pass

    @node.setter
    def node(self, value):
        pass

    @abstractmethod
    def add_node(self, node: Node) -> None:
        pass

    @abstractmethod
    def create_expression_tree(self) -> None:
        pass


class ExpressionTreeBuilder(Builder):
    """
    Concrete Expression Tree Builder
    """
    def __init__(self) -> None:
        self.operators = ['+', '-', '*', '/', '^']
        self.tree_stack = []
        self.stack = []

    @property
    def node(self) -> Node:
        return self._node

    @node.setter
    def node(self, value):
        self._node = value

    def add_node(self, token: str) -> None:
        self.tree_stack.append(
            Operation(token) if token in self.operators else Operand(token)
        )

    def set_children_parameters(self) -> None:
        self.node.left_child.parent = self.node
        self.node.right_child.parent = self.node
        self.node.left_child.sibling = self.node.right_child
        self.node.right_child.sibling = self.node.left_child

    def create_expression_tree(self) -> Node:
        for node in self.tree_stack:
            self.node = node
            if type(node) == Operand:
                self.stack.append(node)
            else:
                if len(self.stack) > 1:
                    self.node.right_child = self.stack.pop()
                    self.node.left_child = self.stack.pop()
                    self.set_children_parameters()
                    self.stack.append(node)
        if len(self.stack) == 1:
            self.node.root = self.stack.pop()

            self.set_children_parameters()
        return builder.node.root


class Director:
    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        """
        The Director works with any builder instance that the client code passes
        to it. This way, the client code may alter the final type of the newly
        assembled product.
        """
        self._builder = builder

    """
    The Director can construct several product variations using the same
    building steps.
    """

    def build_expression_tree(self, tokens: list) -> Node:

        [builder.add_node(token) for token in tokens]

        ex_tree = builder.create_expression_tree()

        return ex_tree


class TreeDecorator(Node):
    """
    Tree Decorator class follows the same interface as Node component.
    """
    _node: Node

    def __init__(self, node: Node) -> None:
        self._node = node

    @property
    def node(self) -> Node:
        return self._node

    @node.setter
    def node(self, node: Node):
        self._node = node

    def __iter__(self) -> TreeTraversalIterator:
        return TreeIterator(self._node.root)

    def operands(self):
        return OperandIterator(self._node.root)

    def operations(self):
        return OperationIterator(self._node.root)

    @property
    def sibling(self) -> Node:
        return self._node.sibling

    @sibling.setter
    def sibling(self, node: Node):
        self._node.sibling = node

    @property
    def root(self) -> Node:
        return self._node.root

    @root.setter
    def root(self, root: Node):
        self._node.root = root

    @property
    def parent(self) -> Node:
        return self._node.parent

    @parent.setter
    def parent(self, parent: Node):
        self._node.parent = parent

    @property
    def left_child(self) -> Node:
        return self._node.left_child

    @left_child.setter
    def left_child(self, left_child: Node):
        self._node.left_child = left_child

    @property
    def right_child(self) -> Node:
        return self._node.right_child

    @right_child.setter
    def right_child(self, right_child: Node):
        self._node.right_child = right_child

    @property
    def a(self) -> int:
        return self._node.a

    @a.setter
    def a(self, value: int):
        self._node.a = value

    @property
    def b(self) -> int:
        return self._node.b

    @b.setter
    def b(self, value: int):
        self._node.b = value

    def is_operation(self) -> bool:
        return self._node.is_operation()

    def value(self) -> str:
        return self._node.value()


class TreeContractor(TreeDecorator):
    """
    Concrete decorator class wrapping expression tree,
    providing rake() operation and additional parameters
    """
    def __init__(self, node: Node):
        super().__init__(node)

    def left_rake(self):
        self.node.parent.left_child = None
        if self.node.parent == self.node.parent.parent.left_child:
            self.node.parent.parent.left_child = self.node.parent.right_child
        elif self.node.parent == self.node.parent.parent.right_child:
            self.node.parent.parent.right_child = self.node.parent.right_child
        self.node.parent.right_child.parent = self.node.parent.parent
        self.node.parent.right_child = None
        self.node.parent.parent = None
        self.node.parent = None

    def right_rake(self):
        self.node.parent.right_child = None
        if self.node.parent == self.node.parent.parent.left_child:
            self.node.parent.parent.left_child = self.node.parent.left_child
        elif self.node.parent == self.node.parent.parent.right_child:
            self.node.parent.parent.right_child = self.node.parent.left_child
        self.node.parent.left_child.parent = self.node.parent.parent
        self.node.parent.left_child = None
        self.node.parent.parent = None
        self.node.parent = None

    def rake(self) -> (int, int, int):
        if self.node.parent is None:
            pass
        else:
            operation = self.node.parent.value()

            if self.node == self.node.parent.left_child:
                print("Left child")
                self.node.sibling = self.node.parent.right_child
            elif self.node == self.node.parent.right_child:
                print("Right child")
                self.node.sibling = self.node.parent.left_child

            if operation == '+':
                a_prim_w, b_prim_w = self.addition()
            elif operation == '*':
                a_prim_w, b_prim_w = self.multiplication()

            self.node.sibling.a = a_prim_w
            self.node.sibling.b = b_prim_w

            if self.node == self.node.parent.left_child:
                self.left_rake()
            elif self.node == self.node.parent.right_child:
                self.right_rake()
        return self.node.sibling.value(), a_prim_w, b_prim_w

    def addition(self) -> (int, int):
        """
        Jezeli w u jest dodawanie
        """
        a_u = self.node.parent.a
        a_v = self.node.a
        a_w = self.node.sibling.a

        b_u = self.node.parent.b
        b_v = self.node.b
        b_w = self.node.sibling.b

        c_v = self.node.value()

        a_prim_w = a_u * a_w
        b_prim_w = a_u * (a_v * int(c_v) + int(b_v) + int(b_w)) + int(b_u)

        print(f"""
*** Rake ***
Operation: (+)
Node value = {c_v}
(A_u, B_u)           = ({a_u}, {b_u})
(A_v, B_v)           = ({a_v}, {b_v})
(A_w, B_w)           = ({a_w}, {b_w})
(A_prim_w, B_prim_w) = ({a_prim_w}, {b_prim_w})
        """)

        return a_prim_w, b_prim_w

    def multiplication(self) -> (int, int):
        """
        Jezeli w u jest mnożenie
        """
        a_u = self.node.parent.a
        a_v = self.node.a
        a_w = self.node.sibling.a

        b_u = self.node.parent.b
        b_v = self.node.b
        b_w = self.node.sibling.b

        c_v = self.node.value()

        a_prim_w = a_u * (a_v * int(c_v) + int(b_v)) * a_w
        b_prim_w = a_u * (a_v * int(c_v) + int(b_v)) * int(b_w) + int(b_u)

        print(f"""
*** Rake ***
Operation: (*)
Node value = {c_v}
(A_u, B_u)           = ({a_u}, {b_u})
(A_v, B_v)           = ({a_v}, {b_v})
(A_w, B_w)           = ({a_w}, {b_w})
(A_prim_w, B_prim_w) = ({a_prim_w}, {b_prim_w})
        """)

        return a_prim_w, b_prim_w


if __name__ == "__main__":

    director = Director()
    builder = ExpressionTreeBuilder()
    director.builder = builder

    # nie działa z liczbami ujemnymi i ze spacjami
    # expression = "( ( ( ( ( 4 + 5 ) * 2 ) + ( 2 + ( -5 ) ) ) * 2 ) + 2 )"
    # expression = "((2+3)*2)+(((2+1)*3)*3)"
    # expression = "((2+3)·2)+((4·2)+2)"
    # expression = "((((2+1)+3)·2)+1)+(2·(1+(3+(2·2))))"
    expression = "((2+3)·2)+((4·2)+2)"

    print("Expression: " + expression)
    expression_tree = director.build_expression_tree(parse_expr(expression))

    print("------------------")
    print([x for x in expression_tree])
    print("------------------")
    print("")
    a = []
    a_odd = []
    a_even = []

    [a.append(x) for x in expression_tree.operands()]
    a = a[1:-1]
    iter_nr = 1

    tc_root = TreeContractor(expression_tree)

    result = []

    while len(a) > 0:
        print(f"A = {a}")
        for i, value in enumerate(a):
            if i % 2 == 0:
                a_odd.append(value)
            else:
                a_even.append(value)
        print("")
        print("----------")
        print(f"Iteration {iter_nr}")
        print("----------")
        print("")
        print("(1)")
        print("")
        print(f"A_odd = {a_odd}")
        print(f"A_even = {a_even}")
        print("")
        print("(2a)")

        next_iter = []

        for node in a_odd:
            tc = TreeContractor(node)
            if tc.node.parent is not None:
                if tc.node.parent.left_child is not None:
                    if tc.node == tc.node.parent.left_child:
                        value, a, b = tc.rake()
                        result.append((value, a, b))
                    else:
                        next_iter.append(node)

        a_odd = next_iter
        next_iter = []
        print(f"A_odd = {a_odd}")
        print("")
        print("(2b)")
        print("")
        for node in a_odd:
            tc = TreeContractor(node)
            value, a, b = tc.rake()
            result.append((value, a, b))
        a_odd = []
        print("(2c)")
        print("")
        a = a_even
        a_even = []
        iter_nr += 1

    print(f"Two remaining nodes: {result[-2]}, {result[-1]}")
    print("Note: check above which one is left and which is right")
    print("")

    a_x, val_x, b_x = result.pop()
    a_y, val_y, b_y = result.pop()
    res_x = int(a_x) * val_x + b_x
    res_y = int(a_y) * val_y + b_y

    operand = expression_tree.value()

    if operand == '+':
        print(f'Result = {res_x} + {res_y} = {res_x + res_y}')
    if operand == '*':
        print(f'Result = {res_x} * {res_y} = {res_x * res_y}')
