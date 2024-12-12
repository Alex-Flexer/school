from avl_dict import Dict
from random import randint, sample
import unittest

from generate_tests import gen_dict_tests


dict_tests = gen_dict_tests()


class TestDict(unittest.TestCase):
    def test_init(self):
        for test_dict_elements in dict_tests:
            custom_dict = Dict[int, int](test_dict_elements)
            original_dict = dict(test_dict_elements)

            self.assertDictEqual(
                custom_dict,
                original_dict
            )

    def test_get(self):
        for test_dict_elements in dict_tests:
            custom_dict = Dict[int, int](test_dict_elements)

            desired_elements = sample(
                population=test_dict_elements,
                k=randint(3, 10)
            )

            for key, value in desired_elements:
                self.assertEqual(custom_dict[key], value)

    def test_set(self):
        for test_dict_elements in dict_tests:
            custom_dict = Dict[int, int](test_dict_elements)
            original_dict = dict(test_dict_elements)

            for _ in range(10):
                key = randint(-100, 100)
                value = randint(-100, 100)

                custom_dict[key] = value
                original_dict[key] = value

                self.assertDictEqual(
                    custom_dict,
                    original_dict
                )

    def test_delete(self):
        for test_dict_elements in dict_tests:
            custom_dict = Dict[int, int](test_dict_elements)

            desired_elements = sample(
                population=test_dict_elements,
                k=randint(3, 10)
            )

            for key, _ in desired_elements:
                custom_dict.pop(key)
                self.assertIsNone(custom_dict[key])

    def test_merge(self):
        dict_for_merging = gen_dict_tests()
        for test_dict_elements, merging_dict_elements in\
                zip(dict_tests, dict_for_merging):

            custom_dict = Dict[int, int](test_dict_elements)
            original_dict = dict(test_dict_elements)

            merging_custom_dict = Dict[int, int](merging_dict_elements)
            merging_original_dict = dict(merging_dict_elements)

            custom_dict.merge(merging_custom_dict)
            original_dict |= merging_original_dict

            self.assertDictEqual(custom_dict, original_dict)


if __name__ == "__main__":
    unittest.main()
