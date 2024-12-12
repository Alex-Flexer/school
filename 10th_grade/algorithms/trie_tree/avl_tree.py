from __future__ import annotations
from typing import Callable, Any
from copy import deepcopy

from bst_tree import BSTNode, Comparable, Compare, Node


class AVLNode[T: Comparable](BSTNode[T]):
    height: int

    def __init__(
        self,
        value: T,
        parent: AVLNode[T] | None = None,
        predicate: Callable[[T, T], Compare] = lambda first, second: (
            Compare.Less
            if first < second
            else (Compare.Greater if first > second else Compare.Equal)
        )
    ) -> None:
        super().__init__(value, parent, predicate)

    def correct(self) -> bool:
        return super().correct() and self._is_balanced()

    def _is_balanced(self):
        l_high = self.left._get_height() + 1 if self.left else 0
        r_high = self.right._get_height() + 1 if self.right else 0
        if abs(l_high - r_high) > 1:
            return False

        if self.left is not None and not self.left._is_balanced():
            return False

        if self.right is not None and not self.right._is_balanced():
            return False
        return True

    def _callback_decorator(func) -> Callable:
        def wrapper(self: AVLNode, *args, **kwargs) -> Any:
            result = func(self, *args, **kwargs)
            self.balance()
            return result
        return wrapper

    def search(self, x: T) -> AVLNode | None:
        return super().search(x)

    @_callback_decorator
    def delete(self, value: T) -> None:
        super().delete(value)

    @_callback_decorator
    def add(self, value: T) -> None:
        compare_result: Compare = self.predicate(self.value, value)
        if compare_result == Compare.Greater:
            if self.left:
                self.left.add(value)
            else:
                self.left = AVLNode(value, self, self.predicate)
        elif compare_result == Compare.Less:
            if self.right:
                self.right.add(value)
            else:
                self.right = AVLNode(value, self, self.predicate)

    @_callback_decorator
    def merge(self, other: AVLNode[T]) -> None:
        self.add(other.value)
        if other.left is not None:
            self.merge(other.left)
        if other.right is not None:
            self.merge(other.right)

    def _update_parents(self):
        if self.right is not None:
            self.right.parent = self
            if self.right.left:
                self.right.left.parent = self.right
            if self.right.right:
                self.right.right.parent = self.right
        if self.left:
            self.left.parent = self
            if self.left.left:
                self.left.left.parent = self.left
            if self.left.right:
                self.left.right.parent = self.left

    def _rotate_left(self) -> None:
        self.value, self.left.value = self.left.value, self.value

        self.right, self.left.left, self.left.right =\
            self.left.left, self.left.right, self.right

        self.left, self.right = self.right, self.left

        self._update_parents()

    def _rotate_right(self) -> None:
        self.value, self.right.value = self.right.value, self.value

        self.left, self.right.right, self.right.left =\
            self.right.right, self.right.left, self.left

        self.left, self.right = self.right, self.left

        self._update_parents()

    def _get_height(self):
        mx_height = 0
        if self.left:
            mx_height = max(mx_height, self.left._get_height() + 1)
        if self.right:
            mx_height = max(mx_height, self.right._get_height() + 1)
        return mx_height

    def _balance(self):
        l_high = self.left._get_height() + 1\
            if self.left is not None\
            else 0

        r_high =\
            self.right._get_height() + 1\
            if self.right is not None\
            else 0

        if abs(r_high - l_high) <= 1:
            return

        if l_high > r_high:
            l_r_high =\
                self.left.right._get_height() + 1\
                if self.left is not None and self.left.right is not None\
                else 0

            l_l_high =\
                self.left.left._get_height() + 1\
                if self.left is not None and self.left.left is not None\
                else 0

            if l_r_high > l_l_high:
                self.left._rotate_right()
            self._rotate_left()
        else:
            r_l_high =\
                self.right.left._get_height() + 1\
                if self.right is not None and self.right.left is not None\
                else 0

            r_r_high =\
                self.right.right._get_height() + 1\
                if self.right is not None and self.right.right is not None\
                else 0

            if r_l_high > r_r_high:
                self.right._rotate_left()
            self._rotate_right()

    def balance(self):
        if self.left is not None:
            self.left.balance()
        if self.right is not None:
            self.right.balance()
        self._balance()


class Tree[T]:
    root: Node[T] | None = None
    predicate: Callable[[T, T], bool]
    tree_type: Node[T]

    def __init__(
            self,
            tree_type: Node[T],
            predicate: Callable[[T, T], Compare] = lambda first, second: (
            Compare.Less
            if first < second
            else (Compare.Greater if first > second else Compare.Equal)
            )
    ) -> None:
        self.predicate = predicate
        self.tree_type = tree_type

    @staticmethod
    def _print_tree(node, level=0, prefix="Root: "):
        if node is not None:
            return "    " * level + prefix + str(node.value) + "\n" +\
                Tree._print_tree(node.left, level + 1, "L--> ") +\
                Tree._print_tree(node.right, level + 1, "R--> ")
        else:
            return "    " * level + prefix + "None" + "\n"

    def __str__(self):
        return Tree._print_tree(self.root)

    def correct(self) -> bool:
        return self.root is None or self.root.correct()

    def add(self, value) -> None:
        if self.root is None:
            self.root = self.tree_type(value, predicate=self.predicate)
        else:
            self.root.add(value)

    def delete(self, value) -> None:
        if self.root is not None:
            if self.predicate(self.root.value, value) == Compare.Equal and\
                    self.root.right is None and\
                    self.root.left is None:
                self.root = None
            else:
                self.root.delete(value)
        else:
            raise KeyError("Tree is empty")

    def merge(self, other: Tree[T]) -> None:
        if other.root is not None:
            if self.root is not None:
                self.root.merge(other.root)
            else:
                self.root = deepcopy(other.root)

    def search(self, value: T) -> Node[T]:
        if self.root is not None:
            return self.root.search(value)

    def to_list(self) -> list[T]:
        return [] if self.root is None else self.root.to_list()
