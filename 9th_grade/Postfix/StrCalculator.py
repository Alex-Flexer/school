from Postfix import PostfixExpression


def calculate(expr: str):
    postfix_expr = PostfixExpression(expr).expression
    operatinos_dict = {'add': lambda a, b: a + b,
                       'sub': lambda a, b: a - b,
                       'mul': lambda a, b: a * b,
                       'div': lambda a, b: a / b,
                       'exp': lambda a, b: a**b}
    ind = 0
    while len(postfix_expr) > 1:
        lexem = postfix_expr[ind]
        if lexem.type_value != 'num':
            left_operand = postfix_expr[ind - 2].value
            right_operand = postfix_expr[ind - 1].value
            postfix_expr[ind - 2].value =\
                operatinos_dict[lexem.type_value](left_operand, right_operand)

            postfix_expr.pop(ind - 1)
            ind -= 1
            postfix_expr.pop(ind)
            ind -= 1
        ind += 1
    return postfix_expr[0].value
