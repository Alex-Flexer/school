class Lexeme:
    value: str
    type_value: str

    def __init__(self, string: str) -> None:
        if string.isdigit():
            self.value = int(string)
            self.type_value = 'num'
        else:
            operatinons = {'(': 'opar', ')': 'cpar', '+': 'add',
                           '-': 'sub', '/': 'div', '*': 'mul', '^': 'exp'}
            self.value = string
            try:
                self.type_value = operatinons[string]
            except KeyError:
                raise KeyError('unknown type')


def lexemize(string: str):
    string = string.replace(' ', '')
    result = []
    last_num = ''
    for sim in string:
        if sim.isdigit():
            last_num += sim
        else:
            if last_num:
                result.append(Lexeme(last_num))
                last_num = ''
            result.append(Lexeme(sim))
    if last_num:
        result.append(Lexeme(last_num))
    return result
