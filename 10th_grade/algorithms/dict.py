from avl_tree import Tree, AVLNode, Compare
from typing import Callable, Iterable


class Dict[K, V](Tree[tuple[K, V]]):
    def __init__(self, collection: Iterable[tuple[K, V]] = []):
        predicate: Callable[[tuple[K, V], tuple[K, V]], Compare] =\
            lambda first, second: (
            Compare.Less
            if first[0] < second[0]
            else (Compare.Greater if first[0] > second[0] else Compare.Equal)
        )

        super().__init__(AVLNode[tuple[K, V]], predicate)
        for element in collection:
            self.add(element)

    def __setitem__(self, key: K, value: V) -> None:
        new_element = (key, value)

        node = self.search(new_element)

        if node is None:
            self.add(new_element)
        else:
            node.value = value

    def __getitem__(self, key: K) -> V | None:
        node = self.search((key, 0,))
        return None if node is None else node.value[1]

    def __contains__(self, key: K) -> bool:
        return self.search((key, 0,)) is not None

    def __str__(self):
        elements = self.to_list()
        inside_str = ", ".join(map(lambda el: f"{el[0]}: {el[1]}", elements))
        return "{" + inside_str + "}"

    def pop(self, key: K) -> None:
        self.delete((key, 0,))
