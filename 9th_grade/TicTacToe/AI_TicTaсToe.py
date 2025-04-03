from field import TicTacToeField


class AI:
    field: TicTacToeField

    def __init__(self, field_arg) -> None:
        self.field = field_arg

    def find_free_cell(self):
        for line in range(3):
            for col in range(3):
                if self.field[line][col] == 0:
                    return (line, col)
        return -1

    def ai_choose_move(self, server_side):
        # i win
        user_side = 3 - server_side

        for col in range(3):
            if [self.field[0][col], self.field[1][col], self.field[2][col]].count(server_side) == 2:
                res = (min(0, 1, 2, key=lambda y: self.field[y][col]), col)
                if self.field[res[0]][res[1]] == 0:
                    return res

        for line in range(3):
            if [self.field[line][0], self.field[line][1], self.field[line][2]].count(server_side) == 2:
                res = (line, min(0, 1, 2, key=lambda x: self.field[line][x]))
                if self.field[res[0]][res[1]] == 0:
                    return res

        if [self.field[0][0], self.field[1][1], self.field[2][2]].count(server_side) == 2:
            index_col_line = min(0, 1, 2, key=lambda ind: self.field[ind][ind])
            if self.field[index_col_line][index_col_line] == 0:
                return (index_col_line, index_col_line)

        if [self.field[0][2], self.field[1][1], self.field[2][0]].count(server_side) == 2:
            index_col_line = min(
                0, 1, 2, key=lambda ind: self.field[ind][2 - ind])
            if self.field[index_col_line][2 - index_col_line] == 0:
                return (index_col_line, 2 - index_col_line)

        # user wins
        for col in range(3):
            if [self.field[0][col], self.field[1][col], self.field[2][col]].count(user_side) == 2:
                res = (min(0, 1, 2, key=lambda y: self.field[y][col]), col)
                if self.field[res[0]][res[1]] == 0:
                    return res

        for line in range(3):
            if [self.field[line][0], self.field[line][1], self.field[line][2]].count(user_side) == 2:
                res = (line, min(0, 1, 2, key=lambda y: self.field[line][y]))
                if self.field[res[0]][res[1]] == 0:
                    return res

        if [self.field[0][0], self.field[1][1], self.field[2][2]].count(user_side) == 2:
            index_col_line = min(0, 1, 2, key=lambda ind: self.field[ind][ind])
            if self.field[index_col_line][index_col_line] == 0:
                return (index_col_line, index_col_line)

        if [self.field[0][2], self.field[1][1], self.field[2][0]].count(user_side) == 2:
            index_col_line = min(
                0, 1, 2, key=lambda ind: self.field[ind][2 - ind])
            if self.field[index_col_line][2 - index_col_line] == 0:
                return (index_col_line, 2 - index_col_line)

        # center
        if self.field[1][1] == 0:
            return (1, 1)

        if self.field[1][1] == user_side:
            # vert/hor
            for y, x in ((0, 1), (1, 2), (2, 1), (1, 0)):
                if self.field[y][x] == 0:
                    return (y, x)

        # corners
        for y, x in ((0, 0), (0, 2), (2, 2), (2, 0)):
            if self.field[2 - y][2 - x] == user_side and self.field[y][x] == 0:
                return (y, x)

        return self.find_free_cell()
