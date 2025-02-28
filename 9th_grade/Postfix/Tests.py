from random import randint


INPUT_DATA = ['1 + 2',
              '1 + 2 - 3',
              '1 * 2 - (9 - 1) * 9',
              '((((1 + 2))))',
              '(1 + 2)^3 - ((1 - 1) * (2 + 2) - (3^3)^3)',
              '(12 - 3) * ((1 + 2 + 3) - (12 - 4) / 2 + 10^3) / 10',
              f'{randint(0, 100)} * {randint(0, 100)} - ({randint(0, 10)^randint(1, 4)})']

OUTPUT_DATA = [eval(expr.replace('^', '**')) for expr in INPUT_DATA]
