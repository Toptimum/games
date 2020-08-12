""" Модуль управления поведением пули """

from pygame import sprite, Rect, draw


class Bullet(sprite.Sprite):
    """ Класс управления пулями, которыми стреляет корабль """

    def __init__(self, settings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen
        # характеристики пули
        self.rect = Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.bullet_color = settings.bullet_color
        self.bullet_speed_factor = settings.bullet_speed_factor
        # положение пули
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

    def update(self):
        """ Перемещаем пулю вверх по экрану """
        self.rect.y -= self.bullet_speed_factor

    def draw_bullet(self):
        """ Выводим пулю на экране """
        draw.rect(self.screen, self.bullet_color, self.rect)
