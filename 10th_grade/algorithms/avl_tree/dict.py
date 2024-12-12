from typing import Iterable
from bst_tree import Node
from avl_tree import Tree


class Dict[K, V](Tree[K]):
    def __init__(self, collection: Iterable[tuple[K, V]]) -> None:
        super().__init__(Node[K])
        for element in collection:
            super().add(element)