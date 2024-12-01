from __future__ import annotations
from abc import ABCMeta, abstractmethod
from enum import Enum, auto
from typing import Any, Callable


class Compare(Enum):
    Less = auto()
    Equal = auto()
    Greater = auto()


class Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: Any) -> bool: ...

    @abstractmethod
    def __gt__(self, other: Any) -> bool: ...

    @abstractmethod
    def __eq__(self, other: Any) -> bool: ...


class Node[T](metaclass=ABCMeta):
    value: T
    left: Node[T] | None
    right: Node[T] | None
    parent: Node[T] | None

    @abstractmethod
    def __init__(self, parent: Node[T], preditcate: Callable[[T, T], bool]): ...

    @abstractmethod
    def add(self, other: T) -> None: ...

    @abstractmethod
    def delete(self, other: T) -> None: ...

    @abstractmethod
    def merge(self, other: Node) -> None: ...

    @abstractmethod
    def to_list(self) -> list[T]: ...

    @abstractmethod
    def search(self, other: Node) -> Node[T] | None: ...


class EmptyValue:
    def __init__(self):
        ...


class BSTNode[T: Comparable]:
    value: T | EmptyValue
    left: BSTNode[T] | None
    right: BSTNode[T] | None
    parent: BSTNode[T] | None
    predicate: Callable[[T, T], Compare]

    def __init__(
        self,
        value: T | EmptyValue = EmptyValue(),
        parent: BSTNode[T] | None = None,
        predicate: Callable[[T, T], Compare] = lambda first, second: (
            Compare.Less
            if first < second
            else (Compare.Greater if first > second else Compare.Equal)
        )
    ) -> None:
        self.value = value
        self.predicate = predicate
        self.left = None
        self.right = None
        self.parent = parent

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

    def search(self, x: T) -> BSTNode | None:
        if isinstance(self.value, EmptyValue):
            return None

        if self.predicate(self.value, x) == Compare.Equal:
            return self

        if self.predicate(self.value, x) == Compare.Greater:
            return self.left.search(x) if self.left else None
        else:
            return self.right.search(x) if self.right else None

    def delete(self, value: T) -> None:
        if isinstance(self.value, EmptyValue):
            return

        if self.predicate(self.value, value) == Compare.Greater:
            if self.left is not None:
                if self.predicate(self.left.value, value) == Compare.Equal:
                    if self.left.left is not None:
                        if self.left.left.right is not None:
                            self.left.left.right.merge(self.left.right)
                        else:
                            self.left.left.right = self.left.right
                        self.left.left.parent = self
                        self.left = self.left.left

                    elif self.left.right is not None:
                        self.left.right.parent = self
                        self.right = self.left.right
                    else:
                        self.left = None
                else:
                    self.left.delete(value)
            else:
                raise KeyError(f"There is no node with value {value}")
        elif self.predicate(self.value, value) == Compare.Less:
            if self.right is not None:
                if self.predicate(self.right.value, value) == Compare.Equal:
                    if self.right.left is not None:
                        if self.right.left.right is not None:
                            self.right.left.right.merge(self.right.right)
                        else:
                            self.right.left.right = self.right.right
                        self.right.left.parent = self.right
                        self.right = self.right.left

                    elif self.right.right is not None:
                        self.right.right.parent = self.right
                        self.right = self.right.right
                    else:
                        self.right = None
                else:
                    self.right.delete(value)
            else:
                raise KeyError(f"There is no node with value {value}")
        else:
            # deletion of root
            if self.left is not None:
                if self.left.right is not None:
                    if self.right is None:
                        self.right = self.left.right
                    else:
                        self.right.merge(self.left.right)
                    self.left.right = None

                self.value = self.left.value
                self.left = self.left.left
            elif self.right is not None:
                if self.right.left is not None:
                    if self.left is None:
                        self.left = self.right.left
                    else:
                        self.left.merge(self.right.left)
                        self.right.left = None

                self.value = self.right.value
                self.right = self.right.right
            else:
                self.value = EmptyValue()

    def add(self, value: T) -> None:
        if isinstance(self.value, EmptyValue):
            self.value = value

        if self.predicate(self.value, value) == Compare.Greater:
            if self.left:
                self.left.add(value)
            else:
                self.left = BSTNode(value, self, self.predicate)
        elif self.predicate(self.value, value) == Compare.Less:
            if self.right:
                self.right.add(value)
            else:
                self.right = BSTNode(value, self, self.predicate)

    def merge(self, other: BSTNode[T]) -> None:
        self.add(other.value)
        if other.left is not None:
            self.merge(other.left)
        if other.right is not None:
            self.merge(other.right)

    def to_list(self) -> list[T]:
        left_list = self.left.to_list() if self.left else []
        right_list = self.right.to_list() if self.right else []

        return left_list + [self.value] + right_list
