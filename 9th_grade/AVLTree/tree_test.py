from random import shuffle

INPUT_DATA = [[1, 2, 3, 4, 5, 6, 7, 8],
                          [8, 7, 6, 5, 4, 3, 2, 1],
                          [el for el in range(1, 8 + 1)],
                          [5, 4, 6, 3, 8, 7, 9]]

shuffle(INPUT_DATA[2])
