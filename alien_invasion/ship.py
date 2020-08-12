""" Модуль для управления кораблем """

from pygame import image, transform, sprite


class Ship(sprite.Sprite):
    """ Класс корабля """

    def __init__(self, settings, screen):
        """ Инициализирует корабль и задает его изначальную позицию """
        super(Ship, self). __init__()
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image_ship = image.load('images/spaceship_with_shadow.png').convert_alpha()

        # уменьшаем размер картинки
        self.new_size_ship = (self.image_ship.get_width() // 9, self.image_ship.get_height() // 9)
        self.image = transform.smoothscale(self.image_ship, self.new_size_ship)

        # задаем изначальные координаты кораблю
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 10

        # задаем скорость перемещения корабля
        self.ship_speed_factor = settings.ship_speed_factor

        # флаги премещения корабля
        self.moving_left, self.moving_right = False, False

    def update_position(self):
        """ Обновляем позицию корабля в зависимости от включенного направления """
        if self.moving_left and self.rect.left > 10:
            self.rect.centerx -= self.ship_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right - 10:
            self.rect.centerx += self.ship_speed_factor

    def center_ship(self):
        """ Размещаем корабль по центру в нижней части экрана """
        self.center = self.screen_rect.centerx

    def blit_ship(self):
        """ Рисуем корабль в текущей позиции """
        self.screen.blit(self.image, self.rect)
