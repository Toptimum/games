""" Модуль инопланетянина """

from pygame import image, sprite


class Alien(sprite.Sprite):
    """ Класс инопланетянина """

    def __init__(self, settings, screen):
        """ Инициализируем пришельца и задаем его изначальную позицию """
        super(Alien, self).__init__()
        self.screen = screen
        self.settings = settings

        # задаем картинку пришельцу
        self.image = image.load('images/alien_ship_mini_with_shadow.png').convert_alpha()
        self.rect = self.image.get_rect()

        # задаем изначальные координаты инопланетянину
        self.rect.x = self.rect.width  # слева от него добавляется интервал, равный ширине пришельца
        self.rect.y = self.rect.height  # а над ним интервал, равный высоте пришельца

    def blit_alien(self):
        """ Выводим пришельца в текущей позиции """
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """ Проверка достижения прищельцем края экрана """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True  # значит достигли края экрана
        elif self.rect.left <= 0:
            return True

    def update(self):
        """ Перемещаем пришельца вправо """
        self.x += (self.settings.alien_speed_factor * self.settings.fleet_direction)
        self.rect.x = self.x

# данные для тестирования
# if __name__ == "__main__":
#     # инициализация
#     init()
#     settings = Settings()
#     # экран
#     screen = display.set_mode((settings.width_screen, settings.height_screen))
#     display.set_caption(settings.title_game)
#     screen.fill(settings.background_color)
#     # пришелец
#     alien = Alien(screen)
#     alien.blit_alien()
#     # отображение
#     display.flip()
#     time.delay(5000)
