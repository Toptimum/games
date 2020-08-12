""" Модуль для реализаии кнопок в игре """

from pygame import font, Rect


class Button:
    """ Класс кнопки """

    def __init__(self, settings, screen, msg):
        """ Инициализируем атрибуты кнопки """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # назначение размером и свойств кнопок
        self.width, self.height = 200, 50
        self.button_color = (150, 150, 150)
        self.shadow_color = (120, 120, 120)
        self.text_color = (255, 255, 255)
        self.font = font.SysFont(None, 48)  # используем шрифт по умолчанию, большого размера
        # объект кнопки и выраванивание
        self.rect = Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect_shadow = Rect(0, 0, self.width, self.height)
        self.rect_shadow.center = self.screen_rect.center
        self.rect_shadow.top += 1
        self.rect_shadow.left += 1
        # задаем сообщение кнопки
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """ Преобразуем текст в изображение и выравниваем по центру """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """ Отображение кнопки с сообщением """
        self.screen.fill(self.shadow_color, self.rect_shadow)
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
