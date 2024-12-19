from trie_tree import TrieNode
from random import randint, sample
from secrets import token_urlsafe as gen_string
import unittest

from generate_tests import gen_set_tests


set_tests = list(gen_set_tests())


class TestSet(unittest.TestCase):
    def test_init(self):
        for test_set_elements in set_tests:
            custom_set = TrieNode(test_set_elements)
            original_set = set(test_set_elements)

            self.assertCountEqual(
                list(custom_set),
                original_set
            )

    def test_contains(self):
        for test_set_elements in set_tests:
            custom_set = TrieNode(test_set_elements)

            desired_elements = sample(
                population=test_set_elements,
                k=randint(3, 10)
            )

            for value in desired_elements:
                self.assertIn(value, custom_set)

    def test_add(self):
        for test_set_elements in set_tests:
            custom_set = TrieNode(test_set_elements)
            original_set = set(test_set_elements)

            for _ in range(10):
                value = gen_string(randint(10, 1000))

                custom_set.add(value)
                original_set.add(value)

                self.assertCountEqual(
                    list(custom_set),
                    original_set
                )

    def test_delete(self):
        for test_set_elements in set_tests:
            custom_set = TrieNode(test_set_elements)

            desired_elements = sample(
                population=test_set_elements,
                k=randint(3, 10)
            )

            for value in desired_elements:
                custom_set.remove(value)
                self.assertNotIn(value, custom_set)


if __name__ == "__main__":
    unittest.main()
