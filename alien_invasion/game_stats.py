""" Отслеживание статистики в игре """


class GameStats:
    """ Класс для отслеживания статистики в игре """

    def __init__(self, settings):
        """ Инициализируем статистику """
        self.settings = settings
        self.ships_left = self.settings.ships_limit
        self.current_score = 0
        self.level = 1
        self.reset_stats()
        self.game_active = False  # игра запускается в неактивном состоянии
        self.record_score = 0  # рекорд не должен сбрасываться
        self.read_high_score()

    def read_high_score(self):
        """ Считываем рекорд из файла """
        try:
            with open(self.settings.file_score, encoding='utf-8') as file_obj:
                self.record_score = int(file_obj.read().rstrip())
        except FileNotFoundError:
            print("К сожалению, файл с рекордом не обнаружен.")

    def write_high_score(self):
        """ Записываем рекорд в файл """
        with open(self.settings.file_score, 'w', encoding='utf-8') as file_obj:
            file_obj.write(str(self.record_score))
            print(f"Новый рекорд {self.record_score} записан в файл.")

    def reset_stats(self):
        """ Сбрасываем статистику в игре """
        self.ships_left = self.settings.ships_limit
        self.current_score = 0
        self.level = 1
