from matrix import Matrix
from matrix_tests import *
import unittest


class TestMatrix(unittest.TestCase):
    def test_det(self):
        for test_data, right_answer in zip(ALONE_OPERATION_INPUT_DATA, DET_OUTPUT_DATA):
            my_dets = Matrix(test_data).get_det()
            self.assertAlmostEqual(my_dets, right_answer, delta=1)

    def test_cramer_rull(self):
        for test_data_coef, test_data_answer in CRAMER_INPUT_DATA:
            my_roots = Matrix(test_data_coef).cramers_rull(test_data_answer)
            my_answers = [sum([root * line_coef[ind_root] for ind_root, root in enumerate(my_roots)])
                          for line_coef in test_data_coef]
            for my_answer, right_answer in zip(my_answers, test_data_answer):
                self.assertAlmostEqual(my_answer, right_answer, delta=1)

    def test_add(self):
        for test_data, right_answer in zip(PAIR_OPERATION_INPUT_DATA, ADD_OUTPUT_DATA):
            matrix_1, matrix_2 = test_data[0], test_data[1]
            my_sum = Matrix(matrix_1) + Matrix(matrix_2)
            self.assertEqual(my_sum.value, right_answer)

    def test_sub(self):
        for test_data, right_answer in zip(PAIR_OPERATION_INPUT_DATA, SUB_OUTPUT_DATA):
            matrix_1, matrix_2 = test_data[0], test_data[1]
            my_sum = Matrix(matrix_1) - Matrix(matrix_2)
            self.assertEqual(my_sum.value, right_answer)

    def test_mul(self):
        for test_data, right_answer in zip(PAIR_OPERATION_INPUT_DATA, MUL_OUTPUT_DATA):
            matrix_1, matrix_2 = test_data[0], test_data[1]
            my_mul = Matrix(matrix_1) * Matrix(matrix_2)
            # PS: ненавижу флоты в питону...
            for my_line, right_line in zip(my_mul, right_answer):
                for my_el, right_el in zip(my_line, right_line):
                    self.assertAlmostEqual(my_el, right_el, 3)

    def test_transpose(self):
        for test_data, right_answer in zip(ALONE_OPERATION_INPUT_DATA, TRANS_OUTPUT_DATA):
            self.assertEqual(Matrix(test_data).transpose().value, right_answer)


tester = TestMatrix()
tester.test_add()
tester.test_sub()
tester.test_mul()
tester.test_transpose()
tester.test_det()
tester.test_cramer_rull()
print("All correct!")
