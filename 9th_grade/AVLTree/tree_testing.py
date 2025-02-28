import unittest
from tree_test import INPUT_DATA
from random import choice, shuffle
from tree import Tree


def is_balanced(subtree: Tree):
    left_high = subtree.left.get_high() if subtree.left else -1
    righ_high = subtree.right.get_high() if subtree.right else -1
    if abs(left_high - righ_high) > 1:
        return False

    return (is_balanced(subtree.left) if subtree.left else True) or\
        (is_balanced(subtree.right) if subtree.right else True)

class TesterAvlTree(unittest.TestCase):
    def test_balanse(self):
        for test_data in INPUT_DATA:
            tree = Tree(test_data[0])
            for node in test_data[1:]:
                tree.add(node)
            tree.full_tree_balance()
            self.assertTrue(is_balanced(tree))
    
    def test_pop(self):
        for test_data in INPUT_DATA:
            tree = Tree(test_data[0])
            for node in test_data[1:]:
                tree.add(node)
            
            tree_preorder_traversal = tree.get_preorder_traversal()
            while tree_preorder_traversal:
                pop_el = choice(tree_preorder_traversal)
                tree = tree.pop(pop_el)
                if tree:
                    return
                tree_preorder_traversal = tree.get_preorder_traversal()
                self.assertEqual(tree_preorder_traversal, sorted(tree_preorder_traversal))
    
    def test_add(self):
        for test_data in INPUT_DATA:
            tree = Tree(test_data[0])
            not_used_nodes = test_data[1:].copy()
            tree_preorder_traversal = tree.get_preorder_traversal()
            while not_used_nodes:
                add_el = choice(not_used_nodes)
                tree.add(add_el)
                if tree:
                    return
                tree_preorder_traversal = tree.get_preorder_traversal()
                self.assertEqual(tree_preorder_traversal, sorted(tree_preorder_traversal))

tester = TesterAvlTree()
tester.test_balanse()
tester.test_pop()
tester.test_add()
print("All correct!")
