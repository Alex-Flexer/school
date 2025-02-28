from Lexeme import lexemize


class Factor:
    value: list

    def __init__(self, expr):
        if isinstance(expr, str):
            self.value = lexemize(expr)
        elif isinstance(expr, list):
            self.value = expr

    def calc(self, x: int):
        if self.value[0].type_value == 'opar' and self.value[-1].type_value == 'cpar':
            return Expression(self.value[1:-1]).calc(x)

        if len(self.value) == 1 and self.value[0].type_value == 'num':
            return self.value[0].value
        if len(self.value) == 1 and self.value[0].type_value == 'var':
            return x

        return Expression(self.value).calc(x)


class Sumand:
    value: list

    def __init__(self, expr):
        if isinstance(expr, str):
            self.value = lexemize(expr)
        elif isinstance(expr, list):
            self.value = expr

    def calc(self, x: int):
        balance = 0
        for ind, lexeme in list(enumerate(self.value))[::-1]:
            if lexeme.type_value == "cpar":
                balance += 1
            elif lexeme.type_value == "opar":
                balance -= 1
            elif lexeme.type_value == "mul" and balance == 0:
                return Expression(self.value[:ind]).calc(x) * Factor(self.value[ind + 1:]).calc(x)
            elif lexeme.type_value == "div" and balance == 0:
                return Expression(self.value[:ind]).calc(x) / Factor(self.value[ind + 1:]).calc(x)
        return Factor(self.value).calc(x)


class Expression:
    value: list

    def __init__(self, expr):
        if isinstance(expr, str):
            self.value = lexemize(expr)
        elif isinstance(expr, list):
            self.value = expr

    def calc(self, x: int):
        balance = 0
        for ind, lexeme in list(enumerate(self.value))[::-1]:
            if lexeme.type_value == "cpar":
                balance -= 1
            elif lexeme.type_value == "opar":
                balance += 1
            elif lexeme.type_value == "add" and balance == 0:
                return Expression(self.value[:ind]).calc(x) + Sumand(self.value[ind + 1:]).calc(x)
            elif lexeme.type_value == "sub" and balance == 0:
                return Expression(self.value[:ind]).calc(x) - Sumand(self.value[ind + 1:]).calc(x)
        return Sumand(self.value).calc(x)
