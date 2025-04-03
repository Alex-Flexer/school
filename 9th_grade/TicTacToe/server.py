from field import TicTacToeField
from AI_TicTaсToe import AI
import socket

PORT = 12345
HOST = "127.0.0.1"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(True)
server.bind((HOST, PORT))
server.listen()

print("SERVER")

user, address = server.accept()

tic_tac_toe_field = TicTacToeField()
ai_field = AI(tic_tac_toe_field)

response_move = 0
while True:
    server_side = int(user.recv(512).decode("utf-8"))
    user_side = 3 - server_side

    print(server_side)

    counter_steps = 0

    if server_side == 1:
        counter_steps += 1
        move = ai_field.ai_choose_move(server_side)
        tic_tac_toe_field.do_move(move[0], move[1], server_side)
        user.send(f"{str(move[0])} {str(move[1])}".encode())

    while True:
        counter_steps += 1
        data = user.recv(512).decode("utf-8")

        data = data.split()
        data = int(data[0]), int(data[1])
        print(data)
        tic_tac_toe_field.do_move(data[0], data[1], user_side)

        move = ai_field.ai_choose_move(server_side)

        tic_tac_toe_field.do_move(move[0], move[1], server_side)

        user.send(f"{str(move[0])} {str(move[1])}".encode())
        if counter_steps - int(server_side == 1) == 4:
            break

    flag_continue = int(user.recv(512).decode("utf-8"))
    if flag_continue == "0":
        break

    tic_tac_toe_field.clear_field()
