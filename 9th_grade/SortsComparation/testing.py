import unittest
from sorts import bubble_sort, quck_sort, insert_sort, merge_sort, cocktail_shaker_sort, heap_sort
from test_data import INPUT_DATA, OUTPUT_DATA
from decorators import List, resousrs_checker


class TestSort(unittest.TestCase):
    def test_sort(self, sort_function):
        test_num = 0
        for test_data, right_answer in zip(INPUT_DATA, OUTPUT_DATA):
            test_num += 1
            res = resousrs_checker(sort_function)(List(list)(test_data))
            self.assertEqual(res['result'], right_answer)
            print(f"{sort_function.__name__} test {test_num}: time = {res['time']}, memory = {res['memory']}, get = {res['get_requests']}, set = {res['set_requests']}")

tester_obj = TestSort()

tester_obj.test_sort(bubble_sort)
tester_obj.test_sort(quck_sort)
tester_obj.test_sort(insert_sort)
tester_obj.test_sort(merge_sort)
tester_obj.test_sort(heap_sort)
tester_obj.test_sort(cocktail_shaker_sort)