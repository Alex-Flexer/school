from random import randint


INPUT_DATA = [[4, 3, 1, 2],
              [randint(-(10**4), 10**4) for _ in range(10**4)],
              [randint(-10**5, 10**5) for _ in range(10**5)],
              [el for el in range(randint(0, 10**3))],
              [1, 0] + [el for el in range(2, 10**3)],
              [el for el in range(10**3, 0, -1)],
              [],
              [randint(-(10**4), 10**4) for _ in range(4759)]]

OUTPUT_DATA = [sorted(sub_list) for sub_list in INPUT_DATA]
