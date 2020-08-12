""" Модуль вывода данных в игре """

from pygame import font, sprite

from ship import Ship


class Scoreboard:
    """ Класс вывода игровой информации """

    def __init__(self, settings, screen, stats):
        """ Инициализируем атрибуты подсчет очков """
        self.settings = settings
        self.screen = screen
        self.stats = stats

        # настройки шрифта для вывода счета
        self.text_color = settings.text_color
        self.font = font.SysFont('Verdana', 20)
        # подготовка исходного изображения
        self.prep_images()

    def prep_score(self):
        """ Преобразуем текущий счет в графическое изображение """
        rounded_score = int(round(self.stats.current_score, -1))  # c -1 округляем до десятков, сотен и т.д.
        score_str = "счет " + "{:,}".format(rounded_score).replace(',', ' ')
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.background_color)

        # вывод счета в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen.get_rect().right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """ Преобразуем рекордный счет в изображение """
        high_score = int(round(self.stats.record_score, -1))
        high_score_str = "рекорд " + "{:,}".format(high_score).replace(',', ' ')
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.background_color)

        # вывод счета по центру верхней части экрана
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen.get_rect().centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """ Преобразуем номер уровня в изображение """
        self.level_image = self.font.render(f"уровень {self.stats.level}", True, self.text_color,
                                            self.settings.background_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """ Формируем кол-во оставшихся жизней """
        self.ships = sprite.Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_images(self):
        """ Разом подготавливаем все изображения статистики """
        self.prep_ships()
        self.prep_score()  # сначала вызываем score
        self.prep_high_score()  # потому что high_score зависит от положения score
        self.prep_level()

    def show_score(self):
        """ Выводим счет на экране """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
