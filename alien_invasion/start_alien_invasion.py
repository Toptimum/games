""" Главный модуль игры """

from pygame import init, display, sprite, mixer

from settings import Settings
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from game_functions import check_events, update_screen, create_fleet, update_aliens, update_bullets
from ship import Ship


def run_game():
    """ Инициализируем игру и создаем объект экрана """
    # инициализация
    init()
    settings = Settings()
    # экран
    screen = display.set_mode((settings.width_screen, settings.height_screen))
    display.set_caption(settings.title_game)
    play_button = Button(settings, screen, 'Играть')
    # music
    mixer.music.load('sounds/background_music.mp3')
    mixer.music.play(-1)

    # инициализируем статистику
    stats = GameStats(settings)
    scoreboard = Scoreboard(settings, screen, stats)
    # корабль и пули
    ship = Ship(settings, screen)
    bullets = sprite.Group()
    # пришельцы и их пули
    aliens = sprite.Group()
    bullets_aliens = sprite.Group()
    # создание флота пришельцев
    create_fleet(settings, screen, ship, aliens)

    # основной цикл программы для отслеживания событий в игре
    while True:
        # функция обработки событий в игре
        check_events(settings, stats, scoreboard, screen, ship, aliens, bullets, bullets_aliens, play_button)

        if stats.game_active:
            # изменяем положение корабля
            ship.update_position()
            # обновляем позиции пуль
            update_bullets(settings, stats, scoreboard, screen, ship, aliens, bullets, bullets_aliens)
            # перемещаем пришельцев
            update_aliens(settings, stats, scoreboard, screen, ship, aliens, bullets, bullets_aliens)

        # перерисовываем экран
        update_screen(settings, stats, scoreboard, screen, ship, aliens, bullets, bullets_aliens, play_button)


run_game()
