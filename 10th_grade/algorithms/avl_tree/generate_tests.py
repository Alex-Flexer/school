from random import sample, randint
from typing import Generator

from avl_tree import Tree, AVLNode
from avl_dict import Dict


AMOUNT_TESTS = 5


def gen_tree(size):
    tree = Tree[int](AVLNode)

    nodes_values =\
        sample(
            population=range(1, 10**(size+2)),
            k=randint(5**(size+1), size * 5**(size+1))
        )

    for node in nodes_values:
        tree.add(node)

    return tree


def gen_dict_elements(size):
    test_length = randint(5**(size+1), size * 5**(size+1))

    keys = sample(
        population=range(test_length, 10**(size+2)),
        k=test_length
    )

    values = sample(
        population=range(test_length, 10**(size+2)),
        k=test_length
    )

    return list(zip(keys, values))


def gen_set_elements(size):
    set_elements =\
        sample(
            population=range(1, 10**(size+2)),
            k=randint(5**(size+1), size * 5**(size+1))
        )

    return set_elements


def gen_tree_tests() -> Generator[Tree, None, None]:
    for lvl in range(1, AMOUNT_TESTS):
        yield gen_tree(lvl)


def gen_dict_tests() -> Generator[Dict, None, None]:
    for lvl in range(1, AMOUNT_TESTS):
        yield gen_dict_elements(lvl)


def gen_set_tests() -> Generator[Dict, None, None]:
    for lvl in range(1, AMOUNT_TESTS):
        yield gen_set_elements(lvl)
