import sqlite3
import random

# Подключение к базе данных или ее создание
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы пользователей ( создается в том случае,  если она отсутствует в корневой папке программы )
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  password TEXT)''')
conn.commit()

# Функция для регистрации нового пользователя
def register():
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("Пользователь с таким именем уже зарегистрирован.")
    else:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Регистрация прошла успешно!")

# Функция для аутентификации пользователя
def login():
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")


    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if user:
        print("Аутентификация успешна!")
        return True
    else:
        print("Неправильное имя пользователя или пароль.")
        return False

# Функция для игры в камень-ножницы-бумага
def rock_paper_scissors():
    choices = ['камень', 'ножницы', 'бумага']
    user_choice = input("Выберите камень, ножницы или бумагу (написать словом с любым регистром): ").lower()
    ai_choice = random.choice(choices)

    print(f"Вы выбрали: {user_choice}")
    print(f"ИИ выбрал: {ai_choice}")

    if user_choice in choices:
        if user_choice == ai_choice:
            print("Ничья!")
        elif (user_choice == 'камень' and ai_choice == 'ножницы') or \
             (user_choice == 'ножницы' and ai_choice == 'бумага') or \
             (user_choice == 'бумага' and ai_choice == 'камень'):
            print("Вы победили!")
        else:
            print("Вы проиграли!")
    else:
        print("Неправильный выбор. Попробуйте еще раз.")

# Функция для игры в "угадай число"
def guess_number():
    number_to_guess = random.randint(1, 100)
    attempts = 0

    print("Я загадал число от 1 до 100. Попробуй угадать его!")

    while True:
        try:
            guess = int(input("Введи свой вариант: "))
            attempts += 1

            if guess < number_to_guess:
                print("Загаданное число больше.")
            elif guess > number_to_guess:
                print("Загаданное число меньше.")
            else:
                print(f"Поздравляю! Ты угадал число {number_to_guess} за {attempts} попыток!")
                break
        except ValueError:
            print("Пожалуйста, введи число.")
# Основная часть программы
def hangman():
    words = ['краситель', 'облако', 'апельсин', 'мячик', 'персик', 'корабль', 'виселица', 'краска', 'парадная']  # Список слов для игры
    secret_word = random.choice(words).lower()  # Выбор случайного слова из списка
    guessed_letters = []  # Список для отслеживания угаданных букв
    attempts = 10  # Количество попыток

    print("Давай поиграем в Виселицу!\nТебе нужно угадать слово, которое я загадал")

    while attempts > 0:
        display_word = ''  # Слово для отображения игроку

        for letter in secret_word:
            if letter in guessed_letters:
                display_word += letter + ' '  # Отображение угаданных букв
            else:
                display_word += '_ '  # Скрытие неугаданных букв

        print(display_word)

        if display_word.replace(' ', '') == secret_word:
            print(f"Поздравляю, ты угадал слово '{secret_word}'!")
            break

        guess = input("Угадай букву или введи слово целиком: ").lower()

        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("Ты уже пробовал эту букву.")
            elif guess in secret_word:
                print("Правильно!")
                guessed_letters.append(guess)
            else:
                print("Неправильно!")
                attempts -= 1
        elif len(guess) > 1 and guess.isalpha():
            if guess == secret_word:
                print(f"Поздравляю, ты угадал слово '{secret_word}'!")
                break
            else:
                print("Неправильно!")
                attempts -= 1
        else:
            print("Некорректный ввод. Попробуй еще раз.")

        print(f"У тебя осталось {attempts} попыток.")

    if attempts == 0:
        print(f"К сожалению, ты не угадал слово. Загаданное слово было '{secret_word}'.")


while True:
    print("\n1. Регистрация")
    print("2. Вход")
    choice = input("Выберите опцию: ")

    if choice == '1':
        register()
    elif choice == '2':
        if login():
            while True:
                print("\n1. Камень-ножницы-бумага")
                print("2. Угадай число")
                print("3. Виселица")
                print("4. Выйти")
                game_choice = input("Выберите игру: ")

                if game_choice == '1':
                    rock_paper_scissors()
                elif game_choice == '2':
                    guess_number()
                elif game_choice == '3':
                    hangman()
                elif game_choice == '4':
                    break
                else:
                    print("Неправильный выбор. Попробуйте еще раз.")
    else:
        print("Неправильный выбор. Попробуйте еще раз.")