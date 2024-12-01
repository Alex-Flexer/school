from __future__ import annotations
from typing import Callable
from copy import deepcopy

from bst_tree import BSTNode, Comparable, Compare, EmptyValue, Node


class AVLNode[T: Comparable](BSTNode[T]):
    height: int

    def __init__(
        self,
        value: T | EmptyValue = EmptyValue(),
        parent: AVLNode[T] | None = None,
        predicate: Callable[[T, T], Compare] = lambda first, second: (
            Compare.Less
            if first < second
            else (Compare.Greater if first > second else Compare.Equal)
        )
    ) -> None:
        super().__init__(value, parent, predicate)

    def correct(self) -> bool:
        if self.left is not None:
            if self.predicate(self.left.value, self.value) != Compare.Less:
                return False
            if not self.left.correct():
                return False
        if self.right is not None:
            if self.predicate(self.right.value, self.value) != Compare.Greater:
                return False
            if not self.right.correct():
                return False
        return True
    
    def is_balanced(self):
        l_high = self.left._get_height() if self.left else -1
        r_high = self.right._get_height() if self.right else -1
        if abs(l_high - r_high) > 1:
            return False
        if self.left is not None and not self.left.is_balanced():
            return False
        if self.right is not None and not self.right.is_balanced():
            return False
        return True

    def _callback_decorator(func):
        def wrapper(self: AVLNode, *args, **kwargs) :
            result = func(self, *args, **kwargs)
            self.balance()
            return result
        return wrapper

    def search(self, x: T) -> AVLNode | None:
        if isinstance(self.value, EmptyValue):
            return None

        if self.predicate(self.value, x) == Compare.Equal:
            return self

        if self.predicate(self.value, x) == Compare.Greater:
            return self.left.search(x) if self.left else None
        else:
            return self.right.search(x) if self.right else None

    @_callback_decorator
    def delete(self, value: T) -> None:
        super().delete(value)

    @_callback_decorator
    def add(self, value: T) -> None:
        if isinstance(self.value, EmptyValue):
            self.value = value

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
        l_high = self.left._get_height() if self.left else -1
        r_high = self.right._get_height() if self.right else -1
        if abs(r_high - l_high) <= 1:
            return

        if l_high > r_high:
            l_r_high = self.left.right._get_height() if self.left and self.left.right else -1
            l_l_high = self.left.left._get_height() if self.left and self.left.left else -1
            if l_r_high > l_l_high:
                self.left._rotate_right()
            self._rotate_left()
        else:
            r_l_high = self.right.left._get_height() if self.right and self.right.left else -1
            r_r_high = self.right.right._get_height() if self.right and self.right.right else -1
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

    def add(self, value) -> None:
        if self.root is None:
            self.root = self.tree_type(value, predicate=self.predicate)
        else:
            self.root.add(value)
    
    def delete(self, value) -> None:
        if self.root is not None:
            self.root.delete(value)
    
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


a = Tree[int](AVLNode)
for el in [3, 8, 11, 14, 16, 21, 23, 25]:
    a.add(el)

print(a.to_list())
a.delete(8)
nodes = a.to_list()
for node_ind in nodes:
    node = a.search(node_ind)
    print(f"{node.parent.value if node.parent else 'No'} -> {node.value}. left: {node.left.value if node.left else 'No'}. right: {node.right.value if node.right else 'No'}")
print(a.to_list())

# tree = AVLNode(5)
# for i in range(6, 10):
#     tree.add(i)

# for i in range(0, 5):
#     tree.add(i)

# print(tree.is_balanced())
# tree.balance()
# print(tree.is_balanced())

# print(tree.to_list())
