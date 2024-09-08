import json
import random
from time import sleep

import keyboard

from utils import clear_screen


class Word:
    """
    Класс для слова, который содержит само слово, сложность слова, категорию слова и подсказку к нему
    """
    def __init__(self, value='Значения нет',
                 level='Сложности нет',
                 category='Категории нет',
                 hint='Подсказки нет'):
        self.__value = value
        self.__level = level
        self.__category = category
        self.__hint = hint
        self.__length = len(self.__value)

    def to_dict(self):
        """
        Функция для перевода параметров слова к словарю для занесения в json файл
        :return: возвращает словарь параметров слова
        """
        return {
            'value': self.__value,
            'level': self.__level,
            'category': self.__category,
            'hint': self.__hint
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Функция обратная предыдущей, конвертирует из словаря в отдельные параметры
        :param data: словарь параметров
        :return: возвращает параметры для слова из словаря
        """
        return cls(
            data['value'],
            data['level'],
            data['category'],
            data['hint']
        )

    def get_value(self):
        return self.__value

    def get_level(self):
        return self.__level

    def get_category(self):
        return self.__category

    def get_hint(self):
        return self.__hint

    def get_length(self):
        return self.__length


class GameSession:
    def __init__(self, result_word, result_count):
        """
        :param self.users_answer: это слово, которое в данный момент получается у пользователя,
         изначально равняется '_' * длину загаданного слова
        :param self.users_count: это оставшиеся попытки у пользователя
        :param self.alphabet: это алфавит оставшихся букв для угадывания
        :param self.letter: это буква, которую ввел пользователь
        :param self.exit: это флаг проверяющий не вышел ли пользователь из игровой сессии
        :param self.hint: это флаг, проверяющий взял ли пользователь подсказку
        :param result_word: это объект класса Word, который был выбран в MainMenu для данной игровой сессии
        :param result_count: это количество попыток, которые были выбраны или зарандомлены в MainMenu
        """
        self.word: Word = result_word
        self.users_answer: str = '_' * self.word.get_length()
        self.count_of_tries: int = result_count
        self.users_count: int = result_count
        self.alphabet: str = ''.join([chr(code) for code in range(ord('а'), ord('я') + 1)])
        self.letter = ''
        self.hint = False
        self.exit = False

    def show(self) -> None:
        """
        Функция отрисовывающая всю игровую сессию
        :return: None
        """
        while not self.exit:
            clear_screen()
            self.print_hangman()
            self.print_count_of_tries()
            self.print_fields()
            self.print_word()
            self.print_hint()
            self.print_alphabet()
            self.get_hint()
            self.get_input()
            if not self.exit:
                self.get_exit()

    def end(self) -> None:
        """
        Функция завершающая игру
        :return: None
        """
        if self.users_count == 0:
            clear_screen()
            print('Вы проиграли ;(')
            sleep(3)
            self.exit = True
        else:
            clear_screen()
            print('Вы выиграли!!!')
            sleep(3)
            self.exit = True

    def print_count_of_tries(self) -> None:
        print('Кол-во оставшихся попыток: ', self.users_count, '\n')

    def print_fields(self) -> None:
        print('Сложность: ', self.word.get_level(), '\n')
        print('Категория: ', self.word.get_category(), '\n')

    def print_word(self) -> None:
        print('Слово: ', self.users_answer + '\n')

    def print_hint(self) -> None:
        """
        Пишет подсказку
        :return: None
        """
        if self.hint:
            print('Подсказка: ', self.word.get_hint(), '\n')
        else:
            print('Подсказка: ___\n')

    def print_alphabet(self) -> None:
        print('Оставшиеся буквы: ', self.alphabet, '\n')

    def get_hint(self) -> None:
        """
        Проверяет нужно ли давать подсказку
        :return: None
        """
        if not self.hint:
            if input('Чтобы показать подсказку напишите Y: ').lower() == 'y':
                self.hint = True

    def get_exit(self) -> None:
        """
        Проверяет нужно ли выходить из игровой сессии
        :return: None
        """
        if input('Чтобы выйти из игры напишите "выход": ').lower() == 'выход':
            self.exit = True

    def get_input(self) -> None:
        """
        Принимает букву пользователя, а также возвращает ошибку, при некорректности ввода
        :return: None
        """
        try:
            self.letter = input('Введите букву: ').lower()
            if len(self.letter) == 1:
                if self.letter in self.alphabet:
                    self.check_answer()
                else:
                    print('Буква должна быть в алфавите')
            else:
                print('Символ должен быть длины 1')
        except ValueError:
            print('Вводите букву!')

    def check_answer(self) -> None:
        """
        Вызывается, если была введена корректная буква, проверяет есть ли буква в слове и меняет self.users_answer,
        а также вызывает конец игры, если кончились попытки или слово было угадано
        :return: None
        """
        self.alphabet = self.alphabet.replace(self.letter, '_')
        if self.letter in self.word.get_value():
            indexes = [ind for ind, letter in enumerate(list(self.word.get_value())) if letter == self.letter]
            for i in indexes:
                self.users_answer = self.users_answer[:i] + self.letter + self.users_answer[i + 1:]
            if self.users_answer == self.word.get_value():
                self.end()
        else:
            self.users_count -= 1
            if self.users_count == 0:
                self.end()

    def print_hangman(self) -> None:
        """
        Печатает виселицу, в зависимости от оставшихся попыток пользователя
        :return: None
        """
        stages = [
            """
                -----
                |   |
                |
                |
                |
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |
                |
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |   |
                |
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|
                |
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |  /
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |  / \\
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |   |
                |  / \\
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |   |
                |   |
                |  / \\
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |   |
                |   |
                |   |
                |  / \\
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |   |
                |   |
                |   |
                |   |
                |  / \\
                |
                |
            """
        ]
        print(stages[self.count_of_tries - self.users_count] + '\n')



class Menu:
    """
    Родительский класс для всех меню
    :param options: для каждой меню принимает разные значения,
     это кнопки в меню, по которым передвигается пользователь
    :param exit: флаг, проверяющий вышел ли пользователь из меню
    :param selected_index: это индекс определяющий на какой кнопке меню сейчас стрелка
    """
    options: list
    exit = False
    selected_index: int = 0

    def exit_menu(self) -> None:
        self.exit = True

    def print_menu(self) -> None:
        """
        Чистит экран с помощью clear_screen() и рисует кнопки меню из options и стрелку напротив соответствующей кнопки
        :return: None
        """
        clear_screen()
        print("Выберите опцию:")
        for i, option in enumerate(self.options):
            if i == self.selected_index:
                print(f"> {option}")
            else:
                print(f"  {option}")

    def handle_key(self, key):
        """
        С помощью библиотеки keyboard отлавливает какая кнопка на клавиатуре была нажата
        :param key: значение клавиши
        :return: None
        """
        if key == 'enter':
            return 'enter'
        elif key == 'up':  # Up arrow
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif key == 'down':  # Down arrow
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif key == 'esc':
            self.exit = True
        return None


class MainMenu(Menu):
    """
    Основное меню
    :param LIST_OF_WORDS: список из объектов слов
    """
    options: list = ['Начать игру',
                     'Зарандомить',
                     'Выбрать категорию',
                     'Выбрать сложность',
                     'Выбрать количество попыток',
                     'Добавить слово',
                     'Удалить слово',
                     'Выйти']
    LIST_OF_WORDS = []
    LIST_OF_CATEGORIES = []
    LIST_OF_LEVELS = []

    def __init__(self, filename: str = 'word_list.json'):
        """
        :param filename: json файл, из которого берутся слова.
        :param self.users_category, self.users_level, self.users_count: параметры категории,
         уровня сложности и количество попыток, которые выбрал пользователь.
        :param self.choice_category_flag, self.choice_level_flag, self.choice_count_flag: флаги,
         которые означают какой параметр пользователь поменял сам,
          а какой нужно будет зарандомить при создании игровой сессии
        """
        self.users_category: str
        self.users_level: str
        self.users_count: int
        self.choice_category_flag: bool = False
        self.choice_level_flag: bool = False
        self.choice_count_flag: bool = False
        self.filename = filename

    def start_game(self):
        """
        Рандомит слово перед игрой
        :return: итоговое слово для игры и количество попыток
        """
        self.random_fields()
        filtered_words = self.filter_words()
        result_word = ''
        try:
            result_word = random.choice(filtered_words)
        except IndexError:
            self.exit_menu()
            # print('json файл пуст')
        try:
            return result_word, self.users_count
        except AttributeError:
            self.exit_menu()
            # print('json файл пуст')

    def filter_words(self):
        """
        Подбирает список слов соответствующие, выбранным сложности и категории
        :return: список слов
        """
        return [word
                for word in self.LIST_OF_WORDS
                if word.get_category() == self.users_category and
                word.get_level() == self.users_level]

    def choice_category(self, new_category) -> None:
        """
        Меняет категорию с рандомной на выбранную и меняет флаг выбора категории
        :param new_category: выбранная в меню категорий категория
        :return: None
        """
        self.users_category = new_category
        self.choice_category_flag = True

    def choice_level(self, new_level) -> None:
        """
        Меняет уровень сложности с рандомного на выбранный и меняет флаг выбора категории,
         а также если после выбора категории и сложности соответствующего слова не оказалось в json файле,
          то он подбирает рандомную категорию для слова, сложность оставляют ту же
        :param new_level: выбранный в меню уровней сложности уровень
        :return: None
        """
        self.users_level = new_level
        if len(self.filter_words()) == 0:
            self.choice_category_flag = False
            self.random_fields()
        self.choice_level_flag = True

    def choice_count_of_tries(self, new_count) -> None:
        self.users_count = new_count
        self.choice_count_flag = True

    def add_word(self) -> None:
        """
        Функция для добавления слова в json файл,
         в случае удачи вызывает функцию create_and_add_word и возвращается в главное меню
        :return: None
        """
        clear_screen()
        print("Введите: слово, уровень сложности, категорию для этого слова, подсказку."
              " Разделяя ', '. Для того чтобы вернуться нажмите 'enter+esc'\n")
        sleep(0.15)
        while True:
            args = input().split(', ')
            if len(args) == 4 and args[0] not in [word.get_value() for word in self.LIST_OF_WORDS]:
                self.create_and_add_word(args[0].lower(), args[1].lower(), args[2].lower(), args[3].lower())
                break
            else:
                print('Вы где-то допустили ошибку!\n')
                if keyboard.is_pressed('esc'):
                    break

    def delete_word(self, value) -> None:
        """
        Функция удаления слова из json файла
        :param value: слово, которое пользователь выбрал в меню удаления
        :return: None
        """
        self.LIST_OF_WORDS = [word for word in self.LIST_OF_WORDS if word.get_value() != value]
        self.save_words()

    def create_and_add_word(self, value, level, category, hint) -> None:
        """
        Создаем объект слова и добавляем его в список, а также вызывает save_words()
        :param value:
        :param level:
        :param category:
        :param hint:
        :return: None
        """
        word = Word(value, level, category, hint)
        self.LIST_OF_WORDS.append(word)
        self.save_words()

    def save_words(self) -> None:
        """
        Функция, которая сохраняет изменения в json файле, а также вызывает refresh_lists()
        :return:
        """
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([word.to_dict() for word in self.LIST_OF_WORDS], f, ensure_ascii=False, indent=4)
        self.refresh_lists()

    def load_words(self) -> None:
        """
        Функция подгружает слова из json файла в LIST_OF_WORDS,
         в случае неудачи печатает сообщение об ошибке и завершает работу меню
        :return:
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.LIST_OF_WORDS = [Word.from_dict(data) for data in json.load(f)]
        except FileNotFoundError:
            self.exit_menu()
            print('Файл не найден')
        except KeyError:
            self.exit_menu()
            print('В json файле некорректные данные')
        except json.decoder.JSONDecodeError:
            self.exit_menu()
            print('json файл некорректен')

    def refresh_lists(self) -> None:
        """
        Обновляет списки с уровнями и категориями, в соответствии с текущим LIST_OF_WORDS
        :return:
        """
        self.LIST_OF_LEVELS = list(set([word.get_level() for word in self.LIST_OF_WORDS]))
        self.LIST_OF_CATEGORIES = list(set([word.get_category() for word in self.LIST_OF_WORDS]))

    def random_fields(self) -> None:
        """
        Если пользователь не выбирал параметры слова, то просто их рандомит
        :return: None
        """
        self.refresh_lists()
        try:
            if not self.choice_level_flag:
                self.users_level = random.choice(self.LIST_OF_LEVELS)
            if not self.choice_category_flag:
                self.users_category = random.choice([word.get_category()
                                                     for word in self.LIST_OF_WORDS
                                                     if word.get_level() == self.users_level])
            if not self.choice_count_flag:
                self.users_count = random.randint(6, 10)
        except IndexError:
            self.exit_menu()
            print('В json файле недостаточно слов')

    def reset_fields(self) -> None:
        """
        Обнавляет флаги изменения параметров слова, обычно вызывается после окончания игровой сессии
        :return: None
        """
        self.choice_category_flag = False
        self.choice_level_flag = False
        self.choice_count_flag = False


class CategoryMenu(Menu):
    """
    Меню для выбора категории, наследуется от Menu
    """
    options: list

    def get_list_from_main_menu(self, main_menu: MainMenu) -> None:
        """
        Принимает экземлпяр MainMenu и заполняет список категорий,
         в соответствии с актуальными данными из LIST_OF_WORDS
        :param main_menu:
        :return: None
        """
        self.options = [word.get_category()
                        for word in main_menu.LIST_OF_WORDS
                        if word.get_level() == main_menu.users_level]


class LevelMenu(Menu):
    """
    Меню для выбора сложности игры
    """
    options: list

    def get_list_from_main_menu(self, main_menu: MainMenu) -> None:
        """
        Принимает экземпляр MainMenu и заполняет список уровней в соответствии с актуальными данными из LIST_OF_LEVELS
        :param main_menu:
        :return: None
        """
        self.options = main_menu.LIST_OF_LEVELS


class DeleteMenu(Menu):
    """
    Меню для выбора слова для удаления
    """
    options: list
    def get_list_from_main_menu(self, main_menu: MainMenu):
        """
        Заполняет список слов для удаления
        :param main_menu:
        :return: None
        """
        self.options = [word.get_value() for word in main_menu.LIST_OF_WORDS]
