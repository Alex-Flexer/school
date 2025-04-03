import socket
from art import tsave
from field import TicTacToeField
import os


HOST = "127.0.0.1"
PORT = 12345


def update_display():
    temp_path = "field.txt"
    tsave(str(tic_tac_toe_field), filename=temp_path)
    os.system("cls")
    with open(temp_path, 'r', encoding='utf-8') as file:
        print(file.read())
    os.remove(temp_path)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setblocking(True)

client.connect((HOST, PORT))
print("CLIENT")


while True:
    user_side = input("Выберете за кого хотите играть: X или O.\n"
                      "1) X\n"
                      "2) O\n")

    while user_side not in {'1', '2'}:
        user_side = input("Нужно ввести 1 или 2.\n"
                          "Если вы хотите играть за крестики отправьте 1\n"
                          "Иначе отправьте 2\n")

    user_side = int(user_side)
    server_side = 3 - user_side
    client.send(str(server_side).encode())
    tic_tac_toe_field = TicTacToeField()

    order = 1
    response_move = 0

    flag_rechoocing_cell = False
    move = ''

    counter_steps = 0
    while True:
        if not flag_rechoocing_cell:
            update_display()

        if response_move == -1 and not flag_rechoocing_cell:
            print("Эта клетка уже занята, выберете другую!")
            flag_rechoocing_cell = True
            continue
        elif response_move == user_side:
            print("Поздравляю, вы победили!")
            break
        elif response_move == server_side:
            print("На этот раз победил я. Ха.")
            break
        elif counter_steps == 9:
            print("Ничья!")
            break

        flag_rechoocing_cell = False

        if order == user_side:
            move = input("Ваш ход: ")
        else:
            if move:
                client.send(' '.join(move).encode())
            move = client.recv(512).decode('utf-8')

        move = move.split()
        response_move = tic_tac_toe_field.do_move(
            int(move[0]), int(move[1]), order)

        if response_move != -1:
            counter_steps += 1
            order += 1
            order = (order + 1) % 2 + 1

    flag_is_continue = input(
        "Хотите продолжить? Введите цифру 1 чтобы продолжить. Чтобы закончить введите любой другой символ:  ")
    if flag_is_continue != '1':
        client.send("0".encode())
        break

    os.system("cls")
    tic_tac_toe_field.clear_field()
    client.send("1".encode())
