class Matrix:
    value: list[list[float]]
    length: int
    high: int

    def __init__(self, *args) -> None:
        if len(args) == 2:
            high, length = args[0], args[1]
            self.high = high
            self.length = length
            self.value = [[0 for _ in range(length)] for _ in range(high)]
        elif isinstance(args[0], (list, Matrix)):
            self.value = [line.copy() for line in args[0]]
            self.high = len(self.value)
            self.length = len(self.value[0])
        else:
            raise TypeError("Unknown type")

    def __str__(self) -> str:
        return '\n'.join([' '.join(map(str, line)) for line in self])

    def __add__(self, _other):
        if not isinstance(_other, Matrix):
            raise TypeError(f"Type must me Matrix, your {type(_other)}")
        if self.length != _other.length or self.high != _other.high:
            raise KeyError("Different sizes")

        return Matrix([[el_self + el_other for el_self, el_other in zip(line_self, line_other)]
                       for line_self, line_other in zip(self.value, _other.value)])

    def __radd__(self, _other):
        return self + _other

    def __sub__(self, _other):
        if not isinstance(_other, Matrix):
            raise TypeError(f"Type must me Matrix, your {type(_other)}")
        
        if self.length != _other.length or self.high != _other.high:
            raise KeyError("different sizes")

        return Matrix([[el_self - el_other for el_self, el_other in zip(line_self, line_other)]
                       for line_self, line_other in zip(self.value, _other.value)])

    def __rsub__(self, other):
        return other + self

    def __mul__(self, _other):
        if not isinstance(_other, (Matrix, float, int)):
            raise TypeError(f"Type must me Matrix, your {type(_other)}")

        if isinstance(_other, (int, float)):
            return Matrix([[el * _other for el in line] for line in self])

        if self.length != _other.high:
            raise KeyError

        res = Matrix(self.high, _other.length)
        ind_col = 0
        for ind_col, other_line in enumerate([[el[i] for el in _other] for i in range(_other.length)]):
            for ind_line, self_line in enumerate(self.value):
                _sum = 0
                for other_el, self_el in zip(other_line, self_line):
                    _sum += self_el * other_el
                res[ind_line][ind_col] = _sum
        return res
    
    def __rmul__(self, _other):
        return self * _other

    def __setitem__(self, key, value) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError(f"Element type must be float or int, not: {type(value)}")

        self.value[key] = value        

    def __getitem__(self, key) -> float:
        return self.value[key]

    def transpose(self):
        res = Matrix(self.length, self.high)
        for i in range(self.high):
            for j in range(self.length):
                res[j][i] = self[i][j]
        return res

    def get_det(self) -> float:

        if self.length != self.high:
            raise KeyError('matrix must be square')

        if self.length == 1:
            return self[0][0]
        elif self.length == 2:
            return self[0][0] * self[1][1] - self[0][1] * self[1][0]

        res = 0
        for ind_removed_col, removed_el in enumerate(self[0]):
            submatrix = Matrix([[el for ind_col, el in enumerate(self[ind_line]) if ind_col != ind_removed_col]
                                for ind_line in range(1, self.high)])
            res += submatrix.get_det() * (-1)**((ind_removed_col + 1) + 1) * removed_el

        return res

    def cramers_rull(self, answers) -> list[float]:
        if not isinstance(answers, Matrix):
            answers = Matrix([answers])
        if answers.high == 1:
            answers = answers.transpose()
        if answers.high != self.high or answers.length > 1:
            raise KeyError('Format of answers is incorrect')

        matrices = [Matrix(self) for _ in range(self.length)]
        for ind_matrix, matrix in enumerate(matrices):
            for ind_line in range(matrix.high):
                matrices[ind_matrix][ind_line][ind_matrix] = answers[ind_line][0]
        main_det = self.get_det()
        if main_det == 0:
            return -1
        dets = [matrix.get_det() for matrix in matrices]
        roots = [det / main_det for det in dets]
        return roots
