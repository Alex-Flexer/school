from avl_set import Set
from random import randint, sample
import unittest

from generate_tests import gen_set_tests


set_tests = gen_set_tests()


class TestSet(unittest.TestCase):
    def test_init(self):
        for test_set_elements in set_tests:
            custom_set = Set[int](test_set_elements)
            original_set = set(test_set_elements)

            self.assertSetEqual(
                custom_set,
                original_set
            )

    def test_get(self):
        for test_set_elements in set_tests:
            custom_set = Set[int](test_set_elements)

            desired_elements = sample(
                population=test_set_elements,
                k=randint(3, 10)
            )

            for value in desired_elements:
                self.assertIn(value, custom_set)

    def test_set(self):
        for test_set_elements in set_tests:
            custom_set = Set[int](test_set_elements)
            original_set = set(test_set_elements)

            for _ in range(10):
                key = randint(-100, 100)
                value = randint(-100, 100)

                custom_set[key] = value
                original_set[key] = value

                self.assertSetEqual(
                    custom_set,
                    original_set
                )

    def test_delete(self):
        for test_set_elements in set_tests:
            custom_set = Set[int](test_set_elements)

            desired_elements = sample(
                population=test_set_elements,
                k=randint(3, 10)
            )

            for value in desired_elements:
                custom_set.remove(value)
                self.assertNotIn(value, custom_set)

    def test_or(self):
        set_for_merging = gen_set_tests()
        for test_set_elements, merging_set_elements in\
                zip(set_tests, set_for_merging):

            custom_set = Set[int](test_set_elements)
            original_set = set(test_set_elements)

            merging_custom_set = Set[int](merging_set_elements)
            merging_original_set = set(merging_set_elements)

            custom_set |= merging_custom_set
            original_set |= merging_original_set

            custom_elements = sorted(custom_set.to_list())
            original_elements = sorted(list(original_set))

            self.assertListEqual(custom_elements, original_elements)

    def test_and(self):
        set_for_intersection = gen_set_tests()
        for test_set_elements, intersection_set_elements in\
                zip(set_tests, set_for_intersection):

            custom_set = Set[int](test_set_elements)
            original_set = set(test_set_elements)

            intersection_custom_set = Set[int](intersection_set_elements)
            intersection_original_set = set(intersection_set_elements)

            custom_set &= intersection_custom_set
            original_set &= intersection_original_set

            custom_elements = sorted(custom_set.to_list())
            original_elements = sorted(list(original_set))

            self.assertListEqual(custom_elements, original_elements)


if __name__ == "__main__":
    unittest.main()
