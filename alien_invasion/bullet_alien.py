""" Модуль управления поведением пули """

from pygame import Rect, draw, sprite


class BulletAlien(sprite.Sprite):
    """ Класс пули, которая вылетает из пришельца """

    def __init__(self, settings, screen, alien):
        super(BulletAlien, self).__init__()
        self.screen = screen
        # характеристики пули
        self.rect = Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.bullet_color = settings.bullet_color
        self.bullet_speed_factor = settings.bullet_speed_factor / 2  # пули пришельца в 2 раза медленнее
        # положение пули
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

    def update(self):
        """ Перемещаем пулю вниз по экрану """
        self.rect.y += self.bullet_speed_factor

    def draw_bullet(self):
        """ Выводим пулю на экране """
        draw.rect(self.screen, self.bullet_color, self.rect)
