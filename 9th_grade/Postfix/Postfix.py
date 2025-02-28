from Stack import Stack
from Lexeme import lexemize, Lexeme


class PostfixExpression:
    expression: list[Lexeme]

    def __to_postfix(expr: str):
        expr = '(' + expr.replace(' ', '') + ')'
        oper_set = set(['add', 'sub', 'div', 'mul', 'exp'])
        oper_preor = {"add": 1, "sub": 1, "mul": 2, "div": 2, "exp": 3}
        oper_stack: Stack[Lexeme] = Stack()
        lexemes: list[Lexeme] = lexemize(expr)
        res = []

        for sim in lexemes:
            if sim.type_value in oper_set:
                while oper_stack.size() and\
                        oper_stack.top().type_value not in ('opar', 'cpar') and\
                        oper_preor[oper_stack.top().type_value] >= oper_preor[sim.type_value]:
                    res.append(oper_stack.top())
                    oper_stack.pop()
                oper_stack.push(sim)
            elif sim.type_value == 'cpar':
                while oper_stack.top().type_value != 'opar':
                    res.append(oper_stack.top())
                    oper_stack.pop()
                oper_stack.pop()
            elif sim.type_value == 'opar':
                oper_stack.push(sim)
            else:
                res.append(sim)
        return res

    def __init__(self, expr) -> None:
        self.expression = PostfixExpression.__to_postfix(expr)
