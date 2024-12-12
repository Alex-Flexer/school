from random import randint, choices
import unittest

from generate_tests import gen_tree_tests, gen_dict_tests


tree_tests = gen_tree_tests()
dict_tests = gen_dict_tests()


class TestAVLTree(unittest.TestCase):
    def test_init(self):
        for test_tree in tree_tests:
            self.assertTrue(test_tree.correct())

    def test_search(self):
        for test_tree in tree_tests:
            desired_nodes = choices(test_tree.to_list(), k=randint(3, 10))
            for node in desired_nodes:
                found_node = test_tree.search(node)
                self.assertTrue(
                    found_node is not None and
                    found_node.value == node
                )

    def test_add(self):
        for test_tree in tree_tests:
            new_node_value = randint(-1000, 1000)
            test_tree.add(new_node_value)
            self.assertTrue(
                test_tree.correct() and
                test_tree.search(new_node_value) is not None
            )

    def test_delete(self):
        for test_tree in tree_tests:
            tree_nodes = test_tree.to_list()
            deletion_nodes = choices(tree_nodes, k=randint(3, 10))
            for del_node in deletion_nodes:
                test_tree.deletion_nodes(del_node)
                self.assertTrue(
                    test_tree.correct() and
                    test_tree.search(del_node) is None
                )

    def test_merge(self):
        tree_for_merging = gen_tree_tests()
        for test_tree, merging_tree in zip(tree_tests, tree_for_merging):
            nodes = set(test_tree.to_list()) | set(merging_tree.to_list())

            test_tree.merge(merging_tree)
            self.assertEqual(set(test_tree.to_list()), nodes)
            self.assertTrue(test_tree.correct())


if __name__ == '__main__':
    unittest.main()
