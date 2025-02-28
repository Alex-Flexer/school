import numpy as np
from numpy import matrix, linalg
from random import randint

# alone( : transpose, get_det
ALONE_OPERATION_INPUT_DATA = [[[randint(1, 1000) / 10 for _ in range(3)] for _ in range(3)],
                              [[randint(1, 1000) / 10 for _ in range(7)] for _ in range(7)]]

DET_OUTPUT_DATA = [linalg.det(matrix(test))
                   for test in ALONE_OPERATION_INPUT_DATA]
TRANS_OUTPUT_DATA = [matrix(test).transpose().tolist()
                     for test in ALONE_OPERATION_INPUT_DATA]

# pair operatins: add, sub, mul
PAIR_OPERATION_INPUT_DATA = [([[randint(1, 1000) / 10 for _ in range(3)] for _ in range(3)],
                              [[randint(1, 1000) / 10 for _ in range(3)] for _ in range(3)]),
                             ([[randint(1, 1000) / 10 for _ in range(8)] for _ in range(8)],
                              [[randint(1, 1000) / 10 for _ in range(8)] for _ in range(8)])]

ADD_OUTPUT_DATA = [(np.matrix(matrix_1) + np.matrix(matrix_2)).tolist()
                   for matrix_1, matrix_2 in PAIR_OPERATION_INPUT_DATA]

SUB_OUTPUT_DATA = [(np.matrix(matrix_1) - np.matrix(matrix_2)).tolist()
                   for matrix_1, matrix_2 in PAIR_OPERATION_INPUT_DATA]

MUL_OUTPUT_DATA = [(np.matrix(matrix_1) * np.matrix(matrix_2)).tolist()
                   for matrix_1, matrix_2 in PAIR_OPERATION_INPUT_DATA]


CRAMER_INPUT_DATA = [([[2, 3, -1, 2],
                      [1, -1, -2, 1],
                      [3, 1, -1, 7],
                      [-1, -2, 1, -1]],
                      [-4, -7, 0, 5]),
                     ([[-2, -10, 6, -9],
                       [-8, -3, 2, -4],
                       [-1, 0, 8, -9],
                       [-8, -1, -3, -5]],
                      [115, 108, 65, 95])]
