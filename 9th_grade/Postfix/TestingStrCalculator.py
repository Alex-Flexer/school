from Tests import *
from unittest import TestCase
from StrCalculator import calculate


class StrCalculatorTester(TestCase):
    def test_str_calculator(self):
        for test_data, right_answer in zip(INPUT_DATA, OUTPUT_DATA):
            self.assertEqual(calculate(test_data), right_answer)


tester = StrCalculatorTester()

tester.test_str_calculator()
print('All correct!')
