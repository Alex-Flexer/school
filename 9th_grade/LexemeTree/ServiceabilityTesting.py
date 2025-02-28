from ServiceabilityTests import *
from unittest import TestCase
from PolishCalculator import calc
from LexemeTree import ExprNode
from BNF import Expression


class Tester(TestCase):
    def polish_test(self):
        for test_data in INPUT_DATA:
            while True:
                try:
                    x = randint(1, 20)
                    right_answer = eval(test_data.replace('^', '**'))
                except ZeroDivisionError:
                    continue
                else:
                    break
            self.assertAlmostEqual(calc(test_data, x), right_answer, delta=0.1)

    def bnf_test(self):
        for test_data in INPUT_DATA:
            if '^' in test_data:
                continue
            while True:
                try:
                    x = randint(1, 20)
                    right_answer = eval(test_data.replace('^', '**'))
                except ZeroDivisionError:
                    continue
                else:
                    break

            self.assertAlmostEqual(Expression(test_data).calc(x), right_answer, delta=0.1)

    def lexeme_tree_test(self):
        for test_data in INPUT_DATA:
            while True:
                try:
                    x = randint(1, 20)
                    right_answer = eval(test_data.replace('^', '**'))
                except ZeroDivisionError:
                    continue
                else:
                    break
            expr_node: ExprNode = ExprNode(test_data)
            expr_node.full_opimize(x)
            self.assertAlmostEqual(expr_node.calc(x), right_answer, delta=0.1)



tester = Tester()

tester.polish_test()
tester.bnf_test()
tester.lexeme_tree_test()
print('All correct!')
