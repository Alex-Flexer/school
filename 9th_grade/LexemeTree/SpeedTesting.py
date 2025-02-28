from SpeedTests import INPUT_DATA
from BNF import Expression
from PolishCalculator import calc as polish_calc
from LexemeTree import ExprNode
from time import time as now
from random import randint
from matplotlib import pyplot as plt
from sys import setrecursionlimit
setrecursionlimit(3000)


results: dict[str, list] = {'bnf_test': [],
                            'polish_test': [],
                            'lexeme_tree_test': []}


def test_time(func):
    def wraper(*args):
        start_time = now()
        func(*args)
        finish_time = now()
        results.get(func.__name__).append(round(finish_time - start_time, 10))
    return wraper


def tester(function):
    for data_test in INPUT_DATA:
        function(data_test, randint(100, 10000) / 100)


@test_time
def polish_test(expr: str, x):
    polish_calc(expr, x)


@test_time
def lexeme_tree_test(expr: str, x):
    expr_node: ExprNode = ExprNode(expr)
    expr_node.calc(x)


@test_time
def bnf_test(expr: str, x):
    Expression(expr).calc(x)


tester(polish_test)
tester(lexeme_tree_test)
tester(bnf_test)
plt.plot([len_expr for len_expr in range(20, 1000, 10)], results['bnf_test'], label='Бэкусовы нормальные формы')
plt.plot([len_expr for len_expr in range(20, 1000, 10)], results['lexeme_tree_test'], label='Дерево выражений')
plt.plot([len_expr for len_expr in range(20, 1000, 10)], results['polish_test'], label='Польская форма записи')
plt.legend()
plt.show()
