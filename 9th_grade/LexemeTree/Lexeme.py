def is_number(str_num: str):
    if str_num[0] == '-':
        str_num = str_num[1:]
    return str_num.isdigit() or (str_num.count('.') == 1 and str_num.split('.')[0].isdigit() and str_num.split('.')[1].isdigit())


class Lexeme:
    value: str
    type_value: str
    prior: int

    def __init__(self, string: str) -> None:
        if is_number(string):
            self.value = float(string)
            self.type_value = 'num'
        else:
            operatinons = {'(': 'opar', ')': 'cpar', '+': 'add',
                           '-': 'sub', '/': 'div', '*': 'mul', '^': 'exp', '**': 'exp', 'x': 'var'}
            prior_dict = {'add': 1, 'sub': 1, 'mul': 2, 'div': 2, 'exp': 3}

            self.value = string
            try:
                self.type_value = operatinons[string]
                if self.type_value in prior_dict.keys():
                    self.prior = prior_dict[self.type_value]
            except KeyError:
                raise KeyError(f'Unknown type {string}')


def lexemize(string: str):
    string = string.replace(' ', '')
    if string in ('+', '-', '*', '/'):
        return [Lexeme(string)]

    if is_number(string):
        return [Lexeme(string)]

    result = []
    last_num = ''
    for sim in string:
        if sim.isdigit() or sim in ('.', ','):
            last_num += sim
        else:
            if last_num:
                result.append(Lexeme(last_num))
                last_num = ''
            result.append(Lexeme(sim))
    if last_num:
        result.append(Lexeme(last_num))
    return result
