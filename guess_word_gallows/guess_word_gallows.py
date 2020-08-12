from random import choice

from constants import HANGED_MAN_GALLOWS, POSSIBLE_WORDS


def generate_secret_word():
    """ Генерируем случайное слово из возможных """
    category_in = choice(list(POSSIBLE_WORDS))
    secret_word_in = choice(POSSIBLE_WORDS[category_in])
    return secret_word_in, category_in


def correct_enter_letter():
    """ Запрашиваем ввод буквы у пользователя """
    user_letter_in = input("Введите русскую букву: ").lower()
    while user_letter_in in guessed_letters or user_letter_in in wrong_letters or user_letter_in.isdigit():
        if user_letter_in in guessed_letters or user_letter_in in wrong_letters:
            print("Вы уже вводили такую букву. Пожалуйста, введите другую букву.")
        elif user_letter_in.isdigit():
            print("Ошибка ввода: необходимо вводить букву, а не цифру.")
        user_letter_in = input("Введите русскую букву: ").lower()
    return user_letter_in


def find_letter_word(user_letter_in):
    """ Ищем букву пользователя в загаданном слове """
    if user_letter_in in SECRET_WORD:
        guessed_letters.append(user_letter_in)
        print(f"Буква '{user_letter_in}' есть в загаданном слове!")
    else:
        wrong_letters.append(user_letter_in)
        print(f"Буквы '{user_letter_in}' нет в загаданном слове.")


def generate_blank_secret_word():
    """ Формируем бланк загаданного слова с угаданными буквами """
    blank_in = ['_' for _ in range(len(SECRET_WORD))]  # используем список для упрощения замены символа буквой
    for letter in guessed_letters:  # сначала находим букву среди разгаданных
        for index_letter in range(len(SECRET_WORD)):  # затем в бланке открываем все разгаданные буквы
            if letter == SECRET_WORD[index_letter]:
                blank_in[index_letter] = letter
    blank_in = ' '.join(blank_in).upper()  # вместо списка возвращаем строку для упрощения вывода
    return blank_in


SECRET_WORD, category = generate_secret_word()  # загадываем слово
print(f"Игра 'Виселица'.\n"
      f"Мы загадали слово из {len(SECRET_WORD)} букв из категории '{category}'. Угадайте слово по буквам!\n"
      f"Если не угадаете слово за {len(HANGED_MAN_GALLOWS) - 1} попыток, то человечек будет повешан.")
guessed_letters, wrong_letters = [], []  # угаданные и ошибочные буквы

# основной цикл игры
while len(wrong_letters) < len(HANGED_MAN_GALLOWS) - 1:
    # формируем бланк загаданного слова
    blank = generate_blank_secret_word()
    print(f"\nЗагаданное слово: {blank}")
    # выводим ошибочные буквы
    if wrong_letters:
        print(f"В слове нет букв: {', '.join(wrong_letters)}.")
    # проверяем не разгаданно ли слово
    if '_' not in blank:
        print("Вы отгадали слово и спасли человеку жизнь!")
        break
    else:  # запрашиваем у пользователя ввод буквы
        user_letter = correct_enter_letter()
    # ищем букву в загаданном слове
    find_letter_word(user_letter)
    # выводим виселицу в зависимости от количества попыток
    print(HANGED_MAN_GALLOWS[len(wrong_letters)])

if len(wrong_letters) == len(HANGED_MAN_GALLOWS) - 1:
    print("К сожалению, вы исчерпали все попытки.")
    if len(guessed_letters) < 5:
        print(f"Программа загадывала слово '{SECRET_WORD}'.")

print("Игра завершена.")
