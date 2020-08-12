""" Игра Крестики-нолики """
from copy import copy
from random import choice, randint


def show_board(board_in):
    """ Выводим игровое поле """
    print(f" {board_in[7]} | {board_in[8]} | {board_in[9]} \n"
          f" {board_in[4]} | {board_in[5]} | {board_in[6]} \n"
          f" {board_in[1]} | {board_in[2]} | {board_in[3]} \n")


def choose_sign_player():
    """ Определяем знак для игрока """
    sign_player_in = input("Выберите ваш знак: 'X' или 'O'. Введите букву: ").upper()
    # проверяем корректность ввода (учитываем русские и английские буквы - они одинаковые)
    while sign_player_in != 'X' and sign_player_in != 'O' and sign_player_in != 'Х' and sign_player_in != 'О':
        print("Ошибка ввода: вы ввели недопустимое значение. Пожалуйста, введите 'X' или 'O'.")
        sign_player_in = input("Выберите ваш знак: 'X' или 'O'. Введите букву: ").upper()
    # назначаем противоположный знак компьютеру
    if sign_player_in == 'X' or sign_player_in == 'Х':  # принимаем английские и русские буквы
        return sign_player_in, 'O'
    else:
        return sign_player_in, 'X'


def who_goes_first():
    """ Определяем, кто первым будет ходить """
    first_step_in = choice(['игрок', 'компьютер'])
    if first_step_in == 'игрок':
        print("Первый ход сделаете Вы.")
    else:
        print("Первый ход сделает компьютер.")
    return first_step_in


def determine_victory(board_in, sign_player_in):
    """ Универсальная функция для определения победы игрока или компьютера """
    # проверяем 3 горизонтали
    if board_in[1] == board_in[2] == board_in[3] == sign_player_in:
        return True
    elif board_in[4] == board_in[5] == board_in[6] == sign_player_in:
        return True
    elif board_in[7] == board_in[8] == board_in[9] == sign_player_in:
        return True
    # проверяем 3 вертикали
    elif board_in[7] == board_in[4] == board_in[1] == sign_player_in:
        return True
    elif board_in[8] == board_in[5] == board_in[2] == sign_player_in:
        return True
    elif board_in[9] == board_in[6] == board_in[3] == sign_player_in:
        return True
    # проверяем 2 диагонали
    elif board_in[7] == board_in[5] == board_in[3] == sign_player_in:
        return True
    elif board_in[9] == board_in[5] == board_in[1] == sign_player_in:
        return True
    else:
        return False


def player_move(board_in, sign_player_in):
    """ Корректный ход игрока """
    # бесконечный цикл проверки ввода
    while True:
        move = input("Ваш ход. Посмотрите Num-блок на клавиатуре и нажмите цифру (1-9), куда хотите поставить свой "
                     "знак? Введите цифру: ")
        if move.isdigit():  # ввели цифру или нет
            move = int(move)
            if move not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:  # цифра от 1 до 9 или нет
                print("Цифра должна быть от 1 до 9.")
            elif board_in[move] != ' ':  # заполнять можно только пусте ячейки на поле
                print(f"Ячейка '{move}' занята. Вам необходимо выбрать пустую ячейку на поле.")
            else:
                # все проверки пройдены, заполняем ячейку поля
                board_in[int(move)] = sign_player_in
                break
        else:
            print("Ошибка ввода - необходимо вводить только цифры от 1 до 9.")
    return board_in


def computer_move(board_in, sign_computer_in, sign_player_in):
    """ Компьютер делает ход """
    # вариант 1: сначала ищем ячейку, которая приведет к победе компьютера
    for step in range(1, 10):
        if board_in[step] == ' ':
            # скопируем поле для имитации хода
            copy_board = copy(board_in)
            copy_board[step] = sign_computer_in
            if determine_victory(copy_board, sign_computer_in):
                board_in[step] = sign_computer_in
                return board_in
    # вариант 2: необходимо помешать выиграть пользователю - предсказываем ход пользователя и ставим знак компьютера
    for step in range(1, 10):
        if board_in[step] == ' ':
            # скопируем поле для имитации хода
            copy_board = copy(board_in)
            copy_board[step] = sign_player_in
            if determine_victory(copy_board, sign_player_in):
                board_in[step] = sign_computer_in
                return board_in
    # вариант 3: компьютер ставит свой знак в любую свободную клетку на поле
    while True:
        step = randint(1, 9)
        if board_in[step] == ' ':
            break
    board_in[step] = sign_computer_in
    return board_in


if __name__ == '__main__':
    # выводим описание игры
    print("Игра 'Крестики-нолики'.\nВам необходимо за несколько шагов собрать последовательность из 3-х знаков: "
          "по горизонтали, вертикали или диагонали.\nПротив вас играет компьютер с простым интеллектом.")
    # определяем переменные
    board = [' '] * 10
    # выводим игровое поле
    print("Пустое игровое поле:")
    show_board(board)
    sign_player, sign_computer = choose_sign_player()
    player = who_goes_first()
    # основной цикл игры
    while True:
        if ' ' in board[1:9]:  # пока имеются пустые клетки на поле, игра продолжается
            # ходит пользователь
            if player == 'игрок':
                # игрок делает ход
                board = player_move(board, sign_player)
                # выводим поле
                show_board(board)
                # определяем победу
                if determine_victory(board, sign_player):
                    print("Поздравляем! Вы победили.")
                    break
                else:  # смена хода
                    player = 'компьютер'
            else:  # ходит компьютер
                # компьютер делает ход
                board = computer_move(board, sign_computer, sign_player)
                # выводим поле
                print("Компьютер сделал ход:")
                show_board(board)
                # проверяем победу
                if determine_victory(board, sign_computer):
                    print("Компьютер победил.")
                    break
                else:  # смена хода
                    player = 'игрок'
        else:
            print("Все клетки заполнены. Никто не победил - ничья.")
            break
