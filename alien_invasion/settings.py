""" Модуль настроек игры """


class Settings:
    """ Класс для хранения настроек игры """

    def __init__(self):
        """ Инициализируем статические настройки """
        # настройки экрана
        self.title_game = "Игра Alien Invasion на Python © Житников Тарас 2020"
        self.width_screen = 1000
        self.height_screen = 700
        self.background_color = (230, 230, 230)
        # настройки корабля
        self.ships_limit = 3
        # настройки пули
        self.bullet_width = 20
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.max_quantity_bullets = 3
        # настройки пришельцев
        self.fleet_drop_speed = 10  # величина снижения флота
        # тем ускорения игры
        self.speedup_scale = 1.1
        # темп роста стоимости очков за подбитых пришельцев
        self.score_scale = 1.5
        self.init_dynamic_settings()
        self.file_score = 'record_score.txt'
        self.text_color = (30, 30, 30)

    def init_dynamic_settings(self):
        """ Инициализируем динамические параметры игры """
        self.ship_speed_factor = 2
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet_direction = 1 означает движение вправо, а -1 - влево
        self.fleet_direction = 1
        # начисление очков за попадание в пришельца
        self.alien_points = 50

    def increase_speed(self):
        """ При уничтожении всего флота, увеличиваем стоимость пришельцев и скорость игры """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        # self.bullet_width *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
