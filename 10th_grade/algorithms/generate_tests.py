from avl_tree import Tree, AVLNode
from random import sample, randint
from typing import Generator


AMOUNT_TESTS = 6

def gen_test(size=0):
    tree = Tree[int](AVLNode)

    def init_tree(nodes_values: list[int]):
        nonlocal tree
        for node in nodes_values:
            tree.add(node)

    match size:
        case 0:
            init_tree(sample(range(1, 100), randint(10, 20)))
        case 1:
            init_tree(sample(range(1, 1000), randint(25, 40)))
        case 2:
            init_tree(sample(range(1, 10000), randint(60, 100)))
        case 3:
            init_tree(sample(range(1, 100000), randint(100, 200)))
        case 4:
            init_tree(sample(range(1, 1000000), randint(300, 500)))
        case 5:
            init_tree(sample(range(1, 10000000), randint(700, 1000)))
    return tree


def gen_tests() -> Generator[Tree, None, None]:
    for lvl in range(AMOUNT_TESTS):
        yield gen_test(lvl)
