""" Модуль с основными функциями игры """

from pygame import display, event, QUIT, sprite, transform, font, mixer
from pygame import mouse, MOUSEBUTTONDOWN, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_SPACE, K_q, K_p
from time import sleep

from alien import Alien
from bullet_alien import BulletAlien
from bullet import Bullet

mixer.init()
sound_hit_alien = mixer.Sound('sounds/hit_alien.ogg')
sound_shot = mixer.Sound('sounds/shot.ogg')
sound_shot_down_ship = mixer.Sound('sounds/shot_down_ship.ogg')


def check_key_down_events(current_event, settings, screen, ship, bullets):
    """ Обработка событий по нажатию клавиш """
    if current_event.key == K_RIGHT:
        ship.moving_right = True
    elif current_event.key == K_LEFT:
        ship.moving_left = True
    elif current_event.key == K_SPACE:
        sound_shot.play()
        fire_bullet(settings, screen, ship, bullets)


def check_key_up_events(current_event, ship):
    """ Обработка событий по отпусканию клавиш """
    if current_event.key == K_RIGHT:
        ship.moving_right = False
    elif current_event.key == K_LEFT:
        ship.moving_left = False


def check_events(settings, stats, scoreboard, screen, ship, aliens, bullets, bullets_aliens, play_button):
    """ Обрабатывает нажатия клавиш и мыши, реагирует на события в игре """
    for current_event in event.get():
        # событие выхода из игры или при нажатии q на клавиатуре
        if current_event.type == QUIT or (current_event.type == KEYDOWN and current_event.key == K_q):
            check_beat_record_score(stats)  # проверяем побит ли рекорд
            exit()
        # запуск новой игры по клавише 'p'
        if current_event.type == KEYDOWN and current_event.key == K_p:
            start_new_game(settings, stats, scoreboard, screen, ship, aliens, bullets, bullets_aliens)
        # отслеживаем клик мыши по кнопке
        elif current_event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = mouse.get_pos()
            check_play_button(settings, screen, stats, scoreboard, play_button, ship, aliens, bullets_aliens, bullets,
                              mouse_x, mouse_y)
        # когда клавиши нажимаем
        elif current_event.type == KEYDOWN:
            check_key_down_events(current_event, settings, screen, ship, bullets)
        # и отпускаем клавиши
        elif current_event.type == KEYUP:
            check_key_up_events(current_event, ship)


def check_play_button(settings, screen, stats, scoreboard, play_button, ship, aliens, bullets_aliens, bullets, mouse_x,
                      mouse_y):
    """ Запускаем новую игру при нажатии кнопки Играть """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:  # новый запуск игры только, когда игра неактивна
        start_new_game(settings, stats, scoreboard, screen, ship, aliens, bullets, bullets_aliens)


def start_new_game(settings, stats, scoreboard, screen, ship, aliens, bullets, bullets_aliens):
    """ Сбрасываем все для запуска новой игры """
    # скроем указатель мыши, чтобы не мешал во время игры
    mouse.set_visible(False)
    # сброс статистики
    stats.reset_stats()
    settings.init_dynamic_settings()
    stats.game_active = True
    # сбрасываем изображения счета и уровня
    scoreboard.prep_images()
    # удаляем флот пришельцев и все пули
    aliens.empty()
    bullets.empty()
    bullets_aliens.empty()
    # создаем новый флот и размещаем корабль
    create_fleet(settings, screen, ship, aliens)
    ship.center_ship()


def update_screen(settings, stats, scoreboard, screen, ship, aliens, bullets, bullets_aliens, play_button):
    """ Перерисовываем экран с объектами игры """
    # заливаем экран цветом
    screen.fill(settings.background_color)
    # отображаем пули
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # отображаем пули пришельцев
    for bullet_alien in bullets_aliens.sprites():
        bullet_alien.draw_bullet()
    # отображаем корабль на экране
    ship.blit_ship()
    # отображаем пришельцев на экране
    aliens.draw(screen)
    # выводим счета
    scoreboard.show_score()
    # отображаем кнопку
    if not stats.game_active:
        # заливаем экран цветом
        screen.fill(settings.background_color)
        play_button.draw_button()
    # отображение последнего прорисованного экрана
    display.flip()


def get_number_aliens_x(settings, alien_width):
    """ Вычисляем кол-во пришельцев в ряду """
    available_space_x = settings.width_screen - 2 * alien_width  # определяем длину ряда за вычетом пространства
    number_aliens_x = int(available_space_x / (2 * alien_width))  # определяем кол-во приельцев в ряд
    return number_aliens_x


def get_number_rows(settings, ship_height, alien_height):
    """ Определяем кол-во рядов, помещающихся на экране """
    available_space_y = (settings.height_screen - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(settings, screen, aliens, alien_number, row_number):
    """ Создаем пришельца и размещаем его в ряду """
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    # интервал между пришельцами равен одному пришельцу
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(settings, screen, ship, aliens):
    """ Генерируем флот пришельцев """
    # создание пришельца и вычисление пришельцев в ряду
    alien = Alien(settings, screen)
    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)
    # создание флота пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(settings, aliens):
    """ Реагирует при достижении прищельцем края экрана """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings, aliens):
    """ Опускает весь флот и меняет направление на противоположное """
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def the_end(settings, stats, scoreboard, screen):
    message = "Конец игры."
    font_message = font.SysFont(None, 50)
    image_message = font_message.render(message, True, settings.text_color, settings.background_color)
    # вывод надписи в центре экрана
    image_message_rect = image_message.get_rect()
    image_message_rect.centerx = screen.get_rect().centerx
    image_message_rect.centery = screen.get_rect().centery
    screen.blit(image_message, image_message_rect)

    display.flip()
    check_beat_record_score(stats)
    stats.game_active = False
    sleep(3)
    mouse.set_visible(True)  # в конце игры включаем указатель мыши


def ship_hit(settings, stats, scoreboard, screen, ship, bullets, aliens, bullets_aliens):
    """ Обрабатываем столкновения корабля """
    if stats.ships_left > 1:
        # уменьшаем кол-во жизней
        sound_shot_down_ship.play()
        stats.ships_left -= 1
        scoreboard.prep_ships()
        # уничтожаем всех пришельцев и пули
        aliens.empty()
        bullets.empty()
        bullets_aliens.empty()
        # создаем новый флот пришельцев и корабль игрока - инициализируем новый уровень
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()
        # задержка, чтобы пользователь заметил столкновение и "перезагрузку" уровня
        sleep(1)
    else:
        the_end(settings, stats, scoreboard, screen)


def check_aliens_bottom(settings, stats, scoreboard, screen, ship, bullets, aliens, bullets_aliens):
    """ Проверяем, добрались ли пришельцы до нижнего края экрана """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # сбрасываем положение корабля и флота пришельцев
            ship_hit(settings, stats, scoreboard, screen, ship, bullets, aliens, bullets_aliens)
            break  # выходим из цикла проверки


def update_aliens(settings, stats, scoreboard, screen, ship, aliens, bullets, bullets_aliens):
    """ Проверяем достиг ли флот края экрана, после чего меняем позиции пришельцев """
    # проверяем, не вылетает ли флот пришельцев за пределы экрана
    check_fleet_edges(settings, aliens)
    aliens.update()

    # проверка столкновения пришельцев и корабля игрока
    if sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, scoreboard, screen, ship, bullets, aliens, bullets_aliens)

    # проверяем, добрались ли пришельцы до нижнего края экрана
    check_aliens_bottom(settings, stats, scoreboard, screen, ship, bullets, aliens, bullets_aliens)


def update_bullets(settings, stats, scoreboard, screen, ship, aliens, bullets, bullets_aliens):
    """ Обновляем позиции пуль и удаляем их, когда те вылетают за пределы окна """
    bullets.update()
    # уничтожение исчезнувших пуль
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    bullets_aliens.update()
    # уничтожение пуль пришельцев, вылетевших за пределы экрана
    for bullet_alien in bullets_aliens.copy():
        if bullet_alien.rect.top >= settings.height_screen:
            bullets_aliens.remove(bullet_alien)

    check_bullets_collisions(settings, stats, scoreboard, screen, ship, bullets, aliens, bullets_aliens)


def check_beat_record_score(stats):
    """ Проверяем побит ли текущий рекорд и записываем новый рекорд в файл """
    if stats.current_score > stats.record_score:
        stats.record_score = stats.current_score
        stats.write_high_score()


def blur_surface(surface, amt):
    """
    Blur the given surface by the given 'amount'.  Only values 1 and greater
    are valid.  Value 1 = no blur.
    """
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s" % amt)
    scale = 1.0 / float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = transform.smoothscale(surface, scale_size)
    surf = transform.smoothscale(surf, surf_size)
    return surf


def check_bullets_collisions(settings, stats, scoreboard, screen, ship, bullets, aliens, bullets_aliens):
    """ Проверка попадания пули в пришельца, при попадании удаляем пулю и пришельца """
    # True говорят, нужно ли удалять столкнувшиеся объекты
    collisions_aliens = sprite.groupcollide(bullets, aliens, True, True)
    if collisions_aliens:
        # sound_hit_alien.play()
        for aliens in collisions_aliens.values():
            stats.current_score += settings.alien_points * len(aliens)
            scoreboard.prep_score()
            # check_high_score(stats, scoreboard)
            # убитый пришелец делает последний выстрел
            bullet_alien = BulletAlien(settings, screen, aliens[0])
            bullets_aliens.add(bullet_alien)

    collisions_ships = sprite.spritecollide(ship, bullets_aliens, True)
    if collisions_ships:
        #sound_shot_down_ship.play()
        ship_hit(settings, stats, scoreboard, screen, ship, bullets, aliens, bullets_aliens)

    collisions_bullets = sprite.groupcollide(bullets, bullets_aliens, True, True)

    # когда флот пришельцев уничтожен, генерируем новый уровень
    if len(aliens) == 0:
        start_new_level(settings, stats, scoreboard, screen, ship, aliens, bullets)


def start_new_level(settings, stats, scoreboard, screen, ship, aliens, bullets):
    """ Повышаем уровень: уничтожаем пули, повышаем скорость, выводим данные, генерируем новый флот пришельцев """
    bullets.empty()
    settings.increase_speed()
    stats.level += 1
    scoreboard.prep_level()
    create_fleet(settings, screen, ship, aliens)


def fire_bullet(settings, screen, ship, bullets):
    """ Выстрел пули """
    if len(bullets) < settings.max_quantity_bullets:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)
