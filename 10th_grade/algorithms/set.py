from __future__ import annotations

from avl_tree import Tree, AVLNode
from typing import Iterable
from copy import deepcopy


class Set[T](Tree[tuple[T]]):
    def __init__(self, collection: Iterable[T] = []):
        super().__init__(AVLNode[T])
        for element in collection:
            self.add(element)

    def __str__(self):
        elements = self.to_list()
        inside_str = ", ".join(map(str, elements))
        return "{" + inside_str + "}"

    def __contains__(self, value: T) -> bool:
        return self.search(value) is not None

    def __eq__(self, other: Set[T]):
        return self.to_list() == other.to_list()

    def __and__(self, other: Set[T]) -> Set[T]:
        result = Set[T]()
        self_nodes = self.to_list()
        other_nodes = other.to_list()

        for s_node in self_nodes:
            if s_node in other_nodes:
                result.add(s_node)

        return result

    def __or__(self, other: Set[T]) -> Set[T]:
        result = deepcopy(self)
        result.merge(other)
        return result

    def add(self, value: T) -> None:
        super().add(value)

    def remove(self, value: T) -> None:
        self.delete(value)

    def is_empty(self) -> bool:
        return self.root is None

    def is_subset(self, other: Set[T]) -> bool:
        return self & other == self
