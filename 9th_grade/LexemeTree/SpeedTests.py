from random import randint, choice


oparatioans = ('-', '+', '/', '*')

INPUT_DATA = [''.join([(str(randint(1, 10000) / 100) if ind % 5 != 0 else 'x') + choice(oparatioans)
                      for ind in range(length * 10)])[:-1] for length in range(2, 100)]
