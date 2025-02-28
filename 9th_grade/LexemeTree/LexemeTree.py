from __future__ import annotations
from typing import Union, Optional
from Lexeme import Lexeme, lexemize 
from copy import deepcopy
from collections import Counter

OPERATIONS = {
    'add': lambda a, b: a + b,
    'sub': lambda a, b: a - b,
    'mul': lambda a, b: a * b,
    'div': lambda a, b: a / b,
    'exp': lambda a, b: a**b
}


class ExprNode:
    node_value: Lexeme
    left: Optional[ExprNode]
    right: Optional[ExprNode]

    __summands = Counter()

    def __init__(self, expr: Union[list[Lexeme], str, int]):
        if isinstance(expr, (int, float)):
            expr = str(expr)
        if isinstance(expr, str):
            expr = lexemize(expr)
        if isinstance(expr, ExprNode):
            self.left = deepcopy(expr.left)
            self.right = deepcopy(expr.right)
            self.node_value = deepcopy(expr.node_value)
            return

        index = self.sign_split(expr)
        while index == -1:
            if expr[0].type_value == "opar" and expr[-1].type_value == "cpar":
                expr = expr[1:-1]
                index = self.sign_split(expr)
            else:
                self.node_value = expr[index]
                self.left = self.right = None
                return
        self.left = ExprNode(expr[:index])
        self.right = ExprNode(expr[index + 1:])
        self.node_value = expr[index]

    def __str__(self) -> str:
        if self.node_value.type_value in ('num', 'var'):
            return str(self.node_value.value)

        left = self.left
        right = self.right
        if self.left.node_value.type_value not in ('var', 'num') and self.left.node_value.prior < self.node_value.prior:
            left = '(' + str(left) + ')'
        if self.right.node_value.type_value not in ('var', 'num') and\
                (self.right.node_value.prior < self.node_value.prior or self.node_value.type_value == 'sub'):
            right = '(' + str(right) + ')'
        if self.node_value.type_value == 'exp':
            return f'{left}{self.node_value.value}{right}'
        return f'{left} {self.node_value.value} {right}'

    @staticmethod
    def sign_split(expr: list[Lexeme]) -> int:
        res_prio_1 = -1
        res_prio_2 = -1
        res_prio_3 = -1
        balance = 0
        for ind, lexeme in enumerate(expr):
            if lexeme.type_value == "cpar":
                balance -= 1
            elif lexeme.type_value == "opar":
                balance += 1
            elif lexeme.type_value == "exp" and res_prio_3 == -1 and balance == 0:
                res_prio_3 = ind
            elif lexeme.type_value in ("mul", "div") and balance == 0:
                res_prio_2 = ind
            elif lexeme.type_value in ("add", "sub") and balance == 0:
                res_prio_1 = ind
        if res_prio_1 == -1 and res_prio_2 == -1 and res_prio_3 == -1:
            return -1
        elif res_prio_1 >= 0:
            return res_prio_1
        elif res_prio_2 >= 0:
            return res_prio_2
        else:
            return res_prio_3

    def calc(self, x: Union[int, float]) -> Union[int, float]:
        if not self.right and not self.left:
            if self.node_value.type_value == "var":
                return x
            else:
                return round(float(self.node_value.value), 5)
        else:
            left_value = self.left.calc(x)
            right_value = self.right.calc(x)
            return OPERATIONS[self.node_value.type_value](left_value, right_value)

    def optimize_mul_add(self, x: Union[int, float]):
        if self.left and self.right:
            self.left.optimize_mul_add(x)
            self.right.optimize_mul_add(x)
        else:
            return

        repl = deepcopy(self)
        if self.left.node_value.type_value == 'num' and\
                self.right.node_value.type_value == 'num':
            repl.node_value.value = self.calc(x)
            repl.node_value.type_value = 'num'
            repl.left = None
            repl.right = None

        elif self.node_value.type_value in ('add', 'sub'):
            if self.left.node_value.value == 0 and self.node_value.type_value != 'sub':
                repl = deepcopy(self.right)
            elif self.right.node_value.value == 0:
                repl = deepcopy(self.left)

        elif self.node_value.type_value in ('div', 'mul'):
            if self.left.node_value.value == 1 and self.node_value.type_value != 'div':
                repl = deepcopy(self.right)
            elif self.right.node_value.value == 1:
                repl = deepcopy(self.left)

            if self.left.node_value.value == 0 or\
                    self.right.node_value.value == 0:
                if self.node_value.type_value == 'div':
                    raise ZeroDivisionError()
                repl = ExprNode('0')

        elif self.node_value.type_value == 'exp':
            if self.right.node_value.value == 0 or\
                    self.left.node_value.value == 1:
                repl = ExprNode('1')

        self.node_value = repl.node_value
        self.left, self.right = repl.left, repl.right

    def open_pars(self) -> int:
        actions = 0
        if self.left and self.right:
            actions += self.left.open_pars()
            actions += self.right.open_pars()
        else:
            return actions
        if self.node_value.type_value == 'mul' and\
                self.right.node_value.type_value not in ('var', 'num') and\
                self.right.node_value.prior < self.node_value.prior:
            self.left, self.right = self.right, self.left

        if self.node_value.type_value == 'mul' and\
                self.left.node_value.type_value not in ('var', 'num') and\
                self.left.node_value.prior < self.node_value.prior:
            actions += 1
            left_term = deepcopy(self.left.left)
            right_term = deepcopy(self.left.right)
            communism_factor = deepcopy(self.right)

            operation = self.node_value

            self.node_value = deepcopy(self.left.node_value)

            self.left.node_value = operation
            self.left.left = left_term
            self.left.right = communism_factor

            self.right.node_value = deepcopy(operation)
            self.right.left = deepcopy(right_term)
            self.right.right = deepcopy(communism_factor)
        return actions

    def move_x_right(self) -> None:
        subtrees_with_variables: list[tuple[ExprNode, int]] = []
        if self.node_value.type_value in ('add', 'sub'):
            if self.left.node_value.type_value == 'mul':
                left_actions = self.left.replace_variable_factors()
                subtrees_with_variables.append((self.left, left_actions))
            elif self.left.node_value.type_value in ('add', 'sub'):
                self.left.move_x_right()

            if self.right.node_value.type_value == 'mul':
                right_actions = self.right.replace_variable_factors()
                subtrees_with_variables.append((self.right, right_actions))
            elif self.right.node_value.type_value in ('add', 'sub'):
                self.right.move_x_right()
        else:
            subtrees_with_variables.append(
                (self, self.replace_variable_factors()))

        for subtree, amount_variables in subtrees_with_variables:
            if amount_variables == 0:
                continue
            subtree.left.right, subtree.left.left = deepcopy(
                subtree.right), deepcopy(subtree.left)
            subtree.left.node_value = Lexeme('*')
            subtree.right.node_value = Lexeme('^')
            subtree.right.left = ExprNode('x')
            subtree.right.right = ExprNode(str(amount_variables))

    def replace_variable_factors(self):
        actions = 0
        if self.node_value.type_value in ('var', 'num'):
            return 0

        if self.left.node_value.type_value == 'var':
            self.left = ExprNode('1')
            actions += self.right.node_value.value if self.node_value.type_value == 'exp' else 1

        if self.right.node_value.type_value == 'var':
            self.right = ExprNode('1')
            actions += 1

        return actions + self.left.replace_variable_factors() + self.right.replace_variable_factors()

    def add_fractions(self):
        operation = deepcopy(self.node_value)
        left_numerator, left_denominator = deepcopy(
            self.left.left), deepcopy(self.left.right)
        right_numerator, right_denominator = deepcopy(
            self.right.left), deepcopy(self.right.right)

        self.node_value = Lexeme('/')
        self.left.node_value = operation

        self.left.left.node_value = Lexeme('*')
        self.left.left.left = left_numerator
        self.left.left.right = right_denominator

        self.left.right.node_value = Lexeme('*')
        self.left.right.left = right_numerator
        self.left.right.right = left_denominator

        self.right.node_value = Lexeme('*')
        self.right.left = deepcopy(left_denominator)
        self.right.right = deepcopy(right_denominator)

    def mul_fractions(self):
        left_numerator, left_denominator = deepcopy(
            self.left.left), deepcopy(self.left.right)
        right_numerator, right_denominator = deepcopy(
            self.right.left), deepcopy(self.right.right)

        self.node_value = Lexeme('/')
        self.left.node_value = Lexeme('*')
        self.left.left = left_numerator
        self.left.right = right_numerator

        self.right.node_value = Lexeme('*')
        self.right.left = left_denominator
        self.right.right = right_denominator

    def optimize_fractions(self):
        if self.node_value.type_value in ('num', 'var'):
            return

        self.left.optimize_fractions()
        self.right.optimize_fractions()

        if self.left.node_value.type_value == 'div' and\
                self.right.node_value.type_value != 'div':
            self.right.left = deepcopy(self.right)
            self.right.right = ExprNode('1')
            self.right.node_value = Lexeme('/')

        elif self.left.node_value.type_value != 'div' and\
                self.right.node_value.type_value == 'div':
            self.left.left = deepcopy(self.left)
            self.left.right = ExprNode('1')
            self.left.node_value = Lexeme('/')

        if self.left.node_value.type_value == 'div' and\
                self.right.node_value.type_value == 'div':
            if self.node_value.type_value in ('add', 'sub'):
                self.add_fractions()

            elif self.node_value.type_value == 'mul':
                self.mul_fractions()

            elif self.node_value.type_value == 'div':
                self.right.left, self.right.right = self.right.right, self.right.left
                self.mul_fractions()

    def count_polynomial_degres(self, sign):
        if self.node_value.type_value == 'mul':
            if self.right.node_value.type_value == 'exp' and\
                    self.right.left.node_value.type_value == 'var' and\
                    self.left.node_value.type_value == 'num':
                coeff = self.left.node_value.value
                degree = self.right.right.node_value.value
                self.__summands[degree] += coeff * sign
        elif self.node_value.type_value == 'exp' and\
            self.left.node_value.type_value == 'var':
            self.__summands[self.right.node_value.value] += 1 * sign
        elif self.node_value.type_value == 'num':
            self.__summands[0] += self.node_value.value * sign
        elif self.node_value.type_value == 'var':
            self.__summands[1] += 1
        else:
            self.left.count_polynomial_degres(sign)
            if self.node_value.type_value == 'add':
                self.right.count_polynomial_degres(sign)
            elif self.node_value.type_value == 'sub':
                self.right.count_polynomial_degres(-sign)

    def add_polymonial(self, polymonial: dict[float, float]):
        result = ''
        for degree, coeff in polymonial.items():
            if degree == 0:
                if coeff < 0:
                    result += f'(0-{-coeff})+'
                else:
                    result += f'{coeff}+'
            else:
                if coeff < 0:
                    result += f'(0-{-coeff}*x^{degree})+'
                else:
                    result += f'{coeff}*x^{degree}+'

        result = result[:-1].replace('+-', '-')
        return ExprNode(result)

    def full_opimize(self, x=None):
        global numerator_summands, denominator_summands
        while self.open_pars():
            pass
        self.optimize_mul_add(x)
        self.optimize_fractions()
        if self.node_value.type_value != 'div':
            self.left = deepcopy(self)
            self.node_value = Lexeme('/')
            self.right = ExprNode('1')
        
        while self.left.open_pars():
            pass
        while self.right.open_pars():
            pass

        self.left.move_x_right()
        self.left.optimize_mul_add(x)
        self.right.move_x_right()
        self.right.optimize_mul_add(x)
        self.left.count_polynomial_degres(-1 if self.node_value.type_value == 'sub' else 1)
        numerator_summands = self.__summands.copy()
        self.__summands.clear()
        self.right.count_polynomial_degres(-1 if self.node_value.type_value == 'sub' else 1)
        denominator_summands = self.__summands.copy()
        self.left = self.add_polymonial(numerator_summands)
        self.right = self.add_polymonial(denominator_summands)
        self.__summands.clear()
