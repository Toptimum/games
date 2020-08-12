""" Игра 'Полет в небе' """
from pygame import init, display, quit, time, font, image, transform, mixer
from pygame import event, KEYDOWN, QUIT, K_ESCAPE, mouse, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from os import environ
from sys import exit
from random import randint
from copy import copy

# инициализируем Pygame
init()

# константы
SIZE_WINDOW = 700
BACKGROUND_COLOR = (109, 183, 252)
COLOR_TEXT = (10, 10, 10)
NAME_FONT = 'Tahoma'
BIG_SIZE_FONT, MEDIUM_SIZE_FONT, SMALL_SIZE_FONT, LITTLE_SIZE_FONT = 35, 25, 15, 12
FPS = 60
MAX_COUNT_INSECTS, MAX_SPEED_INSECT, COST_INSECT = 2, 6, 10
MAX_COUNT_CLOUDS, MAX_SPEED_CLOUD, COST_CLOUD = 10, 6, 1
MAX_LIVES_PLAYER = 3


# функции
def exit_game():
    """ Корректный выход из игры """
    quit()
    exit()


def read_record_score():
    """ Считываем рекорд из файла """
    try:
        with open('record_score.txt', encoding='utf-8') as file_obj:
            return int(file_obj.read().rstrip())
    except FileNotFoundError:
        print("К сожалению, файл с рекордом не обнаружен.")
        return 0
    except ValueError:
        print("К сожалению, в файле недопустимое значение.")
        return 0


def waiting_press_any_key():
    """ Ставим игру на паузу в ожидании нажатия клавиши """
    while True:
        for ev in event.get():
            if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):  # отслеживаем выход из игры
                exit_game()
            elif ev.type == KEYDOWN or ev.type == MOUSEBUTTONDOWN:  # нажатие любой клавиши для начала игры
                return


def show_text(text_in, size_font, x, y):
    """ Генерируем текст с необходимыми параметрами и выводим его на экране """
    x, y = int(x), int(y)
    game_font = font.SysFont(NAME_FONT, size_font)
    text_obj = game_font.render(text_in, 1, COLOR_TEXT)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    window_surf.blit(text_obj, text_rect)


def welcome_screen(text_header, score_in, text_message):
    """ Выводим приветственный экран """
    window_surf.fill(BACKGROUND_COLOR)
    show_text(text_header, BIG_SIZE_FONT, SIZE_WINDOW / 2, SIZE_WINDOW / 2)
    show_text(score_in, MEDIUM_SIZE_FONT, SIZE_WINDOW / 2, SIZE_WINDOW / 2 + 50)
    show_text(text_message, SMALL_SIZE_FONT, SIZE_WINDOW / 2, SIZE_WINDOW / 2 + 150)
    display.update()
    waiting_press_any_key()


def show_help():
    """ Выводим пинструкцию по игре """
    window_surf.fill(BACKGROUND_COLOR)
    show_text('Инструкция', BIG_SIZE_FONT, SIZE_WINDOW / 2, SIZE_WINDOW / 2)
    text_message = ["Ваша задача набрать как можно больше очков и побить рекорд игры.",
                    "Для этого собирайте насекомых и избегайте тучь с молнией.",
                    "Перемещайте мышь и птичка тоже будет перемещаться.",
                    "Нажмите любую клавишу мыши для ускорения игры - получите больше очков.",
                    "За каждую 1000 очков вам вернется потерянная жизнь."]
    indent = 50
    for string in text_message:
        indent += 20
        show_text(string, SMALL_SIZE_FONT, SIZE_WINDOW / 2, SIZE_WINDOW / 2 + indent)

    show_text("Нажмите любую клавишу для продолжения.", SMALL_SIZE_FONT, SIZE_WINDOW / 2, SIZE_WINDOW / 2 + 250)
    display.update()
    waiting_press_any_key()


def player_control(player_in, score_in):
    """ Отслеживаем нажатия клавиш в игре """
    for ev in event.get():
        if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):  # отслеживаем выход из игры
            exit_game()
        elif ev.type == MOUSEMOTION:  # отслеживаем движение мышки
            player_in['rect'].centerx = ev.pos[0]
            player_in['rect'].centery = ev.pos[1]
        elif ev.type == MOUSEBUTTONDOWN:
            score_in['speed_game'] = 2
        elif ev.type == MOUSEBUTTONUP:
            score_in['speed_game'] = 1
    return player_in, score_in


def show_score(score_in):
    """ Во время игры выводим рекорд, текущий счет игрока и его жизни """
    record_score = score_in['record_score']
    current_score = score_in['current_score']
    lives_player = score_in['lives_player']
    show_text(f"® {record_score} — {current_score} {'♥' * lives_player}", LITTLE_SIZE_FONT, SIZE_WINDOW / 2, 10)


def music_control(status):
    """ Управление звуками и музыкой в игре """
    if status == 'play_background':
        mixer.music.load("sounds/background_music.mid")
        mixer.music.play(-1)
    elif status == 'player_catch_insect':
        mixer.Sound("sounds/eat_insect.wav").play()
    elif status == 'player_lost_life':
        mixer.Sound("sounds/player_crash_cloud.ogg").play()
    elif status == 'stop_background':
        mixer.music.stop()
        mixer.Sound("sounds/game_over.wav").play()
    elif status == 'game_over':
        mixer.Sound("sounds/game_over.wav").play()


def create_player():
    """ Создаем персонажа игры """
    image_player = transform.smoothscale(image.load("images/bird.png"), (32, 21))
    player_rect = image_player.get_rect()
    player_rect.right = SIZE_WINDOW
    player_rect.bottom = SIZE_WINDOW
    return {'image': image_player, 'rect': player_rect}


def create_cloud():
    """ Создаем объект облака """
    image_cloud = transform.smoothscale(image.load("images/cloud_lightning2.png"), (100, 78))
    cloud_rect = image_cloud.get_rect()
    cloud_rect.x = randint(0, SIZE_WINDOW - cloud_rect.width)
    cloud_rect.bottom = randint(-SIZE_WINDOW / 2, -5)
    return {'image': image_cloud, 'rect': cloud_rect, 'speed': randint(1, MAX_SPEED_CLOUD)}


def create_insect():
    """ Создаем объект насекомого """
    image_insect = transform.smoothscale(image.load("images/insect.png"), (14, 14))
    insect_rect = image_insect.get_rect()
    insect_rect.x = randint(0, SIZE_WINDOW - insect_rect.width)
    insect_rect.bottom = 0
    return {'image': image_insect, 'rect': insect_rect, 'speed': randint(1, MAX_SPEED_INSECT)}


def move_clouds(clouds_in, score_in):
    """ Перемещение облаков """
    for cloud_in in clouds_in[:]:
        cloud_in['rect'].y += cloud_in['speed']
        if cloud_in['rect'].top > SIZE_WINDOW:
            clouds_in.remove(cloud_in)
            score_in['current_score'] += (COST_CLOUD * score_in['speed_game'])
    return clouds_in, score_in


def move_insects(insects_in):
    """ Перемещение насекомых """
    for insect_in in insects_in[:]:
        insect_in['rect'].y += insect_in['speed']
        if insect_in['rect'].top > SIZE_WINDOW:
            insects_in.remove(insect_in)
    return insects_in


def player_catch_insect(player_in, score_in, insects_in):
    """ Проверяем, поймал ли игрок насекомое """
    for insect_in in insects_in[:]:
        if player_in['rect'].colliderect(insect_in['rect']):
            insects_in.remove(insect_in)
            score_in['current_score'] += (COST_INSECT * score_in['speed_game'])
            music_control('player_catch_insect')
    return score_in, insects_in


def player_crash_cloud(player_in, score_in, clouds_in):
    """ Игрок попал в облако с молнией """
    for cloud_in in clouds_in[:]:
        if player_in['rect'].colliderect(cloud_in['rect']):
            clouds_in = []
            score_in['lives_player'] -= 1
            music_control('player_lost_life')
    return score_in, clouds_in


def insect_crash_cloud(clouds_in, insects_in):
    """ Уничтожаем насекомое, которое попало в облако с молнией """
    for cloud_in in clouds_in:
        for insect_in in insects_in[:]:
            if insect_in['rect'].colliderect(cloud_in['rect']):
                insects_in.remove(insect_in)
    return insects_in


def cloud_crash_cloud(clouds_in):
    """ Облака уничтожают друг друга """
    clouds_copy1 = clouds_in
    for cloud_in1 in clouds_copy1:
        clouds_copy2 = copy(clouds_copy1)
        clouds_copy2.remove(cloud_in1)
        for cloud_in2 in clouds_copy2:
            if cloud_in1['rect'].colliderect(cloud_in2['rect']):
                try:
                    clouds_in.remove(cloud_in1)
                except ValueError:
                    pass
    return clouds_in


def add_life_player(score_in):
    """ За новую тысячу очков начисляем жизнь игроку """
    if score_in['lives_player'] < MAX_LIVES_PLAYER:
        if int(score_in['current_score'] / 1000) > score_in['added_lives']:
            score_in['lives_player'] += 1
            score_in['added_lives'] += 1
    return score_in


def update_screen(score_in, player_in, clouds_in, insects_in):
    """ Обновляем и отображаем объекты на экране """
    window_surf.fill(BACKGROUND_COLOR)  # заливаем окно
    show_score(score_in)  # выводим счет
    window_surf.blit(player_in['image'], player_in['rect'])  # отображаем игрока
    for cloud_in in clouds_in:  # отображаем облака
        window_surf.blit(cloud_in['image'], cloud_in['rect'])
    for insect_in in insects_in:  # отображаем насекомых
        window_surf.blit(insect_in['image'], insect_in['rect'])
    display.update()  # обновляем экран


def write_record_score(score_in):
    """ Записываем новый рекорд в файл """
    if score_in['record_score'] < score_in['current_score']:
        with open('record_score.txt', 'w', encoding='utf-8') as file_obj:
            file_obj.write(str(score_in['current_score']))
            print(f"Новый рекорд {score_in['current_score']} записан в файл.")
    else:
        print("Новый рекорд не установлен - в файл ничего не записано.")


# настраиваем экран
environ['SDL_VIDEO_CENTERED'] = '1'  # выводим окно программы в центре экрана
window_surf = display.set_mode((SIZE_WINDOW, SIZE_WINDOW))
display.set_caption("Игра 'Полет в небе' © Житников Тарас")

# дополнительные настройки
mouse.set_visible(False)  # отключаем указатель мыши
game_clock = time.Clock()  # будем ограничивать кадры в секундку

# бесконечный цикл для быстрого перезапуска игр
while True:
    # в начале игры считываем рекорд из файла
    score = {'record_score': read_record_score(), 'current_score': 0,
             'lives_player': MAX_LIVES_PLAYER, 'added_lives': 0,
             'speed_game': 1}
    # выводим приветственный экран
    welcome_screen("Игра «Полет в небе»", f"рекорд: {score['record_score']}", "Нажмите любую клавишу для начала игры.")
    show_help()

    # запускаем музыку
    music_control('play_background')
    # и создаем объекты для самой игры
    player = create_player()
    insects, clouds = [], []
    acceleration_mode = False

    # основной цикл действий в игре
    while score['lives_player'] > 0:  # играем до тех пор, пока есть жизни
        # создаем объекты для игры
        if len(clouds) < MAX_COUNT_CLOUDS:
            cloud = create_cloud()
            clouds.append(cloud)
        if len(insects) < MAX_COUNT_INSECTS:
            insect = create_insect()
            insects.append(insect)

        # отслеживаем нажатия клавиш и перемещаем объекты
        player, score = player_control(player, score)
        clouds, score = move_clouds(clouds, score)
        insects = move_insects(insects)

        # проверяем столкновения объектов
        score, clouds = player_crash_cloud(player, score, clouds)
        score, insects = player_catch_insect(player, score, insects)
        insects = insect_crash_cloud(clouds, insects)
        clouds = cloud_crash_cloud(clouds)

        # начисляем жизнь игроку по необходимости
        score = add_life_player(score)

        # отображаем объекты на экране
        update_screen(score, player, clouds, insects)
        # ограничиваем количество кадров в секунду
        game_clock.tick(FPS * score['speed_game'])

    # в конце игры запоминаем счет
    write_record_score(score)
    # останавливаем музыку
    music_control('stop_background')
    # и выводим завершающий экран
    welcome_screen("Конец игры.", f"ваш счет: {score['current_score']}", "Нажмите любую клавишу для продолжения.")
