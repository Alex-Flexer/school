PATTER_STRING_FIELD =\
    """{}| {} | {}
--+--+--
{}| {} |{}
--+--+--
{}| {} |{}"""


class TicTacToeField:
    __value: list[list[int]]

    def __init__(self) -> None:
        self.__value = [[0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]]

    def __getitem__(self, index):
        return self.__value[index]

    def __str__(self) -> str:
        print_data = {0: "                ",
                      1: "     x     ",
                      2: "     0    "}
        # https://www.youtube.com/watch?v=QSC_0LoFjxU ↓↓↓
        PATTER_STRING_FIELD.format(*[print_data[self[i][j]] for j in range(3) for i in range(3)])

    def check_victory(self):
        # check horizontal
        for line in range(3):
            if self[line][0] == self[line][1] == self[line][2]:
                return self[line][0]

        # check vertical
        for col in range(3):
            if self[0][col] == self[1][col] == self[2][col]:
                return self[0][col]

        if self[0][0] == self[1][1] == self[2][2]:
            return self[0][0]

        if self[0][2] == self[1][1] == self[2][0]:
            return self[0][2]

        return 0

    def do_move(self, line, col, player_side):
        if self.__value[line][col] == 0:
            self.__value[line][col] = player_side
        else:
            return -1

        return self.check_victory()

    def clear_field(self):
        for line_ind in range(3):
            for col_ind in range(3):
                self[line_ind][col_ind] = 0
