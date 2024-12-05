from avl_tree import Tree, AVLNode
from random import sample, randint
from typing import Generator


AMOUNT_TESTS = 5


def gen_test(size=0):
    tree = Tree[int](AVLNode)

    nodes_values =\
        sample(
            population=range(1, 10**(size+2)),
            k=randint(5**(size+1), size * 5**(size+1))
        )

    for node in nodes_values:
        tree.add(node)

    return tree


def gen_tests() -> Generator[Tree, None, None]:
    for lvl in range(1, AMOUNT_TESTS):
        yield gen_test(lvl)
