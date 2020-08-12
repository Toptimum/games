""" Игра 'Охотник за сокровищами' """

from random import randint
from math import sqrt


def show_description(max_treasures_in, max_sonars_in, sonar_depth_in):
    """ Выводим описание игры и правила """
    print(f"Игра 'Охотник за сокровищами'.\nВам необходимо найти {max_treasures_in} сокровища на дне океана. И для "
          f"этого у вас есть {max_sonars_in} гидролокаторов - они подскажут вам, на каком расстоянии находится "
          f"сокровище,\nно не покажут в каком направлении его искать. Глубина действия гидролокатора {sonar_depth_in} "
          f"клеток. Вам необходимо вводить координаты X-Y, чтобы опустить сонар на дно океана.\nПосле чего на карте "
          f"океана отобразится:\n\t0 - означает, что в этой зоне ничего нет,\n\tцифра (1-{sonar_depth_in}) - это "
          f"дистанция до ближайшего сокровища,\n\tили буква 'С' - точно обнаруженное сокровище.\nУдачи в поисках!")


def generate_new_ocean(width_in=100, height_in=10):
    """ Генерируем поле океана """
    # формируем океан
    ocean_board_in = [['~'] * width_in for _ in range(height_in)]
    return ocean_board_in


def generate_treasures(width_in, height_in, max_treasures_in=3):
    """ Генерируем координаты сокровищ случайным образом """
    all_treasures_in = []
    for i in range(0, max_treasures_in):
        all_treasures_in.append([randint(0, width_in), randint(0, height_in)])
    return all_treasures_in


def show_ocean_board(ocean_board_in, all_treasures_in, max_sonars_in):
    """ Выводим океан с полями и данными """
    # красивый вывод океана
    # выводим десятки по x
    x_axis_dozens = ''
    for i in range(1, int((len(ocean_board[0]) / 10))):
        x_axis_dozens += f"         {i}"
    print(f"\nОкеан с сокровищами:\n   {x_axis_dozens}")
    # выводим единицы по х
    x_axis = '0123456789' * int((len(ocean_board[0]) / 10))
    print(f"  {x_axis}")
    # выводим значения y
    for index, y in enumerate(ocean_board_in):
        print(f"{index} {''.join(y)}")
    print(f"В океане сокровищ: {len(all_treasures_in)} шт. У вас осталось гидролокаторов: {max_sonars_in} шт.\n")


def correct_enter_coordinates(width_in, height_in, previous_moves_in):
    """ Корректный ввод координат для гидролокатора """
    while True:
        try:
            x, y = input("Куда опустить гидролокатор? Введите координаты X-Y через дефис (например, 56-4): ").split('-')
            while not x.isdigit() or not y.isdigit() or int(x) > width_in - 1 or int(y) > height_in - 1 or \
                    [int(x), int(y)] in previous_moves_in:
                if not x.isdigit() or not y.isdigit():
                    print("Необходимо вводить цифры через дефис. Например, 10-2.")
                elif int(x) > width_in - 1 or int(y) > height_in - 1:
                    print(f"Координата X должна быть от 0 до {width_in - 1}, а Y - от 0 до {height_in - 1}.")
                else:
                    print("Вы уже опускали здесь гидролокатор. Укажите другие координаты.")
                x, y = input("Введите координаты X-Y через дефис (например, 56-4): ").split('-')
        except ValueError:
            print("Ошибка ввода.")
        else:
            sonar_x_y_in = [int(x), int(y)]
            previous_moves_in.append([int(x), int(y)])
            return sonar_x_y_in, previous_moves_in


def determine_destination(width_in, all_treasures_in, sonar_x_y_in, sonar_depth_in):
    """ Определяем расстояние до скоровища по теореме Пифагора sqrt(c2 = a^2 + b^2) """
    smallest_distance = width_in
    for cx, cy in all_treasures_in:
        distance = int(sqrt((cx - sonar_x_y_in[0]) ** 2 + (cy - sonar_x_y_in[1]) ** 2))
        if distance < smallest_distance:
            smallest_distance = distance
    if smallest_distance <= sonar_depth_in:
        return str(smallest_distance)
    else:
        return False


def ocean_search(ocean_board_in, width_in, all_treasures_in, max_sonars_in, sonar_x_y_in, sonar_depth_in):
    """ Устанавливаем значение на поле океана """
    # если точно попали в сокровище
    if sonar_x_y_in in all_treasures_in:
        print("Вы точно нашли сокровище!")
        ocean_board[sonar_x_y[1]][sonar_x_y[0]] = 'С'
        all_treasures_in.remove(sonar_x_y)
    # если обнаружили сокровище в определенной зоне
    elif determine_destination(width_in, all_treasures_in, sonar_x_y_in, sonar_depth_in):
        print("В этой зоне обнаружено сокровище - продолжайте поиски!")
        ocean_board[sonar_x_y[1]][sonar_x_y[0]] = determine_destination(width_in, all_treasures_in,
                                                                        sonar_x_y_in, sonar_depth_in)
    else:  # если ничего не нашли
        print("В этой зоне ничего не найдено. Выберите другую зону для поиска.")
        ocean_board[sonar_x_y[1]][sonar_x_y[0]] = '0'
    # в любом случае один гидролокатор уже использован
    max_sonars_in -= 1
    return ocean_board_in, all_treasures_in, max_sonars_in


if __name__ == '__main__':
    # задаем параметры
    WIDTH, HEIGHT, max_treasures, max_sonars, SONAR_DEPTH = 100, 10, 3, 25, 9
    # выводим описание игры
    show_description(max_treasures, max_sonars, SONAR_DEPTH)
    # генерируем океан
    ocean_board = generate_new_ocean(WIDTH, HEIGHT)
    # генерируем координаты сокровищ
    all_treasures = generate_treasures(WIDTH, HEIGHT, max_treasures)
    # выводим океан для демонстрации поля
    show_ocean_board(ocean_board, all_treasures, max_sonars)
    # ведем запись предыдущих ходов игрока
    previous_moves = []
    # основной цикл игры
    while len(all_treasures) > 0 and max_sonars > 0:
        # определяем координаты для очередного гидролокатора
        sonar_x_y, previous_moves = correct_enter_coordinates(WIDTH, HEIGHT, previous_moves)
        # ищем сокровище в океане
        ocean_board, all_treasures, max_sonars = ocean_search(ocean_board, WIDTH, all_treasures,
                                                              max_sonars, sonar_x_y, SONAR_DEPTH)
        # выводим океан с данными
        show_ocean_board(ocean_board, all_treasures, max_sonars)

    # подводим итоги игры
    if len(all_treasures) == 0:
        print("Поздравляем! Вы нашли все сокровища в океане.")
    elif max_sonars == 0:
        print(f"К сожалению, вы использовали все попытки. В океане осталось сокровища: {all_treasures}.")
